package com.receiptledger.v1.commoditydetail;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogKind;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.PriceCohortV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.ProductCatalogStore;
import com.receiptledger.v1.product.ProductType;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** CP32 read service. It composes frozen CP26-28 facts and performs no mutation. */
public final class CommodityDetailServiceV1 {
    private final ProductCatalogStore catalog;
    private final CatalogV2PersistenceStore v2Store;
    private final PriceIntelligenceServiceV2 priceService;
    private final PriceEvaluationServiceV1 evaluationService;

    public CommodityDetailServiceV1(
            ProductCatalogStore catalog,
            CatalogV2PersistenceStore v2Store,
            PriceIntelligenceServiceV2 priceService) {
        this(catalog, v2Store, priceService, new PriceEvaluationServiceV1());
    }

    CommodityDetailServiceV1(
            ProductCatalogStore catalog,
            CatalogV2PersistenceStore v2Store,
            PriceIntelligenceServiceV2 priceService,
            PriceEvaluationServiceV1 evaluationService) {
        if (catalog == null || v2Store == null || priceService == null || evaluationService == null) {
            throw new IllegalArgumentException("services");
        }
        this.catalog = catalog;
        this.v2Store = v2Store;
        this.priceService = priceService;
        this.evaluationService = evaluationService;
    }

    public CommodityDetailV1 load(String productId) {
        String id = productId == null ? "" : productId.trim();
        if (id.isEmpty()) throw new IllegalArgumentException("productId");

        CatalogProduct product = catalog.product(id);
        if (product == null) throw new IllegalArgumentException("unknown product");
        if (product.type != ProductType.NON_STANDARD) {
            throw new IllegalArgumentException("CP32 supports NON_STANDARD commodity only");
        }

        CatalogEntryV2 entry = v2Store.catalogEntryV2(id);
        if (entry != null && entry.kind != CatalogKind.NON_STANDARD_COMMODITY) {
            throw new IllegalStateException("catalog kind mismatch");
        }

        PriceIntelligenceV2 intelligence = priceService.analyze(id);
        final Map<String,Integer> newestRank = newestBasisRank(intelligence.observations);
        List<CommodityDetailV1.BasisSection> strict = new ArrayList<>();
        List<CommodityDetailV1.BasisSection> contextual = new ArrayList<>();
        for (PriceCohortV2 cohort : intelligence.cohorts) {
            PriceEvaluationV1 evaluation = evaluationService.evaluate(cohort);
            CommodityDetailV1.BasisSection section = new CommodityDetailV1.BasisSection(cohort, evaluation);
            if (section.isStrict()) strict.add(section); else contextual.add(section);
        }
        Comparator<CommodityDetailV1.BasisSection> byRecency = new Comparator<CommodityDetailV1.BasisSection>() {
            @Override public int compare(CommodityDetailV1.BasisSection a, CommodityDetailV1.BasisSection b) {
                int ar = rank(newestRank, a.cohort.basis.key());
                int br = rank(newestRank, b.cohort.basis.key());
                int c = Integer.compare(ar, br);
                if (c != 0) return c;
                return a.cohort.basis.key().compareTo(b.cohort.basis.key());
            }
        };
        Collections.sort(strict, byRecency);
        Collections.sort(contextual, byRecency);

        List<CommodityDetailV1.PurchaseRow> rows = new ArrayList<>();
        for (PriceObservationV2 observation : intelligence.observations) {
            rows.add(new CommodityDetailV1.PurchaseRow(observation));
        }
        return new CommodityDetailV1(product, entry, strict, contextual, rows);
    }

    private static Map<String,Integer> newestBasisRank(List<PriceObservationV2> observations) {
        Map<String,Integer> out = new HashMap<>();
        for (int i = 0; i < observations.size(); i++) {
            PriceObservationV2 observation = observations.get(i);
            if (!observation.isEligible() || observation.basis == null) continue;
            String key = observation.basis.key();
            if (!out.containsKey(key)) out.put(key, i);
        }
        return out;
    }

    private static int rank(Map<String,Integer> ranks, String key) {
        Integer value = ranks.get(key);
        return value == null ? Integer.MAX_VALUE : value;
    }
}
