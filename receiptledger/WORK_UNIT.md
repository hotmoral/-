# ReceiptLedger public execution work unit

Updated: 2026-10-17 KST

## Current stage

**CP37 — Physical Device / Real-Image OCR Validation**

Current substage:

**Selective Review Coverage Instrumentation — READY_FOR_PHYSICAL_METRIC_CHECK**

- branch: `receiptledger/run-post-v1-selective-review-coverage-20261017`
- predecessor handoff: `c4e00ff22339869346f0f8692e38d82567568b7e`
- frozen executable: `7dbed4cf73a2963ace7447974e9d972a9776b79f`
- canonical Actions: `38976080450` SUCCESS
- job: `117225743973`
- artifact: `12078898591`
- artifact digest: `sha256:402a5dda9d0892550ff08d5a5f3dbeb228a01a6f32abc40d24f8a75efa510b67`
- APK SHA-256: `29fcd2073d74fee819d53525bf2409db1587a72e72e86af115496843562405b8`
- versionName: `1.0.37-review-coverage-validation`
- versionCode: 38
- package: `com.receiptledger.v1.reviewcoverage`
- label: `ReceiptLedger 검증 B`
- lint: 0 errors / 0 warnings

CP37 is **not complete**.

## Evidence already established

1. First real-device sample exposed a false address/header ITEM row and no removal recovery.
2. Remediation A added narrow pre-date gating and explicit false-item removal.
3. Physical retest confirmed the previously false address row no longer appeared.
4. The retest also exposed that selective review may not cover all item corrections: 15 initial items, 1 selected review item, but several item fields were corrected after full visual inspection.
5. Report v1 could not quantify corrected item ordinals outside the initial review set.

## Report v2

New fields:

- `corrections_outside_review_items=N`
- `review_scope_miss=0|1`

A distinct item ordinal counts once when it was outside the initial selected review set and later had any item field edit or structural add/remove.

This is separate from `false_auto_confirm`:

- `false_auto_confirm=1`: initially AUTO_CONFIRMED receipt required correction;
- `review_scope_miss=1`: at least one corrected item was outside the selected item-review scope.

## Current work unit

No coding is next.

1. Install `ReceiptLedger 검증 B` side by side.
2. Process one real receipt.
3. Visually inspect every recognized field against the original even when not highlighted.
4. Correct all factual/structural errors.
5. Save.
6. Tap `검증 결과 복사`.
7. Return only the generated `RL_CP37_SAMPLE version=2 ...` line.

This is the metric-path verification sample.

If the v2 fields are present and coherent, start the independent 10-receipt campaign. Earlier v1 samples are excluded from that final 10.

## Final 10-sample campaign target after metric check

Where practical:

- 10 successfully saved real receipts;
- >=3 CAMERA;
- >=3 GALLERY;
- >=3 materially different receipt layouts.

Aggregate:

- OCR median/max;
- pass distribution;
- AUTO_CONFIRMED / REVIEW_REQUIRED;
- false_auto_confirm count;
- review_scope_miss count/rate;
- total corrections outside selected review items;
- receipt field corrections;
- item structure/name/quantity/unit-price/line-amount corrections;
- crash/hang/save/duplicate failures.

## Priority

1. correctness / false-auto-confirm;
2. selective-review coverage;
3. save/provenance;
4. review burden;
5. latency.

## Frozen boundary

Until physical v2 evidence is analyzed, do not modify OCR/recovery, Remediation A structure gate, review selection policy, identity/price/search, schemas or permission posture.

## Public/privacy boundary

Only sanitized report lines and aggregate metrics may enter public evidence. Do not commit real receipts or private purchase data.

## Stop condition

**Await one v2 physical report.**
