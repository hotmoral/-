# ReceiptLedger V1 Item Tuple Core

Checkpoint: `RL_V1_ITEM_TUPLE_CORE_01`

## Scope

Resolve `ITEM` rows into conservative item tuples:
- name candidate
- quantity
- unit price
- line amount
- provenance of every numeric value
- resolution state and reason

Resolution states:
- `EXACT`: printed unit price, printed quantity, and printed line amount satisfy exact arithmetic
- `INFERRED`: one missing value is derived by exact integer arithmetic, or quantity defaults to one for a single printed amount
- `PARTIAL`: line amount can be retained but a consistent full tuple cannot be proven

## Non-goals

- discount attachment
- receipt-level arithmetic reconciliation
- merchant/product normalization
- OCR recovery
- persistence/database
- real receipt fixtures

## Safety rule

Arithmetic inconsistency never gets silently repaired. A conflicting row remains `PARTIAL`; later validation/review layers decide what to do.
