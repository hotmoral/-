# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP34 — Commercial UI Shell — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-commercial-ui-shell-20261016`
- predecessor CP33 handoff: `2a15e14e9897aa9785762faef1568254fbeb5f82`
- frozen CP34 implementation HEAD: `d9764b1447aefaaf3e3fdc5785c72c7c98e8314e`
- canonical Actions run: `38878681881` — SUCCESS
- job: `116899840083` — SUCCESS
- artifact ID: `12036721843`
- artifact digest: `sha256:61e31f76bcf1e8d4e7dc596807b2aacd6c7774ad8e9fe05f36b09b59d4a95258`
- debug APK SHA-256: `64899bfdd715780ecb864f033896f66e2c89d7186da338f2dd59c7fc2033a2af`
- version: `1.0.32-commercial-ui-shell` / versionCode 33
- lint: 0 errors / 0 warnings (`No issues found.`)
- CP34 7/7, CP33 13/13, CP32 11/11, CP31 9/9 and CP29 8/8 packaged key suites PASS with zero failures/errors/skips.

Any later handoff/status synchronization must remain documentation-only. The executable/evidence boundary remains `d9764b...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Current user loop:

`홈 -> 영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 반복 구매 정체성 재사용 -> 검색/카테고리 -> 제품/품목 가격기억 -> 영수증 근거`

Receipt storage is supporting evidence; the product result is trustworthy personal price memory by product/commodity.

## 3. CP34 shell result

The packaged launcher is now `HomeActivity`, not the capture harness.

Home exposes:

- `영수증 추가` -> frozen CP33 MainActivity;
- search/category discovery -> SearchBrowseActivity;
- recent/frequent purchase shortcuts;
- recent linked price-memory preview;
- receipt history -> LibraryActivity.

Home is vertically scrollable, uses CP30 components and has explicit recent loading/empty/failure states.

## 4. Discovery result

`SearchBrowseActivity` consumes the frozen CP29 read-only service only.

- text search -> `SearchBrowseQueryV1.text()` / `search()`;
- recent -> `recent()`;
- frequent -> `frequent()`;
- category -> frozen taxonomy + `byCategory()`;
- STANDARD stable ID -> CP31 ProductDetailActivity;
- NON_STANDARD stable ID -> CP32 CommodityDetailActivity;
- unsupported/unclassified -> no identity promotion.

Search relevance remains discovery-only and cannot create, merge, relink or confirm identity.

## 5. Receipt traceability

Library is the normal receipt-history destination.

- legacy PriceHistoryActivity is no longer the primary browse path from Library;
- Library provides receipt-add and find actions;
- whole Library page scrolls on constrained height/enlarged text;
- receipt-list loading failure is explicit;
- receipt rows -> ReceiptDetailActivity by exact receipt ID.

Product/Commodity detail purchase rows continue to route to the exact source receipt.

## 6. Frozen contracts

Unchanged:

- stable catalog ID identity authority;
- CP21–29 semantics;
- CP27 comparison eligibility;
- CP28 thresholds;
- CP30 design system;
- CP31 STANDARD detail;
- CP32 NON_STANDARD detail and strict/contextual separation;
- CP33 capture/review/save/provenance;
- OCR/recovery/item/validation;
- product schema 2 / receipt schema 1;
- direct SQLite posture;
- programmatic `Activity + android.widget` architecture;
- offline/no-network/no-broad-permission posture.

No Compose/Material migration, FTS/index/cache or unrelated product expansion was introduced.

## 7. Canonical metric

`CP34_METRICS shell_version=1 launcher_home=1 add_receipt=1 search_browse=1 category_browse=1 standard_detail=1 commodity_detail=1 receipt_history=1 legacy_price_entry_removed=1 schema_unchanged=1`

## 8. Meaningful pre-closeout history

- Run `38877757713` failed compilation only because five new layout references used nonexistent `SPACE_5_DP`; frozen-contract guards passed. The intended 24dp spacing was corrected to CP30 `SPACE_6_DP`.
- Run `38877971396` was green but rejected after post-green review found Library constrained-height/large-text accessibility risk and a missing list-read failure state.
- Final `d9764b...` corrected those issues; canonical run `38878681881` is clean green.

Green CI is necessary but not sufficient when a material contract gap remains cheaply fixable.

## 9. Completed product checkpoint chain

CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> CP29 Search / Browse -> CP30 Design System Foundation -> CP31 Product Detail -> CP32 Commodity Detail -> CP33 Capture / Review UX V2 -> **CP34 Commercial UI Shell**.

Earlier foundation/OCR/archive/library/review/price-history/vertical-integration work remains inherited and regression-guarded.

## 10. Evidence limitation

CP34 does not include private real-receipt accuracy evaluation, device screenshot comparison, physical-device usability evidence, large-scale performance benchmarking or release signing evidence.

## 11. Next planned checkpoint

**CP35 — Real Receipt Evaluation — NOT STARTED**

Goal:

- validate end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures;
- evaluate receipt -> structured purchase -> identity -> price record -> detail/history traceability as a whole;
- treat correct purchase registration as the primary metric rather than OCR character accuracy alone;
- document failure taxonomy and review burden without weakening the frozen identity/price/review contracts.

CP36 Performance / Reliability remains after CP35.

Do not begin CP35 without explicit user authorization.

## 12. Canonical restart order

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

GitHub is canonical. Always verify the live handoff branch HEAD and frozen executable HEAD separately.

## 13. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately reauthorized.

**Current stop condition: CP34 complete. Await explicit authorization for CP35.**
