# Timing Defense — v0.33 Cloudflare Stage 1 migration preflight

Date: 2026-10-21 KST

Source contracts recovered before implementation:
- `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`
- historical `timing-defense-server/server.js` at v0.33 live HEAD `dfb369ed6aaeb8c2768f50e5a2995a7223ac921d`
- `timing-defense-v011/v033-combat-sync.js`

Scope locked to authoritative Stage 1 only.

Preserve existing values/semantics:
- GRUNT only, 8 spawns, 1120 ms gap,
- GRUNT base HP 320 with existing ordinary-monster +10% experiment,
- speed 0.070, wall damage 90, reward 6, knock resist 0.85,
- base HP 2000,
- passive 40 raw per 2.0 s per human,
- timing-tier damage / combo / EXP / charge semantics from v0.33,
- server-owned HP/death/base HP/kill/coin/progression consequences,
- client-owned local Timing Square input/judgment capture.

Cloudflare architecture change:
- do not reproduce the legacy 50 ms always-on Node simulation loop,
- advance deterministic/time-derived world state on alarm/request/message boundaries,
- use Durable Object storage + WebSocket Hibernation,
- keep rendering interpolation/presentation client-side,
- no shop, Stage 2, Lv6+ authority, or numerical rebalance in this slice.

Device gate after deployment:
1. v0.31/v0.32 room/READY/START remains intact,
2. both clients enter Stage 1 together,
3. same enemy IDs/count/HP trend,
4. A attack changes same enemy on B and vice versa,
5. base HP identical,
6. local EXP/LV/charge/combo server-confirmed,
7. AI/passive effects identical,
8. Stage 1 clear/gameover synchronized,
9. no duplicate local spawns or duplicate AI/passive authority.
