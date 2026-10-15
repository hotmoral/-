# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP24_IDENTITY_RESOLVER_V2_CLOSEOUT.md`
4. `CP24_IDENTITY_RESOLVER_V2_EVIDENCE.md`
5. `CP24_IDENTITY_RESOLVER_V2_PLAN.md`
6. `IDENTITY_RESOLVER_V2_CONSISTENCY_REVIEW.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP24 — Identity Resolver V2 — COMPLETE**

- branch `receiptledger/run-v1-identity-resolver-v2-20261016`
- frozen implementation HEAD `4b556afd4dd52b68cf768e937bb456665ad4c231`
- canonical Actions `38824134990` — SUCCESS
- artifact ID `12014915453`
- artifact digest `sha256:4740590ca2c7d7525842aa3ebe6ec7964911d303322ebad77b5701344ce76867`
- APK SHA-256 `0656c60110ba7debcb0801ddee048cd2220b959c2119539a79274eebbc05eb6e`
- identity tests 8/8 PASS
- semantics tests 7/7 PASS
- catalog tests 15/15 PASS
- persistence tests 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.22-identity-resolver-v2`, versionCode 23

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

CP24 converts confirmed alias knowledge and sufficiently strict semantic evidence into deterministic reuse of an **existing** stable catalog ID.

Key rules:

- MERCHANT exact alias precedes GLOBAL exact alias;
- dangling or strongly contradicted confirmed aliases go to REVIEW;
- strict semantic auto-link requires one unique existing STANDARD candidate with confirmed exact product name and specification, plus confirmed exact brand/variant when applicable;
- product-name similarity or parser HIGH confidence alone cannot auto-link;
- fuzzy/edit-distance/embedding-style similarity is not auto-link authority;
- ambiguity stays review-gated;
- resolver never auto-creates or merges identities;
- category is not identity authority;
- NON_STANDARD semantic grouping remains CP26;
- price truth remains receipt-derived.

## CP24 local quality

- 24 synthetic fixtures / 20 known-identity fixtures
- automatic links 14, correct 14, incorrect 0
- false merge 0
- false split / fragmentation risk 1/20 = 5%
- review-required 6
- unresolved 4
- repeat confirmed reuse 4/4 = 100%

The false-split risk is deliberately reported rather than eliminated by unsafe resolver broadening. These are local synthetic metrics, not final real-receipt accuracy.

## Next planned checkpoint

**CP25 — Category System**

It will define category taxonomy/persistence/assignment/suggestion/correction/reuse for browse and organization. Category remains metadata and must never prove or override product identity.

Do not start CP25 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
