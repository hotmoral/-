# ReceiptLedger — CP37 Partial Row Prefill Remediation C Evidence

Updated: 2026-10-17 KST

## Canonical execution evidence

- executable SHA: `01b22652a45889b6bfaa474131e0c5fa7f19e96e`
- Actions run: `38979684033`
- job: `117237351555`
- conclusion: SUCCESS
- artifact: `12080029714`
- artifact digest: `sha256:55300e9525851f02232dc03f9a528fcd5b3c9c30ba68e7a30eb0bdb6634d46c2`
- APK SHA-256: `65fe0827f3a9ebfeafbbf783c6c8f82544f8594203008692288ab74ec9eb1e0e`

## Test evidence

- `ItemTupleSolverTest`: 4 tests, 0 failures/errors/skips
- `CaptureReviewUxV2Test`: 14 tests, 0 failures/errors/skips
- `DeviceValidationReportV1Test`: 8 tests, 0 failures/errors/skips
- full unit regression: PASS
- Android lint: exact `No issues found.`

Canonical metric:

`CP37_PARTIAL_PREFILL_METRICS version=1 item_tuple_tests=4 capture_review_tests=14 report_v2_tests=8 unique_integer_prefill=1 ambiguous_rejected=1 partial_review_preserved=1 report_v2_unchanged=1 schema_unchanged=1`

## Artifact identity

- package: `com.receiptledger.v1.rowrecovery`
- label: `ReceiptLedger 검증 C`
- FileProvider authority: `com.receiptledger.v1.rowrecovery.capture`
- versionName: `1.0.38-partial-row-prefill-validation`
- versionCode: 39
- signing: debug only

Packaged permissions contain only the generated non-exported dynamic receiver permission. Forbidden CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE permissions are absent.

## Diff boundary

Predecessor handoff `d4f75d8120e4a9c347b3777c64b511e4f5d224d4` -> executable `01b22652a45889b6bfaa474131e0c5fa7f19e96e` changes exactly seven files:

1. CP37 Partial Row Prefill plan;
2. branch-specific validation workflow;
3. debug version/package configuration;
4. debug app label;
5. `ItemTupleSolver.java`;
6. `ItemTupleSolverTest.java`;
7. `CaptureReviewUxV2Test.java`.

The only production behavior source changed is `ItemTupleSolver.java`.

## Safety evidence

The new deterministic vectors prove:

- equal printed unit/line values can prefill quantity 1;
- another exact integer ratio can prefill a larger quantity;
- the resulting row remains `PARTIAL`;
- arithmetic quantity provenance is retained;
- non-integral ratios remain unresolved;
- multiple valid unit candidates remain unresolved as ambiguous;
- a fully populated PARTIAL row still requires explicit review;
- report v2 and selective-review metrics are unchanged.

## Evidence limitations

This evidence does not prove the physical receipt is fixed. It proves only the deterministic production logic and regression boundary. Physical confirmation with the same receipt is still required.

It also does not claim correction of the observed package-suffix OCR character confusion. No literal OCR substitution was added.
