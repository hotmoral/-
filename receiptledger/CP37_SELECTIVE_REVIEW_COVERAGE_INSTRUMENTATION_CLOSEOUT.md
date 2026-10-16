# ReceiptLedger CP37 — Selective Review Coverage Instrumentation Closeout

Updated: 2026-10-17 KST

## Status

**PASS / READY_FOR_PHYSICAL_METRIC_CHECK**

CP37 itself remains open. This checkpoint changes validation instrumentation only; it does not change product review policy.

## Trigger

Remediation A physical retest confirmed the false address/header item was no longer emitted. The same retest reported:

- initial_items=15
- initial_review_items=1
- item_name_changes=3
- item_quantity_changes=1
- item_unit_price_changes=1
- false_auto_confirm=0

This proved the receipt was not falsely auto-confirmed, but the v1 report could not quantify whether corrected item ordinals were outside the initial selective-review set.

## Frozen executable

- branch: `receiptledger/run-post-v1-selective-review-coverage-20261017`
- predecessor handoff: `c4e00ff22339869346f0f8692e38d82567568b7e`
- frozen executable: `7dbed4cf73a2963ace7447974e9d972a9776b79f`
- Actions: `38976080450` — SUCCESS
- job: `117225743973` — SUCCESS
- artifact ID: `12078898591`
- artifact digest: `sha256:402a5dda9d0892550ff08d5a5f3dbeb228a01a6f32abc40d24f8a75efa510b67`
- APK SHA-256: `29fcd2073d74fee819d53525bf2409db1587a72e72e86af115496843562405b8`
- version: `1.0.37-review-coverage-validation` / versionCode 38
- debug package: `com.receiptledger.v1.reviewcoverage`
- label: `ReceiptLedger 검증 B`
- lint: `No issues found.`

## Instrumentation change

The sanitized report is extended to `version=2` with:

- `corrections_outside_review_items=N`
- `review_scope_miss=0|1`

`corrections_outside_review_items` counts distinct item ordinals that were not in the initial `CaptureReviewAssessmentV2.itemOrdinals` but later experienced any item-field correction or item structural add/remove. Multiple corrected fields on one ordinal count once.

`review_scope_miss=1` iff that count is greater than zero.

Receipt-level STORE/DATE/TOTAL/DISCOUNT corrections are intentionally not included in this metric.

## Tests

Canonical metric:

`CP37_REVIEW_COVERAGE_METRICS report_version=2 tests=8 outside_scope_detection=1 in_scope_control=1 distinct_item_counting=1 removal_detection=1 privacy_preserved=1 product_behavior_unchanged=1 schema_unchanged=1`

Device validation report suite: **8/8 PASS**.

The suite covers:

- unchanged control;
- false-auto-confirm correction;
- conservative review control;
- structural replacement;
- removal already inside review scope;
- REVIEW_REQUIRED correction outside selected item scope;
- correction inside selected item scope;
- removal outside review scope.

## Frozen product behavior

Unchanged from Remediation A:

- ML Kit OCR model/options;
- OCR recovery preprocessing/pass policy;
- false-item structure gate;
- selective-review policy itself;
- explicit `상품이 아님` item-removal behavior;
- identity/price/search semantics;
- product schema 2 / receipt schema 1;
- permission posture.

## Physical next step

Install `ReceiptLedger 검증 B` side by side. Process one real receipt and return only its `RL_CP37_SAMPLE version=2 ...` line after visually checking and correcting every field.

The first v2 report is a metric-path verification sample. After it is analyzed, resume the independent 10-receipt CP37 campaign. Earlier v1 diagnostic/remediation samples are not counted toward the final 10.
