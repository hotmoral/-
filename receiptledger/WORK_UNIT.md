# ReceiptLedger public execution work unit

Updated: 2026-10-17 KST

## Current stage

**CP37 — Physical Device / Real-Image OCR Validation**

Current substage:

**Remediation C — READY_FOR_PHYSICAL_PREFILL_RETEST**

- branch: `receiptledger/run-post-v1-partial-row-prefill-20261017`
- predecessor handoff: `d4f75d8120e4a9c347b3777c64b511e4f5d224d4`
- frozen executable: `01b22652a45889b6bfaa474131e0c5fa7f19e96e`
- canonical Actions: `38979684033` SUCCESS
- job: `117237351555`
- artifact: `12080029714`
- artifact digest: `sha256:55300e9525851f02232dc03f9a528fcd5b3c9c30ba68e7a30eb0bdb6634d46c2`
- APK SHA-256: `65fe0827f3a9ebfeafbbf783c6c8f82544f8594203008692288ab74ec9eb1e0e`
- versionName: `1.0.38-partial-row-prefill-validation`
- versionCode: 39
- package: `com.receiptledger.v1.rowrecovery`
- label: `ReceiptLedger 검증 C`
- lint: 0 errors / 0 warnings

CP37 is **not complete**.

## Evidence established

1. First physical sample exposed a false address/header item and no item-removal recovery.
2. Remediation A fixed the triggering false item in same-receipt physical retest.
3. Report v2 added item-level selective-review coverage metrics.
4. First physical v2 sample verified the metric path and produced `review_scope_miss=1` with 2 corrected item ordinals outside initial review scope.
5. The same receipt repeatedly showed first-item quantity and unit price blank across builds.
6. Source review identified a bounded solver gap for multiple money values with a missing quantity token.
7. A separate package-suffix character confusion remains OCR evidence only; no one-off substitution rule has been added.

## Remediation C contract

For an item row with no quantity token, prefill only when exactly one printed unit-price candidate and printed line amount imply an exact integer quantity 1..99.

The recovered item remains `PARTIAL` and therefore remains explicitly review-required.

Ambiguous/non-integral candidates remain unresolved.

Canonical metric:

`CP37_PARTIAL_PREFILL_METRICS version=1 item_tuple_tests=4 capture_review_tests=14 report_v2_tests=8 unique_integer_prefill=1 ambiguous_rejected=1 partial_review_preserved=1 report_v2_unchanged=1 schema_unchanged=1`

## Current work unit

No more coding is next.

1. Install `ReceiptLedger 검증 C` side by side.
2. Process the same receipt/image used for the repeated blank-field observation.
3. Confirm first-item quantity is prefilled.
4. Confirm first-item unit price is prefilled.
5. Confirm that item is still shown for explicit review.
6. Check every other recognized field against the original, including items not highlighted.
7. Correct all factual/structural errors.
8. Save.
9. Tap `검증 결과 복사`.
10. Return the `RL_CP37_SAMPLE version=2 ...` line and state whether checks 3–5 passed.

This repeated receipt is remediation evidence and does not count toward the final independent 10.

## After successful same-receipt retest

Only then begin the independent 10-receipt campaign, aiming where practical for:

- >=3 CAMERA;
- >=3 GALLERY;
- >=3 materially different layouts.

Aggregate:

- OCR latency/pass distribution;
- AUTO_CONFIRMED / REVIEW_REQUIRED;
- false_auto_confirm;
- review_scope_miss count/rate;
- corrections outside selected review items;
- receipt/item correction totals;
- crashes/hangs/save/duplicate failures.

## Priority

1. correctness / false-auto-confirm;
2. selective-review coverage;
3. save/provenance;
4. review burden;
5. latency.

## Public/privacy boundary

Only sanitized report lines and aggregate metrics may enter public evidence. Real receipt images/text/values remain outside the repository.

## Stop condition

**Await Remediation C same-receipt physical retest.**
