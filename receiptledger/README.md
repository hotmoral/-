# ReceiptLedger public execution namespace

ReceiptLedger is a personal purchase-price memory and comparison system. This namespace contains public-safe Android/OCR implementation, validation, CI and debug evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP37_PARTIAL_ROW_PREFILL_REMEDIATION_CLOSEOUT.md`
4. `CP37_PARTIAL_ROW_PREFILL_REMEDIATION_EVIDENCE.md`
5. `CP37_PARTIAL_ROW_PREFILL_REMEDIATION_PLAN.md`
6. `CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_CLOSEOUT.md`
7. `CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_EVIDENCE.md`
8. `CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
9. `CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
10. `CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
11. `PRODUCT_REBASELINE_V1_ROADMAP.md`
12. `WORK_UNIT.md`

GitHub is canonical. Verify current docs-only handoff and frozen executable separately.

## Current boundary

V1 CP20–CP36: **COMPLETE**.

Post-V1 CP37: **IN PROGRESS**.

Current state: **Remediation C — READY_FOR_PHYSICAL_PREFILL_RETEST**.

- branch `receiptledger/run-post-v1-partial-row-prefill-20261017`
- predecessor handoff `d4f75d8120e4a9c347b3777c64b511e4f5d224d4`
- frozen executable `01b22652a45889b6bfaa474131e0c5fa7f19e96e`
- Actions `38979684033` SUCCESS
- job `117237351555`
- artifact `12080029714`
- digest `sha256:55300e9525851f02232dc03f9a528fcd5b3c9c30ba68e7a30eb0bdb6634d46c2`
- APK SHA-256 `65fe0827f3a9ebfeafbbf783c6c8f82544f8594203008692288ab74ec9eb1e0e`
- version `1.0.38-partial-row-prefill-validation` / 39
- debug app `com.receiptledger.v1.rowrecovery`
- label `ReceiptLedger 검증 C`

## What Remediation C does

If OCR misses the quantity token but a row has one unambiguous printed unit-price candidate and a printed line amount whose ratio is an exact quantity from 1 to 99, the app pre-fills quantity and unit price.

The item deliberately remains `PARTIAL` and review-required. Ambiguous/non-integral cases remain unresolved.

This reduces unnecessary retyping without weakening the review boundary.

## What it does not do

- no OCR model change;
- no preprocessing/recovery change;
- no generic text substitution;
- no change to the Remediation A false-item gate;
- no change to selective-review policy;
- no schema/identity/price/search change.

The observed package-suffix character confusion remains tracked as physical evidence only.

## Next physical step

Install `ReceiptLedger 검증 C` side by side and process the same receipt once more.

Verify that the first item quantity and unit price are prefilled **and** that the item still appears in explicit review. Then visually verify/correct all fields, save, and return only the generated `RL_CP37_SAMPLE version=2 ...` line.

Do not count this repeated diagnostic receipt toward the final independent 10-receipt campaign.

## Privacy

Never commit/share publicly real receipt photos, OCR text, merchant/product names, dates, prices, IDs, file paths, private DBs/backups, credentials or signing material.

## Stop condition

**Do not start the independent 10-receipt campaign until the Remediation C same-receipt retest is analyzed.**
