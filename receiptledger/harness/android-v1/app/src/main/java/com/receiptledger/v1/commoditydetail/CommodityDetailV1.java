package com.receiptledger.v1.commoditydetail;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.PriceCohortV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import com.receiptledger.v1.product.CatalogProduct;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** CP32 read-only projection for one NON_STANDARD commodity. */
public final class CommodityDetailV1 {
    public static final int VERSION = 1;

    public final CatalogProduct product;
    public final CatalogEntryV2 catalogEntry;
    public final List<BasisSection> strictSections;
    public final List<BasisSection> contextualSections;
    public final List<PurchaseRow> purchases;
    public final PurchaseRow latestPurchase;

    public CommodityDetailV1(
            CatalogProduct product,
            CatalogEntryV2 catalogEntry,
            List<BasisSection> strictSections,
            List<BasisSection> contextualSections,
            List<PurchaseRow> purchases) {
        if (product == null) throw new IllegalArgumentException("product");
        this.product = product;
        this.catalogEntry = catalogEntry;
        this.strictSections = immutable(strictSections);
        this.contextualSections = immutable(contextualSections);
        this.purchases = immutableRows(purchases);
        this.latestPurchase = this.purchases.isEmpty() ? null : this.purchases.get(0);
    }

    public BasisSection strictSection(String basisKey) {
        return find(strictSections, basisKey);
    }

    public BasisSection contextualSection(String basisKey) {
        return find(contextualSections, basisKey);
    }

    private static BasisSection find(List<BasisSection> sections, String basisKey) {
        if (basisKey == null) return null;
        for (BasisSection section : sections) {
            if (basisKey.equals(section.cohort.basis.key())) return section;
        }
        return null;
    }

    private static List<BasisSection> immutable(List<BasisSection> source) {
        return Collections.unmodifiableList(new ArrayList<>(source == null
                ? Collections.<BasisSection>emptyList() : source));
    }

    private static List<PurchaseRow> immutableRows(List<PurchaseRow> source) {
        return Collections.unmodifiableList(new ArrayList<>(source == null
                ? Collections.<PurchaseRow>emptyList() : source));
    }

    public static final class BasisSection {
        public final PriceCohortV2 cohort;
        public final PriceEvaluationV1 evaluation;

        public BasisSection(PriceCohortV2 cohort, PriceEvaluationV1 evaluation) {
            if (cohort == null || evaluation == null) throw new IllegalArgumentException("basis section");
            if (!cohort.basis.equals(evaluation.basis)) throw new IllegalArgumentException("basis mismatch");
            this.cohort = cohort;
            this.evaluation = evaluation;
        }

        public boolean isStrict() {
            return cohort.strength == PriceCohortV2.Strength.STRICT_NORMALIZED;
        }
    }

    public static final class PurchaseRow {
        public final PriceObservationV2 observation;

        public PurchaseRow(PriceObservationV2 observation) {
            if (observation == null) throw new IllegalArgumentException("observation");
            this.observation = observation;
        }

        public boolean isEligible() { return observation.isEligible(); }
        public boolean isStrictComparable() { return observation.isStrictComparable(); }
        public boolean isContextual() {
            return observation.isEligible() && observation.basis != null && !observation.basis.isStrictNormalized();
        }
    }
}
