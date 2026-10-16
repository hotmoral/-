# ReceiptLedger V1 — Product-Centric Roadmap

Updated: 2026-10-17 KST
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## 0. Governing objective

Complete the smallest coherent product that lets a user add a receipt with minimal manual work, obtain trustworthy product/commodity identities and purchase prices, find a repeat purchase later, inspect personal historical prices, and judge whether a current price is cheap/normal/expensive without fake normalization of non-standard goods.

Every checkpoint closes only after exact executable evidence, plan/code comparison and docs-only handoff synchronization.

## 1. Completed chain

### CP20 — Product Rebaseline / V1 Master Specification — COMPLETE
Personal purchase-price memory and comparison is the frozen product essence.

### CP21 — Catalog Domain V2 — COMPLETE
Stable-ID identity, STANDARD/NON_STANDARD boundary, structured product fields, exact physical measures, raw purchase forms, category non-authority and evidence/confirmation separation.

### CP22 — Persistence V2 — COMPLETE
Frozen `449896c7580fb3412f41c9b58d1ab9412d13d84d`; product schema 2 / receipt schema 1.

### CP23 — Receipt Product Semantics — COMPLETE
Conservative unconfirmed semantic evidence.

### CP24 — Identity Resolver V2 — COMPLETE
Exact authority and review/unresolved fallback preserved.

### CP25 — Category System — COMPLETE
Category remains browse metadata, never identity authority.

### CP26 — Commodity / Non-standard V2 — COMPLETE
Grouping remains distinct from price comparability.

### CP27 — Price Intelligence V2 — COMPLETE
STANDARD exact package; kg/g -> price/kg; L/mL -> price/L; count -> price/each; contextual package forms remain non-normalized; unsupported discount attribution excluded.

### CP28 — Price Evaluation — COMPLETE
Median baseline, minimum-history gate, material/extreme thresholds and contextual no-judgment contract frozen.

### CP29 — Search / Browse — COMPLETE
Read-only deterministic discovery. Search relevance cannot create/merge/relink identity.

### CP30 — Design System Foundation — COMPLETE
Programmatic Android widgets retained; Korean-first typography, semantic states, spacing/radius/elevation/touch targets, responsive classes and single-basis chart grammar frozen.

### CP31 — Product Detail — COMPLETE
STANDARD product detail with exact identity, recent/previous/usual price, CP28 judgment/reason, STANDARD_PACKAGE chart and receipt-traceable history.

### CP32 — Commodity Detail — COMPLETE
NON_STANDARD detail preserving strict WEIGHT_KG/VOLUME_L/EACH cohorts, contextual package-form history and grouping != comparability.

### CP33 — Capture / Review UX V2 — COMPLETE
Automatic OCR/recovery start, selective review, explicit save, DEFAULT_ONE confirmation, exact confirmed alias reuse after durable save and post-save failure isolation.

### CP34 — Commercial UI Shell — COMPLETE
Product-centric Home launcher, receipt-add entry, search/recent/frequent/category discovery, Product/Commodity detail routing and receipt-history provenance.

### CP35 — Real Receipt Evaluation — COMPLETE
Public-safe synthetic token/geometry corpus validated registration safety, exact-alias reuse, conservative unresolved behavior, strict/contextual commodity separation, discount exclusion, mismatch exclusion and detail receipt provenance.

### CP36 — Performance / Reliability — COMPLETE
Frozen executable: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
Canonical Actions: `38926526457` SUCCESS.

Measurement-first hardening found a material CP29 SQLite discovery bottleneck. Bounded remediation changed only the discovery read path:

- `SearchBrowseServiceV1.java`;
- `SqliteSearchBrowseSnapshotV1.java`.

No FTS, persistent cache, new index or schema was introduced.

Final canonical measurements:

- startup median/max: 516 / 748 ms;
- Home PSS: 42,787 KB;
- search 1k: 189 ms;
- search 10k: 1,524 ms;
- recent 10k: 856 ms;
- price 1k: 461 ms;
- detail 1k: 459 ms;
- chart 1k: 19 ms;
- OCR cold: 4,448 ms;
- OCR warm median: 4,078 ms;
- migration 1k: 4 ms;
- archive reconciliation: 41 ms;
- reopen cycles: 10;
- semantic failures: 0.

SQLite fast-path semantic/fail-fast parity: 1/1 PASS.

The only final budget breach is warm OCR on the API 34 x86_64 CI emulator. It is an explicitly accepted V1 risk because cold OCR and memory are within budget, recognizer reuse is already in place, and real-photo OCR accuracy versus downsampling/resolution has not been established. Production OCR remains unchanged.

## 2. Frozen dependency gates

- stable catalog ID remains final identity authority;
- product schema 2 / receipt schema 1 remain frozen unless a separately authorized migration need is proved;
- parser evidence is non-authoritative until confirmed;
- category/price/search/UI cannot widen identity authority;
- commodity grouping remains distinct from comparability;
- CP27 eligible cohort is the only CP28 price input basis;
- CP28 thresholds cannot be reimplemented by UI;
- CP29 search remains read-only;
- CP30 presentation presents rather than reinterprets facts;
- CP31 STANDARD detail consumes STANDARD_PACKAGE only;
- CP32 preserves strict/contextual separation;
- CP33 convenience cannot erase provenance or authorize uncertain data;
- CP34 navigation integrates but does not rewrite truth;
- CP35 evidence must not be overstated beyond its synthetic token-boundary corpus;
- CP36 optimization remains measurement-driven and bounded to proven bottlenecks.

## 3. Current roadmap boundary

The authorized V1 roadmap **CP20 through CP36 is complete**.

No post-V1 checkpoint is currently authorized.

Potential future work such as physical-device OCR profiling, real-image merchant/font coverage, new features, schema changes, release/signing or broader optimization requires:

1. explicit user authorization;
2. recovery of current handoff and frozen executable refs;
3. a newly named bounded checkpoint with scope/non-goals/acceptance/evidence/stop conditions;
4. contradiction/consistency review before implementation.

## 4. Checkpoint discipline

At every future checkpoint, where material:

- recover canonical GitHub state first;
- compare prior frozen contracts against the proposed change;
- catch cheap contradictions before implementation;
- avoid ritual audits and speculative abstractions;
- measure before optimizing;
- preserve provenance and authority boundaries;
- compare plan vs actual even after green CI;
- freeze exact executable/evidence refs;
- synchronize docs-only handoff;
- stop before unauthorized work.

## 5. Handoff discipline

At every completed group:

1. freeze exact executable/spec HEAD;
2. record CI/artifact/evidence and known limitations;
3. record meaningful failure/remediation history;
4. compare acceptance criteria to actual implementation;
5. update status/handoff/readme/work-unit/roadmap docs;
6. verify all post-boundary changes are documentation-only;
7. verify the handoff commit is directly based on the frozen executable when possible;
8. stop before the next unauthorized checkpoint.

## 6. Current stop condition

**Planned ReceiptLedger V1 CP20–CP36 is COMPLETE. Await explicit user authorization for any post-V1 work.**
