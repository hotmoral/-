package com.receiptledger.v1.devicevalidation;

import static org.junit.Assert.*;

import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.review.CaptureReviewAssessmentV2;
import com.receiptledger.v1.validation.ValidationStatus;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Test;

public final class DeviceValidationReportV1Test {

    @Test public void unchangedAutoConfirmedSampleHasNoCorrectionAndNoPrivateValues() {
        ReceiptRecord initial = record(
                "PRIVATE_RECEIPT_ID",
                "2099-12-31",
                "PRIVATE_STORE_XYZ",
                987654L,
                item(0, "SECRET_ITEM_ABC", 2, 493827L, 987654L, ValueOrigin.PRINTED),
                Collections.emptyList());
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(initial);
        assertEquals(CaptureReviewAssessmentV2.Decision.AUTO_CONFIRMED, assessment.decision);

        DeviceValidationReportV1.InitialSnapshot snapshot = DeviceValidationReportV1.captureInitial(
                DeviceValidationReportV1.AcquisitionSource.GALLERY,
                1234,
                1,
                0,
                "ORIGINAL",
                initial,
                assessment);
        String report = DeviceValidationReportV1.savedReport(snapshot, initial);

        assertTrue(report.startsWith("RL_CP37_SAMPLE version=2 source=GALLERY"));
        assertTrue(report.contains("ocr_ms=1234"));
        assertTrue(report.contains("corrections_outside_review_items=0"));
        assertTrue(report.contains("review_scope_miss=0"));
        assertTrue(report.contains("any_correction=0"));
        assertTrue(report.contains("false_auto_confirm=0"));
        assertFalse(report.contains("PRIVATE_RECEIPT_ID"));
        assertFalse(report.contains("PRIVATE_STORE_XYZ"));
        assertFalse(report.contains("SECRET_ITEM_ABC"));
        assertFalse(report.contains("2099-12-31"));
        assertFalse(report.contains("987654"));
    }

    @Test public void correctionAfterAutoConfirmIsOneOutOfScopeItemEvenWithManyFieldChanges() {
        ReceiptRecord initial = record(
                "r1", "2026-10-01", "STORE_A", 3000L,
                item(0, "ITEM_A", 1, 3000L, 3000L, ValueOrigin.PRINTED),
                Collections.emptyList());
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(initial);
        assertEquals(CaptureReviewAssessmentV2.Decision.AUTO_CONFIRMED, assessment.decision);

        ReceiptRecord corrected = record(
                "r1", "2026-10-02", "STORE_B", 3200L,
                item(0, "ITEM_B", 2, 1600L, 3200L, ValueOrigin.USER_EDITED),
                Arrays.asList("USER_EDITED_STORE", "USER_EDITED_DATE"));
        String report = DeviceValidationReportV1.savedReport(
                DeviceValidationReportV1.captureInitial(
                        DeviceValidationReportV1.AcquisitionSource.CAMERA,
                        800,
                        2,
                        1,
                        "CONTRAST",
                        initial,
                        assessment),
                corrected);

        assertTrue(report.contains("store_changed=1"));
        assertTrue(report.contains("date_changed=1"));
        assertTrue(report.contains("total_changed=1"));
        assertTrue(report.contains("item_name_changes=1"));
        assertTrue(report.contains("item_quantity_changes=1"));
        assertTrue(report.contains("item_unit_price_changes=1"));
        assertTrue(report.contains("item_line_amount_changes=1"));
        assertTrue(report.contains("corrections_outside_review_items=1"));
        assertTrue(report.contains("review_scope_miss=1"));
        assertTrue(report.contains("any_correction=1"));
        assertTrue(report.contains("false_auto_confirm=1"));
    }

    @Test public void conservativeReviewWithUnchangedConfirmedDefaultHasNoScopeMiss() {
        ReceiptRecord initial = record(
                "r2", "2026-10-01", "STORE", 2000L,
                item(0, "ITEM", 1, 2000L, 2000L, ValueOrigin.DEFAULT_ONE),
                Collections.emptyList());
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(initial);
        assertEquals(CaptureReviewAssessmentV2.Decision.REVIEW_REQUIRED, assessment.decision);

        ReceiptRecord confirmed = record(
                "r2", "2026-10-01", "STORE", 2000L,
                item(0, "ITEM", 1, 2000L, 2000L, ValueOrigin.DEFAULT_ONE),
                Collections.singletonList("USER_CONFIRMED_DEFAULT_ONE:0"));
        String report = DeviceValidationReportV1.savedReport(
                DeviceValidationReportV1.captureInitial(
                        DeviceValidationReportV1.AcquisitionSource.GALLERY,
                        1500,
                        1,
                        0,
                        "ORIGINAL",
                        initial,
                        assessment),
                confirmed);

        assertTrue(report.contains("initial_decision=REVIEW_REQUIRED"));
        assertTrue(report.contains("initial_review_items=1"));
        assertTrue(report.contains("corrections_outside_review_items=0"));
        assertTrue(report.contains("review_scope_miss=0"));
        assertTrue(report.contains("any_correction=0"));
        assertTrue(report.contains("false_auto_confirm=0"));
    }

    @Test public void itemStructureReplacementCountsBothOutOfScopeOrdinalsWithoutSerializingItems() {
        ReceiptRecord initial = record(
                "r3", "2026-10-01", "S", 1000L,
                item(0, "PRIVATE_OLD_ITEM", 1, 1000L, 1000L, ValueOrigin.PRINTED),
                Collections.emptyList());
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(initial);
        PersistedItem replacement = new PersistedItem(
                1, 1, "PRIVATE_NEW_ITEM", 1, 1000L, 1000L,
                ValueOrigin.USER_EDITED, ValueOrigin.USER_EDITED, ValueOrigin.USER_EDITED,
                ItemResolution.EXACT, null);
        ReceiptRecord finalRecord = new ReceiptRecord(
                "r3", 1L, "2026-10-01", "S", "PRIVATE_RAW_OCR",
                1000L, 1000L, 0L, 1000L, 0L, ValidationStatus.PASS,
                1800, 2400, false, Collections.emptyList(), Collections.singletonList(replacement));

        String report = DeviceValidationReportV1.savedReport(
                DeviceValidationReportV1.captureInitial(
                        DeviceValidationReportV1.AcquisitionSource.UNKNOWN,
                        999,
                        3,
                        1,
                        "BINARY",
                        initial,
                        assessment),
                finalRecord);

        assertTrue(report.contains("item_count_changed=0"));
        assertTrue(report.contains("item_structure_changes=2"));
        assertTrue(report.contains("corrections_outside_review_items=2"));
        assertTrue(report.contains("review_scope_miss=1"));
        assertTrue(report.contains("any_correction=1"));
        assertTrue(report.contains("false_auto_confirm=1"));
        assertFalse(report.contains("PRIVATE_OLD_ITEM"));
        assertFalse(report.contains("PRIVATE_NEW_ITEM"));
        assertFalse(report.contains("PRIVATE_RAW_OCR"));
    }

    @Test public void removedFalseItemAlreadyInsideMismatchReviewScopeIsNotScopeMiss() {
        PersistedItem falseItem = item(0, "PRIVATE_ADDRESS_ROW", 1, 1234L, 1234L, ValueOrigin.DEFAULT_ONE);
        PersistedItem realItem = item(1, "PRIVATE_REAL_ITEM", 1, 4500L, 4500L, ValueOrigin.PRINTED);
        ReceiptRecord initial = recordWithItems(
                "r4", 4500L, 5734L, 1234L, ValidationStatus.MISMATCH,
                Collections.singletonList("RECEIPT_TOTAL_MISMATCH:1234"), Arrays.asList(falseItem, realItem));
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(initial);
        assertTrue(assessment.flagsItem(0));
        assertTrue(assessment.flagsItem(1));
        ReceiptRecord corrected = recordWithItems(
                "r4", 4500L, 4500L, 0L, ValidationStatus.PASS_WITH_WARNINGS,
                Collections.singletonList("USER_REMOVED_ITEM:0"), Collections.singletonList(realItem));

        String report = DeviceValidationReportV1.savedReport(
                DeviceValidationReportV1.captureInitial(
                        DeviceValidationReportV1.AcquisitionSource.GALLERY,
                        600,
                        3,
                        2,
                        "ORIGINAL",
                        initial,
                        assessment),
                corrected);

        assertTrue(report.contains("item_count_changed=1"));
        assertTrue(report.contains("item_structure_changes=1"));
        assertTrue(report.contains("corrections_outside_review_items=0"));
        assertTrue(report.contains("review_scope_miss=0"));
        assertTrue(report.contains("any_correction=1"));
        assertTrue(report.contains("false_auto_confirm=0"));
        assertFalse(report.contains("PRIVATE_ADDRESS_ROW"));
        assertFalse(report.contains("PRIVATE_REAL_ITEM"));
    }

    @Test public void reviewRequiredSampleDetectsCorrectionOutsideSelectedItemScope() {
        PersistedItem flagged = item(0, "PRIVATE_FLAGGED", 1, 1000L, 1000L, ValueOrigin.DEFAULT_ONE);
        PersistedItem unflagged = item(1, "PRIVATE_UNFLAGGED", 1, 4000L, 4000L, ValueOrigin.PRINTED);
        ReceiptRecord initial = recordWithItems(
                "r5", 5000L, 5000L, 0L, ValidationStatus.PASS,
                Collections.emptyList(), Arrays.asList(flagged, unflagged));
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(initial);
        assertEquals(CaptureReviewAssessmentV2.Decision.REVIEW_REQUIRED, assessment.decision);
        assertEquals(Collections.singletonList(0), assessment.itemOrdinals);

        PersistedItem correctedUnflagged = new PersistedItem(
                1, 1, "PRIVATE_CORRECTED", 2, 2000L, 4000L,
                ValueOrigin.USER_EDITED, ValueOrigin.USER_EDITED, ValueOrigin.PRINTED,
                ItemResolution.EXACT, null);
        ReceiptRecord corrected = recordWithItems(
                "r5", 5000L, 5000L, 0L, ValidationStatus.PASS_WITH_WARNINGS,
                Arrays.asList("USER_CONFIRMED_DEFAULT_ONE:0", "USER_EDITED_ITEM:1"),
                Arrays.asList(flagged, correctedUnflagged));

        String report = DeviceValidationReportV1.savedReport(
                DeviceValidationReportV1.captureInitial(
                        DeviceValidationReportV1.AcquisitionSource.GALLERY,
                        500,
                        1,
                        0,
                        "ORIGINAL",
                        initial,
                        assessment),
                corrected);

        assertTrue(report.contains("initial_review_items=1"));
        assertTrue(report.contains("item_name_changes=1"));
        assertTrue(report.contains("item_quantity_changes=1"));
        assertTrue(report.contains("item_unit_price_changes=1"));
        assertTrue(report.contains("corrections_outside_review_items=1"));
        assertTrue(report.contains("review_scope_miss=1"));
        assertTrue(report.contains("false_auto_confirm=0"));
        assertFalse(report.contains("PRIVATE_FLAGGED"));
        assertFalse(report.contains("PRIVATE_UNFLAGGED"));
        assertFalse(report.contains("PRIVATE_CORRECTED"));
    }

    @Test public void correctionInsideSelectedItemScopeIsNotScopeMiss() {
        PersistedItem flagged = item(0, "PRIVATE_FLAGGED", 1, 1000L, 1000L, ValueOrigin.DEFAULT_ONE);
        PersistedItem unflagged = item(1, "PRIVATE_UNFLAGGED", 1, 4000L, 4000L, ValueOrigin.PRINTED);
        ReceiptRecord initial = recordWithItems(
                "r6", 5000L, 5000L, 0L, ValidationStatus.PASS,
                Collections.emptyList(), Arrays.asList(flagged, unflagged));
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(initial);
        assertEquals(Collections.singletonList(0), assessment.itemOrdinals);

        PersistedItem correctedFlagged = new PersistedItem(
                0, 0, "PRIVATE_FIXED_FLAGGED", 1, 1000L, 1000L,
                ValueOrigin.DEFAULT_ONE, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.EXACT, null);
        ReceiptRecord corrected = recordWithItems(
                "r6", 5000L, 5000L, 0L, ValidationStatus.PASS_WITH_WARNINGS,
                Collections.singletonList("USER_CONFIRMED_DEFAULT_ONE:0"),
                Arrays.asList(correctedFlagged, unflagged));

        String report = DeviceValidationReportV1.savedReport(
                DeviceValidationReportV1.captureInitial(
                        DeviceValidationReportV1.AcquisitionSource.GALLERY,
                        450,
                        1,
                        0,
                        "ORIGINAL",
                        initial,
                        assessment),
                corrected);

        assertTrue(report.contains("item_name_changes=1"));
        assertTrue(report.contains("corrections_outside_review_items=0"));
        assertTrue(report.contains("review_scope_miss=0"));
        assertTrue(report.contains("false_auto_confirm=0"));
    }

    @Test public void removalOutsideReviewScopeCountsOnce() {
        PersistedItem item = item(0, "PRIVATE_REMOVED", 1, 2500L, 2500L, ValueOrigin.PRINTED);
        ReceiptRecord initial = record(
                "r7", "2026-10-01", "S", 2500L, item, Collections.emptyList());
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(initial);
        assertEquals(CaptureReviewAssessmentV2.Decision.AUTO_CONFIRMED, assessment.decision);

        ReceiptRecord corrected = recordWithItems(
                "r7", 2500L, null, 0L, ValidationStatus.INCOMPLETE,
                Collections.singletonList("USER_REMOVED_ITEM:0"), Collections.emptyList());
        String report = DeviceValidationReportV1.savedReport(
                DeviceValidationReportV1.captureInitial(
                        DeviceValidationReportV1.AcquisitionSource.GALLERY,
                        400,
                        1,
                        0,
                        "ORIGINAL",
                        initial,
                        assessment),
                corrected);

        assertTrue(report.contains("item_count_changed=1"));
        assertTrue(report.contains("item_structure_changes=1"));
        assertTrue(report.contains("corrections_outside_review_items=1"));
        assertTrue(report.contains("review_scope_miss=1"));
        assertTrue(report.contains("false_auto_confirm=1"));
    }

    private static ReceiptRecord record(
            String id,
            String date,
            String store,
            Long total,
            PersistedItem item,
            List<String> issues) {
        return new ReceiptRecord(
                id,
                1L,
                date,
                store,
                "PRIVATE_RAW_TEXT",
                total,
                total,
                0L,
                total,
                0L,
                ValidationStatus.PASS,
                1800,
                2400,
                false,
                issues,
                Collections.singletonList(item));
    }

    private static ReceiptRecord recordWithItems(
            String id,
            Long printedTotal,
            Long itemLineSum,
            Long difference,
            ValidationStatus status,
            List<String> issues,
            List<PersistedItem> items) {
        return new ReceiptRecord(
                id,
                1L,
                "2026-10-01",
                "PRIVATE_STORE",
                "PRIVATE_RAW_TEXT",
                printedTotal,
                itemLineSum,
                0L,
                itemLineSum,
                difference,
                status,
                1800,
                2400,
                false,
                issues,
                items);
    }

    private static PersistedItem item(
            int ordinal,
            String name,
            Integer quantity,
            Long unitPrice,
            Long lineAmount,
            ValueOrigin quantityOrigin) {
        return new PersistedItem(
                ordinal,
                ordinal,
                name,
                quantity,
                unitPrice,
                lineAmount,
                quantityOrigin,
                ValueOrigin.PRINTED,
                ValueOrigin.PRINTED,
                ItemResolution.EXACT,
                null);
    }
}
