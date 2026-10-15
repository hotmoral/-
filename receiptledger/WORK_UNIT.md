# ReceiptLedger public execution work unit

## Current stage

**CP20 — Product Rebaseline / V1 Master Specification is COMPLETE.**

CP20 branch:
`receiptledger/run-v1-product-rebaseline-20261016`

Frozen CP20 specification boundary:
`961d64ecfa484478b97e6fcd8e9ffec542be7b51`

Result:
**PASS / COMPLETE**

Checkpoint type:
**documentation/specification only**

No production Android source, DB schema, OCR/runtime behavior, permissions, toolchain, APK, or executable CI contract changed in CP20.

## Latest executable baseline remains Target API 36 Core

- implementation HEAD: `56abeee3bb185cea8dd136d972a9660f243ded27`
- canonical Actions run: `38800790544` — SUCCESS
- artifact digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- debug APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`
- lint: 0 errors / 0 warnings
- AGP 8.11.1
- Gradle 8.13
- JDK 17
- compileSdk 36
- targetSdk 36
- minSdk 23
- versionCode 19
- versionName `1.0.18-target-api36-core`

## CP20 essence

ReceiptLedger is now explicitly defined around:

> trustworthy personal purchase-price memory and comparison

Primary loop:

`receipt -> extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

Frozen safety direction:

- preserve provenance and contradictions;
- wrong identity merge is worse than unresolved identity;
- exact confirmed knowledge may reduce repeated review;
- semantic/fuzzy matching is suggestion evidence by default, not silent merge authority;
- merchant-context alias capability is required in V2;
- non-standard goods may group mixed sales forms without claiming cross-unit comparability;
- no guessed unit conversion;
- price history remains traceable to canonical receipts + links;
- price labels require explicit deterministic statistics and data sufficiency;
- tested OCR/validation/privacy/API36 foundations are preserved;
- commercial UI is introduced incrementally rather than by rewriting proven internals.

## CP20 canonical documents

Primary:

- `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
- `PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
- `PRODUCT_REBASELINE_V1_ROADMAP.md`

Supporting records are indexed in:

- `CP20_PRODUCT_REBASELINE_NAVIGATION.md`

## Consistency result

**COMPATIBLE WITH CONTROLLED EXTENSION**

No blocking contradiction requiring a restart/rewrite was found.

Known future gaps:

- Product/Commodity Domain V2
- brand/specification/pack semantics
- merchant-aware alias context
- category system
- non-standard sales-unit/form model
- persistence migration
- semantic product parsing
- resolver V2
- richer price statistics and price evaluation
- search/browse/detail
- intake/review UX V2
- commercial design system/UI shell
- real-receipt evaluation
- performance/reliability hardening

## Next planned work unit

**CP21 — Catalog Domain V2**

Purpose:
freeze exact domain contracts for Product, Commodity, Brand, Specification, SalesUnit, Category reference, AliasContext, PurchaseObservation, provenance/confirmation states, identity/equality rules, and legacy compatibility.

Critical gate:
**CP21 domain semantics must freeze before CP22 persistence migration implementation.**

CP21 is only planned. Do not start it until explicit user authorization.

## Group discipline

For every future checkpoint:

1. recover current canonical GitHub state;
2. state essence/non-goals;
3. check compatibility with prior contracts;
4. examine only materially relevant domain/data/UX/privacy/performance/test risks;
5. avoid unrelated cleanup and repeated audits;
6. implement the smallest coherent proof of the checkpoint;
7. run ReceiptLedger-scoped CI/evidence for executable changes;
8. record exact refs/results;
9. synchronize handoff/status documents;
10. stop before the next unauthorized checkpoint.

## Public repository rules

Modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Never include release signing secrets, credentials, real private receipt photos, personal purchase databases/backups, personal identifiers, or uncleared private assets.

Do not use other project namespaces or change repo-wide settings without separate explicit approval.

## Privacy firewall

The executable APK must continue not to request:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

## Current stop condition

**CP20 is closed. Await explicit authorization for CP21.**
