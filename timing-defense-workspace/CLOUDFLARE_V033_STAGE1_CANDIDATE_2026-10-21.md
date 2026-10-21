# Timing Defense — Cloudflare v0.33 Stage 1 candidate

Date: 2026-10-21 KST
Status: IMPLEMENTED / DEPLOYMENT TRIGGERED / DEVICE VALIDATION PENDING

Implementation branch:
- `timing-defense-cloudflare-v033-stage1`

Cloudflare-watched deployment branch:
- `timing-defense-cloudflare-do-poc`

Current candidate/deployment HEAD:
- `dd35771a198355b0d7ff2a99e88b8e32b1c0df37`

Preserved rollback baseline:
- `timing-defense-cloudflare-v031-v032-pass-20261021`

Implemented scope:
- existing v0.31/v0.32 FRIEND/LINK waiting-room path preserved,
- shared run id/seed/startAt/combatAt,
- Stage 1 GRUNT only,
- 8 spawns / 1120 ms gap,
- existing ordinary-monster +10% HP experiment,
- authoritative monster IDs/HP/death,
- authoritative base HP / wall hits,
- client timing judgment capture + monotonic action sequence,
- server-resolved tier/damage/knockback/kill/coin/EXP/LV/charge/combo,
- server-owned passive 40/2.0 s per human,
- server-owned AI FILL attack cadence,
- synchronized Stage 1 clear/gameover,
- Durable Object alarm/event advancement instead of legacy 50 ms always-on simulation loop,
- time-derived monster position between authoritative events,
- local emergency spawning blocked during network run,
- local wall collision authority blocked by visual wall floor,
- thin entry wrapper persists overdue event advancement before message handling.

Out of scope / not claimed:
- v0.34 smoothing/projectile parity,
- Team Shop / Stage 2,
- Lv6+ server skill authority,
- Stage 3–10,
- production persistence/security/balance freeze.

Device validation gate:
1. v0.31/v0.32 room/READY/START still passes,
2. both clients enter Stage 1 together,
3. same enemy IDs/count/HP trend,
4. A attack changes the same enemy on B and vice versa,
5. base HP remains equal,
6. local EXP/LV/charge/combo follows server state,
7. passive/AI effects are identical,
8. Stage 1 clear/gameover synchronizes,
9. no duplicate local spawn / AI / passive / wall damage.

Do not mark PASS until Android + PC evidence closes this gate.
