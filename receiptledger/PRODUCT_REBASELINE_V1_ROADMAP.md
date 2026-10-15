# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, inspect personal historical prices, and judge whether a current price is cheap/normal/expensive without fake normalization of non-standard goods.

Every checkpoint requires explicit user authorization and closes with exact evidence plus handoff synchronization.

## 1. Completed product/storage stages

### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE

Frozen product essence: personal purchase-price memory and comparison.

### CP21 — Catalog Domain V2 — COMPLETE

Frozen semantics: Product/Commodity boundary, stable-ID identity, structured STANDARD fields, exact physical measures, raw purchase forms, category non-authority, global/merchant alias context and source/confidence/confirmation separation.

### CP22 — Persistence V2 — COMPLETE

Frozen implementation: `449896c7580fb3412f41c9b58d1ab9412d13d84d`; Actions `38816200340` SUCCESS.

Product schema v2 stores CP21 semantics while preserving legacy IDs/links. Receipt schema stays v1 and remains the price/date/store truth source. Direct SQLite is retained.

### CP23 — Receipt Product Semantics — COMPLETE

Frozen implementation: `5bffb66bd43814f8d638791b5697f79ff089028b`; Actions `38822100885` SUCCESS.

CP23 parses receipt item names into conservative unconfirmed semantic evidence without identity authority.

Frozen parsing rules include:

- explicit/known brand evidence only;
- explicit parenthetical variant only;
- `입/개입` and multipack parsing;
- standalone weight/volume remains package-vs-purchase-form ambiguous and review-gated;
- raw package forms preserved without guessed conversion;
- parser confidence never grants merge authority.

Local synthetic metrics: precision 96.9696%, recall 94.1176%, ambiguity review-gating 10/10.

## 2. Stage C — Identity and classification

### CP24 — Identity Resolver V2 — NEXT PLANNED

Goal: convert safe evidence and confirmed knowledge into deterministic catalog-link decisions while minimizing both false merge and false split.

Must include:

- exact GLOBAL vs MERCHANT alias precedence;
- confirmed-decision reuse;
- deterministic candidate ranking;
- explicit auto-link authority boundary;
- ambiguity/review path;
- false merge rate;
- false split / identity-fragmentation rate;
- automatic link success rate;
- incorrect automatic decision rate;
- review-required rate;
- repeat-purchase reuse rate after confirmation.

CP23 parser confidence alone is not identity authority. Fuzzy/semantic similarity remains suggestion evidence unless separately proven safe.

### CP25 — Category System

Taxonomy, persistence, assignment, suggestion, correction and reuse. Category never proves product identity.

Measure category suggestion accuracy and review burden locally.

### CP26 — Commodity / Non-standard V2

Make mixed raw forms such as 봉/팩/kg/개/상자 first-class while preserving grouping != comparability and prohibiting guessed conversion.

Measure commodity grouping correctness, false grouping/splitting, raw-unit preservation and review burden locally.

## 3. Stage D — Price intelligence

### CP27 — Price Intelligence V2

Before statistics, define the canonical comparison price for one purchase observation.

At minimum cover:

- line amount vs one purchased unit/package;
- quantity > 1;
- item-specific discounts;
- unallocated receipt-level coupons/discounts;
- provenance;
- invalid/incomplete observations;
- same-product package identity;
- like-unit NON_STANDARD subsets.

Then provide deterministic latest/previous, delta, min/max, mean/median, period and store-aware metrics.

### CP28 — Price Evaluation

Define explicit data-sufficiency, window and threshold rules for cheap/normal/expensive labels. Sparse data yields `데이터 부족`.

## 4. Stage E — Find and inspect

### CP29 — Search / Browse

Global search/browse by product/commodity, brand, safe aliases, category, specification, store, recent/frequent and price change. Freeze data access/interaction behavior; final visual polish is later.

## 5. Stage F — Commercial UX

### CP30 — Design System Foundation

Freeze typography, color, spacing, shapes, icons, cards, fields, chart grammar, feedback states and accessibility baseline before final detail screens.

### CP31 — Product Detail

Commercial STANDARD price-memory screen: graph, recent/previous/typical price, store context, comparison-price explanation and source-receipt traceability.

### CP32 — Commodity Detail

Commercial NON_STANDARD mixed-form history without misleading aggregate comparison.

### CP33 — Capture / Review UX V2

Move toward:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

Acceptance includes review burden and repeat-use automation, not only visuals.

### CP34 — Commercial UI Shell

Product-centric home/navigation/search/category/product/commodity/receipt/settings integration without gratuitous domain rewrite.

## 6. Stage G — Validation and hardening

### CP35 — Real Receipt Evaluation

Measure end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures. Primary metric is correct purchase registration, not OCR character accuracy alone.

CP35 aggregates earlier local metrics; it is not the first quality check.

### CP36 — Performance / Reliability

Verify startup, OCR latency/memory, large catalog/history, alias/search queries, aggregation, charts, migration, archive reconciliation and failure recovery at representative scale.

## 7. Dependency gates

- CP21 identity semantics remain frozen.
- CP22 persistence semantics remain frozen unless an explicit amendment is required.
- CP23 evidence semantics remain unconfirmed and non-authoritative.
- CP24 must measure both false merge and false split and prove repeat-use automation behavior.
- CP25 category remains browse metadata, never identity authority.
- CP26 grouping remains distinct from comparability.
- CP27 comparison-price definition precedes CP28 price judgment.
- CP29 data access precedes commercial shell dependencies.
- CP30 Design System precedes final CP31/CP32 visual implementation.
- CP33 must not bypass identity/provenance rules for convenience.

## 8. Every checkpoint asks, only where materially relevant

- Does this change stored-data meaning?
- Can it create a false merge?
- Can it create/perpetuate a false split?
- Does confirmed repeat use reduce review burden?
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
3. record limitations and superseded failures;
4. update status/handoff/readme/work-unit/roadmap docs;
5. verify post-boundary changes are documentation-only;
6. stop before the next unauthorized checkpoint.

## 10. Current boundary

**CP23 is COMPLETE. CP24 — Identity Resolver V2 is the next planned checkpoint and must not start without explicit user authorization.**
