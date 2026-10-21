# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 real-game waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**

Read before execution:
1. `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`
2. `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
3. `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
4. `CLOUDFLARE_V033_STAGE1_PASS_2026-10-21.md`
5. `CLOUDFLARE_V034_RENDER_PASS_2026-10-21.md`
6. `PROJECT_STATUS.md`
7. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
8. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`

Public Cloudflare URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Validated v0.34 checkpoint:
- branch: `timing-defense-cloudflare-v034-pass-20261021`
- deployment trigger HEAD: `adc6709d51e9b076498c7c26e172478d24d9f797`

## Immediate execution group — v0.35 reconnect / Team Shop / Stage 2 parity
Do not generalize to Stage 3–10 yet. Do not alter numerical balance.

### A. Recover exact legacy v0.35 semantics
Read live v0.35 client/server code and `V035_RECONNECT_SHOP_STAGE2_REPORT.md` before implementation.

Recover exactly:
- 180 s same-server reconnect/session grace semantics,
- `/resume` and event-floor behavior,
- Stage 1 -> Team Shop transition,
- Stage-clear reward `55 + stage*12`,
- per-human authoritative coin/ranks/purchases,
- existing upgrade grammar and costs,
- purchase READY lock/unlock,
- all-human shop READY gate,
- host-only NEXT STAGE,
- synchronized future Stage 2 start,
- Stage 2 count/gap/mix and HP scaling,
- bounded Stage 2 clear,
- current shared WALL HP / DEF prototype semantics.

### B. Preserve already validated behavior
Must not regress:
- room/session/slot/host/READY/START,
- Stage 1 authoritative HP / BASE HP / EXP / charge / clear,
- v0.34 smoothing,
- remote human/AI/passive projectile VFX,
- local immediate hit presentation.

### C. Cloudflare implementation boundary
Durable Object owns:
- session identity and reconnect state,
- shop state,
- coin/ranks/purchase validation,
- shop READY / canNext / host NEXT,
- Stage 2 run authority,
- Stage 2 monster/base/player state,
- event ordering.

Client owns only:
- local input/judgment capture,
- presentation/interpolation/VFX,
- shop UI presentation.

### D. Device validation gate
Android + PC must validate:
1. Stage 1 shared run remains correct,
2. Stage 1 clear moves both clients to Team Shop,
3. reward/coin values match,
4. purchases are independent per human and server-authoritative,
5. purchase changes READY lock state correctly,
6. shop READY propagates,
7. NEXT unavailable until all humans READY,
8. non-host cannot NEXT,
9. host NEXT starts one shared future Stage 2,
10. Stage 2 GRUNT/RUNNER identities/HP/deaths/BASE HP match,
11. v0.34 smoothing/projectiles remain good,
12. Stage 2 bounded clear is shared,
13. refresh/reconnect works in Stage 1,
14. refresh/reconnect works in Team Shop,
15. refresh/reconnect works in Stage 2,
16. no historic projectile burst after reconnect.

## Closure rule
Close v0.35 only when:
- public deployment succeeds,
- Android + PC device validation passes through Stage 2,
- reconnect passes in Stage 1 / Team Shop / Stage 2,
- no balance values were silently changed,
- canonical docs are synchronized.

Only then proceed to Stage 3–10, larger-party coverage and Lv6+ multiplayer authority.

## Frozen governance
No numerical change to attack damage, monster HP, passive interval, combo coefficients, EXP, shop cost, knockback, stage count/gap or class balance without the established measure/report/discuss/explicit-decision workflow.

## Current truth boundary
Safe:
- Cloudflare v0.31/v0.32 device-PASS,
- Cloudflare v0.33 authoritative Stage 1 device-PASS,
- Cloudflare v0.34 render parity device-PASS,
- legacy v0.35 reconnect/shop/Stage-2 exists and passed local/API integration checks.

Not yet safe:
- Cloudflare v0.35 parity,
- Stage 3–10 multiplayer,
- full Lv6+ multiplayer authority,
- final numerical freeze.
