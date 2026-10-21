# Timing Defense — Cloudflare v0.31/v0.32 Parity Implementation Report

Updated: 2026-10-21 KST

## Status
Implementation complete; public Cloudflare deployment/device validation pending.

## Branch / HEAD
- implementation branch: `timing-defense-cloudflare-v031-parity`
- implementation HEAD: `610236a617531ba9d9d428348e3983d2bb848c86`
- base/frozen PoC branch: `timing-defense-cloudflare-do-poc`
- frozen PoC checkpoint before parity work: `04ee9c2237089a5105fa4f829565f6f50ff248a8`

## Production source preservation
`timing-defense-live-v011` is unchanged by this migration implementation.

## Implemented files
- `timing-defense-cloudflare-poc/src/index.js`
  - lobby-only Durable Object authority,
  - FRIEND/LINK room metadata,
  - host/session/slot/nickname/class/AI FILL/READY,
  - host-only START,
  - shared `startAt = now + 2500 ms`,
  - Durable Object alarm for `starting -> running`,
  - WebSocket Hibernation reconnect ownership guard,
  - explicit leave/host transfer.
- `timing-defense-v011/v031-cloudflare-network.js`
  - preserves existing v0.31 waiting-room DOM/presentation contract,
  - replaces HTTP+SSE live transport with same-origin WebSocket,
  - real `?room=<CODE>` invite/link,
  - local session identity for waiting-room refresh recovery,
  - saved-session `?room=` reload automatically reopens waiting room,
  - fresh invite users still choose nickname/class before joining.
- `timing-defense-v011/v032-cloudflare.html`
  - existing game stack,
  - Cloudflare lobby adapter instead of legacy `v031-network.js`,
  - unchanged `v032-waiting-layout.js` loaded after the network adapter.
- `timing-defense-cloudflare-poc/wrangler.jsonc`
  - existing `timing-defense-v011/` served directly as Workers Static Assets,
  - Worker-first only for root/API/WebSocket routes,
  - `html_handling: none` to preserve the legacy loader's exact `.html` fetch behavior.
- `timing-defense-cloudflare-poc/V031_PARITY.md`
  - scope and device gate.

## Scope guards
Not implemented in this slice:
- RANDOM matchmaking migration,
- Stage 1 combat,
- monster/base state,
- damage/EXP/coin/combo,
- v0.34 smoothing/projectiles,
- v0.35 Team Shop/Stage 2,
- numerical balance changes.

The diagnostic monster/attack behavior from the PoC was removed from the parity branch server so this branch cannot accidentally be treated as Stage 1 migration.

## Audit fixes before deployment
1. Preserved host ownership across transient WebSocket disconnect/reconnect; host transfer happens only on explicit leave.
2. Reconnect uses active connection IDs so the replaced old socket cannot mark the new connection offline.
3. Added saved-session auto-resume for `?room=` refresh while keeping fresh invite behavior unchanged.
4. Set Workers Static Assets `html_handling: none`; default HTML canonical redirects could interfere with the legacy `index.html` bootstrap fetch.

## Public deployment next step
Change the existing Cloudflare Worker project's Production branch from:
- `timing-defense-cloudflare-do-poc`

to:
- `timing-defense-cloudflare-v031-parity`

Keep:
- Root directory: `/timing-defense-cloudflare-poc`
- Deploy command: `npx wrangler deploy`
- existing build API token.

Then inspect the automatic build before device validation.

## Device PASS gate
Android + PC must prove:
1. FRIEND/LINK create/join,
2. same nickname/class/slot/host state,
3. READY propagation,
4. READY cancel propagation,
5. non-host cannot START,
6. host cannot START until all humans READY,
7. one shared future `startAt`,
8. both clients cross `starting -> running`,
9. waiting-room refresh preserves room/session/slot,
10. transient disconnect/reconnect preserves host/online ownership,
11. v0.32 Samsung Browser short-landscape controls remain visible.

Do not start v0.33 Stage 1 migration until this gate is device-PASS.
