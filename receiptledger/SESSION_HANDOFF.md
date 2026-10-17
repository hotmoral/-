# ReceiptLedger — Session Handoff

Updated: 2026-10-17 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct current project state from old chat before reading current documents and verifying refs.

Read in order:

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

## 1. Current state

V1 CP20–CP36 is complete. CP37 remains open.

Current state: **Remediation D READY_FOR_PHYSICAL_DIAGNOSTIC_RETEST**.

- branch: `receiptledger/run-post-v1-candidate-diagnostics-20261017`
- predecessor handoff: `99a7de8ba1c83771f11cefd7b6ab47e7d0590f99`
- frozen executable: `3e19741521b9be4039028bcb9981e400ff2ad867`
- Actions: `38987300764` SUCCESS
- job: `117261641673` SUCCESS
- artifact: `12083716548`
- artifact digest: `sha256:faada9ea2c87874d828e5c57fae9d42ccf4f966056ed6ce68943b33122784432`
- APK SHA-256: `1aa0f2d6ec2510b77a7b273eefd2b037ae8f0207021849c7da81ac054cb125e9`
- version: `1.0.39-candidate-diagnostics-validation` / 40
- package: `com.receiptledger.v1.candidateprobe`
- label: `ReceiptLedger 검증 D`
- lint: `No issues found.`

Do **not** mark CP37 complete.

## 2. Physical evidence sequence

### False item row

The first real-device sample exposed an address/header row classified as an item. Remediation A added narrow pre-date gating plus explicit non-product removal. Same-receipt retest confirmed the triggering row no longer appeared.

### Selective review coverage

Report v2 added `corrections_outside_review_items` and `review_scope_miss`. The first v2 physical sample confirmed `review_scope_miss=1`, with 2 corrected item ordinals outside the initially selected review set. `false_auto_confirm=0`.

### Repeated first-item blank fields

The same diagnostic receipt repeatedly showed the first reviewed item with blank quantity and unit price. Remediation C added a narrow exact-integer arithmetic prefill while preserving PARTIAL/review-required status.

Physical C retest showed the fields were still blank. The item remained review-required, so safety held but C's physical objective failed.

## 3. Why D exists

The C failure means the physical row did not match the C assumption. Do not add another solver rule by guess.

D observes the first initially reviewed item only and appends:

`RL_CP37_DIAG version=1 ...`

It reports candidate counts and relative regions, not receipt values.

The primary hypothesis is a product-name-zone numeric token being parsed as a quantity candidate. Strong support would be:

- `quantity_candidates > 0`
- `quantity_before_first_money > 0`
- `exact_arithmetic_pairs = 0`
- `integer_unit_pairs = 1`

This remains a hypothesis until physical output confirms it.

## 4. Frozen/non-goals

D does not change:

- `ItemTupleSolver`;
- `QuantityCandidate`;
- OCR/recovery;
- structure gating;
- selective-review policy;
- report v2 semantics;
- identity/price/search/persistence;
- schemas;
- permission posture.

The debug diagnostic is captured transiently and not saved into receipt DB/issues/items.

## 5. Verification

Canonical metric:

`CP37_CANDIDATE_DIAG_METRICS version=1 candidate_tests=4 integration_tests=1 report_v2_tests=8 item_tuple_tests=4 capture_review_tests=14 product_zone_quantity_probe=1 privacy_preserved=1 behavior_unchanged=1 schema_unchanged=1`

Focused tests, full regression, lint and APK packaging passed. The public repo contains no real receipt image or private purchase data.

## 6. Exact next task

This is physical diagnosis, not more coding.

1. install `ReceiptLedger 검증 D` side by side;
2. process the same diagnostic receipt/image once;
3. review every field against the original;
4. correct all factual/structural errors;
5. save;
6. tap `검증 결과 복사`;
7. return both copied lines: `RL_CP37_SAMPLE version=2 ...` and `RL_CP37_DIAG version=1 ...`.

Do not start the independent 10-receipt campaign yet.

## 7. Privacy

Real receipt images and values from chat must not be committed to the public repository. Public evidence remains sanitized counts/flags and generic defect descriptions only.
