package com.receiptledger.v1.catalog;

import com.receiptledger.v1.product.ProductType;

/** Classified V2 catalog kinds. UNCLASSIFIED is intentionally not a catalog entity. */
public enum CatalogKind {
    STANDARD_PRODUCT(ProductType.STANDARD),
    NON_STANDARD_COMMODITY(ProductType.NON_STANDARD);

    private final ProductType legacyType;

    CatalogKind(ProductType legacyType) {
        this.legacyType = legacyType;
    }

    public ProductType toLegacyType() {
        return legacyType;
    }

    public static CatalogKind fromLegacyClassified(ProductType type) {
        if (type == ProductType.STANDARD) return STANDARD_PRODUCT;
        if (type == ProductType.NON_STANDARD) return NON_STANDARD_COMMODITY;
        throw new IllegalArgumentException("UNCLASSIFIED is unresolved, not a catalog entity");
    }
}
