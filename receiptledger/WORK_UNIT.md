# ReceiptLedger public execution work unit

Updated: 2026-10-17 KST

## Current stage

**CP37 — Physical Device / Real-Image OCR Validation**

Current substage:

**Remediation D — READY_FOR_PHYSICAL_DIAGNOSTIC_RETEST**

- branch: `receiptledger/run-post-v1-candidate-diagnostics-20261017`
- predecessor handoff: `99a7de8ba1c83771f11cefd7b6ab47e7d0590f99`
- frozen executable: `3e19741521b9be4039028bcb9981e400ff2ad867`
- canonical Actions: `38987300764` SUCCESS
- job: `117261641673`
- artifact: `12083716548`
- artifact digest: `sha256:faada9ea2c87874d828e5c57fae9d42ccf4f966056ed6ce68943b33122784432`
- APK SHA-256: `1aa0f2d6ec2510b77a7b273eefd2b037ae8f0207021849c7da81ac054cb125e9`
- versionName: `1.0.39-candidate-diagnostics-validation`
- versionCode: 40
- package: `com.receiptledger.v1.candidateprobe`
- label: `ReceiptLedger 검증 D`
- lint: 0 errors / 0 warnings

CP37 is **not complete**.

## Evidence already established

1. False address/header item was physically reproduced and Remediation A physically fixed the triggering row.
2. Report v2 physically confirmed a selective-review scope miss while `false_auto_confirm=0`.
3. The same diagnostic receipt repeatedly showed the first reviewed item with blank quantity and unit price.
4. Remediation C preserved explicit review but failed to fill those fields in the physical retest.
5. Therefore another solver heuristic is not authorized until candidate structure is observed.

## Diagnostic D output

The normal sanitized line remains:

`RL_CP37_SAMPLE version=2 ...`

A second line is now copied with it:

`RL_CP37_DIAG version=1 target=FIRST_REVIEW_ITEM ...`

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

No receipt value or OCR text is included.

## Current work unit

No further remediation coding is next.

1. Install `ReceiptLedger 검증 D` side by side.
2. Process the same diagnostic receipt/image once.
3. Visually inspect all recognized fields against the original.
4. Correct all factual/structural errors.
5. Save.
6. Tap `검증 결과 복사`.
7. Return both copied lines.
8. Analyze the candidate geometry before deciding any solver change.

The repeated diagnostic receipt does not count in the final independent 10.

## Decision rule

Strong evidence for a product-name-zone false quantity candidate is:

- `quantity_candidates > 0`
- `quantity_before_first_money > 0`
- `exact_arithmetic_pairs = 0`
- `integer_unit_pairs = 1`

If the physical values differ, diagnose that actual pattern instead of forcing this hypothesis.

## Frozen boundary

Until physical D evidence is analyzed, do not modify:

- ItemTupleSolver / QuantityCandidate;
- OCR/recovery;
- structure gating;
- selective-review policy;
- identity/price/search;
- schemas or permission posture.

## Public/privacy boundary

Only sanitized report/diagnostic lines and aggregate metrics may enter public evidence. Do not commit real receipts or private purchase data.

## Stop condition

**Await one same-receipt D physical report.**
