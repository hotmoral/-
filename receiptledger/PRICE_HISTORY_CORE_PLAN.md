# ReceiptLedger V1 Price History Core

Checkpoint: `RL_V1_PRICE_HISTORY_CORE_01`

## Derivation policy
Price observations are derived on demand from canonical receipt records plus product links. No duplicate price-observation table is created.

## Eligibility
- product must be classified and linked
- receipt validation must be PASS or PASS_WITH_WARNINGS
- MISMATCH / INCOMPLETE receipts are excluded
- prefer persisted unitPrice
- if unitPrice is absent, derive only when quantity > 0 and lineAmount divides exactly by quantity

## Type policy
- STANDARD: observations are comparable for latest/min/max/average package-unit trend
- NON_STANDARD: observations are shown as raw history only; no cross-unit conversion or aggregate trend is claimed yet
- UNCLASSIFIED: no history

## Non-goals
- explicit sales-unit model (kg/봉/팩/단 etc.)
- quantity conversion
- charts
- online price comparison
