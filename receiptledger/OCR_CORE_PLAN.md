# ReceiptLedger V1 OCR Core

Checkpoint: `RL_V1_OCR_CORE_01`

## Scope

- bundled Google ML Kit Korean Text Recognition v2
- OCR on the currently selected source image or perspective-corrected image
- preserve block / line / element text and geometry
- map OCR element/line corners back to canonical normalized-source coordinates
- stale-result protection when the user changes images during recognition
- lightweight OCR overlay and raw-text inspection in the app
- deterministic JVM tests for coordinate mapping/model contracts
- public CI compile/test/debug APK and permission audit

## Non-goals

- receipt row reconstruction
- product / price / quantity parsing
- arithmetic validation
- multi-pass OCR recovery
- persistence/database
- release signing
- real receipt fixtures or personal data

## OCR dependency

Bundled Korean model:
`com.google.mlkit:text-recognition-korean:16.0.1`

The bundled model is selected deliberately so runtime recognition does not depend on a first-use Play Services model download.

## Coordinate contract

Every OCR element keeps geometry in the OCR input image and in canonical source-image coordinates. When OCR runs on a perspective-corrected bitmap, `PerspectivePlan.outputToSource` is used to restore coordinates to the original EXIF-normalized source bitmap.
