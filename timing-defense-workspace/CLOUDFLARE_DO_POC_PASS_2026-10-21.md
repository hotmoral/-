# Timing Defense — Cloudflare Durable Objects PoC PASS

Date: 2026-10-21 KST
Status: **PASS / architecture viability established**

## Scope
This checkpoint validates the isolated Cloudflare Workers + Durable Objects multiplayer architecture before production v0.35 migration.

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- health endpoint: `/api/health`

Experimental source:
- branch: `timing-defense-cloudflare-do-poc`
- directory: `timing-defense-cloudflare-poc/`

The production/live branch `timing-defense-live-v011` was intentionally not modified by this PoC.

## Public deployment checks — PASS
Validated on the public `workers.dev` deployment:
- root diagnostic UI loads,
- `/api/health` returns HTTP success and reports:
  - service `timing-defense-do-poc`,
  - version `0.1.0`,
  - transport `websocket-hibernation`,
  - authority `durable-object-event-driven`,
  - location hint `apac-ne`,
- Cloudflare production route is enabled,
- Workers Static Assets and Worker routing operate on the same public origin.

## Two-client device checks — PASS
Two independent clients completed the public multiplayer sequence.

Observed/confirmed:
1. one client created a six-character authoritative room,
2. second client joined the same room,
3. both clients appeared online in the same participant state,
4. READY propagated both ways,
5. host identity remained P1,
6. START produced the same authoritative diagnostic monster on both clients,
7. shared monster HP changed identically across clients:
   - `300 -> 200`,
   - `200 -> 100`,
   - `100 -> 0`,
8. both clients reached `CLEAR`,
9. refresh/reconnect preserved the shared room/session/slot/state,
10. the other client remained in the same shared state,
11. post-refresh interaction continued correctly.

The reconnect test closes the previously identified replacement-socket ownership race boundary for this PoC.

## Architecture conclusion
The Cloudflare architecture is viable for Timing Defense multiplayer migration.

Validated properties:
- one Durable Object per room,
- SQLite-backed durable room state,
- WebSocket Hibernation transport,
- event-driven authoritative state changes,
- no legacy 50 ms always-on simulation loop in the PoC,
- public Korea-centered `apac-ne` placement hint,
- reload/reconnect without losing the shared authoritative state.

## What this PASS does NOT mean
This is an architecture PASS, not v0.35 parity.

Not yet migrated/validated on Cloudflare:
- existing v0.31 production room UX/contract,
- v0.32 waiting-layout behavior,
- v0.33 full Stage 1 authoritative combat consequences,
- v0.34 interpolation/extrapolation and remote projectile VFX,
- v0.35 Team Shop / purchases / Stage 2 / production reconnect semantics,
- Stage 3–10,
- full Lv6+ multiplayer skill authority,
- final persistence lifetime / cleanup / invite security policy.

## Promotion decision
The PoC gate is closed as PASS.

Next authorized migration slice:
1. port the existing v0.31 room/session/READY/START contract onto Durable Object/WebSocket transport,
2. preserve v0.32 waiting-room UX/layout behavior,
3. validate Android + PC parity before introducing Stage 1 combat migration.

Only after that slice passes should v0.33 authoritative Stage 1 consequences be moved.

## Frozen guards
During migration:
- do not change combat/balance values,
- do not change approved combo display/size/position/animation,
- preserve `timing-defense-live-v011` as the v0.35 source baseline until Cloudflare migration independently reaches parity,
- classify parity defects separately from architecture defects.
