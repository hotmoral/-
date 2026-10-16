# ReceiptLedger — CP37 Partial Row Prefill Remediation C Closeout

Updated: 2026-10-17 KST

## Status

**READY_FOR_PHYSICAL_PREFILL_RETEST**

CP37 is not complete. The independent 10-receipt campaign remains paused until the same receipt that exposed the repeated first-item blank-field defect is retested.

## Frozen executable

- branch: `receiptledger/run-post-v1-partial-row-prefill-20261017`
- predecessor handoff: `d4f75d8120e4a9c347b3777c64b511e4f5d224d4`
- frozen executable: `01b22652a45889b6bfaa474131e0c5fa7f19e96e`
- canonical Actions: `38979684033` — SUCCESS
- canonical job: `117237351555` — SUCCESS
- artifact ID: `12080029714`
- artifact digest: `sha256:55300e9525851f02232dc03f9a528fcd5b3c9c30ba68e7a30eb0bdb6634d46c2`
- APK SHA-256: `65fe0827f3a9ebfeafbbf783c6c8f82544f8594203008692288ab74ec9eb1e0e`
- version: `1.0.38-partial-row-prefill-validation` / versionCode 39
- debug applicationId: `com.receiptledger.v1.rowrecovery`
- label: `ReceiptLedger 검증 C`

## Triggering physical evidence

A repeated same-receipt physical test showed:

- the Remediation A false address/header item remained fixed;
- report v2 correctly emitted `review_scope_miss=1` and `corrections_outside_review_items=2`;
- the first product row repeatedly presented quantity and unit price as blank across validation builds;
- a separate package-suffix character recognition error also repeated.

The package-suffix character error is not corrected by this remediation. One real sample is not enough evidence for a generic OCR substitution rule.

## Root cause addressed

`ItemTupleSolver` previously fell through to unresolved `PARTIAL` when an item row had multiple printed money candidates but no parsed quantity token. This discarded a usable printed unit-price candidate even when the printed line amount divided by that unit price exactly.

## Remediation contract

When there is no parsed quantity and there is exactly one preceding printed money candidate satisfying:

- positive unit price;
- positive line amount;
- exact divisibility;
- inferred quantity in 1..99;

then the row is prefilled with:

- quantity = exact arithmetic ratio;
- unit price = printed candidate;
- line amount = printed rightmost amount;
- quantity origin = `INFERRED_ARITHMETIC`;
- unit/line origins = `PRINTED`.

Crucially the row remains `ItemResolution.PARTIAL` with reason `PRINTED_UNIT_AND_LINE_INFER_QTY_REVIEW_REQUIRED`.

Therefore values are no longer unnecessarily blank, but explicit user review is still required.

Ambiguous or non-integral candidates remain unresolved as before.

## Scope preserved

Unchanged:

- ML Kit OCR model/options;
- OCR preprocessing and recovery passes;
- Remediation A structure gate;
- `CaptureReviewAssessmentV2` production policy;
- report v2 and review-scope metrics;
- identity, price, search and persistence semantics;
- product schema 2 / receipt schema 1;
- privacy/permission posture.

## Verification

Canonical metric:

`CP37_PARTIAL_PREFILL_METRICS version=1 item_tuple_tests=4 capture_review_tests=14 report_v2_tests=8 unique_integer_prefill=1 ambiguous_rejected=1 partial_review_preserved=1 report_v2_unchanged=1 schema_unchanged=1`

All focused suites and full regression/lint/APK build passed.

## Exact next action

Install `ReceiptLedger 검증 C` side by side and rerun the same receipt once.

Verify specifically:

1. first item quantity is prefilled rather than blank;
2. first item unit price is prefilled rather than blank;
3. the first item is still explicitly included in review;
4. all remaining fields are visually checked and corrected;
5. save and return only the `RL_CP37_SAMPLE version=2 ...` line.

The repeated diagnostic receipt does not count toward the final independent 10-receipt corpus.
