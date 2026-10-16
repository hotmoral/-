# ReceiptLedger V1 — CP31 Product Detail Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_DETAIL_01`

## 1. Frozen executable boundary

- branch: `receiptledger/run-v1-product-detail-20261016`
- predecessor handoff: `f67e39654d1d4cfdc2cd6fce8e7c16f72ed34b60`
- frozen implementation HEAD: `1d2e7ef67e949af9098027a78e30551c228c255c`
- versionName: `1.0.29-product-detail`
- versionCode: `30`

Any later status/handoff commit must remain documentation-only. The executable/evidence boundary stays `1d2e7ef...`.

## 2. Canonical CI

- Actions run: `38852423981` — SUCCESS
- job: `116816787905` — SUCCESS
- `BUILD SUCCESSFUL`
- Gradle tasks: 49 actionable / 49 executed
- Android lint: `No issues found.`

Successful workflow stages:

1. public namespace audit;
2. CP31 scope/frozen-contract guard;
3. unit tests + lint + debug APK build;
4. deterministic CP31 metric extraction;
5. APK permission/evidence packaging;
6. public debug artifact upload.

The scope guard confirms frozen catalog/product/semantics/identity/category/commodity/persistence/price/priceintel/priceeval/search packages were not changed by CP31. MainActivity, ReceiptDetailActivity and ReceiptReviewDialog also remained frozen.

## 3. Canonical artifact

- artifact ID: `12025398048`
- artifact name: `receiptledger-v1-product-detail-38852423981`
- artifact size: `23,159,698` bytes
- artifact digest: `sha256:d4ad68382e6b666f796345c452c42e18f03ef1bd3084d18182a78059da0b4b0f`
- debug APK SHA-256: `8be04d623cc0bea95f87868dca2a45a774440e0dddc3cd32be5a63baf867e3ae`
- artifact expiry: 2026-10-30

Artifact content was independently inspected after upload; `APK_SHA256.txt`, lint report, CP31 metric and permission evidence match the canonical run.

## 4. Test evidence

Packaged XML reports:

- CP31 Product Detail: **9/9 PASS**, failures 0 / errors 0 / skipped 0
- CP30 Design System Foundation: **9/9 PASS**, failures 0 / errors 0 / skipped 0
- CP29 Search / Browse: **8/8 PASS**, failures 0 / errors 0 / skipped 0
- CP28 Price Evaluation: **8/8 PASS**, failures 0 / errors 0 / skipped 0
- CP27 Price Intelligence V2: **8/8 PASS**, failures 0 / errors 0 / skipped 0

The workflow additionally requires the prior legacy price, CP26, CP25, CP24, CP23, CP21 and CP22 test XMLs to exist after the full unit-test run; the build succeeded with that guard enabled.

## 5. Canonical CP31 metric

`CP31_METRICS product_detail_version=1 standard_basis=1 identity_fallbacks=1 price_states=8 responsive_cases=6 traceability=1 chart_single_basis=1 purchase_rows=4`

Interpretation:

- Product Detail projection version 1 exercised;
- STANDARD comparison basis frozen to one basis;
- legacy STANDARD identity fallback covered;
- frozen price/no-judgment presentation coverage retained;
- responsive boundary cases covered;
- receipt traceability covered;
- chart basis isolation covered;
- deterministic purchase-row fixture covered.

## 6. Product Detail evidence

Implementation includes:

- `ProductDetailV1` read-only projection;
- `ProductDetailServiceV1` composing canonical catalog/CP27/CP28 data;
- `ProductDetailFormatterV1` Korean presentation formatting;
- `ProductPriceChartViewV1` actual-purchase chart;
- `ProductDetailActivity` commercial STANDARD-product detail screen;
- minimal STANDARD-product route from legacy `PriceHistoryActivity`;
- deterministic CP31 unit tests.

User-facing information hierarchy:

`identity -> recent purchase price -> CP28 judgment/reason -> previous/usual price -> price trend -> receipt-traceable purchase history`

## 7. Semantic safety evidence

- CP31 service rejects NON_STANDARD scope;
- comparison basis is `ComparisonBasisV2.standardPackage()`;
- chart calls `ChartGrammarV1.requireSingleBasis`;
- UI consumes `PriceEvaluationServiceV1` results rather than reimplementing thresholds;
- structured identity fields are used only when canonical V2 data exists;
- legacy STANDARD falls back to canonical name without inference;
- excluded CP27 observations do not enter chart/evaluation values;
- purchase rows retain receipt ID and open the existing receipt detail.

## 8. Accessibility/responsive evidence

- history rows use >=64dp minimum height;
- chart exposes Korean content description summary;
- judgment text accompanies semantic color;
- price always carries `상품 1개 기준` context;
- compact/medium are single-column;
- two-pane requires expanded width + height >=480dp;
- chart Path allocation was removed from `onDraw()`;
- SP conversion uses Android dimension APIs rather than direct `scaledDensity` calculation.

Final Android lint is clean.

## 9. Permission/privacy evidence

Packaged permission evidence contains only the app's internal dynamic-receiver permission:

`com.receiptledger.v1.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

Forbidden CAMERA, READ_MEDIA_IMAGES, broad storage, INTERNET and ACCESS_NETWORK_STATE permissions are absent.

Product schema = 2 and receipt schema = 1 remain unchanged. Debug signing only.

## 10. Non-blocking notices

- Gradle reports build-system deprecated features relevant before Gradle 9;
- bundled ML Kit native library is packaged unstripped;
- GitHub-hosted actions report Node.js 20 action-runtime transition notices.

These are existing infrastructure notices, not CP31 functional/UI contract failures.

## 11. Evidence limitation

CI validates contracts, code, lint, artifact integrity, permissions and deterministic layout policy. No emulator/device screenshot comparison or real-user usability study is included in this checkpoint evidence.

## 12. Conclusion

**CP31 Product Detail = PASS / COMPLETE.**

Canonical executable/evidence boundary is `1d2e7ef67e949af9098027a78e30551c228c255c` with Actions run `38852423981`.
