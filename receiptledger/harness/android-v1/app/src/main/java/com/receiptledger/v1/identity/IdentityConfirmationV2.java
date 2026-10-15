package com.receiptledger.v1.identity;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.ProductNameNormalizer;

/** CP24 least-authority alias learning after an explicit user confirmation. */
public final class IdentityConfirmationV2 {
    private IdentityConfirmationV2() {}

    public static AliasContext rememberConfirmedAlias(
            CatalogV2PersistenceStore store,
            String merchantKey,
            String rawAlias,
            String catalogEntryId,
            boolean explicitlyGlobal) {
        if (store == null) throw new IllegalArgumentException("store");
        if (store.catalogEntryV2(catalogEntryId) == null) throw new IllegalArgumentException("catalogEntryId");
        AliasContext context;
        if (explicitlyGlobal || ProductNameNormalizer.key(merchantKey).isEmpty()) {
            context = AliasContext.global();
        } else {
            context = AliasContext.merchant(merchantKey);
        }
        store.saveAliasV2(context, rawAlias, catalogEntryId);
        return context;
    }
}
