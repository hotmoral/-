# CP37 Candidate Structure Diagnostics — Evidence

Updated: 2026-10-17 KST

## Canonical execution

- frozen executable: `3e19741521b9be4039028bcb9981e400ff2ad867`
- Actions run: `38987300764`
- job: `117261641673`
- conclusion: SUCCESS
- artifact ID: `12083716548`
- artifact digest: `sha256:faada9ea2c87874d828e5c57fae9d42ccf4f966056ed6ce68943b33122784432`
- APK SHA-256: `1aa0f2d6ec2510b77a7b273eefd2b037ae8f0207021849c7da81ac054cb125e9`

## Test evidence

- CandidateStructureDiagnosticsV1Test: 4/4 PASS
- CandidateDiagnosticReportIntegrationV1Test: 1/1 PASS
- DeviceValidationReportV1Test: 8/8 PASS
- ItemTupleSolverTest: 4/4 PASS
- CaptureReviewUxV2Test: 14/14 PASS
- full unit regression: PASS
- Android lint: `No issues found.`
- APK build: PASS

Canonical metric:

`CP37_CANDIDATE_DIAG_METRICS version=1 candidate_tests=4 integration_tests=1 report_v2_tests=8 item_tuple_tests=4 capture_review_tests=14 product_zone_quantity_probe=1 privacy_preserved=1 behavior_unchanged=1 schema_unchanged=1`

## Artifact inspection

APK badging:

- package `com.receiptledger.v1.candidateprobe`
- versionName `1.0.39-candidate-diagnostics-validation`
- versionCode 40
- label `ReceiptLedger 검증 D`
- provider authority `com.receiptledger.v1.candidateprobe.capture`

Packaged permissions contain only the Android-generated dynamic receiver not-exported permission. The following remain absent:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

## Diff boundary

Compared with predecessor handoff `99a7de8ba1c83771f11cefd7b6ab47e7d0590f99`, the executable changes are limited to:

- candidate diagnostics workflow;
- candidate diagnostics plan;
- debug version/package/label;
- `CandidateStructureDiagnosticsV1`;
- debug-only publication hook in `ReceiptRecordFactory`;
- diagnostic attachment in `DeviceValidationReportV1`;
- two focused diagnostic tests.

Explicitly unchanged:

- `MainActivity.java`
- `ItemTupleSolver.java`
- `QuantityCandidate.java`
- OCR/recovery implementation
- structure analyzer/gates
- capture review policy
- identity/price/search semantics
- product schema 2 / receipt schema 1

## Privacy evidence

Focused integration tests use synthetic private-marker strings and assert that the emitted report does not contain receipt ID, store, product name, raw OCR, date, or amount values.

The public repository contains no real receipt image or private purchase data.

## Evidence limitation

This checkpoint does not prove the cause of the physical blank-field defect. It only proves that the new diagnostic projection is bounded, privacy-preserving, and behavior-neutral.

Root cause requires the next same-receipt physical `RL_CP37_DIAG` line.
