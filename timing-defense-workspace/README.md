# Timing Defense — Public Workspace

This directory is the persistent planning / balance / simulation / handoff workspace for the Timing Defense prototype.

## Repository layout
- Live playable code branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: https://timing-defense-v011.onrender.com
- Current playable prototype: **v0.16**
- Current play page: `https://timing-defense-v011.onrender.com/v016.html`

The workspace branch is separated from the Render deployment branch so analysis/documentation work does not deploy automatically.

## New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V016_IMPLEMENTATION_REPORT.md`
4. `DESIGN_DECISIONS.md`
5. `SKILL_PLAN_LV6_31.md`
6. `TIER_PRESSURE_GRAMMAR_V1.md`
7. `PRESSURE_RECIPES_V1.md`
8. `BALANCE_SIM_REPORT_V4_TEAM.md`
9. `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
10. `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`
11. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
12. `SIMULATION_METHOD.md`
13. `NEXT_WORK.md`

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

Simulation is diagnostic, not self-authorizing. A measured gap must be explained and discussed before numerical live balance changes.

---

# Current implementation — v0.16

v0.16 implements the first playable multi-skill block through:
`Lv6 / Lv11 / Lv16 / Lv21`.

The HUD reserves all six long-term milestones:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.

Important frozen mechanics now implemented:
- Rogue same-target dagger hits remain uncapped.
- Boss dagger damage scalar = 0.70.
- Boss knockback scalar = 0.40.
- Tank Lv11 wall reduction / Lv16 shield / Lv21 Ground Impact.
- Mage Lv16 center-excluding Resonance / Lv21 Greater Arcane Orb.
- Archer true straight-line penetration.

Important v0.16 fix:
Archer projectiles now lock their trajectory at launch. The initial v0.16 source still inherited generic post-target-death retargeting, which could bend an arrow toward an off-line enemy. That semantic defect was fixed at live commit:
`b8b823742bd5fb16026090045cd347feb0f9275e`.

Current Render deployment:
`dep-dbbb6pom7kps73ebd0eg` / LIVE.

See `V016_IMPLEMENTATION_REPORT.md`.

---

# Encounter framework

Pressure families:
- `S` = Swarm,
- `E` = Elite/Heavy,
- `X` = Special/Mixed.

The game does not force all three into every stage. Tier identity comes from 1/2/3-pattern ratios, S/E/X frequency, internal pressure ratios, geometry, event timing, intensity and overlap.

Current candidate Swarm burst envelope:
- S-line 2P/3P/4P = 8 / 11 / 14.
- S-cluster = 7 / 10 / 13.
- S-scatter = 9 / 12 / 16.

Current candidate P95 four-second spawn density:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

X carries most multiplayer scaling through role-bearing composition. E is an effective durability budget rather than one giant mandatory HP bar.

---

# Latest completed analysis — v7

v7 mirrors the actual v0.16 formulas instead of the earlier approximate Lv21 model.

Final/formula-corrected analysis volume:
- 12,300 campaign-bound runs,
- 50,000 durable-normal targeted duels,
- 20,000 static geometry trials.

## Fixed-level pressure response
3P Average / Skilled clear:
- Lv6 = 36.2 / 50.7%,
- Lv11 = 49.6 / 68.0%,
- Lv16 = 55.6 / 77.8%,
- Lv21 = **81.6 / 96.4%**.

4P:
- Lv6 = 22.7 / 33.0%,
- Lv11 = 33.3 / 42.7%,
- Lv16 = 33.7 / 49.3%,
- Lv21 = **52.8 / 73.6%**.

2P is already near saturation in the current pressure/AI-bound diagnostic.

## Specialist checks
Rogue remains the fastest high-HP-normal killer at Lv21:
- Rogue 20.54 / 15.92 s Average/Skilled,
- Archer 25.44 / 19.76,
- Knight 33.45 / 25.14,
- Mage 39.98 / 31.31,
- Tank 42.67 / 33.47.

After Archer trajectory locking:
- line packs remain clearly Archer-favored,
- dense-pack Archer/Mage results are close and remain a watch item rather than a balance verdict.

## Current balance decision
**No numerical class rebalance is authorized from v7.**

Watch items only:
- Archer broad Lv21 campaign throughput,
- 2P saturation,
- Mage/Archer dense-pack separation on the real rendered battlefield,
- future real-human teammate cadence.

Files:
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- `combat_exact_v016.py`

## Current next boundary
Human/device/browser v0.16 validation for implementation/readability defects only:
- six-slot skill-strip fit,
- visually straight Archer trajectories,
- Tank shield lifecycle,
- Rogue barrage readability,
- Mage Resonance center exclusion,
- Lv21 VFX readability under dense pressure.

Fix implementation defects immediately if found, but report/discuss before any numerical rebalance.
