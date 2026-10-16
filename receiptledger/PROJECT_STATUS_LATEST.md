# ReceiptLedger — Project Status Latest

Updated: 2026-10-17 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current boundary

Planned V1 CP20–CP36 is complete.

Post-V1 checkpoint **CP37 — Physical Device / Real-Image OCR Validation** is open.

Current state:

**Remediation A — READY_FOR_PHYSICAL_RETEST**

CP37 itself is **NOT COMPLETE** and the broad Phase B campaign is temporarily paused until the same receipt that exposed the false-item defect is rerun.

### Active branch / frozen executable

- active branch: `receiptledger/run-post-v1-physical-ocr-remediation-20261017`
- Phase A handoff predecessor: `6b7d7b9b65432701b43da53a0e6f0ff1e47a1449`
- frozen remediation executable: `06fafa9db1da0e4592ddc15a468a9c6e4e338515`
- canonical Actions: `38957744298` — SUCCESS
- job: `117164770764` — SUCCESS
- artifact ID: `12071212297`
- artifact digest: `sha256:6540c6350ea47280dc3d9fec64cdaef3b2aef24976f833a44e0cb13bd3b2a811`
- APK SHA-256: `109b61603c9f4a0a399ecb919399151427ab3ba243e626bbe8543340a4ee0f3d`
- version: `1.0.36-physical-ocr-remediation` / versionCode 37
- debug applicationId: `com.receiptledger.v1.remediation`
- label: `ReceiptLedger 검증`
- lint: 0 errors / 0 warnings

## 2. Physical finding that triggered remediation

First physical Phase B sample was correctly conservative:

- GALLERY
- OCR 562ms
- attempted passes 3
- merged candidates 2
- best pass ORIGINAL
- initial MISMATCH / REVIEW_REQUIRED
- false_auto_confirm=0
- save success

However, the user observed a spatially separate address/header row classified as a product item. The previous review UI had no way to remove a false item row. Therefore the original report's `item_count_changed=0` and `item_structure_changes=0` were not proof that item structure was correct.

This finding is classified as `FALSE_ITEM_ROW`, a structure/recoverability defect rather than merely an OCR character error.

## 3. Remediation A

### Conservative structure gate

If a valid DATE is recognized and at least two ITEM rows exist below it, provisional ITEM rows above the first date are demoted to HEADER with reason:

`ITEM_BEFORE_DATE_WITH_BODY_BELOW`

No general address-language classifier was added.

### Review recovery

Each review item may now be marked:

`이 항목은 상품이 아님`

Removal:

- preserves remaining original ordinals;
- adds `USER_REMOVED_ITEM:<ordinal>` provenance;
- recomputes totals/validation;
- is treated as explicit user provenance rather than an unresolved warning.

### Evidence report

A removed row is visible in the existing sanitized CP37 report through `item_count_changed` / `item_structure_changes` / `any_correction`, without exporting receipt values.

## 4. Side-by-side retest packaging

GitHub runner debug certificates changed between builds. To avoid requiring uninstall of the original Phase A validation app and deleting its local evidence, the remediation debug APK is intentionally a separate app:

- package `com.receiptledger.v1.remediation`
- label `ReceiptLedger 검증`
- provider `com.receiptledger.v1.remediation.capture`

The normal production applicationId remains `com.receiptledger.v1`.

The two apps have separate local data sandboxes. Product aliases/history from the old validation app therefore do not carry into the remediation app; this is intentional for isolated retesting.

## 5. Validation result

Canonical metric:

`CP37_REMEDIATION_METRICS version=1 structure_tests=5 review_tests=5 report_tests=5 predate_false_item_gate=1 explicit_item_removal=1 provenance_preserved=1 report_structure_delta=1 side_by_side_debug=1 schema_unchanged=1`

- structure 5/5 PASS
- review 5/5 PASS
- device report 5/5 PASS
- full unit regression/lint/debug APK build PASS
- forbidden CAMERA/media/storage/network permissions absent

## 6. Frozen invariants

Still unchanged:

- stable catalog ID identity authority;
- commodity grouping != comparability;
- CP27/28 price semantics;
- CP29 discovery semantics;
- ML Kit OCR model/options;
- OCR preprocessing/recovery pass policy;
- product schema 2 / receipt schema 1;
- offline/privacy permission posture.

## 7. Exact next action

Install the remediation APK **without uninstalling the original ReceiptLedger validation app**. It appears separately as `ReceiptLedger 검증`.

Rerun the **same receipt** once:

1. use the same image/acquisition path where practical;
2. verify whether the previously false address/header row is gone;
3. inspect every remaining item against the original receipt;
4. if a false item remains, mark `이 항목은 상품이 아님`;
5. correct any other factual errors;
6. save;
7. copy and return only the new `RL_CP37_SAMPLE ...` line.

Do not resume the remaining 10-sample campaign until this retest is analyzed.

## 8. Canonical restart order

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

GitHub is canonical. Verify docs-only handoff HEAD and frozen remediation executable separately.
