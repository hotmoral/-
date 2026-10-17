# CP37 Candidate Structure Diagnostics — Closeout

Updated: 2026-10-17 KST

## Status

**READY_FOR_PHYSICAL_DIAGNOSTIC_RETEST**

CP37 remains open. The independent 10-receipt campaign is still paused.

## Trigger

Remediation C passed code/CI validation but failed the same-receipt physical retest: the first reviewed item still showed blank quantity and unit price while remaining safely review-required.

This disproved the narrow assumption that the physical row had no parsed quantity candidate plus exactly one valid printed unit candidate.

## Scope

Candidate Diagnostics D adds privacy-preserving structural evidence only. It does not change solver, OCR, structure gating, review selection, identity, price, search, persistence, schemas, or permissions.

Existing output remains:

`RL_CP37_SAMPLE version=2 ...`

A second line is appended:

`RL_CP37_DIAG version=1 target=FIRST_REVIEW_ITEM ...`

The diagnostic line contains only counts, relative candidate regions, arithmetic-pair counts, solver resolution, and sanitized reason tokens. It never emits OCR text, names, dates, stores, IDs, prices, amounts, or coordinates.

## Diagnostic fields

- `money_candidates`
- `quantity_candidates`
- `quantity_before_first_money`
- `quantity_between_money`
- `quantity_after_line`
- `exact_arithmetic_pairs`
- `integer_unit_pairs`
- `solver_resolution`
- `solver_reason`

## Physical hypothesis under test

The leading hypothesis is that a numeric token in the product-name zone is parsed as a quantity candidate and blocks the Remediation C prefill path.

Strong support would be:

- `quantity_candidates > 0`
- `quantity_before_first_money > 0`
- `exact_arithmetic_pairs = 0`
- `integer_unit_pairs = 1`

No remediation is authorized until the physical diagnostic line is observed.

## Frozen executable

- branch: `receiptledger/run-post-v1-candidate-diagnostics-20261017`
- frozen executable: `3e19741521b9be4039028bcb9981e400ff2ad867`
- predecessor handoff: `99a7de8ba1c83771f11cefd7b6ab47e7d0590f99`
- Actions: `38987300764` SUCCESS
- job: `117261641673` SUCCESS
- artifact: `12083716548`
- artifact digest: `sha256:faada9ea2c87874d828e5c57fae9d42ccf4f966056ed6ce68943b33122784432`
- APK SHA-256: `1aa0f2d6ec2510b77a7b273eefd2b037ae8f0207021849c7da81ac054cb125e9`
- version: `1.0.39-candidate-diagnostics-validation` / 40
- debug applicationId: `com.receiptledger.v1.candidateprobe`
- label: `ReceiptLedger 검증 D`
- lint: `No issues found.`

## Validation

Canonical metric:

`CP37_CANDIDATE_DIAG_METRICS version=1 candidate_tests=4 integration_tests=1 report_v2_tests=8 item_tuple_tests=4 capture_review_tests=14 product_zone_quantity_probe=1 privacy_preserved=1 behavior_unchanged=1 schema_unchanged=1`

Focused and full regression checks passed. Forbidden camera/media/storage/network permissions are absent.

## Next action

Install `ReceiptLedger 검증 D`, process the same diagnostic receipt once, visually correct all fields, save, tap `검증 결과 복사`, and return both lines:

1. `RL_CP37_SAMPLE version=2 ...`
2. `RL_CP37_DIAG version=1 ...`

Do not start the independent 10-receipt campaign before this result is analyzed.
