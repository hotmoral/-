# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Persistent planning/balance branch: `timing-defense-workspace`
- Live playable branch: `timing-defense-live-v011`
- Live prototype: `v0.15`
- Play URL: https://timing-defense-v011.onrender.com/v015.html

The workspace branch is the source of truth for design decisions, balance interpretation, simulation reports and session handoff. The live branch is separate so analysis/documentation changes do not deploy automatically.

## Current playable state
- Five classes: Knight / Rogue / Tank / Archer / Mage.
- Live growth implementation: Lv6 skill layer only.
- Planned unlocks: `Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.
- Current playable stage prototype: 1–10.
- Run EXP / coins / shop reset each run.

## Frozen class-role decisions
- Knight: generalist / stable frontline / penetration / strong heavy.
- Rogue: fast multihit / crit / high-HP normal execution.
- Tank: team-specialist / knockback / wall protection / battlefield control. Fresh-run solo Stage-10 parity is NOT required.
- Archer: straight-line geometric penetration only. No retargeting/homing/automatic next-enemy chain.
- Mage: density specialist / area burst / chained explosions.

## Frozen boss/progression decisions
- Rogue dagger hits have no same-target hit cap.
- Boss dagger damage scalar starting value: `0.70`.
- Boss knockback scalar starting value: `0.40`.
- EXP remains tied to timing attack results/events.
- Faster-killing classes are not compensated merely because they perform fewer attacks.

## Player-mastery interpretation
`Skilled` ≈ N10 / G50 / P40 plus modestly faster commitment than Average.

This is treated as an attainable learned-player state, not an extreme expert-only state. Strong Average→Skilled improvement is desirable.

## Balance governance
Never patch solely because simulation shows a large performance gap.

Required order:
`model/simulate → identify cause → report → discuss → explicit decision → live patch`

## Simulation status

### v1 — role separation
Established the intended class identity split.

### v2 — Stage 1–10 + run shop
- exposed Archer auto-chain model artifact,
- froze Archer to true straight-line penetration,
- accepted Tank solo weakness as role specialization,
- retained EXP/attack-count coupling.

### v3 — mastery curve
- confirmed useful Average→Skilled progression,
- confirmed cadence is a real skill dimension,
- no live change.

### v4 — team composition / co-op role isolation
Deliberate volume: 13,780 runs.

Main findings:
- Tank produces real team defensive value under meaningful wall pressure.
- Rogue takes disproportionate BRUTE/SHIELD kills in mixed teams.
- Archer wins long-line geometry; Mage wins dense-cluster geometry.
- Knight remains a strong stabilizing generalist.
- current unscaled Stage 1–10 waves saturate at 3–4 players.
- double-Knight remains a re-test flag only because exact playable Knight penetration is not implemented yet.

Report: `BALANCE_SIM_REPORT_V4_TEAM.md`

### v5 — latest: Tier Pressure Grammar / role opportunity
The co-op pressure philosophy is now formalized structurally.

Pressure families:
- `S` Swarm = temporary high-count pressure.
- `E` Elite/Heavy = one/few unusually durable threats.
- `X` Special/Mixed = disruptive speed/flight/shield/split compositions.

Important decision:
- a stage may use 1, 2 or 3 pressure families,
- do NOT force all three into every stage,
- tier identity comes from stage-type proportions, S/E/X frequency, internal pressure ratios, geometry, timing, duration/intensity and overlap,
- higher tier does NOT automatically mean more pattern types; high tiers may return to extreme 1-pattern stages.

Five representative 50-stage prototypes were tested:

| Tier | 1-pattern | 2-pattern | 3-pattern | Identity |
|---|---:|---:|---:|---|
| T1 Foundations | 30 | 17 | 3 | balanced pressure literacy |
| T2 Breakers | 21 | 23 | 6 | elite/durability |
| T3 Rushline | 17 | 25 | 8 | swarm + line/special tempo |
| T4 Crossfire | 11 | 25 | 14 | mixed/split special pressure |
| T5 Extremes | 23 | 19 | 8 | focused extremes / late spikes |

Across 250 prototype stages:
- 1-pattern = 40.8%
- 2-pattern = 43.6%
- 3-pattern = 15.6%
- therefore 84.4% use only one or two pressure families.

Structural class role-coverage across all 250 prototype stages:
- Knight 18.6%
- Rogue 20.1%
- Tank 20.4%
- Archer 22.0%
- Mage 18.9%

Tier-local specialist peaks still appear:
- Rogue peaks in T2,
- Archer peaks in T3,
- Tank peaks in T4,
- Knight remains comparatively stable.

This is a structural opportunity score, not final DPS share.

Files:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`

## Current skill-design candidate through Lv21
See `SKILL_PLAN_LV6_31.md`.

Through Lv21:
- Knight: Lv6 +12% blade-wave damage; Lv11 penetration; Lv16 PERFECT enhancement; Lv21 large heavy blade wave.
- Rogue: Lv6 second dagger 55%; Lv11 +6%p crit; Lv16 PERFECT cycle reduction; Lv21 five-dagger heavy.
- Tank: Lv6 width/knockback; Lv11 wall incoming damage -10%; Lv16 80 shield / 3 s refresh/non-stack; Lv21 broad heavy shockwave.
- Archer: Lv6 straight-line penetration; Lv11 speed +25% and damage +10%; Lv16 PERFECT armor-ignore/preserved penetration; Lv21 triple shot.
- Mage: Lv6 burst; Lv11 larger/stronger burst; Lv16 outer-ring resonance excluding center target; Lv21 greater arcane orb.

These remain candidate values, not automatic deploy authority.

## Exact next work boundary
Do NOT patch live difficulty or class coefficients yet.

Next analysis slice:
1. translate abstract S/E/X pressure budgets into concrete recipes using GRUNT/RUNNER/BRUTE/SHIELD/FLYER,
2. define candidate swarm sizes, elite HP/armor packages and special compositions,
3. preserve v5 timing/ratio/geometry grammar,
4. run 2/3/4-player headless calibration,
5. measure clear rate, wall HP, peak enemy concurrency/readability, target-type contribution and Average→Skilled response,
6. report before any live difficulty change.

Still unresolved:
- exact 2/3/4-player scaling multipliers,
- exact S count / E durability / X recipe values,
- final number/names/order of tiers,
- final stage length and boss/checkpoint schedule,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync round/bonus implementation.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `DESIGN_DECISIONS.md`
4. `TIER_PRESSURE_GRAMMAR_V1.md`
5. `SKILL_PLAN_LV6_31.md`
6. `BALANCE_SIM_REPORT_V4_TEAM.md`
7. `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
8. `SIMULATION_METHOD.md`
9. `NEXT_WORK.md`

Older v1/v2/v3 reports remain available for historical reasoning and numerical provenance.
