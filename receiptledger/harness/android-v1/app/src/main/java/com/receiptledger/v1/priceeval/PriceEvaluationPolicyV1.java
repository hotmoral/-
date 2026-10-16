package com.receiptledger.v1.priceeval;

import java.math.BigDecimal;

/** Frozen CP28 V1 judgment policy. Values are explicit product heuristics, not market-price truth. */
public final class PriceEvaluationPolicyV1 {
    public final int minimumPriorObservations;
    public final int baselineWindow;
    public final BigDecimal materialPercent;
    public final BigDecimal materialAbsoluteMinor;
    public final BigDecimal extremePercent;
    public final BigDecimal extremeAbsoluteMinor;

    private PriceEvaluationPolicyV1(
            int minimumPriorObservations,
            int baselineWindow,
            BigDecimal materialPercent,
            BigDecimal materialAbsoluteMinor,
            BigDecimal extremePercent,
            BigDecimal extremeAbsoluteMinor) {
        if (minimumPriorObservations < 1 || baselineWindow < minimumPriorObservations) {
            throw new IllegalArgumentException("baseline counts");
        }
        this.minimumPriorObservations = minimumPriorObservations;
        this.baselineWindow = baselineWindow;
        this.materialPercent = positive(materialPercent, "materialPercent");
        this.materialAbsoluteMinor = positive(materialAbsoluteMinor, "materialAbsoluteMinor");
        this.extremePercent = positive(extremePercent, "extremePercent");
        this.extremeAbsoluteMinor = positive(extremeAbsoluteMinor, "extremeAbsoluteMinor");
        if (this.extremePercent.compareTo(this.materialPercent) <= 0
                || this.extremeAbsoluteMinor.compareTo(this.materialAbsoluteMinor) <= 0) {
            throw new IllegalArgumentException("extreme thresholds must exceed material thresholds");
        }
    }

    public static PriceEvaluationPolicyV1 canonical() {
        return new PriceEvaluationPolicyV1(
                3,
                5,
                new BigDecimal("5"),
                new BigDecimal("100"),
                new BigDecimal("15"),
                new BigDecimal("500"));
    }

    private static BigDecimal positive(BigDecimal value, String name) {
        if (value == null || value.compareTo(BigDecimal.ZERO) <= 0) throw new IllegalArgumentException(name);
        return value.stripTrailingZeros();
    }
}
