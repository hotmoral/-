# ReceiptLedger Post-V1 — CP37 Phase A Closeout

Updated: 2026-10-17 KST
Checkpoint: **CP37 — Physical Device / Real-Image OCR Validation**
Phase: **A — Device Validation Instrumentation**
Status: **READY_FOR_DEVICE_EVIDENCE — CP37 NOT COMPLETE**

## 1. Frozen Phase A execution boundary

- branch: `receiptledger/run-post-v1-physical-ocr-validation-20261017`
- predecessor CP36 handoff: `d0a3a9ec7658808c82247715d58ac106a3778186`
- predecessor CP36 frozen executable: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- frozen CP37 Phase A executable HEAD: `9bb5dcc276fae4632ade5ac3134e586baad65235`
- canonical Actions run: `38950400666` — SUCCESS
- canonical job: `117140033593` — SUCCESS
- artifact ID: `12068811009`
- artifact digest: `sha256:86d3861727db107e26edf4073666e010f59249ac746496524f6007ca09787697`
- debug APK SHA-256: `f9e5b73db79043a6fc6f76f3381e0e2fdab164b7b53c59d8b9ce405d1147120f`
- version: `1.0.35-physical-ocr-validation` / versionCode 36
- lint: `No issues found.`

Any later Phase A handoff synchronization is documentation-only. Do not move the executable boundary from `9bb5dcc2...` without a new implementation decision.

## 2. Why Phase A exists

CP35 validated downstream receipt-registration semantics from synthetic OCR token/geometry input. CP36 measured repeatable warm OCR latency on an x86_64 emulator but deliberately did not trade recognition correctness for emulator speed.

CP37 Phase A prepares a privacy-safe physical-device measurement path before any OCR optimization.

## 3. What Phase A added

A debug-only local validation layer records only structural metrics around the existing capture/review/save path:

- CAMERA/GALLERY acquisition source;
- source image dimensions and perspective flag;
- full `OcrRecoveryEngine.recognize(...)` elapsed time;
- attempted OCR passes, merged candidates and selected pass;
- initial validation / CP33 review decision;
- initial item/review counts;
- receipt/item correction counts between the initial OCR record and final reviewed record;
- `any_correction` and `false_auto_confirm` flags;
- final validation and durable-save success.

After a successful save, a debuggable build exposes `검증 결과 복사`. It copies one sanitized `RL_CP37_SAMPLE ...` line to the clipboard.

## 4. Privacy and release isolation

The report never serializes:

- OCR text;
- store/product names;
- purchase dates;
- prices/totals;
- receipt/product IDs;
- file paths/URIs;
- image bytes.

There is no automatic upload and no network permission.

The validation button is debuggable-only. The initial validation snapshot is also gated by generated `BuildConfig.DEBUG`, so a non-debug build does not retain the CP37 initial receipt snapshot.

## 5. Frozen behavior preserved

Phase A does **not** change:

- ML Kit recognizer/model/options;
- OCR preprocessing;
- recovery pass ordering / `MAX_PASSES`;
- `ReceiptRecognitionPipeline`;
- item tuple solving;
- CP33 review policy;
- identity/category/commodity/price/search/detail semantics;
- product schema 2 / receipt schema 1;
- manifest permissions;
- save authority or provenance.

Validation report construction happens only after durable save and is isolated so report failure cannot turn a successful receipt save into failure.

## 6. Test / regression result

Canonical artifact confirms:

- `DeviceValidationReportV1Test`: 4/4 PASS, 0 failure/error/skip;
- privacy-leak assertion coverage;
- false-auto-confirm detection coverage;
- conservative-review/no-correction coverage;
- item-structure delta coverage;
- existing CP27–35 key regression suites required by workflow;
- full unit regression / APK build PASS;
- lint 0 errors / 0 warnings;
- forbidden CAMERA/media/storage/network permissions absent.

Canonical metric:

`CP37_PHASE_A_METRICS report_version=1 tests=4 privacy_leak_tests=1 false_auto_confirm_tests=1 conservative_review_tests=1 structure_delta_tests=1 schema_unchanged=1`

## 7. Post-green corrections before freeze

Phase A was not frozen on the first green run.

- Run #1 succeeded, then post-green review found the campaign protocol omitted three actual report keys (`item_structure_changes`, `any_correction`, `false_auto_confirm`). The protocol was corrected.
- Run #2 succeeded, then static review found the initial validation snapshot would still be retained in non-debug builds even though the UI/report were debug-only. The snapshot was explicitly gated to debug builds.
- Run #3 failed to compile because this AGP configuration did not generate `BuildConfig`; `buildFeatures { buildConfig true }` was added solely to make the debug boundary explicit.
- Run #4 is the canonical all-green Phase A run.

## 8. Phase B campaign

CP37 is **not complete**. The next action is physical-device evidence collection using this exact debug APK.

Minimum target:

- 10 successfully saved real receipt samples;
- aim for at least 3 CAMERA and 3 GALLERY samples;
- at least 3 materially different receipt layouts where practical.

For every sample, visually inspect the recognized result against the actual receipt even if the app says AUTO_CONFIRMED, correct every factual error, save, tap `검증 결과 복사`, and return only the sanitized `RL_CP37_SAMPLE ...` line.

`false_auto_confirm=1` is a blocker-quality trust finding and must be investigated before PASS.

## 9. Stop condition

**CP37 Phase A is READY_FOR_DEVICE_EVIDENCE. Do not change OCR behavior until Phase B real-device reports are supplied and analyzed.**
