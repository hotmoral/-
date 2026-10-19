# Timing Defense — Next Work Boundary

## Current boundary after v5

Do **not** immediately change live numerical balance and do not treat a simulation gap as authorization to patch.

Required governance:

`model → simulate → identify intentional specialization vs model artifact vs actual defect → report → discuss → explicit decision → patch`

The v5 pressure-grammar model is structurally coherent enough to continue. No class coefficient or live Stage rule was changed.

## Accepted pressure philosophy

Co-op difficulty should not be one flat HP/count multiplier.

Use three encounter-pressure families:
- `S` Swarm — temporary high-count pressure.
- `E` Elite/Heavy — one/few unusually durable threats.
- `X` Special/Mixed — disruptive special compositions.

A stage may use 1, 2 or 3 families. Do not force all three into every stage.

A 50-stage tier receives identity through:
- 1/2/3-pattern stage proportions,
- S/E/X frequency,
- internal pair/triple pressure ratios,
- event timing,
- formation geometry,
- duration/intensity,
- overlap frequency.

Higher tiers are allowed to return to many 1-pattern stages if that single pressure becomes more extreme.

See:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`

## v5 structural result

Across five representative 50-stage prototype tiers:
- 1-pattern = 40.8%
- 2-pattern = 43.6%
- 3-pattern = 15.6%

So 84.4% of stages use only one or two pressure families.

The role-coverage model across all 250 prototype stages produced:
- Knight 18.6%
- Rogue 20.1%
- Tank 20.4%
- Archer 22.0%
- Mage 18.9%

Tier-specific peaks still occurred (e.g. Rogue in durability-heavy T2, Archer in line-heavy T3, Tank in split-special T4), while Knight stayed stable as a generalist.

This supports the grammar concept but does **not** freeze exact production stage counts.

## Immediate next analysis slice — concrete spawn recipes

Translate abstract pressure budgets into actual monster recipes using the current roster:
- GRUNT
- RUNNER
- BRUTE
- SHIELD
- FLYER

Required mapping work:
1. `S` recipes — burst size, spacing, line/cluster/scatter geometry, weak/medium mix.
2. `E` recipes — which monsters become durable anchors, HP/armor scaling, one-vs-two-vs-three elite timing.
3. `X` recipes — RUNNER/FLYER/SHIELD combinations, split pressure and geometry.
4. pair/triple stages — convert abstract internal pressure shares into spawn budgets without stacking all maximum pressures at once.
5. 1-pattern extremes — define how long/intense one pressure can become without visual overload.

## Then calibrate team-size scaling

Only after concrete recipes exist, run 2/3/4-player headless calibration.

Keep class coefficients unchanged while tuning encounter pressure.

Measure:
- clear/fail rate,
- wall HP / wall hits,
- stage clear time,
- per-class target-type contribution,
- battlefield concurrency / peak living enemies,
- durable-anchor TTK,
- swarm clear delay,
- special-threat leakage,
- Average vs Skilled mastery response,
- duplicate-class compositions.

Primary question:

> Can additional players increase encounter variety and role demand without turning the battlefield into permanent visual clutter or flattening all classes into raw DPS?

## Important not-yet-frozen values

- exact 2/3/4-player pressure multiplier,
- exact monster count per S budget,
- exact E HP/armor multiplier,
- exact X composition recipes,
- final number/names/order of tiers,
- stage length,
- boss/checkpoint schedule,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync bonus magnitude / round-ID implementation.

These must not be silently invented as production decisions merely to make a simulation pass.

## Multi-skill implementation remains pending

The first playable multi-skill implementation candidate is still:
- Lv6 / Lv11 / Lv16 / Lv21 skills for all five classes,
- multi-skill HUD strip below Timing Square,
- exact straight-line Archer collision,
- current documented boss resistance rules.

Whether this implementation occurs before or after concrete co-op spawn calibration is a project sequencing decision; it is not authorized merely by v5.

## Human-play focus remains
Simulation does not replace checks for:
- impact feel / hitstop,
- VFX readability,
- Timing Square readability,
- projectile visibility,
- screen crowding during swarm events,
- whether role-switching stages remain readable,
- subjective class fun.
