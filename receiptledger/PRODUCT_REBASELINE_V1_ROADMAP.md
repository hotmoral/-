# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, inspect personal historical prices, and judge whether a current price is cheap/normal/expensive without fake normalization of non-standard goods.

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

- receipt-traceable numerator/denominator comparison price;
- STANDARD compares one exact stable package;
- kg/g -> price/kg, L/mL -> price/L, count -> price/each;
- package/form units contextual only;
- unsupported discount attribution excluded rather than guessed;
- deterministic latest/previous/min/max/mean/median and period/store scopes.

### CP28 — Price Evaluation — COMPLETE
Frozen implementation `dd4f98613677ae998932d77f3e5f89d7bddba107`; Actions `38834818192` SUCCESS.

- latest observation excluded from its own baseline;
- minimum 3 prior observations;
- recent maximum 5 prior observations;
- usual price = prior median;
- material change = >=5% AND >=100 minor units;
- extreme = >=15% AND >=500 minor units;
- contextual LIKE_FORM remains unjudged;
- every judgment exposes reason/baseline evidence;
- no market-price or free-form AI opinion.

## 3. Stage E — Find and inspect

### CP29 — Search / Browse — COMPLETE
Frozen implementation `b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`; Actions `38839041465` SUCCESS.

- read-only discovery over canonical stores;
- canonical/brand/product/variant/specification and observed linked receipt text searchable;
- exact/prefix/all-term/contains deterministic ranking;
- no fuzzy identity authority;
- category descendants and exact normalized store filtering;
- recent = latest purchase occasion;
- frequent = distinct receipt occasions;
- price-change = strict CP28 evaluated non-typical basis-specific rows;
- no mutable search index/table/FTS;
- scan diagnostics retained for CP36.

## 4. Stage F — Commercial UX

### CP30 — Design System Foundation — COMPLETE
Frozen implementation `ff0745db529499171246866039521a0b83e830e4`; canonical Actions `38842905325` SUCCESS.

Frozen contract:

- current programmatic `Activity + android.widget` architecture retained;
- no Compose/Material migration;
- typography roles: price hero/title/body/label;
- semantic tones: neutral/primary/positive/negative/review/error/info/disabled;
- color always paired with text meaning;
- spacing 4/8/12/16/24/32dp;
- radii 8/12/16dp;
- elevations 1/3dp;
- minimum interaction area 48dp;
- 10 stable icon roles with 24dp glyph token and Korean accessibility labels;
- width classes compact <600, medium 600–839, expanded >=840;
- chart series cannot mix CP27 comparison bases;
- loading/empty/no-result/review/insufficient/contextual/error/disabled state presentations;
- LibraryActivity and legacy PriceHistoryActivity are representative UiKit adopters only.

Canonical metric:

`CP30_METRICS typography_roles=6 semantic_tones=8 price_presentations=8 validation_presentations=4 ui_states=8 contrast_pairs=9 responsive_cases=5 chart_cross_basis_rejections=1 min_touch_dp=48 icon_roles=10 elevation_tokens=2 representative_activities=2`

Initial green implementation `5c63a537...` was not closed because plan/code review found icon semantics and elevation centralization incomplete. Those were corrected before the canonical CP30 boundary.

### CP31 — Product Detail — NEXT PLANNED

Goal: first full commercial STANDARD product price-memory detail surface.

Must consume frozen CP21–30 contracts and expose:

- stable identity/specification;
- latest/current price;
- previous price and delta;
- usual-price baseline and CP28 judgment/explanation;
- one-basis price-history chart;
- store/date context;
- receipt traceability;
- insufficient/no-judgment states;
- CP30 responsive/accessibility grammar.

Must not:

- infer/merge identity from UI/search similarity;
- mix price comparison bases;
- invent unsupported discount allocation;
- change CP28 thresholds;
- redesign commodity/capture/shell scope in the same checkpoint.

### CP32 — Commodity Detail
Commercial NON_STANDARD history that clearly separates strict normalized cohorts from contextual same-form observations.

### CP33 — Capture / Review UX V2
Move toward `영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`; acceptance includes review burden and repeat-use automation.

### CP34 — Commercial UI Shell
Product-centric home/navigation/search/category/product/commodity/receipt/settings integration without gratuitous domain rewrite.

## 5. Stage G — Validation and hardening

### CP35 — Real Receipt Evaluation
Measure end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures. Primary metric is correct purchase registration, not OCR character accuracy alone. Search/detail usability should also be exercised on representative accumulated histories.

### CP36 — Performance / Reliability
Verify startup, OCR latency/memory, large catalog/history, alias/search/category queries, CP27/28 aggregation, chart workloads, migrations, archive reconciliation and failure recovery at representative scale.

For CP29 specifically, benchmark canonical-store linear scan at approximately 1k/10k catalog/history scale before deciding whether FTS/index/cache is justified.

## 6. Dependency gates

- CP21 stable-ID identity semantics remain frozen.
- CP22 product schema 2 / receipt schema 1 remain frozen unless explicit migration need is proved.
- CP23 parser evidence remains unconfirmed/non-authoritative.
- CP24 resolver authority remains frozen; category/price/search/UI cannot widen identity authority.
- CP25 category remains browse/classification metadata only.
- CP26 commodity grouping remains distinct from comparability.
- CP27 eligible cohort is the only price input basis for CP28 judgment.
- CP28 judgment is deterministic/explainable and cannot be replaced by UI opinion.
- CP29 search is read-only; relevance never becomes merge/relink authority.
- CP29 price-change rows remain comparison-basis-specific.
- CP30 visual semantics must present, not reinterpret, CP21–29 facts.
- CP30 chart grammar forbids cross-basis visual lines.
- CP31/32 consume CP30 components/tokens rather than create parallel ad-hoc systems.
- CP33 must not bypass identity/provenance rules for convenience.

## 7. Every checkpoint asks, only where materially relevant

- Does this change stored-data meaning?
- Can it create false merge/grouping or false split?
- Does confirmed repeat use reduce review burden?
- Is raw receipt/purchase evidence preserved?
- Is every compared price exactly defined and receipt-traceable?
- Can incomparable prices look comparable?
- Can discounts be falsely allocated?
- Can search relevance be mistaken for identity evidence?
- Can UI styling accidentally imply a business judgment that does not exist?
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
4. compare plan/acceptance to actual implementation before closure, even if CI is green;
5. update status/handoff/readme/work-unit/roadmap docs;
6. verify post-boundary changes are documentation-only;
7. stop before the next unauthorized checkpoint.

## 9. Current boundary

**CP30 is COMPLETE. CP31 — Product Detail is the next planned checkpoint and must not start without explicit user authorization.**
