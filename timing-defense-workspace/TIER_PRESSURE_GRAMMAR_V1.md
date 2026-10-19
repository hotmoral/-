# Timing Defense — Tier Pressure Grammar v1

Date: 2026-10-20 KST
Status: **candidate encounter-design grammar / analysis artifact — not a live gameplay patch**

## Purpose

Define a reusable encounter-pressure grammar for future 50-stage tiers so that co-op difficulty scales through changing combat problems rather than flat global HP/count inflation.

The grammar is based on three pressure families:

- `S` — **Swarm**: many low/medium-durability enemies arriving in a concentrated burst or short sustained wave.
- `E` — **Elite/Heavy**: one or a few unusually durable / armored / high-threat normal enemies.
- `X` — **Special/Mixed**: disruptive compositions using speed, flight, shields, split lanes or other special traits.

Core design rule:

> A stage does **not** need to use all three pressure families. 1-pattern, 2-pattern and 3-pattern stages are deliberately mixed across a 50-stage tier. The tier identity comes from their proportions, internal ratios, timing placement, formation geometry and intensity.

## Stage grammar

### 1-pattern stage

One pressure family owns the stage's special pressure budget.

Examples:
- late `S` flood,
- long `E` durability check,
- sustained `X` special-mob disruption.

A 1-pattern stage may be short/spiky or long/sustained. Higher tiers are allowed to return to many 1-pattern stages if that one pressure is pushed to an extreme.

### 2-pattern stage

Two pressure families appear at separate or partially overlapping times.

The pair is one of:
- `S+E`
- `S+X`
- `E+X`

The two patterns do not have to be 50:50. Each tier may bias the internal pressure share toward one member.

### 3-pattern stage

`S+E+X` all appear, but this is intentionally the least common stage type overall.

A 3-pattern stage may be:
- roughly balanced,
- dominated by one pressure family,
- or a rotating-extreme stage where the dominant family changes between stages.

Do not use maximum `S + E + X` pressure simultaneously by default. The normal grammar is time-separated role switching; deliberate overlap is a rarer chaos tool.

## Timing windows

Pressure events are placed into normalized stage windows:
- `early` ~20%
- `mid` ~48%
- `late` ~72%
- `final` ~90%

A tier owns a timing-bias vector. This allows two tiers with the same S/E/X counts to feel different because one favors mid-stage checks while another favors late/final spikes.

## Formation geometry

Swarm and Special events also carry geometry because class value depends on formation, not only target count.

### Swarm (`S`) forms
- `line`: long straight alignment — strong Archer opportunity.
- `cluster`: spatially dense pack — strong Mage opportunity.
- `scatter`: less exploitable geometry — raises generalist/control value.

### Special (`X`) forms
- `line`: special enemies aligned along a trajectory.
- `cluster`: special enemies spatially dense.
- `split`: divided / awkward pressure where control and broad coverage matter.

`E` is treated as a durability check rather than a formation archetype.

## Five prototype tier identities

These are **representative test identities**, not a declaration that the final game must contain exactly five tiers or use these final names.

Each row is exactly 50 stages.

| Prototype tier | 1-pattern | 2-pattern | 3-pattern | Main identity |
|---|---:|---:|---:|---|
| T1 Foundations | 30 (60%) | 17 (34%) | 3 (6%) | learn/read individual pressures |
| T2 Breakers | 21 (42%) | 23 (46%) | 6 (12%) | elite/durability checks |
| T3 Rushline | 17 (34%) | 25 (50%) | 8 (16%) | swarm + special tempo / line pressure |
| T4 Crossfire | 11 (22%) | 25 (50%) | 14 (28%) | frequent mixed pressure / role switching |
| T5 Extremes | 23 (46%) | 19 (38%) | 8 (16%) | fewer grammar pieces again, but stronger focused extremes |

Across these 250 prototype stages:
- 1-pattern = `102 / 250 = 40.8%`
- 2-pattern = `109 / 250 = 43.6%`
- 3-pattern = `39 / 250 = 15.6%`

Therefore **84.4%** of stages use only one or two pressure families. This intentionally prevents every stage from becoming the same three-pattern routine.

## Exact pattern-occurrence allocations

Pattern occurrence counts include each pattern once when it appears in a stage signature.

| Tier | S | E | X | S share | E share | X share |
|---|---:|---:|---:|---:|---:|---:|
| T1 | 25 | 24 | 24 | 34.2% | 32.9% | 32.9% |
| T2 | 24 | 37 | 24 | 28.2% | 43.5% | 28.2% |
| T3 | 40 | 19 | 32 | 44.0% | 20.9% | 35.2% |
| T4 | 32 | 28 | 43 | 31.1% | 27.2% | 41.7% |
| T5 | 30 | 31 | 24 | 35.3% | 36.5% | 28.2% |

### Single-stage allocations
- T1: `S10 / E10 / X10`
- T2: `S4 / E12 / X5`
- T3: `S12 / E0 / X5`
- T4: `S1 / E0 / X10`
- T5: `S10 / E9 / X4`

### Two-pattern allocations
- T1: `SE6 / SX6 / EX5`
- T2: `SE10 / SX4 / EX9`
- T3: `SE6 / SX14 / EX5`
- T4: `SE6 / SX11 / EX8`
- T5: `SE7 / SX5 / EX7`

## Internal pressure-share rules

### T1 Foundations
- two-pattern stages: approximately `52–58% / 48–42%`; primary side rotates.
- triple stages: approximately `S34 / E33 / X33`.

### T2 Breakers
- when E is present in a pair, E receives roughly `62–68%` of the special pressure budget.
- triple stages: approximately `S22 / E55 / X23`.

### T3 Rushline
- `S+X`: usually near `54–60 / 46–40` with S slightly favored overall.
- when E is paired with S or X, E is usually the secondary pressure.
- triple stages: approximately `S45 / E15 / X40`.

### T4 Crossfire
- X is normally primary in any pair containing X: about `58–64%`.
- `S+E` stays near-even.
- triple stages: approximately `S25 / E20 / X55`.

### T5 Extremes
- two-pattern stages use a stronger dominant-side split, roughly `66–74 / 34–26`.
- triple stages rotate a dominant family rather than using the same internal ratio every time.
- for the 8 prototype triple stages: S-dominant 3, E-dominant 3, X-dominant 2, normally around `60 / 20 / 20`.

## Geometry quotas used in the v1 prototype

### Swarm forms
| Tier | line | cluster | scatter |
|---|---:|---:|---:|
| T1 | 8 | 11 | 6 |
| T2 | 7 | 11 | 6 |
| T3 | 22 | 10 | 8 |
| T4 | 8 | 10 | 14 |
| T5 | 9 | 17 | 4 |

### Special forms
| Tier | line | cluster | split |
|---|---:|---:|---:|
| T1 | 7 | 6 | 11 |
| T2 | 5 | 6 | 13 |
| T3 | 14 | 5 | 13 |
| T4 | 9 | 8 | 26 |
| T5 | 6 | 6 | 12 |

Interpretation:
- T3 intentionally creates many line opportunities.
- T4 intentionally creates many split/special-control situations.
- T5 makes its swarm events cluster-heavy, while also keeping large durability spikes through E.

## Timing-bias prototypes

| Tier | early | mid | late | final |
|---|---:|---:|---:|---:|
| T1 | 22% | 34% | 28% | 16% |
| T2 | 14% | 36% | 34% | 16% |
| T3 | 16% | 25% | 34% | 25% |
| T4 | 18% | 28% | 30% | 24% |
| T5 | 10% | 24% | 30% | 36% |

T5 deliberately shifts much more of its special pressure toward the stage ending.

## Overlap policy

Most events should be time-separated because readable role switching is the default goal.

Prototype overlap probabilities:
- T1: 3%
- T2: 5%
- T3: 8%
- T4: 16%
- T5: 10%

T4 is the main deliberate chaos / cross-pressure identity.

## Anti-repetition constraints

The generator should treat these as structural constraints rather than relying on random luck:
- avoid the same exact stage signature back-to-back where possible,
- avoid adjacent 3-pattern stages except where a tier identity intentionally allows it,
- do not use the same dominant pressure at the same timing window repeatedly for long runs,
- checkpoint-like stages (10/20/30/40/50) may receive extra pressure but are not required to be 3-pattern stages,
- repetition is allowed when the implementation changes duration, intensity, formation or timing enough to produce a different tactical problem.

The prototype schedules used for v5 achieved zero exact-signature back-to-back repeats.

## Class-role connection

The pressure grammar exists to create **situational class contribution**, not equal DPS everywhere.

Expected role windows:
- E durability check → Rogue peak opportunity.
- S-line / X-line → Archer peak opportunity.
- S-cluster / X-cluster → Mage opportunity; Tank also gains value in dangerous special clusters.
- X-split / heavy wall pressure → Tank peak opportunity.
- S-scatter / multi-pattern transitions → Knight generalist value rises because no narrow specialist cleanly owns the whole problem.

The quantitative v5 role-coverage result is documented in `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`.

## What this grammar does NOT freeze yet

- exact monster counts for each pressure budget,
- exact HP/armor multipliers for E,
- exact 2/3/4-player scaling multipliers,
- actual stage length,
- exact event duration in seconds,
- final boss/checkpoint placement,
- final number/names/order of tiers,
- multiplayer economy/shop rules.

Those should be calibrated only after the grammar is accepted structurally.

## Next implementation-analysis boundary

Translate the pressure budget into concrete spawn recipes using current monster types, then run headless 2/3/4-player campaign calibration while keeping class coefficients unchanged.

Required order remains:

`model → simulate → report → discuss → explicit decision → live patch`
