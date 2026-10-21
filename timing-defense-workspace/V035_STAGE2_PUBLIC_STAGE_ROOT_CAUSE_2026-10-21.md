# Cloudflare v0.35 Stage 2 Input Failure — Root Cause

Date: 2026-10-21 KST

## Symptom
After both players READY in Team Shop and HOST NEXT STAGE:
- no Stage 2 transition/ready/start presentation,
- authoritative Stage 2 monsters spawn immediately,
- passive/AI attacks continue,
- local Timing Square is absent,
- local tap input does not work.

## Root cause
The inherited v0.33 `TimingDefenseRoom.runPublic()` hardcodes `stage: 1` in every published run snapshot.

The v0.35 server correctly advances its internal run to Stage 2, but clients continue receiving `run.stage === 1`.

Therefore v0.35 client transition logic guarded by `run.stage === 2` never executes. This suppresses Stage 2 presentation/input re-arming while server-authoritative Stage 2 simulation continues.

## Fix
Override public run serialization in the v0.35 audit layer so `out.stage` is taken from the authoritative internal `room.run.stage`.

No numerical balance, damage, HP, EXP, shop cost, spawn count/gap, or class values are changed.

## Validation required
- health version bump distinguishes deployment,
- Stage 1 -> Team Shop -> READY -> NEXT,
- both clients show Stage 2 transition state,
- both clients regain Timing Square and tap input,
- Stage 2 server-authoritative synchronization remains intact.
