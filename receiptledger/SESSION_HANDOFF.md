# ReceiptLedger — Session Handoff

Updated: 2026-10-17 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct state from old chat before reading the current files and verifying refs.

Read in order:

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

## 1. Current execution state

V1 CP20–CP36 is complete.

Post-V1 CP37 is open.

**CP37 Phase A — READY_FOR_DEVICE_EVIDENCE**

- branch: `receiptledger/run-post-v1-physical-ocr-validation-20261017`
- predecessor handoff: `d0a3a9ec7658808c82247715d58ac106a3778186`
- frozen Phase A executable: `9bb5dcc276fae4632ade5ac3134e586baad65235`
- canonical Actions: `38950400666` — SUCCESS
- job: `117140033593` — SUCCESS
- artifact ID: `12068811009`
- artifact digest: `sha256:86d3861727db107e26edf4073666e010f59249ac746496524f6007ca09787697`
- APK SHA-256: `f9e5b73db79043a6fc6f76f3381e0e2fdab164b7b53c59d8b9ce405d1147120f`
- versionName `1.0.35-physical-ocr-validation`, versionCode 36
- lint: `No issues found.`

**Do not mark CP37 complete.** Phase B physical-device evidence is still missing.

## 2. Phase A implementation

Phase A instruments the existing MainActivity capture/review/save path without changing OCR/recovery/review semantics.

It adds:

- `DeviceValidationReportV1`;
- 4 deterministic privacy/correction tests;
- debug-only `검증 결과 복사` control;
- OCR/recovery elapsed/pass metadata capture;
- initial-vs-final correction counting;
- `false_auto_confirm` detection.

The validation snapshot is debug-gated. Report generation occurs after durable save and cannot convert a successful save into failure.

## 3. Exact report contract

Expected line:

`RL_CP37_SAMPLE version=1 source=GALLERY image_w=... image_h=... perspective=0 ocr_ms=... attempted_passes=... merged_candidates=... best_pass=ORIGINAL initial_validation=PASS initial_decision=AUTO_CONFIRMED initial_items=... initial_review_items=... initial_review_fields=... store_changed=0 date_changed=0 total_changed=0 discount_changed=0 item_count_changed=0 item_structure_changes=0 item_name_changes=0 item_quantity_changes=0 item_unit_price_changes=0 item_line_amount_changes=0 any_correction=0 false_auto_confirm=0 final_validation=PASS saved=1`

No raw receipt value belongs in this line.

## 4. Phase B user procedure

For each real receipt:

1. Install/use the canonical CP37 validation APK.
2. Enter `영수증 추가`.
3. Acquire by CAMERA or GALLERY.
4. Allow OCR/recovery to finish.
5. Visually compare the recognized receipt with the original **even if AUTO_CONFIRMED**.
6. Correct every factual error using existing review/full-edit UI.
7. Save.
8. Tap `검증 결과 복사`.
9. Paste only the `RL_CP37_SAMPLE ...` line into the chat.

Minimum decision target: 10 saved samples, with >=3 CAMERA, >=3 GALLERY and >=3 materially different layouts where practical.

## 5. Interpretation

- `initial_decision=AUTO_CONFIRMED` + `any_correction=1` -> `false_auto_confirm=1` -> blocker-quality trust finding.
- REVIEW_REQUIRED + `any_correction=0` -> conservative review burden, not a false auto-confirm.
- `ocr_ms` measures only the existing full `OcrRecoveryEngine.recognize(...)` operation.

After enough samples, classify CP37 as:

- `PASS_NO_OCR_CHANGE`, or
- `REMEDIATION_REQUIRED`, or
- `INSUFFICIENT_EVIDENCE`.

## 6. Frozen authority / non-goals

Until Phase B is analyzed, do not change:

- ML Kit model/options;
- OCR preprocessing;
- recovery pass rules / MAX_PASSES;
- CP33 review rules;
- identity/price/search semantics;
- schema;
- permissions.

Do not add telemetry, network upload, real receipt fixtures, release signing or unrelated features.

## 7. Public/privacy boundary

Never put real receipt photos, OCR text, merchant/product names, dates, prices, receipt/product IDs, file paths, private DBs/backups or credentials into the public repository.

Only sanitized report lines and aggregate conclusions may become public evidence.

## 8. Stop condition

**Current task is to collect Phase B physical-device reports. No further code work is authorized by Phase A itself.**
