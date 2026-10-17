package com.receiptledger.v1.layout;

import static org.junit.Assert.*;

import com.receiptledger.v1.devicevalidation.CandidateStructureDiagnosticsV1;
import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ItemTupleResult;
import com.receiptledger.v1.item.ItemTupleSolver;
import com.receiptledger.v1.ocr.OcrElement;
import com.receiptledger.v1.structure.ReceiptStructure;
import com.receiptledger.v1.structure.ReceiptStructureAnalyzer;
import java.util.Arrays;
import java.util.Collections;
import org.junit.Test;

public final class CandidateStructureDiagnosticsV1Test {
    @Test public void productZoneNumberIsSeparatedFromArithmeticEvidence() {
        ReceiptStructure structure = structure(
                token("ITEM", 40),
                token("12", 140),
                token("3,980", 320),
                token("3,980", 520));
        ItemTupleResult tuples = new ItemTupleSolver().solve(structure);
        assertEquals(1, tuples.items.size());
        assertEquals(ItemResolution.PARTIAL, tuples.items.get(0).resolution);

        CandidateStructureDiagnosticsV1.Summary summary =
                CandidateStructureDiagnosticsV1.summarize(structure, tuples, 0);
        assertTrue(summary.available);
        assertEquals(2, summary.moneyCandidates);
        assertEquals(1, summary.quantityCandidates);
        assertEquals(1, summary.quantityBeforeFirstMoney);
        assertEquals(0, summary.quantityBetweenMoney);
        assertEquals(0, summary.quantityAfterLine);
        assertEquals(0, summary.exactArithmeticPairs);
        assertEquals(1, summary.integerUnitPairs);
        assertEquals("PARTIAL", summary.solverResolution);
        assertEquals("NO_EXACT_ARITHMETIC_SOLUTION", summary.solverReason);
        String line = summary.reportLine();
        assertFalse(line.contains("3980"));
        assertFalse(line.contains("ITEM"));
    }

    @Test public void trueQuantityBetweenMoneyProducesExactPair() {
        ReceiptStructure structure = structure(
                token("ITEM", 40),
                token("3,980", 300),
                token("1", 410),
                token("3,980", 520));
        ItemTupleResult tuples = new ItemTupleSolver().solve(structure);
        CandidateStructureDiagnosticsV1.Summary summary =
                CandidateStructureDiagnosticsV1.summarize(structure, tuples, 0);
        assertEquals(ItemResolution.EXACT, tuples.items.get(0).resolution);
        assertEquals(2, summary.moneyCandidates);
        assertEquals(1, summary.quantityCandidates);
        assertEquals(0, summary.quantityBeforeFirstMoney);
        assertEquals(1, summary.quantityBetweenMoney);
        assertEquals(1, summary.exactArithmeticPairs);
        assertEquals(1, summary.integerUnitPairs);
        assertEquals("EXACT", summary.solverResolution);
    }

    @Test public void multipleIntegerUnitPairsExposeAmbiguity() {
        ReceiptStructure structure = structure(
                token("ITEM", 40),
                token("1,000", 260),
                token("2,000", 360),
                token("4,000", 520));
        ItemTupleResult tuples = new ItemTupleSolver().solve(structure);
        CandidateStructureDiagnosticsV1.Summary summary =
                CandidateStructureDiagnosticsV1.summarize(structure, tuples, 0);
        assertEquals(ItemResolution.PARTIAL, tuples.items.get(0).resolution);
        assertEquals(3, summary.moneyCandidates);
        assertEquals(0, summary.quantityCandidates);
        assertEquals(0, summary.exactArithmeticPairs);
        assertEquals(2, summary.integerUnitPairs);
    }

    @Test public void unavailableTargetEmitsOnlyNeutralDiagnostics() {
        CandidateStructureDiagnosticsV1.Summary summary =
                CandidateStructureDiagnosticsV1.summarize(null, null, -1);
        assertFalse(summary.available);
        assertEquals("RL_CP37_DIAG version=1 target=FIRST_REVIEW_ITEM available=0 money_candidates=0 quantity_candidates=0 quantity_before_first_money=0 quantity_between_money=0 quantity_after_line=0 exact_arithmetic_pairs=0 integer_unit_pairs=0 solver_resolution=UNKNOWN solver_reason=UNKNOWN", summary.reportLine());
    }

    private static ReceiptStructure structure(LayoutToken... tokens) {
        ReceiptRow row = new ReceiptRow(Arrays.asList(tokens), 10.0);
        ReceiptLayout layout = new ReceiptLayout(Collections.singletonList(row), tokens.length, 0.0, 10.0);
        return new ReceiptStructureAnalyzer().analyze(layout);
    }

    private static LayoutToken token(String text, double centerX) {
        double halfW = 20.0;
        Quad q = new Quad(
                new PointD(centerX - halfW, 0),
                new PointD(centerX + halfW, 0),
                new PointD(centerX + halfW, 20),
                new PointD(centerX - halfW, 20));
        return LayoutToken.from(new OcrElement(text, q, q));
    }
}
