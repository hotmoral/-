package com.receiptledger.v1.search;

import com.receiptledger.v1.product.ProductType;

/** Immutable CP29 search/filter request. */
public final class SearchBrowseQueryV1 {
    public final String text;
    public final String categoryId;
    public final String storeName;
    public final ProductType productType;
    public final int limit;

    public SearchBrowseQueryV1(String text, String categoryId, String storeName, ProductType productType, int limit) {
        if (limit < 1 || limit > 100) throw new IllegalArgumentException("limit must be 1..100");
        this.text = clean(text);
        this.categoryId = clean(categoryId);
        this.storeName = clean(storeName);
        this.productType = productType;
        this.limit = limit;
    }

    public static SearchBrowseQueryV1 all(int limit) {
        return new SearchBrowseQueryV1(null, null, null, null, limit);
    }

    public static SearchBrowseQueryV1 text(String text, int limit) {
        return new SearchBrowseQueryV1(text, null, null, null, limit);
    }

    public boolean hasText() { return text != null; }
    public boolean hasCategory() { return categoryId != null; }
    public boolean hasStore() { return storeName != null; }

    private static String clean(String value) {
        if (value == null) return null;
        String v = value.trim();
        return v.isEmpty() ? null : v;
    }
}
