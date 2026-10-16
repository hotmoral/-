package com.receiptledger.v1.review;

import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.validation.ValidationStatus;
import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/** Deterministic CP33 projection deciding what still needs explicit user review. */
public final class CaptureReviewAssessmentV2 {
    public enum Decision { AUTO_CONFIRMED, REVIEW_REQUIRED }
    public enum ReceiptField { STORE, PURCHASE_DATE, PRINTED_TOTAL, DISCOUNT_SUM }

    public final Decision decision;
    public final Set<ReceiptField> receiptFields;
    public final List<Integer> itemOrdinals;
    public final List<String> reasons;
    public final int autoConfirmedItems;

    private CaptureReviewAssessmentV2(
            Decision decision,
            Set<ReceiptField> receiptFields,
            List<Integer> itemOrdinals,
            List<String> reasons,
            int autoConfirmedItems) {
        this.decision = decision;
        this.receiptFields = Collections.unmodifiableSet(new LinkedHashSet<>(receiptFields));
        this.itemOrdinals = Collections.unmodifiableList(new ArrayList<>(itemOrdinals));
        this.reasons = Collections.unmodifiableList(new ArrayList<>(reasons));
        this.autoConfirmedItems = autoConfirmedItems;
    }

    public static CaptureReviewAssessmentV2 assess(ReceiptRecord record) {
        if (record == null) throw new IllegalArgumentException("record");
        EnumSet<ReceiptField> fields = EnumSet.noneOf(ReceiptField.class);
        LinkedHashSet<Integer> flagged = new LinkedHashSet<>();
        LinkedHashSet<String> reasons = new LinkedHashSet<>();

        if (blank(record.storeName)) {
            fields.add(ReceiptField.STORE);
            reasons.add("STORE_MISSING");
        }
        if (blank(record.purchaseDate)) {
            fields.add(ReceiptField.PURCHASE_DATE);
            reasons.add("PURCHASE_DATE_MISSING");
        }
        if (record.printedTotal == null) {
            fields.add(ReceiptField.PRINTED_TOTAL);
            reasons.add("PRINTED_TOTAL_MISSING");
        }
        if (record.items.isEmpty()) reasons.add("NO_ITEMS");

        for (PersistedItem item : record.items) {
            if (itemNeedsReview(record, item)) {
                flagged.add(item.ordinal);
                reasons.add("ITEM_REVIEW_REQUIRED:" + item.ordinal);
            }
        }

        boolean safeValidation = record.validationStatus == ValidationStatus.PASS
                || (record.validationStatus == ValidationStatus.PASS_WITH_WARNINGS
                    && onlyUserProvenanceIssues(record.issues));

        if (record.validationStatus == ValidationStatus.MISMATCH) {
            fields.add(ReceiptField.PRINTED_TOTAL);
            fields.add(ReceiptField.DISCOUNT_SUM);
            flagAll(record, flagged);
            reasons.add("RECEIPT_TOTAL_MISMATCH");
        } else if (record.validationStatus == ValidationStatus.INCOMPLETE) {
            reasons.add("RECEIPT_INCOMPLETE");
        } else if (!safeValidation) {
            reasons.add("RECEIPT_WARNING_REQUIRES_REVIEW");
        }

        if (!safeValidation && fields.isEmpty() && flagged.isEmpty() && !record.items.isEmpty()) {
            fields.add(ReceiptField.PRINTED_TOTAL);
            fields.add(ReceiptField.DISCOUNT_SUM);
            flagAll(record, flagged);
        }

        boolean requires = !fields.isEmpty() || !flagged.isEmpty() || !safeValidation || record.items.isEmpty();
        int autoCount = Math.max(0, record.items.size() - flagged.size());
        return new CaptureReviewAssessmentV2(
                requires ? Decision.REVIEW_REQUIRED : Decision.AUTO_CONFIRMED,
                fields,
                new ArrayList<>(flagged),
                new ArrayList<>(reasons),
                autoCount);
    }

    public boolean requiresReview() {
        return decision == Decision.REVIEW_REQUIRED;
    }

    public boolean flags(ReceiptField field) {
        return receiptFields.contains(field);
    }

    public boolean flagsItem(int ordinal) {
        return itemOrdinals.contains(ordinal);
    }

    public int reviewItemCount() {
        return itemOrdinals.size();
    }

    private static boolean itemNeedsReview(ReceiptRecord record, PersistedItem item) {
        if (item == null) return true;
        if (blank(item.name) || item.lineAmount == null) return true;
        if (item.quantity == null || item.quantity <= 0) return true;
        if (item.resolution == ItemResolution.PARTIAL) return true;
        if (item.quantityOrigin == ValueOrigin.UNKNOWN
                || item.unitPriceOrigin == ValueOrigin.UNKNOWN
                || item.lineAmountOrigin == ValueOrigin.UNKNOWN) return true;
        if (item.quantityOrigin == ValueOrigin.DEFAULT_ONE
                && !hasIssue(record.issues, "USER_CONFIRMED_DEFAULT_ONE:" + item.ordinal)) return true;
        return false;
    }

    private static boolean onlyUserProvenanceIssues(List<String> issues) {
        if (issues == null || issues.isEmpty()) return false;
        for (String issue : issues) {
            if (issue == null) return false;
            if (!issue.startsWith("USER_EDITED_")
                    && !issue.startsWith("USER_CONFIRMED_")
                    && !issue.startsWith("USER_REMOVED_")) return false;
        }
        return true;
    }

    private static boolean hasIssue(List<String> issues, String exact) {
        if (issues == null) return false;
        for (String issue : issues) if (exact.equals(issue)) return true;
        return false;
    }

    private static void flagAll(ReceiptRecord record, Set<Integer> out) {
        for (PersistedItem item : record.items) out.add(item.ordinal);
    }

    private static boolean blank(String value) {
        return value == null || value.trim().isEmpty();
    }
}
