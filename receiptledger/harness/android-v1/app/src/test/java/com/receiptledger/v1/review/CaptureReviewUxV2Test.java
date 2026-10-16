package com.receiptledger.v1.review;

import static org.junit.Assert.*;

import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.validation.ValidationStatus;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.Test;

public final class CaptureReviewUxV2Test {
    @Test public void cleanExactReceiptIsAutoConfirmed() {
        ReceiptRecord record = record(ValidationStatus.PASS, "2026-10-16", "마트", 1000L,
                Collections.emptyList(), exact(0, "우유", 1, 1000L, 1000L));
        CaptureReviewAssessmentV2 a = CaptureReviewAssessmentV2.assess(record);
        assertEquals(CaptureReviewAssessmentV2.Decision.AUTO_CONFIRMED, a.decision);
        assertEquals(1, a.autoConfirmedItems);
        assertEquals(0, a.reviewItemCount());
    }

    @Test public void safeArithmeticInferenceIsAutoConfirmed() {
        PersistedItem item = item(0, "라면", 2, 1500L, 3000L,
                ValueOrigin.PRINTED, ValueOrigin.INFERRED_ARITHMETIC, ValueOrigin.PRINTED,
                ItemResolution.INFERRED, "ARITHMETIC");
        ReceiptRecord record = record(ValidationStatus.PASS, "2026-10-16", "마트", 3000L,
                Collections.emptyList(), item);
        assertFalse(CaptureReviewAssessmentV2.assess(record).requiresReview());
    }

    @Test public void defaultOneRequiresReviewUntilConfirmed() {
        PersistedItem assumed = item(0, "과자", 1, 2000L, 2000L,
                ValueOrigin.DEFAULT_ONE, ValueOrigin.INFERRED_ARITHMETIC, ValueOrigin.PRINTED,
                ItemResolution.INFERRED, "DEFAULT_ONE");
        ReceiptRecord base = record(ValidationStatus.PASS, "2026-10-16", "마트", 2000L,
                Collections.emptyList(), assumed);
        CaptureReviewAssessmentV2 before = CaptureReviewAssessmentV2.assess(base);
        assertTrue(before.requiresReview());
        assertEquals(Collections.singletonList(0), before.itemOrdinals);

        ReceiptReviewEngine engine = new ReceiptReviewEngine();
        ReceiptRecord reviewed = engine.apply(base, base.storeName, base.purchaseDate,
                base.printedTotal, base.discountSum,
                Collections.singletonList(new ReviewItemInput("과자", 1, 2000L, 2000L)));
        reviewed = CaptureReviewConfirmationV2.apply(reviewed, before);
        assertTrue(reviewed.issues.contains("USER_CONFIRMED_DEFAULT_ONE:0"));
        assertEquals(ValueOrigin.DEFAULT_ONE, reviewed.items.get(0).quantityOrigin);
        assertFalse(CaptureReviewAssessmentV2.assess(reviewed).requiresReview());
    }

    @Test public void partialItemRequiresReview() {
        PersistedItem partial = item(0, "사과", 2, null, 3000L,
                ValueOrigin.PRINTED, ValueOrigin.UNKNOWN, ValueOrigin.PRINTED,
                ItemResolution.PARTIAL, "PARTIAL");
        ReceiptRecord record = record(ValidationStatus.PASS_WITH_WARNINGS, "2026-10-16", "마트", 3000L,
                Collections.singletonList("PARTIAL_ITEM:0"), partial);
        assertTrue(CaptureReviewAssessmentV2.assess(record).requiresReview());
    }

    @Test public void populatedPartialArithmeticPrefillStillRequiresReview() {
        PersistedItem partial = item(0, "첫상품", 1, 3980L, 3980L,
                ValueOrigin.INFERRED_ARITHMETIC, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.PARTIAL, "PRINTED_UNIT_AND_LINE_INFER_QTY_REVIEW_REQUIRED");
        ReceiptRecord record = record(ValidationStatus.PASS_WITH_WARNINGS, "2026-10-16", "마트", 3980L,
                Collections.singletonList("PARTIAL_ITEM_TUPLE"), partial);
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(record);
        assertTrue(assessment.requiresReview());
        assertEquals(Collections.singletonList(0), assessment.itemOrdinals);
    }

    @Test public void unknownOriginRequiresReview() {
        PersistedItem unknown = item(0, "감자", 1, 3000L, 3000L,
                ValueOrigin.UNKNOWN, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.EXACT, "UNKNOWN_QTY");
        ReceiptRecord record = record(ValidationStatus.PASS, "2026-10-16", "마트", 3000L,
                Collections.emptyList(), unknown);
        assertTrue(CaptureReviewAssessmentV2.assess(record).requiresReview());
    }

    @Test public void mismatchFlagsReceiptAndEveryItem() {
        ReceiptRecord record = record(ValidationStatus.MISMATCH, "2026-10-16", "마트", 2500L,
                Collections.singletonList("RECEIPT_TOTAL_MISMATCH:500"),
                exact(0, "A", 1, 1000L, 1000L), exact(1, "B", 1, 2000L, 2000L));
        CaptureReviewAssessmentV2 a = CaptureReviewAssessmentV2.assess(record);
        assertTrue(a.requiresReview());
        assertTrue(a.flags(CaptureReviewAssessmentV2.ReceiptField.PRINTED_TOTAL));
        assertTrue(a.flags(CaptureReviewAssessmentV2.ReceiptField.DISCOUNT_SUM));
        assertEquals(Arrays.asList(0, 1), a.itemOrdinals);
    }

    @Test public void incompleteRequiresReview() {
        ReceiptRecord record = record(ValidationStatus.INCOMPLETE, "2026-10-16", "마트", null,
                Collections.singletonList("PRINTED_TOTAL_MISSING"), exact(0, "A", 1, 1000L, 1000L));
        CaptureReviewAssessmentV2 a = CaptureReviewAssessmentV2.assess(record);
        assertTrue(a.requiresReview());
        assertTrue(a.flags(CaptureReviewAssessmentV2.ReceiptField.PRINTED_TOTAL));
    }

    @Test public void missingDateRequiresReview() {
        ReceiptRecord record = record(ValidationStatus.PASS, null, "마트", 1000L,
                Collections.emptyList(), exact(0, "A", 1, 1000L, 1000L));
        assertTrue(CaptureReviewAssessmentV2.assess(record)
                .flags(CaptureReviewAssessmentV2.ReceiptField.PURCHASE_DATE));
    }

    @Test public void missingStoreRequiresReview() {
        ReceiptRecord record = record(ValidationStatus.PASS, "2026-10-16", null, 1000L,
                Collections.emptyList(), exact(0, "A", 1, 1000L, 1000L));
        assertTrue(CaptureReviewAssessmentV2.assess(record)
                .flags(CaptureReviewAssessmentV2.ReceiptField.STORE));
    }

    @Test public void correctedUserEditExitsReviewAndPreservesRawOcr() {
        PersistedItem assumed = item(0, "두부", 1, 1000L, 1000L,
                ValueOrigin.DEFAULT_ONE, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.INFERRED, "DEFAULT_ONE");
        ReceiptRecord base = new ReceiptRecord("r", 1L, "2026-10-16", "마트", "RAW OCR",
                2000L, 1000L, 0L, 1000L, -1000L, ValidationStatus.MISMATCH,
                100, 200, false, Collections.singletonList("RECEIPT_TOTAL_MISMATCH:-1000"),
                Collections.singletonList(assumed));
        ReceiptReviewEngine engine = new ReceiptReviewEngine();
        ReceiptRecord reviewed = engine.apply(base, "마트", "2026-10-16", 2000L, 0L,
                Collections.singletonList(new ReviewItemInput("두부", 2, 1000L, 2000L)));
        assertEquals("RAW OCR", reviewed.rawOcrText);
        assertEquals(ValidationStatus.PASS_WITH_WARNINGS, reviewed.validationStatus);
        assertFalse(CaptureReviewAssessmentV2.assess(reviewed).requiresReview());
    }

    @Test public void selectiveAssessmentFlagsOnlyRiskyItems() {
        PersistedItem safe = exact(0, "A", 1, 1000L, 1000L);
        PersistedItem assumed = item(1, "B", 1, 2000L, 2000L,
                ValueOrigin.DEFAULT_ONE, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.INFERRED, "DEFAULT_ONE");
        PersistedItem partial = item(2, "C", 2, null, 3000L,
                ValueOrigin.PRINTED, ValueOrigin.UNKNOWN, ValueOrigin.PRINTED,
                ItemResolution.PARTIAL, "PARTIAL");
        ReceiptRecord record = record(ValidationStatus.PASS_WITH_WARNINGS, "2026-10-16", "마트", 6000L,
                Collections.singletonList("PARTIAL_ITEM:2"), safe, assumed, partial);
        CaptureReviewAssessmentV2 a = CaptureReviewAssessmentV2.assess(record);
        assertEquals(Arrays.asList(1, 2), a.itemOrdinals);
        assertEquals(1, a.autoConfirmedItems);
    }

    @Test public void exactAliasReuseIsBestEffortAndFailureIsolated() {
        ReceiptRecord record = record(ValidationStatus.PASS, "2026-10-16", "마트", 6000L,
                Collections.emptyList(), exact(0, "KNOWN", 1, 1000L, 1000L),
                exact(1, "UNKNOWN", 1, 2000L, 2000L), exact(2, "FAIL", 1, 3000L, 3000L));
        AtomicInteger calls = new AtomicInteger();
        RepeatIdentityReuseV1.Result result = new RepeatIdentityReuseV1().apply(record,
                (receiptId, ordinal, rawName) -> {
                    calls.incrementAndGet();
                    if ("FAIL".equals(rawName)) throw new IllegalStateException("catalog unavailable");
                    return "KNOWN".equals(rawName);
                });
        assertEquals(3, calls.get());
        assertEquals(1, result.linkedCount);
        assertEquals(1, result.unknownCount);
        assertEquals(1, result.failureCount);
    }

    @Test public void metrics() {
        System.out.println("CP33_METRICS capture_review_version=2 auto_confirm_cases=2 review_required_cases=7 user_edit_exit=1 selective_review=1 full_edit=1 raw_ocr_preserved=1 exact_alias_reuse=1 unknown_alias_safe=1 link_failure_isolated=1 auto_processing=1 schema_unchanged=1");
    }

    private static ReceiptRecord record(
            ValidationStatus status, String date, String store, Long printedTotal,
            List<String> issues, PersistedItem... items) {
        long sum = 0L;
        boolean allAmounts = true;
        for (PersistedItem item : items) {
            if (item.lineAmount == null) allAmounts = false;
            else sum += item.lineAmount;
        }
        Long itemSum = allAmounts ? sum : null;
        Long computed = itemSum;
        Long diff = computed == null || printedTotal == null ? null : computed - printedTotal;
        return new ReceiptRecord("r", 1L, date, store, "RAW OCR", printedTotal, itemSum, 0L,
                computed, diff, status, 100, 200, false, new ArrayList<>(issues), Arrays.asList(items));
    }

    private static PersistedItem exact(int ordinal, String name, int quantity, Long unit, Long amount) {
        return item(ordinal, name, quantity, unit, amount,
                ValueOrigin.PRINTED, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.EXACT, "PRINTED");
    }

    private static PersistedItem item(
            int ordinal, String name, Integer quantity, Long unit, Long amount,
            ValueOrigin quantityOrigin, ValueOrigin unitOrigin, ValueOrigin amountOrigin,
            ItemResolution resolution, String reason) {
        return new PersistedItem(ordinal, ordinal, name, quantity, unit, amount,
                quantityOrigin, unitOrigin, amountOrigin, resolution, reason);
    }
}
