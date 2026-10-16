package com.receiptledger.v1.commodity;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CatalogKind;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.identity.IdentityConfirmationV2;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.semantics.SemanticCandidate;

/** Explicit user-confirmation helpers for CP26. No implicit entity creation or merging. */
public final class CommodityConfirmationV2 {
    private CommodityConfirmationV2() {}

    public static AliasContext rememberConfirmedGrouping(
            CatalogV2PersistenceStore store,
            String merchantKey,
            String rawAlias,
            String commodityId,
            boolean explicitlyGlobal) {
        if (store == null) throw new IllegalArgumentException("store");
        CatalogEntryV2 entry = store.catalogEntryV2(commodityId);
        if (entry == null || entry.kind != CatalogKind.NON_STANDARD_COMMODITY) {
            throw new IllegalArgumentException("commodityId must reference NON_STANDARD_COMMODITY");
        }
        return IdentityConfirmationV2.rememberConfirmedAlias(
                store, merchantKey, rawAlias, commodityId, explicitlyGlobal);
    }

    /** Persists CP23 purchase-form evidence unchanged; confirmation state is not upgraded here. */
    public static void persistObservedPurchaseForm(
            CatalogV2PersistenceStore store,
            String receiptId,
            int itemOrdinal,
            SemanticCandidate<PurchaseForm> purchaseForm) {
        if (store == null) throw new IllegalArgumentException("store");
        CatalogField<PurchaseForm> field = purchaseForm == null
                ? CatalogField.<PurchaseForm>absent()
                : purchaseForm.asCatalogField();
        store.savePurchaseFormV2(receiptId, itemOrdinal, field);
    }
}
