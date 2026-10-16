package com.receiptledger.v1.search;

import com.receiptledger.v1.product.ProductType;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Product/commodity-level read model. Search relevance never becomes identity authority. */
public final class SearchBrowseEntryV1 {
    public final String productId;
    public final ProductType type;
    public final String canonicalName;
    public final String brand;
    public final String productName;
    public final String variant;
    public final String specificationSummary;
    public final String categoryId;
    public final String categoryPath;
    public final List<String> observedItemNames;
    public final List<String> stores;
    public final int purchaseCount;
    public final String latestPurchaseDate;
    public final String latestStoreName;
    public final long latestCreatedAtMillis;
    public final int relevanceScore;
    public final String matchReason;

    SearchBrowseEntryV1(
            String productId,
            ProductType type,
            String canonicalName,
            String brand,
            String productName,
            String variant,
            String specificationSummary,
            String categoryId,
            String categoryPath,
            List<String> observedItemNames,
            List<String> stores,
            int purchaseCount,
            String latestPurchaseDate,
            String latestStoreName,
            long latestCreatedAtMillis,
            int relevanceScore,
            String matchReason) {
        this.productId = productId;
        this.type = type;
        this.canonicalName = canonicalName;
        this.brand = brand;
        this.productName = productName;
        this.variant = variant;
        this.specificationSummary = specificationSummary;
        this.categoryId = categoryId;
        this.categoryPath = categoryPath;
        this.observedItemNames = immutable(observedItemNames);
        this.stores = immutable(stores);
        this.purchaseCount = purchaseCount;
        this.latestPurchaseDate = latestPurchaseDate;
        this.latestStoreName = latestStoreName;
        this.latestCreatedAtMillis = latestCreatedAtMillis;
        this.relevanceScore = relevanceScore;
        this.matchReason = matchReason;
    }

    SearchBrowseEntryV1 withMatch(int score, String reason) {
        return new SearchBrowseEntryV1(productId, type, canonicalName, brand, productName, variant,
                specificationSummary, categoryId, categoryPath, observedItemNames, stores, purchaseCount,
                latestPurchaseDate, latestStoreName, latestCreatedAtMillis, score, reason);
    }

    private static List<String> immutable(List<String> values) {
        return Collections.unmodifiableList(new ArrayList<>(values == null ? Collections.<String>emptyList() : values));
    }
}
