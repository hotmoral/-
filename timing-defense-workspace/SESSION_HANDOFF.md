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

Five classes are playable: Knight / Rogue / Tank / Archer / Mage.
Current live growth implementation contains the Lv6 skill layer only.
Planned unlock levels are:

`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Stage prototype is 1–10. Run EXP, coins and shop upgrades reset each run.

## Frozen class-role decisions

- Knight: generalist / stable frontline / penetration / strong heavy.
- Rogue: fast multihit / crit / high-HP normal target execution.
- Tank: team-specialist / knockback / wall protection / battlefield control. Fresh-run solo Stage-10 parity is NOT required.
- Archer: straight-line geometric penetration only. No retargeting, homing or automatic next-enemy chaining.
- Mage: density specialist / area burst / chained explosions.

## Frozen boss interaction rules for the next implementation candidate

- Rogue dagger hits have no same-target hit cap.
- Boss dagger damage scalar: `0.70` starting value.
- Boss knockback scalar: `0.40` starting value.
- These are tuning values, but they are NOT to be changed automatically from simulation output.

## Frozen progression philosophy

- EXP stays tied to timing attack results/events.
- Faster-killing classes are not compensated merely because they perform fewer attacks and therefore may gain EXP more slowly.
- `Skilled` simulation profile means approximately `NORMAL 10% / GOOD 50% / PERFECT 40%`, plus modestly faster attack commitment than Average.
- Strong Skilled performance is acceptable because player mastery is intended to materially reduce difficulty.
- The user expects players to reach Skilled consistency relatively quickly; preserve room for that mastery progression.

## Balance governance

**Never patch solely because a simulation exposes a large performance gap.**

Required order:

`simulate → identify cause/model artifact/intentional specialization → report → discuss with user → explicit decision → only then patch live gameplay`

This rule is important. Tank's low solo clear, for example, is currently intentional role specialization rather than authorization to buff Tank.

## Simulation status

### v1
Role-scenario validation established the intended identity split:
- Rogue strongest vs durable normal targets.
- Archer strongest in aligned line packs.
- Mage strongest in dense clusters.
- Tank strongest in wall preservation/control.
- Knight stable generalist.

### v2
Added run shop and Stage 1–10 campaign simulation. Important discoveries:
- permissive Archer auto-chain penetration badly overestimated Archer, so penetration semantics were explicitly frozen to straight-line geometry.
- Tank's poor solo result was discussed and accepted as team specialization.
- EXP/attack-count coupling was discussed and intentionally retained.

Report: `BALANCE_SIM_REPORT_V2.md`

### v3 — latest completed validation
Average→Skilled mastery curve was simulated after the above decisions were frozen.

Main 500-seed/class confirmation:

| PERFECT | Knight clear | Rogue clear | Archer clear | Mage clear |
|---:|---:|---:|---:|---:|
| 30.0% | 32.6% | 0.0% | 12.4% | 19.4% |
| 32.5% | 54.8% | 1.0% | 36.8% | 43.0% |
| 35.0% | 79.8% | 5.2% | 60.2% | 73.8% |
| 37.5% | 94.8% | 15.8% | 80.8% | 92.6% |
| 40.0% | 98.4% | 32.8% | 94.6% | 97.0% |

Interpretation:
- Knight / Archer / Mage show a useful mastery curve.
- Rogue remains a specialist and should be evaluated in team context before any solo-driven adjustment.
- Tank solo curve is intentionally non-normative.
- Timing cadence matters strongly in addition to raw judgment accuracy.
- No live balance patch was authorized or applied.

Report: `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`

## Current skill-design candidate through Lv21

See `SKILL_PLAN_LV6_31.md` for complete Lv6–31 plan. Through Lv21, notable candidate values are:

- Knight: Lv6 +12% blade-wave damage; Lv11 penetration; Lv16 PERFECT enhancement; Lv21 large heavy blade wave.
- Rogue: Lv6 second dagger 55%; Lv11 +6%p class crit; Lv16 PERFECT cycle reduction; Lv21 five-dagger heavy.
- Tank: Lv6 width/knockback enhancement; Lv11 wall incoming damage -10%; Lv16 80 shield / 3 s refresh non-stack; Lv21 broad heavy shockwave.
- Archer: Lv6 straight-line penetration; Lv11 speed +25% and damage +10%; Lv16 PERFECT armor-ignoring preserved penetration; Lv21 triple shot.
- Mage: Lv6 burst; Lv11 larger/stronger burst; Lv16 outer-ring resonance excluding original center target; Lv21 greater arcane orb.

These are candidate implementation values, not authority to deploy without the normal discussion/implementation boundary.

## Exact next work boundary

Do NOT immediately alter live numerical balance.

Highest-value next analysis:

**team-composition / co-op role simulation**

Focus:
- 2 / 3 / 4 player compositions under identical seeded waves.
- quantify Tank survival contribution without demanding solo parity.
- verify Rogue's high-HP-normal niche has real team value.
- detect excessive Archer+Mage crowd-clear overlap.
- confirm Knight remains useful as a generalist.
- preserve local-player timing mastery as the main skill component; teammate automation/synchronization assumptions must be documented explicitly.

After that simulation, report findings first and discuss them before any live patch.

## New-session read order

1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `DESIGN_DECISIONS.md`
4. `SKILL_PLAN_LV6_31.md`
5. `BALANCE_SIM_REPORT_V2.md`
6. `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`
7. `NEXT_WORK.md`
