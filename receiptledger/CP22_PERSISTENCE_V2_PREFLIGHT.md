# ReceiptLedger V1 — CP22 Persistence V2 Preflight

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PERSISTENCE_V2_01`
Branch: `receiptledger/run-v1-persistence-v2-20261016`
Base handoff HEAD: `dc62d7adb650ced200fe5058aaf20f23d23fb34c`

## 0. Objective

Freeze the cheapest safe persistence boundary before changing any schema.

CP22 exists to persist the already-frozen CP21 Catalog Domain V2 without reinterpreting identity, units, provenance, or price truth.

## 1. Existing database inventory

### Receipt database

File: `receiptledger-v1.db`
Schema version: `1`
Owner: `SqliteReceiptStore`

Tables:

- `receipts`
- `receipt_items`
- `receipt_issues`

Authoritative facts already stored here include receipt ID, purchase date, store, raw OCR text, validation state, item raw name, quantity, unit price, line amount and their numeric provenance.

Decision: **Receipt DB remains schema version 1 in CP22.**

Reason: CP22 has no requirement to change these authoritative receipt facts. Moving or duplicating price/date/store values would increase migration risk and violate the receipt-derived price-truth direction.

### Product/catalog database

File: `receipt-products-v1.db`
Schema version before CP22: `1`
Owner: `SqliteProductCatalogStore`

Tables:

- `products(id,type,canonical_name,canonical_key,created_at_ms)`
- `aliases(alias_key,raw_alias,product_id)`
- `item_links(receipt_id,item_ordinal,product_id,link_source)`

Important boundary: `item_links` references receipt items logically by `(receipt_id,item_ordinal)` across a separate database. SQLite cannot enforce a cross-database foreign key here, so application lifecycle must continue unlinking receipt links explicitly when receipts are removed.

## 2. CP21 meanings that persistence may not reinterpret

- stable catalog ID is catalog identity/equality authority;
- separate legacy IDs must never collapse during migration;
- STANDARD/NON_STANDARD meaning is preserved;
- UNCLASSIFIED is unresolved and has no V2 catalog row;
- category is descriptive metadata, not identity authority;
- merchant alias scope is context, not SKU identity;
- HIGH confidence is not CONFIRMED;
- unknown is not a default value;
- grouping is not price comparability;
- package forms have no guessed physical conversion;
- price truth remains receipt-traceable.

## 3. Migration boundary decision

Only the product/catalog DB advances from schema 1 to schema 2.

V2 storage extends the existing database instead of creating a second catalog database or replacing legacy IDs.

Preserved in place:

- database filename;
- every `products.id`;
- legacy `type`;
- `canonical_name`;
- `canonical_key`;
- `created_at_ms`;
- every item-link tuple and link source.

Legacy alias rows migrate one-for-one into GLOBAL alias context.

No canonical name is parsed during migration. No brand, specification, category or merchant scope is guessed.

## 4. V2 storage additions

### `products`

Add `record_origin`, defaulting legacy rows to `LEGACY_V1`.

### context-aware `aliases`

Replace the global-only primary key with:

`(scope, merchant_key, alias_key)`

Storage mapping:

- GLOBAL -> `scope='GLOBAL'`, `merchant_key=''`
- MERCHANT -> `scope='MERCHANT'`, non-empty normalized merchant key

Every V1 alias migrates as GLOBAL with the exact alias key, raw alias and product ID preserved.

### `catalog_fields`

Stores BRAND / PRODUCT_NAME / VARIANT semantic values plus independent source, confidence and confirmation.

### `product_specifications`

Stores exact product specification values plus field evidence state. Decimal quantities are stored as canonical decimal text so no binary floating-point precision is introduced.

### `category_refs`

Stores only stable category IDs. Taxonomy/hierarchy remains CP25.

### `observation_purchase_forms`

Stores only purchase-form semantics for an already-linked receipt item:

- exact decimal quantity text;
- unit code;
- raw unit label;
- source/confidence/confirmation.

It deliberately stores **no unit price, line amount, store or purchase date**. Those remain in the receipt DB and are joined logically when a PurchaseObservation is projected.

## 5. Direct SQLite vs Room decision

Decision for CP22: **retain direct SQLite / SQLiteOpenHelper**.

Reasons:

1. current stores and migration surface are small and already proven;
2. the highest CP22 risk is data-preservation correctness, not query boilerplate;
3. introducing Room now would combine a persistence-framework migration with a schema migration, increasing the number of simultaneous failure modes;
4. no CP22 query requires Room-only capability;
5. Room can be reconsidered incrementally later if CP29 search/query complexity or CP36 maintainability evidence justifies it.

Current Android documentation was reviewed and confirms both Room's benefits and an incremental SQLite-to-Room path. CP22 therefore does not reject Room; it defers the framework migration because it is not necessary to achieve this checkpoint's product goal.

## 6. Migration failure policy

- only explicit `1 -> 2` upgrade is accepted;
- unsupported version paths fail closed;
- no `DROP TABLE products`;
- no `DROP TABLE item_links`;
- alias-table rebuild must preserve row count and values;
- migration is exercised against a deterministic V1 SQLite fixture before acceptance;
- fresh V2 database creation is tested separately from V1 migration;
- receipt DB version must remain 1.

## 7. Query/index needs frozen for later checkpoints

CP22 provides only indexes with clear downstream need:

- aliases -> product lookup;
- semantic field `(field_code,value_key)` candidate lookup;
- category -> products lookup;
- existing item-link -> product index remains unchanged.

Do not add speculative caches or duplicate price-history tables.

## 8. Scope/non-goals

CP22 does not:

- parse receipt item semantics;
- change identity resolver authority;
- define category taxonomy;
- define commodity comparability;
- compute price statistics/judgment;
- redesign UI;
- migrate receipt DB;
- add network/permissions;
- migrate to Room.

## 9. Preflight result

**PASS — controlled product-DB-only migration is compatible with CP20/CP21 and the client-alignment amendment.**
