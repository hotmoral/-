# Timing Defense — Cloudflare v0.31/v0.32 Parity Implementation Plan

Updated: 2026-10-21 KST

## Purpose
Implement the first production-parity migration slice after the Durable Objects PoC PASS.

This slice ports the existing v0.31/v0.32 waiting-room contract onto Cloudflare Durable Objects + WebSocket Hibernation without migrating Stage 1 combat.

## Recovered source contract
From `v031-network.js`, `V031_MULTIPLAYER_FOUNDATION_REPORT.md`, `v032-waiting-layout.js`, and `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`:
- TEAM FRIEND/LINK creates or joins a real six-character room.
- Share/invite URL uses `?room=<CODE>`.
- Opening an invite selects TEAM/LINK.
- Maximum total room slots: 4.
- Host occupies slot 1 on creation.
- TEAM AI FILL reserves up to two positions among P2–P4.
- Human join uses the first unoccupied/non-AI slot.
- Server owns room code/method/session/slot/host/nickname/class/READY/AI fill/status/revision.
- At least two humans and every human READY are required for START.
- Only host may START.
- START sets one authoritative future `startAt` approximately 2500 ms ahead.
- v0.32 short-landscape fix constrains the invite URL to one line and reserves action/footer space.

## Cloudflare architecture mapping
- Initial room creation: Worker HTTP route.
- Participant live transport and mutations: Durable Object WebSocket Hibernation.
- Room state: SQLite-backed Durable Object storage.
- START boundary: Durable Object alarm changes `starting` to `running` at the shared `startAt`.
- Reload recovery: per-room session identity stored locally; reconnect replaces only the prior connection for that same session.
- Host is not transferred on transient WebSocket close. Explicit leave transfers host to the lowest remaining human slot.
- No legacy 50 ms tick.

## Scope guard
Included:
- FRIEND/LINK create/join,
- nickname/class,
- slots/host,
- AI FILL reservation,
- READY and READY cancel,
- host-only START,
- shared future `startAt`,
- starting/running gate,
- waiting-room reconnect,
- existing v0.31 waiting-room presentation,
- unchanged v0.32 short-landscape CSS.

Not included:
- RANDOM matchmaking migration,
- Stage 1 monsters/combat,
- damage/EXP/coin/combo,
- v0.34 smoothing/projectiles,
- Team Shop/Stage 2,
- numerical balance changes.

## Device PASS gate
Android + PC:
1. FRIEND/LINK equivalent create/join.
2. Identical participant/slot/class/nickname state.
3. READY propagation both ways.
4. READY cancel propagation.
5. Non-host cannot START.
6. Host cannot START before every human READY.
7. Host START after readiness yields one shared `startAt`.
8. Both clients cross `starting -> running` together.
9. Refresh in waiting preserves room/session/slot.
10. Disconnect/reconnect does not corrupt host/online ownership.
11. Samsung Browser short-landscape waiting room remains usable.

Only a device PASS authorizes v0.33 Stage 1 migration.
