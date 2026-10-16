package com.receiptledger.v1.priceeval;

import com.receiptledger.v1.priceintel.PriceCohortV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Deterministic CP28 judgment over exactly one CP27 cohort. */
public final class PriceEvaluationServiceV1 {
    private final PriceEvaluationPolicyV1 policy;

    public PriceEvaluationServiceV1() { this(PriceEvaluationPolicyV1.canonical()); }

    public PriceEvaluationServiceV1(PriceEvaluationPolicyV1 policy) {
        if (policy == null) throw new IllegalArgumentException("policy");
        this.policy = policy;
    }

    public PriceEvaluationV1 evaluate(PriceCohortV2 cohort) {
        if (cohort == null) throw new IllegalArgumentException("cohort");
        BigDecimal latest = cohort.latest;
        BigDecimal previous = cohort.previous;
        BigDecimal previousDelta = cohort.delta;
        BigDecimal previousPercent = cohort.deltaPercent;

        if (cohort.strength == PriceCohortV2.Strength.CONTEXTUAL_LIKE_FORM) {
            return result(cohort, PriceEvaluationV1.Status.CONTEXTUAL_ONLY, PriceEvaluationV1.Judgment.NONE,
                    "CONTEXTUAL_LIKE_FORM_NOT_JUDGED", 0, latest, previous, previousDelta, previousPercent,
                    null, null, null, Collections.<String>emptyList());
        }

        if (latest == null || cohort.count() < 1) {
            return result(cohort, PriceEvaluationV1.Status.INSUFFICIENT_HISTORY, PriceEvaluationV1.Judgment.NONE,
                    "NO_CURRENT_ELIGIBLE_PRICE", 0, latest, previous, previousDelta, previousPercent,
                    null, null, null, Collections.<String>emptyList());
        }

        int availablePrior = Math.max(0, cohort.observations.size() - 1);
        int baselineCount = Math.min(policy.baselineWindow, availablePrior);
        List<BigDecimal> baselinePrices = new ArrayList<>();
        List<String> baselineReceiptIds = new ArrayList<>();
        for (int i = 1; i <= baselineCount; i++) {
            PriceObservationV2 row = cohort.observations.get(i);
            baselinePrices.add(row.comparisonPriceMinor);
            baselineReceiptIds.add(row.receiptId);
        }

        if (baselineCount < policy.minimumPriorObservations) {
            return result(cohort, PriceEvaluationV1.Status.INSUFFICIENT_HISTORY, PriceEvaluationV1.Judgment.NONE,
                    "INSUFFICIENT_PRIOR_OBSERVATIONS", baselineCount, latest, previous, previousDelta, previousPercent,
                    null, null, null, baselineReceiptIds);
        }

        BigDecimal usual = median(baselinePrices);
        if (usual == null || usual.compareTo(BigDecimal.ZERO) <= 0) {
            return result(cohort, PriceEvaluationV1.Status.NON_POSITIVE_BASELINE, PriceEvaluationV1.Judgment.NONE,
                    "NON_POSITIVE_USUAL_PRICE", baselineCount, latest, previous, previousDelta, previousPercent,
                    usual, null, null, baselineReceiptIds);
        }

        BigDecimal delta = latest.subtract(usual).stripTrailingZeros();
        BigDecimal percent = delta.multiply(new BigDecimal("100"))
                .divide(usual, 4, RoundingMode.HALF_UP).stripTrailingZeros();
        BigDecimal absDelta = delta.abs();
        BigDecimal absPercent = percent.abs();

        PriceEvaluationV1.Judgment judgment;
        String reason;
        boolean material = absPercent.compareTo(policy.materialPercent) >= 0
                && absDelta.compareTo(policy.materialAbsoluteMinor) >= 0;
        boolean extreme = absPercent.compareTo(policy.extremePercent) >= 0
                && absDelta.compareTo(policy.extremeAbsoluteMinor) >= 0;

        if (!material || delta.compareTo(BigDecimal.ZERO) == 0) {
            judgment = PriceEvaluationV1.Judgment.TYPICAL;
            reason = "WITHIN_MATERIALITY_BAND";
        } else if (delta.signum() < 0) {
            judgment = extreme ? PriceEvaluationV1.Judgment.VERY_CHEAP : PriceEvaluationV1.Judgment.CHEAP;
            reason = extreme ? "BELOW_EXTREME_THRESHOLDS" : "BELOW_MATERIAL_THRESHOLDS";
        } else {
            judgment = extreme ? PriceEvaluationV1.Judgment.VERY_EXPENSIVE : PriceEvaluationV1.Judgment.EXPENSIVE;
            reason = extreme ? "ABOVE_EXTREME_THRESHOLDS" : "ABOVE_MATERIAL_THRESHOLDS";
        }

        return result(cohort, PriceEvaluationV1.Status.EVALUATED, judgment, reason,
                baselineCount, latest, previous, previousDelta, previousPercent,
                usual, delta, percent, baselineReceiptIds);
    }

    private PriceEvaluationV1 result(
            PriceCohortV2 cohort,
            PriceEvaluationV1.Status status,
            PriceEvaluationV1.Judgment judgment,
            String reason,
            int baselineCount,
            BigDecimal latest,
            BigDecimal previous,
            BigDecimal previousDelta,
            BigDecimal previousPercent,
            BigDecimal usual,
            BigDecimal delta,
            BigDecimal percent,
            List<String> baselineReceiptIds) {
        return new PriceEvaluationV1(
                cohort.basis,
                cohort.strength,
                status,
                judgment,
                reason,
                cohort.count(),
                baselineCount,
                policy,
                latest,
                previous,
                previousDelta,
                previousPercent,
                usual,
                delta,
                percent,
                baselineReceiptIds);
    }

    private static BigDecimal median(List<BigDecimal> values) {
        if (values == null || values.isEmpty()) return null;
        List<BigDecimal> sorted = new ArrayList<>(values);
        Collections.sort(sorted);
        int middle = sorted.size() / 2;
        if ((sorted.size() & 1) == 1) return sorted.get(middle).stripTrailingZeros();
        return sorted.get(middle - 1).add(sorted.get(middle))
                .divide(new BigDecimal("2"), MathContext.DECIMAL128).stripTrailingZeros();
    }
}
