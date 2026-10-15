# ReceiptLedger V1 — CP22 Persistence V2 Consistency Review

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PERSISTENCE_V2_01`

## Executive result

**COMPATIBLE / NO BLOCKING CONTRADICTION.**

The lowest-risk implementation is a product-catalog-only schema migration that keeps receipt evidence authoritative and leaves CP21 semantics unchanged.

## 1. Identity review

Risk: migration could collapse rows because canonical names or new semantic fields look equivalent.

Control:

- products table is not rebuilt;
- IDs are never regenerated;
- no semantic parsing during migration;
- no merge SQL exists;
- existing canonical key uniqueness is preserved but does not become a V2 equality rule.

Result: stable-ID authority preserved.

## 2. Alias review

Risk: V1 global alias primary key cannot represent merchant-scoped aliases.

Control:

- rebuild only aliases table;
- each V1 alias is copied exactly once as GLOBAL;
- new primary key includes scope + merchant key + alias key;
- legacy resolver explicitly queries GLOBAL context only.

Result: merchant namespace becomes persistable without changing current auto-link authority.

## 3. Receipt/price-truth review

Risk: persisting PurchaseObservation fields could duplicate prices and diverge from saved receipts.

Control:

- receipt DB remains version 1;
- no price/date/store columns are added to catalog observation metadata;
- only PurchaseForm semantic overlay is persisted;
- later observation projection still reads numeric/store/date facts from receipt storage.

Result: receipt-derived price truth remains intact.

## 4. Cross-database lifecycle review

Receipt and product data live in separate SQLite databases. Cross-database foreign keys are unavailable.

Existing item links therefore remain logical references and deletion coordination remains an application responsibility. CP22 does not pretend to create impossible cross-DB referential integrity.

Within the product DB, new purchase-form metadata is allowed only for an existing item link and cascades when the link disappears.

## 5. Unit/comparability review

V2 persistence stores exact decimal/unit codes but defines no comparison API and no conversion for BAG/PACK/BOX/BUNDLE.

Result: persistence cannot accidentally upgrade grouping into comparability.

## 6. Provenance review

Catalog semantic field rows and purchase-form rows persist source/confidence/confirmation independently.

Result: HIGH confidence cannot be reconstructed as CONFIRMED by storage shortcuts.

## 7. Legacy runtime compatibility

Current `ProductCatalogStore` API remains available.

Required compatibility adjustments are limited to:

- schema upgrade delegation;
- fresh V2 table creation;
- GLOBAL alias insert/query columns.

No identity resolver policy change is introduced.

## 8. Direct SQLite vs Room

Room offers useful compile-time SQL validation and migration facilities, but migrating frameworks in the same checkpoint would expand the blast radius beyond the client goal. Current direct SQLite is retained for CP22; later migration remains possible if query complexity provides evidence for it.

Result: avoid architecture churn while preserving an upgrade path.

## 9. Performance/index review

Only obvious downstream indexes are added. No price cache, duplicate observation table or speculative search materialization is introduced.

Result: sufficient for CP23/24/25/29 without premature optimization.

## 10. Failure/rollback review

- 1->2 is the only supported upgrade path;
- migration uses additive product column + alias rebuild + new tables;
- products and item_links are never dropped;
- actual SQLite fixture validates migration before acceptance;
- unsupported path fails closed.

Result: migration failure is detectable rather than silently destructive.

## 11. Client-requirement alignment

This storage work directly supports the client's product goal by enabling:

- richer exact product identity metadata;
- merchant-aware repeat-product learning;
- category references;
- non-standard purchase forms;
- later search and price-memory queries.

It deliberately does not add unrelated budgeting/cloud/e-commerce scope.

## 12. Conclusion

CP22 may proceed with the product-DB-only V2 migration. No CP20/CP21 contract amendment is required.
