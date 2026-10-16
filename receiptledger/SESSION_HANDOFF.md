# ReceiptLedger — Session Handoff

Updated: 2026-10-17 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct current state from old chat before reading the current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_CLOSEOUT.md`
4. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_EVIDENCE.md`
5. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_PLAN.md`
6. `receiptledger/CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
7. `receiptledger/CP37_FALSE_ITEM_ROW_REMEDIATION_EVIDENCE.md`
8. `receiptledger/CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
9. `receiptledger/CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

## 1. Current state

V1 CP20–CP36 is complete. CP37 is open.

Current state: **Selective Review Coverage Instrumentation READY_FOR_PHYSICAL_METRIC_CHECK**.

- branch: `receiptledger/run-post-v1-selective-review-coverage-20261017`
- predecessor handoff: `c4e00ff22339869346f0f8692e38d82567568b7e`
- frozen executable: `7dbed4cf73a2963ace7447974e9d972a9776b79f`
- Actions: `38976080450` SUCCESS
- job: `117225743973` SUCCESS
- artifact: `12078898591`
- artifact digest: `sha256:402a5dda9d0892550ff08d5a5f3dbeb228a01a6f32abc40d24f8a75efa510b67`
- APK SHA-256: `29fcd2073d74fee819d53525bf2409db1587a72e72e86af115496843562405b8`
- version: `1.0.37-review-coverage-validation` / 38
- package: `com.receiptledger.v1.reviewcoverage`
- label: `ReceiptLedger 검증 B`
- lint: `No issues found.`

Do **not** mark CP37 complete.

## 2. Physical evidence sequence

### Sample A — initial Phase B diagnostic

REVIEW_REQUIRED correctly prevented false auto-confirm, but an address/header row was classified as a product item. The old review UI could not delete that row.

### Remediation A

Implemented a narrow pre-date false-item gate plus explicit `이 항목은 상품이 아님` removal recovery.

### Sample B — Remediation A physical retest

The same false address row did **not** appear as an item. Remediation A is therefore physically confirmed for the triggering defect.

The retest also showed initial_items=15 and initial_review_items=1, but after full visual verification the user corrected 3 item names, 1 quantity and 1 unit price. Since report v1 only counted field deltas, it could not determine how many corrected item ordinals were outside the initially selected review set.

## 3. New report v2 contract

Output begins:

`RL_CP37_SAMPLE version=2 ...`

New fields:

- `corrections_outside_review_items=N`
- `review_scope_miss=0|1`

Definition:

A distinct item ordinal counts once when it was not in initial `assessment.itemOrdinals` and later had any name/quantity/unit-price/line-amount edit, removal or addition.

`review_scope_miss=1` iff the count is greater than zero.

Multiple field corrections on one item still count as one out-of-scope item.

Receipt-level field corrections are not included in this metric.

## 4. Instrumentation-only boundary

No product review behavior changed. Frozen from Remediation A:

- OCR/recovery;
- false-item structure gate;
- review selection policy;
- item removal behavior;
- identity/price/search;
- schemas;
- permissions.

## 5. Verification

Canonical metric:

`CP37_REVIEW_COVERAGE_METRICS report_version=2 tests=8 outside_scope_detection=1 in_scope_control=1 distinct_item_counting=1 removal_detection=1 privacy_preserved=1 product_behavior_unchanged=1 schema_unchanged=1`

Report suite 8/8 PASS; full unit regression/lint/APK PASS. APK badging confirms package `com.receiptledger.v1.reviewcoverage`, label `ReceiptLedger 검증 B`, and provider `com.receiptledger.v1.reviewcoverage.capture`.

## 6. Exact next task

This is physical evidence collection, not more coding.

1. install `ReceiptLedger 검증 B` side by side;
2. use one real receipt;
3. visually compare every field with the original, regardless of initial decision;
4. correct every factual/structural error;
5. save;
6. tap `검증 결과 복사`;
7. return only the `RL_CP37_SAMPLE version=2 ...` line.

Analyze the v2 metrics first. If the path is working, resume the independent 10-receipt campaign with v2 only. Earlier v1 samples remain diagnostic evidence and do not count toward the final 10.

## 7. Privacy

Do not upload or commit real receipt images, OCR text, merchant/product values, dates, prices, IDs, paths, private DBs/backups, or credentials.

## 8. Stop condition

No further OCR/structure/review-policy change before the first v2 physical report is analyzed.
