# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Live playable branch: `timing-defense-live-v011`
- Current live prototype: `v0.15`
- Play URL: https://timing-defense-v011.onrender.com/v015.html

The workspace branch is the canonical source for design decisions, simulation interpretation and new-session recovery. The live branch is separate so analysis/documentation does not deploy automatically.

---

# Current playable state

- Classes: Knight / Rogue / Tank / Archer / Mage.
- Current live skill implementation: Lv6 only.
- Planned automatic unlocks: `Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.
- Current playable stage prototype: 1–10.
- Run EXP / coins / shop reset each run.
- Team control currently supports solo through +3 AI.

## Frozen combat / class-role decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: fast multihit / crit / high-HP normal execution.
- Tank: team-specialist / knockback / wall protection / control. Fresh-run solo parity is not required.
- Archer: true straight-line geometric penetration only. No homing/retarget/automatic next-target chaining.
- Mage: density specialist / area burst / chained explosions.

## Frozen boss / progression decisions
- Rogue same-target dagger hits are uncapped.
- Boss dagger damage scalar starting value = `0.70`.
- Boss knockback scalar starting value = `0.40`.
- EXP remains tied to timing attack results/events.
- Faster-clearing classes are not compensated merely because they perform fewer attacks.

## Player mastery reference
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

Skilled is considered an attainable learned-player state. Strong Average→Skilled improvement is intended.

## Balance governance
Never patch solely because simulation shows a large performance gap.

Required order:
`model/simulate → identify cause/artifact/specialization → report → discuss → explicit decision → live patch`

---

# Skill-design candidate through Lv21

See `SKILL_PLAN_LV6_31.md` for the full Lv6–31 tree.

Through Lv21:
- Knight: Lv6 +12% blade-wave damage; Lv11 penetration; Lv16 PERFECT enhancement; Lv21 large heavy blade wave.
- Rogue: Lv6 second dagger; Lv11 +6%p crit; Lv16 PERFECT cycle reduction; Lv21 five-dagger heavy.
- Tank: Lv6 width/knockback; Lv11 wall incoming damage -10%; Lv16 wall shield 80 / 3 s / refresh-only / non-stack; Lv21 broad heavy shockwave.
- Archer: Lv6 straight-line penetration; Lv11 speed +25% / damage +10%; Lv16 PERFECT armor-ignore / preserved penetration; Lv21 triple shot.
- Mage: Lv6 burst; Lv11 larger/stronger burst; Lv16 outer-ring resonance excluding the original center target; Lv21 greater arcane orb.

These are implementation candidates, not automatic deployment authority.

---

# Simulation history

## v1 — role separation
Established the intended class identity split.

## v2 — Stage 1–10 + run shop
Resolved:
- Archer permissive auto-chain was a simulation artifact → straight-line only.
- Tank solo weakness → accepted as team specialization.
- EXP/attack-count coupling → retained.

## v3 — mastery curve
Confirmed a useful Average→Skilled progression and that cadence is an important skill dimension.

## v4 — team composition / role isolation
13,780 deliberate runs.

Findings:
- Tank has measurable team defensive value.
- Rogue takes disproportionate durable-normal kills.
- Archer wins line geometry; Mage wins dense geometry.
- Knight remains a stabilizing generalist.
- current unscaled Stage 1–10 waves saturate at 3–4 players.

Report: `BALANCE_SIM_REPORT_V4_TEAM.md`.

## v5 — Tier Pressure Grammar
Formalized long-run encounter variety for future 50-stage tiers.

Pressure families:
- `S` Swarm,
- `E` Elite/Heavy,
- `X` Special/Mixed.

Stages may use 1, 2 or 3 families; all three are not forced into every stage.

Five representative 50-stage tier prototypes produced across 250 stages:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

Tier identity is defined by pattern frequency, internal ratios, geometry, timing, intensity and overlap.

Files:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
- `pressure_grammar_sim_v1.py`

## v6 — latest completed: concrete current-roster pressure recipes
v6 converted S/E/X into GRUNT/RUNNER/BRUTE/SHIELD/FLYER recipes and checked readability + role preservation + combat bounds.

### Candidate Swarm bursts
- S-line 2P/3P/4P = `8 / 11 / 14`.
- S-cluster = `7 / 10 / 13`.
- S-scatter = `9 / 12 / 16`.

### Candidate X direction
X is the primary co-op scaling language:
- add role-bearing SHIELD/BRUTE anchors,
- add RUNNER/FLYER disruption,
- vary line/cluster/split geometry,
- avoid one flat global all-monster HP multiplier.

### Candidate E direction
E is an **effective durability budget**, not permission to create one absurd single HP bar. Final production should distribute the budget across moderate HP, armor, extra durable target(s), type and timing.

### Readability result
Across 250 generated stages per team-size model, approximate P95 4-second spawn density:
- 2P = 11,
- 3P = 15,
- 4P = 18.

The earlier overpacked candidate with 20+ ordinary enemies in one event was rejected.

### Role-opportunity result
Concrete recipes preserve broad class opportunity:
- 2P: Knight 20.5 / Rogue 19.0 / Tank 20.2 / Archer 21.1 / Mage 19.2%.
- 3P: 20.4 / 19.0 / 20.7 / 21.2 / 18.8%.
- 4P: 20.4 / 19.1 / 20.5 / 21.2 / 18.8%.

Tier-local specialist peaks remain, so the concrete roster did not collapse the abstract grammar.

### Combat-envelope diagnostic
Absolute final clear rate is not frozen because exact human multiplayer cadence and exact Lv11–21 implementation do not yet exist.

Conservative-ish bound:
- one human local player,
- teammates approximate current live AI cadence/result quality,
- 7,000 runs across all unique 2/3/4-player compositions, every possible local member, T1–T5, Average/Skilled.

Aggregate clear:
- 2P Average/Skilled = 100 / 100%.
- 3P = 88.4 / 94.9%.
- 4P = 68.3 / 83.0%.

T4 Crossfire was hardest:
- 3P = 77.7 / 90.3%.
- 4P = 48.0 / 77.5%.

Upper-ish bound:
- all teammates modeled as fully capable humans,
- candidate Lv21 kits,
- idealized targeting.

Representative slices saturate near 100%, so final co-op difficulty must wait for exact implementation.

Files:
- `PRESSURE_RECIPES_V1.md`
- `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`
- `pressure_recipe_sim_v1.py`

No live gameplay value changed from v6.

---

# Exact next work boundary

Further co-op numeric tuning pauses here.

Next implementation slice:
1. implement Lv6 / Lv11 / Lv16 / Lv21 for all five classes,
2. add multi-skill HUD strip below Timing Square,
3. implement exact straight-line Archer collision,
4. keep boss dagger scalar 0.70 and boss knockback scalar 0.40,
5. implement agreed Mage/Tank candidate behavior,
6. do not simultaneously redesign stage difficulty.

After implementation:
1. extract exact formulas back into the simulator,
2. rerun `PRESSURE_RECIPES_V1` under 2/3/4-player models,
3. identify suspicious windows/stages,
4. human-play only those targeted slices,
5. report/discuss before any live numerical rebalance.

## Still unresolved
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- true human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync round / DUO-TRIPLE-FULL SYNC implementation,
- final number/names/order of tiers,
- Lv26/Lv31 exact coefficients.

---

# New-session read order
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

Older v1/v2/v3 reports remain available for numerical provenance and decision history.
