package com.receiptledger.v1.identity;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import java.util.List;

/** Read-only knowledge surface used by CP24. */
public interface IdentityKnowledgeV2 {
    String exactAliasCatalogEntryId(AliasContext context, String rawAlias);
    CatalogEntryV2 catalogEntry(String catalogEntryId);
    List<CatalogEntryV2> catalogEntries();
}
