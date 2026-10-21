# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 real-game waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**

## Current v0.35 status
Cloudflare v0.35 reconnect / Team Shop / Stage 2 parity is **DEVICE VALIDATION PARTIAL PASS**.

Confirmed on device through cf.3:
- Stage 1 -> shared Team Shop,
- shop purchase,
- both-human shop READY,
- host NEXT STAGE,
- synchronized Stage 2 transition,
- `STAGE 2 / READY / START` presentation,
- Timing Square active on both clients,
- local tap attacks active,
- remote projectile VFX visible,
- bounded Stage 2 clear reached on both clients.

Known cf.3 defect:
- final board still used inherited local/single-player result data,
- title displayed `STAGE 10 CLEAR`,
- Android/PC contribution values could differ.

cf.4 candidate deployed to fix result/reporting only:
- authoritative human result values from `run.players`,
- authoritative AI kill/damage accumulation,
- authoritative stage title (`STAGE 2 CLEAR`),
- same final snapshot rendered on both clients.

Read:
- `CLOUDFLARE_V035_CANDIDATE_2026-10-21.md`
- `V035_CF3_STAGE2_FLOW_PASS_CF4_RESULT_CANDIDATE_2026-10-21.md`
- `V035_RECONNECT_SHOP_STAGE2_REPORT.md`

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Current cf.4 deployment trigger HEAD:
- `ce0151894d2a972863bd511ed95a04b808fef941`

## Immediate remaining device gate
Do not add Stage 3–10 or new multiplayer skill authority yet.

### A. cf.4 authoritative result board
1. Confirm `/api/health` reports `0.35-cf.4`.
2. Complete Stage 2 on Android + PC.
3. Both clients must show `STAGE 2 CLEAR`.
4. Human/AI KILLS, DMG, COIN, LV, MAX COMBO must match across clients.

### B. Reconnect parity
Refresh one client separately in each phase:
1. Stage 1 combat,
2. Team Shop,
3. Stage 2 combat.

For each refresh confirm:
- same room code,
- same session/slot,
- same run/stage,
- current authoritative HP/base/shop state restored,
- other client remains in the same shared state,
- no burst of historical projectile VFX is replayed.

## Closure rule
Close v0.35 only when A and B pass. Then create a preserved v0.35 PASS checkpoint and synchronize project status/handoff. Only then proceed to Stage 3–10 / larger-party validation / Lv6+ multiplayer authority.

## Frozen governance
No numerical change to attack damage, monster HP, passive interval, combo coefficients, EXP, shop cost, knockback, stage count/gap or class balance without the established measure/report/discuss/explicit-decision workflow.
