# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

Do not reconstruct ReceiptLedger state from old chat memory. GitHub is the source of truth.

Read in this order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CATALOG_DOMAIN_V2_PLAN.md`
4. `receiptledger/CATALOG_DOMAIN_V2_CONSISTENCY_REVIEW.md`
5. `receiptledger/CATALOG_DOMAIN_V2_GOLDEN_VECTORS.md`
6. `receiptledger/PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
7. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `receiptledger/README.md`
9. `receiptledger/WORK_UNIT.md`
10. current catalog source/test/workflow only when required

Then verify the current branch against the frozen CP21 implementation HEAD below. Any later handoff/status commits must be documentation-only until the user authorizes CP22.

## 1. Latest completed checkpoint

**CP21 — Catalog Domain V2**

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- predecessor CP20 handoff HEAD: `3149beb339a2d541a61a694fb1f052556a95c8c1`
- frozen CP21 implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical Actions run: `38808985222` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- debug APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- lint: 0 errors / 0 warnings
- CatalogDomainV2Test: 15 tests, 0 failures, 0 errors, 0 skipped
- result: **PASS / COMPLETE**

## 2. Current executable/build contract

- application ID: `com.receiptledger.v1`
- versionName: `1.0.19-catalog-domain-v2`
- versionCode: 20
- AGP 8.11.1
- Gradle 8.13
- JDK / Java 17
- compileSdk 36
- targetSdk 36
- minSdk 23
- Korean ML Kit remains bundled/local
- legacy product schema remains version 1

CP21 did not change persistence schema, normal UI/navigation, OCR behavior, exact-alias runtime authority, manifest, or permission model.

## 3. CP21 domain contract

New V2 catalog domain is additive and storage-independent.

### Catalog kinds

- `STANDARD_PRODUCT`: exact repeatable packaged/manufactured commercial identity.
- `NON_STANDARD_COMMODITY`: semantic commodity/item that may contain multiple raw purchase forms.
- legacy `UNCLASSIFIED`: unresolved state; it is not a V2 catalog entity.

### Identity authority

Catalog entity equality is stable ID only.

Two rows with different IDs remain distinct even if brand/name/specification fields match. Structured similarity is candidate evidence for later resolver work, not merge authority.

Category and merchant/store are not SKU identity.

### Legacy migration rule

`LegacyCatalogAdapter` preserves existing:

- product ID;
- classified STANDARD/NON_STANDARD meaning;
- canonical name;
- creation time.

It does not parse brand/specification/category, invent units, or merge similar rows.

### Evidence state

Catalog fields keep independent:

- source;
- confidence;
- confirmation.

`HIGH confidence != CONFIRMED`.

### Units / package specification

Exact physical package equivalence is allowed for:

- kg <-> g
- L <-> mL
- exact count

Package-form units such as BAG/PACK/BOX/BUNDLE do not have guessed physical conversion.

Missing pack count remains unknown; it is not silently converted to `1`.

### NON_STANDARD

One commodity ID can group forms such as:

- 1봉
- 1kg
- 5개
- 1상자

Grouping does not imply those prices are directly comparable.

### Purchase observation

`PurchaseObservationV2` is a logical receipt-linked projection with raw item evidence, store/date, value origins, link source and receipt validation. CP21 does not create a second persisted price truth table.

## 4. Existing foundations that remain authoritative

Preserve:

- external-camera/system-picker privacy model;
- EXIF/document correction;
- local Korean OCR;
- source-coordinate preservation;
- geometry-based layout reconstruction;
- item extraction and numeric provenance;
- arithmetic validation / contradiction preservation;
- bounded OCR recovery / conservative merge;
- review/edit before save;
- app-private receipt/image storage;
- receipt list/detail/delete;
- merchant/store evidence;
- exact confirmed alias reuse only;
- receipt-derived price history;
- MISMATCH/INCOMPLETE exclusion from normal comparable history;
- API36/lint/permission firewall.

## 5. CP22 gate

Next planned checkpoint: **CP22 — Persistence V2**.

Before schema implementation, CP22 must inspect current receipt/product schemas and freeze a migration plan that preserves:

1. every existing catalog product ID;
2. item links and receipt traceability;
3. canonical names/types without semantic guessing;
4. separate receipt/product DB consistency;
5. merchant alias namespace semantics;
6. unknown values as unknown;
7. category non-authority;
8. grouping != comparability;
9. source/confidence/confirmation distinctions.

CP22 must decide direct SQLite vs Room from actual migration/query requirements, not from aesthetic preference.

CP22 must not begin automatically. Wait for explicit user authorization.

## 6. Scope/security boundary

ReceiptLedger may modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Do not use other project namespaces.

Never commit/upload secrets, signing material, real private receipt photos, real purchase DBs/backups, personal identifiers, or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE.

## 7. Infrastructure notes

CP21 CI succeeded. Node-action runtime and future Gradle-9 deprecation notices were observed and recorded as non-blocking infrastructure notes; do not expand them into CP22 unless they materially affect that checkpoint.

## 8. Stop condition

**CP21 is complete. Await explicit authorization for CP22.**
