# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, browse/search it, inspect personal historical prices, and judge whether the current personal purchase price is cheap/normal/expensive without fake normalization.

Every checkpoint requires explicit authorization and closes with exact evidence plus handoff synchronization.

## 1. Completed product/storage stages

### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE
Personal purchase-price memory and comparison is the frozen product essence.

### CP21 — Catalog Domain V2 — COMPLETE
Stable-ID identity, STANDARD/NON_STANDARD boundary, structured product fields, raw purchase forms, category non-authority, contextual aliases and provenance/confidence separation.

### CP22 — Persistence V2 — COMPLETE
Product schema 2; receipt schema 1; legacy IDs/links preserved; no duplicate price truth.

### CP23 — Receipt Product Semantics — COMPLETE
Conservative semantic evidence; ambiguity stays review-gated.

### CP24 — Identity Resolver V2 — COMPLETE
Confirmed alias/strict semantic authority with false-merge and false-split controls.

### CP25 — Category System — COMPLETE
Bounded reusable classification metadata; category never becomes identity authority.

### CP26 — Commodity / Non-standard V2 — COMPLETE
Heterogeneous purchase forms can share commodity identity while grouping remains distinct from comparability.

## 2. Stage D — Price intelligence

### CP27 — Price Intelligence V2 — COMPLETE
Frozen implementation `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`; Actions `38831623548` SUCCESS.

- comparison price is receipt-traceable numerator/denominator evidence;
- STANDARD one-package basis;
- kg/L/each strict normalized commodity cohorts;
- package/form cohorts contextual only;
- unsafe discounts/invalid receipts/conflicts excluded;
- deterministic latest/previous/delta/min/max/mean/median and scope filters.

### CP28 — Price Evaluation — COMPLETE
Frozen implementation `dd4f98613677ae998932d77f3e5f89d7bddba107`; Actions `38834818192` SUCCESS.

Frozen policy:

- latest observation excluded from baseline;
- minimum prior observations = 3;
- recent prior window = 5;
- usual price = median;
- material threshold = >=5% AND >=100 minor units;
- extreme threshold = >=15% AND >=500 minor units;
- labels = VERY_CHEAP / CHEAP / TYPICAL / EXPENSIVE / VERY_EXPENSIVE;
- no-judgment states = INSUFFICIENT_HISTORY / CONTEXTUAL_ONLY / NON_POSITIVE_BASELINE;
- contextual LIKE_FORM never receives cheap/expensive judgment;
- previous-price change and usual-price judgment remain separate;
- every result exposes baseline/reason/threshold evidence;
- no external market price or generative-AI opinion.

Local metric:

`cases=12 evaluated=9 insufficient=1 contextual=1 nonpositive=1 typical=2 cheap=2 very_cheap=1 expensive=2 very_expensive=2 latest_excluded=1 recent_five_window=1 deterministic_repeat=1`

## 3. Stage E — Find and inspect

### CP29 — Search / Browse — NEXT PLANNED

Goal: make accumulated product/commodity/history/evaluation knowledge practically findable before final visual polish.

Must define:

- searchable stable product/commodity fields;
- product name / brand / variant / specification queries;
- confirmed safe alias discovery;
- category browse;
- store context;
- recent and frequent purchase views;
- price-change/judgment browse facts derived from CP27/28;
- deterministic ranking and no-result states;
- fuzzy discovery as suggestion only, never identity-merge authority;
- query-performance evidence suitable for later CP36 hardening.

Do not redesign commercial UI here.

## 4. Stage F — Commercial UX

### CP30 — Design System Foundation
Freeze typography, color, spacing, shapes, icons, cards, fields, chart grammar, feedback states and accessibility baseline.

### CP31 — Product Detail
Commercial STANDARD price-memory screen with latest/previous/usual price, judgment, graph, store/history and receipt traceability.

### CP32 — Commodity Detail
Commercial NON_STANDARD history separating strict normalized and contextual same-form cohorts.

### CP33 — Capture / Review UX V2
Move toward `영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장` and reduce repeat-use review burden.

### CP34 — Commercial UI Shell
Product-centric home/navigation/search/category/product/commodity/receipt/settings integration without gratuitous domain rewrite.

## 5. Stage G — Validation and hardening

### CP35 — Real Receipt Evaluation
Measure end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures. Primary metric is correct purchase registration, not OCR character accuracy alone.

### CP36 — Performance / Reliability
Verify startup, OCR latency/memory, large catalog/history, search/category queries, CP27/28 aggregation, charts, migrations, archive reconciliation and failure recovery at representative scale.

## 6. Dependency gates

- CP21 stable-ID identity semantics remain frozen.
- CP22 product schema 2 / receipt schema 1 remain frozen unless a later checkpoint proves migration necessary.
- CP23 parser evidence remains unconfirmed/non-authoritative.
- CP24 resolver authority remains frozen; category/price/search cannot widen identity authority.
- CP25 category remains browse metadata only.
- CP26 commodity grouping remains distinct from comparability.
- CP27 eligible comparison cohort is the only input basis for CP28 judgment.
- CP28 judgment is personal-history policy, not identity or market-price truth.
- CP29 search may discover candidates but must not silently merge identities.
- CP30 Design System precedes final CP31/CP32 visual implementation.
- CP33 must not bypass identity/provenance rules for convenience.

## 7. Every checkpoint asks, only where materially relevant

- Does this change stored-data meaning?
- Can it create false merge/grouping or false split?
- Does repeat confirmation reduce review burden?
- Is raw receipt/purchase evidence preserved?
- Is every compared price exactly defined and receipt-traceable?
- Can incomparable prices look comparable?
- Can discounts be falsely allocated?
- Can a price judgment overstate sparse/contextual evidence?
- Can identity/provenance be bypassed?
- Can privacy/permissions/network posture change?
- Can a new performance hot path appear?
- Which local regression catches failure now?

Avoid ritual re-audits, speculative abstractions, unrelated cleanup and expansion into budgeting/banking/cloud/e-commerce before the core loop is complete.

## 8. Handoff discipline

At every completed group:

1. freeze exact implementation/spec HEAD;
2. record CI/artifact/evidence;
3. record limitations and meaningful failures/process anomalies;
4. update status/handoff/readme/work-unit/roadmap docs;
5. verify post-boundary changes are documentation-only;
6. stop before the next unauthorized checkpoint.

## 9. Current boundary

**CP28 is COMPLETE. CP29 — Search / Browse is the next planned checkpoint and must not start without explicit user authorization.**
