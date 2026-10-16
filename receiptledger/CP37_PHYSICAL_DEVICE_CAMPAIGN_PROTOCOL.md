# ReceiptLedger Post-V1 — CP37 Physical Device Campaign Protocol

Updated: 2026-10-17 KST
Checkpoint: CP37 Phase B

## 1. Purpose

Collect real-device / real-image evidence without uploading receipt images, OCR text or purchase details to the public repository.

## 2. Required build

Use only the CP37 validation APK produced by the canonical Phase A workflow. Do not mix reports from older CP36 APKs or later experimental OCR builds.

## 3. Sample target

Minimum: **10 successfully saved real receipt samples**.

Aim for:

- at least 3 CAMERA samples when practical;
- at least 3 GALLERY samples;
- at least 3 materially different receipt layouts;
- a mix of short/long receipts if available;
- perspective correction where visually warranted and available.

Do not manufacture difficult images solely to increase failure count. Use representative personal usage.

## 4. Per-sample procedure

For each receipt:

1. Open ReceiptLedger and choose `영수증 추가`.
2. Acquire via camera or gallery.
3. If perspective correction is visibly warranted and the app offers it, apply it before the final OCR run.
4. Wait for OCR/recovery completion.
5. **Regardless of AUTO_CONFIRMED/REVIEW_REQUIRED, visually compare the recognized receipt against the original image.**
6. Correct every factual error using the existing review / 전체 내용 수정 path.
7. Save once the record matches the source receipt as closely as the current editable model allows.
8. Tap the debug-only `검증 결과 복사` control.
9. Paste the resulting `RL_CP37_SAMPLE ...` line into this chat.

Do not paste OCR text, store name, product names, dates, prices or screenshots containing receipt content unless separately requested in a private context.

## 5. Sanitized report contract

Expected shape:

`RL_CP37_SAMPLE version=1 source=GALLERY image_w=... image_h=... perspective=0 ocr_ms=... attempted_passes=... merged_candidates=... best_pass=ORIGINAL initial_validation=PASS initial_decision=AUTO_CONFIRMED initial_items=... initial_review_items=... initial_review_fields=... store_changed=0 date_changed=0 total_changed=0 discount_changed=0 item_count_changed=0 item_name_changes=0 item_quantity_changes=0 item_unit_price_changes=0 item_line_amount_changes=0 final_validation=PASS saved=1`

The exact key order is frozen by the Phase A implementation.

The line must not contain source values.

## 6. Interpretation

### Critical trust signal

If:

- `initial_decision=AUTO_CONFIRMED`, and
- any correction count/receipt-field change is non-zero,

classify the sample as `FALSE_AUTO_CONFIRM`.

Any such sample requires investigation before declaring CP37 PASS_NO_OCR_CHANGE.

### Review burden

For REVIEW_REQUIRED samples, correction counts distinguish useful conservative review from actual OCR/structure errors.

A review request with zero factual corrections is conservative burden; it is not equivalent to a false auto-confirm.

### Latency

Use `ocr_ms` only for full OCR/recovery time. Do not compare it directly with image load/camera launch time.

After at least 10 samples, compute median, max and pass-count distribution. The CP36 1,500 ms warm target is a reference trigger, not a standalone physical-device correctness gate.

## 7. Blocking failures

Record separately if any of the following occur:

- crash;
- OCR never returns;
- save reports failure;
- duplicate save from one tap;
- saved record differs from what was reviewed;
- original receipt provenance disappears;
- validation report contains forbidden private text/value data.

A blocker may stop the campaign early if repeated sampling risks corrupting data.

## 8. Privacy rules

Never commit or paste into the public GitHub repository:

- real receipt photos;
- raw OCR text;
- store/product names;
- dates/prices/totals;
- receipt/product IDs;
- real database backups.

Only the sanitized validation lines and aggregated conclusions are suitable for canonical public evidence.

## 9. Campaign outcome

After enough samples, aggregate:

- sample count;
- CAMERA/GALLERY counts;
- median/max OCR latency;
- pass-count distribution;
- AUTO_CONFIRMED / REVIEW_REQUIRED counts;
- false-auto-confirm count;
- total receipt-field correction count;
- total item-field correction counts;
- crashes/save failures/duplicates.

Then classify CP37 as PASS_NO_OCR_CHANGE, REMEDIATION_REQUIRED or INSUFFICIENT_EVIDENCE.
