# ReceiptLedger V1 Layout Core

Checkpoint: `RL_V1_LAYOUT_CORE_01`

## Scope

- ignore ML Kit block/line grouping for canonical receipt-row reconstruction
- flatten non-blank OCR elements that have input geometry
- estimate dominant text-row skew from element quadrilaterals
- group elements by skew-corrected vertical position
- sort every reconstructed row by horizontal position
- retain element input/source geometry for downstream parsing provenance
- expose reconstructed rows in the debug UI
- deterministic JVM regression tests with deliberately shuffled OCR elements
- public CI compile/test/debug APK and offline permission audit

## Non-goals

- merchant/date/total parsing
- product/price/quantity association
- arithmetic validation
- OCR recovery/multi-pass fusion
- persistence/database
- release signing
- real receipt fixtures

## Coordinate rule

Layout analysis always uses `OcrElement.inputQuad` because that coordinate space is the actual OCR image (original or perspective-corrected). `OcrElement.sourceQuad` remains attached to each token for later mapping back to the EXIF-normalized source image.
