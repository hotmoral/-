# Timing Defense Cloudflare v0.31/v0.32 Parity Slice

This branch is the first production-behavior migration after the public Durable Objects PoC PASS.

## Scope
Included:
- existing v0.31 FRIEND/LINK room semantics,
- nickname/class/slot/host state,
- up to four slots,
- TEAM AI FILL reservation (max two),
- READY and READY cancel propagation,
- host-only START,
- shared authoritative `startAt = now + 2500 ms`,
- `starting -> running` gate through a Durable Object alarm,
- waiting-room refresh/reconnect,
- existing v0.31 waiting-room presentation,
- unchanged v0.32 Samsung Browser short-landscape layout fix.

Excluded:
- RANDOM matchmaking migration,
- Stage 1 combat,
- monster/base state,
- damage/EXP/coin/combo,
- v0.34 smoothing/projectiles,
- v0.35 Team Shop/Stage 2,
- numerical balance changes.

## Platform mapping
- Static game assets: existing `timing-defense-v011/` files through Workers Static Assets.
- Public root `/`: `v032-cloudflare.html`.
- Authoritative room state: SQLite-backed `TimingDefenseRoom` Durable Object.
- Live room transport: WebSocket Hibernation.
- Northeast Asia placement hint: `apac-ne`.
- No 50 ms server tick.

## Public validation gate
Android + PC must verify:
1. FRIEND/LINK create/join,
2. identical nickname/class/slot/host state,
3. READY propagation and cancellation,
4. host START disabled before all humans READY,
5. non-host cannot START,
6. one shared future `startAt`,
7. both clients cross to `running`,
8. refresh/reconnect preserves room/session/slot,
9. disconnect/reconnect does not corrupt host ownership,
10. short-landscape waiting-room controls remain visible.

Do not start v0.33 Stage 1 migration before this slice is device-PASS.
