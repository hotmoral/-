package com.receiptledger.v1.detail;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogKind;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.ComparisonBasisV2;
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
import java.util.List;

/** CP31 read service. It composes frozen catalog/price services and performs no mutation. */
public final class ProductDetailServiceV1 {
    private final ProductCatalogStore catalog;
    private final CatalogV2PersistenceStore v2Store;
    private final PriceIntelligenceServiceV2 priceService;
    private final PriceEvaluationServiceV1 evaluationService;

    public ProductDetailServiceV1(
            ProductCatalogStore catalog,
            CatalogV2PersistenceStore v2Store,
            PriceIntelligenceServiceV2 priceService) {
        this(catalog, v2Store, priceService, new PriceEvaluationServiceV1());
    }

    ProductDetailServiceV1(
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

    public ProductDetailV1 load(String productId) {
        String id = productId == null ? "" : productId.trim();
        if (id.isEmpty()) throw new IllegalArgumentException("productId");

        CatalogProduct product = catalog.product(id);
        if (product == null) throw new IllegalArgumentException("unknown product");
        if (product.type != ProductType.STANDARD) {
            throw new IllegalArgumentException("CP31 supports STANDARD product only");
        }

        CatalogEntryV2 entry = v2Store.catalogEntryV2(id);
        if (entry != null && entry.kind != CatalogKind.STANDARD_PRODUCT) {
            throw new IllegalStateException("catalog kind mismatch");
        }

        PriceIntelligenceV2 intelligence = priceService.analyze(id);
        ComparisonBasisV2 basis = ComparisonBasisV2.standardPackage();
        PriceCohortV2 cohort = intelligence.cohort(basis.key());
        if (cohort == null) cohort = PriceCohortV2.from(basis, Collections.<PriceObservationV2>emptyList());
        PriceEvaluationV1 evaluation = evaluationService.evaluate(cohort);

        List<ProductDetailV1.PurchaseRow> rows = new ArrayList<>();
        for (PriceObservationV2 observation : intelligence.observations) {
            rows.add(new ProductDetailV1.PurchaseRow(observation));
        }
        return new ProductDetailV1(product, entry, cohort, evaluation, rows);
    }
}
