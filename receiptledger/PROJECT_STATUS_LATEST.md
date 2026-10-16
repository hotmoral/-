# ReceiptLedger — Project Status Latest

Updated: 2026-10-17 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current boundary

Planned V1 CP20–CP36 is complete.

Post-V1 **CP37 — Physical Device / Real-Image OCR Validation** remains open.

Current state:

**Remediation C — READY_FOR_PHYSICAL_PREFILL_RETEST**

CP37 itself is **NOT COMPLETE**. The independent 10-receipt campaign is paused until the repeated same-receipt blank-field defect is physically rechecked.

### Active refs

- branch: `receiptledger/run-post-v1-partial-row-prefill-20261017`
- predecessor review-coverage handoff: `d4f75d8120e4a9c347b3777c64b511e4f5d224d4`
- frozen Remediation C executable: `01b22652a45889b6bfaa474131e0c5fa7f19e96e`
- canonical Actions: `38979684033` — SUCCESS
- canonical job: `117237351555` — SUCCESS
- artifact ID: `12080029714`
- artifact digest: `sha256:55300e9525851f02232dc03f9a528fcd5b3c9c30ba68e7a30eb0bdb6634d46c2`
- APK SHA-256: `65fe0827f3a9ebfeafbbf783c6c8f82544f8594203008692288ab74ec9eb1e0e`
- version: `1.0.38-partial-row-prefill-validation` / versionCode 39
- debug applicationId: `com.receiptledger.v1.rowrecovery`
- label: `ReceiptLedger 검증 C`
- lint: 0 errors / 0 warnings

## 2. Physical evidence sequence

### Initial physical sample

A real receipt was conservatively REVIEW_REQUIRED but exposed a false address/header item and no way to remove it.

### Remediation A

A narrow pre-date false-item gate plus explicit non-product item removal was added. Same-receipt physical retest confirmed the false address/header row no longer appeared.

### Review Coverage Instrumentation

The Remediation A retest showed only 1 of 15 items initially selected for review while full visual verification required multiple item corrections. Report schema v2 added:

- `corrections_outside_review_items`
- `review_scope_miss`

The first physical v2 metric-check sample emitted:

- `initial_items=15`
- `initial_review_items=1`
- `corrections_outside_review_items=2`
- `review_scope_miss=1`
- `false_auto_confirm=0`

This verifies the v2 metric path and confirms a real selective-review coverage miss.

The same sample also reproduced a separate first-item issue across builds: quantity and unit price were blank. A package-suffix character recognition confusion also repeated, but remains unmodified pending broader evidence.

## 3. Remediation C

The first-item blank-field pattern matched a deterministic `ItemTupleSolver` gap: when two or more money values were recognized but the quantity token was missing, a valid printed unit-price candidate could be discarded.

Remediation C now prefills quantity/unit price only when exactly one preceding printed money candidate gives an exact integer ratio to the printed line amount, with quantity 1..99.

Safety boundary:

- quantity origin = `INFERRED_ARITHMETIC`;
- unit and line amount origins = `PRINTED`;
- resolution remains `PARTIAL`;
- explicit review remains required;
- ambiguous or non-integral cases remain unresolved.

## 4. Validation

Canonical metric:

`CP37_PARTIAL_PREFILL_METRICS version=1 item_tuple_tests=4 capture_review_tests=14 report_v2_tests=8 unique_integer_prefill=1 ambiguous_rejected=1 partial_review_preserved=1 report_v2_unchanged=1 schema_unchanged=1`

All focused tests, full unit regression, lint and APK packaging passed.

## 5. Frozen contracts

Unchanged:

- ML Kit OCR model/options;
- OCR preprocessing/recovery passes;
- Remediation A false-item gate;
- CP33 selective-review policy itself;
- report v2 semantics;
- identity/price/search/persistence;
- product schema 2 / receipt schema 1;
- offline/privacy permission posture.

## 6. Exact next action

Install `ReceiptLedger 검증 C` side by side and rerun the same receipt once.

Confirm:

1. first item quantity is no longer blank;
2. first item unit price is no longer blank;
3. the first item still appears in explicit review;
4. all fields are visually checked and corrected;
5. save and return only `RL_CP37_SAMPLE version=2 ...`.

Do not start the independent 10-receipt campaign until this retest is analyzed.

## 7. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP37_PARTIAL_ROW_PREFILL_REMEDIATION_CLOSEOUT.md`
4. `receiptledger/CP37_PARTIAL_ROW_PREFILL_REMEDIATION_EVIDENCE.md`
5. `receiptledger/CP37_PARTIAL_ROW_PREFILL_REMEDIATION_PLAN.md`
6. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_CLOSEOUT.md`
7. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_EVIDENCE.md`
8. `receiptledger/CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
9. `receiptledger/CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
10. `receiptledger/CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
11. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
12. `receiptledger/README.md`
13. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify docs-only handoff HEAD and frozen executable separately.
