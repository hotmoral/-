# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, validation, product/domain specifications, CI, and debug APK build material.

## Start here for a new GPT session

Read in this order:

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CATALOG_DOMAIN_V2_PLAN.md`
4. `CATALOG_DOMAIN_V2_CONSISTENCY_REVIEW.md`
5. `CATALOG_DOMAIN_V2_GOLDEN_VECTORS.md`
6. `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `README.md`
9. `WORK_UNIT.md`

Do not reconstruct state from old chat before reading canonical files and verifying refs.

## Current completed boundary

Latest completed checkpoint:
**CP21 — Catalog Domain V2**

Branch:
`receiptledger/run-v1-catalog-domain-v2-20261016`

Frozen implementation HEAD:
`8596106c370e172161ef00e8d460dc78667bf80d`

Canonical Actions:
`38808985222` — **SUCCESS**

Evidence:

- artifact ID `12008555521`
- artifact digest `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- APK SHA-256 `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- catalog-domain tests 15/15 PASS
- lint 0 errors / 0 warnings
- version `1.0.19-catalog-domain-v2` / versionCode 20

Post-boundary commits on this branch may synchronize handoff/status documentation only. Compare the current branch against frozen implementation HEAD before assuming additional implementation exists.

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

## CP21 domain result

CP21 added an additive, storage-independent Catalog Domain V2 while preserving the V1 runtime and product DB schema.

Key rules:

- stable catalog ID is entity equality authority;
- different IDs never merge merely because semantic fields match;
- STANDARD and NON_STANDARD legacy meanings are preserved;
- UNCLASSIFIED remains unresolved, not a catalog entity;
- category is not product-identity proof;
- alias context can be global or merchant-scoped;
- confidence and confirmation are independent;
- exact physical package equivalence is limited to safe count/weight/volume conversions;
- package forms such as 봉/팩/박스 remain raw purchase forms without guessed conversion;
- NON_STANDARD grouping does not imply cross-form comparability;
- legacy migration must preserve IDs without parsing/merging canonical names;
- purchase price truth remains receipt-derived.

Legacy `ProductCatalogSchema.VERSION` remains **1**. Persistence migration has not started.

## Roadmap

See `PRODUCT_REBASELINE_V1_ROADMAP.md`.

Next planned checkpoint:
**CP22 — Persistence V2**

CP22 must implement migration-safe storage for CP21 semantics. It is planned but not automatically authorized.

## Current privacy/security model

This repository is public. Never place here signing secrets, credentials, real private receipt photos, real purchase-history databases/backups, personal identifiers, or uncleared private/proprietary assets.

The executable app intentionally does not request:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

Camera intake uses an external camera app plus a constrained temporary URI. Gallery intake uses the system picker. Korean ML Kit OCR remains bundled/local.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not read from, modify, depend on, cache from, or consume artifacts/output from other project namespaces. Do not alter repo-wide settings without separate explicit approval.

## Current stop condition

**CP21 is complete. Do not begin CP22 until explicitly authorized.**
