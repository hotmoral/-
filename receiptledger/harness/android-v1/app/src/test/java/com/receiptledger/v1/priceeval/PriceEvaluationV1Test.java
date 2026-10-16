package com.receiptledger.v1.priceeval;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.priceintel.ComparisonBasisV2;
import com.receiptledger.v1.priceintel.PriceCohortV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import com.receiptledger.v1.product.LinkSource;
import com.receiptledger.v1.validation.ValidationStatus;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Test;

public final class PriceEvaluationV1Test {
    private final PriceEvaluationServiceV1 service = new PriceEvaluationServiceV1();

    @Test public void baselineExcludesLatestAndUsesOnlyRecentFivePriorMedian() {
        PriceCohortV2 cohort = cohort(ComparisonBasisV2.standardPackage(),
                14000, 10000, 10200, 9800, 10100, 9900, 50000);
        PriceEvaluationV1 r = service.evaluate(cohort);
        assertEquals(PriceEvaluationV1.Status.EVALUATED, r.status);
        assertEquals(PriceEvaluationV1.Judgment.VERY_EXPENSIVE, r.judgment);
        assertEquals(5, r.baselineCount);
        bd("10000", r.usualPriceMinor);
        bd("4000", r.deltaFromUsualMinor);
        bd("40", r.deltaFromUsualPercent);
        assertEquals(Arrays.asList("r1", "r2", "r3", "r4", "r5"), r.baselineReceiptIds);
        assertFalse(r.baselineReceiptIds.contains("r0"));
        assertFalse(r.baselineReceiptIds.contains("r6"));
    }

    @Test public void minimumThreePriorObservationsAreRequired() {
        PriceEvaluationV1 r = service.evaluate(cohort(ComparisonBasisV2.standardPackage(), 12000, 10000, 10000));
        assertEquals(PriceEvaluationV1.Status.INSUFFICIENT_HISTORY, r.status);
        assertEquals(PriceEvaluationV1.Judgment.NONE, r.judgment);
        assertEquals("INSUFFICIENT_PRIOR_OBSERVATIONS", r.reasonCode);
        assertEquals(2, r.baselineCount);
        assertNull(r.usualPriceMinor);
    }

    @Test public void contextualLikeFormNeverReceivesCheapOrExpensiveJudgment() {
        PriceEvaluationV1 r = service.evaluate(cohort(ComparisonBasisV2.likeForm("BAG", "봉"),
                7000, 4000, 4200, 4100, 4300));
        assertEquals(PriceEvaluationV1.Status.CONTEXTUAL_ONLY, r.status);
        assertEquals(PriceEvaluationV1.Judgment.NONE, r.judgment);
        assertEquals("CONTEXTUAL_LIKE_FORM_NOT_JUDGED", r.reasonCode);
        assertEquals(0, r.baselineCount);
        bd("7000", r.latestPriceMinor);
        bd("4000", r.previousPriceMinor);
    }

    @Test public void nonPositiveMedianBaselineSuppressesPercentageJudgment() {
        PriceEvaluationV1 r = service.evaluate(cohort(ComparisonBasisV2.standardPackage(), 100, 0, 0, 0));
        assertEquals(PriceEvaluationV1.Status.NON_POSITIVE_BASELINE, r.status);
        assertEquals(PriceEvaluationV1.Judgment.NONE, r.judgment);
        assertEquals("NON_POSITIVE_USUAL_PRICE", r.reasonCode);
        bd("0", r.usualPriceMinor);
        assertNull(r.deltaFromUsualPercent);
    }

    @Test public void percentageAndAbsoluteMaterialityGatesBothApply() {
        assertJudgment(PriceEvaluationV1.Judgment.TYPICAL, 10400, 10000, 10000, 10000); // +4%
        assertJudgment(PriceEvaluationV1.Judgment.TYPICAL, 1080, 1000, 1000, 1000);     // +8% but only 80
        assertJudgment(PriceEvaluationV1.Judgment.CHEAP, 9000, 10000, 10000, 10000);
        assertJudgment(PriceEvaluationV1.Judgment.EXPENSIVE, 11000, 10000, 10000, 10000);
        assertJudgment(PriceEvaluationV1.Judgment.VERY_CHEAP, 8000, 10000, 10000, 10000);
        assertJudgment(PriceEvaluationV1.Judgment.VERY_EXPENSIVE, 12000, 10000, 10000, 10000);
    }

    @Test public void exactThresholdBoundariesAreDeterministic() {
        assertJudgment(PriceEvaluationV1.Judgment.EXPENSIVE, 10500, 10000, 10000, 10000);
        assertJudgment(PriceEvaluationV1.Judgment.CHEAP, 9500, 10000, 10000, 10000);
        assertJudgment(PriceEvaluationV1.Judgment.VERY_EXPENSIVE, 11500, 10000, 10000, 10000);
        assertJudgment(PriceEvaluationV1.Judgment.VERY_CHEAP, 8500, 10000, 10000, 10000);
    }

    @Test public void previousPurchaseChangeRemainsSeparateFromUsualPriceJudgment() {
        PriceEvaluationV1 r = service.evaluate(cohort(ComparisonBasisV2.standardPackage(),
                12000, 8000, 10000, 10000));
        bd("8000", r.previousPriceMinor);
        bd("4000", r.previousDeltaMinor);
        bd("50", r.previousDeltaPercent);
        bd("10000", r.usualPriceMinor);
        bd("2000", r.deltaFromUsualMinor);
        bd("20", r.deltaFromUsualPercent);
        assertEquals(PriceEvaluationV1.Judgment.VERY_EXPENSIVE, r.judgment);
    }

    @Test public void canonicalMetricsCoverJudgmentsAndNoJudgmentStates() {
        List<PriceEvaluationV1> cases = new ArrayList<>();
        cases.add(eval(8000,10000,10000,10000));
        cases.add(eval(9000,10000,10000,10000));
        cases.add(eval(10400,10000,10000,10000));
        cases.add(eval(1080,1000,1000,1000));
        cases.add(eval(11000,10000,10000,10000));
        cases.add(eval(12000,10000,10000,10000));
        cases.add(service.evaluate(cohort(ComparisonBasisV2.standardPackage(),12000,10000,10000)));
        cases.add(service.evaluate(cohort(ComparisonBasisV2.likeForm("BAG","봉"),7000,4000,4200,4100)));
        cases.add(service.evaluate(cohort(ComparisonBasisV2.standardPackage(),100,0,0,0)));
        cases.add(eval(10500,10000,10000,10000));
        cases.add(eval(11500,10000,10000,10000));
        cases.add(eval(9500,10000,10000,10000));

        int evaluated=0,insufficient=0,contextual=0,nonpositive=0,typical=0,cheap=0,veryCheap=0,expensive=0,veryExpensive=0;
        for (PriceEvaluationV1 r : cases) {
            if (r.status == PriceEvaluationV1.Status.EVALUATED) evaluated++;
            if (r.status == PriceEvaluationV1.Status.INSUFFICIENT_HISTORY) insufficient++;
            if (r.status == PriceEvaluationV1.Status.CONTEXTUAL_ONLY) contextual++;
            if (r.status == PriceEvaluationV1.Status.NON_POSITIVE_BASELINE) nonpositive++;
            if (r.judgment == PriceEvaluationV1.Judgment.TYPICAL) typical++;
            if (r.judgment == PriceEvaluationV1.Judgment.CHEAP) cheap++;
            if (r.judgment == PriceEvaluationV1.Judgment.VERY_CHEAP) veryCheap++;
            if (r.judgment == PriceEvaluationV1.Judgment.EXPENSIVE) expensive++;
            if (r.judgment == PriceEvaluationV1.Judgment.VERY_EXPENSIVE) veryExpensive++;
        }
        assertEquals(12, cases.size());
        assertEquals(9, evaluated);
        assertEquals(1, insufficient);
        assertEquals(1, contextual);
        assertEquals(1, nonpositive);
        assertEquals(2, typical);
        assertEquals(2, cheap);
        assertEquals(1, veryCheap);
        assertEquals(2, expensive);
        assertEquals(2, veryExpensive);

        PriceEvaluationV1 window = service.evaluate(cohort(ComparisonBasisV2.standardPackage(),
                14000,10000,10200,9800,10100,9900,50000));
        int latestExcluded = window.baselineReceiptIds.contains("r0") ? 0 : 1;
        int recentFive = window.baselineCount == 5 && !window.baselineReceiptIds.contains("r6") ? 1 : 0;
        PriceEvaluationV1 repeat = service.evaluate(cohort(ComparisonBasisV2.standardPackage(),
                14000,10000,10200,9800,10100,9900,50000));
        int deterministic = window.judgment == repeat.judgment
                && window.usualPriceMinor.compareTo(repeat.usualPriceMinor) == 0 ? 1 : 0;

        System.out.println("CP28_METRICS cases=12 evaluated="+evaluated+" insufficient="+insufficient
                +" contextual="+contextual+" nonpositive="+nonpositive+" typical="+typical
                +" cheap="+cheap+" very_cheap="+veryCheap+" expensive="+expensive
                +" very_expensive="+veryExpensive+" latest_excluded="+latestExcluded
                +" recent_five_window="+recentFive+" deterministic_repeat="+deterministic);
    }

    private PriceEvaluationV1 eval(long latest, long p1, long p2, long p3) {
        return service.evaluate(cohort(ComparisonBasisV2.standardPackage(), latest, p1, p2, p3));
    }

    private void assertJudgment(PriceEvaluationV1.Judgment expected, long latest, long p1, long p2, long p3) {
        PriceEvaluationV1 r = eval(latest,p1,p2,p3);
        assertEquals(PriceEvaluationV1.Status.EVALUATED, r.status);
        assertEquals(expected, r.judgment);
    }

    private static PriceCohortV2 cohort(ComparisonBasisV2 basis, long... newestFirstPrices) {
        List<PriceObservationV2> rows = new ArrayList<>();
        for (int i=0;i<newestFirstPrices.length;i++) {
            String day = String.format("%02d", 20-i);
            rows.add(PriceObservationV2.eligible(
                    "r"+i, 0, "2026-10-"+day, "store", 1000-i, "item", 1,
                    newestFirstPrices[i], newestFirstPrices[i], 0L, ValidationStatus.PASS,
                    LinkSource.USER_CONFIRMED, null, CatalogField.Source.UNKNOWN,
                    CatalogField.Confirmation.UNCONFIRMED, CatalogField.Confidence.UNKNOWN,
                    PriceObservationV2.DiscountTreatment.NONE, basis,
                    PriceObservationV2.PriceSource.PRINTED_UNIT_PRICE,
                    BigDecimal.valueOf(newestFirstPrices[i]), BigDecimal.ONE));
        }
        return PriceCohortV2.from(basis, rows);
    }

    private static void bd(String expected, BigDecimal actual) {
        assertNotNull(actual);
        assertEquals(0, new BigDecimal(expected).compareTo(actual));
    }
}
