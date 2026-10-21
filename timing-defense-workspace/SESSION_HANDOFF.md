# Timing Defense — Session Handoff

Updated: 2026-10-21 KST

## Current execution status
Cloudflare Workers + Durable Objects migration has four closed public device-validation gates:
- isolated architecture viability PoC — **PASS**,
- real-game v0.31/v0.32 waiting-room parity — **PASS**,
- v0.33 authoritative Stage 1 parity — **PASS**,
- v0.34 render smoothing / remote projectile parity — **PASS**.

Current next boundary: **v0.35 reconnect / Team Shop / Stage 2 parity**.

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Cloudflare watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- last validated v0.34 deployment trigger HEAD: `adc6709d51e9b076498c7c26e172478d24d9f797`

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`

## What v0.34 Cloudflare PASS established
Android + PC device validation confirmed:
- v0.33 authoritative Stage 1 remained synchronized,
- remote human projectile is visible on the other client,
- local projectile hit reaction occurs at projectile arrival without waiting for the server round trip,
- no duplicate gameplay damage from presentation projectiles,
- server authority for HP / EXP / coin / kills remains intact,
- monster presentation is acceptably smooth.

Read:
- `CLOUDFLARE_V034_RENDER_PASS_2026-10-21.md`

## Exact next action — v0.35 parity migration
Before coding, recover exact semantics from:
- `V035_RECONNECT_SHOP_STAGE2_REPORT.md`,
- live `v035-reconnect-shop.js`,
- live `timing-defense-server/server.js`,
- related v0.35 host/adapter files only as needed.

Port only:
1. same-session/reload recovery,
2. Stage 1 -> Team Shop,
3. authoritative coin/ranks/purchases,
4. purchase READY lock/unlock,
5. all-human shop READY gate,
6. host-only NEXT STAGE,
7. synchronized future Stage 2 start,
8. authoritative Stage 2 GRUNT/RUNNER combat,
9. bounded Stage 2 clear,
10. reconnect validation in Stage 1 / Team Shop / Stage 2.

Do not yet generalize Stage 3–10 or move additional Lv6+ multiplayer skill consequences.

## Legacy baseline
- repository: `hotmoral/-`
- live source: `timing-defense-live-v011`
- workspace: `timing-defense-workspace`
- latest implemented legacy prototype: **v0.35**
- last device-PASS legacy prototype: **v0.34**
- last verified legacy live HEAD before migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

Render remains suspended for **Monthly Quota Exceeded** after successful v0.35 deployments. This is classified as hosting outage, not proof of gameplay regression.

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
- Cloudflare v0.34 render parity device-PASS,
- legacy v0.35 reconnect/shop/Stage-2 code exists and passed local/API integration checks,
- Render quota incident confirmed.

Do not claim yet:
- Cloudflare v0.35 parity,
- Stage 3–10 multiplayer,
- full Lv6+ multiplayer authority,
- final persistence/security/shop/shared-wall semantics,
- final numerical balance.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V034_RENDER_PASS_2026-10-21.md`
5. `CLOUDFLARE_V033_STAGE1_PASS_2026-10-21.md`
6. `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
7. `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
8. `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`
9. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
10. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`
11. `V035_RENDER_QUOTA_OUTAGE_REPORT.md`
12. `DESIGN_DECISIONS.md`
13. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
14. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
15. `SKILL_PLAN_LV6_31.md`
16. `TIER_PRESSURE_GRAMMAR_V1.md`
17. `PRESSURE_RECIPES_V1.md`
18. `SIMULATION_METHOD.md`
