# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

The latest completed checkpoint is **CP21 — Catalog Domain V2**.

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- predecessor CP20 handoff HEAD: `3149beb339a2d541a61a694fb1f052556a95c8c1`
- frozen CP21 implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical successful Actions run: `38808985222` — **SUCCESS**
- job: `116677102660` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- debug APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- CP21 domain tests: **15/15 PASS**
- Android lint: **0 errors / 0 warnings** (`No issues found.`)
- result: **PASS / COMPLETE**

Current Android build contract:

- application ID: `com.receiptledger.v1`
- AGP: `8.11.1`
- Gradle: `8.13`
- JDK / Java: `17`
- compileSdk: `36`
- targetSdk: `36`
- minSdk: `23`
- versionCode: `20`
- versionName: `1.0.19-catalog-domain-v2`

The frozen implementation HEAD above is the code/evidence boundary. Any later commit on this branch made to synchronize closeout/status/handoff documentation must remain documentation-only and must not be mistaken for additional CP21 implementation.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

The receipt is source evidence. Product/commodity history and price judgment are the user-facing destination.

## 3. CP21 result

CP21 added a storage-independent pure-Java Catalog Domain V2 beside the existing V1 product runtime. It did not migrate persistence or change normal app UI behavior.

Frozen meanings:

- `STANDARD_PRODUCT`: repeatable packaged/manufactured commercial identity;
- `NON_STANDARD_COMMODITY`: one semantic commodity that may hold different raw purchase forms;
- legacy `UNCLASSIFIED`: unresolved state, not a V2 catalog entity;
- stable catalog ID is the only catalog-entity equality authority;
- structured brand/product/variant/specification metadata does not silently merge IDs;
- category is descriptive browse metadata, not identity authority;
- alias context supports global and merchant-scoped namespaces;
- source, confidence and confirmation are independent;
- HIGH confidence does not equal CONFIRMED;
- exact kg/g and L/mL equivalence is allowed only for exact physical package measurement;
- package forms such as BAG/PACK/BOX/BUNDLE have no guessed physical conversion;
- NON_STANDARD grouping does not imply cross-form price comparability;
- missing pack count remains unknown and is not defaulted to 1;
- purchase observations remain logical receipt-linked projections, not a second persisted price truth source.

## 4. Legacy compatibility / persistence boundary

The proven V1 product runtime remains intact.

CP21 explicitly did **not** change:

- `ProductCatalogSchema.VERSION` — remains **1**;
- legacy `product/**` runtime;
- receipt `persistence/**` runtime;
- `AndroidManifest.xml`;
- OCR/layout/item/validation behavior;
- Activities/navigation/UI;
- exact-alias auto-link behavior;
- permission/privacy model.

`LegacyCatalogAdapter` preserves existing product ID, classified type, canonical name and creation timestamp without parsing brand/spec/category or merging similar rows.

This is the migration contract for CP22.

## 5. CP21 canonical documents

Read these for the checkpoint contract:

1. `CATALOG_DOMAIN_V2_PLAN.md`
2. `CATALOG_DOMAIN_V2_CONSISTENCY_REVIEW.md`
3. `CATALOG_DOMAIN_V2_GOLDEN_VECTORS.md`
4. `CP21_CATALOG_DOMAIN_V2_EVIDENCE.md`
5. `CP21_CATALOG_DOMAIN_V2_CLOSEOUT.md`

CP20 product direction remains upstream context:

- `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
- `PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
- `PRODUCT_REBASELINE_V1_ROADMAP.md`

## 6. Completed checkpoint chain

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
21. **Catalog Domain V2 — COMPLETE**

## 7. Next planned checkpoint

**CP22 — Persistence V2**

Goal: implement migration-safe storage and indexes for the frozen CP21 domain semantics.

Before writing schema migration code CP22 must examine:

- exact current receipt/product DB schemas and relationships;
- preservation of all existing product IDs and item links;
- migration sequencing and fail-closed/rollback behavior across separate app-private DBs;
- merchant alias context representation;
- specification / category / purchase-form storage needs;
- query/index needs for later identity/search/history work;
- whether direct SQLite should be retained or Room introduced, based on concrete migration/runtime evidence rather than framework preference.

CP22 must not reinterpret CP21 identity/unit/provenance semantics implicitly.

**Do not begin CP22 without explicit user authorization.**

## 8. Existing application invariants to preserve

- external-camera capture without app CAMERA permission;
- system picker without broad storage/media permission;
- EXIF normalization / bounded bitmap decode;
- document detection / perspective correction;
- bundled local Korean OCR;
- source-coordinate preservation;
- geometry-based layout reconstruction;
- structure/item extraction with provenance;
- arithmetic validation and contradiction preservation;
- bounded OCR recovery / conservative cross-pass merge;
- user review/edit before save;
- app-private receipt/image persistence;
- merchant/store handling;
- conservative identity linking;
- invalid-receipt exclusion from normal comparable history;
- receipt-derived price truth;
- API36/lint/privacy permission firewall.

## 9. Public repository / namespace firewall

ReceiptLedger may modify only:

- `receiptledger/**`
- explicitly ReceiptLedger-prefixed `.github/workflows/receiptledger-*.yml`

Do not read/use/modify/depend/cache/artifact from other project namespaces.

Never commit/upload signing material, credentials, real private receipt photos, actual purchase databases, private backups, personal identifiers, or uncleared private assets.

The APK must continue not to request CAMERA, broad media/storage, INTERNET, or ACCESS_NETWORK_STATE permission unless separately authorized by a later product decision.

## 10. Non-blocking infrastructure notes

CP21 CI succeeded fully. The log also records platform/build-tool deprecation notices concerning Node.js action runtime and future Gradle 9 compatibility. They are not CP21 domain failures and were intentionally not expanded into unrelated scope.

## 11. Restart order

For a new session:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CATALOG_DOMAIN_V2_PLAN.md`
4. `receiptledger/CATALOG_DOMAIN_V2_CONSISTENCY_REVIEW.md`
5. `receiptledger/CATALOG_DOMAIN_V2_GOLDEN_VECTORS.md`
6. `receiptledger/PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
7. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `receiptledger/README.md`
9. `receiptledger/WORK_UNIT.md`
10. current catalog source/test/workflow only as required

Then verify the current branch against frozen implementation HEAD `8596106c370e172161ef00e8d460dc78667bf80d`. Any post-boundary handoff changes must be documentation-only unless the user explicitly authorizes CP22.

**Current stop condition: CP21 is complete. Await explicit authorization for CP22.**
