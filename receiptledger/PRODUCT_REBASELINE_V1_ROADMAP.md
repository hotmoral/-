# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`

## 0. Roadmap purpose

This roadmap turns the product rebaseline into bounded, dependency-aware work units. It is not permission to execute all checkpoints automatically. Each checkpoint requires explicit user authorization and must close with status/handoff synchronization.

## 1. Governing objective

Complete the smallest coherent product that lets a user:

1. add a receipt with minimal manual work;
2. obtain trustworthy product/item identities and purchase prices;
3. find a repeat purchase later;
4. see its personal historical prices;
5. judge whether a current price is cheap, normal, or expensive relative to that history;
6. do the equivalent for non-standard goods without fake unit normalization.

Everything else is secondary.

## 2. Roadmap stages

### Stage A — Rebaseline and contracts

#### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE

Artifacts:

- `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
- `PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
- `PRODUCT_REBASELINE_V1_ROADMAP.md`

No production implementation changes.

#### CP21 — Catalog Domain V2

Goal: freeze exact domain contracts before schema code.

Must define:

- Product vs Commodity boundaries
- Brand
- Product specification / variant / pack structure
- SalesUnit / raw purchase form
- Category references
- AliasContext (merchant/global)
- PurchaseObservation logical contract
- provenance/confidence/confirmation states
- legacy ProductType compatibility
- equality/identity rules
- serialization/test vectors as appropriate

Acceptance emphasis: domain-level contradictions found before persistence work.

### Stage B — Storage and migration

#### CP22 — Persistence V2

Goal: migration-safe storage for CP21.

Must include:

- legacy schema inventory
- schema version plan
- old-product/link preservation
- merchant alias context
- categories/sales forms/specification storage
- indexes for alias/search/history
- fail-closed migration
- migration regression fixtures
- direct SQLite vs Room decision with evidence, not preference

Non-goal: new commercial UI.

### Stage C — Receipt-to-product understanding

#### CP23 — Receipt Product Semantics

Goal: turn raw receipt item text into structured candidates without inventing identity.

Outputs may include:

- brand candidate
- product/family candidate
- variant candidate
- quantity/specification candidate
- unit candidate
- pack-count candidate
- confidence/reason/provenance

Must preserve raw text.

#### CP24 — Identity Resolver V2

Goal: resolve observations safely and reduce repeated user work.

Priority evidence:

- confirmed merchant alias
- safe confirmed global alias
- compatible exact structured match
- semantic/fuzzy suggestions
- unresolved

Fuzzy/semantic evidence is suggestion-oriented unless separately proven safe for automatic authority.

#### CP25 — Category System

Goal: make products/items browseable without making category a product-identity shortcut.

Includes taxonomy contract, persistence, assignment, correction, reuse, suggestion quality tests.

#### CP26 — Commodity / Non-standard V2

Goal: make non-standard goods first-class.

Includes mixed raw units/forms under one commodity, filters, like-unit comparison, no guessed conversion.

### Stage D — Price intelligence

#### CP27 — Price Intelligence V2

Goal: produce one canonical comparable-observation layer and deterministic metrics.

STANDARD target metrics:

- latest / previous
- absolute/percent delta
- min / max
- recent mean / median
- period mean / median
- store-specific views
- observation count/date range

NON_STANDARD:

- raw mixed-form history
- like-unit subsets
- optional normalized comparison only when explicit evidence supports it

#### CP28 — Price Evaluation

Goal: convert statistics into an understandable judgment without false confidence.

Must define:

- minimum observation counts
- time-window behavior
- outlier policy if any
- thresholds for cheap/normal/expensive labels
- exact explanation string/data payload
- `데이터 부족` behavior

### Stage E — Find and inspect

#### CP29 — Search / Browse

Goal: product/item retrieval at realistic history size.

Search dimensions:

- product/commodity name
- brand
- aliases where safe
- category
- specification
- store

Browse:

- category
- recent
- frequent
- recent price change

#### CP30 — Product Detail

Goal: STANDARD product price-memory screen.

Includes price summary, graph, store context, chronological observations, source receipt links.

#### CP31 — Commodity Detail

Goal: NON_STANDARD mixed-form history without misleading aggregate comparison.

### Stage F — Intake UX and visual product quality

#### CP32 — Capture / Review UX V2

Goal: replace manual debug sequence with automatic processing + uncertainty-focused review.

Target interaction:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

Preserve debug/evidence access until replacement is proven.

#### CP33 — Design System

Goal: commercial-quality visual foundation.

Includes typography, colors, spacing, shapes, elevation, iconography, buttons, cards, list rows, fields, charts, loading/error/empty/success states, accessibility baselines.

#### CP34 — Commercial UI Shell

Goal: integrate product-centric home/navigation/search/category/product/commodity/receipt/settings into a coherent application.

No gratuitous domain rewrite.

### Stage G — Validation and hardening

#### CP35 — Real Receipt Evaluation

Goal: measure end-to-end registration correctness using public-safe/synthetic or explicitly approved sanitized fixtures.

Primary metric is not OCR character accuracy alone. Measure:

- correct receipt merchant/date
- correct item boundary
- correct amount/quantity
- correct product/commodity resolution
- correct category
- correct price-history eligibility
- number of user interventions required

#### CP36 — Performance / Reliability

Goal: verify realistic scale and failure recovery.

Areas:

- startup
- OCR latency and memory
- large receipt/catalog DB
- alias/search latency
- price-history aggregation
- chart loading
- migration
- image archive reconciliation
- interrupted operations/crash recovery

## 3. Cross-stage rules

### Every checkpoint must ask

- Does this change the meaning of previously stored data?
- Can this create a false product merge?
- Can this make incomparable prices look comparable?
- Can this bypass validation/provenance?
- Can this require a new permission/network capability?
- Can this degrade repeated-use automation?
- Can this create a new performance hot path?
- What existing regression test would detect breakage?

Only questions relevant to the actual scope need deep analysis.

### Every checkpoint must avoid

- unrelated architecture cleanup;
- speculative future abstractions without an immediate contract need;
- UI work that forces domain rewrites;
- database migration before the model is frozen;
- repeated revalidation of unrelated proven checkpoints;
- expanding into budgeting/banking/cloud/e-commerce before the core loop works.

## 4. Handoff discipline

At the end of every completed group:

1. freeze implementation/spec boundary with exact HEAD;
2. record CI/evidence where the group has executable changes;
3. document known non-blocking limitations and superseded failures;
4. update `PROJECT_STATUS_LATEST.md`;
5. update `SESSION_HANDOFF.md`;
6. update `README.md`;
7. update `WORK_UNIT.md`;
8. update the active checkpoint document(s);
9. verify post-boundary handoff changes are documentation-only when applicable;
10. stop before the next group unless explicitly authorized.

## 5. Current boundary

CP20 is the current completed planning boundary.

The next planned checkpoint is **CP21 — Catalog Domain V2**.

Planning existence does not equal execution authorization. Do not start CP21 until the user explicitly directs the next group to proceed.
