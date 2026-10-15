# ReceiptLedger V1 Review / Edit Core

Checkpoint: `RL_V1_REVIEW_EDIT_CORE_01`

## Goal
No automatically recognized receipt becomes persisted trusted data without an explicit user review step.

## Editable fields
- purchase date
- printed total
- aggregate discount (signed; discounts are negative)
- each item name
- each item quantity
- each item unit price
- each item line amount

## Contracts
- OCR raw text remains immutable evidence.
- Save stays disabled after OCR until review is applied.
- Changed numeric values use `ValueOrigin.USER_EDITED`.
- Review never silently re-infers a value the user cleared.
- `quantity * unitPrice == lineAmount` is recomputed after edits.
- receipt net total is recomputed after edits.
- arithmetic mismatch is reported, never auto-repaired.
- blank/invalid user input blocks Apply.
- DB schema remains v1; enum provenance is stored as text.

## Non-goals
- product aliases / canonical identity
- price history
- bulk editing from receipt library
- cloud sync
