# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
4. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_EVIDENCE.md`
5. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_PLAN.md`
6. `receiptledger/DESIGN_SYSTEM_FOUNDATION_CONSISTENCY_REVIEW.md`
7. `receiptledger/DESIGN_SYSTEM_FOUNDATION_GOLDEN_VECTORS.md`
8. `receiptledger/CP29_SEARCH_BROWSE_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP30 — Design System Foundation — PASS / COMPLETE**

- branch: `receiptledger/run-v1-design-system-foundation-20261016`
- predecessor handoff: `3727db04d2207fe92c0552d4691dbf421d71444c`
- frozen implementation HEAD: `ff0745db529499171246866039521a0b83e830e4`
- canonical Actions: `38842905325` — SUCCESS
- job: `116786812761` — SUCCESS
- artifact ID: `12022330459`
- artifact digest: `sha256:f1bcb1b2d58e328b15cf4811dd1dc107888cc2f5ba733ce1bb1ee60bf8ec0e5e`
- APK SHA-256: `cb35afb3ee0bf00dafad48f0b33733401661a982df11557bb01f716ca6655373`
- CP30 9/9 PASS
- CP29 8/8, CP28 8/8, CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint 0 errors / 0 warnings
- versionName `1.0.28-design-system-foundation`, versionCode 29

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 검색/탐색 -> 제품/품목 상세 -> 과거 가격과 현재 가격 판단`

CP30 supplies the visual/interaction grammar for later user-facing surfaces; it does not create new business truth.

## 3. Frozen architecture choice

Current Android architecture remains programmatic platform Views:

`Activity + android.widget`

Frozen CP30 decisions:

- no Compose migration;
- no AppCompat/Material dependency migration;
- no custom/downloadable font;
- no new navigation framework;
- CP31–34 should consume `design/**` rather than add new hardcoded visual values.

## 4. Typography / layout foundation

Typography roles:

- PRICE_HERO 30/36 bold
- TITLE_LARGE 22/28 bold
- TITLE_MEDIUM 18/24 medium
- BODY_LARGE 16/24 normal
- BODY_MEDIUM 14/20 normal
- LABEL 12/16 medium

Layout/surface:

- spacing 4/8/12/16/24/32dp
- radius 8/12/16dp
- elevation card 1dp / floating 3dp
- touch target >=48dp
- list row >=56dp
- content max-width token 720dp

## 5. Semantic state foundation

Tones:

`NEUTRAL / PRIMARY / POSITIVE / NEGATIVE / REVIEW / ERROR / INFO / DISABLED`

Rules:

- color never carries state meaning alone;
- CP28 judgments always have explicit Korean text;
- no-judgment states never use cheap/expensive tone;
- validation/review/loading/empty/error/unavailable states have explicit Korean title/body copy;
- semantic foreground/background pairs are tested to CP30's >=4.5:1 small-text contrast requirement.

## 6. Icons / accessibility

Frozen semantic icon roles:

`ADD_RECEIPT / SEARCH / FILTER / RECEIPT / PRODUCT / CATEGORY / PRICE_TREND / REVIEW / MORE / DELETE`

- glyph token 24dp;
- minimum interactive hit area 48dp;
- icon-only controls require Korean content descriptions;
- final icon artwork/library is not frozen yet.

## 7. Responsive / chart rules

Width classes:

- compact `<600dp`
- medium `600..839dp`
- expanded `>=840dp`

Two-pane only when expanded width and height >=480dp.

Chart series key is effectively stable catalog ID + CP27 comparison basis. Different bases may not be connected into one line. LIKE_FORM remains contextual/reference-only.

## 8. Representative adoption

Only:

- `LibraryActivity`
- legacy `PriceHistoryActivity`

use `UiKitV1` as the CP30 proof.

Do not infer that Main/Review/Detail are already commercially redesigned.

## 9. Pre-closeout correction history

Initial implementation `5c63a537...` / Actions `38842440663` passed. Before closure, plan/code comparison caught missing icon-role centralization and hardcoded elevation. Those were fixed in `ff0745db...`; full CI reran as `38842905325` and passed.

This is an example of the required project discipline: a green CI does not override a missing product/contract requirement.

## 10. Frozen upstream rules

- stable catalog ID remains identity authority;
- product schema 2 / receipt schema 1;
- CP23 parser evidence remains unconfirmed unless later confirmed;
- CP24 resolver authority unchanged;
- category remains non-identifying;
- commodity grouping != price comparability;
- CP27 discount/price eligibility unchanged;
- CP28 evaluation thresholds unchanged;
- CP29 search relevance never becomes identity authority;
- no duplicate mutable truth/index introduced;
- offline/privacy/permission posture unchanged.

## 11. Next planned implementation checkpoint

**CP31 — Product Detail**

Required direction:

1. STANDARD-product identity/spec header;
2. current/latest price as primary focus;
3. previous and usual price kept distinct;
4. CP28 judgment with explanation/reason-safe copy;
5. one-basis historical chart using CP30 chart grammar;
6. purchase dates/stores and receipt traceability;
7. explicit insufficient/no-judgment states;
8. responsive behavior from CP30 width policy;
9. no cross-basis mixing or identity inference from UI/search;
10. no incidental redesign of capture/review/commodity detail/shell.

CP31 is planned, not automatically authorized.

## 12. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipts, real purchase DB/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

## 13. Stop condition

**CP30 is complete and handoff-synchronized. Await explicit authorization for CP31.**
