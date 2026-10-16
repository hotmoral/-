# ReceiptLedger V1 — CP31 Product Detail Closeout

Updated: 2026-10-16 KST

## 1. Result

**PASS / COMPLETE**

CP31 delivers the first commercial STANDARD-product price-memory detail surface on top of frozen CP21–30 contracts.

Canonical executable/evidence boundary:

- branch: `receiptledger/run-v1-product-detail-20261016`
- predecessor handoff: `f67e39654d1d4cfdc2cd6fce8e7c16f72ed34b60`
- frozen implementation HEAD: `1d2e7ef67e949af9098027a78e30551c228c255c`
- canonical Actions run: `38852423981` — SUCCESS
- job: `116816787905` — SUCCESS
- artifact ID: `12025398048`
- artifact digest: `sha256:d4ad68382e6b666f796345c452c42e18f03ef1bd3084d18182a78059da0b4b0f`
- debug APK SHA-256: `8be04d623cc0bea95f87868dca2a45a774440e0dddc3cd32be5a63baf867e3ae`
- version: `1.0.29-product-detail`, versionCode 30
- CP31 tests: 9/9 PASS
- lint: 0 errors / 0 warnings (`No issues found.`)

## 2. Product/design outcome

Visual direction is **quiet confidence / price-first / evidence-backed**.

The first-view hierarchy is deliberately:

1. exact product identity;
2. recent purchase price;
3. personal-history judgment;
4. previous/usual price context;
5. purchase-price trend;
6. receipt-traceable purchase history.

The screen uses CP30 typography, spacing, semantic tones, radius/elevation and responsive rules. It avoids promotional deal theatrics, gradients, decorative badges, market-price language and debug metadata.

## 3. Read-model architecture

CP31 adds a read-only Product Detail projection and service. It composes existing canonical truth from:

- `CatalogProduct` / optional `CatalogEntryV2`;
- `PriceIntelligenceServiceV2`;
- `PriceEvaluationServiceV1`;
- receipt-linked observation provenance.

It does not add a duplicate price table, mutable cache, new identity authority or UI-side price policy.

Legacy STANDARD products without structured V2 fields degrade to the canonical product name rather than fabricating brand/variant/specification.

## 4. Price semantics preserved

CP31 supports STANDARD products only.

STANDARD history uses exactly one CP27 basis: `STANDARD_PACKAGE`.

Therefore:

- no comparison-basis picker is introduced;
- no weight/volume/count normalization is manufactured;
- chart input is actual eligible purchase observations only;
- latest/previous/usual values come from frozen CP27/CP28 services;
- CP28 thresholds are not reimplemented in the UI;
- insufficient/no-judgment states never receive cheap/expensive semantics.

## 5. Chart / purchase-history behavior

`ProductPriceChartViewV1` is a lightweight programmatic View renderer.

- actual observed purchases only;
- chronological oldest -> newest display;
- latest point visually emphasized;
- usual-price reference only when CP28 is `EVALUATED`;
- judgment color only when judgment is valid;
- Korean accessibility summary independent of the drawing;
- no per-frame Path allocation;
- SP conversion uses Android dimension APIs so nonlinear font scaling is respected.

The chart is intentionally not the only interaction surface. Purchase rows are >=64dp high and expose date, store, price/comparison status and direct navigation to the existing receipt detail.

Excluded CP27 observations remain provenance-visible when listed but do not enter chart/evaluation values.

## 6. Responsive/accessibility result

Compact and medium widths use one vertical reading flow.

Two-pane layout is enabled only when CP30 says it is eligible: expanded width and height >=480dp.

The implementation preserves:

- CP30 max-width/gutter policy;
- text + color semantic communication;
- >=48dp interaction baseline;
- Korean content descriptions for actionable history rows;
- chart spoken summary;
- price basis/context adjacent to the large numeric price.

## 7. Minimal integration

The legacy Price History screen now routes STANDARD products into `ProductDetailActivity`.

NON_STANDARD products remain on the existing legacy path until CP32. Receipt Detail, Capture, Review and the full navigation shell were not redesigned.

## 8. Pre-closeout corrections

CP31 was not closed on the first successful-looking state.

- initial CI `38851792728` exposed two simple Java implementation errors (`setMinimumHeight` and dp typing); both were fixed without domain changes;
- a later green implementation still had Android lint `DrawAllocation` in chart drawing; the Path was centralized/reused and CI reran;
- after that green run, source review found direct `scaledDensity` use in the chart, which is unsuitable for modern nonlinear font scaling; it was replaced with Android SP dimension conversion;
- the final HEAD `1d2e7ef...` then passed run `38852423981` with no source deprecation note from the chart and lint `No issues found.`

Only `1d2e7ef...` / `38852423981` is canonical CP31 evidence.

## 9. Frozen upstream/safety boundary

Unchanged:

- stable catalog ID identity authority;
- product schema 2 / receipt schema 1;
- CP24 resolver authority;
- CP25 category non-authority;
- CP26 grouping != comparability;
- CP27 comparison/discount eligibility;
- CP28 thresholds and judgment logic;
- CP29 search mutation boundary;
- Main capture/OCR behavior;
- Receipt Detail behavior;
- Receipt Review behavior;
- offline/privacy posture.

Packaged forbidden permissions CAMERA, broad storage/media, INTERNET and ACCESS_NETWORK_STATE remain absent.

## 10. Evidence limitation

CP31 has deterministic contract tests, build/lint/APK/permission evidence and implementation-level accessibility/responsive checks.

It does **not** claim device screenshot/pixel-perfect visual QA or real-user usability validation. Those require separate on-device evidence and should not be inferred from CI success alone.

## 11. Next planned checkpoint

**CP32 — Commodity Detail**

CP32 will handle NON_STANDARD commodity history while keeping strict normalized cohorts separate from contextual same-form history. It must not weaken the CP26/27 comparability rules merely to mirror the STANDARD screen.

## 12. Stop condition

CP31 is closed. Do not begin CP32 without explicit user authorization.
