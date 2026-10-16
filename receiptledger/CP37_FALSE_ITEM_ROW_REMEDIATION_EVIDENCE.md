# ReceiptLedger CP37 — False Item Row Remediation A Evidence

Updated: 2026-10-17 KST
Status: **READY_FOR_PHYSICAL_RETEST**

## Physical trigger evidence

First CP37 physical sample, sanitized:

- source: GALLERY
- image: 800x1067
- perspective correction: no
- OCR/recovery elapsed: 562 ms
- attempted passes: 3
- merged candidates: 2
- selected pass: ORIGINAL
- initial validation: MISMATCH
- initial decision: REVIEW_REQUIRED
- initial items: 16
- review items: 16
- review receipt fields: 2
- name corrections: 5
- quantity corrections: 0
- unit-price corrections: 1
- line-amount corrections: 1
- false auto-confirm: 0
- final validation: PASS_WITH_WARNINGS
- save: success

The user additionally reported that a spatially separate address/header row had been emitted as a product item. The Phase A review UI could not remove that row. This was classified as a `FALSE_ITEM_ROW` structural/recoverability defect.

No real receipt text, merchant/product values, dates, prices, IDs, images or DB content are recorded here.

## Root-cause evidence

Prior structure classification considered a row an ITEM when a money-like numeric candidate existed and a letter token appeared to its left. It had no item-body continuity guard. Prior review required the edit list to match the original item count and had no explicit removal state.

## Code evidence

Remediation is bounded to:

- `ReceiptStructureAnalyzer` and its tests;
- `ReviewItemInput`;
- `ReceiptReviewEngine`;
- `CaptureReviewAssessmentV2`;
- `ReceiptReviewDialog`;
- review/report tests and validation copy;
- debug-only side-by-side package configuration;
- the remediation workflow and plan.

No OCR/recovery/identity/price/schema implementation changed.

## Canonical execution evidence

- frozen executable: `06fafa9db1da0e4592ddc15a468a9c6e4e338515`
- Actions run: `38957744298`
- job: `117164770764`
- conclusion: SUCCESS
- artifact: `12071212297`
- artifact digest: `sha256:6540c6350ea47280dc3d9fec64cdaef3b2aef24976f833a44e0cb13bd3b2a811`
- APK SHA-256: `109b61603c9f4a0a399ecb919399151427ab3ba243e626bbe8543340a4ee0f3d`

## Packaged APK evidence

AAPT/package inspection:

- package: `com.receiptledger.v1.remediation`
- versionCode: 37
- versionName: `1.0.36-physical-ocr-remediation`
- application label: `ReceiptLedger 검증`
- FileProvider authority: `com.receiptledger.v1.remediation.capture`

Permissions:

- only Android-generated `DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION` was present;
- CAMERA, READ_MEDIA_IMAGES, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET and ACCESS_NETWORK_STATE were absent.

Lint:

`No issues found.`

## Test evidence

- `ReceiptStructureAnalyzerTest`: 5 tests / 0 failures / 0 errors / 0 skipped
- `ReceiptReviewEngineTest`: 5 / 0 / 0 / 0
- `DeviceValidationReportV1Test`: 5 / 0 / 0 / 0

Canonical metric:

`CP37_REMEDIATION_METRICS version=1 structure_tests=5 review_tests=5 report_tests=5 predate_false_item_gate=1 explicit_item_removal=1 provenance_preserved=1 report_structure_delta=1 side_by_side_debug=1 schema_unchanged=1`

## Remaining evidence gap

Synthetic/unit/CI evidence cannot prove that the observed real receipt no longer creates the false row. The same real receipt must therefore be rerun on the frozen remediation APK before declaring this remediation effective.

CP37 remains open.
