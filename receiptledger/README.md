# ReceiptLedger public execution namespace

ReceiptLedger is a personal purchase-price memory and comparison system. This namespace contains public-safe Android/OCR implementation, validation, CI and debug evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP37_CANDIDATE_STRUCTURE_DIAGNOSTICS_CLOSEOUT.md`
4. `CP37_CANDIDATE_STRUCTURE_DIAGNOSTICS_EVIDENCE.md`
5. `CP37_CANDIDATE_STRUCTURE_DIAGNOSTICS_PLAN.md`
6. `CP37_PARTIAL_ROW_PREFILL_REMEDIATION_CLOSEOUT.md`
7. `CP37_PARTIAL_ROW_PREFILL_REMEDIATION_EVIDENCE.md`
8. `CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_CLOSEOUT.md`
9. `CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
10. `CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
11. `CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
12. `PRODUCT_REBASELINE_V1_ROADMAP.md`
13. `WORK_UNIT.md`

GitHub is canonical. Verify current docs-only handoff and frozen executable separately.

## Current boundary

V1 CP20–CP36: **COMPLETE**.

Post-V1 CP37: **IN PROGRESS**.

Current state: **Remediation D — READY_FOR_PHYSICAL_DIAGNOSTIC_RETEST**.

- branch `receiptledger/run-post-v1-candidate-diagnostics-20261017`
- predecessor handoff `99a7de8ba1c83771f11cefd7b6ab47e7d0590f99`
- frozen executable `3e19741521b9be4039028bcb9981e400ff2ad867`
- Actions `38987300764` SUCCESS
- job `117261641673`
- artifact `12083716548`
- digest `sha256:faada9ea2c87874d828e5c57fae9d42ccf4f966056ed6ce68943b33122784432`
- APK SHA-256 `1aa0f2d6ec2510b77a7b273eefd2b037ae8f0207021849c7da81ac054cb125e9`
- version `1.0.39-candidate-diagnostics-validation` / 40
- debug app `com.receiptledger.v1.candidateprobe`
- label `ReceiptLedger 검증 D`

## Why D exists

The same diagnostic receipt repeatedly showed the first reviewed item with blank quantity and unit price. Remediation C attempted a narrow arithmetic prefill but the physical retest still showed both fields blank.

Rather than stacking another heuristic, D adds a privacy-safe second line:

`RL_CP37_DIAG version=1 ...`

It exposes only candidate counts/relative regions and sanitized solver tokens. Existing `RL_CP37_SAMPLE version=2` semantics are unchanged.

The current leading hypothesis is a numeric token in the product-name zone being parsed as a quantity candidate, but this is not yet proven.

## Next physical step

Install `ReceiptLedger 검증 D`, rerun the same diagnostic receipt once, correct all factual fields, save, and return both copied lines:

- `RL_CP37_SAMPLE version=2 ...`
- `RL_CP37_DIAG version=1 ...`

Do not begin the independent 10-receipt campaign until the diagnostic result is analyzed.

## Privacy

Never commit/share publicly real receipt photos, OCR text, merchant/product names, dates, prices, IDs, file paths, private DBs/backups, credentials or signing material.

The diagnostic report emits structural counts/flags only.
