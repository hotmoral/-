# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, browse/search it, inspect personal historical prices, and judge whether a current price is cheap/normal/expensive without fake normalization of non-standard goods.

Every checkpoint requires explicit user authorization and closes with exact evidence plus handoff synchronization.

## 1. Completed product/storage stages

### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE
Frozen essence: personal purchase-price memory and comparison.

### CP21 — Catalog Domain V2 — COMPLETE
Stable-ID identity, STANDARD/NON_STANDARD boundary, structured product fields, exact physical measures, raw purchase forms, category non-authority, contextual aliases and source/confidence/confirmation separation.

### CP22 — Persistence V2 — COMPLETE
Frozen implementation `449896c7580fb3412f41c9b58d1ab9412d13d84d`; Actions `38816200340` SUCCESS. Product schema 2; receipt schema 1; legacy IDs/links preserved; direct SQLite retained.

### CP23 — Receipt Product Semantics — COMPLETE
Frozen implementation `5bffb66bd43814f8d638791b5697f79ff089028b`; Actions `38822100885` SUCCESS. Conservative unconfirmed semantic evidence; standalone physical-measure ambiguity remains review-gated.

### CP24 — Identity Resolver V2 — COMPLETE
Frozen implementation `4b556afd4dd52b68cf768e937bb456665ad4c231`; Actions `38824134990` SUCCESS.

Authority: MERCHANT exact alias -> GLOBAL exact alias -> unique strict semantic exact -> review/suggestion -> unresolved. Resolver never auto-creates/merges identities. Local metrics: correct auto-links 14/14, false merge 0, false split risk 1/20, repeat confirmed reuse 4/4.

### CP25 — Category System — COMPLETE
Frozen implementation `042c3b59063f0e58a273a5f685b25780683fcf36`; Actions `38827880730` SUCCESS.

Frozen category contract:

- bounded 28-node FOOD/HOUSEHOLD taxonomy;
- category is browse/classification metadata only, never identity authority;
- persisted category reuses before classification rules;
- unique high-confidence rule -> AUTO_ASSIGNABLE;
- generic/conflicting evidence -> REVIEW;
- unsupported evidence -> UNRESOLVED; no forced OTHER;
- correction changes only CategoryRef on the same stable catalog ID;
- existing product-schema-v2 `category_refs` is reused; no schema migration.

Local metrics:

- fixtures 30 / known category 28;
- auto suggestions 24, correct 24, incorrect 0;
- review-required 6, unresolved 2;
- persisted repeat reuse 4/4;
- correction reuse 3/3.

## 2. Stage C — Identity and classification

### CP26 — Commodity / Non-standard V2 — NEXT PLANNED

Goal: make common non-standard commodity history useful across heterogeneous purchase forms without creating fake comparability.

Must include:

- stable commodity identity for concepts such as 감자/사과/대파;
- preserve observed sales form/unit/quantity such as 봉/팩/단/상자/개/kg/g;
- same commodity can group heterogeneous observations;
- grouping != comparability remains explicit;
- no guessed conversion or arbitrary package equivalence;
- deterministic suggestion/review/confirmation reuse boundary;
- false grouping rate;
- false splitting/fragmentation rate;
- raw unit/form preservation rate;
- review burden and repeat confirmed reuse metrics;
- category remains metadata only;
- do not prematurely implement CP27 price-comparison statistics.

## 3. Stage D — Price intelligence

### CP27 — Price Intelligence V2

Before statistics, define the canonical comparison price for one purchase observation, covering quantity >1, item discounts, unallocated receipt coupons, provenance, invalid observations, exact packaged identity and like-unit NON_STANDARD subsets. Then provide deterministic latest/previous, delta, min/max, mean/median, period and store-aware metrics.

### CP28 — Price Evaluation

Define explicit data-sufficiency/window/threshold rules for cheap/normal/expensive labels. Sparse data yields `데이터 부족`.

## 4. Stage E — Find and inspect

### CP29 — Search / Browse

Global search/browse by product/commodity, brand, safe aliases, category, specification, store, recent/frequent and price change. Freeze data access/interaction behavior before final visual polish.

## 5. Stage F — Commercial UX

### CP30 — Design System Foundation
Freeze typography, color, spacing, shapes, icons, cards, fields, chart grammar, feedback states and accessibility baseline.

### CP31 — Product Detail
Commercial STANDARD price-memory screen with graph, recent/previous/typical price, store context, comparison-price explanation and receipt traceability.

### CP32 — Commodity Detail
Commercial NON_STANDARD mixed-form history without misleading aggregate comparison.

### CP33 — Capture / Review UX V2
Move toward `영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`; acceptance includes review burden and repeat-use automation.

### CP34 — Commercial UI Shell
Product-centric home/navigation/search/category/product/commodity/receipt/settings integration without gratuitous domain rewrite.

## 6. Stage G — Validation and hardening

### CP35 — Real Receipt Evaluation
Measure end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures. Primary metric is correct purchase registration, not OCR character accuracy alone.

### CP36 — Performance / Reliability
Verify startup, OCR latency/memory, large catalog/history, alias/search/category queries, aggregation, charts, migrations, archive reconciliation and failure recovery at representative scale.

## 7. Dependency gates

- CP21 stable-ID identity semantics remain frozen.
- CP22 product schema 2 / receipt schema 1 remain frozen unless explicit amendment is justified.
- CP23 parser evidence remains unconfirmed/non-authoritative.
- CP24 resolver authority remains frozen; category cannot widen/override it.
- CP25 category remains browse/classification metadata, never identity authority.
- CP26 commodity grouping remains distinct from comparability.
- CP27 comparison-price definition precedes CP28 price judgment.
- CP29 data access precedes commercial shell dependencies.
- CP30 Design System precedes final CP31/CP32 visual implementation.
- CP33 must not bypass identity/provenance rules for convenience.

## 8. Every checkpoint asks, only where materially relevant

- Does this change stored-data meaning?
- Can it create a false merge/grouping?
- Can it create/perpetuate a false split?
- Does confirmed repeat use reduce review burden?
- Is raw receipt/purchase evidence preserved?
- Is any compared price exactly defined and receipt-traceable?
- Can incomparable prices look comparable?
- Can provenance/validation be bypassed?
- Can permissions/network/privacy posture change?
- Can a new performance hot path appear?
- Which local regression catches failure now?

Avoid ritual re-audits, speculative abstractions, unrelated cleanup and expansion into budgeting/banking/cloud/e-commerce before the core loop is complete.

## 9. Handoff discipline

At every completed group:

1. freeze exact implementation/spec HEAD;
2. record CI/artifact/evidence;
3. record limitations and failures/process anomalies that matter;
4. update status/handoff/readme/work-unit/roadmap docs;
5. verify post-boundary changes are documentation-only;
6. stop before the next unauthorized checkpoint.

## 10. Current boundary

**CP25 is COMPLETE. CP26 — Commodity / Non-standard V2 is the next planned checkpoint and must not start without explicit user authorization.**
