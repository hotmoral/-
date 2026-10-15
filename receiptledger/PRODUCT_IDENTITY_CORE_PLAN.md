# ReceiptLedger V1 Product Identity Core

Checkpoint: `RL_V1_PRODUCT_IDENTITY_CORE_01`

## Model
- `STANDARD`: repeatable packaged product whose price history can be compared as the same product.
- `NON_STANDARD`: user-defined item identity where observations are retained without automatic unit conversion.
- `UNCLASSIFIED`: no product link exists yet; this is not persisted as a product row.

## Safety contracts
- receipt DB schema v1 remains unchanged.
- product identity uses a separate app-private SQLite DB.
- raw receipt item name is never overwritten.
- no fuzzy/embedding/substring auto-merge.
- only a previously user-confirmed exact normalized alias may auto-link later observations.
- canonical-name/type conflict and alias collision fail closed.
- deleting a receipt removes item links but keeps reusable product/alias definitions.

## Normalization
Conservative NFKC + trim + repeated-whitespace collapse + Latin uppercase. Internal spaces, digits, units and punctuation remain significant.

## Non-goals
- unit conversion
- price trends
- category taxonomy
- fuzzy suggestions
- cloud catalog
