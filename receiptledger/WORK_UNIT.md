# ReceiptLedger public execution work unit

Updated: 2026-10-17 KST

## Current stage

**CP37 — Physical Device / Real-Image OCR Validation**

Current substage: **Phase A READY_FOR_DEVICE_EVIDENCE / Phase B PENDING**

- branch: `receiptledger/run-post-v1-physical-ocr-validation-20261017`
- predecessor CP36 handoff: `d0a3a9ec7658808c82247715d58ac106a3778186`
- frozen CP37 Phase A executable: `9bb5dcc276fae4632ade5ac3134e586baad65235`
- canonical Actions: `38950400666` — SUCCESS
- job: `117140033593`
- artifact ID: `12068811009`
- artifact digest: `sha256:86d3861727db107e26edf4073666e010f59249ac746496524f6007ca09787697`
- APK SHA-256: `f9e5b73db79043a6fc6f76f3381e0e2fdab164b7b53c59d8b9ce405d1147120f`
- versionCode 36
- versionName `1.0.35-physical-ocr-validation`
- lint: 0 errors / 0 warnings

**Do not label CP37 complete yet.**

## Phase A frozen result

Phase A added only a privacy-safe, debug-only measurement layer around the existing OCR/recovery/review/save path.

Canonical metric:

`CP37_PHASE_A_METRICS report_version=1 tests=4 privacy_leak_tests=1 false_auto_confirm_tests=1 conservative_review_tests=1 structure_delta_tests=1 schema_unchanged=1`

No OCR model/options/preprocessing/recovery rule or CP33 review rule changed. Product schema 2 / receipt schema 1 remain unchanged.

## Phase B work unit

The next work is **evidence collection, not coding**.

Minimum target: 10 successfully saved real receipts.

Desired coverage when practical:

- >=3 CAMERA;
- >=3 GALLERY;
- >=3 materially different receipt layouts;
- short/long receipts mixed if naturally available;
- perspective correction where warranted.

## Per-sample procedure

1. Install the canonical CP37 validation APK.
2. Open `영수증 추가`.
3. Acquire a real receipt via camera or gallery.
4. Let OCR/recovery finish.
5. Compare every recognized field against the original receipt, even for AUTO_CONFIRMED.
6. Correct all factual errors using existing review/full-edit flow.
7. Save once correct.
8. Tap `검증 결과 복사`.
9. Return only the generated `RL_CP37_SAMPLE ...` line to the planning chat.

Do not return receipt photos, OCR text or purchase values unless separately and privately authorized.

## Decision metrics after >=10 samples

Aggregate:

- sample count;
- CAMERA/GALLERY counts;
- OCR median/max latency;
- attempted-pass distribution;
- AUTO_CONFIRMED / REVIEW_REQUIRED counts;
- `false_auto_confirm` count;
- receipt-field correction totals;
- item structure/name/quantity/unit-price/line-amount correction totals;
- crashes/OCR hangs/save failures/duplicates.

## Decision rule

Priority order:

1. correctness / false-auto-confirm safety;
2. save/provenance reliability;
3. review burden;
4. latency.

`false_auto_confirm=1` is blocker-quality evidence.

Final CP37 outcome must be one of:

- PASS_NO_OCR_CHANGE;
- REMEDIATION_REQUIRED;
- INSUFFICIENT_EVIDENCE.

No downsampling, pass reduction, recognizer replacement or other OCR optimization is authorized before this evidence is analyzed.

## Group discipline

- recover canonical refs first;
- compare physical evidence against the frozen Phase A build only;
- do not mix APK versions;
- catch material inconsistencies before remediation;
- avoid speculative optimization or unrelated UI/domain changes;
- if remediation is justified, define a new bounded implementation/evidence boundary before coding;
- maintain docs-only handoff discipline for new sessions.

## Public/privacy rules

Only sanitized report lines and aggregate metrics may become public evidence. Never commit real receipts, OCR text, real DBs/backups, credentials or signing material.

## Stop condition

**Wait for user-supplied Phase B sanitized reports.**
