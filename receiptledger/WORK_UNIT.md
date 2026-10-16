# ReceiptLedger public execution work unit

Updated: 2026-10-17 KST

## Current stage

**CP37 — Physical Device / Real-Image OCR Validation**

Current substage: **Remediation A READY_FOR_PHYSICAL_RETEST**

- active branch: `receiptledger/run-post-v1-physical-ocr-remediation-20261017`
- predecessor Phase A handoff: `6b7d7b9b65432701b43da53a0e6f0ff1e47a1449`
- frozen remediation executable: `06fafa9db1da0e4592ddc15a468a9c6e4e338515`
- canonical Actions: `38957744298` — SUCCESS
- job: `117164770764`
- artifact: `12071212297`
- artifact digest: `sha256:6540c6350ea47280dc3d9fec64cdaef3b2aef24976f833a44e0cb13bd3b2a811`
- APK SHA-256: `109b61603c9f4a0a399ecb919399151427ab3ba243e626bbe8543340a4ee0f3d`
- versionName: `1.0.36-physical-ocr-remediation`
- versionCode: 37
- debug applicationId: `com.receiptledger.v1.remediation`
- app label: `ReceiptLedger 검증`
- lint: 0 errors / 0 warnings

**CP37 is not complete.**

## Why the work unit changed

The first physical receipt sample exposed a false item row: a non-product address/header row was included as an item despite being spatially separate from the product body.

The sample was REVIEW_REQUIRED and `false_auto_confirm=0`, so the safety gate behaved conservatively. The defect was instead in structure classification and user recoverability.

## Remediation A contents

1. If a recognized date has at least two real item candidates below it, provisional item rows above the date are demoted to HEADER.
2. Review now supports `이 항목은 상품이 아님`.
3. Removed rows preserve remaining original ordinals and write `USER_REMOVED_ITEM:<ordinal>`.
4. Validation arithmetic is recomputed after removal.
5. CP37 sanitized reports detect item-count/structure changes without private receipt values.
6. The debug build installs side-by-side as `ReceiptLedger 검증` so the original Phase A app/data are preserved.

Canonical metric:

`CP37_REMEDIATION_METRICS version=1 structure_tests=5 review_tests=5 report_tests=5 predate_false_item_gate=1 explicit_item_removal=1 provenance_preserved=1 report_structure_delta=1 side_by_side_debug=1 schema_unchanged=1`

## Current physical work unit

The next task is **one same-receipt physical retest**.

Do not collect new campaign receipts yet.

### Procedure

1. Keep the existing `ReceiptLedger` Phase A app installed.
2. Install the remediation APK; it appears separately as `ReceiptLedger 검증`.
3. In `ReceiptLedger 검증`, process the same receipt image that produced the first sample, using GALLERY again where practical.
4. Check whether the prior false address/header item appears.
5. Compare every recognized field with the original receipt.
6. If any false item remains, check `이 항목은 상품이 아님` for it.
7. Correct all other factual errors.
8. Save.
9. Tap `검증 결과 복사`.
10. Return only the new `RL_CP37_SAMPLE ...` line plus a short yes/no statement on whether the original false address row appeared again.

## Retest interpretation

### Remediation confirmation

Strong confirmation requires:

- prior false address/header row absent, OR remaining false row safely removable;
- no crash/OCR hang/save failure/duplicate save;
- report records structural removal if used;
- false_auto_confirm remains 0 unless a real AUTO_CONFIRMED error is discovered.

### If the false row persists

Do not immediately add a broad address/product classifier. Preserve the report and analyze the remaining row position/structure. Extend the rule only with evidence.

## Frozen non-goals

No change to:

- ML Kit model/options;
- OCR preprocessing/recovery scoring/pass order;
- identity authority;
- price/comparability semantics;
- product schema 2 / receipt schema 1;
- network/storage permission posture.

## Public/privacy rule

Only sanitized `RL_CP37_SAMPLE` lines and aggregate conclusions may become public evidence. Never commit real receipt image/text/value data, DBs, credentials or signing material.

## Stop condition

**Wait for the same-receipt remediation retest. Do not resume the broad Phase B campaign or add more code before that evidence is analyzed.**
