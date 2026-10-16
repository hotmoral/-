# ReceiptLedger — Project Status Latest

Updated: 2026-10-17 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current boundary

Planned V1 CP20–CP36 is complete.

Current post-V1 checkpoint: **CP37 — Physical Device / Real-Image OCR Validation**.

Current phase: **Phase A — READY_FOR_DEVICE_EVIDENCE**.

Important: **CP37 itself is NOT COMPLETE.** Phase B requires physical-device / real-receipt reports.

- branch: `receiptledger/run-post-v1-physical-ocr-validation-20261017`
- predecessor CP36 handoff: `d0a3a9ec7658808c82247715d58ac106a3778186`
- frozen CP36 executable: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- frozen CP37 Phase A executable: `9bb5dcc276fae4632ade5ac3134e586baad65235`
- canonical Phase A Actions: `38950400666` — SUCCESS
- canonical job: `117140033593` — SUCCESS
- artifact ID: `12068811009`
- artifact digest: `sha256:86d3861727db107e26edf4073666e010f59249ac746496524f6007ca09787697`
- debug APK SHA-256: `f9e5b73db79043a6fc6f76f3381e0e2fdab164b7b53c59d8b9ce405d1147120f`
- version: `1.0.35-physical-ocr-validation` / versionCode 36
- lint: 0 errors / 0 warnings

Any later handoff synchronization must be docs-only. Keep Phase A executable/evidence boundary at `9bb5dcc2...` unless Phase B evidence explicitly justifies a new implementation.

## 2. Product objective

ReceiptLedger remains a **personal purchase-price memory and comparison system**.

Core loop:

`홈 -> 영수증 추가 -> 자동 처리 -> 필요한 항목 확인 -> 저장 -> 검색/탐색 -> 제품/품목 가격기억 -> 영수증 근거`

CP37 does not add a product feature. It validates the unresolved real-image OCR boundary before any OCR optimization.

## 3. Why CP37 follows CP36

CP35's public evaluation begins at synthetic OCR token/geometry input and therefore does not quantify real-image recognition accuracy.

CP36 found warm OCR around 4 seconds on an API34 x86_64 emulator, but deliberately left OCR unchanged because physical-device performance and any accuracy tradeoff from optimization were unknown.

CP37 resolves this evidence gap in two phases:

- Phase A: privacy-safe debug instrumentation — complete;
- Phase B: user-supplied physical-device sanitized samples — pending.

## 4. Phase A result

Phase A adds a debug-only local report around the existing OCR/recovery/review/save path without changing OCR behavior.

Canonical metric:

`CP37_PHASE_A_METRICS report_version=1 tests=4 privacy_leak_tests=1 false_auto_confirm_tests=1 conservative_review_tests=1 structure_delta_tests=1 schema_unchanged=1`

The validation APK records only structural data such as OCR time/pass counts, initial review state and correction counts. It never exports receipt text, store/product values, dates, prices, IDs, paths or images.

## 5. Critical Phase B rule

Every physical receipt must be visually checked against the original **even when initial_decision=AUTO_CONFIRMED**.

If the user makes any factual/structural correction after an initial AUTO_CONFIRMED decision, the report emits:

`false_auto_confirm=1`

Any such sample is a blocker-quality trust finding requiring investigation before CP37 can pass without OCR changes.

## 6. Frozen contracts

Unchanged through Phase A:

- stable catalog ID identity authority;
- commodity grouping != comparability;
- CP27 comparison eligibility;
- CP28 evaluation thresholds;
- CP29 discovery meaning;
- CP30–34 UI/review/navigation contracts;
- CP35 registration-safety conclusions;
- CP36 bounded search optimization;
- ML Kit recognition model/options;
- OCR recovery preprocessing/pass order/MAX_PASSES;
- product schema 2 / receipt schema 1;
- no broad storage/media/network permissions.

## 7. Phase B campaign target

Use only the canonical CP37 validation APK.

Minimum target:

- 10 successfully saved real receipt samples;
- aim for >=3 CAMERA and >=3 GALLERY samples;
- aim for >=3 materially different receipt layouts.

For each sample: process -> visually inspect all fields -> correct factual errors -> save -> tap `검증 결과 복사` -> return only the sanitized `RL_CP37_SAMPLE ...` line.

Do not upload real receipt photos, OCR text, store/product names, dates, prices, IDs or DB backups to GitHub.

## 8. Current stop condition

**Wait for Phase B physical-device evidence. Do not optimize/downsample/change OCR before those reports are analyzed.**

## 9. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
4. `receiptledger/CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_EVIDENCE.md`
5. `receiptledger/CP37_PHYSICAL_DEVICE_REAL_IMAGE_OCR_VALIDATION_PLAN.md`
6. `receiptledger/PHYSICAL_DEVICE_OCR_VALIDATION_CONSISTENCY_REVIEW.md`
7. `receiptledger/CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
8. `receiptledger/CP36_PERFORMANCE_RELIABILITY_CLOSEOUT.md`
9. `receiptledger/CP36_PERFORMANCE_RELIABILITY_EVIDENCE.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify current docs-only handoff HEAD and frozen Phase A executable separately.
