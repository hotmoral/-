# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
4. `CP37_FALSE_ITEM_ROW_REMEDIATION_EVIDENCE.md`
5. `CP37_FALSE_ITEM_ROW_REMEDIATION_PLAN.md`
6. `CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
7. `CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_EVIDENCE.md`
8. `CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
9. `PRODUCT_REBASELINE_V1_ROADMAP.md`
10. `WORK_UNIT.md`

GitHub is canonical. Verify the current docs-only handoff and the frozen executable separately before using old chat context.

## Current boundary

V1 CP20–CP36: **COMPLETE**.

Post-V1 CP37: **IN PROGRESS**.

Current state: **Remediation A READY_FOR_PHYSICAL_RETEST**.

- active branch `receiptledger/run-post-v1-physical-ocr-remediation-20261017`
- predecessor Phase A handoff `6b7d7b9b65432701b43da53a0e6f0ff1e47a1449`
- frozen remediation executable `06fafa9db1da0e4592ddc15a468a9c6e4e338515`
- canonical Actions `38957744298` — SUCCESS
- job `117164770764`
- artifact `12071212297`
- artifact digest `sha256:6540c6350ea47280dc3d9fec64cdaef3b2aef24976f833a44e0cb13bd3b2a811`
- APK SHA-256 `109b61603c9f4a0a399ecb919399151427ab3ba243e626bbe8543340a4ee0f3d`
- version `1.0.36-physical-ocr-remediation`, code 37
- debug package `com.receiptledger.v1.remediation`
- label `ReceiptLedger 검증`
- lint `No issues found.`

CP37 is **not complete**.

## Why remediation exists

The first physical sample was correctly REVIEW_REQUIRED, but user inspection found a non-product address/header row classified as a product item. The row was spatially separated from the real item body, and the Phase A review UI could not remove a false item row.

The issue was therefore classified as a structure/recoverability defect.

## Remediation A

The frozen remediation build adds:

- a conservative rule demoting provisional item rows above a recognized date when a real multi-item body exists below;
- `이 항목은 상품이 아님` in review;
- `USER_REMOVED_ITEM:<ordinal>` provenance;
- correct sanitized structural-delta reporting;
- a side-by-side debug package so the original validation app and its local evidence remain intact.

OCR model/options, recovery passes, identity, price semantics and schemas remain unchanged.

## Next physical retest

Install the remediation APK alongside the existing validation app. It appears as **ReceiptLedger 검증**.

Rerun the same receipt that exposed the false item, using the same acquisition path where practical.

Then:

1. check whether the previous address/header false item is absent;
2. visually verify every remaining recognized field;
3. if another false item remains, mark `이 항목은 상품이 아님`;
4. correct other factual errors;
5. save;
6. tap `검증 결과 복사`;
7. return only the new `RL_CP37_SAMPLE ...` line and state whether the original false row appeared again.

Do not resume the broader 10-receipt campaign before this retest is analyzed.

## Privacy/security

Never commit or share in the public repository:

- real receipt images;
- OCR text;
- merchant/product names;
- dates/prices/totals;
- receipt/product IDs;
- real DBs/backups;
- credentials/signing secrets.

The remediation APK packages no CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permission.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly ReceiptLedger-prefixed workflows.
