# ReceiptLedger V1 Persistence Core

Checkpoint: `RL_V1_PERSISTENCE_CORE_01`

## Scope
- immutable persisted receipt/item domain contract
- schema v1 for receipts, items, validation issues
- transactionally atomic SQLite save/replace
- get/list/count/delete operations
- deterministic newest-first ordering
- UI save action after successful OCR/structure/item/validation pipeline
- app-private database only

## Stored receipt fields
- stable receipt id and creation timestamp
- normalized purchase date when detected
- raw OCR text
- source image dimensions and whether perspective-corrected input was OCRed
- printed/computed totals, discount/item sums, validation status/difference
- all validation issues
- item name, quantity, unit price, line amount, value origins, resolution and reason

## Non-goals
- source image archival (separate checkpoint)
- product normalization / aliases
- price history
- receipt list/detail UI
- cloud sync / networking

## Safety contracts
- one DB transaction writes receipt + items + issues
- foreign keys + ON DELETE CASCADE
- no destructive automatic schema upgrade
- no network/camera/storage permission additions
- no real receipt fixture in the public repository
