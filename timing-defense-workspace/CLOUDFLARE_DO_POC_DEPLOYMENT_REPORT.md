# Timing Defense — Cloudflare Durable Objects PoC Deployment Report

Updated: 2026-10-21 KST

## Public deployment
- Worker: `timing-defense-do-poc`
- Public URL: `https://timing-defense-do-poc.sktjsek.workers.dev`
- Source branch: `timing-defense-cloudflare-do-poc`
- PoC source root: `/timing-defense-cloudflare-poc`
- Production branch configured to `timing-defense-cloudflare-do-poc`
- Deploy command: `npx wrangler deploy`
- Preview builds disabled

## Deployment state
Cloudflare production deployment succeeded after correcting the initial wrong-branch/root-directory configuration.

Verified by device screenshots:
1. Root URL loads the dedicated `TIMING DEFENSE · DO PoC` UI.
2. `GET /api/health` returns a successful JSON response with:
   - `ok: true`
   - `service: timing-defense-do-poc`
   - `version: 0.1.0`
   - `transport: websocket-hibernation`
   - `authority: durable-object-event-driven`
   - `locationHint: apac-ne`

Therefore the following are PASS:
- public `workers.dev` route enabled,
- static asset delivery,
- Worker routing,
- health endpoint,
- production branch/build configuration.

## Still pending — PoC authority gate
The architecture PoC is NOT yet fully PASS until two independent clients verify:
1. room creation,
2. second-client join,
3. participant synchronization,
4. READY propagation both ways,
5. host-only START,
6. one authoritative 300 HP monster appears on both clients,
7. client A attack: 300 -> 200 on both,
8. client B attack: 200 -> 100 on both,
9. third attack: 100 -> 0 and shared clear state,
10. refresh/reconnect restores same session/slot/state and accepts the next attack sequence.

Do not migrate v0.35 gameplay into this architecture until this two-client public gate passes.
