# ReceiptLedger V1 Structure Core

Checkpoint: `RL_V1_STRUCTURE_CORE_01`

## Scope

Convert reconstructed spatial rows into conservative receipt-structure semantics without yet solving item quantity/unit-price details.

Canonical row roles:
- `HEADER`
- `DATE`
- `ITEM`
- `DISCOUNT`
- `TOTAL`
- `PAYMENT`
- `UNKNOWN`

The analyzer also exposes:
- money candidates parsed from individual layout tokens
- validated date candidate
- selected receipt total candidate from explicit total rows
- item-candidate rows
- a deterministic reason string for every role decision

## Non-goals

- merchant identity normalization
- quantity/unit-price/line-total tuple solving
- discount attachment to a specific item
- arithmetic validation
- multi-pass OCR recovery
- persistence/database
- real receipt fixtures

## Conservative rules

A numeric token is not treated as money merely because it contains digits. Unmarked 1–2 digit tokens are rejected as money candidates so ordinary quantities are not immediately confused with prices. Item rows require both a money candidate and textual material to its left. Explicit total/discount/payment keywords take precedence over item inference.
