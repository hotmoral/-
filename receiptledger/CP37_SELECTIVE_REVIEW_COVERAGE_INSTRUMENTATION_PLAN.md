# ReceiptLedger CP37 — Selective Review Coverage Instrumentation Plan

Updated: 2026-10-17 KST

## 1. Trigger

CP37 Remediation A physical retest removed the previously observed false address/header item, but exposed a second evidence gap:

- initial_items=15
- initial_review_items=1
- item_name_changes=3
- item_quantity_changes=1
- item_unit_price_changes=1
- false_auto_confirm=0

The receipt was conservatively REVIEW_REQUIRED, so this is not a false-auto-confirm defect. However, the existing sanitized report cannot tell how many corrected item ordinals were outside the initially selected review set.

## 2. Goal

Add privacy-safe instrumentation to quantify selective-review coverage before resuming the broader CP37 physical campaign.

No product behavior changes are authorized in this step.

## 3. New report metrics

`corrections_outside_review_items=N`

Count distinct item ordinals that:

- were not present in the initial `CaptureReviewAssessmentV2.itemOrdinals`; and
- experienced at least one final-vs-initial item correction:
  - name changed;
  - quantity changed;
  - unit price changed;
  - line amount changed;
  - item removed;
  - item added.

Multiple corrected fields on one ordinal count once.

`review_scope_miss=1`

Emit 1 iff `corrections_outside_review_items > 0`, else 0.

Receipt-level fields STORE/PURCHASE_DATE/PRINTED_TOTAL/DISCOUNT_SUM are intentionally excluded from this metric. This checkpoint is narrowly about item-level selective-review coverage.

## 4. Privacy contract

The report must continue to exclude:

- merchant/product names;
- OCR text;
- dates;
- prices/totals;
- receipt/product IDs;
- file paths/images.

Only integer counts/flags are added.

## 5. Frozen contracts

Do not change:

- OCR model/options;
- OCR preprocessing/recovery pass policy;
- Remediation A structure gate;
- review selection policy;
- item-removal behavior;
- identity/price/search semantics;
- product schema 2 / receipt schema 1;
- permission posture.

## 6. Acceptance

1. deterministic report test proves an out-of-scope item correction yields `corrections_outside_review_items=1 review_scope_miss=1`;
2. a corrected item already in initial review scope yields `corrections_outside_review_items=0 review_scope_miss=0`;
3. multiple field corrections on one unflagged ordinal count once;
4. item removal outside scope counts once;
5. privacy tests remain green;
6. all prior CP37 remediation/V1 regression and lint remain green;
7. debug side-by-side package remains `com.receiptledger.v1.remediation`.

## 7. Stop condition

After a green build, freeze a new validation executable and rerun one physical receipt to verify the metrics are emitted. Then resume the independent 10-receipt campaign only after that report is analyzed.
