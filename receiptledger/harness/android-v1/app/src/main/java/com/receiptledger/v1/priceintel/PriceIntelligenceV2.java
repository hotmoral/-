package com.receiptledger.v1.priceintel;

import com.receiptledger.v1.product.CatalogProduct;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** CP27 result: receipt-traceable observations plus statistics partitioned by safe comparison basis. */
public final class PriceIntelligenceV2 {
    public final CatalogProduct product;
    public final PriceScopeV2 scope;
    public final List<PriceObservationV2> observations;
    public final List<PriceCohortV2> cohorts;

    public PriceIntelligenceV2(CatalogProduct product, PriceScopeV2 scope,
            List<PriceObservationV2> observations, List<PriceCohortV2> cohorts) {
        this.product = product;
        this.scope = scope == null ? PriceScopeV2.all() : scope;
        this.observations = Collections.unmodifiableList(new ArrayList<>(observations));
        this.cohorts = Collections.unmodifiableList(new ArrayList<>(cohorts));
    }

    public int eligibleCount() {
        int n = 0;
        for (PriceObservationV2 observation : observations) if (observation.isEligible()) n++;
        return n;
    }

    public int excludedCount() { return observations.size() - eligibleCount(); }

    public PriceCohortV2 cohort(String basisKey) {
        if (basisKey == null) return null;
        for (PriceCohortV2 cohort : cohorts) if (basisKey.equals(cohort.basis.key())) return cohort;
        return null;
    }
}
