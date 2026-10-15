# ReceiptLedger V1 Validation Core

Checkpoint: `RL_V1_VALIDATION_CORE_01`

## Scope

Receipt-level arithmetic validation after Structure Core and Item Tuple Core.

Formula:
`computedNet = sum(item.lineAmount) + sum(discount.effect)`

Discount effect rules:
- printed negative discount stays negative
- printed positive value on a row already classified `DISCOUNT` is interpreted as a negative effect

Statuses:
- `PASS`: total matches and no partial item tuple remains
- `PASS_WITH_WARNINGS`: total matches but at least one item tuple is still partial
- `MISMATCH`: complete line coverage and printed total exist, but arithmetic differs
- `INCOMPLETE`: required line amount/discount amount/printed total is missing or arithmetic overflows

## Non-goals

- automatic repair of mismatches
- attaching discounts to individual products
- OCR recovery
- merchant/product normalization
- persistence/database

A mismatch is evidence, not permission to mutate OCR values.
