# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 real-game waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**

## Current v0.35 status
Cloudflare v0.35 reconnect / Team Shop / Stage 2 parity is **DEVICE VALIDATION PARTIAL PASS**.

Confirmed on device:
- Stage 1 -> shared Team Shop,
- shop purchase,
- coin/rank update presentation,
- both-human shop READY,
- host NEXT STAGE,
- both clients enter Stage 2.

Read:
- `CLOUDFLARE_V035_CANDIDATE_2026-10-21.md`
- `V035_RECONNECT_SHOP_STAGE2_REPORT.md`

Public Cloudflare URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Current deployment candidate:
- implementation branch: `timing-defense-cloudflare-v035-parity`
- watched deployment trigger HEAD: `3b5e8ec65ad8f62343b86159fe48f71aebbb79be`

## Immediate remaining device gate
Do not add Stage 3–10 or new multiplayer skill authority yet.

### A. Stage 2 authority parity
Using Android + PC in the same run, confirm:
1. same GRUNT/RUNNER identities,
2. same monster HP/deaths,
3. same BASE HP,
4. remote attacks affect the same authoritative monsters,
5. v0.34 smoothing/projectiles remain correct,
6. Stage 2 bounded clear occurs on both clients.

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
- the other client remains in the same shared state,
- no burst of historical projectile VFX is replayed.

## Closure rule
Close v0.35 only when both A and B pass. Then:
- create a preserved v0.35 PASS checkpoint branch,
- synchronize `PROJECT_STATUS.md`, `SESSION_HANDOFF.md`, and PASS report,
- only then proceed to Stage 3–10 / larger-party validation / Lv6+ multiplayer authority.

## Frozen governance
No numerical change to attack damage, monster HP, passive interval, combo coefficients, EXP, shop cost, knockback, stage count/gap or class balance without the established measure/report/discuss/explicit-decision workflow.

## Current truth boundary
Safe:
- Cloudflare v0.31/v0.32 device-PASS,
- Cloudflare v0.33 authoritative Stage 1 device-PASS,
- Cloudflare v0.34 render parity device-PASS,
- Cloudflare v0.35 Stage 1 -> Team Shop -> shop READY/NEXT -> Stage 2 transition is device-confirmed.

Not yet safe:
- full Cloudflare v0.35 parity PASS,
- Stage 3–10 multiplayer,
- full Lv6+ multiplayer authority,
- final numerical freeze.
