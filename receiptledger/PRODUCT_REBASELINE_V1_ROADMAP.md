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

CP23 parses receipt item names into conservative unconfirmed semantic evidence without identity authority. Standalone physical measures remain ambiguous/review-gated; parser confidence never grants merge authority.

Local synthetic metrics: precision 96.9696%, recall 94.1176%, ambiguity review-gating 10/10.

## 2. Stage C — Identity and classification

### CP24 — Identity Resolver V2 — COMPLETE

Frozen implementation: `4b556afd4dd52b68cf768e937bb456665ad4c231`; Actions `38824134990` SUCCESS.

Frozen resolver contract:

- MERCHANT exact alias precedes GLOBAL exact alias;
- confirmed alias conflicts/dangling targets are review-gated;
- unique strict semantic auto-link requires confirmed exact productName and specification plus confirmed symmetric brand/variant when applicable;
- weaker semantics produce suggestion/review, not forced identity;
- resolver never auto-creates or merges catalog rows;
- fuzzy/edit-distance/embedding/phonetic similarity is not auto-link authority;
- user confirmation learns the narrowest useful alias scope;
- NON_STANDARD semantic grouping remains deferred to CP26.

Local synthetic metrics:

- known identity 20;
- auto-links 14, correct 14, incorrect 0;
- false merge 0;
- false split / fragmentation risk 1/20 = 5%;
- repeat confirmed reuse 4/4 = 100%;
- review-required 6, unresolved 4.

The fragmentation-risk fixture remains visible. It must be reduced through better evidence/review/confirmed knowledge, not by unsafe merge broadening.

### CP25 — Category System — NEXT PLANNED

Goal: make product/commodity browsing useful through stable category metadata while keeping category completely outside identity authority.

Must include:

- smallest useful V1 taxonomy/hierarchy;
- stable category identity and persistence;
- assignment/suggestion rules;
- explicit confidence/review boundary;
- user correction;
- safe confirmed reuse;
- STANDARD and NON_STANDARD compatibility;
- deterministic local category suggestion accuracy;
- review-required burden;
- no category-driven product merge/link authority.

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
- CP24 resolver authority remains frozen; category cannot widen or override it.
- CP25 category remains browse/classification metadata, never identity authority.
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

**CP24 is COMPLETE. CP25 — Category System is the next planned checkpoint and must not start without explicit user authorization.**
