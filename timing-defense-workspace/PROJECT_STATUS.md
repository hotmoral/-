# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Public repo: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning/balance/handoff branch: `timing-defense-workspace`
- Current playable prototype: `v0.15`
- Public play URL: https://timing-defense-v011.onrender.com/v015.html

## Current playable scope
- Landscape mobile/browser timing-defense prototype.
- Fixed player position near the left wall; monsters approach from the right.
- Rhythm: `X → X → X → X+Y`.
- Judgments: NORMAL / GOOD / PERFECT plus HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Team controls: solo through +3 AI.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Current playable Stage 1–10 prototype.
- Run-only EXP / level / coin / shop upgrades.
- Live class-skill implementation currently stops at Lv6.

## Planned growth
Automatic skill unlocks:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Lv21 is the first major fourth-attack transformation. Lv31 P×P CRITICAL is intended to become the class-signature finisher.

## Frozen class / progression decisions
- Archer penetration = true straight-line geometry only.
- Tank = team-specialist; fresh-run solo parity is not required.
- Rogue same-target dagger hits are uncapped.
- Boss dagger damage scalar starting value = `0.70`.
- Boss knockback scalar starting value = `0.40`.
- EXP remains tied to timing attack events/results.
- Faster clear does not receive compensating EXP merely because it generated fewer attack events.
- Simulation never self-authorizes a live balance patch.

## Player mastery reference
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

Skilled is considered an attainable learned-player state. A strong mastery curve is intended.

---

# Simulation / design status

## v1 — role separation
Established the intended class identity split.

## v2 — Stage 1–10 + run shop
Resolved:
- Archer auto-chain model artifact → straight-line only,
- Tank solo weakness → accepted team specialization,
- EXP/attack-count coupling → retained.

## v3 — mastery curve
Confirmed meaningful Average→Skilled improvement. No live change.

## v4 — team composition
13,780 deliberate runs.

Findings:
- Tank has real defensive team value under pressure.
- Rogue takes a disproportionate share of durable-normal kills.
- Archer wins line geometry; Mage wins dense geometry.
- Knight remains a strong stabilizing generalist.
- current unscaled Stage 1–10 waves saturate at 3–4 players.

Report: `BALANCE_SIM_REPORT_V4_TEAM.md`

## v5 — Tier Pressure Grammar
Formalized future 50-stage tier encounter grammar.

Pressure families:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Across five representative 50-stage tier prototypes:
- 1-pattern = 40.8%,
- 2-pattern = 43.6%,
- 3-pattern = 15.6%.

So 84.4% of stages use only one or two pressure families.

Tier identity varies through pattern frequency, internal ratios, geometry, timing, intensity and overlap rather than forcing all three patterns every stage.

Files:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`

## v6 — latest completed: concrete current-roster pressure recipes
v6 translated S/E/X into GRUNT/RUNNER/BRUTE/SHIELD/FLYER recipes and ran structural + combat-envelope diagnostics.

### Candidate Swarm burst sizes
- S-line 2P/3P/4P = `8 / 11 / 14`.
- S-cluster = `7 / 10 / 13`.
- S-scatter = `9 / 12 / 16`.

### Candidate X philosophy
X carries most multiplayer scaling through extra role-bearing threats rather than blanket HP:
- more SHIELD/BRUTE anchors,
- more RUNNER/FLYER disruption,
- line/cluster/split geometry.

### Readability result
Across 250 generated tier stages per team-size model, current candidate short-window P95 is approximately:
- 2P: 11 spawns / 4 s,
- 3P: 15 / 4 s,
- 4P: 18 / 4 s.

This replaced an earlier overpacked candidate that produced 20+ ordinary enemies in one event.

### Role-opportunity preservation
Concrete recipe aggregate structural opportunity stays broad:
- 2P: Knight 20.5 / Rogue 19.0 / Tank 20.2 / Archer 21.1 / Mage 19.2%.
- 3P: 20.4 / 19.0 / 20.7 / 21.2 / 18.8%.
- 4P: 20.4 / 19.1 / 20.5 / 21.2 / 18.8%.

Tier-local specialist peaks remain, so concrete monster conversion did not erase role rotation.

### Combat-envelope diagnostic
A 7,000-run conservative bound used one human local player plus teammates approximating current live AI cadence/result quality.

Aggregate clear rates:
- 2P: Average 100%, Skilled 100%.
- 3P: Average 88.4%, Skilled 94.9%.
- 4P: Average 68.3%, Skilled 83.0%.

T4 Crossfire was the hardest identity in that bound:
- 3P Average 77.7%, Skilled 90.3%.
- 4P Average 48.0%, Skilled 77.5%.

A fully capable all-human candidate-Lv21 upper-bound model still saturates near 100% in representative slices. Therefore **final co-op clear-rate targets are not frozen** until exact Lv11–21 playable behavior and a real-human multiplayer cadence model exist.

Files:
- `PRESSURE_RECIPES_V1.md`
- `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`
- `pressure_recipe_sim_v1.py`

No live monster, class, stage, EXP, shop or boss value changed from v6.

---

# Current next boundary
The highest-value next implementation step is now the first playable multi-skill block:
- Lv6 / Lv11 / Lv16 / Lv21 for all five classes,
- exact straight-line Archer collision,
- multi-skill HUD strip below Timing Square,
- documented boss resistance rules,
- agreed Mage/Tank candidate behavior.

After implementation:
1. extract exact formulas back into the simulator,
2. rerun concrete pressure recipes,
3. identify suspicious stages/pressure windows,
4. human-play only those targeted slices,
5. report/discuss before any live numerical rebalance.

Still not frozen:
- literal E HP/armor package,
- final X hardened values,
- final stage duration,
- true human multiplayer cadence,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync-bonus implementation,
- final number/names/order of tiers.

## Important live UX decisions
- No `X LOCK` explanatory text after first heavy tap.
- Shop does not auto-advance.
- Short shop input protection prevents accidental purchase/advance.
- Timing Square-side EXP remains primary growth HUD.
- Permanent skill-name text beside EXP remains removed.
- Timing Square renders above monsters.
