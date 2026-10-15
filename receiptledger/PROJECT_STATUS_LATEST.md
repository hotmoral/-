# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP22 — Persistence V2 — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-persistence-v2-20261016`
- predecessor handoff HEAD: `dc62d7adb650ced200fe5058aaf20f23d23fb34c`
- frozen CP22 implementation HEAD: `449896c7580fb3412f41c9b58d1ab9412d13d84d`
- canonical Actions run: `38816200340` — SUCCESS
- job: `116701369902` — SUCCESS
- artifact ID: `12010832560`
- artifact digest: `sha256:6b27c9e8aa9541346d9a3f5844c12a2f0dacd26841e869bd5b4834d7cb67bea1`
- debug APK SHA-256: `1cddd2f19c70b8ab883a97630c3dbc10e8971d75a3c9e4ec62be72eb69328884`
- migration vectors: 15/15 PASS
- Catalog Domain tests: 15/15 PASS
- Persistence V2 contract tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.20-persistence-v2` / versionCode 21

Any later commit that only synchronizes closeout/status/handoff documents is not additional CP22 implementation. The frozen executable boundary above remains canonical.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

The receipt remains source evidence. Product/commodity history and price judgment remain the user-facing destination.

## 3. CP22 result

CP22 implemented migration-safe persistence for the CP21 Catalog Domain V2 without changing receipt-price truth.

### Product/catalog database

- DB file remains `receipt-products-v1.db`;
- schema version is now `2`;
- existing product IDs/types/names/keys/creation timestamps survive migration unchanged;
- existing item links survive unchanged;
- V1 aliases migrate as GLOBAL aliases;
- merchant-scoped aliases are now persistable;
- BRAND / PRODUCT_NAME / VARIANT evidence fields are persistable;
- exact product specification is persistable;
- stable category reference is persistable;
- linked PurchaseForm semantic metadata is persistable.

### Receipt database

- DB remains `receiptledger-v1.db`;
- `ReceiptSchema.VERSION` remains `1`;
- no receipt persistence source was modified;
- unit price, line amount, purchase date, store and validation remain receipt-derived authoritative facts.

`observation_purchase_forms` deliberately contains no copied price/date/store truth.

## 4. Migration safety contract

The real SQLite V1->V2 fixture verified:

- products preserved;
- aliases preserved and moved to GLOBAL context;
- item links preserved;
- no semantic guessing from legacy names;
- products/item_links are not dropped;
- merchant alias namespace separation;
- same-context collision rejection;
- metadata/index target structure;
- catalog-local cascades;
- fresh V2 schema parity;
- receipt DB unchanged.

Unsupported catalog migration paths fail closed.

## 5. Persistence technology decision

CP22 retains direct SQLite / `SQLiteOpenHelper`.

Room was evaluated but deliberately deferred: the dominant CP22 risk was migration/data preservation, and replacing the persistence framework at the same time would expand the failure surface without advancing the product objective. Re-evaluate only if later query/search complexity or maintainability evidence justifies it.

## 6. Frozen upstream and downstream invariants

Preserve:

- stable catalog ID = identity/equality authority;
- UNCLASSIFIED remains unresolved, not a V2 entity;
- category is not identity proof;
- merchant scope contextualizes aliases but does not define SKU identity;
- HIGH confidence != CONFIRMED;
- unknown != invented default;
- package-form units have no guessed conversion;
- grouping != comparability;
- price truth remains receipt-traceable;
- false merge and false split both become explicit CP24 quality metrics;
- repeated confirmed use should reduce review burden;
- CP27 defines canonical comparison-price semantics before statistics/labels;
- CP30 Design System precedes final commercial detail-screen visual implementation.

## 7. Completed checkpoint chain

1. Foundation
2. Image Intake / Document Core
3. OCR Core
4. Layout Core
5. Structure Core
6. Item Tuple Core
7. Validation Core
8. Persistence Core
9. Image Archive Core
10. Receipt Library Core
11. Review / Edit Core
12. Product Identity Core
13. Price History Core
14. OCR Quality / Recovery Core
15. Vertical Integration Core
16. Merchant / Store Core
17. Conservative Cross-Pass Merge Core
18. Build Hygiene Core
19. Target API 36 Core
20. Product Rebaseline / V1 Master Specification
21. Catalog Domain V2
22. **Persistence V2 — COMPLETE**

## 8. Next planned checkpoint

**CP23 — Receipt Product Semantics**

Goal: convert raw receipt item text into structured semantic candidates for brand/product/variant/specification/pack/sales-unit with explicit reason/provenance/confidence, without inventing identity or gaining merge authority.

CP23 must measure local parsing coverage/accuracy and review-required burden. CP24 remains responsible for identity linking authority and false-merge/false-split metrics.

**Do not begin CP23 without explicit user authorization.**

## 9. Public/privacy invariants

ReceiptLedger may modify only:

- `receiptledger/**`
- explicitly ReceiptLedger-prefixed workflows.

Do not use other project namespaces. Never commit secrets, signing material, real private receipt photos, real personal purchase databases/backups, personal identifiers or uncleared assets.

APK permission firewall remains no CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permission unless separately authorized.

## 10. Canonical restart order

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

Then verify the branch against frozen implementation HEAD `449896c7580fb3412f41c9b58d1ab9412d13d84d`. Post-boundary closeout/handoff changes must be documentation-only unless CP23 was explicitly authorized.

**Current stop condition: CP22 is complete. Await explicit authorization for CP23.**
