package com.receiptledger.v1.integration;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.ocr.OcrBlock;
import com.receiptledger.v1.ocr.OcrDocument;
import com.receiptledger.v1.ocr.OcrElement;
import com.receiptledger.v1.ocr.OcrLine;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.persistence.ReceiptRecordFactory;
import com.receiptledger.v1.recovery.RecognitionCandidate;
import com.receiptledger.v1.recovery.RecognitionPass;
import com.receiptledger.v1.recovery.ReceiptRecognitionPipeline;
import com.receiptledger.v1.review.ReceiptReviewEngine;
import com.receiptledger.v1.review.ReviewItemInput;
import com.receiptledger.v1.validation.ValidationStatus;

import org.junit.Test;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.*;

public class VerticalIntegrationContractTest {
    @Test public void syntheticReceiptTraversesRecognitionRecordAndReview() {
        RecognitionCandidate candidate = recognizeSyntheticReceipt();

        assertEquals(2, candidate.items.items.size());
        assertEquals(Long.valueOf(7690), candidate.structure.totalAmount);
        assertEquals(ValidationStatus.PASS, candidate.validation.status);

        ReceiptRecord base = ReceiptRecordFactory.create(
                "fixture-001", 1L, candidate.document, candidate.structure,
                candidate.items, candidate.validation, 150, 160, false);

        assertEquals("2026-10-15", base.purchaseDate);
        assertEquals(Long.valueOf(7690), base.printedTotal);
        assertEquals(Long.valueOf(7690), base.computedNet);
        assertEquals(2, base.items.size());

        List<ReviewItemInput> edits = new ArrayList<>();
        for (int i = 0; i < base.items.size(); i++) {
            PersistedItem item = base.items.get(i);
            String name = i == 0 ? item.name + "(확인)" : item.name;
            edits.add(new ReviewItemInput(name, item.quantity, item.unitPrice, item.lineAmount));
        }

        ReceiptRecord reviewed = new ReceiptReviewEngine().apply(
                base, base.purchaseDate, base.printedTotal, base.discountSum, edits);

        assertEquals(ValidationStatus.PASS_WITH_WARNINGS, reviewed.validationStatus);
        assertEquals(base.rawOcrText, reviewed.rawOcrText);
        assertEquals(base.computedNet, reviewed.computedNet);
        assertTrue(reviewed.issues.contains("USER_EDITED_ITEM:1"));
    }

    @Test public void reviewCannotTurnWrongPrintedTotalIntoPass() {
        RecognitionCandidate candidate = recognizeSyntheticReceipt();
        ReceiptRecord base = ReceiptRecordFactory.create(
                "fixture-002", 2L, candidate.document, candidate.structure,
                candidate.items, candidate.validation, 150, 160, false);
        List<ReviewItemInput> unchanged = new ArrayList<>();
        for (PersistedItem item : base.items) {
            unchanged.add(new ReviewItemInput(item.name, item.quantity, item.unitPrice, item.lineAmount));
        }

        ReceiptRecord reviewed = new ReceiptReviewEngine().apply(
                base, base.purchaseDate, 9999L, base.discountSum, unchanged);

        assertEquals(ValidationStatus.MISMATCH, reviewed.validationStatus);
        assertNotNull(reviewed.difference);
        assertNotEquals(Long.valueOf(0), reviewed.difference);
        assertTrue(reviewed.issues.stream().anyMatch(s -> s.startsWith("RECEIPT_TOTAL_MISMATCH:")));
    }

    private static RecognitionCandidate recognizeSyntheticReceipt() {
        List<OcrElement> all = new ArrayList<>();
        Collections.addAll(all,
                token("가상마트", 10, 10, 45),
                token("2026-10-15", 10, 30, 58),
                token("서울우유1L", 10, 50, 52), token("3,200", 95, 50, 30),
                token("신라면5입", 10, 70, 48), token("4,990", 95, 70, 30),
                token("쿠폰할인", 10, 90, 40), token("-500", 98, 90, 27),
                token("합계", 10, 110, 20), token("7,690", 95, 110, 30),
                token("신용카드", 10, 130, 42), token("7,690", 95, 130, 30));
        Collections.reverse(all);
        OcrLine deliberatelyWrongMlKitLine = new OcrLine("all-in-one", null, null, all);
        String raw = "가상마트\n2026-10-15\n서울우유1L 3,200\n신라면5입 4,990\n쿠폰할인 -500\n합계 7,690\n신용카드 7,690";
        OcrDocument document = new OcrDocument(raw, 150, 160,
                Collections.singletonList(new OcrBlock("all", null, null,
                        Collections.singletonList(deliberatelyWrongMlKitLine))));
        return new ReceiptRecognitionPipeline().evaluate(RecognitionPass.ORIGINAL, document);
    }

    private static OcrElement token(String text, double x, double y, double w) {
        Quad q = new Quad(new PointD(x, y), new PointD(x + w, y),
                new PointD(x + w, y + 10), new PointD(x, y + 10));
        return new OcrElement(text, q, q);
    }
}
