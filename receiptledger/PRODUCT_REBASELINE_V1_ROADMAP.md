# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, inspect personal historical prices, and judge whether a current price is cheap/normal/expensive without fake normalization of non-standard goods.

Each checkpoint requires explicit user authorization and closes with exact evidence plus handoff synchronization.

## 1. Completed contract stages

### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE

Frozen product essence: personal purchase-price memory and comparison.

### CP21 — Catalog Domain V2 — COMPLETE

Frozen implementation HEAD:
`8596106c370e172161ef00e8d460dc78667bf80d`

Canonical Actions:
`38808985222` — SUCCESS

CP21 froze:

- Product vs Commodity boundary;
- legacy ProductType compatibility;
- stable-ID identity/equality rule;
- Brand/Product/Variant/Specification field contract;
- exact physical package-measure semantics;
- raw SalesUnit/PurchaseForm semantics;
- CategoryRef non-authority;
- global/merchant AliasContext;
- independent source/confidence/confirmation;
- logical PurchaseObservation contract;
- fail-closed legacy adaptation.

Persistence schema remains V1 and migration has not started.

## 2. Stage B — Storage and migration

### CP22 — Persistence V2 — NEXT PLANNED

Goal: migration-safe storage for CP21 semantics.

Must include:

- exact legacy schema/data inventory;
- schema version/migration plan;
- product ID and item-link preservation;
- no semantic guessing from legacy canonical names;
- merchant alias context storage;
- specification/category/purchase-form representation;
- indexes needed for later identity/search/history;
- separate-DB sequencing and fail-closed behavior;
- deterministic migration regression fixtures;
- direct SQLite vs Room decision based on concrete evidence.

Non-goals: semantic parsing, resolver V2, price judgment, commercial UI.

## 3. Stage C — Receipt-to-product understanding

### CP23 — Receipt Product Semantics

Parse brand/product/variant/specification/pack/sales-unit candidates from raw receipt item text with confidence/reason/provenance and without inventing identity.

### CP24 — Identity Resolver V2

Merchant-aware aliases, deterministic candidate ranking, safe auto-link authority, ambiguous review and confirmed-decision reuse. Fuzzy/semantic similarity remains suggestion evidence unless separately proven safe.

### CP25 — Category System

Taxonomy, persistence, assignment, suggestion, user correction and reuse. Category must never become a shortcut for product identity.

### CP26 — Commodity / Non-standard V2

Make mixed raw forms such as 봉/팩/kg/개/상자 first-class while preserving grouping != comparability and prohibiting guessed conversion.

## 4. Stage D — Price intelligence

### CP27 — Price Intelligence V2

Define one canonical comparable-observation layer and deterministic metrics: latest/previous, deltas, min/max, means/medians, period and store-aware views, plus like-unit NON_STANDARD subsets.

### CP28 — Price Evaluation

Define explicit data-sufficiency, time-window and threshold rules for cheap/normal/expensive labels. Sparse data yields `데이터 부족`.

## 5. Stage E — Find and inspect

### CP29 — Search / Browse

Global search and browse by product/commodity, brand, safe aliases, category, specification, store, recent/frequent and price change.

### CP30 — Product Detail

Commercial STANDARD product price-memory screen with historical graph, store context and source receipt traceability.

### CP31 — Commodity Detail

Commercial NON_STANDARD mixed-form history screen without misleading aggregate comparison.

## 6. Stage F — Intake UX and visual product quality

### CP32 — Capture / Review UX V2

Move from manual debug sequence toward:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

Retain debug/evidence paths until replacement parity is proven.

### CP33 — Design System

Typography, colors, spacing, shapes, iconography, cards, fields, charts, feedback states and accessibility baseline.

### CP34 — Commercial UI Shell

Product-centric home/navigation/search/category/product/commodity/receipt/settings integration without gratuitous domain rewrite.

## 7. Stage G — Validation and hardening

### CP35 — Real Receipt Evaluation

Measure end-to-end registration correctness using public-safe synthetic or explicitly approved sanitized fixtures. Primary metric is correct purchase registration, not OCR character accuracy alone.

### CP36 — Performance / Reliability

Verify startup, OCR memory/latency, large catalog/history, alias/search queries, aggregation, charts, migration, archive reconciliation and failure recovery at representative scale.

## 8. Dependency gates

- CP21 Domain V2 must remain frozen before CP22 persistence semantics are implemented.
- CP22 must precede production consumers of new stored fields.
- CP23 semantic parsing precedes CP24 resolver authority.
- CP27 statistics precede CP28 price judgment.
- CP29 data access precedes CP34 shell dependencies.
- CP25 and CP26 may partially overlap only after shared CP21/22 contracts are stable.
- CP33 must not force domain/storage rewrites.

## 9. Every checkpoint must ask, only where materially relevant

- Does this change the meaning of stored data?
- Can it create a false product merge?
- Can it make incomparable prices look comparable?
- Can it bypass provenance/validation?
- Can it require new permission/network capability?
- Can it degrade repeat-use automation?
- Can it create a new performance hot path?
- Which regression/evidence catches failure?

Avoid ritual re-audits of unrelated proven work, speculative abstractions, unrelated architecture cleanup, and scope expansion into budgeting/banking/cloud/e-commerce before the core loop is complete.

## 10. Handoff discipline

At each completed group:

1. freeze exact implementation/spec HEAD;
2. record CI/artifact/evidence when executable changes exist;
3. record relevant limitations/superseded failures;
4. update `PROJECT_STATUS_LATEST.md`, `SESSION_HANDOFF.md`, `README.md`, `WORK_UNIT.md` and roadmap/checkpoint docs;
5. verify post-boundary handoff changes are documentation-only;
6. stop before the next unauthorized group.

## 11. Current boundary

CP21 is complete.

The next planned checkpoint is **CP22 — Persistence V2**.

Planning existence does not equal execution authorization. Do not start CP22 until the user explicitly directs it.
