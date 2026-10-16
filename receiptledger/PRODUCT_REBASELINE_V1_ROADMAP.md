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
Frozen implementation `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`; Actions `38829423445` SUCCESS. Same commodity can group heterogeneous purchase forms while grouping remains distinct from comparability.

## 2. Stage D — Price intelligence — COMPLETE

### CP27 — Price Intelligence V2 — COMPLETE
Frozen implementation `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`; Actions `38831623548` SUCCESS.

- comparison price is receipt-traceable numerator/denominator evidence;
- STANDARD compares one exact stable package;
- kg/g -> price/kg, L/mL -> price/L, count -> price/each;
- package/form units remain contextual only;
- unsupported discount attribution is excluded rather than guessed;
- latest/previous/min/max/mean/median and period/store scopes are deterministic.

### CP28 — Price Evaluation — COMPLETE
Frozen implementation `dd4f98613677ae998932d77f3e5f89d7bddba107`; Actions `38834818192` SUCCESS.

- latest observation excluded from its own baseline;
- minimum 3 prior observations;
- recent maximum 5 prior observations;
- usual price = prior median;
- material change = >=5% AND >=100 minor units;
- extreme = >=15% AND >=500 minor units;
- contextual LIKE_FORM stays unjudged;
- every judgment exposes reason/baseline evidence;
- no market-price or free-form AI opinion.

## 3. Stage E — Find and inspect

### CP29 — Search / Browse — COMPLETE
Frozen implementation `b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`; Actions `38839041465` SUCCESS.

Frozen contract:

- read-only discovery over canonical stores;
- searchable canonical/brand/product/variant/specification fields;
- linked receipt item names usable as discovery text only;
- category path and store context searchable;
- exact/prefix/all-term/contains deterministic ranking;
- whitespace-compacted discovery allowed;
- no fuzzy identity authority;
- category parent includes descendants;
- store filter is exact normalized text;
- recent = latest purchase occasion;
- frequent = distinct receipt occasions;
- price-change = strict CP28 evaluated non-typical cohort rows only;
- one commodity may expose multiple independent basis rows;
- no mutable search index/table/FTS;
- scanned/matched diagnostics retained for CP36.

Local metric:

`CP29_METRICS documents=3 exact_hits=1 compact_hits=1 observed_hits=1 category_rows=3 store_rows=1 recent_rows=3 frequent_rows=3 no_result_rows=0 mutation_checks=1 diagnostics_scanned=3`

## 4. Stage F — Commercial UX

### CP30 — Design System Foundation — NEXT PLANNED

Goal: freeze a commercial-quality visual and interaction language **before** final user-facing detail/shell work.

Must define:

- Korean typography hierarchy and price/numeric roles;
- color tokens and semantic price/judgment/review/error states;
- spacing/grid and responsive rhythm;
- radius, elevation and surface hierarchy;
- icon grammar;
- buttons, fields, search bars, chips, list/card rows;
- price history and CP28 judgment presentation;
- chart grammar that preserves comparison-basis distinctions;
- loading/empty/error/review states;
- accessibility/touch-target/contrast baseline;
- responsive profiles for representative Android sizes.

CP30 should establish reusable components/tokens and limited visual proofs. It must not rewrite CP21–29 domain/search semantics for convenience.

### CP31 — Product Detail
Commercial STANDARD price-memory screen with identity/specification, latest/previous/usual price, graph, store context, CP28 explanation and receipt traceability.

### CP32 — Commodity Detail
Commercial NON_STANDARD history that clearly separates strict normalized cohorts from contextual same-form observations.

### CP33 — Capture / Review UX V2
Move toward `영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`; acceptance includes review burden and repeat-use automation.

### CP34 — Commercial UI Shell
Product-centric home/navigation/search/category/product/commodity/receipt/settings integration without gratuitous domain rewrite.

## 5. Stage G — Validation and hardening

### CP35 — Real Receipt Evaluation
Measure end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures. Primary metric is correct purchase registration, not OCR character accuracy alone. Search/discovery usability should also be exercised on representative accumulated histories.

### CP36 — Performance / Reliability
Verify startup, OCR latency/memory, large catalog/history, alias/search/category queries, CP27/28 aggregation, chart workloads, migrations, archive reconciliation and failure recovery at representative scale.

For CP29 specifically, benchmark the current canonical-store linear scan at approximately 1k/10k catalog/history scale before deciding whether FTS/index/cache is justified.

## 6. Dependency gates

- CP21 stable-ID identity semantics remain frozen.
- CP22 product schema 2 / receipt schema 1 remain frozen unless a later checkpoint proves an explicit migration necessary.
- CP23 parser evidence remains unconfirmed/non-authoritative.
- CP24 resolver authority remains frozen; category/price/search cannot widen identity authority.
- CP25 category remains browse/classification metadata only.
- CP26 commodity grouping remains distinct from comparability.
- CP27 eligible comparison cohort is the only input basis for CP28 judgment.
- CP28 judgment is deterministic/explainable and must not be replaced by UI opinion.
- CP29 search is read-only; discovery relevance must never become merge/relink authority.
- CP29 price-change rows remain comparison-basis-specific.
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
- Can search relevance be mistaken for identity evidence?
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

**CP29 is COMPLETE. CP30 — Design System Foundation is the next planned checkpoint and must not start without explicit user authorization.**
