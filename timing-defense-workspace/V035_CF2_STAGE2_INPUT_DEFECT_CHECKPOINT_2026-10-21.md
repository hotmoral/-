# Cloudflare v0.35 cf.2 Stage 2 Input Defect Checkpoint

Date: 2026-10-21 KST

This checkpoint records the deployed cf.2 behavior before the root-cause fix:
- Stage 1 -> Team Shop works,
- purchases work,
- all-human shop READY and HOST NEXT work,
- authoritative Stage 2 monsters/passive attacks start,
- local Stage 2 stage-intro/Timing Square/tap input do not resume.

Root cause was subsequently identified as inherited v0.33 public run serialization hardcoding `stage: 1`, compounded by the v0.35 client manually bypassing the existing `startStage()` / v0.20 stage-intro path.

Do not treat cf.2 as PASS.
