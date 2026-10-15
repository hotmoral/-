package com.receiptledger.v1.identity;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.ProductCatalogStore;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/** Read-only adapter over the existing CP22 stores; no schema changes or writes. */
public final class CatalogIdentityKnowledgeAdapter implements IdentityKnowledgeV2 {
    private final ProductCatalogStore catalogStore;
    private final CatalogV2PersistenceStore v2Store;

    public CatalogIdentityKnowledgeAdapter(ProductCatalogStore catalogStore, CatalogV2PersistenceStore v2Store) {
        if (catalogStore == null || v2Store == null) throw new IllegalArgumentException("stores");
        this.catalogStore = catalogStore;
        this.v2Store = v2Store;
    }

    @Override public String exactAliasCatalogEntryId(AliasContext context, String rawAlias) {
        return v2Store.aliasCatalogEntryIdV2(context, rawAlias);
    }

    @Override public CatalogEntryV2 catalogEntry(String catalogEntryId) {
        return v2Store.catalogEntryV2(catalogEntryId);
    }

    @Override public List<CatalogEntryV2> catalogEntries() {
        List<CatalogEntryV2> out = new ArrayList<>();
        for (CatalogProduct product : catalogStore.listProducts()) {
            CatalogEntryV2 entry = v2Store.catalogEntryV2(product.id);
            if (entry != null) out.add(entry);
        }
        Collections.sort(out, new Comparator<CatalogEntryV2>() {
            @Override public int compare(CatalogEntryV2 a, CatalogEntryV2 b) {
                return a.id.compareTo(b.id);
            }
        });
        return Collections.unmodifiableList(out);
    }
}
