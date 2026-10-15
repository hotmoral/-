# ReceiptLedger V1 OCR Quality / Recovery Core

Checkpoint: `RL_V1_OCR_RECOVERY_CORE_01`

## Pass policy
1. ORIGINAL: current displayed original or perspective-corrected bitmap
2. CONTRAST: bounded recovery bitmap, grayscale percentile contrast stretch
3. BINARY: same recovery bitmap mutated in-place with local adaptive threshold

Maximum passes: 3. Strong original recognition stops immediately.

## Candidate selection
Every OCR document is run through Layout → Structure → Item Tuple → Validation. Selection uses structural quality, not raw character count alone.

Signals include:
- raw chars / OCR elements
- item count / partial tuple count
- date and total presence
- receipt validation status

A later pass is selected only when its score is strictly better. No text rows are blindly merged in this checkpoint.

## Memory and coordinate safety
- recovery bitmap max edge 3200
- recovery bitmap max 6,000,000 pixels
- only one recovery bitmap is alive; it is reused for binary pass
- OOM/preprocess failure falls back to best completed pass
- recovery coordinates map back to normalized source coordinates
- UI overlay maps source coordinates back into current display coordinates

## Non-goals
- cross-pass row merging
- crop-specific quantity re-OCR
- receipt corpus regression images in public repo
