# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP35_REAL_RECEIPT_EVALUATION_CLOSEOUT.md`
4. `CP35_REAL_RECEIPT_EVALUATION_EVIDENCE.md`
5. `CP35_REAL_RECEIPT_EVALUATION_PLAN.md`
6. `REAL_RECEIPT_EVALUATION_CONSISTENCY_REVIEW.md`
7. `REAL_RECEIPT_EVALUATION_FIXTURES_V1.md`
8. `CP34_COMMERCIAL_UI_SHELL_CLOSEOUT.md`
9. `CP34_COMMERCIAL_UI_SHELL_EVIDENCE.md`
10. `CP33_CAPTURE_REVIEW_UX_V2_CLOSEOUT.md`
11. `CP32_COMMODITY_DETAIL_CLOSEOUT.md`
12. `CP31_PRODUCT_DETAIL_CLOSEOUT.md`
13. `CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
14. `PRODUCT_REBASELINE_V1_ROADMAP.md`
15. `WORK_UNIT.md`

GitHub is canonical. Verify the current handoff branch HEAD and frozen executable ref separately before relying on old chat context.

## Current boundary

**CP35 — Real Receipt Evaluation — COMPLETE**

- branch `receiptledger/run-v1-real-receipt-evaluation-20261016`
- predecessor handoff `386c1b3d9ef7f3737ffd8b4d0f34fe2e076cab8e`
- frozen executable/evaluation HEAD `6ae9fbcfe0abc17dd9471de243170a9a87272767`
- canonical Actions `38884870134` — SUCCESS
- job `116920055654` — SUCCESS
- artifact ID `12038973171`
- artifact digest `sha256:3336486a5807fa971e8385cdd10008f29cb85daf1779ab5fd226008d9ad72258`
- APK SHA-256 `3e89e7ab1358278889c55410fc49f4b5e4e50f54c8a490aeb473dd58c0cab9cf`
- lint `No issues found.`
- version `1.0.33-real-receipt-evaluation`, versionCode 34

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Current experience:

`홈 -> 영수증 추가 -> 자동 처리/필요 검토 -> 저장 -> 반복 구매 재사용 -> 검색/카테고리 -> 제품/품목 가격기억 -> 영수증 근거`

## CP35 result

A public-safe synthetic evaluation corpus exercised the frozen purchase-registration chain from synthetic `OcrDocument` tokens through production recognition/structure, review, identity, price intelligence and detail provenance.

Key result:

`CP35_METRICS evaluation_version=1 fixtures=8 receipts=9 items=11 structured_correct=9 auto_confirmed=8 review_required=1 final_safe_registrations=7 exact_alias_reuse=2 conservative_unresolved=1 false_auto_links=0 strict_weight_observations=2 contextual_cohorts=2 discount_exclusions=1 invalid_exclusions=1 detail_trace_rows=7 schema_unchanged=1`

Observed safety properties:

- zero false automatic links;
- exact confirmed alias reuse works;
- similar product names stay unresolved rather than silently merging;
- kg/g strict normalization works without mixing contextual package forms;
- 봉/상자 contextual cohorts remain separate and unjudged;
- unsupported receipt-level discount allocation is excluded;
- mismatch receipts remain review-required and price-ineligible;
- CP31/32 history rows retain source receipt IDs.

No production Java, manifest or production-resource change was needed.

## Evidence limitation

CP35's public evidence uses synthetic token/geometry fixtures. It does **not** measure ML Kit image-to-text accuracy, camera variability or statistical merchant/font coverage. Those claims must not be inferred from this checkpoint.

## Frozen domain / architecture

CP21–34 identity/category/commodity/price/evaluation/search/detail/review/UI contracts remain frozen.

- stable product ID remains identity authority;
- product schema 2;
- receipt schema 1;
- programmatic `Activity + android.widget`;
- no Compose/Material migration;
- no duplicate mutable price truth;
- offline/local OCR posture;
- no broad storage/media/network permissions.

## Next planned checkpoint

**CP36 — Performance / Reliability — NOT STARTED**

CP36 is measurement-driven hardening: startup/OCR latency and memory, large catalog/history/search/price/detail workloads, migration/archive/recovery reliability, and representative CP29 1k/10k search measurement before any FTS/index/cache decision.

Do not start CP36 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
