# ReceiptLedger V1 Receipt Library Core

Checkpoint: `RL_V1_LIBRARY_CORE_01`

## Scope
- saved receipt list, newest first
- receipt detail view
- sampled app-private archived image decode
- item tuple + validation issue display
- explicit delete confirmation and coordinated DB/image delete

## Non-goals
- editing recognized values
- product aliases / normalization
- price history
- thumbnails/cache
- search/filter

## Memory rule
List view never decodes receipt images. Detail image uses bounds-first power-of-two sampling with a bounded max edge.
