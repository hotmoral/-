package com.receiptledger.v1.priceintel;

import com.receiptledger.v1.product.ProductNameNormalizer;

/** Optional deterministic date/store filter for price statistics. Dates are canonical ISO yyyy-MM-dd strings. */
public final class PriceScopeV2 {
    public final String fromDateInclusive;
    public final String toDateInclusive;
    public final String storeKey;

    private PriceScopeV2(String fromDateInclusive, String toDateInclusive, String storeName) {
        if (fromDateInclusive != null && toDateInclusive != null && fromDateInclusive.compareTo(toDateInclusive) > 0) {
            throw new IllegalArgumentException("fromDate > toDate");
        }
        this.fromDateInclusive = clean(fromDateInclusive);
        this.toDateInclusive = clean(toDateInclusive);
        String key = ProductNameNormalizer.key(storeName);
        this.storeKey = key.isEmpty() ? null : key;
    }

    public static PriceScopeV2 all() { return new PriceScopeV2(null, null, null); }
    public static PriceScopeV2 period(String fromDateInclusive, String toDateInclusive) { return new PriceScopeV2(fromDateInclusive, toDateInclusive, null); }
    public static PriceScopeV2 store(String storeName) { return new PriceScopeV2(null, null, storeName); }
    public static PriceScopeV2 periodAtStore(String fromDateInclusive, String toDateInclusive, String storeName) {
        return new PriceScopeV2(fromDateInclusive, toDateInclusive, storeName);
    }

    public boolean matches(String purchaseDate, String storeName) {
        String date = clean(purchaseDate);
        if (fromDateInclusive != null) {
            if (date == null || date.compareTo(fromDateInclusive) < 0) return false;
        }
        if (toDateInclusive != null) {
            if (date == null || date.compareTo(toDateInclusive) > 0) return false;
        }
        if (storeKey != null && !storeKey.equals(ProductNameNormalizer.key(storeName))) return false;
        return true;
    }

    private static String clean(String value) {
        if (value == null) return null;
        String v = value.trim();
        return v.isEmpty() ? null : v;
    }
}
