# Timing Defense — Session Handoff

Updated: 2026-10-21 KST

## Current execution status
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Closed public/device-validation gates:
- isolated Durable Objects viability PoC — **PASS**
- v0.31/v0.32 waiting-room parity — **PASS**
- v0.33 authoritative Stage 1 parity — **PASS**
- v0.34 render smoothing / remote projectile parity — **PASS**
- v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Cloudflare watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- exact v0.35 validated HEAD: `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- validated health version: `0.35-cf.7`

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`

Canonical closure report:
- `CLOUDFLARE_V035_PASS_2026-10-21.md`

## What v0.35 PASS established
Android + PC multiplayer validation confirmed the scoped Stage 1 -> Team Shop -> Stage 2 run:
- authoritative shared combat state,
- authoritative monster HP/death and BASE HP,
- EXP/charge/run progression synchronization,
- Team Shop purchase/coin/rank authority,
- immediate purchase pending feedback with duplicate-tap protection,
- all-human READY gate,
- host-only NEXT STAGE,
- synchronized Stage 2 `STAGE / READY / START`,
- Stage 2 Timing Square and direct input,
- Stage 2 GRUNT/RUNNER authoritative combat and bounded clear,
- remote projectile visibility and local immediate-hit presentation,
- authoritative result board with actual run participants and contribution values,
- reconnect gate,
- Rogue CHARGE palette/flicker correction,
- remote human timing-projectile visual parity.

No numerical balance values were intentionally changed while closing cf.3-cf.7 defects.

## Important v0.35 defects that were fixed
- inherited public snapshot hardcoded `stage: 1`, preventing Stage 2 client transition,
- Stage 2 bypassed the legacy `startStage(2)` intro/input initialization path,
- legacy result board used local/single-player state and hardcoded `STAGE 10 CLEAR`,
- result KILL COIN initially used wallet balance rather than cumulative monster-kill contribution,
- Team Shop lacked in-flight purchase feedback,
- inherited v0.24 Rogue Timing Square temporarily rendered base square as Knight,
- remote human timing hits shared the simplified passive/automatic projectile visual.

## Exact next boundary
**Do not start broad implementation immediately. Perform a bounded preflight first.**

Next migration slice must audit and scope:
1. Stage 3–10 multiplayer generalization,
2. larger-party (3–4 slot / human+AI) validation,
3. Lv6+ multiplayer skill consequence authority.

For Lv6+ effects, explicitly classify each effect as:
- presentation-only,
- client prediction + server confirmation,
- server-authoritative combat consequence.

For Stage 3–10, inspect the existing stage plan, composition, gap and scaling rules before generalizing the Stage 2 implementation. Do not silently change any numerical values.

For larger parties, validate slot/host/READY/reconnect/result/event-volume behavior separately.

Read `NEXT_WORK.md` for the preflight deliverable and acceptance boundary.

## Deferred UX item
Heterogeneous phone-size/aspect-ratio responsive safety is intentionally deferred until after the current migration closure. Handle later as a shared responsive-safety layer rather than device-specific patches.

## Legacy baseline
- repository: `hotmoral/-`
- legacy live source: `timing-defense-live-v011`
- planning/status branch: `timing-defense-workspace`
- latest implemented legacy prototype: **v0.35**
- last legacy Android + PC device-PASS before Cloudflare migration: **v0.34**
- last verified legacy live HEAD before migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

Render remains suspended for **Monthly Quota Exceeded**. This is classified as a hosting outage, not gameplay-regression evidence.

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
- Cloudflare PoC through v0.35 are device-PASS for their scoped validation gates,
- exact v0.35 validated deployment/checkpoint is preserved,
- legacy v0.35 reconnect/shop/Stage-2 code existed and Cloudflare parity is now device-confirmed,
- Render quota incident confirmed.

Do not claim yet:
- Stage 3–10 multiplayer parity,
- full Lv6+ multiplayer authority,
- final persistence/security/anti-cheat architecture,
- final shop/shared-wall semantics beyond the validated v0.35 slice,
- final numerical balance.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V035_PASS_2026-10-21.md`
5. `CLOUDFLARE_V034_RENDER_PASS_2026-10-21.md`
6. `CLOUDFLARE_V033_STAGE1_PASS_2026-10-21.md`
7. `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
8. `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
9. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
10. `DESIGN_DECISIONS.md`
11. `SKILL_PLAN_LV6_31.md`
12. `TIER_PRESSURE_GRAMMAR_V1.md`
13. `PRESSURE_RECIPES_V1.md`
14. `SIMULATION_METHOD.md`
