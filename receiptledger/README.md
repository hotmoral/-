# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP33_CAPTURE_REVIEW_UX_V2_CLOSEOUT.md`
4. `CP33_CAPTURE_REVIEW_UX_V2_EVIDENCE.md`
5. `CP33_CAPTURE_REVIEW_UX_V2_PLAN.md`
6. `CAPTURE_REVIEW_UX_V2_CONSISTENCY_REVIEW.md`
7. `CAPTURE_REVIEW_UX_V2_GOLDEN_VECTORS.md`
8. `CP32_COMMODITY_DETAIL_CLOSEOUT.md`
9. `CP32_COMMODITY_DETAIL_EVIDENCE.md`
10. `CP31_PRODUCT_DETAIL_CLOSEOUT.md`
11. `CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
12. `PRODUCT_REBASELINE_V1_ROADMAP.md`
13. `WORK_UNIT.md`

GitHub is canonical. Verify the current handoff ref and frozen executable ref separately before relying on old chat context.

## Current boundary

**CP33 — Capture / Review UX V2 — COMPLETE**

- branch `receiptledger/run-v1-capture-review-ux-v2-20261016`
- predecessor handoff `1996668e1fec6961eb158c5dd2e6b673fdb46ee0`
- frozen implementation HEAD `34cdac2d3e61081ab2a529173dbef9a2431431e0`
- canonical Actions `38874509796` — SUCCESS
- job `116886197267` — SUCCESS
- artifact ID `12034453925`
- artifact digest `sha256:36da341582f3e4083699a31d87eb5366b62e6c99c555d1fcd41dec4b9dd3f912`
- APK SHA-256 `8f78d9dab92c65bdccd31008f9cd15221f26ef63dbfcfab2741e9a066d2237b0`
- lint `No issues found.`
- version `1.0.31-capture-review-ux-v2`, versionCode 32

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Core experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 반복 구매 재사용 -> 검색/탐색 -> 제품/품목 가격기억 확인`

## CP33 result

The capture surface now:

- automatically starts OCR/recovery after image load;
- no longer requires a manual OCR button step;
- does not force every clean receipt through a full edit dialog;
- blocks Save when material uncertainty remains;
- shows only flagged fields/items by default;
- preserves `전체 내용 수정`;
- preserves raw OCR and frozen review-engine provenance behavior;
- requires explicit confirmation for `DEFAULT_ONE` quantity;
- permits deterministic arithmetic inference when the final receipt arithmetic is trustworthy;
- performs best-effort reuse of already-confirmed GLOBAL exact aliases only after receipt persistence;
- never creates products or aliases automatically and never uses fuzzy/search/category/price identity inference;
- isolates post-save optional failures from receipt-save success;
- uses a vertically scrollable capture surface so review/save controls remain reachable on constrained heights;
- replaces old debug/pass-score copy with Korean product-facing states.

## Frozen domain / architecture

CP21–32 identity/category/commodity/price/evaluation/search/detail contracts remain frozen.

- product schema 2;
- receipt schema 1;
- programmatic `Activity + android.widget`;
- no Compose/Material migration;
- no duplicate mutable price truth;
- offline/local OCR posture;
- no broad storage/media/network permissions.

## CP33 metric

`CP33_METRICS capture_review_version=2 auto_confirm_cases=2 review_required_cases=7 user_edit_exit=1 selective_review=1 full_edit=1 raw_ocr_preserved=1 exact_alias_reuse=1 unknown_alias_safe=1 link_failure_isolated=1 auto_processing=1 schema_unchanged=1`

Packaged evidence includes CP33 13/13, legacy ReviewEngine 4/4 and CP26–32 key regressions with zero failures/errors/skips.

## Next planned checkpoint

**CP34 — Commercial UI Shell — NOT STARTED**

CP34 will connect the existing receipt-add, search/browse/category, Product Detail, Commodity Detail and receipt history/detail capabilities into a coherent normal-user app shell. It is integration/presentation work, not authorization to change identity/price/review/schema truth.

Do not start CP34 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
