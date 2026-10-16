# ReceiptLedger CP37 — False Item Row Remediation Plan

Updated: 2026-10-17 KST

## Trigger

Physical-device sample #1 exposed a structural false positive: a non-product address/header row was classified as a purchase item. The row was spatially separate from the item body. The initial sample correctly required review, but the existing review UI could not remove a false item row.

## Classification

This is not primarily an OCR character-recognition defect. It is a structure/recoverability defect:

1. `ReceiptStructureAnalyzer.looksLikeItem()` can treat any row containing letters left of a money-like numeric token as an item.
2. A header/address row with a 3+ digit number can therefore become `ITEM`.
3. Once marked `ITEM`, it can incorrectly establish the receipt body boundary.
4. `ReceiptReviewEngine` previously required a one-for-one item edit list and exposed no explicit row-removal operation.

## Remediation scope

### A. Conservative structure gate

When a valid receipt date is recognized and at least two item rows exist below it, any provisional item row above that date is demoted to `HEADER` with reason `ITEM_BEFORE_DATE_WITH_BODY_BELOW`.

This rule deliberately does **not** attempt a general address-language classifier and does not affect:

- receipts with no recognized date;
- single-item receipts where fewer than two items exist below the date;
- OCR/recovery pass selection;
- price/identity/schema logic.

### B. Explicit review recovery

The review UI gains `이 항목은 상품이 아님` for each displayed item row.

Selecting it:

- removes that item from the reviewed record;
- preserves the original ordinal of all remaining items;
- records `USER_REMOVED_ITEM:<ordinal>` provenance;
- recomputes totals/validation;
- permits the reviewed record to become safe once arithmetic and required fields are valid.

### C. CP37 evidence

The existing sanitized report must record a removed row as:

- `item_count_changed=1`
- `item_structure_changes>=1`
- `any_correction=1`

No receipt text/value content is added to the report.

## Non-goals

- no OCR model change;
- no recovery-score change;
- no fuzzy header/address text classifier;
- no database schema change;
- no identity or price semantics change;
- no attempt to solve every possible footer/header false positive from a single physical sample.

## Acceptance

1. Synthetic address-with-number row before a recognized date is not emitted as an item when a real multi-item body exists below.
2. Conservative single-item edge case is preserved.
3. Review engine can remove one false item and preserve remaining ordinal/provenance.
4. Removed false item can resolve a total mismatch into `PASS_WITH_WARNINGS` without a review loop.
5. CP37 sanitized report records the structural correction without leaking receipt values.
6. Existing V1 regression suites and lint remain green.
7. Forbidden permissions remain absent.

## Next physical-device step

After a green remediation build, rerun the same receipt once. If the address row no longer appears, record the new sanitized line as the remediation verification sample before resuming the broader CP37 campaign.
