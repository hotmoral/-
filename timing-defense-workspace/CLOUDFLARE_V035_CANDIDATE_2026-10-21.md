# Cloudflare v0.35 Parity Candidate — 2026-10-21

## Status
**IMPLEMENTED / DEPLOYED / DEVICE VALIDATION PARTIAL PASS**

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

## Device validation evidence — partial PASS
Android + independent second client device run confirmed:
- Stage 1 remains playable,
- both clients enter the same Team Shop after Stage 1 clear,
- shop purchase succeeds,
- coin/rank UI updates are visible,
- both human players can READY in shop,
- host proceeds through NEXT STAGE,
- both clients transition into Stage 2,
- uploaded Samsung Browser recording visually confirms the Stage 1 -> Team Shop -> both READY -> NEXT STAGE -> Stage 2 path.

This closes the shop/transition path only. It does **not** yet close full v0.35 parity.

## Remaining device validation required
1. Stage 2 GRUNT/RUNNER HP/deaths/BASE HP match on both clients,
2. v0.34 smoothing/projectiles remain correct during Stage 2,
3. Stage 2 bounded clear is shared,
4. refresh/reconnect in Stage 1 preserves room/session/slot/run,
5. refresh/reconnect in Team Shop preserves room/session/slot/run/shop state,
6. refresh/reconnect in Stage 2 preserves room/session/slot/run,
7. other client remains in the same shared state during one-client refresh,
8. no historical projectile burst occurs after reconnect.

## Truth boundary
Do not mark Cloudflare v0.35 PASS until the remaining Stage 2 authority and reconnect gates are complete.
No numerical balance values were intentionally changed in this migration slice.
