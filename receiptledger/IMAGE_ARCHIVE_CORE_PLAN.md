# ReceiptLedger V1 Image Archive Core

Checkpoint: `RL_V1_IMAGE_ARCHIVE_CORE_01`

## Scope
- archive the EXIF-normalized source bitmap as app-private JPEG
- one stable image filename per receipt id
- fsync + temp-file rename before DB save
- DB save only after image archive succeeds
- rollback image when DB save throws
- orphan/temp cleanup on startup
- coordinated receipt delete removes DB row and archived image

## Crash consistency
The preferred failure mode is an orphan image, never a receipt row that claims a successful save while its image write failed.

1. write image temp file
2. flush + fsync
3. rename temp to final app-private file
4. save SQLite receipt/items/issues transaction
5. if step 4 throws, delete final image

A process death between 3 and 4 can leave only an orphan image. Startup reconciliation deletes files whose receipt ids are absent from SQLite.

## Non-goals
- thumbnails / list UI
- image editing
- cloud backup
- product normalization
- DB schema migration (schema stays v1)
