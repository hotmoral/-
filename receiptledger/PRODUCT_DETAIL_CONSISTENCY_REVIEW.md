# ReceiptLedger V1 — CP31 Product Detail Consistency Review

Updated: 2026-10-16 KST
Status: IMPLEMENTATION ALLOWED / PRESENTATION + READ-MODEL EXTENSION

## 1. Verdict

CP31 can implement a commercial STANDARD-product detail experience without changing catalog identity, persistence schemas, price comparability, price-evaluation policy or search authority.

The cheapest safe architecture is a read-only projection over existing CP21–30 services plus a new View-based Activity.

## 2. Identity safety

`CatalogEntryV2` already exposes stable ID, canonical name, brand, product name, variant and exact specification. Stable-ID equality remains the only entity authority.

CP31 must not infer missing brand/variant/specification from search similarity, category, merchant, receipt wording or visual proximity.

Legacy STANDARD entries may lack structured fields. The UI must degrade to canonical name rather than fabricating structured identity.

## 3. Price-data safety

`PriceIntelligenceServiceV2` already derives receipt-traceable observations and partitions them by `ComparisonBasisV2`.

For STANDARD products the canonical basis is `STANDARD_PACKAGE`; therefore the Product Detail surface requires no basis selector and can show exactly one safe historical series.

Excluded observations remain provenance records but are not chart/judgment inputs.

## 4. Evaluation safety

`PriceEvaluationServiceV1` already owns:

- latest price;
- previous price;
- previous delta;
- usual-price baseline;
- baseline count;
- delta from usual;
- cheap/typical/expensive judgment;
- minimum-history/materiality/extreme thresholds.

CP31 consumes these values. The UI must not independently implement threshold logic.

## 5. Receipt traceability

Every CP27 observation carries receipt ID, item ordinal, date, store, raw item name, eligibility and comparison price/provenance fields.

Thus CP31 can link purchase rows back to the existing Receipt Detail without a new table or duplicated history store.

## 6. Design-system compatibility

CP30 already provides:

- neutral commercial palette;
- price-hero/title/body/label typography;
- spacing/radius/elevation tokens;
- semantic Korean price-state copy;
- responsive width/two-pane policy;
- single-basis chart guardrails;
- accessibility contrast and touch-target contracts.

CP31 should extend composition, not fork a new style system. A custom chart View is acceptable because CP30 froze chart grammar but deliberately did not choose a renderer.

## 7. Visual risk review

### Risk: card soup
Mitigation: use whitespace and typography as the primary hierarchy; reserve surfaces for price judgment and clearly bounded sections.

### Risk: shopping-app exaggeration
Mitigation: no promotional badges, sale theatrics, gradients or market-price language. Semantic colors represent personal-history state only.

### Risk: current/previous/usual confusion
Mitigation: current price receives PRICE_HERO; previous/usual are secondary labeled metrics and never merged.

### Risk: chart appears like market time series
Mitigation: label it as purchase history, plot only actual purchase observations, expose dates/stores, and avoid interpolation semantics beyond connecting observed points.

### Risk: missing structured identity makes screen look broken
Mitigation: canonical name remains reliable primary identity; optional structured fields collapse cleanly.

### Risk: insufficient history looks like a negative judgment
Mitigation: frozen INFO/REVIEW state presentations; no positive/negative judgment tone when status is not EVALUATED.

## 8. Responsive risk review

- compact/medium remain single-column for predictable reading order;
- expanded two-pane is allowed only by CP30 `twoPaneEligible(width,height)`;
- max content width remains bounded;
- chart height and history rows must remain usable under font scaling and compact height.

## 9. Scope isolation

Permitted incidental changes:

- add Product Detail Activity to manifest;
- add Product Detail strings;
- add minimal STANDARD-product launch path from legacy Price History;
- add CP31-specific design helpers/tests/workflow.

Not permitted:

- redesign Receipt Detail;
- redesign Main/Capture/Review;
- implement Commodity Detail;
- introduce full app navigation shell;
- modify schemas, identity resolver or CP28 policy;
- add prohibited permissions/network use.

## 10. Result

No blocking contradiction remains. CP31 implementation is allowed as a read-only, STANDARD-only commercial presentation layer over frozen CP21–30 contracts.
