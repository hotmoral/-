package com.receiptledger.v1.catalog;

import com.receiptledger.v1.product.CatalogProduct;

/** Fail-closed bridge from the frozen V1 catalog entity into the V2 domain view. */
public final class LegacyCatalogAdapter {
    private LegacyCatalogAdapter() {}

    public static CatalogEntryV2 fromLegacy(CatalogProduct legacy) {
        if (legacy == null) throw new IllegalArgumentException("legacy product");
        CatalogKind kind = CatalogKind.fromLegacyClassified(legacy.type);
        return CatalogEntryV2.legacy(legacy.id, kind, legacy.canonicalName, legacy.createdAtMillis);
    }
}
