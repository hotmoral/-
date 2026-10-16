# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP25_CATEGORY_SYSTEM_CLOSEOUT.md`
4. `CP25_CATEGORY_SYSTEM_EVIDENCE.md`
5. `CP25_CATEGORY_SYSTEM_PLAN.md`
6. `CATEGORY_SYSTEM_CONSISTENCY_REVIEW.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP25 — Category System — COMPLETE**

- branch `receiptledger/run-v1-category-system-20261016`
- frozen implementation HEAD `042c3b59063f0e58a273a5f685b25780683fcf36`
- canonical Actions `38827880730` — SUCCESS
- job `116739504019` — SUCCESS
- artifact ID `12015144887`
- artifact digest `sha256:06e0dcd1d74e3abafd4f39a97363d51b9d53cfb2253c0cf4e742e39f5b257a92`
- APK SHA-256 `69244c65cfb09476f371b9c748d42cbe58a5974c3f49d662be90e603e3622a1f`
- category tests 8/8 PASS
- identity tests 8/8 PASS
- semantics tests 7/7 PASS
- catalog tests 15/15 PASS
- persistence tests 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.23-category-system`, versionCode 24

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

CP25 makes resolved products/commodities easier to browse through category metadata without changing identity.

Key current category rules:

- bounded 28-node FOOD/HOUSEHOLD taxonomy;
- persisted category reuses before rules;
- unique high-confidence rule -> AUTO_ASSIGNABLE;
- generic/conflicting evidence -> REVIEW;
- unsupported evidence -> UNRESOLVED;
- no forced OTHER;
- correction changes only category on the same stable catalog ID;
- category never proves identity or merges price histories;
- existing product schema 2 `category_refs` is reused; no schema v3;
- grouping != comparability remains frozen;
- price truth stays receipt-derived.

## CP25 local quality

`fixtures=30 known_category=28 auto_suggestions=24 correct_auto_suggestions=24 incorrect_auto_suggestions=0 review_required=6 unresolved=2 repeat_cases=4 repeat_reused=4 correction_cases=3 correction_reused=3`

These are synthetic/local metrics, not final real-receipt accuracy.

## Next planned checkpoint

**CP26 — Commodity / Non-standard V2**

It will formalize common commodity grouping across heterogeneous purchase forms while preserving raw unit/form and prohibiting guessed conversion or fake comparability.

Do not start CP26 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
