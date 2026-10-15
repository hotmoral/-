# ReceiptLedger V1 — CP22 Persistence V2 Closeout

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PERSISTENCE_V2_01`
Status: **PASS / COMPLETE**

## 1. Frozen implementation

- branch: `receiptledger/run-v1-persistence-v2-20261016`
- frozen implementation HEAD: `449896c7580fb3412f41c9b58d1ab9412d13d84d`
- canonical Actions run: `38816200340` — SUCCESS
- artifact ID: `12010832560`
- artifact digest: `sha256:6b27c9e8aa9541346d9a3f5844c12a2f0dacd26841e869bd5b4834d7cb67bea1`
- debug APK SHA-256: `1cddd2f19c70b8ab883a97630c3dbc10e8971d75a3c9e4ec62be72eb69328884`
- lint: 0 errors / 0 warnings

## 2. What changed

Only the product/catalog persistence layer advanced to V2.

Product database:

- file remains `receipt-products-v1.db`;
- schema version is now `2`;
- existing product IDs/types/names/keys/creation times are preserved;
- existing item links are preserved;
- legacy aliases migrate one-for-one into GLOBAL context;
- merchant-scoped alias namespaces are now persistable;
- Catalog Domain V2 semantic field evidence is persistable;
- product specification is persistable with exact decimal/unit representation;
- stable category reference is persistable;
- linked purchase-form semantics are persistable without copying price truth.

Receipt database:

- remains `receiptledger-v1.db`;
- schema version remains `1`;
- receipt/item numeric evidence, date, store and validation remain authoritative.

## 3. What deliberately did not change

CP22 does not:

- parse brand/product/specification from receipt text;
- change resolver/fuzzy matching authority;
- create category taxonomy;
- define NON_STANDARD comparison rules;
- define comparison-price statistics or cheap/expensive thresholds;
- redesign UI/navigation;
- add network capability or new permissions;
- move to Room;
- create a duplicate purchase-price history truth table.

## 4. Migration safety result

The V1->V2 migration was exercised against a real SQLite fixture before closeout.

Verified:

- stable IDs survive unchanged;
- item links survive unchanged;
- aliases survive as GLOBAL context;
- no legacy semantic guessing occurs;
- `products` and `item_links` are not dropped/rebuilt;
- merchant alias namespaces work without global collision;
- unsupported migration paths fail closed;
- fresh V2 schema and migrated V2 schema reach the intended target;
- receipt DB remains untouched.

## 5. Direct SQLite decision

CP22 retains `SQLiteOpenHelper`.

Room was evaluated but not introduced because combining framework migration with data-schema migration would add failure modes without improving the essential client goal at this checkpoint. Room remains a later option if search/query complexity or maintainability evidence justifies it.

## 6. Consistency result

**COMPATIBLE WITH CP20 / CP21 / client-alignment amendment.**

No identity, provenance, unit, comparison, privacy or price-truth contradiction was introduced.

In particular:

- stable ID remains identity authority;
- category remains non-authoritative for identity;
- HIGH confidence remains distinct from CONFIRMED;
- grouping remains distinct from comparability;
- false-merge / false-split acceptance requirements remain downstream CP24 concerns;
- price basis remains a CP27 contract;
- repeated-use automation remains a CP23–CP26 quality requirement.

## 7. Next planned checkpoint

**CP23 — Receipt Product Semantics**

Its purpose is to parse brand/product/variant/specification/pack/sales-unit candidates from receipt item text with confidence/reason/provenance while preserving unresolved ambiguity.

CP23 must include local quality evidence for parsing coverage/accuracy and review burden. It must not silently gain product-merge authority; CP24 owns identity resolver authority.

CP23 is not started by this closeout. Explicit user direction is required.
