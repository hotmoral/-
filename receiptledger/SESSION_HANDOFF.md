# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct ReceiptLedger execution state from old chat before reading current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP22_PERSISTENCE_V2_CLOSEOUT.md`
4. `receiptledger/CP22_PERSISTENCE_V2_EVIDENCE.md`
5. `receiptledger/PERSISTENCE_V2_PLAN.md`
6. `receiptledger/PERSISTENCE_V2_CONSISTENCY_REVIEW.md`
7. `receiptledger/PERSISTENCE_V2_GOLDEN_VECTORS.md`
8. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
9. `receiptledger/CATALOG_DOMAIN_V2_PLAN.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP22 — Persistence V2 — PASS / COMPLETE**

- branch: `receiptledger/run-v1-persistence-v2-20261016`
- predecessor handoff HEAD: `dc62d7adb650ced200fe5058aaf20f23d23fb34c`
- frozen implementation HEAD: `449896c7580fb3412f41c9b58d1ab9412d13d84d`
- canonical Actions run: `38816200340` — SUCCESS
- job: `116701369902` — SUCCESS
- artifact ID: `12010832560`
- artifact digest: `sha256:6b27c9e8aa9541346d9a3f5844c12a2f0dacd26841e869bd5b4834d7cb67bea1`
- debug APK SHA-256: `1cddd2f19c70b8ab883a97630c3dbc10e8971d75a3c9e4ec62be72eb69328884`
- migration vectors: 15/15 PASS
- CatalogDomainV2Test: 15/15 PASS
- CatalogPersistenceContractV2Test: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionName `1.0.20-persistence-v2`, versionCode 21

The implementation/evidence boundary remains `449896c...` even after later documentation-only handoff commits.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색 -> 과거 가격과 현재 가격 판단`

Receipt is evidence/input; product/commodity history and price judgment are the destination.

## 3. CP22 persistence contract

### Product database

File remains:
`receipt-products-v1.db`

Schema is now version 2.

Migration preserves in place:

- product ID;
- type;
- canonical name/key;
- creation timestamp;
- every item link and link source.

Legacy aliases migrate one-for-one to GLOBAL context.

V2 storage now supports:

- GLOBAL / MERCHANT alias namespaces;
- BRAND / PRODUCT_NAME / VARIANT fields with source/confidence/confirmation;
- exact package specification;
- stable category reference;
- linked observation PurchaseForm semantics.

### Receipt database

File remains:
`receiptledger-v1.db`

Schema remains version 1 and source is unchanged.

Authoritative receipt facts remain there:

- raw item name;
- quantity / unit price / line amount and provenance;
- purchase date;
- store;
- receipt validation.

Do not create a duplicate price truth from CP22 metadata.

## 4. Critical migration guardrails

CP23 and later checkpoints must not reinterpret these facts:

1. stable ID remains identity authority;
2. migrated legacy rows are not semantically parsed by migration;
3. separate old IDs remain separate;
4. V1 aliases are GLOBAL, not guessed merchant aliases;
5. merchant scope is contextual alias knowledge, not SKU identity;
6. PurchaseForm persistence is semantic overlay only;
7. PurchaseForm storage does not prove cross-unit comparability;
8. receipt price/date/store/validation remain authoritative;
9. unsupported catalog migration paths fail closed;
10. receipt DB was not migrated.

## 5. Direct SQLite / Room decision

CP22 deliberately retains `SQLiteOpenHelper`.

Reason: schema migration correctness and data preservation were the checkpoint's risk center. Simultaneously migrating to Room would add architecture churn without advancing the core product outcome.

Room remains a future option if later search/query complexity or maintainability evidence justifies it. Do not reopen this choice ritualistically in CP23.

## 6. CP21 / client-alignment invariants still governing

- STANDARD_PRODUCT vs NON_STANDARD_COMMODITY;
- UNCLASSIFIED remains unresolved;
- category is not identity authority;
- HIGH confidence != CONFIRMED;
- unknown != invented default;
- exact physical unit equivalence only where mathematically defensible;
- BAG/PACK/BOX/BUNDLE have no guessed conversion;
- grouping != comparability;
- false merge remains higher severity but false split is also a product failure;
- repeat confirmed use should reduce review burden;
- CP27 defines canonical comparison-price semantics before price statistics;
- CP30 Design System Foundation precedes final commercial detail-screen polish.

## 7. Next planned checkpoint

**CP23 — Receipt Product Semantics**

Purpose:
parse structured semantic candidates from raw receipt item text:

- brand;
- product/family name;
- variant;
- net quantity/unit;
- pack count / inner content when evidenced;
- purchase/sales-unit candidate where evidenced.

Required behavior:

- output confidence/reason/provenance;
- preserve ambiguity;
- no automatic product merge authority;
- no invented missing fields;
- local parsing coverage/accuracy and review-required metrics;
- prepare evidence for CP24 without doing CP24's resolver job.

CP23 must not start automatically. Explicit user authorization is required.

## 8. Existing foundations to preserve

- external camera/system picker privacy model;
- local Korean OCR;
- EXIF/document correction;
- coordinate preservation;
- geometry-based layout reconstruction;
- item extraction with provenance;
- arithmetic validation / contradiction preservation;
- bounded OCR recovery / conservative merge;
- review/edit before save;
- app-private receipt/image storage;
- merchant/store evidence;
- receipt-derived price history;
- API36/lint/permission firewall.

## 9. Public/security boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Do not use other project namespaces. Never commit secrets, release signing material, real private receipt photos, personal purchase DBs/backups, personal identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

## 10. Stop condition

**CP22 is complete and handoff-synchronized. Await explicit authorization for CP23.**
