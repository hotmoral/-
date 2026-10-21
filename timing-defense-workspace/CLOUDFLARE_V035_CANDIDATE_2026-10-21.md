# Cloudflare v0.35 Parity Candidate — 2026-10-21

## Status
**IMPLEMENTED / DEPLOYMENT TRIGGERED / DEVICE VALIDATION PENDING**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Implementation branch:
- `timing-defense-cloudflare-v035-parity`
- implementation HEAD before deployment trigger: `d63ddf982c7a8a9bae35dbe82c4944a888280768`

Cloudflare watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- deployment trigger HEAD: `3b5e8ec65ad8f62343b86159fe48f71aebbb79be`

Validated base:
- v0.34 render parity PASS checkpoint: `timing-defense-cloudflare-v034-pass-20261021`
- validated v0.34 trigger HEAD: `adc6709d51e9b076498c7c26e172478d24d9f797`

## Implemented scope
This candidate ports only the bounded legacy v0.35 slice:
- same-session/reload recovery from Durable Object state,
- event-floor recovery to suppress historical projectile replay,
- Stage 1 -> Team Shop,
- Stage 1 reward `55 + stage*12` (67 after Stage 1),
- server-owned per-human coin/ranks/purchases,
- READY purchase lock/unlock,
- all-human shop READY gate,
- host-only NEXT STAGE,
- synchronized future Stage 2 start,
- Stage 2 authoritative GRUNT/RUNNER combat,
- Stage 2 count 10 / gap 1040 ms / 62% GRUNT 38% RUNNER,
- existing Stage 2 HP scaling and +10% ordinary non-boss experiment,
- shared WALL HP +100 and aggregate DEF prototype semantics,
- bounded Stage 2 clear,
- v0.34 render smoothing/projectile behavior retained.

## Audit findings fixed before deployment
- restored exact legacy AI interval contract: Rogue 1150 ms, Tank 1650 ms, all other classes 1400 ms,
- restored Stage 2 `starting` room status / shared `startAt` publication,
- restored Stage 2 clear room/event grammar,
- prevented duplicate reconnect WebSocket competition by preferring the existing v0.31 reconnect path and using a delayed fallback only when necessary,
- added per-room event-floor guard so v0.34 fresh-run `lastEvent=0` initialization cannot replay historical projectiles after recovery,
- removed superseded v0.35 client draft before deployment.

## Effective diff from v0.34 PASS
Only v0.35 extension files are added plus the Wrangler entry switch:
- `timing-defense-cloudflare-poc/src/v035-entry.js`
- `timing-defense-cloudflare-poc/src/v035-audit-entry.js`
- `timing-defense-cloudflare-poc/wrangler.jsonc`
- `timing-defense-v011/v035-cloudflare-v2.js`
- `timing-defense-v011/v035-event-floor-guard.js`
- `timing-defense-v011/v035-cloudflare.html`

The validated v0.34 combat/render files are not modified.

## Expected health response after deployment
- service: `timing-defense-cloudflare-v035-parity`
- version: `0.35-cf.1`
- authority: `durable-object-event-driven-stage2-shop`
- presentation: `v034-render-parity-retained`
- scope: `room-stage1-shop-stage2-reconnect`

## Device validation required
Android + PC:
1. v0.31-v0.34 room/READY/START/Stage 1 behavior remains intact,
2. Stage 1 clear moves both clients to the same Team Shop,
3. reward/coin/ranks/purchases are authoritative and synchronized,
4. READY locks purchases; un-READY unlocks them,
5. all-human READY gates NEXT,
6. non-host cannot NEXT and host can NEXT only after all humans READY,
7. Stage 2 starts from one shared future start time,
8. Stage 2 GRUNT/RUNNER HP/deaths/BASE HP match on both clients,
9. v0.34 smoothing/projectiles remain correct,
10. Stage 2 clear is shared,
11. refresh/reconnect in Stage 1, Team Shop and Stage 2 preserves room/session/slot/run,
12. other client remains in the same shared state during one-client refresh,
13. no historical projectile burst occurs after reconnect.

## Truth boundary
Do not mark Cloudflare v0.35 PASS until the above device gate is complete.
No numerical balance values were intentionally changed in this migration slice.
