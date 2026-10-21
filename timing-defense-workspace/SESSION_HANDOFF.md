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

Canonical next-slice preflight:
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`

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

## Post-v0.35 preflight — COMPLETE
The preflight audited the next three axes before implementation:
1. Stage 3–10 multiplayer generalization,
2. larger 3–4 slot / human+AI parties,
3. Lv6+ multiplayer skill consequence authority.

Key conclusions:
- exact legacy Stage 3–10 plans/compositions/gaps/scaling were recovered,
- future S/E/X pressure grammar remains candidate analysis data and must not replace current 10-stage prototype values during migration,
- Cloudflare has several Stage-2-only server/client/result assumptions that require one generic Stage-N path,
- server lacks BRUTE/SHIELD/FLYER, Stage 5/10 boss rules and authoritative Y geometry needed by FLYER/geometry skills,
- four-slot transport/session/READY/shop/result foundations are reusable,
- 3–4 participant + multi-hit skills require stronger event-delivery semantics than the current short fixed tail,
- actual playable legacy skill authority is Lv6/11/16/21,
- Lv26/Lv31 remain roadmap/design effects and must not be invented during migration.

## Numerical parity decision gate — implementation is paused here
Two pre-existing Cloudflare-vs-legacy numerical mismatches were discovered.
They are documented but **not patched**, because numerical changes require explicit approval.

### N1 Heavy-tier EXP
Legacy exact:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

Current Cloudflare effectively gives:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 8
- HEAVY+ 8
- GREAT 12
- SUPER 18
- CRITICAL 28

Recommendation: classify as parity defect and restore legacy exact values before Lv6+ migration.

### N2 AI stage damage scaling
Legacy AI multiplier:
`1 + (stage-1)*0.035`

Current Cloudflare omits it.

Recommendation: classify as parity defect and restore legacy exact scaling before Stage 3–10 migration.

### N3 Combo milestone attacks
Legacy experimental v0.18 has extra milestone attack rewards. Cloudflare currently implements persistent combo percentage bonus but not those milestone attacks.

Recommendation: defer to a separate explicit decision after event delivery is generalized; do not silently combine it with Stage 3 work.

## Exact next implementation after N1/N2 approval — Slice A
Do not add Stage 3 yet.

Start from exact v0.35 PASS HEAD on a new implementation branch.

Scope:
- keep Stage 1–2 flow unchanged,
- add generic server skill-authority primitives,
- implement exact existing Lv6 consequences for all five human classes,
- add action/cast identity and secondary-hit event metadata,
- keep client projectile prediction presentation-only,
- forced/API Lv5 vs Lv6 verification,
- Stage 1–2 multiplayer regression gate.

Lv6 targets:
- Knight +12% server damage; size presentation only,
- Rogue second dagger 55%, same-target allowed,
- Tank +30% server knockback,
- Archer up to 2 strict-line penetrations, no seeking,
- Mage 50% authoritative splash.

Non-goals:
- no Stage 3,
- no Lv11+,
- no Lv26/Lv31,
- no pressure-grammar replacement,
- no new team-size balance,
- no responsive-safety work.

After Slice A PASS:
- Slice B: Stage 3 only, 2 humans first, exact `12 / 980 ms / G44-R34-B22`, Stage 3 clear -> Team Shop.
- Slice C: 3H / 4H / 2H+2AI / 3H+1AI baseline and event-volume validation.
- Later bounded groups: Stage 4 SHIELD, Stage 5–6 boss+FLYER+Y geometry, Stage 7–9 mixed roster, Stage 10 final boss/result, Lv11/16/21 authority before progression depends on each milestone.

## Deferred UX item
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred until after the current migration authority work. Handle it later as a shared responsive-safety layer rather than device-specific patches.

## Legacy baseline
- repository: `hotmoral/-`
- legacy live source: `timing-defense-live-v011`
- workspace: `timing-defense-workspace`
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
- Cloudflare isolated PoC through v0.35 are device-PASS for their scoped gates,
- exact v0.35 validated deployment/checkpoint is preserved,
- post-v0.35 Stage/party/skill preflight is complete,
- legacy v0.35 reconnect/shop/Stage-2 code existed and Cloudflare parity is device-confirmed,
- Render quota incident confirmed.

Do not claim yet:
- Stage 3–10 multiplayer parity,
- full Lv6+ multiplayer authority,
- Lv26/Lv31 playable implementation,
- final persistence/security/anti-cheat architecture,
- final shop/shared-wall semantics beyond the validated v0.35 slice,
- final numerical balance.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V035_PASS_2026-10-21.md`
5. `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
6. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
7. `DESIGN_DECISIONS.md`
8. `SKILL_PLAN_LV6_31.md`
9. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
10. `TIER_PRESSURE_GRAMMAR_V1.md`
11. `PRESSURE_RECIPES_V1.md`
12. `SIMULATION_METHOD.md`
