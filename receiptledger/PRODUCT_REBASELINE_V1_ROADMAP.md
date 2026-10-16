# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-16 KST
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, inspect personal historical prices, and judge whether a current price is cheap/normal/expensive without fake normalization of non-standard goods.

Every checkpoint closes only after exact executable evidence, plan/code comparison and docs-only handoff synchronization.

## 1. Completed product/storage stages

### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE
Personal purchase-price memory and comparison is the frozen product essence.

### CP21 — Catalog Domain V2 — COMPLETE
Stable-ID identity, STANDARD/NON_STANDARD boundary, structured product fields, exact physical measures, raw purchase forms, category non-authority and evidence/confirmation separation.

### CP22 — Persistence V2 — COMPLETE
Frozen `449896c7580fb3412f41c9b58d1ab9412d13d84d`; Actions `38816200340` SUCCESS. Product schema 2; receipt schema 1.

### CP23 — Receipt Product Semantics — COMPLETE
Frozen `5bffb66bd43814f8d638791b5697f79ff089028b`; Actions `38822100885` SUCCESS. Conservative unconfirmed semantic evidence.

### CP24 — Identity Resolver V2 — COMPLETE
Frozen `4b556afd4dd52b68cf768e937bb456665ad4c231`; Actions `38824134990` SUCCESS. Exact authority and review/unresolved fallback preserved.

### CP25 — Category System — COMPLETE
Frozen `042c3b59063f0e58a273a5f685b25780683fcf36`; Actions `38827880730` SUCCESS. Category remains classification/browse metadata, never identity authority.

### CP26 — Commodity / Non-standard V2 — COMPLETE
Frozen `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`; Actions `38829423445` SUCCESS. Grouping remains distinct from price comparability.

## 2. Price intelligence

### CP27 — Price Intelligence V2 — COMPLETE
Frozen `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`; Actions `38831623548` SUCCESS.

- receipt-traceable comparison numerator/denominator;
- STANDARD exact package;
- kg/g -> price/kg, L/mL -> price/L, count -> price/each;
- package/form units contextual only;
- unsupported discount attribution excluded, not guessed.

### CP28 — Price Evaluation — COMPLETE
Frozen `dd4f98613677ae998932d77f3e5f89d7bddba107`; Actions `38834818192` SUCCESS.

- baseline = median of previous max 5 eligible observations;
- minimum 3 prior observations;
- material difference >=5% AND >=100 minor units;
- extreme >=15% AND >=500 minor units;
- contextual LIKE_FORM remains unjudged;
- no market-price claim.

## 3. Find and inspect

### CP29 — Search / Browse — COMPLETE
Frozen `b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`; Actions `38839041465` SUCCESS.

Read-only deterministic discovery. Search relevance cannot create/merge/relink identity. Mutable FTS/index/cache remains deferred pending CP36 measurement.

## 4. Commercial UX

### CP30 — Design System Foundation — COMPLETE
Frozen `ff0745db529499171246866039521a0b83e830e4`; Actions `38842905325` SUCCESS.

Programmatic Android widgets retained; Korean-first typography, semantic states, spacing/radius/elevation/touch targets, responsive classes and single-basis chart grammar frozen.

### CP31 — Product Detail — COMPLETE
Frozen `1d2e7ef67e949af9098027a78e30551c228c255c`; Actions `38852423981` SUCCESS.

Commercial STANDARD-product price-memory detail: exact identity, recent/previous/usual price, CP28 judgment/reason, STANDARD_PACKAGE chart, receipt-traceable history and responsive composition.

### CP32 — Commodity Detail — COMPLETE
Frozen `e42629ccd66a80a4a1a14de0c7798b178d6b0062`; Actions `38855942283` SUCCESS.

Commercial NON_STANDARD detail while preserving grouping != comparability:

- separate WEIGHT_KG / VOLUME_L / EACH strict cohorts;
- contextual package-form history reference-only;
- no fake conversion;
- basis-specific chart/judgment;
- receipt/store/date traceability.

### CP33 — Capture / Review UX V2 — COMPLETE
Frozen `34cdac2d3e61081ab2a529173dbef9a2431431e0`; canonical Actions `38874509796` SUCCESS.

Delivered:

- image selection/capture automatically starts existing OCR/recovery;
- explicit Save remains mandatory;
- clean deterministic receipts skip mandatory full edit;
- deterministic V2 review assessment exposes only material blockers;
- selective review plus voluntary full edit;
- `DEFAULT_ONE` quantity requires explicit user confirmation;
- corrected USER_EDITED/USER_CONFIRMED provenance can exit review when material truth is valid;
- raw OCR preserved;
- already-confirmed GLOBAL exact aliases reused best-effort only after successful receipt persistence;
- no fuzzy/new-product auto identity;
- optional post-save work cannot make an already-saved receipt appear failed;
- primary capture content vertically scrollable for constrained-height accessibility;
- old development diagnostics removed from primary user UI;
- schemas and upstream domain logic unchanged.

Canonical metric:

`CP33_METRICS capture_review_version=2 auto_confirm_cases=2 review_required_cases=7 user_edit_exit=1 selective_review=1 full_edit=1 raw_ocr_preserved=1 exact_alias_reuse=1 unknown_alias_safe=1 link_failure_isolated=1 auto_processing=1 schema_unchanged=1`

### CP34 — Commercial UI Shell — NEXT PLANNED

Goal: integrate the already-built capabilities into one coherent normal-user product shell.

Expected scope:

- product-centric home/primary navigation;
- obvious receipt-add entry into the CP33 flow;
- search/browse/category destinations;
- STANDARD Product Detail and NON_STANDARD Commodity Detail entry paths;
- receipt history/detail;
- supporting settings/help/navigation only where justified;
- remove reliance on legacy engineering-oriented entry paths.

CP34 must **not** redefine identity, price, review or persistence truth to make navigation easier. No Compose/Material migration is implied.

## 5. Validation and hardening

### CP35 — Real Receipt Evaluation
Use public-safe synthetic or explicitly approved sanitized fixtures to measure end-to-end correct purchase registration. Primary metric is correct purchase registration, not OCR character accuracy alone.

### CP36 — Performance / Reliability
Verify startup, OCR latency/memory, large catalog/history, search, price/evaluation/chart workloads, migrations, archive reconciliation and recovery. Benchmark CP29 linear scan around representative 1k/10k scale before adding FTS/index/cache.

## 6. Dependency gates

- stable catalog ID remains final identity authority;
- product schema 2 / receipt schema 1 remain frozen unless an explicit migration need is proved;
- parser evidence is non-authoritative until confirmed;
- category/price/search/UI cannot widen identity authority;
- commodity grouping remains distinct from comparability;
- CP27 eligible cohort is the only CP28 price input basis;
- CP28 judgment thresholds cannot be reimplemented by UI;
- CP29 search is read-only;
- CP30 presentation presents rather than reinterprets facts;
- CP31 STANDARD detail consumes STANDARD_PACKAGE only;
- CP32 preserves strict basis separation and contextual package semantics;
- CP33 selective-review convenience cannot erase provenance or make uncertain values authoritative;
- CP34 navigation must integrate these frozen contracts, not rewrite them.

## 7. Every checkpoint asks, only where material

- Does stored-data meaning change?
- Can false merge/grouping or false split occur?
- Does confirmed repeat use reduce review burden?
- Is raw receipt/purchase evidence preserved?
- Is every compared price exactly defined and receipt-traceable?
- Can incomparable prices look comparable?
- Can discounts be falsely allocated?
- Can search relevance be mistaken for identity evidence?
- Can UI imply a judgment that upstream logic did not produce?
- Can provenance/validation be bypassed?
- Can permissions/network/privacy posture change?
- Can a new performance hot path appear?
- Which local regression catches failure now?

Avoid ritual audits, speculative abstractions, unrelated cleanup and expansion into budgeting/banking/cloud/e-commerce before the core loop is complete.

## 8. Handoff discipline

At every completed group:

1. freeze exact implementation/spec HEAD;
2. record CI/artifact/evidence;
3. record limitations and meaningful failures;
4. compare plan/acceptance to actual implementation even if CI is green;
5. update status/handoff/readme/work-unit/roadmap docs;
6. verify all post-boundary changes are documentation-only;
7. stop before the next unauthorized checkpoint.

## 9. Current boundary

**CP33 is COMPLETE. CP34 — Commercial UI Shell is next planned and has NOT STARTED. Await explicit user authorization.**
