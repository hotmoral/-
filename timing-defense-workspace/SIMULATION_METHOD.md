# Timing Defense — Headless Simulation Method

## Purpose
Use renderer-free models to validate numerical balance, progression, team-role value and encounter structure faster than manual play.

Simulation is diagnostic. It is not a replacement for feel/UX testing and never self-authorizes a live balance patch.

## Governance
Required order:
1. model/simulate,
2. identify intentional specialization vs abstraction/artifact vs real defect,
3. report,
4. discuss,
5. make explicit decision,
6. only then patch live gameplay.

---

# Frozen semantic decisions

## Timing profiles
- Novice: N45 / G45 / P10.
- Average: N25 / G55 / P20.
- Skilled: N10 / G50 / P40.
- Expert: N3 / G32 / P65.

Average cadence reference:
- normal 1.14 s,
- heavy 1.68 s.

Skilled cadence reference:
- normal 1.04 s,
- heavy 1.54 s.

## Archer
Straight-line geometric penetration only.
- no homing,
- no auto-retarget,
- no automatic next-enemy chain.

## Tank
Team-specialist. Fresh-run solo Stage-10 parity is not required.

## Rogue / bosses
- no same-target dagger hit cap,
- boss dagger damage scalar starting value = 0.70,
- boss knockback scalar starting value = 0.40.

## EXP
EXP remains tied to timing attack results/events. Faster-clearing classes are allowed to level differently because they may perform fewer attack events.

---

# Live prototype facts used when mirroring combat

The current v0.15 live prototype was re-read during v6 to avoid over-idealized timing assumptions.

Important current behaviors:
- projectile lifetime varies by class at roughly 0.14–0.28 s,
- local recovery waits about 390 ms after hit resolution,
- live AI intervals differ by class,
- live AI uses fixed lower timing-result probabilities than a real Skilled human,
- monsters move continuously toward the wall,
- current Stage 1–10 live spawner caps simultaneous active monsters at 10,
- current local targeting is nearest-target based,
- current Lv6 Archer live implementation still uses an older simplified second-hit behavior; future production is explicitly frozen to straight-line geometry instead.

When a future simulation intentionally differs from current live behavior because it is validating a planned Lv11+ skill, that difference must be stated explicitly.

---

# Simulation history

## v1 — role separation
Validated basic class identities:
- Rogue vs durable normal,
- Archer vs line pack,
- Mage vs dense cluster,
- Tank vs wall pressure,
- Knight as stable generalist.

## v2 — Stage 1–10 + run shop
Added current campaign/shop economy and candidate Lv6–21 skills.

Deliberate volume: 39,600 runs.

Key decisions:
- permissive Archer auto-chain was rejected as a model artifact,
- Tank solo weakness was accepted as specialization,
- EXP/attack-count coupling was retained.

Report: `BALANCE_SIM_REPORT_V2.md`.

## v3 — Average→Skilled mastery curve
Nine interpolation points plus accuracy-only diagnostics.

Deliberate volume: 27,500 runs.

Key result:
- mastery response is strong and desirable,
- cadence is a real skill axis in addition to raw judgment accuracy.

Report: `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`.

## v4 — team-composition / co-op role isolation
2/3/4-player compositions, identical seeded waves, duplicate-class checks and targeted Lv21 role diagnostics.

Deliberate volume: 13,780 runs.

Key result:
- Tank has real defensive team utility,
- Rogue has durable-normal team value,
- Archer and Mage remain line-vs-density distinct,
- Knight remains a stabilizing generalist,
- current unscaled Stage 1–10 waves saturate at 3–4 players.

Report: `BALANCE_SIM_REPORT_V4_TEAM.md`.

## v5 — Tier Pressure Grammar
Moved above exact combat to validate long-run encounter variety.

Pressure families:
- S Swarm,
- E Elite/Heavy,
- X Special/Mixed.

Five representative 50-stage prototypes were generated.
Across 250 stages:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

Geometry, internal ratios and timing are authored as gameplay data.

Structural role coverage across all 250 prototype stages stayed broad while specialist tier peaks remained.

Files:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
- `pressure_grammar_sim_v1.py`

## v6 — concrete current-roster recipes
v6 converted S/E/X into GRUNT/RUNNER/BRUTE/SHIELD/FLYER recipes.

### Structural recipe layer
Candidate Swarm counts:
- line = 8 / 11 / 14 for 2P/3P/4P,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

X scaling primarily adds role-bearing anchors/disruption rather than blanket HP.

E is represented as an **effective durability budget**. Do not read the stress-model multiplier as a literal production HP instruction.

### Readability metrics
Across 250 generated stages per team-size model, current candidate P95 4-second spawn burst is approximately:
- 2P = 11,
- 3P = 15,
- 4P = 18.

This replaced an earlier overpacked candidate with 20+ ordinary enemies in a single spike.

### Structural role-opportunity check
Concrete recipes preserve broad long-run role access while keeping local specialist peaks.

### Combat envelope
Absolute final clear rate is not frozen because real-human multiplayer cadence and exact Lv11–21 implementation do not exist yet.

Therefore v6 used **bounds**:

1. Conservative-ish bound:
   - one human local player,
   - teammates approximate current live AI cadence/result quality,
   - 7,000 runs over all unique compositions, every local member, T1–T5, Average/Skilled.

Aggregate clear:
- 2P: 100% / 100%,
- 3P: 88.4% / 94.9%,
- 4P: 68.3% / 83.0%.

T4 Crossfire was hardest:
- 3P 77.7% / 90.3%,
- 4P 48.0% / 77.5%.

2. Upper-ish bound:
   - all teammates modeled as fully capable humans,
   - current candidate Lv21 kits,
   - idealized class targeting.

Representative slices saturate near 100%, so these results are **not** used to freeze final difficulty.

The production result should lie between those bounds after exact multiplayer/skill implementation exists.

Files:
- `PRESSURE_RECIPES_V1.md`
- `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`
- `pressure_recipe_sim_v1.py`

---

# Deterministic comparison principle
When comparing classes, compositions or pressure candidates, reuse the same seeds / authored stage grammar so only the tested variable changes.

## Metrics by layer

### Combat/campaign
- clear/fail,
- wall HP / wall hits,
- clear time,
- target-type TTK / kill share,
- total/skill damage,
- shield generation/absorption,
- level/EXP timing,
- attack count/cadence,
- shop ranks where applicable.

### Encounter grammar / recipe
- 1/2/3-pattern stage counts,
- S/E/X occurrence and pressure shares,
- pair/triple internal ratios,
- early/mid/late/final placement,
- formation geometry,
- repeated signatures,
- short-window spawn density,
- total stage population,
- threat-index envelope,
- role-opportunity distribution.

---

# Current next extension
Further co-op difficulty tuning is intentionally paused until the first playable Lv6–21 multi-skill block exists.

Next implementation candidate:
- Lv6 / Lv11 / Lv16 / Lv21 skills for all five classes,
- exact straight-line Archer collision,
- multi-skill HUD strip,
- documented boss resistance rules,
- agreed Mage/Tank candidate behavior.

After implementation:
1. extract exact formulas into the simulator,
2. rerun concrete pressure recipes,
3. identify suspicious pressure windows numerically,
4. human-play only those targeted slices,
5. report/discuss before any live numerical rebalance.
