# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
4. `CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_EVIDENCE.md`
5. `CP37_PHYSICAL_DEVICE_REAL_IMAGE_OCR_VALIDATION_PLAN.md`
6. `PHYSICAL_DEVICE_OCR_VALIDATION_CONSISTENCY_REVIEW.md`
7. `CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
8. `CP36_PERFORMANCE_RELIABILITY_CLOSEOUT.md`
9. `CP36_PERFORMANCE_RELIABILITY_EVIDENCE.md`
10. `PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `WORK_UNIT.md`

GitHub is canonical. Verify the current docs-only handoff HEAD and frozen executable ref separately before using old chat context.

## Current boundary

V1 CP20–CP36: **COMPLETE**.

Post-V1 CP37: **IN PROGRESS**.

**CP37 Phase A — READY_FOR_DEVICE_EVIDENCE**

- branch `receiptledger/run-post-v1-physical-ocr-validation-20261017`
- predecessor handoff `d0a3a9ec7658808c82247715d58ac106a3778186`
- frozen Phase A executable `9bb5dcc276fae4632ade5ac3134e586baad65235`
- canonical Actions `38950400666` — SUCCESS
- job `117140033593`
- artifact ID `12068811009`
- artifact digest `sha256:86d3861727db107e26edf4073666e010f59249ac746496524f6007ca09787697`
- APK SHA-256 `f9e5b73db79043a6fc6f76f3381e0e2fdab164b7b53c59d8b9ce405d1147120f`
- version `1.0.35-physical-ocr-validation`, versionCode 36
- lint `No issues found.`

CP37 is **not complete** until physical-device / real-image evidence is analyzed.

## What the validation APK does

The normal ReceiptLedger product flow remains intact. In a debuggable build, after a successful receipt save it additionally exposes `검증 결과 복사`.

That copies one sanitized line describing:

- acquisition source;
- image dimensions/perspective flag;
- OCR/recovery elapsed time and pass counts;
- initial validation/review state;
- correction counts made before save;
- final validation;
- whether an initial AUTO_CONFIRMED sample actually required correction.

It does not copy merchant/product/date/price/OCR text, IDs, paths or images.

## Phase B procedure

Use the canonical CP37 debug APK for at least 10 real receipts.

For each receipt:

1. add via camera or gallery;
2. let OCR finish;
3. visually compare every field with the original receipt, even if AUTO_CONFIRMED;
4. correct all factual errors;
5. save;
6. tap `검증 결과 복사`;
7. return only the `RL_CP37_SAMPLE ...` line to this chat.

Aim for >=3 camera, >=3 gallery and >=3 different receipt layouts where practical.

`false_auto_confirm=1` is a blocker-quality trust finding.

## Privacy/security

Never commit or share in the public repository:

- real receipt images;
- OCR text;
- store/product names;
- dates/prices/totals;
- receipt/product IDs;
- real purchase databases/backups;
- credentials/signing secrets.

No CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permission is packaged.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly ReceiptLedger-prefixed workflows.

## Stop condition

**Wait for physical-device Phase B reports before changing OCR behavior.**
