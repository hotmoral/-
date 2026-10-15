# ReceiptLedger public execution work unit

## Current stage

**CP21 — Catalog Domain V2 is COMPLETE.**

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- frozen implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical Actions run: `38808985222` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- debug APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- catalog-domain tests: 15/15 PASS
- lint: 0 errors / 0 warnings
- versionCode 20
- versionName `1.0.19-catalog-domain-v2`

Post-boundary handoff commits must remain documentation-only.

## What is now frozen

CP21 defines the V2 meanings that CP22 persistence must implement:

- `STANDARD_PRODUCT` vs `NON_STANDARD_COMMODITY`;
- no V2 catalog row for UNCLASSIFIED;
- stable catalog ID is entity identity/equality authority;
- structured semantic fields are not implicit merge authority;
- legacy IDs/names/types migrate without semantic guessing;
- category is not identity proof;
- global and merchant-scoped alias context are distinct namespaces;
- source/confidence/confirmation are independent;
- HIGH confidence != CONFIRMED;
- exact package measurement may safely canonicalize kg/g, L/mL and exact count;
- package forms BAG/PACK/BOX/BUNDLE have no guessed physical conversion;
- missing pack count remains unknown;
- commodity grouping != price comparability;
- purchase observations remain traceable to saved receipt evidence rather than becoming an independent price truth.

## Explicitly unchanged

- `ProductCatalogSchema.VERSION = 1`
- legacy `product/**` runtime
- receipt persistence runtime
- manifest/permissions
- OCR/layout/item/validation logic
- exact alias resolution behavior
- Activities/UI/navigation

## Next planned work unit

**CP22 — Persistence V2**

Purpose:
implement migration-safe storage/indexing for the frozen CP21 domain.

Required preflight before schema writes:

1. inventory current receipt/product DB schema and lifecycle;
2. map every old product/link into the V2 preservation contract;
3. design migration sequencing/fail-closed behavior across separate DBs;
4. define V2 tables/columns/indexes for structured catalog fields and alias context without duplicating receipt price truth;
5. determine direct SQLite vs Room from migration/query evidence;
6. write migration regression vectors before destructive/irreversible schema operations.

CP22 must not infer semantic fields from old canonical names as authoritative data and must not collapse separate product IDs.

## Group discipline

For every checkpoint:

1. recover canonical GitHub state;
2. state essence/non-goals;
3. inspect only materially affected consistency risks;
4. resolve cheap contract contradictions before implementation;
5. avoid unrelated cleanup/architecture churn;
6. implement the smallest coherent proof;
7. run ReceiptLedger-scoped CI/evidence;
8. freeze exact implementation/spec refs;
9. synchronize status/handoff documents;
10. stop before the next unauthorized checkpoint.

## Public repository / privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows.

Never include release signing secrets, credentials, real private receipt photos, personal purchase DBs/backups, personal identifiers, or uncleared assets.

The APK must continue not to request CAMERA, broad media/storage, INTERNET, or ACCESS_NETWORK_STATE permission unless explicitly reauthorized later.

## Current stop condition

**CP21 is closed. Await explicit authorization for CP22.**
