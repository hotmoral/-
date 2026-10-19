# Timing Defense — Public Workspace

This directory is the persistent planning / balance / simulation / handoff workspace for the Timing Defense prototype.

## Repository layout
- Live playable code branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: https://timing-defense-v011.onrender.com
- Current playable prototype: `v0.15`

The workspace branch is intentionally separated from the Render deployment branch so documentation and balance work do not trigger a live deploy.

## Read order for a new session
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

## Current project boundary
Timing-action side defense prototype with five classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

Core timing rhythm is `X → X → X → X+Y`; the fourth attack is charged/heavy. Timing judgment directly drives projectile outcome, EXP and class growth.

## Working principle
Automated simulation is used for numerical balance, growth speed, encounter difficulty, team-role validation and now encounter-grammar design. Human playtesting is reserved for timing feel, readability, hit impact, VFX density and subjective fun.

Simulation is diagnostic, not self-authorizing. A measured gap must be explained and discussed before a live balance patch.

## Latest completed analysis — v5
v5 formalized a reusable **Tier Pressure Grammar** for future 50-stage tiers.

Pressure families:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Stages may use one, two or all three pressure families. All three are intentionally **not** used every stage.

Five representative 50-stage tier prototypes produce, across 250 stages:
- 1-pattern: 40.8%
- 2-pattern: 43.6%
- 3-pattern: 15.6%

Therefore 84.4% of stages use only one or two pressure families.

The grammar also varies:
- pair/triple internal pressure ratio,
- line/cluster/scatter/split geometry,
- early/mid/late/final timing,
- duration/intensity,
- overlap rate.

Structural role-coverage across all 250 prototype stages is broadly distributed:
- Knight 18.6%
- Rogue 20.1%
- Tank 20.4%
- Archer 22.0%
- Mage 18.9%

Tier-specific specialist peaks still appear, which is intentional.

No live gameplay value was changed by v5.

## Current next boundary
Translate abstract S/E/X pressure budgets into concrete GRUNT/RUNNER/BRUTE/SHIELD/FLYER spawn recipes, then calibrate 2/3/4-player pressure headlessly before any live difficulty patch.
