# ReceiptLedger V1 Image Intake / Document Core

Checkpoint: `RL_V1_IMAGE_DOCUMENT_CORE_01`

## Scope

- system camera capture without requesting `CAMERA` permission in ReceiptLedger
- system document/image picker input without broad media/storage permission
- bounded bitmap decoding and JPEG EXIF orientation normalization
- canonical normalized-source bitmap coordinate contract
- conservative receipt quadrilateral detection
- projective transform and inverse coordinate mapping
- Android perspective-warp adapter
- source / detected-quad / corrected preview
- deterministic JVM regression tests
- public CI debug APK and build evidence

## Non-goals

- OCR
- receipt parsing
- database/persistence
- product normalization
- release signing
- real receipt fixtures or personal data

## Coordinate contract

The EXIF-normalized source bitmap is canonical for this checkpoint. Detector points are expressed in canonical bitmap pixels. Perspective correction records both source-to-output and output-to-source projective transforms so a later OCR layer can restore recognized coordinates to the canonical source image.

## Safety contract

- no real receipts, purchase histories, databases, credentials, signing keys, or tokens in this public namespace
- no `CAMERA`, `READ_MEDIA_IMAGES`, `READ_EXTERNAL_STORAGE`, or `WRITE_EXTERNAL_STORAGE` permission
- camera and gallery access only through system intents and temporary URI grants
- generated debug APK is disposable public evidence, not a release artifact
