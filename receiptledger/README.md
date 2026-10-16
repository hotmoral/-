# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP28_PRICE_EVALUATION_CLOSEOUT.md`
4. `CP28_PRICE_EVALUATION_EVIDENCE.md`
5. `CP28_PRICE_EVALUATION_PLAN.md`
6. `PRICE_EVALUATION_CONSISTENCY_REVIEW.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP28 — Price Evaluation — COMPLETE**

- branch `receiptledger/run-v1-price-evaluation-20261016`
- frozen implementation HEAD `dd4f98613677ae998932d77f3e5f89d7bddba107`
- canonical Actions `38834818192` — SUCCESS
- job `116761457914` — SUCCESS
- artifact ID `12018776680`
- artifact digest `sha256:aa90bff8107f34d1974fd9998ceb543fba33fd8b0d402cc972840f9495b9e4b6`
- APK SHA-256 `692e16f0bd6ad23caba3361d831376620bac09e1505f4780d7147402f9fd48f6`
- CP28 tests 8/8 PASS
- CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.26-price-evaluation`, versionCode 27

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable price judgment`

CP28 now judges the latest strict-comparable personal price against a baseline formed from the most recent prior purchases:

- latest excluded from its own baseline;
- minimum 3 prior observations;
- maximum recent 5 prior observations;
- usual price = median;
- material change = >=5% AND >=100 minor units;
- extreme change = >=15% AND >=500 minor units;
- contextual 봉/팩/상자/단/OTHER histories remain unjudged;
- no external market price or generative-AI opinion.

Canonical local metric:

`cases=12 evaluated=9 insufficient=1 contextual=1 nonpositive=1 typical=2 cheap=2 very_cheap=1 expensive=2 very_expensive=2 latest_excluded=1 recent_five_window=1 deterministic_repeat=1`

## Next planned checkpoint

**CP29 — Search / Browse**

Make products/commodities/history practically findable by product name, brand, confirmed aliases, category, specification, store, recent/frequent use and price change without widening identity authority.

Do not start CP29 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only `receiptledger/**` and explicitly approved `.github/workflows/receiptledger-*.yml`. Do not use other project namespaces or alter repo-wide settings without separate approval.
