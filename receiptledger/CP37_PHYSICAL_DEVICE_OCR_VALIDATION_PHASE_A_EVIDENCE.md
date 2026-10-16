# ReceiptLedger Post-V1 — CP37 Phase A Evidence

Updated: 2026-10-17 KST
Checkpoint: CP37 Phase A
Canonical executable HEAD: `9bb5dcc276fae4632ade5ac3134e586baad65235`

## 1. Canonical CI identity

- workflow: `ReceiptLedger Post-V1 Physical OCR Validation`
- run: `38950400666`
- conclusion: SUCCESS
- job: `117140033593`
- artifact ID: `12068811009`
- artifact name: `receiptledger-post-v1-physical-ocr-validation-38950400666`
- artifact digest: `sha256:86d3861727db107e26edf4073666e010f59249ac746496524f6007ca09787697`

## 2. APK identity

- versionName: `1.0.35-physical-ocr-validation`
- versionCode: 36
- signing: debug only
- APK SHA-256: `f9e5b73db79043a6fc6f76f3381e0e2fdab164b7b53c59d8b9ce405d1147120f`
- lint: `No issues found.`
- product schema: 2 unchanged
- receipt schema: 1 unchanged
- OCR engine: unchanged
- recovery policy: unchanged

## 3. Artifact metric

`CP37_PHASE_A_METRICS report_version=1 tests=4 privacy_leak_tests=1 false_auto_confirm_tests=1 conservative_review_tests=1 structure_delta_tests=1 schema_unchanged=1`

`DEVICE_VALIDATION_REPORT_V1_TEST.xml`:

- tests: 4
- failures: 0
- errors: 0
- skipped: 0

## 4. Sanitized report v1 contract

The copied report has this structural form:

`RL_CP37_SAMPLE version=1 source=GALLERY image_w=... image_h=... perspective=0 ocr_ms=... attempted_passes=... merged_candidates=... best_pass=ORIGINAL initial_validation=PASS initial_decision=AUTO_CONFIRMED initial_items=... initial_review_items=... initial_review_fields=... store_changed=0 date_changed=0 total_changed=0 discount_changed=0 item_count_changed=0 item_structure_changes=0 item_name_changes=0 item_quantity_changes=0 item_unit_price_changes=0 item_line_amount_changes=0 any_correction=0 false_auto_confirm=0 final_validation=PASS saved=1`

It contains no source receipt values.

## 5. Privacy evidence

Unit tests use deliberately distinctive private-like sentinel values and assert the report does not contain receipt ID, store, item name, date, raw OCR text or price/total values.

The implementation emits only enums, dimensions, durations, counts and booleans. No report persistence or network upload exists.

`aapt dump permissions` contains only:

- `com.receiptledger.v1.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

Absent:

- CAMERA;
- READ_MEDIA_IMAGES;
- READ_EXTERNAL_STORAGE;
- WRITE_EXTERNAL_STORAGE;
- MANAGE_EXTERNAL_STORAGE;
- INTERNET;
- ACCESS_NETWORK_STATE.

## 6. Debug-only isolation evidence

`MainActivity` only creates the `검증 결과 복사` control when `ApplicationInfo.FLAG_DEBUGGABLE` is present.

`DeviceValidationReportV1.captureInitial(...)` is additionally gated by generated `BuildConfig.DEBUG`; `buildFeatures { buildConfig true }` is explicitly enabled for that purpose.

Report construction is attempted only after `repository.save(...)` succeeds and is wrapped so instrumentation failure cannot alter durable-save success.

## 7. Timing boundary

The CP37 OCR timer starts immediately before the pre-existing `OcrRecoveryEngine.recognize(...)` call and stops in its final success callback.

Thus `ocr_ms` measures the existing full OCR/recovery operation including extra recovery passes when triggered. Image loading, camera launch, picker time and document detection are not folded into this number.

No OCR option, recognizer lifetime, pass ordering, preprocessing or candidate selection was changed.

## 8. Scope evidence

Compared with predecessor handoff `d0a3a9ec...`, Phase A changes are limited to:

- one CP37 workflow;
- three CP37 plan/protocol/consistency Markdown files;
- app version/buildConfig declaration;
- MainActivity's local validation bridge;
- `DeviceValidationReportV1`;
- `DeviceValidationReportV1Test`;
- two CP37 UI strings.

No manifest, OCR package, recovery package or review package diff is allowed by the workflow guard.

## 9. Evidence limitation

Phase A proves only that the validation build and privacy/reporting mechanism are ready. It does **not** prove real-image OCR correctness, physical-device latency, review burden or absence of false auto-confirmation.

Those claims require Phase B physical-device samples.

## 10. Conclusion

CP37 Phase A is **READY_FOR_DEVICE_EVIDENCE**. Full CP37 remains open pending physical-device / real-image reports.
