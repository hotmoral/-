# ReceiptLedger — Project Status Latest

Updated: 2026-10-17 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current boundary

Planned V1 CP20–CP36 is complete.

Post-V1 **CP37 — Physical Device / Real-Image OCR Validation** remains open.

Current state:

**Remediation D — READY_FOR_PHYSICAL_DIAGNOSTIC_RETEST**

CP37 is **NOT COMPLETE**. The independent 10-receipt campaign remains paused.

### Active refs

- branch: `receiptledger/run-post-v1-candidate-diagnostics-20261017`
- predecessor Remediation C handoff: `99a7de8ba1c83771f11cefd7b6ab47e7d0590f99`
- frozen Remediation D executable: `3e19741521b9be4039028bcb9981e400ff2ad867`
- canonical Actions: `38987300764` — SUCCESS
- canonical job: `117261641673` — SUCCESS
- artifact ID: `12083716548`
- artifact digest: `sha256:faada9ea2c87874d828e5c57fae9d42ccf4f966056ed6ce68943b33122784432`
- APK SHA-256: `1aa0f2d6ec2510b77a7b273eefd2b037ae8f0207021849c7da81ac054cb125e9`
- version: `1.0.39-candidate-diagnostics-validation` / versionCode 40
- debug applicationId: `com.receiptledger.v1.candidateprobe`
- label: `ReceiptLedger 검증 D`
- lint: 0 errors / 0 warnings

## 2. Physical evidence sequence

1. Initial physical sample: false address/header item found; Remediation A added narrow pre-date gating and explicit non-product item removal.
2. Same-receipt retest: triggering false address row no longer appeared.
3. Review-coverage instrumentation v2: first metric sample confirmed `review_scope_miss=1` with 2 corrected item ordinals outside the initially selected review set, while `false_auto_confirm=0`.
4. Repeated same-receipt evidence: first reviewed item repeatedly showed blank quantity and unit price.
5. Remediation C attempted a narrow arithmetic prefill while retaining PARTIAL/review-required status.
6. Physical C retest: quantity and unit price were still blank, while the item correctly remained explicitly review-required. Therefore C failed its physical objective but did not weaken safety.

A separate repeated OCR character-confusion pattern remains unmodified pending broader evidence.

## 3. Remediation D

Do not add another solver heuristic yet.

D adds a second privacy-preserving report line:

`RL_CP37_DIAG version=1 target=FIRST_REVIEW_ITEM ...`

It reports only candidate counts, relative regions, arithmetic-pair counts, solver resolution and sanitized reason token.

Important fields:

- `money_candidates`
- `quantity_candidates`
- `quantity_before_first_money`
- `quantity_between_money`
- `quantity_after_line`
- `exact_arithmetic_pairs`
- `integer_unit_pairs`
- `solver_resolution`
- `solver_reason`

The main hypothesis is that a numeric token in the product-name zone is being parsed as a quantity candidate and blocking the otherwise unique arithmetic recovery path. This is not yet proven.

## 4. Validation

Canonical metric:

`CP37_CANDIDATE_DIAG_METRICS version=1 candidate_tests=4 integration_tests=1 report_v2_tests=8 item_tuple_tests=4 capture_review_tests=14 product_zone_quantity_probe=1 privacy_preserved=1 behavior_unchanged=1 schema_unchanged=1`

All focused tests, full unit regression, lint, APK packaging, package/provider and permission checks passed.

## 5. Frozen behavior

Unchanged from the predecessor:

- `ItemTupleSolver` behavior;
- `QuantityCandidate` parsing;
- ML Kit OCR model/options;
- recovery preprocessing/pass order;
- Remediation A false-item gate;
- CP33 selective-review policy;
- report v2 semantics;
- item-removal behavior;
- identity/price/search/persistence semantics;
- product schema 2 / receipt schema 1;
- offline/privacy permission posture.

## 6. Exact next action

Install `ReceiptLedger 검증 D` side by side. Process the same diagnostic receipt once, visually inspect and correct all fields, save, tap `검증 결과 복사`, and return both copied lines:

1. `RL_CP37_SAMPLE version=2 ...`
2. `RL_CP37_DIAG version=1 ...`

The repeated diagnostic receipt does not count toward the final independent 10.

Do not modify solver/OCR/review policy or start the 10-receipt campaign until the diagnostic line is analyzed.

## 7. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP37_CANDIDATE_STRUCTURE_DIAGNOSTICS_CLOSEOUT.md`
4. `receiptledger/CP37_CANDIDATE_STRUCTURE_DIAGNOSTICS_EVIDENCE.md`
5. `receiptledger/CP37_CANDIDATE_STRUCTURE_DIAGNOSTICS_PLAN.md`
6. `receiptledger/CP37_PARTIAL_ROW_PREFILL_REMEDIATION_CLOSEOUT.md`
7. `receiptledger/CP37_PARTIAL_ROW_PREFILL_REMEDIATION_EVIDENCE.md`
8. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_CLOSEOUT.md`
9. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_EVIDENCE.md`
10. `receiptledger/CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
11. `receiptledger/CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
12. `receiptledger/CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
13. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
14. `receiptledger/README.md`
15. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify docs-only handoff HEAD and frozen executable separately.
