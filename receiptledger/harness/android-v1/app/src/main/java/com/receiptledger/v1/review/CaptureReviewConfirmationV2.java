package com.receiptledger.v1.review;

import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.validation.ValidationStatus;
import java.util.ArrayList;
import java.util.List;

/** Adds explicit CP33 confirmation provenance without erasing original automatic origins. */
public final class CaptureReviewConfirmationV2 {
    private CaptureReviewConfirmationV2() {}

    public static ReceiptRecord apply(ReceiptRecord reviewed, CaptureReviewAssessmentV2 prior) {
        if (reviewed == null) throw new IllegalArgumentException("reviewed");
        if (prior == null) return reviewed;
        List<String> issues = new ArrayList<>(reviewed.issues);
        boolean added = false;
        for (Integer ordinal : prior.itemOrdinals) {
            PersistedItem item = find(reviewed, ordinal == null ? -1 : ordinal);
            if (item == null) continue;
            if (item.quantityOrigin == ValueOrigin.DEFAULT_ONE
                    && item.quantity != null && item.quantity > 0
                    && item.lineAmount != null) {
                String marker = "USER_CONFIRMED_DEFAULT_ONE:" + item.ordinal;
                if (!issues.contains(marker)) {
                    issues.add(marker);
                    added = true;
                }
            }
        }
        if (!added) return reviewed;
        ValidationStatus status = reviewed.validationStatus == ValidationStatus.PASS
                ? ValidationStatus.PASS_WITH_WARNINGS : reviewed.validationStatus;
        return new ReceiptRecord(
                reviewed.id,
                reviewed.createdAtMillis,
                reviewed.purchaseDate,
                reviewed.storeName,
                reviewed.rawOcrText,
                reviewed.printedTotal,
                reviewed.itemLineSum,
                reviewed.discountSum,
                reviewed.computedNet,
                reviewed.difference,
                status,
                reviewed.sourceWidth,
                reviewed.sourceHeight,
                reviewed.perspectiveCorrected,
                issues,
                reviewed.items);
    }

    private static PersistedItem find(ReceiptRecord record, int ordinal) {
        for (PersistedItem item : record.items) if (item.ordinal == ordinal) return item;
        return null;
    }
}
