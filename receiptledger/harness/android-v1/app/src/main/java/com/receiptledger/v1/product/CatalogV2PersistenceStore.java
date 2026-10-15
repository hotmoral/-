package com.receiptledger.v1.product;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;

/** Storage-facing V2 contract kept separate from the legacy ProductCatalogStore API. */
public interface CatalogV2PersistenceStore {
    CatalogEntryV2 catalogEntryV2(String catalogEntryId);
    void saveCatalogEntryV2(CatalogEntryV2 entry);
    void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId);
    String aliasCatalogEntryIdV2(AliasContext context, String rawAlias);
    void savePurchaseFormV2(String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm);
    CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal);
}
