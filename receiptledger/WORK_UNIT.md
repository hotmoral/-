# ReceiptLedger public execution work unit

## Current stage

**CP22 — Persistence V2 is COMPLETE.**

- branch: `receiptledger/run-v1-persistence-v2-20261016`
- predecessor handoff: `dc62d7adb650ced200fe5058aaf20f23d23fb34c`
- frozen implementation HEAD: `449896c7580fb3412f41c9b58d1ab9412d13d84d`
- canonical Actions run: `38816200340` — SUCCESS
- artifact ID: `12010832560`
- artifact digest: `sha256:6b27c9e8aa9541346d9a3f5844c12a2f0dacd26841e869bd5b4834d7cb67bea1`
- debug APK SHA-256: `1cddd2f19c70b8ab883a97630c3dbc10e8971d75a3c9e4ec62be72eb69328884`
- migration vectors: 15/15 PASS
- Catalog Domain tests: 15/15 PASS
- Persistence V2 tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionCode 21
- versionName `1.0.20-persistence-v2`

Post-implementation handoff commits must remain documentation-only until CP23 is explicitly authorized.

## What is now frozen

### Product catalog persistence

- existing DB filename remains `receipt-products-v1.db`;
- product schema is V2;
- existing product IDs/types/names/keys/creation times are preserved;
- existing item links are preserved;
- legacy aliases migrate as GLOBAL aliases;
- GLOBAL and MERCHANT alias contexts can be stored independently;
- catalog semantic fields retain source/confidence/confirmation;
- product specification uses exact decimal/unit representation;
- stable category reference can be persisted;
- linked PurchaseForm semantics can be persisted.

### Receipt persistence

- receipt DB remains schema V1;
- receipt persistence source is unchanged;
- quantity/unit-price/line-amount provenance, date, store and validation remain authoritative receipt evidence;
- no independent copied purchase-price truth was introduced.

### Persistence technology

- direct SQLite / `SQLiteOpenHelper` retained;
- Room migration deferred until later evidence justifies the additional framework change.

## Critical downstream constraints

CP23+ must not:

- regenerate/merge stable product IDs during semantic parsing;
- treat migrated empty semantic fields as evidence that values do not exist;
- turn GLOBAL legacy aliases into guessed merchant aliases;
- copy receipt price/date/store truth into new catalog metadata tables;
- treat PurchaseForm persistence as comparability authority;
- conflate parser confidence with confirmation.

## Next planned work unit

**CP23 — Receipt Product Semantics**

Purpose:
extract structured candidates from receipt product text for brand/product/variant/specification/pack/sales-unit with explicit reason, provenance and confidence.

Acceptance direction already frozen:

- unresolved ambiguity is allowed;
- missing values are not invented;
- parser output is candidate evidence, not product merge authority;
- parsing coverage/accuracy and review-required burden are measured locally;
- prepare data for CP24 without implementing CP24 resolver policy.

## Group discipline

- recover canonical GitHub state;
- state essential goal/non-goals;
- inspect materially affected consistency risks;
- fix cheap contradictions before implementation;
- avoid unrelated cleanup/architecture churn;
- implement the smallest coherent proof;
- run scoped CI/evidence for executable changes;
- freeze exact implementation/evidence refs;
- synchronize handoff/status materials;
- stop before the next unauthorized checkpoint.

## Public/privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows.

Never include secrets, signing material, real private receipt photos, personal purchase DBs/backups, personal identifiers or uncleared assets.

APK permission firewall remains no CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permission unless explicitly reauthorized.

## Stop condition

**CP22 is closed. Await explicit authorization for CP23.**
