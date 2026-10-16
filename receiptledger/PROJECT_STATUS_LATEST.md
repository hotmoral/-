# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP30 — Design System Foundation — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-design-system-foundation-20261016`
- predecessor CP29 handoff: `3727db04d2207fe92c0552d4691dbf421d71444c`
- frozen CP30 implementation HEAD: `ff0745db529499171246866039521a0b83e830e4`
- canonical Actions run: `38842905325` — SUCCESS
- job: `116786812761` — SUCCESS
- artifact ID: `12022330459`
- artifact digest: `sha256:f1bcb1b2d58e328b15cf4811dd1dc107888cc2f5ba733ce1bb1ee60bf8ec0e5e`
- debug APK SHA-256: `cb35afb3ee0bf00dafad48f0b33733401661a982df11557bb01f716ca6655373`
- CP30 tests: 9/9 PASS
- CP29 8/8, CP28 8/8, CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.28-design-system-foundation` / versionCode 29

Any later handoff commit must remain documentation-only. Executable/evidence boundary remains `ff0745db...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable judgment -> find/browse -> inspect`

CP30 does not change the loop's semantics. It freezes the visual/interaction grammar through which later commercial screens will present them.

## 3. Frozen CP30 foundation

### Typography

- PRICE_HERO 30/36 bold
- TITLE_LARGE 22/28 bold
- TITLE_MEDIUM 18/24 medium
- BODY_LARGE 16/24 normal
- BODY_MEDIUM 14/20 normal
- LABEL 12/16 medium

System sans-serif remains; no custom/downloadable font.

### Layout / interaction

- spacing 4/8/12/16/24/32dp
- radii 8/12/16dp
- elevation card 1dp / floating 3dp
- minimum touch target 48dp
- list row minimum 56dp
- content max-width token 720dp

### Responsive

- compact `<600dp`
- medium `600..839dp`
- expanded `>=840dp`
- gutter 16dp compact / 24dp medium+expanded
- two-pane only expanded and height >=480dp

### Semantic presentation

8 tones: neutral / primary / positive / negative / review / error / info / disabled.

All price judgments and no-judgment states have explicit Korean text. Color never carries state meaning alone.

### Icons

10 stable semantic roles with 24dp glyph token, 48dp hit area and Korean accessibility labels. Final icon artwork/library remains a later implementation choice.

### Charts

A chart series may contain only one CP27 comparison basis. Cross-basis lines are forbidden.

## 4. Architecture / safety boundary

- existing programmatic `Activity + android.widget` architecture preserved;
- no Compose migration;
- no Material dependency added;
- product schema 2 / receipt schema 1 unchanged;
- CP21–29 domain/search/price semantics unchanged;
- Main capture/OCR flow, ReceiptDetail, ReceiptReviewDialog and manifest unchanged;
- forbidden permissions remain absent.

Representative UiKit adoption exists only in LibraryActivity and legacy PriceHistoryActivity.

## 5. Canonical metric

`CP30_METRICS typography_roles=6 semantic_tones=8 price_presentations=8 validation_presentations=4 ui_states=8 contrast_pairs=9 responsive_cases=5 chart_cross_basis_rejections=1 min_touch_dp=48 icon_roles=10 elevation_tokens=2 representative_activities=2`

Synthetic deterministic foundation evidence only; not final commercial-screen usability evidence.

## 6. Pre-closeout completeness correction

Initial HEAD `5c63a537...` and run `38842440663` were green, but pre-closeout plan/code comparison found missing centralized icon semantics and a hardcoded card elevation. Those were corrected, and the full CI reran successfully on `ff0745db...` / `38842905325`. The latter is the only canonical CP30 evidence boundary.

## 7. Known limitations

- final Product Detail/Commodity Detail screens not yet implemented;
- final chart rendering not yet implemented;
- final capture/review UX not redesigned;
- no final commercial shell/home/navigation;
- no dark-theme finalization;
- final icon artwork/library not selected;
- no real-user usability evidence yet.

## 8. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> CP29 Search / Browse -> **CP30 Design System Foundation**.

## 9. Next planned checkpoint

**CP31 — Product Detail**.

Goal: build the first commercial STANDARD-product price-memory detail surface from frozen CP21–30 data/interaction contracts.

Required direction:

- identity/specification header;
- latest, previous and usual price;
- CP28 judgment and explanation;
- single-basis price-history chart;
- store/date context;
- receipt traceability;
- insufficient/no-judgment states;
- CP30 responsive/accessibility grammar;
- no domain/search/price reinterpretation for UI convenience.

**Do not begin CP31 without explicit user authorization.**

## 10. Canonical restart order

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

GitHub is canonical. Verify branch/ref and frozen executable boundary before future work.

## 11. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

**Current stop condition: CP30 is complete. Await explicit authorization for CP31.**
