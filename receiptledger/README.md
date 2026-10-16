# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP34_COMMERCIAL_UI_SHELL_CLOSEOUT.md`
4. `CP34_COMMERCIAL_UI_SHELL_EVIDENCE.md`
5. `CP34_COMMERCIAL_UI_SHELL_PLAN.md`
6. `COMMERCIAL_UI_SHELL_CONSISTENCY_REVIEW.md`
7. `COMMERCIAL_UI_SHELL_GOLDEN_VECTORS.md`
8. `CP33_CAPTURE_REVIEW_UX_V2_CLOSEOUT.md`
9. `CP33_CAPTURE_REVIEW_UX_V2_EVIDENCE.md`
10. `CP32_COMMODITY_DETAIL_CLOSEOUT.md`
11. `CP31_PRODUCT_DETAIL_CLOSEOUT.md`
12. `CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
13. `PRODUCT_REBASELINE_V1_ROADMAP.md`
14. `WORK_UNIT.md`

GitHub is canonical. Verify the current handoff branch HEAD and frozen executable ref separately before relying on old chat context.

## Current boundary

**CP34 — Commercial UI Shell — COMPLETE**

- branch `receiptledger/run-v1-commercial-ui-shell-20261016`
- predecessor handoff `2a15e14e9897aa9785762faef1568254fbeb5f82`
- frozen implementation HEAD `d9764b1447aefaaf3e3fdc5785c72c7c98e8314e`
- canonical Actions `38878681881` — SUCCESS
- job `116899840083` — SUCCESS
- artifact ID `12036721843`
- artifact digest `sha256:61e31f76bcf1e8d4e7dc596807b2aacd6c7774ad8e9fe05f36b09b59d4a95258`
- APK SHA-256 `64899bfdd715780ecb864f033896f66e2c89d7186da338f2dd59c7fc2033a2af`
- lint `No issues found.`
- version `1.0.32-commercial-ui-shell`, versionCode 33

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Current experience:

`홈 -> 영수증 추가 -> 자동 처리/필요 검토 -> 저장 -> 검색/카테고리 -> 제품/품목 가격기억 -> 영수증 근거`

## CP34 result

The packaged app now launches into a real product-centric Home instead of the capture harness.

Home connects:

- receipt add -> frozen CP33 capture/review flow;
- text search and category browse -> frozen CP29 discovery;
- recent/frequent purchase views;
- STANDARD results -> frozen CP31 Product Detail;
- NON_STANDARD results -> frozen CP32 Commodity Detail;
- receipt history -> Library -> Receipt Detail;
- recent linked price-memory preview.

Library no longer exposes legacy PriceHistoryActivity as the primary product browse path. Home, Search and Library are vertically scrollable and use CP30 design tokens/components.

## Frozen domain / architecture

CP21–33 identity/category/commodity/price/evaluation/search/detail/review contracts remain frozen.

- stable product ID remains identity authority;
- search/category/UI cannot relink identity;
- product schema 2;
- receipt schema 1;
- programmatic `Activity + android.widget`;
- no Compose/Material migration;
- no duplicate mutable price truth;
- offline/local OCR posture;
- no broad storage/media/network permissions.

## CP34 metric

`CP34_METRICS shell_version=1 launcher_home=1 add_receipt=1 search_browse=1 category_browse=1 standard_detail=1 commodity_detail=1 receipt_history=1 legacy_price_entry_removed=1 schema_unchanged=1`

Packaged evidence includes CP34 7/7, CP33 13/13, CP32 11/11, CP31 9/9 and CP29 8/8 key regressions with zero failures/errors/skips.

## Next planned checkpoint

**CP35 — Real Receipt Evaluation — NOT STARTED**

CP35 evaluates end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures. Correct purchase registration is the primary metric, not OCR character accuracy alone.

Do not start CP35 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
