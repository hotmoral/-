# ReceiptLedger — Project Status Latest

Updated: 2026-10-17 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current boundary

Planned V1 CP20–CP36 is complete.

Post-V1 **CP37 — Physical Device / Real-Image OCR Validation** is open.

Current state:

**Selective Review Coverage Instrumentation — READY_FOR_PHYSICAL_METRIC_CHECK**

CP37 itself is **NOT COMPLETE**. The independent 10-receipt campaign remains paused until one physical report verifies the new v2 metrics.

### Active refs

- active branch: `receiptledger/run-post-v1-selective-review-coverage-20261017`
- predecessor Remediation A handoff: `c4e00ff22339869346f0f8692e38d82567568b7e`
- frozen Remediation A executable: `06fafa9db1da0e4592ddc15a468a9c6e4e338515`
- frozen review-coverage executable: `7dbed4cf73a2963ace7447974e9d972a9776b79f`
- canonical Actions: `38976080450` — SUCCESS
- canonical job: `117225743973` — SUCCESS
- artifact ID: `12078898591`
- artifact digest: `sha256:402a5dda9d0892550ff08d5a5f3dbeb228a01a6f32abc40d24f8a75efa510b67`
- APK SHA-256: `29fcd2073d74fee819d53525bf2409db1587a72e72e86af115496843562405b8`
- version: `1.0.37-review-coverage-validation` / versionCode 38
- debug applicationId: `com.receiptledger.v1.reviewcoverage`
- label: `ReceiptLedger 검증 B`
- lint: 0 errors / 0 warnings

## 2. Physical findings so far

### Initial Phase B sample

A real GALLERY receipt produced REVIEW_REQUIRED rather than false auto-confirm, but a spatially separate address/header row was incorrectly included as an item. Review UI could not remove the false item. This triggered Remediation A.

### Remediation A physical retest

Using the remediated build, the previously false address row was **not classified as an item**. Therefore the narrow `ITEM_BEFORE_DATE_WITH_BODY_BELOW` structure gate is physically confirmed for the defect that triggered it.

The retest sanitized metrics included:

- GALLERY, 1080x2316;
- OCR 328ms;
- attempted passes 1;
- initial PASS_WITH_WARNINGS / REVIEW_REQUIRED;
- initial items 15;
- initial review items 1;
- item name changes 3;
- item quantity changes 1;
- item unit-price changes 1;
- false_auto_confirm=0;
- final PASS_WITH_WARNINGS / saved.

This exposed a separate evidence gap: the v1 report could not tell how many corrected items were outside the initially selected review set.

## 3. Review coverage instrumentation

The sanitized report is now `version=2` and adds:

- `corrections_outside_review_items=N`
- `review_scope_miss=0|1`

The count is by distinct item ordinal, not corrected field count. An item is outside scope when it was not in the initial `CaptureReviewAssessmentV2.itemOrdinals` but was later edited, removed or added.

Receipt-level STORE/DATE/TOTAL/DISCOUNT fields are intentionally excluded from this metric.

## 4. Validation result

Canonical metric:

`CP37_REVIEW_COVERAGE_METRICS report_version=2 tests=8 outside_scope_detection=1 in_scope_control=1 distinct_item_counting=1 removal_detection=1 privacy_preserved=1 product_behavior_unchanged=1 schema_unchanged=1`

- report tests: 8/8 PASS
- full unit regression: PASS
- lint: `No issues found.`
- APK build: PASS
- side-by-side package/provider/label checks: PASS
- forbidden camera/media/storage/network permissions: absent

## 5. Frozen product behavior

This instrumentation does **not** change:

- ML Kit OCR model/options;
- OCR preprocessing/recovery pass policy;
- Remediation A false-item structure gate;
- CP33 selective-review policy;
- explicit false-item removal behavior;
- stable-ID identity authority;
- commodity/price/search semantics;
- product schema 2 / receipt schema 1;
- offline/privacy permission posture.

## 6. Exact next action

Install `ReceiptLedger 검증 B` side by side. Process one real receipt, visually inspect every field, correct all factual errors, save, and return only the generated:

`RL_CP37_SAMPLE version=2 ...`

This first v2 sample is a metric-path verification sample. Analyze `corrections_outside_review_items` and `review_scope_miss` before resuming the independent 10-receipt campaign.

Earlier v1 diagnostic/remediation samples are evidence but do **not** count toward the final 10.

## 7. Stop condition

Do not change OCR, structure gating or review selection again before the v2 physical metric check is analyzed.

## 8. Canonical restart order

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

GitHub is canonical. Verify docs-only handoff HEAD and frozen executable separately.
