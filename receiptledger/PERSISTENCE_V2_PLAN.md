# ReceiptLedger V1 — CP22 Persistence V2 Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PERSISTENCE_V2_01`
Branch: `receiptledger/run-v1-persistence-v2-20261016`
Depends on: CP21 Catalog Domain V2 + Client Requirement Alignment Amendment

## 0. Objective

Implement migration-safe SQLite persistence for the frozen CP21 catalog semantics while preserving every existing product identity and receipt-item link.

## 1. Approved implementation scope

- product catalog schema version 1 -> 2;
- explicit 1 -> 2 migration executor;
- legacy alias -> GLOBAL contextual alias migration;
- storage for catalog field evidence;
- storage for product specification;
- storage for stable category reference;
- storage for linked observation purchase form only;
- V2 persistence read/write API beside legacy ProductCatalogStore API;
- legacy exact-global-alias behavior preserved;
- deterministic host SQLite migration verifier;
- pure JVM persistence-contract tests;
- version metadata bump;
- ReceiptLedger-scoped CI/evidence.

## 2. Explicitly unchanged

- receipt DB schema/version;
- receipt rows/items/issues semantics;
- raw OCR/layout/item/validation behavior;
- item price/date/store source of truth;
- catalog stable-ID authority;
- exact alias resolver authority beyond adding storage context;
- user-facing Activities/navigation;
- permissions/network posture;
- CP23 semantic parsing and CP24 resolver logic.

## 3. Product catalog schema V2

### products

Existing columns remain unchanged and gain:

- `record_origin TEXT NOT NULL DEFAULT 'LEGACY_V1'`

Current legacy UI/runtime-created rows continue to use the compatibility default until later checkpoints wire native V2 authoring.

### aliases

Columns:

- `scope`
- `merchant_key`
- `alias_key`
- `raw_alias`
- `product_id`

Primary key:

`(scope,merchant_key,alias_key)`

The same POS alias may therefore exist in separate merchant namespaces without collision. Legacy/global lookup is explicitly restricted to `GLOBAL + empty merchant key`.

### catalog_fields

One row per `(product_id,field_code)` for BRAND / PRODUCT_NAME / VARIANT.

Stores:

- value text;
- normalized lookup key;
- source;
- confidence;
- confirmation.

### product_specifications

One row per STANDARD product, with exact decimal text and unit enums for net/inner content, optional pack count, plus source/confidence/confirmation.

### category_refs

One stable category ID per catalog entity. No taxonomy table is introduced yet.

### observation_purchase_forms

One semantic purchase-form row per linked receipt item. Foreign key targets `item_links(receipt_id,item_ordinal)` inside the catalog DB so unlinking also removes its semantic overlay.

No price columns are allowed here.

## 4. Migration algorithm 1 -> 2

1. add `products.record_origin` with `LEGACY_V1` default;
2. rename old global alias table;
3. create context-aware alias table under a temporary name;
4. copy every old alias as GLOBAL / empty merchant key;
5. drop only the old alias table;
6. rename the V2 alias table into place;
7. create alias product index;
8. create catalog fields/spec/category/purchase-form tables and indexes;
9. leave products and item_links rows untouched.

Unsupported upgrade paths throw.

## 5. V2 persistence API

A separate `CatalogV2PersistenceStore` contract is added so legacy runtime consumers do not need to change type immediately.

Required operations:

- save/read one `CatalogEntryV2`;
- save/read contextual alias target;
- save/read purchase-form semantic field.

Rules:

- existing product ID may not silently change type, canonical name, creation timestamp or record origin through a metadata save;
- absent semantic fields delete only their V2 metadata row, never the catalog entity;
- save of a commodity must not persist STANDARD-only fields/specification;
- alias collision is evaluated within context, not globally across all contexts;
- purchase form may exist only for an existing item link;
- values are rehydrated into CP21 domain types with strict enum/decimal parsing.

## 6. Migration regression vectors

Host SQLite fixture must prove:

1. all V1 product IDs survive unchanged;
2. type/name/key/created timestamp survive unchanged;
3. all aliases survive as GLOBAL context unchanged;
4. all item links and link sources survive unchanged;
5. no semantic fields/spec/category/purchase form are invented;
6. same alias key can coexist under two different merchant keys after migration;
7. same alias key in one context cannot target two products;
8. catalog-field/category indexes exist;
9. purchase-form table contains no price truth;
10. cascade from product removal continues through aliases/links and their V2 dependent rows;
11. fresh V2 schema creation has the same target structure;
12. receipt schema remains version 1.

## 7. Acceptance criteria

CP22 is PASS only if:

- migration fixture passes all vectors;
- ProductCatalogSchema.VERSION = 2;
- ReceiptSchema.VERSION = 1;
- database filename stays `receipt-products-v1.db`;
- legacy exact-global alias behavior remains deterministic;
- existing full unit suite passes;
- CP22 persistence JVM tests pass;
- lint = 0 errors / 0 warnings;
- assembleDebug succeeds;
- forbidden APK permission audit remains clean;
- diff contains only CP22-approved files;
- exact implementation/evidence refs are recorded;
- status/handoff documents are synchronized after the frozen implementation boundary.

## 8. Stop condition

After CP22 closeout, stop. Do not start CP23 Receipt Product Semantics without explicit user direction.
