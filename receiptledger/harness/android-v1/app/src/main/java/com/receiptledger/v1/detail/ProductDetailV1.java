package com.receiptledger.v1.detail;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.PriceCohortV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import com.receiptledger.v1.product.CatalogProduct;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Read-only CP31 projection. No field here is a new source of product or price truth. */
public final class ProductDetailV1 {
    public final CatalogProduct product;
    public final CatalogEntryV2 catalogEntry;
    public final PriceCohortV2 cohort;
    public final PriceEvaluationV1 evaluation;
    public final List<PurchaseRow> purchases;

    public ProductDetailV1(
            CatalogProduct product,
            CatalogEntryV2 catalogEntry,
            PriceCohortV2 cohort,
            PriceEvaluationV1 evaluation,
            List<PurchaseRow> purchases) {
        if (product == null || cohort == null || evaluation == null) throw new IllegalArgumentException("detail");
        this.product = product;
        this.catalogEntry = catalogEntry;
        this.cohort = cohort;
        this.evaluation = evaluation;
        this.purchases = Collections.unmodifiableList(new ArrayList<>(purchases));
    }

    public List<PurchaseRow> comparablePurchases() {
        List<PurchaseRow> out = new ArrayList<>();
        for (PurchaseRow row : purchases) if (row.comparable) out.add(row);
        return Collections.unmodifiableList(out);
    }

    public static final class PurchaseRow {
        public final String receiptId;
        public final int itemOrdinal;
        public final String purchaseDate;
        public final String storeName;
        public final long createdAtMillis;
        public final String rawItemName;
        public final boolean comparable;
        public final java.math.BigDecimal comparisonPriceMinor;
        public final PriceObservationV2.Eligibility eligibility;
        public final String exclusionReason;

        public PurchaseRow(PriceObservationV2 observation) {
            if (observation == null) throw new IllegalArgumentException("observation");
            this.receiptId = observation.receiptId;
            this.itemOrdinal = observation.itemOrdinal;
            this.purchaseDate = observation.purchaseDate;
            this.storeName = observation.storeName;
            this.createdAtMillis = observation.createdAtMillis;
            this.rawItemName = observation.rawItemName;
            this.comparable = observation.isEligible();
            this.comparisonPriceMinor = observation.comparisonPriceMinor;
            this.eligibility = observation.eligibility;
            this.exclusionReason = observation.exclusionReason;
        }
    }
}
