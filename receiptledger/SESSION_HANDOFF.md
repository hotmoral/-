# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading the current canonical files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP34_COMMERCIAL_UI_SHELL_CLOSEOUT.md`
4. `receiptledger/CP34_COMMERCIAL_UI_SHELL_EVIDENCE.md`
5. `receiptledger/CP34_COMMERCIAL_UI_SHELL_PLAN.md`
6. `receiptledger/COMMERCIAL_UI_SHELL_CONSISTENCY_REVIEW.md`
7. `receiptledger/COMMERCIAL_UI_SHELL_GOLDEN_VECTORS.md`
8. `receiptledger/CP33_CAPTURE_REVIEW_UX_V2_CLOSEOUT.md`
9. `receiptledger/CP33_CAPTURE_REVIEW_UX_V2_EVIDENCE.md`
10. `receiptledger/CP32_COMMODITY_DETAIL_CLOSEOUT.md`
11. `receiptledger/CP31_PRODUCT_DETAIL_CLOSEOUT.md`
12. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
13. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
14. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
15. `receiptledger/README.md`
16. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP34 — Commercial UI Shell — PASS / COMPLETE**

- branch: `receiptledger/run-v1-commercial-ui-shell-20261016`
- predecessor CP33 handoff: `2a15e14e9897aa9785762faef1568254fbeb5f82`
- frozen implementation HEAD: `d9764b1447aefaaf3e3fdc5785c72c7c98e8314e`
- canonical Actions: `38878681881` — SUCCESS
- job: `116899840083` — SUCCESS
- artifact ID: `12036721843`
- artifact digest: `sha256:61e31f76bcf1e8d4e7dc596807b2aacd6c7774ad8e9fe05f36b09b59d4a95258`
- APK SHA-256: `64899bfdd715780ecb864f033896f66e2c89d7186da338f2dd59c7fc2033a2af`
- versionName `1.0.32-commercial-ui-shell`, versionCode 33
- lint: `No issues found.`
- CP34 7/7, CP33 13/13, CP32 11/11, CP31 9/9, CP29 8/8 packaged key regressions PASS.

Any later status/closeout synchronization must remain documentation-only. Do not move the executable boundary from `d9764b...`.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Current target loop:

`홈 -> 영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 검색/카테고리 -> 제품/품목 상세 -> 내 과거 가격 판단 -> 영수증 근거`

Receipt storage is supporting evidence, not the final product purpose.

## 3. CP34 commercial shell

The app now launches into `HomeActivity`.

Home connects:

- CP33 receipt add;
- CP29 search/browse/category;
- recent and frequent purchase views;
- CP31 STANDARD Product Detail;
- CP32 NON_STANDARD Commodity Detail;
- receipt history/detail.

The old capture screen remains intact as an internal destination rather than being treated as the whole app.

## 4. Discovery authority

`SearchBrowseActivity` is a presentation/integration layer over frozen CP29.

It may call:

- `search()` with `SearchBrowseQueryV1.text()`;
- `recent()`;
- `frequent()`;
- `byCategory()` with frozen taxonomy nodes.

It cannot create/merge/relink products, confirm aliases or treat relevance/category/price similarity as identity evidence.

Stable product type routing only:

- STANDARD -> ProductDetailActivity;
- NON_STANDARD -> CommodityDetailActivity;
- UNCLASSIFIED/unsupported -> no classification promotion.

## 5. Receipt evidence

Library is the receipt-history destination and no longer promotes legacy PriceHistoryActivity as the main product browse path.

- whole page scrolls;
- CP30 max-width/touch grammar retained;
- list read failure is explicit;
- receipt rows route by receipt ID to ReceiptDetailActivity;
- CP31/32 purchase rows already route by receipt ID, preserving provenance end to end.

## 6. Frozen upstream authority

Unchanged for CP34:

- catalog/product/semantics/identity/category;
- commodity and commodity-detail comparability semantics;
- persistence/price/priceintel/priceeval/search/detail;
- CP30 design contracts;
- CP33 capture/review engine and save semantics;
- OCR/recovery/item/validation;
- ProductDetailActivity / CommodityDetailActivity / MainActivity / ReceiptDetailActivity / PriceHistoryActivity source;
- product schema 2 / receipt schema 1.

Architecture remains `Activity + android.widget`; no Compose/Material migration.

## 7. Security/public boundary

Repository is public. ReceiptLedger may modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Never commit secrets, signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

Forbidden CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE permissions remain absent from the packaged APK.

## 8. Pre-closeout discipline

Meaningful sequence:

- `38877757713`: failed only because five new references used nonexistent `SPACE_5_DP`; scope/frozen guards passed;
- `38877971396`: green but rejected after post-green review;
- review found Library constrained-height/large-text accessibility risk and missing list-read failure state;
- final `d9764b...` / `38878681881` is the canonical CP34 execution boundary.

## 9. Evidence limitation

CP34 does not include private real-receipt accuracy evaluation, emulator screenshot comparison, physical-device usability study, large-scale performance benchmarking or release signing evidence.

## 10. Next planned checkpoint

**CP35 — Real Receipt Evaluation — NOT STARTED**

Expected boundary:

- use public-safe synthetic or explicitly approved sanitized fixtures;
- measure end-to-end correct purchase registration, not OCR character accuracy alone;
- verify structured receipt, identity assignment/review outcome, stored price observation and detail/history traceability together;
- document real failure modes and review burden without weakening frozen CP20–34 truth contracts;
- do not combine CP36 performance/index/cache work into CP35.

## 11. Stop condition

**CP34 is complete and handoff-ready. Await explicit authorization for CP35.**
