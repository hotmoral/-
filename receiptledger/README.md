# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP29_SEARCH_BROWSE_CLOSEOUT.md`
4. `CP29_SEARCH_BROWSE_EVIDENCE.md`
5. `CP29_SEARCH_BROWSE_PLAN.md`
6. `SEARCH_BROWSE_CONSISTENCY_REVIEW.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP29 — Search / Browse — COMPLETE**

- branch `receiptledger/run-v1-search-browse-20261016`
- frozen implementation HEAD `b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`
- canonical Actions `38839041465` — SUCCESS
- job `116774625167` — SUCCESS
- artifact ID `12020980247`
- artifact digest `sha256:16505e577d84180771fe8e6da8f8d4243cf389aa0892f2446e621933fad4de81`
- APK SHA-256 `e8f0503cd12126461f6eb257a11be2d0ef7bac68cc2857c6b4f523c059830088`
- CP29 tests 8/8 PASS
- CP28 8/8, CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.27-search-browse`, versionCode 28

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable judgment -> find/browse`

CP29 now makes the frozen product/commodity/history facts discoverable through a read-only search/browse layer.

Key rules:

- canonical/brand/product/variant/specification can be searched;
- already-linked receipt item names can be used as discovery text;
- observed search text never becomes identity authority;
- category browse includes descendants;
- store filter uses exact normalized text;
- recent and frequent views are deterministic;
- frequency counts distinct receipt occasions;
- price-change browse includes only strict CP28 evaluated non-typical cohorts;
- contextual 봉/팩/상자 histories never become cheap/expensive alerts;
- one commodity may expose separate kg/each/etc. price-change rows;
- no mutable search table/index/FTS was added;
- product schema 2 and receipt schema 1 remain unchanged.

## CP29 local contract metric

`CP29_METRICS documents=3 exact_hits=1 compact_hits=1 observed_hits=1 category_rows=3 store_rows=1 recent_rows=3 frequent_rows=3 no_result_rows=0 mutation_checks=1 diagnostics_scanned=3`

Synthetic/local evidence only; not real-user search-quality or large-scale performance evidence.

## Next planned checkpoint

**CP30 — Design System Foundation**

It will define typography, color/semantic states, spacing/grid, shapes, icons, component grammar, charts and accessibility before final Product/Commodity Detail and commercial shell work.

Do not start CP30 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
