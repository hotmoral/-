# Timing Defense — Public Workspace

This directory is the persistent planning / balance / simulation / handoff workspace for the Timing Defense prototype.

## Repository layout
- Live playable code branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: https://timing-defense-v011.onrender.com
- Current playable prototype: `v0.15`

The workspace branch is separated from the Render deployment branch so analysis/documentation work does not deploy automatically.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `DESIGN_DECISIONS.md`
4. `TIER_PRESSURE_GRAMMAR_V1.md`
5. `PRESSURE_RECIPES_V1.md`
6. `SKILL_PLAN_LV6_31.md`
7. `BALANCE_SIM_REPORT_V4_TEAM.md`
8. `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
9. `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`
10. `SIMULATION_METHOD.md`
11. `NEXT_WORK.md`

Older v1/v2/v3 reports remain available for historical reasoning and numerical provenance.

## Core project
Timing-action side defense prototype with five classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

Core rhythm is `X → X → X → X+Y`. The fourth attack is charged/heavy. Timing judgment drives combat outcome, EXP and class growth.

## Working principle
Automated simulation is used for:
- numerical balance,
- growth speed,
- encounter difficulty,
- team-role validation,
- tier encounter grammar,
- concrete spawn-recipe calibration.

Human playtesting is reserved for feel, readability, impact, VFX density and subjective fun.

Simulation is diagnostic, not self-authorizing. A measured gap must be explained and discussed before live balance changes.

---

# Latest completed analysis — v6

v5 created the abstract Tier Pressure Grammar:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

v6 translated that grammar into current-roster GRUNT/RUNNER/BRUTE/SHIELD/FLYER recipes.

## Current candidate Swarm burst envelope
- S-line 2P/3P/4P = 8 / 11 / 14.
- S-cluster = 7 / 10 / 13.
- S-scatter = 9 / 12 / 16.

## Concrete scaling philosophy
- X carries most multiplayer scaling through role-bearing composition.
- S creates readable temporary count spikes.
- E creates durable-anchor moments through an effective durability budget rather than one mandatory giant HP multiplier.

## Readability result
Across 250 prototype stages per team-size model, P95 4-second spawn density is approximately:
- 2P = 11,
- 3P = 15,
- 4P = 18.

## Combat-envelope result
Conservative one-human + current-AI-like teammate diagnostic, 7,000 runs:
- 2P Average/Skilled = 100 / 100% clear,
- 3P = 88.4 / 94.9%,
- 4P = 68.3 / 83.0%.

A fully capable all-human candidate-Lv21 upper-bound model still saturates near 100% in representative slices. Therefore final co-op difficulty is not frozen yet.

Files:
- `PRESSURE_RECIPES_V1.md`
- `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`
- `pressure_recipe_sim_v1.py`

No live gameplay value changed from v6.

## Current next boundary
Implement the playable Lv6–21 multi-skill block first, then mirror the exact implementation back into the simulator and rerun concrete pressure calibration before any final co-op difficulty tuning.
