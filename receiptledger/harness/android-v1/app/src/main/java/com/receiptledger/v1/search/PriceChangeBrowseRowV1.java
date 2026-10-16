package com.receiptledger.v1.search;

import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.product.ProductType;
import java.math.BigDecimal;

/** One strict, evaluated CP28 cohort shown in the price-change browse stream. */
public final class PriceChangeBrowseRowV1 {
    public final String productId;
    public final ProductType type;
    public final String canonicalName;
    public final String basisKey;
    public final String displayUnit;
    public final PriceEvaluationV1.Judgment judgment;
    public final BigDecimal latestPriceMinor;
    public final BigDecimal usualPriceMinor;
    public final BigDecimal deltaFromUsualMinor;
    public final BigDecimal deltaFromUsualPercent;
    public final String latestPurchaseDate;
    public final String latestStoreName;
    public final int cohortCount;

    PriceChangeBrowseRowV1(
            String productId,
            ProductType type,
            String canonicalName,
            String basisKey,
            String displayUnit,
            PriceEvaluationV1.Judgment judgment,
            BigDecimal latestPriceMinor,
            BigDecimal usualPriceMinor,
            BigDecimal deltaFromUsualMinor,
            BigDecimal deltaFromUsualPercent,
            String latestPurchaseDate,
            String latestStoreName,
            int cohortCount) {
        this.productId = productId;
        this.type = type;
        this.canonicalName = canonicalName;
        this.basisKey = basisKey;
        this.displayUnit = displayUnit;
        this.judgment = judgment;
        this.latestPriceMinor = latestPriceMinor;
        this.usualPriceMinor = usualPriceMinor;
        this.deltaFromUsualMinor = deltaFromUsualMinor;
        this.deltaFromUsualPercent = deltaFromUsualPercent;
        this.latestPurchaseDate = latestPurchaseDate;
        this.latestStoreName = latestStoreName;
        this.cohortCount = cohortCount;
    }
}
