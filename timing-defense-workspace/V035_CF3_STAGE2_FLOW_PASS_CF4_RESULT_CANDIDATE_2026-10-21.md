# Timing Defense — Cloudflare v0.35 cf.3 Stage 2 Flow PASS / cf.4 Result Candidate

Date: 2026-10-21 KST

## Device evidence
Android + PC confirmed on cf.3:
- Stage 1 -> Team Shop,
- purchases,
- both-human READY,
- host NEXT STAGE,
- Stage 2 `STAGE 2 / READY / START` flow,
- Timing Square active on both clients,
- local tap attacks active,
- remote projectile VFX visible,
- Stage 2 reaches bounded clear.

## Remaining cf.3 defect
The final result board was still inherited from the local/single-player result layer:
- title incorrectly displayed `STAGE 10 CLEAR`,
- KILLS / DMG / COIN / LV / MAX COMBO were taken from each client's local presentation state,
- therefore Android and PC could display different result values.

Root cause: `v023-results.js` reads local `S.v019Stats` and hardcodes `STAGE 10 CLEAR` when `S.runComplete` is true.

## cf.4 candidate
Implementation branch: `timing-defense-cloudflare-v035-parity`
Deployment watched branch: `timing-defense-cloudflare-do-poc`
Deployment trigger HEAD: `ce0151894d2a972863bd511ed95a04b808fef941`

Changes are result/reporting only:
- human result metrics read from authoritative `run.players`,
- AI damage/kills are accumulated on the Durable Object and exposed in public run state,
- final board title uses authoritative stage (`STAGE 2 CLEAR` for current bounded v0.35),
- final board is rendered from the same server snapshot on every client,
- inherited local result board is suppressed only during authoritative final rendering.

No combat-balance values or authority rules were changed.

## Remaining validation
1. Confirm `/api/health` reports `0.35-cf.4`.
2. Complete Stage 2 with Android + PC.
3. Confirm both clients show `STAGE 2 CLEAR`.
4. Confirm both clients show the same human/AI contribution values.
5. Then validate reconnect in Stage 1 / Team Shop / Stage 2 before closing v0.35.
