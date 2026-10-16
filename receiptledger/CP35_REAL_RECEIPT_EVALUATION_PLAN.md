# ReceiptLedger V1 — CP35 Real Receipt Evaluation Plan

Updated: 2026-10-16 KST
Checkpoint: **CP35 — Real Receipt Evaluation**
Status: **AUTHORIZED / IN PROGRESS**

## 1. Canonical baseline

- predecessor handoff: `386c1b3d9ef7f3737ffd8b4d0f34fe2e076cab8e`
- predecessor frozen executable: `d9764b1447aefaaf3e3fdc5785c72c7c98e8314e`
- working branch: `receiptledger/run-v1-real-receipt-evaluation-20261016`

The handoff ref and executable/evidence ref remain distinct.

## 2. Product objective

ReceiptLedger is a personal purchase-price memory and comparison system. CP35 evaluates whether a receipt becomes a trustworthy purchase-memory record end to end.

Primary metric is **correct purchase registration**, not OCR character accuracy by itself.

Evaluated chain:

`public-safe receipt fixture -> recognition/structure -> ReceiptRecord -> CP33 review decision -> identity resolution/confirmation -> price observation/cohort -> CP31/32 detail projection -> source receipt traceability`

## 3. Evaluation philosophy

CP35 does not require 100% automatic classification. A conservative unresolved/review outcome is correct when the system lacks authority.

Priority order:

1. zero false authoritative registration;
2. after fixture-prescribed minimal review/confirmation, final registration matches ground truth;
3. confirmed repeat identity reduces later review burden through the frozen exact-alias path;
4. only CP27-eligible prices enter comparable cohorts;
5. every displayed purchase remains traceable to the exact receipt ID.

## 4. Public-safe fixture policy

Only synthetic or explicitly approved sanitized fixtures may enter the public repository.

This checkpoint will use synthetic Korean retail receipts with fictional merchant names and invented purchase data. No private receipt image, personal identifier, payment identifier, membership number, address, phone number or real purchase database is permitted.

The fixtures represent realistic failure classes but are not claimed to be a statistically representative market corpus.

## 5. Frozen production contracts

CP35 must preserve:

- stable catalog ID as identity authority;
- exact confirmed alias reuse only;
- no fuzzy/category/search/price identity promotion;
- product schema 2 / receipt schema 1;
- CP27 comparison eligibility and discount attribution rules;
- CP28 evaluation thresholds;
- CP30–34 UI/navigation meaning;
- CP33 review/provenance behavior;
- OCR/recovery/item/validation production algorithms unless evaluation proves a material correctness defect;
- offline/no-network/no-broad-permission posture.

The default implementation strategy is **evaluation-only**. Production changes require a demonstrated failing fixture and the smallest coherent correction.

## 6. Canonical fixture classes

The initial corpus covers eight independent risk classes:

1. `RRE-01 STANDARD_NEW` — a new packaged product is recognized correctly but remains non-authoritative until explicit identity confirmation.
2. `RRE-02 STANDARD_REPEAT_EXACT` — the same confirmed alias on a later receipt reuses the exact stable ID automatically and contributes a second comparable STANDARD_PACKAGE observation.
3. `RRE-03 STANDARD_SIMILAR_NOT_EXACT` — a similar but different raw name must not inherit the confirmed alias or stable ID.
4. `RRE-04 COMMODITY_WEIGHT` — `1kg` and `500g` purchases of one confirmed commodity normalize only into WEIGHT_KG.
5. `RRE-05 COMMODITY_CONTEXTUAL` — `1봉` and `1상자` may belong to one commodity while remaining separate contextual LIKE_FORM cohorts.
6. `RRE-06 MULTI_ITEM_DISCOUNT` — a receipt-level discount across multiple items must not be allocated to a linked item; the observation remains excluded.
7. `RRE-07 TOTAL_MISMATCH_REVIEW` — arithmetic mismatch must remain REVIEW_REQUIRED and cannot be treated as safe price evidence.
8. `RRE-08 DETAIL_TRACEABILITY` — CP31/32 detail purchase rows must preserve exact source receipt IDs and comparison eligibility.

## 7. Required measurements

The evaluation test must emit one deterministic `CP35_METRICS` line covering at minimum:

- fixture count;
- receipt structure correctness;
- expected review decisions;
- final registration correctness;
- exact-alias repeat reuse;
- conservative unresolved similar-name case;
- false auto-link count;
- strict commodity normalization cases;
- contextual separation cases;
- discount exclusion cases;
- invalid/mismatch exclusion cases;
- detail receipt-traceability cases;
- product/receipt schema unchanged.

Any nonzero false auto-link or false comparable-price inclusion is a checkpoint failure.

## 8. Acceptance criteria

CP35 may close only if:

- all public-safe fixture ground truths are deterministic and documented;
- every fixture traverses the frozen production services relevant to its risk class;
- final authoritative registrations are correct after only the fixture-declared user confirmations;
- unknown/similar identities are not silently promoted;
- repeat exact aliases reuse the same stable ID;
- strict vs contextual commodity semantics remain separated;
- multi-item discount and invalid receipt evidence do not contaminate comparable price cohorts;
- CP31/32 detail rows remain receipt-traceable;
- upstream CP29–34 regressions remain green;
- lint is clean and debug APK builds;
- packaged forbidden permissions remain absent;
- plan/code comparison is performed after green CI;
- exact executable HEAD/run/artifact/hash are frozen before docs-only handoff synchronization.

## 9. Non-goals

CP35 does not include:

- OCR model replacement or tuning campaign;
- private real-receipt publication;
- broad parser redesign without a failing fixture;
- market-price accuracy claims;
- search/index/cache/performance optimization;
- CP36 scale, latency, memory or reliability benchmarking;
- release signing;
- Compose/Material migration;
- budgeting, banking, cloud sync or e-commerce scope.

## 10. Stop condition

After CP35 acceptance/evidence and docs-only handoff synchronization, stop before CP36 without explicit user authorization.
