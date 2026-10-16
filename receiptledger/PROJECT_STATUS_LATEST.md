# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP33 — Capture / Review UX V2 — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-capture-review-ux-v2-20261016`
- predecessor CP32 handoff: `1996668e1fec6961eb158c5dd2e6b673fdb46ee0`
- frozen CP33 implementation HEAD: `34cdac2d3e61081ab2a529173dbef9a2431431e0`
- canonical Actions run: `38874509796` — SUCCESS
- job: `116886197267` — SUCCESS
- artifact ID: `12034453925`
- artifact digest: `sha256:36da341582f3e4083699a31d87eb5366b62e6c99c555d1fcd41dec4b9dd3f912`
- debug APK SHA-256: `8f78d9dab92c65bdccd31008f9cd15221f26ef63dbfcfab2741e9a066d2237b0`
- version: `1.0.31-capture-review-ux-v2` / versionCode 32
- lint: 0 errors / 0 warnings (`No issues found.`)
- CP33 13/13 + legacy ReviewEngine 4/4 + CP26–32 packaged key regressions all PASS with zero failures/errors/skips.

Any later handoff/status synchronization must remain documentation-only. The executable/evidence boundary remains `34cdac2d...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`영수증 추가 -> 신뢰 가능한 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 반복 구매 정체성 재사용 -> 검색/탐색 -> 제품/품목 상세 -> 과거 가격 판단`

Receipts are input/evidence. The product result is trustworthy personal price memory by product/commodity.

## 3. CP33 user flow

CP33 changes the old development-harness behavior into:

`촬영/사진 선택 -> 자동 분석 -> 검토 필요 여부 판정 -> 필요한 항목만 검토 -> 명시적 저장`

Frozen principles:

- image load starts OCR/recovery automatically;
- explicit Save remains mandatory;
- a clean deterministic receipt need not open the full edit dialog;
- unresolved material uncertainty blocks Save;
- full edit remains available;
- primary UI no longer surfaces raw pass diagnostics/engineering scores.

## 4. Review assessment V2

AUTO_CONFIRMED may include deterministic arithmetic inference when final receipt arithmetic is trustworthy.

REVIEW_REQUIRED includes:

- MISMATCH / INCOMPLETE;
- missing date/store/printed total;
- no items;
- blank item name / missing line amount;
- PARTIAL item;
- UNKNOWN material provenance;
- quantity `DEFAULT_ONE` until explicit confirmation;
- non-user-only warning states.

After a user review, PASS_WITH_WARNINGS can become save-ready only when remaining warnings are explicit USER_EDITED / USER_CONFIRMED provenance and no material blocker remains.

`USER_CONFIRMED_DEFAULT_ONE:<ordinal>` records that the user explicitly accepted the assumed quantity while preserving the original `ValueOrigin.DEFAULT_ONE`.

## 5. Selective review / save reliability

- default dialog shows only flagged receipt fields/items;
- untouched values pass unchanged into the frozen ReceiptReviewEngine;
- unknown/un-narrowable review reason safely falls back to full edit;
- raw OCR stays unchanged;
- clear values are not silently inferred again;
- mismatch is not auto-repaired;
- complete capture surface scrolls vertically so review/save actions remain reachable.

Only `repository.save()` failure can be presented as a receipt save failure. Optional post-save exact-link reuse cannot make an already-saved receipt look failed.

## 6. Repeat exact identity reuse

After successful receipt/image persistence, CP33 best-effort reuses only the existing confirmed GLOBAL exact alias path via `resolveAndLinkExact`.

It never:

- auto-creates products;
- confirms a new alias;
- uses fuzzy/search/category/price similarity as identity authority.

Unknown aliases safely remain unclassified.

## 7. Frozen upstream domain/UI contracts

Unchanged:

- stable catalog ID identity authority;
- CP21–29 semantics;
- CP27 comparison eligibility;
- CP28 deterministic thresholds;
- CP30 design system;
- CP31 STANDARD Product Detail;
- CP32 NON_STANDARD Commodity Detail;
- OCR/recovery algorithms;
- item tuple semantics;
- receipt arithmetic validation;
- product schema 2 / receipt schema 1;
- direct SQLite posture;
- programmatic `Activity + android.widget` architecture;
- offline/no-network/no-broad-permission posture.

## 8. Canonical metric

`CP33_METRICS capture_review_version=2 auto_confirm_cases=2 review_required_cases=7 user_edit_exit=1 selective_review=1 full_edit=1 raw_ocr_preserved=1 exact_alias_reuse=1 unknown_alias_safe=1 link_failure_isolated=1 auto_processing=1 schema_unchanged=1`

## 9. Meaningful pre-closeout history

- First CP33 run `38873199997` was rejected by the zero-warning gate because 27 old development-harness strings became unused.
- Run `38873592904` was green but intentionally not accepted as canonical: post-green review found save-state ambiguity, a no-target review dead-end and constrained-height action reachability risk.
- Final `34cdac2d...` fixed those issues and canonical run `38874509796` is clean green.

Green CI remains necessary but not sufficient when a cheap material contract gap remains.

## 10. Evidence limitation

No private real receipts, emulator screenshot comparison or physical-device usability study are included in CP33 evidence. Those are not inferred from deterministic CI.

## 11. Completed product checkpoint chain

CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> CP29 Search / Browse -> CP30 Design System Foundation -> CP31 Product Detail -> CP32 Commodity Detail -> **CP33 Capture / Review UX V2**.

Earlier foundation/OCR/persistence/archive/library/review/price-history/vertical-integration stages remain inherited and regression-guarded.

## 12. Next planned checkpoint

**CP34 — Commercial UI Shell — NOT STARTED**

Goal: integrate the already-built capabilities into a product-centric normal-user shell:

- home / primary destinations;
- receipt add entry;
- search / browse / category;
- STANDARD Product Detail;
- NON_STANDARD Commodity Detail;
- receipt history/detail;
- settings/supporting navigation as justified.

CP34 is integration/presentation work. It must not redefine identity, price, OCR, review or schema truth for navigation convenience.

Do not begin CP34 without explicit user authorization.

## 13. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP33_CAPTURE_REVIEW_UX_V2_CLOSEOUT.md`
4. `receiptledger/CP33_CAPTURE_REVIEW_UX_V2_EVIDENCE.md`
5. `receiptledger/CP33_CAPTURE_REVIEW_UX_V2_PLAN.md`
6. `receiptledger/CAPTURE_REVIEW_UX_V2_CONSISTENCY_REVIEW.md`
7. `receiptledger/CAPTURE_REVIEW_UX_V2_GOLDEN_VECTORS.md`
8. `receiptledger/CP32_COMMODITY_DETAIL_CLOSEOUT.md`
9. `receiptledger/CP32_COMMODITY_DETAIL_EVIDENCE.md`
10. `receiptledger/CP31_PRODUCT_DETAIL_CLOSEOUT.md`
11. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
12. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
13. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
14. `receiptledger/README.md`
15. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Always verify current handoff HEAD and frozen executable HEAD separately.

## 14. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately reauthorized.

**Current stop condition: CP33 complete. Await explicit authorization for CP34.**
