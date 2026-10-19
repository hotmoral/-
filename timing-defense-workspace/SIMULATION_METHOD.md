# Timing Defense — Headless Simulation Method

## Purpose
Use renderer-free models to validate numerical balance, progression, team-role value and encounter structure much faster than manual play. Simulation is not a replacement for feel/UX testing and does not self-authorize live balance patches.

## Core governance

Required order:
1. identify a measured difference,
2. determine whether it comes from intentional specialization, model abstraction/artifact, or a real balance defect,
3. report the result,
4. discuss with the user,
5. make an explicit design decision,
6. only then change live gameplay values.

## Frozen semantic decisions

### Timing profiles
- Novice: N45 / G45 / P10.
- Average: N25 / G55 / P20.
- Skilled: N10 / G50 / P40.
- Expert: N3 / G32 / P65.

Average cadence:
- normal 1.14 s
- heavy 1.68 s

Skilled cadence:
- normal 1.04 s
- heavy 1.54 s

### Archer
Straight-line geometric penetration only.
- no homing,
- no auto-retarget,
- no automatic next-enemy chain,
- only intersected hitboxes can be penetrated.

### Tank
Team-specialist. Fresh-run solo Stage-10 parity is not required.

### Rogue / bosses
- no same-target dagger hit cap,
- boss dagger damage scalar starting value: 0.70,
- boss knockback scalar starting value: 0.40.

### EXP
EXP remains attached to timing attack results/events. Faster-clearing classes are allowed to level differently because they may perform fewer attack events.

---

# Simulation history

## v1 — role scenarios
Purpose: verify basic class identity.

Scenarios:
- durable normal duel → Rogue,
- boss duel → boss resistance behavior,
- straight-line pack → Archer,
- dense cluster → Mage,
- wall pressure → Tank.

Result: intended role split was plausible.

## v2 — Stage 1–10 + run shop
Added:
- current Stage 1–10 structure,
- coins / clear rewards,
- run-shop costs and upgrades,
- Lv6/Lv11/Lv16/Lv21 candidate skills,
- deterministic shopping policies.

Deliberate volume: 39,600 runs.

Important outcome:
- permissive Archer next-target chaining was identified as a model artifact and rejected,
- Tank solo weakness was discussed and accepted as role specialization,
- EXP/attack-count coupling was explicitly retained.

See `BALANCE_SIM_REPORT_V2.md`.

## v3 — Average → Skilled mastery curve
Nine interpolation points between Average and Skilled plus accuracy-only diagnostics.

Deliberate volume: 27,500 runs.

Important outcome:
- Knight / Archer / Mage show a strong useful mastery response,
- Rogue remains specialist-shaped,
- Tank solo remains non-normative,
- cadence is a real skill axis in addition to accuracy.

See `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`.

## v4 — team-composition / co-op role isolation
Added:
- 2/3/4-player compositions,
- identical seeded waves,
- targeted Lv21 role diagnostics,
- duplicate-class checks.

Deliberate volume: 13,780 runs.

Important modeling boundary:
- the main v4 matrix uses current unscaled Stage 1–10 waves,
- multiplayer shop/economy ownership is not frozen, so v4 does not claim final co-op campaign balance.

Important outcome:
- Tank team defensive utility is real under meaningful pressure,
- Rogue takes disproportionate durable-normal kills,
- Archer wins line geometry while Mage wins dense geometry,
- Knight remains a useful stabilizing generalist,
- current waves saturate at 3–4 players and therefore cannot serve as final multiplayer difficulty targets.

See `BALANCE_SIM_REPORT_V4_TEAM.md`.

## v5 — Tier Pressure Grammar / role opportunity

v5 moves one level above exact combat and tests **encounter structure** before concrete co-op scaling is authored.

### Pressure families
- `S` Swarm — temporary high-count pressure.
- `E` Elite/Heavy — one/few unusually durable threats.
- `X` Special/Mixed — disruptive special compositions.

### Stage complexity
A stage may contain:
- one pressure family,
- two pressure families,
- all three pressure families.

The important design choice is that all three are **not** required every stage.

### Five representative 50-stage prototypes

| Tier | 1-pattern | 2-pattern | 3-pattern |
|---|---:|---:|---:|
| T1 | 30 | 17 | 3 |
| T2 | 21 | 23 | 6 |
| T3 | 17 | 25 | 8 |
| T4 | 11 | 25 | 14 |
| T5 | 23 | 19 | 8 |

Across 250 prototype stages:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

Thus 84.4% of stages contain only one or two pressure families.

### Geometry layer
Swarm:
- line,
- cluster,
- scatter.

Special:
- line,
- cluster,
- split.

Geometry is stored as encounter data because class contribution changes materially with it.

### Pressure-budget layer
Two-pattern and three-pattern stages carry explicit internal shares rather than assuming equal 50:50 or 33:33:33 pressure.

Examples:
- T2 E-heavy pair ≈ 65/35,
- T3 triple ≈ S45/E15/X40,
- T4 triple ≈ S25/E20/X55,
- T5 rotates one ~60% dominant pressure.

### Timing layer
Events use early / mid / late / final windows with tier-specific biases. Higher tiers may become harder through later spikes, longer duration, stronger internal dominance or more overlap rather than simply more pattern types.

### Structural role-coverage model
v5 does not pretend to be final DPS simulation. It uses role-response vectors derived from v1/v4 behavior and a cooperative coverage function.

Exact Shapley allocation is used to estimate how much of the encounter-problem space each class helps cover.

Across all 250 prototype stages:
- Knight 18.6%,
- Rogue 20.1%,
- Tank 20.4%,
- Archer 22.0%,
- Mage 18.9%.

Tier-specific peaks still appear:
- Rogue peaks in elite-heavy T2,
- Archer peaks in line-heavy T3,
- Tank peaks in split/special-heavy T4,
- Knight stays comparatively stable as generalist.

This is structural evidence that local specialist moments can coexist with broad long-run opportunity balance.

See:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`

---

# Deterministic comparison principle

Whenever comparing classes, compositions or scaling candidates, reuse the same random seeds / authored stage grammar so the world is held constant and the tested variable changes.

## Metrics by simulation layer

### Combat/campaign layers
- Stage clear / failure,
- Stage reached,
- wall HP / wall hits,
- clear time,
- target-type TTK / kill share,
- total and skill damage,
- shield generation/absorption,
- level / EXP timing,
- attack count / cadence,
- shop rank distribution where applicable.

### Encounter-grammar layer
- 1/2/3-pattern stage counts,
- S/E/X occurrence and pressure-budget shares,
- pair/triple internal ratios,
- early/mid/late/final event placement,
- formation geometry quotas,
- overlap rate,
- repeated signature/run detection,
- class pressure-coverage / Shapley share,
- peak concurrency once concrete spawn recipes exist.

---

# Next required extension

Translate v5 abstract pressure budgets into **concrete current-roster spawn recipes**:
- GRUNT,
- RUNNER,
- BRUTE,
- SHIELD,
- FLYER.

Then calibrate 2/3/4-player scaling while keeping class coefficients unchanged.

Required questions:
- How many extra enemies can S add before readability collapses?
- How much HP/armor can E add before combat becomes tedious?
- Which X recipes create role demand without unavoidable leakage?
- How should extra human players change event budget rather than simply multiplying everything?
- Can Average→Skilled mastery remain meaningful under co-op pressure?

No live difficulty patch should occur until this concrete spawn calibration is reported and discussed.
