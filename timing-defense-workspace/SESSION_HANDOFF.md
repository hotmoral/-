# Timing Defense — Session Handoff

Updated: 2026-10-21 KST

## Current execution status
Cloudflare Workers + Durable Objects migration has three closed public device-validation gates:
- isolated architecture viability PoC — **PASS**,
- real-game v0.31/v0.32 waiting-room parity — **PASS**,
- v0.33 authoritative Stage 1 parity — **PASS**.

Current active candidate: **v0.34 render smoothing / remote projectile parity**.

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Cloudflare watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- current v0.34 deployment trigger HEAD: `adc6709d51e9b076498c7c26e172478d24d9f797`

Implementation branch:
- `timing-defense-cloudflare-v034-render`
- implementation commit: `c78765b2c29b1ab0812e64c6de7a8ca3b379c2cc`

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`

## What v0.33 Cloudflare PASS established
Android + PC device validation confirmed:
- shared authoritative Stage 1,
- same monster HP/deaths,
- cross-device attacks affect the same world state,
- same BASE HP,
- same EXP / charge,
- shared Stage 1 clear,
- no duplicate client enemy spawning or wall-damage authority observed.

Read `CLOUDFLARE_V033_STAGE1_PASS_2026-10-21.md`.

## Why v0.34 is the current slice
Video/device review identified two presentation issues while authority remained correct:
1. remote player projectile was not visible,
2. local projectile reached the monster before visible hit response because presentation waited for server confirmation.

The v0.34 candidate fixes only presentation:
- monster object reconciliation by server id,
- smooth time-derived target following,
- remote human / AI / passive projectile VFX from authoritative events,
- local projectile-arrival visual impact immediately,
- no local HP/progression mutation from predicted visuals,
- duplicate local flash/particle suppression when server confirmation arrives.

The v0.33 Durable Object combat server is unchanged by this v0.34 candidate.

Read `CLOUDFLARE_V034_RENDER_CANDIDATE_2026-10-21.md`.

## Exact next action
Device-test v0.34 on Android + PC:
1. confirm `/api/health` reports `0.34-cf.1`,
2. join same room and READY/START,
3. verify shared HP / BASE HP / EXP / charge / Stage 1 clear remains identical,
4. verify remote human projectile is visible,
5. verify local hit visually reacts at projectile arrival,
6. verify no double flash / double damage number,
7. verify no presentation projectile applies duplicate damage,
8. verify monster movement is smooth on Android.

Only after this PASS may migration proceed to v0.35 reconnect / Team Shop / Stage 2.

## Legacy baseline
- repository: `hotmoral/-`
- live source: `timing-defense-live-v011`
- workspace: `timing-defense-workspace`
- latest implemented legacy prototype: **v0.35**
- last device-PASS legacy prototype: **v0.34**
- last verified legacy live HEAD before migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

Render remains suspended for **Monthly Quota Exceeded** after successful v0.35 deployments. This remains classified as hosting outage, not proof of gameplay regression.

## Frozen governance
- Rhythm: `X -> X -> X -> X+Y`.
- Knight stable generalist / penetration / strong heavy.
- Rogue multihit / crit; same-target dagger hits uncapped.
- Tank knockback / wall protection / team specialist.
- Archer strict straight-line trajectory; no seeking/bending.
- Mage density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP only from valid timing events; passive gives no EXP.
- Current combo display/size/position/animation remains frozen unless explicitly changed.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent `5/8/12/15%` candidate,
- combo milestone raw-equivalent `60/90/150/210` cap.

No numerical balance change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.

## Truth boundary
Safe claims:
- Cloudflare isolated PoC device-PASS,
- Cloudflare v0.31/v0.32 waiting-room parity device-PASS,
- Cloudflare v0.33 authoritative Stage 1 device-PASS,
- legacy v0.34 smoothing/projectile behavior device-PASS,
- legacy v0.35 reconnect/shop/Stage-2 code exists and passed local/API integration checks,
- Render quota incident confirmed.

Do not claim yet:
- Cloudflare v0.34 render parity PASS,
- Cloudflare v0.35 parity,
- Stage 3–10 multiplayer,
- full Lv6+ multiplayer authority,
- final persistence/security/shop/shared-wall semantics,
- final numerical balance.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V033_STAGE1_PASS_2026-10-21.md`
5. `CLOUDFLARE_V034_RENDER_CANDIDATE_2026-10-21.md`
6. `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
7. `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
8. `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`
9. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`
10. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
11. `V035_RENDER_QUOTA_OUTAGE_REPORT.md`
12. `DESIGN_DECISIONS.md`
13. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
14. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
15. `SKILL_PLAN_LV6_31.md`
16. `TIER_PRESSURE_GRAMMAR_V1.md`
17. `PRESSURE_RECIPES_V1.md`
18. `SIMULATION_METHOD.md`
