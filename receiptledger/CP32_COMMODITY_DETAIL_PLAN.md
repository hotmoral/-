# ReceiptLedger V1 — CP32 Commodity Detail Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_COMMODITY_DETAIL_01`

## 1. Product objective

CP32 builds the commercial NON_STANDARD commodity detail experience on top of frozen CP21–31 contracts.

The screen must let a user answer quickly:

1. What commodity is this?
2. What was my most recent recorded purchase and purchase form?
3. Which historical prices are directly comparable?
4. For a strict basis such as kg/L/each, is the latest comparable price cheap, typical or expensive versus my own prior purchases?
5. Which package-form histories are reference-only?
6. Which receipts support every row?

The screen presents existing truth. It must not manufacture conversions or new price policy.

## 2. Experience direction

Carry forward CP31's commercial direction: **quiet confidence / price-first / evidence-backed**.

NON_STANDARD requires an additional rule: **clarity before apparent simplicity**. The UI must not make unlike purchase forms look comparable merely to create one clean chart or one headline judgment.

Design principles:

- commodity identity is simple and stable;
- the latest purchase record remains visible even when it cannot be judged;
- strict normalized bases are visibly separated;
- contextual package forms are visibly reference-only;
- semantic text accompanies all color;
- typography/whitespace create hierarchy before borders/cards;
- no shopping-promotion language, market-price claims or fake normalization;
- no raw enum/reason/ID strings in normal user copy.

## 3. Frozen upstream boundary

CP32 consumes without reinterpretation:

- CP21 stable-ID catalog equality;
- CP22 product schema 2 / receipt schema 1;
- CP23 semantic evidence authority;
- CP24 identity resolver authority;
- CP25 category non-authority;
- CP26 commodity grouping != comparability and raw PurchaseForm preservation;
- CP27 basis derivation and receipt-traceable observations;
- CP28 deterministic evaluation policy;
- CP29 read-only discovery authority;
- CP30 design-system grammar;
- CP31 commercial composition/accessibility quality bar.

No schema migration is permitted.

## 4. Comparison contract

CP32 supports NON_STANDARD only.

Strict normalized bases:

- weight: kg/g observations -> `WEIGHT_KG` -> displayed as `원/kg`;
- volume: L/mL observations -> `VOLUME_L` -> displayed as `원/L`;
- count: exact count observations -> `EACH` -> displayed as `원/개`.

These three bases are independent. A commodity may have more than one strict basis, but they never enter the same chart, baseline or judgment.

Contextual bases:

- bag/pack/box/bundle/other forms -> `LIKE_FORM:<form>`;
- may preserve same-form reference history;
- always receive CP28 `CONTEXTUAL_ONLY` and no cheap/expensive judgment;
- never convert to kg/L/each without exact evidence;
- different LIKE_FORM keys remain separate.

Examples that must stay forbidden:

- `1봉 = 1kg`;
- `1상자 = N개` without exact receipt/catalog evidence;
- connecting kg and each observations in one chart;
- showing contextual package-form history with positive/negative judgment tone.

## 5. Read model

Add one read-only Commodity Detail projection assembled from:

- `CatalogProduct` and optional `CatalogEntryV2` commodity identity;
- `PriceIntelligenceServiceV2` observations/cohorts;
- `PriceEvaluationServiceV1`, applied separately to each cohort;
- receipt provenance already carried by CP27 observations.

Required projection groups:

- `strictSections`: one per WEIGHT_KG / VOLUME_L / EACH cohort;
- `contextualSections`: one per LIKE_FORM cohort;
- `purchases`: all observations newest first, including excluded observations;
- `latestPurchase`: first receipt-traceable observation if present.

No duplicated mutable price truth/cache/table may be added.

## 6. Information architecture

### 6.1 Header

- screen context `품목 상세`;
- canonical commodity name as primary identity;
- no STANDARD-only brand/variant/spec fields;
- category may be shown only when a safe user-facing label already exists; raw IDs are forbidden.

### 6.2 Latest purchase record

Show the most recent receipt-linked observation as provenance, not as a global comparison verdict.

Display where available:

- purchase amount or receipt line amount with truthful label;
- purchase form (`500g`, `2봉`, `5개` etc.);
- date/store;
- comparison status.

If latest purchase is contextual or excluded, the screen must say so explicitly. It must not silently substitute an older strict observation and call it the latest purchase.

### 6.3 Strict comparison sections

Each strict basis gets an independent section.

For each section show:

- basis title and explicit unit (`무게 기준 · 원/kg`, etc.);
- latest normalized price;
- CP28 judgment/presentation;
- explanation and baseline evidence;
- previous price;
- usual price when available;
- basis-specific actual-purchase chart;
- purchase count.

The most recently observed strict basis may appear first, but no basis becomes global authority over the commodity.

### 6.4 Contextual form section

Group LIKE_FORM cohorts under `포장 형태 참고 이력`.

Each group shows:

- exact form label;
- latest same-form reference price;
- previous same-form reference when available;
- count;
- explicit copy that no cheap/expensive judgment is made and it is not compared with kg/L/each or other forms.

CP32 does not need a contextual line chart. Avoiding one reduces the risk that reference-only data appears mathematically equivalent to strict normalized history.

### 6.5 Purchase history

Newest first, all receipt-linked observations retained.

Rows show:

- date/store;
- purchase form;
- attributable/printed amount when available;
- strict normalized rate OR contextual reference rate OR explicit exclusion status;
- receipt navigation.

Excluded rows remain provenance-visible and never enter a chart or CP28 judgment.

## 7. Responsive composition

Compact/medium:

`identity -> latest purchase -> strict comparisons -> contextual forms -> purchase history`

Expanded + height >=480dp:

- left: identity + latest purchase + comparison-safety explanation;
- right: strict/contextual sections + purchase history.

Use CP30 max-width/gutter/two-pane policy exactly.

## 8. Accessibility

- minimum action target >=48dp; purchase rows >=64dp;
- chart has a Korean accessibility summary;
- basis/unit text is adjacent to every normalized price;
- judgment never relies on color alone;
- contextual/reference-only state has explicit text;
- chart interaction never requires tapping tiny points;
- SP conversion respects nonlinear font scaling.

## 9. Implementation scope

Expected changes:

- new `commoditydetail/**` read model/service/formatter/chart;
- new `CommodityDetailActivity`;
- minimal NON_STANDARD route from existing `PriceHistoryActivity`;
- Korean strings;
- manifest registration;
- deterministic CP32 unit tests;
- ReceiptLedger-prefixed CP32 workflow;
- version `1.0.30-commodity-detail` / versionCode 31.

## 10. Explicit non-goals

- CP33 Capture/Review UX redesign;
- CP34 home/navigation shell;
- STANDARD Product Detail redesign;
- identity merge/relink changes;
- category authority changes;
- new conversion tables or guessed package weights;
- CP28 threshold changes;
- schema migration;
- FTS/index/cache work;
- Compose/AppCompat/Material migration;
- final icon-library/dark-theme/motion work.

## 11. Commercial-quality acceptance

CP32 closes only if:

1. latest purchase and latest comparable basis are not conflated;
2. WEIGHT_KG / VOLUME_L / EACH stay isolated;
3. LIKE_FORM is unmistakably reference-only;
4. no fake conversion appears in model, formatter, chart or copy;
5. CP28 judgment is applied per strict cohort only;
6. contextual cohorts remain `CONTEXTUAL_ONLY`;
7. charts are single-basis and actual-purchase only;
8. all purchase rows remain receipt-traceable;
9. empty/insufficient/excluded states look intentional;
10. CP30/31 visual and accessibility grammar is consumed rather than forked;
11. compact/expanded policy remains correct;
12. CP21–31 regressions pass;
13. lint/build/permission/evidence checks pass;
14. final plan-to-code review finds no material omission.

## 12. Stop condition

After exact CP32 implementation/evidence refs and handoff docs are frozen, stop before CP33.