# ReceiptLedger — Session Handoff

Updated: 2026-10-17 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct project state from old chat before reading current documents and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
4. `receiptledger/CP37_FALSE_ITEM_ROW_REMEDIATION_EVIDENCE.md`
5. `receiptledger/CP37_FALSE_ITEM_ROW_REMEDIATION_PLAN.md`
6. `receiptledger/CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
7. `receiptledger/CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_EVIDENCE.md`
8. `receiptledger/CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
9. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
10. `receiptledger/README.md`
11. `receiptledger/WORK_UNIT.md`

## 1. Current execution state

V1 CP20–CP36 is complete.

CP37 is open.

Current state: **Remediation A READY_FOR_PHYSICAL_RETEST**.

- active branch: `receiptledger/run-post-v1-physical-ocr-remediation-20261017`
- predecessor Phase A handoff: `6b7d7b9b65432701b43da53a0e6f0ff1e47a1449`
- frozen remediation executable: `06fafa9db1da0e4592ddc15a468a9c6e4e338515`
- canonical Actions: `38957744298` SUCCESS
- job: `117164770764`
- artifact: `12071212297`
- artifact digest: `sha256:6540c6350ea47280dc3d9fec64cdaef3b2aef24976f833a44e0cb13bd3b2a811`
- APK SHA-256: `109b61603c9f4a0a399ecb919399151427ab3ba243e626bbe8543340a4ee0f3d`
- versionName: `1.0.36-physical-ocr-remediation`
- versionCode: 37
- package: `com.receiptledger.v1.remediation`
- label: `ReceiptLedger 검증`
- lint: `No issues found.`

Do **not** label CP37 complete.

## 2. Why remediation was opened

First real-device sample produced a privacy-safe report with:

- GALLERY, 800x1067;
- OCR 562ms;
- 3 attempted passes, 2 merged candidates;
- ORIGINAL selected;
- MISMATCH / REVIEW_REQUIRED;
- 16 initial items / 16 review items;
- 5 item-name edits, 1 unit-price edit, 1 line-amount edit;
- false_auto_confirm=0;
- final PASS_WITH_WARNINGS / save success.

After sending the report, the user noted that a spatially separate address/header row had also been treated as a product item.

Inspection confirmed:

- item detection accepted letters left of a money-like numeric token with no body-continuity guard;
- a 3+ digit header/address number could therefore create a false ITEM row;
- review could edit item values but could not delete an item row.

This is a structural/recoverability defect, not just OCR spelling error.

## 3. Remediation implementation

### Structure

If a valid receipt DATE exists and at least two ITEM rows exist below it, provisional ITEM rows above the date are demoted to HEADER with reason `ITEM_BEFORE_DATE_WITH_BODY_BELOW`.

The rule is intentionally narrow. No generic address text classifier was introduced.

### Review

Review displays `이 항목은 상품이 아님` for shown item rows.

A removed row:

- is omitted from the reviewed record;
- leaves remaining original ordinals unchanged;
- writes `USER_REMOVED_ITEM:<ordinal>`;
- recomputes arithmetic/validation;
- is recognized by `CaptureReviewAssessmentV2` as explicit user provenance.

### Report

The existing CP37 report maps items by ordinal. Removal therefore produces `item_count_changed=1` and at least one `item_structure_changes`, while still exporting no receipt values.

## 4. Side-by-side installation

Do not uninstall the original Phase A validation app.

Runner-generated debug signing certificates differed between builds, so Remediation A uses a separate debug package:

- package: `com.receiptledger.v1.remediation`
- label: `ReceiptLedger 검증`
- FileProvider authority: `com.receiptledger.v1.remediation.capture`

The package has its own empty local DB/catalog. This is intentional. The original app/data remain untouched.

## 5. Verification

Canonical metric:

`CP37_REMEDIATION_METRICS version=1 structure_tests=5 review_tests=5 report_tests=5 predate_false_item_gate=1 explicit_item_removal=1 provenance_preserved=1 report_structure_delta=1 side_by_side_debug=1 schema_unchanged=1`

All three focused suites: 5/5 PASS. Full debug unit regression, lint and APK build passed. Forbidden camera/media/storage/network permissions remain absent.

OCR/recovery/identity/price/schema implementations were not changed.

## 6. Exact next task

This is **physical retest evidence**, not more coding.

Use the frozen remediation APK and rerun the same receipt that exposed the false item.

Procedure:

1. install `ReceiptLedger 검증` side by side;
2. process the same image via the same acquisition method where practical;
3. check whether the address/header false item is gone;
4. compare every remaining field against the original;
5. if any false item remains, select `이 항목은 상품이 아님`;
6. correct remaining factual errors;
7. save;
8. tap `검증 결과 복사`;
9. return only the resulting `RL_CP37_SAMPLE ...` line and separately state whether the original false address row appeared again.

Do not continue with additional campaign receipts before this retest is analyzed.

## 7. Decision after retest

If the original false item is gone and no new blocker appears, record Remediation A physical confirmation and resume the CP37 campaign.

If it remains, use the new removal recovery if possible, record the sanitized line, and analyze the remaining structure pattern before broadening the rule.

Avoid speculative general classifiers or OCR changes from one sample.

## 8. Privacy boundary

Never commit/share in public GitHub:

- real receipt photo;
- raw OCR text;
- merchant/product names;
- real dates/prices/totals;
- receipt/product IDs;
- DB backup/private files;
- credentials/signing material.

Sanitized CP37 report lines and aggregate conclusions are permitted evidence.
