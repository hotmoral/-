# ReceiptLedger V1 — CP31 Product Detail Golden Vectors

Updated: 2026-10-16 KST

## PD01 STANDARD identity hierarchy

Given a native V2 STANDARD product with brand, productName, variant and specification:

- stable ID remains unchanged;
- brand is secondary identity text;
- productName/canonical identity is primary;
- variant and exact specification are supporting text;
- no field is inferred from search/category/store.

## PD02 Legacy STANDARD fallback

Given a legacy STANDARD product with no structured V2 fields:

- canonical name is still shown as primary identity;
- missing structured fields are omitted;
- Product Detail remains usable and does not invent metadata.

## PD03 Current / previous / usual separation

For one STANDARD_PACKAGE cohort with latest=3,000, previous=3,200 and valid usual=3,500:

- current = 3,000원;
- previous = 3,200원;
- usual = 3,500원;
- these values have distinct labels and hierarchy;
- the UI must not substitute cohort median for CP28 usual price.

## PD04 Evaluated judgment

Given CP28 EVALUATED/CHEAP:

- label uses frozen Korean semantic presentation `평소보다 저렴`;
- positive tone is permitted;
- usual-price delta/reason evidence is shown without exposing raw reason code;
- market-price language is absent.

## PD05 Insufficient history

Given CP28 INSUFFICIENT_HISTORY:

- label uses `비교 데이터 부족`;
- no cheap/expensive tone is used;
- latest price may still be shown when available;
- usual-price metric is explicitly unavailable/insufficient, not zero.

## PD06 Single-basis chart

Given STANDARD Product Detail:

- chart series basis = STANDARD_PACKAGE only;
- axis label = `원/상품`;
- mixed basis input is rejected;
- latest observed purchase point is visually distinguished;
- usual-price reference exists only when CP28 status is EVALUATED.

## PD07 Chart chronology

Given newest-first CP27 observations:

- visual x-order is oldest -> newest;
- purchase points represent actual receipt observations only;
- no synthetic daily/monthly interpolation points are generated.

## PD08 Purchase history traceability

For every rendered history row:

- receipt ID remains available internally for navigation;
- date/store context is shown when present;
- tapping the row opens the existing receipt detail;
- Product Detail does not duplicate or rewrite the receipt record.

## PD09 Excluded observation

Given an observation excluded by CP27:

- it does not enter chart/evaluation values;
- provenance may remain visible as `가격 비교 제외` with safe Korean explanation;
- exclusion does not become an error judgment about the product.

## PD10 Responsive composition

- 360dp width -> single column;
- 599dp -> single column;
- 600dp -> single column;
- 839dp -> single column;
- 840x479dp -> single column;
- 840x480dp -> two-pane eligible.

## PD11 Accessibility

- interactive receipt-history row target >=48dp;
- chart has non-empty Korean accessibility summary;
- judgment is understandable without color;
- price includes explicit comparison basis/context.

## PD12 Scope preservation

CP31 must leave unchanged:

- product schema 2;
- receipt schema 1;
- CP24 identity authority;
- CP27 comparison derivation;
- CP28 thresholds;
- CP29 search mutation boundary;
- Capture/Review behavior;
- forbidden permission posture.

## PD13 Commercial first-view hierarchy

On a normal compact phone with sufficient data, the first screenful prioritizes in order:

1. exact product identity;
2. recent purchase price;
3. personal-history judgment;
4. previous/usual comparison context.

Debug metadata, IDs and raw enums are absent from this first-view hierarchy.

## PD14 Deterministic metric

Expected CP31 metric should report at minimum:

`product_detail_version=1 standard_basis=STANDARD_PACKAGE identity_fallbacks=1 price_states=8 responsive_cases=6 traceability=1 chart_single_basis=1`

The final metric may add fields but must preserve deterministic coverage of these contracts.
