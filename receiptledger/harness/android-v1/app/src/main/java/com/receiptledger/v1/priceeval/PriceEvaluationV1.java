package com.receiptledger.v1.priceeval;

import com.receiptledger.v1.priceintel.ComparisonBasisV2;
import com.receiptledger.v1.priceintel.PriceCohortV2;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Explainable CP28 result for one already-safe CP27 cohort. */
public final class PriceEvaluationV1 {
    public enum Status {
        EVALUATED,
        INSUFFICIENT_HISTORY,
        CONTEXTUAL_ONLY,
        NON_POSITIVE_BASELINE
    }

    public enum Judgment {
        NONE,
        VERY_CHEAP,
        CHEAP,
        TYPICAL,
        EXPENSIVE,
        VERY_EXPENSIVE
    }

    public final ComparisonBasisV2 basis;
    public final PriceCohortV2.Strength cohortStrength;
    public final Status status;
    public final Judgment judgment;
    public final String reasonCode;
    public final int cohortCount;
    public final int baselineCount;
    public final int baselineWindow;
    public final int minimumPriorObservations;
    public final BigDecimal latestPriceMinor;
    public final BigDecimal previousPriceMinor;
    public final BigDecimal previousDeltaMinor;
    public final BigDecimal previousDeltaPercent;
    public final BigDecimal usualPriceMinor;
    public final BigDecimal deltaFromUsualMinor;
    public final BigDecimal deltaFromUsualPercent;
    public final BigDecimal materialPercentThreshold;
    public final BigDecimal materialAbsoluteThresholdMinor;
    public final BigDecimal extremePercentThreshold;
    public final BigDecimal extremeAbsoluteThresholdMinor;
    public final List<String> baselineReceiptIds;

    PriceEvaluationV1(
            ComparisonBasisV2 basis,
            PriceCohortV2.Strength cohortStrength,
            Status status,
            Judgment judgment,
            String reasonCode,
            int cohortCount,
            int baselineCount,
            PriceEvaluationPolicyV1 policy,
            BigDecimal latestPriceMinor,
            BigDecimal previousPriceMinor,
            BigDecimal previousDeltaMinor,
            BigDecimal previousDeltaPercent,
            BigDecimal usualPriceMinor,
            BigDecimal deltaFromUsualMinor,
            BigDecimal deltaFromUsualPercent,
            List<String> baselineReceiptIds) {
        this.basis = basis;
        this.cohortStrength = cohortStrength;
        this.status = status;
        this.judgment = judgment;
        this.reasonCode = reasonCode;
        this.cohortCount = cohortCount;
        this.baselineCount = baselineCount;
        this.baselineWindow = policy.baselineWindow;
        this.minimumPriorObservations = policy.minimumPriorObservations;
        this.latestPriceMinor = latestPriceMinor;
        this.previousPriceMinor = previousPriceMinor;
        this.previousDeltaMinor = previousDeltaMinor;
        this.previousDeltaPercent = previousDeltaPercent;
        this.usualPriceMinor = usualPriceMinor;
        this.deltaFromUsualMinor = deltaFromUsualMinor;
        this.deltaFromUsualPercent = deltaFromUsualPercent;
        this.materialPercentThreshold = policy.materialPercent;
        this.materialAbsoluteThresholdMinor = policy.materialAbsoluteMinor;
        this.extremePercentThreshold = policy.extremePercent;
        this.extremeAbsoluteThresholdMinor = policy.extremeAbsoluteMinor;
        this.baselineReceiptIds = Collections.unmodifiableList(new ArrayList<>(baselineReceiptIds));
    }

    public boolean hasJudgment() { return status == Status.EVALUATED && judgment != Judgment.NONE; }
}
