# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP31 — Product Detail — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-product-detail-20261016`
- predecessor CP30 handoff: `f67e39654d1d4cfdc2cd6fce8e7c16f72ed34b60`
- frozen CP31 implementation HEAD: `1d2e7ef67e949af9098027a78e30551c228c255c`
- canonical Actions run: `38852423981` — SUCCESS
- job: `116816787905` — SUCCESS
- artifact ID: `12025398048`
- artifact digest: `sha256:d4ad68382e6b666f796345c452c42e18f03ef1bd3084d18182a78059da0b4b0f`
- debug APK SHA-256: `8be04d623cc0bea95f87868dca2a45a774440e0dddc3cd32be5a63baf867e3ae`
- CP31 9/9, CP30 9/9, CP29 8/8, CP28 8/8, CP27 8/8 PASS in packaged evidence
- prior targeted regressions remain guarded by the full unit-test run
- lint: 0 errors / 0 warnings (`No issues found.`)
- version: `1.0.29-product-detail` / versionCode 30

Any later handoff/status commit must remain documentation-only. Executable/evidence boundary remains `1d2e7ef...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable judgment -> find/browse -> inspect`

CP31 makes the STANDARD-product `inspect` destination commercial and immediately useful without changing the upstream truth.

## 3. CP31 commercial Product Detail

Visual/product direction:

**quiet confidence / price-first / evidence-backed**

Primary hierarchy:

1. exact product identity;
2. recent purchase price;
3. personal-history judgment and reason;
4. previous/usual price context;
5. actual-purchase price trend;
6. receipt-traceable purchase history.

The screen deliberately avoids shopping-promotion language, decorative sale badges, market-price claims, raw enums/IDs and debug-oriented presentation.

## 4. Frozen CP31 data contract

CP31 supports STANDARD products only.

- stable catalog ID remains identity authority;
- structured brand/product/variant/specification is read from canonical V2 data when present;
- legacy STANDARD falls back to canonical name without guessing fields;
- price observations come from CP27;
- evaluation/latest/previous/usual/judgment come from CP28;
- STANDARD chart basis is exactly `STANDARD_PACKAGE`;
- UI does not implement replacement thresholds or unit normalization;
- excluded observations remain provenance but cannot enter chart/evaluation values;
- purchase rows preserve receipt traceability and open the existing Receipt Detail.

## 5. UI / accessibility / responsive result

CP31 consumes the frozen CP30 design system:

- PRICE_HERO/title/body/label typography roles;
- spacing/radius/elevation tokens;
- semantic text + color state presentations;
- minimum interaction target rules;
- max-width/gutter policy;
- compact `<600dp`, medium `600..839dp`, expanded `>=840dp`;
- two-pane only expanded + height >=480dp.

`ProductPriceChartViewV1` plots actual purchases oldest -> newest, emphasizes the latest point, shows a usual-price reference only for evaluated histories, and exposes a Korean accessibility summary.

History rows are >=64dp and carry date/store/price or exclusion context plus receipt navigation.

## 6. Architecture / safety boundary

- existing `Activity + android.widget` architecture preserved;
- no Compose/AppCompat/Material migration;
- no custom/downloadable font;
- product schema 2 / receipt schema 1 unchanged;
- CP21–30 identity/category/commodity/price/evaluation/search semantics unchanged;
- Main capture/OCR, Receipt Detail and Receipt Review behavior unchanged;
- no duplicate price truth/cache/index introduced;
- forbidden CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE permissions remain absent.

## 7. Canonical metric

`CP31_METRICS product_detail_version=1 standard_basis=1 identity_fallbacks=1 price_states=8 responsive_cases=6 traceability=1 chart_single_basis=1 purchase_rows=4`

This is deterministic contract evidence, not device visual-usability evidence.

## 8. Pre-closeout correction history

CP31 was deliberately not closed on the first build attempt or first green run.

- first run `38851792728` found two implementation compile errors;
- after functional green, plan/code review caught chart `DrawAllocation` and it was fixed;
- another green run still exposed direct `scaledDensity` use inconsistent with modern nonlinear font scaling; it was replaced with Android SP dimension conversion;
- final HEAD `1d2e7ef...` passed canonical run `38852423981` with lint `No issues found.`

Only the final HEAD/run pair is canonical.

## 9. Known limitations

- CP32 NON_STANDARD Commodity Detail not yet implemented;
- Capture/Review UX V2 remains CP33;
- final commercial home/navigation shell remains CP34;
- final icon artwork/library still not selected;
- no dark-theme finalization;
- CP31 has no emulator/device screenshot or real-user usability evidence yet.

## 10. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> CP29 Search / Browse -> CP30 Design System Foundation -> **CP31 Product Detail**.

## 11. Next planned checkpoint

**CP32 — Commodity Detail**

Goal: build the NON_STANDARD commodity detail experience while preserving the critical distinction between grouping and price comparability.

Required direction:

- commodity identity and purchase forms;
- strict comparable cohorts separated by basis (kg / L / each);
- contextual SAME_FORM/LIKE_FORM history visibly reference-only;
- no fake conversion such as bag = kg;
- basis-specific charts/judgments only;
- receipt/store/date traceability;
- CP30 design grammar and CP31 commercial quality bar where semantically applicable.

Do not begin CP32 without explicit user authorization.

## 12. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP31_PRODUCT_DETAIL_CLOSEOUT.md`
4. `receiptledger/CP31_PRODUCT_DETAIL_EVIDENCE.md`
5. `receiptledger/CP31_PRODUCT_DETAIL_PLAN.md`
6. `receiptledger/PRODUCT_DETAIL_CONSISTENCY_REVIEW.md`
7. `receiptledger/PRODUCT_DETAIL_GOLDEN_VECTORS.md`
8. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
9. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_EVIDENCE.md`
10. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
11. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
12. `receiptledger/README.md`
13. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify current handoff HEAD and frozen executable boundary separately before future work.

## 13. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

**Current stop condition: CP31 is complete. Await explicit authorization for CP32.**
