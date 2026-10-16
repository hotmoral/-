# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP27_PRICE_INTELLIGENCE_V2_CLOSEOUT.md`
4. `CP27_PRICE_INTELLIGENCE_V2_EVIDENCE.md`
5. `CP27_PRICE_INTELLIGENCE_V2_PLAN.md`
6. `PRICE_INTELLIGENCE_V2_CONSISTENCY_REVIEW.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP27 — Price Intelligence V2 — COMPLETE**

- branch `receiptledger/run-v1-price-intelligence-v2-20261016`
- frozen implementation HEAD `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`
- canonical Actions `38831623548` — SUCCESS
- job `116751473084` — SUCCESS
- artifact ID `12017014494`
- artifact digest `sha256:660ead5ea86bae86fbd6cf67643866c17acfa5f144c9b1d06f29d50f71f44dd5`
- APK SHA-256 `8455e4ce23e15c6a113e87ddbd0ddb000e41d9f1849e7f431c9ed5dfbfabe1bc`
- CP27 tests 8/8 PASS
- legacy price-history tests 2/2 PASS
- CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.25-price-intelligence-v2`, versionCode 26

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

CP27 now defines historical price using receipt-traceable comparison ratios and safe comparison cohorts.

Key rules:

- STANDARD compares one exact stable package;
- kg/g normalize exactly to price/kg;
- L/mL normalize exactly to price/L;
- count normalizes to price/each;
- 봉/팩/상자/단/OTHER remain contextual same-form cohorts only;
- multi-item unallocated receipt discounts are excluded from aggregates;
- sole-item discount attribution is permitted only because the target item is unique;
- invalid receipts and arithmetic conflicts remain visible but excluded;
- statistics include latest/previous/delta/min/max/mean/median plus period/store filtering;
- no cheap/normal/expensive judgment yet;
- product schema 2 and receipt schema 1 remain unchanged;
- legacy price-history core remains intact.

## CP27 local contract metric

`observations=10 eligible=7 excluded_discount=1 excluded_invalid=1 missing_form=1 standard_cohorts=1 commodity_strict_cohorts=1 commodity_contextual_cohorts=1 scope_checks=2 receipt_traceable_rates=7`

Synthetic/local evidence only; not real-receipt accuracy.

## Next planned checkpoint

**CP28 — Price Evaluation**

It will turn only CP27-eligible cohort facts into deterministic, explainable price judgments using explicit data-sufficiency, baseline/window and threshold rules. It must not use free-form AI judgment or combine incomparable cohorts.

Do not start CP28 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
