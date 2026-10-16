# ReceiptLedger public execution namespace

ReceiptLedger is a personal purchase-price memory and comparison system. This namespace contains public-safe Android/OCR implementation, validation, CI and debug evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_CLOSEOUT.md`
4. `CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_EVIDENCE.md`
5. `CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_PLAN.md`
6. `CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
7. `CP37_FALSE_ITEM_ROW_REMEDIATION_EVIDENCE.md`
8. `CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
9. `CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
10. `PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `WORK_UNIT.md`

GitHub is canonical. Verify current docs-only handoff and frozen executable separately.

## Current boundary

V1 CP20–CP36: **COMPLETE**.

Post-V1 CP37: **IN PROGRESS**.

Current state: **Selective Review Coverage Instrumentation — READY_FOR_PHYSICAL_METRIC_CHECK**.

- branch `receiptledger/run-post-v1-selective-review-coverage-20261017`
- predecessor handoff `c4e00ff22339869346f0f8692e38d82567568b7e`
- frozen executable `7dbed4cf73a2963ace7447974e9d972a9776b79f`
- Actions `38976080450` SUCCESS
- job `117225743973`
- artifact `12078898591`
- digest `sha256:402a5dda9d0892550ff08d5a5f3dbeb228a01a6f32abc40d24f8a75efa510b67`
- APK SHA-256 `29fcd2073d74fee819d53525bf2409db1587a72e72e86af115496843562405b8`
- version `1.0.37-review-coverage-validation` / 38
- debug app `com.receiptledger.v1.reviewcoverage`
- label `ReceiptLedger 검증 B`

## Why report v2 exists

Remediation A physically fixed the triggering address/header false-item sample. The retest was REVIEW_REQUIRED but full visual comparison still found multiple item corrections while only one item had been initially selected for review.

Report v2 therefore adds item-level review coverage metrics without changing the review policy:

- `corrections_outside_review_items=N`
- `review_scope_miss=0|1`

A distinct corrected item ordinal counts once regardless of how many of its fields changed.

## Next physical step

Install `ReceiptLedger 검증 B` side by side, process one real receipt, visually verify all fields, correct everything necessary, save, and return only the generated `RL_CP37_SAMPLE version=2 ...` line.

After confirming the metric path, use v2 for the independent 10-receipt campaign. Earlier v1 reports are diagnostic evidence only and do not count toward the final 10.

## Privacy

Never commit/share public real receipt photos, OCR text, merchant/product names, dates, prices, IDs, file paths, private DBs/backups, credentials or signing material.

The validation report emits structural counts/flags only.

## Stop condition

**No further OCR, structure or review-policy implementation until the first v2 physical report is analyzed.**
