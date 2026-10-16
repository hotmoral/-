# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, browse/search it, inspect personal historical prices, and judge whether a current price is cheap/normal/expensive without fake normalization of non-standard goods.

Every checkpoint requires explicit user authorization and closes with exact evidence plus handoff synchronization.

## 1. Completed product/storage stages

### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE
Personal purchase-price memory and comparison is the frozen product essence.

### CP21 — Catalog Domain V2 — COMPLETE
Stable-ID identity, STANDARD/NON_STANDARD boundary, structured product fields, exact physical measures, raw purchase forms, category non-authority, contextual aliases and source/confidence/confirmation separation.

### CP22 — Persistence V2 — COMPLETE
Frozen implementation `449896c7580fb3412f41c9b58d1ab9412d13d84d`; Actions `38816200340` SUCCESS. Product schema 2; receipt schema 1; legacy IDs/links preserved; direct SQLite retained.

### CP23 — Receipt Product Semantics — COMPLETE
Frozen implementation `5bffb66bd43814f8d638791b5697f79ff089028b`; Actions `38822100885` SUCCESS. Conservative unconfirmed semantic evidence; ambiguity stays review-gated.

### CP24 — Identity Resolver V2 — COMPLETE
Frozen implementation `4b556afd4dd52b68cf768e937bb456665ad4c231`; Actions `38824134990` SUCCESS. MERCHANT alias -> GLOBAL alias -> strict semantic exact -> review/unresolved; false merge and false split both measured.

### CP25 — Category System — COMPLETE
Frozen implementation `042c3b59063f0e58a273a5f685b25780683fcf36`; Actions `38827880730` SUCCESS. Bounded taxonomy and reusable classification metadata; category never becomes identity authority.

### CP26 — Commodity / Non-standard V2 — COMPLETE
Frozen implementation `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`; Actions `38829423445` SUCCESS.

- same commodity can group heterogeneous purchase forms;
- purchase quantity/unit/raw form is preserved;
- exact quantity basis is separate from same-form-only history;
- grouping != comparability;
- no guessed package conversion;
- false grouping 0 in bounded local fixture; visible false split retained.

## 2. Stage D — Price intelligence

### CP27 — Price Intelligence V2 — COMPLETE
Frozen implementation `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`; Actions `38831623548` SUCCESS.

Frozen contract:

- comparison price is a receipt-traceable numerator/denominator ratio;
- STANDARD compares one exact stable package;
- kg/g -> price/kg, L/mL -> price/L, count -> price/each;
- package/form units remain contextual same-form cohorts only;
- sole-item receipt discount may be attributed exactly;
- multi-item unallocated discount stays visible but excluded from aggregates;
- invalid receipts and contradictory item arithmetic are excluded, not repaired;
- latest/previous/delta/delta-percent/min/max/mean/median are deterministic per cohort;
- period/store filtering supported;
- legacy price core, product schema 2 and receipt schema 1 remain unchanged;
- price judgment is deferred.

Local metric:

`observations=10 eligible=7 excluded_discount=1 excluded_invalid=1 missing_form=1 standard_cohorts=1 commodity_strict_cohorts=1 commodity_contextual_cohorts=1 scope_checks=2 receipt_traceable_rates=7`

### CP28 — Price Evaluation — NEXT PLANNED

Goal: turn CP27 facts into deterministic and explainable user-facing price judgments without pretending sparse or incomparable data is stronger than it is.

Must define before implementation:

- minimum observation count / data sufficiency;
- which historical window becomes the baseline;
- robust usual-price statistic, likely median-centered rather than fragile single-value intuition;
- explicit percentage/absolute thresholds for cheap / normal / expensive bands;
- treatment of latest vs immediately previous price separately from baseline judgment;
- zero/near-zero baseline behavior;
- handling of contextual LIKE_FORM cohorts and weaker evidence labeling;
- transparent output containing baseline, sample count, delta and reason;
- no free-form AI opinion;
- no cross-cohort mixing.

## 3. Stage E — Find and inspect

### CP29 — Search / Browse

Global search/browse by product/commodity, brand, safe aliases, category, specification, store, recent/frequent and price change. Freeze data-access and interaction behavior before final visual polish.

## 4. Stage F — Commercial UX

### CP30 — Design System Foundation
Freeze typography, color, spacing, shapes, icons, cards, fields, chart grammar, feedback states and accessibility baseline.

### CP31 — Product Detail
Commercial STANDARD price-memory screen with graph, latest/previous/usual price, store context, CP27/28 explanation and receipt traceability.

### CP32 — Commodity Detail
Commercial NON_STANDARD mixed-form history, clearly separating strict normalized and contextual same-form cohorts.

### CP33 — Capture / Review UX V2
Move toward `영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`; acceptance includes review burden and repeat-use automation.

### CP34 — Commercial UI Shell
Product-centric home/navigation/search/category/product/commodity/receipt/settings integration without gratuitous domain rewrite.

## 5. Stage G — Validation and hardening

### CP35 — Real Receipt Evaluation
Measure end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures. Primary metric is correct purchase registration, not OCR character accuracy alone.

### CP36 — Performance / Reliability
Verify startup, OCR latency/memory, large catalog/history, alias/search/category queries, CP27/28 aggregation, charts, migrations, archive reconciliation and failure recovery at representative scale.

## 6. Dependency gates

- CP21 stable-ID identity semantics remain frozen.
- CP22 product schema 2 / receipt schema 1 remain frozen unless a later checkpoint proves an explicit migration is necessary.
- CP23 parser evidence remains unconfirmed/non-authoritative.
- CP24 resolver authority remains frozen; category/price cannot widen identity authority.
- CP25 category remains browse/classification metadata only.
- CP26 commodity grouping remains distinct from comparability.
- CP27 eligible comparison cohort is the only input basis for CP28 judgment.
- CP28 must expose deterministic data-sufficiency and threshold reasons before UI consumption.
- CP29 data access precedes commercial-shell dependencies.
- CP30 Design System precedes final CP31/CP32 visual implementation.
- CP33 must not bypass identity/provenance rules for convenience.

## 7. Every checkpoint asks, only where materially relevant

- Does this change stored-data meaning?
- Can it create a false merge/grouping or false split?
- Does confirmed repeat use reduce review burden?
- Is raw receipt/purchase evidence preserved?
- Is every compared price exactly defined and receipt-traceable?
- Can incomparable prices look comparable?
- Can discounts be falsely allocated?
- Can provenance/validation be bypassed?
- Can permissions/network/privacy posture change?
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

**CP27 is COMPLETE. CP28 — Price Evaluation is the next planned checkpoint and must not start without explicit user authorization.**
