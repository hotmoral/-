# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading current files and verifying refs.

Read in order:

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

## 1. Latest executable checkpoint

**CP31 — Product Detail — PASS / COMPLETE**

- branch: `receiptledger/run-v1-product-detail-20261016`
- predecessor handoff: `f67e39654d1d4cfdc2cd6fce8e7c16f72ed34b60`
- frozen implementation HEAD: `1d2e7ef67e949af9098027a78e30551c228c255c`
- canonical Actions: `38852423981` — SUCCESS
- job: `116816787905` — SUCCESS
- artifact ID: `12025398048`
- artifact digest: `sha256:d4ad68382e6b666f796345c452c42e18f03ef1bd3084d18182a78059da0b4b0f`
- APK SHA-256: `8be04d623cc0bea95f87868dca2a45a774440e0dddc3cd32be5a63baf867e3ae`
- CP31 9/9, CP30 9/9, CP29 8/8, CP28 8/8, CP27 8/8 PASS in packaged XML evidence
- full unit-test run also guards prior CP26/25/24/23/21/22/legacy suites
- lint: 0 errors / 0 warnings (`No issues found.`)
- versionName `1.0.29-product-detail`, versionCode 30

Later closeout/status commits must remain documentation-only. Do not move the executable evidence boundary from `1d2e7ef...`.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 검색/탐색 -> 제품/품목 상세 -> 과거 가격과 현재 가격 판단`

CP31 completes the STANDARD-product detail destination; it does not change the product's identity/price truth.

## 3. CP31 design direction

Commercial direction is:

**quiet confidence / price-first / evidence-backed**

The screen should answer quickly:

1. what exact product is this;
2. what did I pay most recently;
3. is that cheap/typical/expensive versus my own prior purchases;
4. why;
5. what does my actual purchase history show;
6. which receipts support it.

The UI intentionally avoids deal-promotion styling, market-price claims and engineering/debug language.

## 4. Frozen CP31 read model

`ProductDetailServiceV1` is read-only.

It consumes:

- canonical product identity from catalog stores;
- CP27 price observations/cohort;
- CP28 evaluation;
- receipt provenance.

It does not persist a new price truth, cache, alias or evaluation.

STANDARD only:

- exact basis = `STANDARD_PACKAGE`;
- no basis picker;
- no cross-basis chart;
- no artificial normalization;
- legacy STANDARD missing structured fields falls back to canonical product name.

## 5. Product Detail composition

Normal compact reading order:

`identity -> recent price -> judgment/reason -> previous/usual -> chart -> purchase history`

Price hero shows `상품 1개 기준 · 내 구매이력` context.

Previous and usual prices are distinct concepts and remain visually subordinate to the latest price.

CP28 Korean presentation is reused; thresholds are never recalculated by UI code.

## 6. Chart / traceability

`ProductPriceChartViewV1`:

- plots eligible actual purchases only;
- displays oldest -> newest;
- emphasizes latest observation;
- usual reference only for EVALUATED status;
- judgment color only for valid judgment;
- exposes Korean accessibility summary;
- uses reusable Path allocation;
- uses Android SP dimension conversion for nonlinear font scaling.

Purchase rows remain the primary detailed interaction target. They are >=64dp and open the existing `ReceiptDetailActivity` using preserved receipt IDs.

Excluded observations remain provenance-visible when rendered but never enter chart/evaluation facts.

## 7. Responsive / accessibility

Frozen CP30 policy continues:

- compact `<600dp`;
- medium `600..839dp`;
- expanded `>=840dp`;
- two-pane only expanded + height >=480dp;
- max content width and gutters from CP30;
- state meaning uses Korean text + color;
- minimum touch baseline >=48dp.

CP31 history rows exceed that minimum and the chart does not require tiny point tapping.

## 8. Minimal integration boundary

STANDARD products in the legacy Price History screen launch Product Detail.

NON_STANDARD stays on the legacy path until CP32.

Frozen/unmodified for CP31:

- Main capture/OCR flow;
- Receipt Detail behavior;
- Receipt Review behavior;
- catalog/product/semantics/identity/category/commodity/persistence/price/priceintel/priceeval/search packages;
- product schema 2 / receipt schema 1.

## 9. Pre-closeout discipline

Meaningful process history:

- first CI caught two straightforward Java implementation errors;
- later green run was not accepted because chart `DrawAllocation` remained;
- another green run was not accepted because direct `scaledDensity` use remained;
- both were corrected and final `1d2e7ef...` / `38852423981` is the only canonical CP31 execution boundary.

This repeats the project rule: green CI is necessary but not sufficient if a cheap material contract gap remains.

## 10. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Never commit secrets, signing material, private receipts, real purchase DB/backups, identifiers or uncleared assets.

Forbidden packaged permissions CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE remain absent.

## 11. Evidence limitation

No emulator/device screenshot comparison or real-user usability study is included in CP31 evidence. Do not interpret deterministic CI as pixel-perfect on-device validation.

## 12. Next planned checkpoint

**CP32 — Commodity Detail**

CP32 must focus only on NON_STANDARD commodity history and preserve:

- grouping != comparability;
- kg/g -> price/kg;
- L/mL -> price/L;
- count -> price/each;
- package/form SAME_FORM/LIKE_FORM contextual only unless strict comparability exists;
- no fake conversion such as bag = kg;
- basis-specific charts and judgments;
- receipt traceability.

Do not widen into CP33 Capture/Review or CP34 shell work.

## 13. Stop condition

**CP31 is complete and handoff-ready. Await explicit authorization for CP32.**
