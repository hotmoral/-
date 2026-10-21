# Cloudflare v0.35 Stage 2 Input Defect — 2026-10-21

## Device observation
Android + PC both reached Stage 2 after Team Shop READY/NEXT, but both clients showed:
- no Timing Square,
- local touch input did not trigger timing attacks,
- server-owned automatic/passive attacks continued.

## Classification
**CLIENT LOCAL-INPUT REACTIVATION DEFECT.**

The server Stage 2 simulation was active. This was not evidence of a Stage 2 authority failure or balance regression.

## Cause boundary
The Stage 2 transition did not robustly re-arm the local timing/input state after the Team Shop / stage-transition idle state. The base input gate requires local combat state and an active timing phase.

## Fix
Added `v035-stage2-input-guard.js` which, only for authoritative Stage 2 `combat` state:
- asserts `S.stageMode='combat'`,
- clears stale `gameOver` / `runComplete`,
- clears stale input/hit-stop locks when the local phase is inactive,
- restarts `startAttack()` only when no local attack/projectile/recover phase is active.

It does not:
- alter server damage,
- alter monster HP,
- alter EXP/coin,
- alter shop costs,
- enable local monster spawning or local damage authority.

## Validation required
Repeat Stage 1 -> Team Shop -> READY/NEXT -> Stage 2 on Android + PC and confirm:
1. Timing Square appears on both clients,
2. touch timing input works on both clients,
3. remote/projectile behavior remains synchronized,
4. authoritative Stage 2 HP/BASE HP remains identical.
