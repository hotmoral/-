# ReceiptLedger CP37 — Selective Review Coverage Instrumentation Evidence

Updated: 2026-10-17 KST

## Canonical execution evidence

- frozen executable: `7dbed4cf73a2963ace7447974e9d972a9776b79f`
- Actions run: `38976080450` — SUCCESS
- job: `117225743973` — SUCCESS
- artifact: `12078898591`
- artifact digest: `sha256:402a5dda9d0892550ff08d5a5f3dbeb228a01a6f32abc40d24f8a75efa510b67`
- APK SHA-256: `29fcd2073d74fee819d53525bf2409db1587a72e72e86af115496843562405b8`

## Build identity

- checkpoint: `RL_POST_V1_CP37_REVIEW_COVERAGE_INSTRUMENTATION`
- report version: 2
- versionName: `1.0.37-review-coverage-validation`
- versionCode: 38
- debug applicationId: `com.receiptledger.v1.reviewcoverage`
- label: `ReceiptLedger 검증 B`
- provider authority: `com.receiptledger.v1.reviewcoverage.capture`
- signing: debug only

## Regression / lint

- report suite: 8 tests, 0 failures, 0 errors, 0 skipped
- full debug unit regression: PASS
- Android lint: `No issues found.`
- debug APK build: PASS

Canonical metric:

`CP37_REVIEW_COVERAGE_METRICS report_version=2 tests=8 outside_scope_detection=1 in_scope_control=1 distinct_item_counting=1 removal_detection=1 privacy_preserved=1 product_behavior_unchanged=1 schema_unchanged=1`

## APK privacy / permissions

Packaged permissions contain only the app-internal dynamic receiver permission. The following remain absent:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

The report still exports no receipt text, merchant/product values, dates, prices, IDs, paths or images.

## Scope evidence

Predecessor handoff -> executable changed only:

- new review-coverage plan;
- new review-coverage workflow;
- debug build version/applicationId suffix;
- debug app label;
- `DeviceValidationReportV1` instrumentation;
- `DeviceValidationReportV1Test`.

Frozen product paths including `MainActivity`, OCR, recovery, structure, review policy, identity, price and search were guarded unchanged.

## Metric semantics

`corrections_outside_review_items` is a count of distinct corrected item ordinals outside the initial selected review set. It is not a count of corrected fields.

`review_scope_miss=1` iff at least one such item ordinal exists.

This distinguishes:

- whole-receipt trust failure: `false_auto_confirm=1`;
- selective-review coverage failure: `review_scope_miss=1` while initial decision may still be REVIEW_REQUIRED.

## Evidence limitation

This checkpoint proves deterministic instrumentation behavior and packaging only. It does not yet establish a physical-device review-scope miss rate. That requires the v2 physical campaign.
