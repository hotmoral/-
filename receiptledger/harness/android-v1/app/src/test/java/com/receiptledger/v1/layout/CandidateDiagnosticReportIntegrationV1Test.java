package com.receiptledger.v1.layout;

import static org.junit.Assert.*;

import com.receiptledger.v1.devicevalidation.CandidateStructureDiagnosticsV1;
import com.receiptledger.v1.devicevalidation.DeviceValidationReportV1;
import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.item.ItemTupleResult;
import com.receiptledger.v1.item.ItemTupleSolver;
import com.receiptledger.v1.ocr.OcrElement;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.review.CaptureReviewAssessmentV2;
import com.receiptledger.v1.structure.ReceiptStructure;
import com.receiptledger.v1.structure.ReceiptStructureAnalyzer;
import com.receiptledger.v1.validation.ValidationStatus;
import java.util.Arrays;
import java.util.Collections;
import org.junit.Test;

public final class CandidateDiagnosticReportIntegrationV1Test {
    @Test public void savedReportAppendsSanitizedDiagnosticForFirstReviewItem() {
        ReceiptStructure structure = structure(
                token("PRIVATE_ITEM", 40), token("12", 140),
                token("3,980", 320), token("3,980", 520));
        ItemTupleResult tuples = new ItemTupleSolver().solve(structure);
        PersistedItem persisted = PersistedItem.from(0, tuples.items.get(0));
        ReceiptRecord record = new ReceiptRecord(
                "PRIVATE_RECEIPT_ID", 1L, "2099-12-31", "PRIVATE_STORE", "PRIVATE_RAW_OCR",
                3980L, 3980L, 0L, 3980L, 0L, ValidationStatus.PASS,
                1080, 2316, false, Collections.emptyList(), Collections.singletonList(persisted));
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(record);
        assertEquals(Collections.singletonList(0), assessment.itemOrdinals);

        CandidateStructureDiagnosticsV1.publishForReceipt(record.id, structure, tuples);
        DeviceValidationReportV1.InitialSnapshot snapshot = DeviceValidationReportV1.captureInitial(
                DeviceValidationReportV1.AcquisitionSource.GALLERY, 300, 1, 0, "ORIGINAL",
                record, assessment);
        String report = DeviceValidationReportV1.savedReport(snapshot, record);

        assertTrue(report.startsWith("RL_CP37_SAMPLE version=2"));
        assertTrue(report.contains("\nRL_CP37_DIAG version=1 target=FIRST_REVIEW_ITEM available=1"));
        assertTrue(report.contains("money_candidates=2"));
        assertTrue(report.contains("quantity_candidates=1"));
        assertTrue(report.contains("quantity_before_first_money=1"));
        assertTrue(report.contains("exact_arithmetic_pairs=0"));
        assertTrue(report.contains("integer_unit_pairs=1"));
        assertTrue(report.contains("solver_resolution=PARTIAL"));
        assertTrue(report.contains("solver_reason=NO_EXACT_ARITHMETIC_SOLUTION"));
        assertFalse(report.contains("PRIVATE_RECEIPT_ID"));
        assertFalse(report.contains("PRIVATE_STORE"));
        assertFalse(report.contains("PRIVATE_ITEM"));
        assertFalse(report.contains("PRIVATE_RAW_OCR"));
        assertFalse(report.contains("3980"));
        assertFalse(report.contains("2099-12-31"));
    }

    private static ReceiptStructure structure(LayoutToken... tokens) {
        ReceiptRow row = new ReceiptRow(Arrays.asList(tokens), 10.0);
        ReceiptLayout layout = new ReceiptLayout(Collections.singletonList(row), tokens.length, 0.0, 10.0);
        return new ReceiptStructureAnalyzer().analyze(layout);
    }

    private static LayoutToken token(String text, double centerX) {
        Quad q = new Quad(
                new PointD(centerX - 20, 0), new PointD(centerX + 20, 0),
                new PointD(centerX + 20, 20), new PointD(centerX - 20, 20));
        return LayoutToken.from(new OcrElement(text, q, q));
    }
}
