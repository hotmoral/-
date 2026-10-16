# ReceiptLedger CP37 — False Item Row Remediation A Closeout

Updated: 2026-10-17 KST
Status: **READY_FOR_PHYSICAL_RETEST** — CP37 NOT COMPLETE

## Trigger

The first physical-device Phase B sample was safe in the sense that it was `REVIEW_REQUIRED` and `false_auto_confirm=0`, but the user observed a non-product address/header row being classified as an item even though it was spatially separated from the real item body.

The existing review UI also could not remove a false item row, so `item_count_changed=0` / `item_structure_changes=0` in that first report did not prove the recognized item structure was correct.

## Root cause

Two bounded defects were confirmed:

1. `ReceiptStructureAnalyzer.looksLikeItem()` accepted a row containing letters left of a money-like numeric token without considering whether the row belonged to the actual item body. A 3+ digit address/header number could therefore be treated as money and establish a false ITEM row.
2. Receipt review required a one-for-one edit list and exposed no item-row removal operation.

## Remediation

### Conservative structure gate

When a valid DATE row is recognized and at least two ITEM rows exist below it, provisional ITEM rows above that date are demoted to HEADER with reason `ITEM_BEFORE_DATE_WITH_BODY_BELOW`.

The rule is intentionally narrow. It does not guess address vocabulary and does not apply when no date is recognized or when fewer than two items exist below the date.

### Explicit false-item recovery

Review now exposes `이 항목은 상품이 아님`.

Selecting it:

- removes that item from the reviewed record;
- preserves remaining original ordinals;
- records `USER_REMOVED_ITEM:<ordinal>` provenance;
- recomputes receipt arithmetic and validation;
- may resolve a mismatch into `PASS_WITH_WARNINGS` without creating a review loop.

### Side-by-side validation build

GitHub-hosted debug signing certificates differ between runs, so replacing the earlier CP37 validation APK could require uninstalling it and losing local evidence. The remediation debug build therefore uses:

- applicationId `com.receiptledger.v1.remediation`;
- label `ReceiptLedger 검증`;
- provider authority `com.receiptledger.v1.remediation.capture`.

The normal production applicationId remains `com.receiptledger.v1`. The manifest source uses `${applicationId}.capture`, preserving the production authority while allowing the isolated debug package.

## Frozen executable

- branch: `receiptledger/run-post-v1-physical-ocr-remediation-20261017`
- predecessor Phase A handoff: `6b7d7b9b65432701b43da53a0e6f0ff1e47a1449`
- frozen remediation executable: `06fafa9db1da0e4592ddc15a468a9c6e4e338515`
- canonical Actions: `38957744298` — SUCCESS
- job: `117164770764` — SUCCESS
- artifact ID: `12071212297`
- artifact digest: `sha256:6540c6350ea47280dc3d9fec64cdaef3b2aef24976f833a44e0cb13bd3b2a811`
- APK SHA-256: `109b61603c9f4a0a399ecb919399151427ab3ba243e626bbe8543340a4ee0f3d`
- versionName: `1.0.36-physical-ocr-remediation`
- versionCode: 37
- lint: `No issues found.`

## Verification

Canonical remediation metric:

`CP37_REMEDIATION_METRICS version=1 structure_tests=5 review_tests=5 report_tests=5 predate_false_item_gate=1 explicit_item_removal=1 provenance_preserved=1 report_structure_delta=1 side_by_side_debug=1 schema_unchanged=1`

- Structure tests: 5/5 PASS
- Review engine tests: 5/5 PASS
- Device validation report tests: 5/5 PASS
- Full debug unit regression/lint/APK build: PASS
- packaged debug applicationId: `com.receiptledger.v1.remediation`
- packaged provider authority: `com.receiptledger.v1.remediation.capture`
- forbidden CAMERA/media/storage/INTERNET/ACCESS_NETWORK_STATE permissions: absent

## Frozen invariants

Unchanged:

- ML Kit model/options;
- OCR preprocessing and recovery pass policy;
- stable-ID identity authority;
- CP27/28 price semantics;
- CP29 discovery semantics;
- product schema 2 / receipt schema 1;
- offline/privacy posture.

## Physical retest gate

Do not resume the broad 10-sample campaign yet.

Next action is to install the side-by-side remediation APK and rerun the **same receipt** once.

Pass condition for Remediation A physical confirmation:

1. the previously observed address/header row no longer appears as an item; OR, if another false row remains, the user can explicitly mark it `이 항목은 상품이 아님` and save correctly;
2. saved report reflects any actual structural removal via `item_count_changed` / `item_structure_changes`;
3. no false auto-confirm, crash, save failure, duplicate save, or new privacy issue occurs.

Only after this physical retest is analyzed may the broader CP37 campaign resume.
