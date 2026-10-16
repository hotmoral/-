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
Frozen implementation `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`; Actions `38829423445` SUCCESS. Same commodity may group heterogeneous purchase forms while grouping remains distinct from comparability.

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
- recent/frequent/price-change browsing;
- no mutable search index/table/FTS;
- scan diagnostics retained for CP36.

## 4. Stage F — Commercial UX

### CP30 — Design System Foundation — COMPLETE
Frozen implementation `ff0745db529499171246866039521a0b83e830e4`; canonical Actions `38842905325` SUCCESS.

Frozen contract:

- programmatic `Activity + android.widget` retained;
- no Compose/Material migration;
- purpose-based typography roles and Korean-first hierarchy;
- semantic tones always paired with text meaning;
- spacing 4/8/12/16/24/32dp;
- radii 8/12/16dp;
- elevations 1/3dp;
- minimum interaction area 48dp;
- compact/medium/expanded width classes at 600/840dp;
- chart series cannot mix CP27 comparison bases;
- reusable loading/empty/review/error/unavailable state presentations.

### CP31 — Product Detail — COMPLETE
Frozen implementation `1d2e7ef67e949af9098027a78e30551c228c255c`; canonical Actions `38852423981` SUCCESS.

Commercial direction: **quiet confidence / price-first / evidence-backed**.

Delivered STANDARD product detail:

- canonical identity/specification;
- latest/previous/usual kept distinct;
- frozen CP28 judgment/explanation;
- STANDARD_PACKAGE-only actual-purchase chart;
- store/date/receipt traceability;
- insufficient/no-judgment states;
- CP30 responsive/accessibility grammar;
- no domain/schema/search/price-policy rewrite.

Canonical metric:

`CP31_METRICS product_detail_version=1 standard_basis=1 identity_fallbacks=1 price_states=8 responsive_cases=6 traceability=1 chart_single_basis=1 purchase_rows=4`

### CP32 — Commodity Detail — COMPLETE
Frozen implementation `e42629ccd66a80a4a1a14de0c7798b178d6b0062`; canonical Actions `38855942283` SUCCESS.

Commercial direction remains CP31's **quiet confidence / price-first / evidence-backed**, with **clarity before apparent simplicity** for NON_STANDARD cases.

Delivered:

- read-only NON_STANDARD Commodity Detail projection;
- real newest purchase preserved independently of comparability;
- separate WEIGHT_KG / VOLUME_L / EACH sections;
- per-strict-basis latest/previous/usual/CP28 judgment;
- one strict basis per chart;
- independent LIKE_FORM groups for package forms;
- contextual package forms explicitly reference-only, unjudged and chartless;
- no fake bag/box/bundle conversion;
- excluded observations preserved as receipt provenance;
- >=64dp history rows opening Receipt Detail;
- compact/medium single-column and expanded eligible two-pane composition;
- Korean chart accessibility summary and nonlinear font-scaling-safe custom drawing;
- no identity/schema/price/search/Product Detail rewrite.

Canonical metric:

`CP32_METRICS commodity_detail_version=1 strict_basis_kinds=3 contextual_policy=1 grouping_not_comparability=1 responsive_cases=6 traceability=1 chart_single_basis=1 strict_sections=2 contextual_sections=2 purchase_rows=9`

Known evidence limit: no emulator/device screenshot campaign or real-user usability study in CP32 CI evidence.

### CP33 — Capture / Review UX V2 — NEXT PLANNED

Target flow:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

Primary acceptance direction:

- reduce manual review burden, especially for repeat known purchases;
- distinguish auto-confirmed versus review-required results clearly;
- preserve raw OCR/receipt evidence and correction provenance;
- never bypass CP24 identity authority or CP27 price eligibility for convenience;
- preserve offline/privacy permission posture;
- use CP30 commercial design grammar;
- do not absorb CP34 home/navigation shell into this checkpoint.

### CP34 — Commercial UI Shell
Product-centric home/navigation/search/category/product/commodity/receipt/settings integration. The user explicitly chose to defer complete navigation/launcher integration to this checkpoint rather than add temporary navigation during CP31/32.

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
- CP30 visual semantics present rather than reinterpret upstream facts.
- CP31 STANDARD Product Detail consumes exactly STANDARD_PACKAGE history and receipt provenance.
- CP32 NON_STANDARD detail preserves strict-basis isolation and contextual-only LIKE_FORM semantics.
- CP33 must not bypass identity/provenance rules for convenience.
- CP34 shell may connect existing destinations but must not redefine their business truth.

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

**CP32 is COMPLETE. CP33 — Capture / Review UX V2 is the next planned checkpoint and must not start without explicit user authorization.**
