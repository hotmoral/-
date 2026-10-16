package com.receiptledger.v1.devicevalidation;

import com.receiptledger.v1.BuildConfig;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.review.CaptureReviewAssessmentV2;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/**
 * CP37 local-only validation projection. It intentionally emits structural metrics only and never
 * serializes receipt text, IDs, dates, stores, item names, prices, or OCR content.
 */
public final class DeviceValidationReportV1 {
    public enum AcquisitionSource { CAMERA, GALLERY, UNKNOWN }

    public static final class InitialSnapshot {
        private final AcquisitionSource source;
        private final long ocrMillis;
        private final int attemptedPasses;
        private final int mergedCandidates;
        private final String bestPass;
        private final ReceiptRecord record;
        private final CaptureReviewAssessmentV2 assessment;

        private InitialSnapshot(
                AcquisitionSource source,
                long ocrMillis,
                int attemptedPasses,
                int mergedCandidates,
                String bestPass,
                ReceiptRecord record,
                CaptureReviewAssessmentV2 assessment) {
            this.source = source;
            this.ocrMillis = ocrMillis;
            this.attemptedPasses = attemptedPasses;
            this.mergedCandidates = mergedCandidates;
            this.bestPass = bestPass;
            this.record = record;
            this.assessment = assessment;
        }
    }

    private static final class Delta {
        int storeChanged;
        int dateChanged;
        int totalChanged;
        int discountChanged;
        int itemCountChanged;
        int itemStructureChanges;
        int itemNameChanges;
        int itemQuantityChanges;
        int itemUnitPriceChanges;
        int itemLineAmountChanges;
        final Set<Integer> correctedItemOrdinals = new LinkedHashSet<>();

        boolean anyCorrection() {
            return storeChanged != 0
                    || dateChanged != 0
                    || totalChanged != 0
                    || discountChanged != 0
                    || itemCountChanged != 0
                    || itemStructureChanges != 0
                    || itemNameChanges != 0
                    || itemQuantityChanges != 0
                    || itemUnitPriceChanges != 0
                    || itemLineAmountChanges != 0;
        }
    }

    private DeviceValidationReportV1() {}

    public static InitialSnapshot captureInitial(
            AcquisitionSource source,
            long ocrMillis,
            int attemptedPasses,
            int mergedCandidates,
            String bestPass,
            ReceiptRecord record,
            CaptureReviewAssessmentV2 assessment) {
        if (!BuildConfig.DEBUG) return null;
        if (record == null || assessment == null) throw new IllegalArgumentException("initial validation state");
        if (ocrMillis < 0 || attemptedPasses < 0 || mergedCandidates < 0) {
            throw new IllegalArgumentException("validation metrics");
        }
        return new InitialSnapshot(
                source == null ? AcquisitionSource.UNKNOWN : source,
                ocrMillis,
                attemptedPasses,
                mergedCandidates,
                token(bestPass),
                record,
                assessment);
    }

    public static String savedReport(InitialSnapshot initial, ReceiptRecord finalRecord) {
        if (initial == null || finalRecord == null) throw new IllegalArgumentException("saved validation state");
        Delta delta = compare(initial.record, finalRecord);
        int anyCorrection = delta.anyCorrection() ? 1 : 0;
        int falseAutoConfirm = initial.assessment.decision == CaptureReviewAssessmentV2.Decision.AUTO_CONFIRMED
                && delta.anyCorrection() ? 1 : 0;
        int correctionsOutsideReviewItems = correctionsOutsideReviewItems(initial.assessment, delta);
        int reviewScopeMiss = correctionsOutsideReviewItems > 0 ? 1 : 0;

        StringBuilder out = new StringBuilder(640);
        out.append("RL_CP37_SAMPLE")
                .append(" version=2")
                .append(" source=").append(initial.source.name())
                .append(" image_w=").append(initial.record.sourceWidth)
                .append(" image_h=").append(initial.record.sourceHeight)
                .append(" perspective=").append(initial.record.perspectiveCorrected ? 1 : 0)
                .append(" ocr_ms=").append(initial.ocrMillis)
                .append(" attempted_passes=").append(initial.attemptedPasses)
                .append(" merged_candidates=").append(initial.mergedCandidates)
                .append(" best_pass=").append(initial.bestPass)
                .append(" initial_validation=").append(initial.record.validationStatus.name())
                .append(" initial_decision=").append(initial.assessment.decision.name())
                .append(" initial_items=").append(initial.record.items.size())
                .append(" initial_review_items=").append(initial.assessment.reviewItemCount())
                .append(" initial_review_fields=").append(initial.assessment.receiptFields.size())
                .append(" store_changed=").append(delta.storeChanged)
                .append(" date_changed=").append(delta.dateChanged)
                .append(" total_changed=").append(delta.totalChanged)
                .append(" discount_changed=").append(delta.discountChanged)
                .append(" item_count_changed=").append(delta.itemCountChanged)
                .append(" item_structure_changes=").append(delta.itemStructureChanges)
                .append(" item_name_changes=").append(delta.itemNameChanges)
                .append(" item_quantity_changes=").append(delta.itemQuantityChanges)
                .append(" item_unit_price_changes=").append(delta.itemUnitPriceChanges)
                .append(" item_line_amount_changes=").append(delta.itemLineAmountChanges)
                .append(" corrections_outside_review_items=").append(correctionsOutsideReviewItems)
                .append(" review_scope_miss=").append(reviewScopeMiss)
                .append(" any_correction=").append(anyCorrection)
                .append(" false_auto_confirm=").append(falseAutoConfirm)
                .append(" final_validation=").append(finalRecord.validationStatus.name())
                .append(" saved=1");
        return out.toString();
    }

    private static Delta compare(ReceiptRecord initial, ReceiptRecord finalRecord) {
        Delta out = new Delta();
        out.storeChanged = changed(initial.storeName, finalRecord.storeName);
        out.dateChanged = changed(initial.purchaseDate, finalRecord.purchaseDate);
        out.totalChanged = changed(initial.printedTotal, finalRecord.printedTotal);
        out.discountChanged = changed(initial.discountSum, finalRecord.discountSum);
        out.itemCountChanged = initial.items.size() == finalRecord.items.size() ? 0 : 1;

        Map<Integer, PersistedItem> before = byOrdinal(initial);
        Map<Integer, PersistedItem> after = byOrdinal(finalRecord);
        for (Map.Entry<Integer, PersistedItem> entry : before.entrySet()) {
            PersistedItem other = after.get(entry.getKey());
            if (other == null) {
                out.itemStructureChanges++;
                out.correctedItemOrdinals.add(entry.getKey());
                continue;
            }
            PersistedItem item = entry.getValue();
            int nameChanged = changed(item.name, other.name);
            int quantityChanged = changed(item.quantity, other.quantity);
            int unitPriceChanged = changed(item.unitPrice, other.unitPrice);
            int lineAmountChanged = changed(item.lineAmount, other.lineAmount);
            out.itemNameChanges += nameChanged;
            out.itemQuantityChanges += quantityChanged;
            out.itemUnitPriceChanges += unitPriceChanged;
            out.itemLineAmountChanges += lineAmountChanged;
            if (nameChanged != 0 || quantityChanged != 0 || unitPriceChanged != 0 || lineAmountChanged != 0) {
                out.correctedItemOrdinals.add(entry.getKey());
            }
        }
        for (Integer ordinal : after.keySet()) {
            if (!before.containsKey(ordinal)) {
                out.itemStructureChanges++;
                out.correctedItemOrdinals.add(ordinal);
            }
        }
        return out;
    }

    private static int correctionsOutsideReviewItems(CaptureReviewAssessmentV2 assessment, Delta delta) {
        Set<Integer> initialReviewOrdinals = new HashSet<>(assessment.itemOrdinals);
        int out = 0;
        for (Integer ordinal : delta.correctedItemOrdinals) {
            if (!initialReviewOrdinals.contains(ordinal)) out++;
        }
        return out;
    }

    private static Map<Integer, PersistedItem> byOrdinal(ReceiptRecord record) {
        Map<Integer, PersistedItem> out = new HashMap<>();
        for (PersistedItem item : record.items) out.put(item.ordinal, item);
        return out;
    }

    private static int changed(Object before, Object after) {
        return Objects.equals(before, after) ? 0 : 1;
    }

    private static String token(String value) {
        if (value == null || value.isEmpty()) return "UNKNOWN";
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            boolean ok = (c >= 'A' && c <= 'Z') || c == '_' || (c >= '0' && c <= '9');
            if (!ok) return "UNKNOWN";
        }
        return value;
    }
}
