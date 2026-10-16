package com.receiptledger.v1.category;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CategoryRef;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;

/** Category assignment facade over the frozen CP22 persistence contract. */
public final class CategoryAssignmentServiceV1 {
    private final CatalogV2PersistenceStore store;
    private final CategoryClassifierV1 classifier;

    public CategoryAssignmentServiceV1(CatalogV2PersistenceStore store) {
        this(store, new CategoryClassifierV1());
    }

    CategoryAssignmentServiceV1(CatalogV2PersistenceStore store, CategoryClassifierV1 classifier) {
        if (store == null || classifier == null) throw new IllegalArgumentException("store/classifier");
        this.store = store;
        this.classifier = classifier;
    }

    public CategoryDecisionV1 decision(String catalogEntryId) {
        CatalogEntryV2 entry = requireEntry(catalogEntryId);
        return classifier.classify(entry);
    }

    /** Persists the current high-confidence suggestion. No identity or alias data is changed. */
    public CategoryRef acceptAutomaticSuggestion(String catalogEntryId) {
        CategoryDecisionV1 decision = decision(catalogEntryId);
        if (!decision.canAutoAssign() || decision.category == null) {
            throw new IllegalStateException("category is not auto-assignable");
        }
        assign(catalogEntryId, decision.category);
        return decision.category;
    }

    /** User correction/confirmation. Replaces only category metadata on the same stable catalog id. */
    public void assign(String catalogEntryId, CategoryRef category) {
        if (category == null) throw new IllegalArgumentException("category");
        CategoryTaxonomyV1.require(category.id);
        CatalogEntryV2 old = requireEntry(catalogEntryId);
        CatalogEntryV2 updated = CatalogEntryV2.rehydrate(
                old.id,
                old.kind,
                old.canonicalName,
                old.brand,
                old.productName,
                old.variant,
                old.specification,
                category,
                old.createdAtMillis,
                old.recordOrigin);
        store.saveCatalogEntryV2(updated);
    }

    public void clear(String catalogEntryId) {
        CatalogEntryV2 old = requireEntry(catalogEntryId);
        CatalogEntryV2 updated = CatalogEntryV2.rehydrate(
                old.id,
                old.kind,
                old.canonicalName,
                old.brand,
                old.productName,
                old.variant,
                old.specification,
                null,
                old.createdAtMillis,
                old.recordOrigin);
        store.saveCatalogEntryV2(updated);
    }

    private CatalogEntryV2 requireEntry(String id) {
        String clean = id == null ? "" : id.trim();
        if (clean.isEmpty()) throw new IllegalArgumentException("catalogEntryId");
        CatalogEntryV2 entry = store.catalogEntryV2(clean);
        if (entry == null) throw new IllegalArgumentException("unknown catalog entry: " + clean);
        return entry;
    }
}
