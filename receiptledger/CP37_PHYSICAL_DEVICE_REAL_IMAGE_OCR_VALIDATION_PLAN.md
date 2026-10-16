# ReceiptLedger Post-V1 — CP37 Physical Device / Real-Image OCR Validation Plan

Updated: 2026-10-17 KST
Checkpoint: **CP37 — Physical Device / Real-Image OCR Validation**
Status: **AUTHORIZED / PHASE A PREPARATION**

## 1. Canonical predecessor

- current handoff predecessor: `d0a3a9ec7658808c82247715d58ac106a3778186`
- frozen CP36 executable: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- CP36 canonical Actions: `38926526457` — SUCCESS
- branch: `receiptledger/run-post-v1-physical-ocr-validation-20261017`

CP36 executable behavior is the comparison baseline. CP37 must not reinterpret CP36 emulator numbers as physical-device certification.

## 2. Why CP37 exists

Two material evidence gaps remain after V1:

1. CP35's public receipt corpus starts at synthetic `OcrDocument` token/geometry input, so real-image ML Kit accuracy was never measured.
2. CP36 measured reproducible warm OCR latency around 4 seconds on an API 34 x86_64 CI emulator, but deliberately did not change OCR because physical-device speed and real-image accuracy were unknown.

The cheapest next step is therefore physical-device real-image measurement before any OCR redesign, downsampling or pass-policy change.

## 3. Governing objective

Measure the existing frozen OCR/recovery/capture path on a physical Android device with real receipt images while keeping private receipt content local to the device.

CP37 answers:

- How long does the existing full OCR/recovery path take on the target device?
- How often does it need 1/2/3 OCR passes?
- How often does CP33 request review?
- After the user checks the real receipt, how many receipt/item fields actually require correction before save?
- Does any sample start as `AUTO_CONFIRMED` but still require a user correction?
- Are there crashes, failed saves, duplicate saves or provenance regressions?

## 4. Phase model

### Phase A — Device Validation Instrumentation

Repository work may add only enough debug-only/local instrumentation to produce a sanitized per-receipt report.

Phase A may record:

- acquisition source: CAMERA or GALLERY;
- source image dimensions;
- perspective-corrected flag;
- total OCR/recovery elapsed milliseconds;
- attempted OCR pass count;
- merged/derived candidate count;
- selected recognition pass;
- initial validation status;
- initial CP33 review decision;
- initial item count / review-item count / receipt-field review count;
- whether receipt-level fields changed before final save;
- counts of changed item name / quantity / unit-price / line-amount fields;
- item-count change;
- final validation status;
- save success.

The report must not contain:

- raw OCR text;
- store/merchant name;
- product/item names;
- purchase date;
- receipt ID;
- prices or totals;
- image bytes/path/URI;
- stable product IDs;
- personal identifiers.

No report is uploaded automatically. No network permission is introduced.

### Phase B — Physical Device Campaign

The user processes real receipts with the Phase A debug APK, visually checks every result against the original receipt even when the app says AUTO_CONFIRMED, corrects any wrong fields using the existing review/edit path, saves, then copies the sanitized report into this chat.

Minimum campaign target:

- 10 saved receipt samples;
- at least 3 CAMERA acquisitions when practical;
- at least 3 GALLERY acquisitions;
- at least 3 materially different receipt layouts;
- perspective-corrected samples where detector/capture geometry makes correction appropriate.

Raw receipts and OCR text remain off GitHub.

## 5. Primary reliability rule

A sample that is initially `AUTO_CONFIRMED` but requires any factual receipt/item correction after visual comparison is a **FALSE_AUTO_CONFIRM** and is a blocker-quality trust finding.

CP37 prioritizes correctness over latency. A faster configuration must not be accepted if it worsens real-image correctness or review safety.

## 6. Latency decision rule

The CP36 warm OCR budget of 1,500 ms remains a reference target, not an automatic physical-device pass/fail threshold.

After at least 10 physical samples, report:

- median OCR/recovery latency;
- max latency;
- pass-count distribution;
- CAMERA vs GALLERY observations where enough samples exist.

If physical-device latency is materially high, remediation may be proposed only together with correction-burden evidence. No downsampling/pass reduction is authorized before Phase B results.

## 7. Frozen contracts / non-goals

CP37 Phase A must not change:

- OCR recognition model/options;
- image preprocessing semantics;
- recovery pass decision rules;
- ReceiptRecognitionPipeline;
- item tuple solving;
- CP33 review policy;
- identity authority;
- price/comparability rules;
- product schema 2 or receipt schema 1;
- CP34 shell navigation except a debug-only validation affordance if necessary;
- privacy/permission posture.

Explicitly out of scope before Phase B evidence:

- image downsampling optimization;
- replacing ML Kit;
- changing MAX_PASSES;
- OCR parallelization;
- persistent analytics/telemetry;
- uploading receipts or OCR text;
- release signing;
- new product features.

## 8. Phase A acceptance

Phase A is READY_FOR_DEVICE_EVIDENCE only when:

1. report generation is deterministic and contains no forbidden receipt content;
2. initial-vs-final correction counts are covered by unit tests;
3. OCR elapsed/pass metrics do not alter OCR execution;
4. validation UI is debuggable-build-only or otherwise isolated from future release behavior;
5. product/receipt schemas remain unchanged;
6. forbidden CAMERA/media/storage/network permissions remain absent;
7. full existing regressions and lint remain clean;
8. APK artifact and SHA are recorded;
9. plan/code post-green review finds no authority/provenance regression.

Phase A completion does **not** close CP37.

## 9. Phase B acceptance / decision outcomes

After physical reports are supplied, CP37 must classify the result as one of:

- `PASS_NO_OCR_CHANGE`: no material correctness/safety defect and latency acceptable for the observed device/corpus;
- `REMEDIATION_REQUIRED`: measured real-image correctness/review/latency evidence justifies a bounded OCR change;
- `INSUFFICIENT_EVIDENCE`: corpus or report count is too small/incomplete to decide.

Any remediation requires its own measurement-preserving before/after comparison on the same physical corpus where practical.

## 10. Stop condition

Phase A stops after producing and validating the physical-device validation APK. Then wait for the user's real-device reports before altering OCR behavior.
