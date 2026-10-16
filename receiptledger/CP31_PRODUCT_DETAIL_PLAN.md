# ReceiptLedger V1 — CP31 Product Detail Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_DETAIL_01`

## 1. Product objective

ReceiptLedger is a personal purchase-price memory and comparison system. CP31 builds the first commercial-quality STANDARD-product detail screen that lets a user answer, within a few seconds:

1. What product is this exactly?
2. What did I pay most recently?
3. Is that price cheap, typical or expensive compared with my own prior purchases?
4. Why is that judgment being made?
5. What does the historical trend look like?
6. Which purchases and receipts support the result?

The screen presents frozen CP21–30 truth. It does not create new identity, price, search or persistence semantics.

## 2. Experience direction

Visual direction: **quiet confidence / price-first / evidence-backed**.

The screen should feel like a mature consumer utility rather than a debug dashboard, shopping promotion or finance trading screen.

Design principles:

- current purchase price is the dominant numeric focus;
- price judgment appears immediately adjacent to its evidence;
- typography and whitespace create hierarchy before borders and cards do;
- surfaces are used for semantic grouping, not to turn every datum into a card;
- primary blue is for navigation/action emphasis, not decorative saturation;
- positive/negative/review/error colors are reserved for actual semantic states;
- no gradients, decorative illustration, promotional badges or deal theatrics;
- no raw enum names, reason codes, IDs or engineering terminology in normal user copy;
- receipt provenance stays reachable from every purchase-history row.

## 3. Frozen upstream boundary

CP31 consumes without reinterpretation:

- CP21 stable catalog-ID equality and STANDARD structured identity fields;
- CP22 product schema 2 / receipt schema 1;
- CP23 semantic evidence authority;
- CP24 identity resolver authority;
- CP25 category as non-identifying metadata;
- CP26 grouping/comparability separation;
- CP27 receipt-traceable comparison observations;
- CP28 deterministic evaluation and thresholds;
- CP29 read-only search/discovery authority;
- CP30 typography, semantic tones, spacing, radii, elevation, responsive and accessibility grammar.

No schema migration is permitted for CP31.

## 4. STANDARD-product comparison contract

CP31 only supports `STANDARD_PRODUCT` / legacy `STANDARD` catalog identity.

For STANDARD products, CP27 comparison is the exact same stable package identity and uses the `STANDARD_PACKAGE` comparison basis. Therefore CP31 does not add a comparison-basis picker and does not manufacture alternate unit normalization.

A Product Detail chart contains only this one basis. If no eligible STANDARD_PACKAGE observation exists, the screen presents an explicit insufficient/unavailable state instead of inventing a price.

## 5. Read model

CP31 adds one read-only Product Detail projection assembled from canonical stores and services.

Required inputs:

- `CatalogProduct` / `CatalogEntryV2` for stable identity and structured fields;
- `PriceIntelligenceServiceV2` for receipt-derived observations and the STANDARD_PACKAGE cohort;
- `PriceEvaluationServiceV1` for latest/previous/usual price, deltas, judgment and baseline evidence;
- receipt-linked observation metadata for date, store and receipt traceability.

The projection may format presentation values, but must not persist duplicated price truth or recompute CP28 policy.

## 6. Information architecture

### 6.1 Header / identity

Show in descending hierarchy:

- screen context: `제품 상세`;
- brand when present;
- product name / canonical product identity;
- variant when present;
- exact package specification when present.

Unknown structured fields remain omitted/unknown; they are never guessed from the canonical display name merely to fill the UI.

### 6.2 Price hero

Primary area:

- label `최근 구매가`;
- latest comparable price in `PRICE_HERO`;
- comparison-basis text (`상품 1개 기준` / chart axis `원/상품`);
- latest purchase store/date when available.

If latest comparable price is unavailable, use an explicit state presentation instead of a numeric placeholder that looks authoritative.

### 6.3 Evaluation

Immediately below/adjacent to current price:

- frozen Korean CP28 presentation label;
- short explanation;
- when EVALUATED, the delta from usual price and usual-price basis count;
- no judgment color for insufficient/no-judgment states.

The UI never calculates a replacement threshold.

### 6.4 Secondary comparison summary

Keep `이전 가격` and `평소 가격` visually subordinate to current price but directly scannable.

- previous price comes from CP28/CP27;
- usual price comes only from valid CP28 baseline;
- missing values display a truthful unavailable/insufficient label, not zero.

### 6.5 Price history chart

The chart:

- contains only STANDARD_PACKAGE observations;
- orders observations chronologically;
- emphasizes the latest point;
- may display a usual-price reference only when CP28 status is EVALUATED;
- uses judgment color only when CP28 status is EVALUATED;
- exposes a Korean accessibility summary independent of the drawing;
- never implies market price or continuous market sampling.

The chart is purchase-history evidence, not a financial-market graph.

### 6.6 Purchase history

Newest purchase first.

Every receipt-linked observation remains traceable. Eligible rows show:

- purchase date;
- store;
- comparable purchase price;
- receipt affordance.

Excluded observations are not silently deleted from provenance. When presented, they must be labeled as excluded from price comparison with reason-safe Korean copy and must not affect the chart/judgment.

Tapping a history row opens the existing `ReceiptDetailActivity` for that receipt. CP31 does not redesign Receipt Detail.

## 7. Responsive composition

### Compact / medium

Single vertical reading flow:

`identity -> price hero -> evaluation -> previous/usual summary -> chart -> purchase history`

The content stays within the CP30 max-width contract and uses CP30 page gutters.

### Expanded + height >=480dp

Two-pane composition is permitted:

- left: identity, price hero, evaluation, previous/usual summary;
- right: chart and purchase history.

Two-pane is never enabled solely from physical device type.

## 8. Accessibility

- minimum interactive area 48dp;
- Korean content descriptions for icon-only actions;
- chart has a spoken/text summary;
- state meaning is not carried by color alone;
- text uses CP30 sp roles and supports font scaling;
- purchase rows remain operable without relying on tiny chart targets;
- large numeric price remains accompanied by its basis/context.

## 9. Implementation scope

Expected source additions/changes:

- Product Detail read model/service under a dedicated detail package;
- `ProductDetailActivity`;
- lightweight programmatic price-history chart View;
- CP30-compatible reusable detail helpers only where they are genuinely reusable;
- Product Detail Korean strings;
- manifest registration;
- minimal STANDARD-product entry from the existing legacy Price History screen;
- deterministic CP31 unit tests;
- ReceiptLedger-prefixed CP31 Actions workflow;
- version increment to `1.0.29-product-detail` / versionCode 30.

## 10. Explicit non-goals

- NON_STANDARD Commodity Detail (CP32);
- capture/review redesign (CP33);
- home/navigation shell redesign (CP34);
- changing Receipt Detail UX;
- identity merge/relink rules;
- new price thresholds or market-price semantics;
- schema migration;
- FTS/index/cache work;
- Compose/AppCompat/Material migration;
- custom/downloadable fonts;
- final icon-library selection;
- unrelated dark-theme or motion-system work.

## 11. Commercial-quality acceptance

CP31 does not close merely because it compiles. It closes only if plan, implementation and evidence jointly show:

1. first-view hierarchy clearly prioritizes current price and personal-history judgment;
2. identity/specification is legible without competing with price;
3. previous and usual prices remain semantically distinct;
4. CP28 judgment/no-judgment copy is preserved and explainable;
5. chart is basis-safe, chronologically coherent and accessible;
6. purchase history provides direct receipt traceability;
7. insufficient/error states look intentional rather than broken;
8. compact and expanded layouts obey CP30 policy;
9. no screen-local visual system competes with CP30 tokens;
10. no domain/schema/search/permission mutation occurs;
11. CP21–30 targeted regressions pass;
12. lint/build/permission/evidence checks pass;
13. a final plan-to-code review finds no material omission before closure.

## 12. Stop condition

After exact CP31 implementation/evidence refs and handoff docs are frozen, stop before CP32.
