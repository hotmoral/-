# ReceiptLedger V1 — CP28 Price Evaluation Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRICE_EVALUATION_01`

## 1. Product essence

ReceiptLedger should answer a repeat purchaser's practical question: **"이번 가격이 내 과거 구매 이력에 비해 싼가, 평소 수준인가, 비싼가?"**

CP28 adds only an explainable personal-history judgment over CP27-safe cohorts. It does not estimate market price, forecast future price, allocate unknown discounts, or mix incomparable products/forms.

## 2. Frozen input boundary

CP28 consumes exactly one `PriceCohortV2` produced by CP27.

Frozen upstream:

- stable product/commodity identity unchanged;
- product schema 2 unchanged;
- receipt schema 1 unchanged;
- CP27 comparison-price derivation and exclusion rules unchanged;
- no cross-cohort mixing;
- no new price table;
- no network/AI market-price opinion.

## 3. Baseline semantics

Judgment compares the **latest eligible observation** to a historical baseline that never contains that latest observation.

Canonical V1 baseline:

- minimum prior observations: 3;
- take at most the 5 most recent prior observations from the same CP27 cohort;
- `usualPrice` = median of those prior observations;
- older observations outside that five-observation window do not move the current baseline;
- previous-purchase change remains separately visible and is not the baseline judgment.

Why: including the latest price in its own baseline creates self-reference; an all-history mean is too sensitive to stale history/outliers.

## 4. Judgment thresholds

The V1 policy uses two materiality gates so tiny currency differences or tiny percentages are not overstated.

Material change requires both:

- absolute difference >= 100 minor currency units;
- absolute percentage difference >= 5%.

Extreme change requires both:

- absolute difference >= 500 minor currency units;
- absolute percentage difference >= 15%.

Labels:

- below extreme thresholds -> `VERY_CHEAP`;
- below material thresholds -> `CHEAP`;
- not material by both gates -> `TYPICAL`;
- above material thresholds -> `EXPENSIVE`;
- above extreme thresholds -> `VERY_EXPENSIVE`.

Exact threshold boundaries are inclusive.

These constants are explicit personal-history V1 product heuristics, not a claim about external market value.

## 5. Data-sufficiency / no-judgment states

No cheap/expensive label when:

- fewer than 3 prior comparable observations -> `INSUFFICIENT_HISTORY`;
- CP27 cohort is `CONTEXTUAL_LIKE_FORM` -> `CONTEXTUAL_ONLY`;
- historical median is <= 0 -> `NON_POSITIVE_BASELINE`;
- no latest eligible price -> `INSUFFICIENT_HISTORY`.

A contextual 봉/팩/상자 history can still show latest/previous facts but cannot claim normalized cheap/expensive judgment because physical content may differ.

## 6. Explainability contract

Every result exposes:

- CP27 comparison basis and strength;
- status and judgment;
- reason code;
- current/latest price;
- immediately previous price and delta/percent when available;
- baseline sample count and window size;
- baseline receipt IDs;
- usual-price median;
- current-vs-usual delta and percent;
- frozen threshold constants.

No natural-language generative opinion is needed for correctness.

## 7. Scope / non-goals

In scope:

- pure deterministic `priceeval/**` domain layer;
- policy + result + evaluator;
- bounded golden tests/metrics;
- full upstream regression/lint/build/evidence.

Out of scope:

- search/browse (CP29);
- charts/UI polish (CP30+);
- market/online prices;
- predictive pricing;
- merchant consolidation;
- item-level discount attribution redesign;
- user-customizable thresholds;
- time-decay/seasonality models.

## 8. Acceptance

CP28 passes only if:

1. latest observation is provably excluded from baseline;
2. only recent 5 prior observations can affect baseline;
3. at least 3 prior observations are required;
4. median baseline is deterministic;
5. percentage and absolute materiality gates both apply;
6. threshold boundaries are deterministic;
7. contextual LIKE_FORM never receives cheap/expensive labels;
8. non-positive baseline never divides for percentage judgment;
9. previous-purchase change remains separate from usual-price judgment;
10. CP27 and upstream tests remain green;
11. lint/build/privacy/permission checks pass;
12. handoff documents are synchronized and work stops before CP29.
