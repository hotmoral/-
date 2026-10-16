# ReceiptLedger — CP37 Partial Row Prefill Remediation Plan

Updated: 2026-10-17 KST

## 1. Trigger

The CP37 physical metric-check receipt reproducibly produced one first-item row with both quantity and unit price blank across multiple validation builds. The same sample also showed `review_scope_miss=1`, so any remediation must not weaken review safety.

The current `ItemTupleSolver` can parse two printed money values on an item row but, when the quantity token is absent, falls through to `PARTIAL` and discards the otherwise usable unit-price candidate.

## 2. Scope

This remediation is intentionally narrow.

When an ITEM row contains:

- at least two non-negative printed money candidates;
- no parsed quantity token;
- a rightmost line amount;
- a preceding money candidate that can serve as unit price;
- exact integer ratio `lineAmount / unitPrice` in the supported quantity range 1..99;

then prefill:

- quantity = exact arithmetic ratio;
- unit price = printed preceding money value;
- line amount = printed rightmost money value.

The row remains `ItemResolution.PARTIAL` and therefore remains explicitly review-required.

Provenance:

- quantity origin = `INFERRED_ARITHMETIC`;
- unit price origin = `PRINTED`;
- line amount origin = `PRINTED`;
- reason = `PRINTED_UNIT_AND_LINE_INFER_QTY_REVIEW_REQUIRED`.

## 3. Safety contract

This remediation MUST NOT:

- promote the row to `EXACT` or normal `INFERRED`;
- reduce the number of review-required rows solely because fields were prefilled;
- change `CaptureReviewAssessmentV2` production policy;
- change OCR recognition, recovery passes or preprocessing;
- add OCR text substitutions such as correcting package suffix characters;
- change product/receipt schemas;
- change identity, price, search or persistence semantics.

The purpose is to reduce manual data entry while preserving the existing trust boundary.

## 4. Evidence contract

Add deterministic tests proving:

1. two printed equal money values with missing quantity prefill quantity=1 and unit price while remaining PARTIAL;
2. another exact integer ratio prefill uses that ratio and remains PARTIAL;
3. non-integral ratios remain unresolved PARTIAL with null quantity/unit as before;
4. a fully populated PARTIAL item remains review-required in `CaptureReviewAssessmentV2`;
5. existing ItemTupleSolver and CP33 regressions remain green.

The CP37 report stays `version=2`; selective-review coverage instrumentation is unchanged.

## 5. Physical confirmation

After CI passes, produce a side-by-side debug validation APK. Re-run the same physical receipt once.

Success criteria for the triggering row:

- first item quantity and unit price are prefilled rather than blank;
- the first item is still shown as requiring explicit review;
- the user can correct/confirm it normally;
- `review_scope_miss` metrics remain available for unrelated OCR-name errors.

The literal OCR character confusion observed in a package suffix is recorded only as sanitized physical evidence and is NOT auto-corrected by this remediation.

## 6. Stop condition

Do not start the independent 10-receipt campaign until the same-receipt physical confirmation verifies that prefill works without weakening the review boundary.
