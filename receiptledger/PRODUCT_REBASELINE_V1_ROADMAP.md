# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, inspect personal historical prices, and judge whether a current price is cheap/normal/expensive without fake normalization of non-standard goods.

Every checkpoint requires explicit user authorization and closes with exact evidence plus handoff synchronization.

## 1. Completed contract stages

### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE

Frozen product essence: personal purchase-price memory and comparison.

### CP21 — Catalog Domain V2 — COMPLETE

Frozen implementation HEAD:
`8596106c370e172161ef00e8d460dc78667bf80d`

Canonical Actions:
`38808985222` — SUCCESS

CP21 froze Product/Commodity boundary, stable-ID identity, structured STANDARD fields, exact physical package measures, raw purchase forms, CategoryRef non-authority, global/merchant AliasContext, source/confidence/confirmation separation, logical PurchaseObservation, and fail-closed legacy adaptation.

### CP22 — Persistence V2 — COMPLETE

Frozen implementation HEAD:
`449896c7580fb3412f41c9b58d1ab9412d13d84d`

Canonical Actions:
`38816200340` — SUCCESS

CP22 froze/implemented:

- product DB V1 -> V2 migration while preserving DB filename;
- legacy product IDs and item links unchanged;
- legacy aliases -> GLOBAL contextual aliases;
- merchant-scoped alias persistence;
- catalog semantic field evidence persistence;
- exact product specification persistence;
- stable category-reference persistence;
- linked PurchaseForm semantic persistence without duplicate price truth;
- receipt DB remains schema V1 and authoritative for price/date/store/validation;
- direct SQLite retained; Room deferred based on scope/risk evidence;
- deterministic real-SQLite migration verification.

Migration vectors: 15/15 PASS. Persistence V2 focused tests: 7/7 PASS. Lint: 0/0.

## 2. Stage C — Receipt-to-product understanding

### CP23 — Receipt Product Semantics — NEXT PLANNED

Parse brand/product/variant/specification/pack/sales-unit candidates from raw receipt item text with confidence/reason/provenance and without inventing identity.

Local quality evidence must include materially relevant parsing accuracy/coverage and review-required rate. Do not defer all semantic quality measurement to CP35.

Storage target is the CP22 V2 catalog metadata contract. Parser output must not mutate stable IDs or gain product-merge authority.

### CP24 — Identity Resolver V2

Merchant-aware aliases, deterministic candidate ranking, safe auto-link authority, ambiguous review and confirmed-decision reuse.

Mandatory quality metrics:

- false merge rate;
- false split / identity-fragmentation rate;
- automatic link success rate;
- ambiguous/review-required rate;
- incorrect automatic decision rate;
- repeat-purchase reuse rate after prior confirmation.

False merge remains the stricter safety failure, but false split may not be ignored.

Fuzzy/semantic similarity remains suggestion evidence unless separately proven safe.

### CP25 — Category System

Taxonomy, persistence, assignment, suggestion, user correction and reuse. Category must never become a shortcut for product identity.

Measure category suggestion accuracy and review burden locally.

### CP26 — Commodity / Non-standard V2

Make mixed raw forms such as 봉/팩/kg/개/상자 first-class while preserving grouping != comparability and prohibiting guessed conversion.

Measure commodity grouping correctness, false grouping/splitting, raw-unit preservation and review burden locally.

## 3. Stage D — Price intelligence

### CP27 — Price Intelligence V2

Define one canonical comparable-observation layer and deterministic metrics: latest/previous, deltas, min/max, means/medians, period and store-aware views, plus like-unit NON_STANDARD subsets.

Before statistics, CP27 must define the **canonical comparison price** for an observation.

At minimum the contract must cover:

- line amount vs one purchased unit/package;
- quantity > 1;
- item-specific discounts;
- receipt-level coupons/discounts with unprovable allocation;
- printed/inferred/user-edited price provenance;
- invalid/incomplete observations;
- same-product package identity;
- like-unit NON_STANDARD comparability.

Default principle: compare the price actually attributable to one purchased unit/package of the same catalog identity when evidence supports it. Do not arbitrarily distribute unallocated receipt-level discounts.

### CP28 — Price Evaluation

Define explicit data-sufficiency, time-window and threshold rules for cheap/normal/expensive labels. Sparse data yields `데이터 부족`.

## 4. Stage E — Find and inspect

### CP29 — Search / Browse

Global search and browse by product/commodity, brand, safe aliases, category, specification, store, recent/frequent and price change.

This checkpoint freezes data access and interaction behavior; it does not need final commercial visual polish.

## 5. Stage F — Commercial UX foundation and screens

### CP30 — Design System Foundation

Freeze typography, colors, spacing, shapes, iconography, cards, fields, chart grammar, feedback states and accessibility baseline **before final detail-screen visual implementation**.

Design System must not force domain/storage rewrites.

### CP31 — Product Detail

Commercial STANDARD product price-memory screen with historical graph, store context, comparison-price explanation and source receipt traceability.

### CP32 — Commodity Detail

Commercial NON_STANDARD mixed-form history screen without misleading aggregate comparison.

### CP33 — Capture / Review UX V2

Move from manual debug sequence toward:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

Retain debug/evidence paths until replacement parity is proven.

Acceptance must include review burden and repeat-use automation behavior, not only visual completion.

### CP34 — Commercial UI Shell

Product-centric home/navigation/search/category/product/commodity/receipt/settings integration without gratuitous domain rewrite.

## 6. Stage G — Validation and hardening

### CP35 — Real Receipt Evaluation

Measure end-to-end purchase-registration correctness using public-safe synthetic or explicitly approved sanitized fixtures.

Primary metric is correct purchase registration, not OCR character accuracy alone.

CP35 aggregates earlier local metrics; it is not the first point where false split, auto-link, category or commodity quality is measured.

### CP36 — Performance / Reliability

Verify startup, OCR memory/latency, large catalog/history, alias/search queries, aggregation, charts, migration, archive reconciliation and failure recovery at representative scale.

## 7. Dependency gates

- CP21 domain meanings and CP22 persistence semantics remain frozen before production semantic consumers expand.
- CP23 semantic parsing precedes CP24 resolver authority.
- CP23 must write only evidence-backed candidate semantics into the CP22 storage shape and must not reinterpret legacy migration gaps.
- CP24 must measure both false merge and false split and prove repeat-use automation behavior.
- CP27 canonical comparison-price semantics precede CP28 price judgment.
- CP29 data access precedes commercial shell dependencies.
- CP30 Design System Foundation precedes final CP31/CP32 commercial visual implementation.
- CP25 and CP26 may partially overlap only after shared CP21/22 contracts are stable.
- CP33 must not bypass identity/provenance rules for convenience.

## 8. Every checkpoint must ask, only where materially relevant

- Does this change the meaning of stored data?
- Can it create a false product merge?
- Can it create or perpetuate a false product split?
- Does confirmed repeat use reduce review burden?
- Is any compared price exactly defined and receipt-traceable?
- Can incomparable prices look comparable?
- Can it bypass provenance/validation?
- Can it require new permission/network capability?
- Can it create a new performance hot path?
- Which local regression/evidence catches failure now?

Avoid ritual re-audits of unrelated proven work, speculative abstractions, unrelated architecture cleanup, and scope expansion into budgeting/banking/cloud/e-commerce before the core loop is complete.

## 9. Handoff discipline

At each completed group:

1. freeze exact implementation/spec HEAD;
2. record CI/artifact/evidence when executable changes exist;
3. record relevant limitations/superseded failures;
4. update `PROJECT_STATUS_LATEST.md`, `SESSION_HANDOFF.md`, `README.md`, `WORK_UNIT.md` and roadmap/checkpoint docs;
5. verify post-boundary handoff changes are documentation-only;
6. stop before the next unauthorized group.

## 10. Current boundary

CP22 — Persistence V2 is complete.

The next planned implementation checkpoint is **CP23 — Receipt Product Semantics**.

Planning existence does not equal execution authorization. Do not start CP23 until the user explicitly directs it.
