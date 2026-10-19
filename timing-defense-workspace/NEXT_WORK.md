# Timing Defense — Next Work Boundary

## Current boundary after v6

Do **not** change live numerical balance merely because a simulation exposes a gap.

Required governance:
`model → simulate → identify specialization/artifact/defect → report → discuss → explicit decision → patch`

The v6 concrete pressure-recipe model is coherent enough to stop abstract encounter tuning for now.

## Accepted encounter state

Pressure grammar:
- `S` Swarm,
- `E` Elite/Heavy,
- `X` Special/Mixed.

Rules:
- X is the main co-op scaling language.
- S/E are timed spikes.
- 1/2/3-pattern stages are all valid.
- all three families are not required every stage.
- higher tier does not automatically mean more active pattern types.
- geometry/timing/internal ratios are gameplay data.

See:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `PRESSURE_RECIPES_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
- `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`

## v6 concrete recipe status

Candidate Swarm burst sizes:
- line 2P/3P/4P = 8 / 11 / 14,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

Current candidate P95 4-second spawn density:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

E remains an effective durability budget, not a literal single-monster HP multiplier.

X scales mainly by role-bearing composition rather than blanket HP.

Concrete recipe structural opportunity remains broad across all five classes.

## Why encounter tuning pauses here

A fully capable all-human candidate-Lv21 model still over-saturates toward 100% clear in representative slices, while a conservative current-AI teammate bound produces meaningful pressure.

Therefore final co-op difficulty cannot be frozen until:
1. exact Lv11–21 playable behavior exists,
2. exact Archer straight-line collision exists,
3. multiplayer human cadence assumptions can be mirrored more faithfully.

Further numeric recipe tuning before that would optimize against simulation assumptions rather than the actual game.

---

# Immediate next implementation slice

Implement the first playable **multi-skill growth block**:

### All five classes
- Lv6
- Lv11
- Lv16
- Lv21

### Required systemic changes
- multi-skill HUD strip below Timing Square,
- exact straight-line Archer penetration/collision,
- current boss dagger scalar = 0.70,
- current boss knockback scalar = 0.40,
- Mage Lv16 Resonance excludes original center target,
- Tank Lv11 wall reduction = 10%,
- Tank Lv16 wall shield = 80 / 3 s / refresh-only / non-stack,
- Lv21 class-specific heavy transformation.

Use `SKILL_PLAN_LV6_31.md` as the candidate formula source.

## Implementation discipline
Do not simultaneously redesign stage difficulty while implementing Lv6–21.

The implementation objective is **formula fidelity + readable VFX/UI**, not difficulty tuning.

After implementation:
1. extract exact code formulas back into the headless simulator,
2. rerun the concrete v6 pressure recipes,
3. compare 2/3/4-player role and mastery behavior,
4. flag suspicious windows,
5. human-play only those targeted slices,
6. report/discuss before numerical rebalance.

## Still not frozen
- literal final E HP/armor package,
- final X hardened multipliers,
- exact stage duration,
- final number/names/order of tiers,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- true human multiplayer cadence/network behavior,
- sync round / DUO-TRIPLE-FULL SYNC implementation,
- Lv26/Lv31 coefficients.

## Later boundary
Only after the Lv6–21 block and its re-simulation close:
- finalize co-op pressure calibration,
- then proceed to Lv26/Lv31 signature skills,
- larger stage/tier production authoring,
- permanent/meta-stat layer.

## Human-play focus
Simulation does not replace checks for:
- impact feel / hitstop,
- VFX readability,
- Timing Square readability,
- projectile visibility,
- skill-strip density,
- screen crowding during S/X events,
- whether Lv21 heavy attacks feel meaningfully transformed,
- subjective class fun.
