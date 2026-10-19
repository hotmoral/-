# Timing Defense — Concrete Pressure Recipes V1

Date: 2026-10-20 KST  
Status: **candidate encounter-authoring data; not live production values**

## 1. Purpose

Translate the abstract pressure grammar into concrete recipes using the current monster roster:

- GRUNT
- RUNNER
- BRUTE
- SHIELD
- FLYER

This file defines a first calibration envelope for 2 / 3 / 4-player co-op. It does **not** authorize a live difficulty patch.

Pressure families:

- `S` = Swarm burst
- `E` = Elite / extreme durability spike
- `X` = Special / mixed disruption

The governing philosophy is:

1. `X` is the main co-op scaling language.
2. `S` and `E` appear as time-separated spikes.
3. A stage can use 1, 2 or 3 families; all three are not mandatory.
4. Team-size scaling should increase event budget and specialist threats before applying any global all-monster multiplier.
5. Readability is protected by limiting short-window spawn density.

---

## 2. S — Swarm recipes

Swarm enemies keep roughly ordinary durability. Team size primarily changes **burst count**, not blanket HP.

### S-LINE
Aligned horizontal pressure; Archer-favorable.

| Players | Recipe | Burst count |
|---|---|---:|
| 2 | 5 GRUNT + 3 RUNNER | 8 |
| 3 | 7 GRUNT + 4 RUNNER | 11 |
| 4 | 9 GRUNT + 5 RUNNER | 14 |

### S-CLUSTER
Spatially dense pressure; Mage-favorable.

| Players | Recipe | Burst count |
|---|---|---:|
| 2 | 5 GRUNT + 2 FLYER | 7 |
| 3 | 7 GRUNT + 3 FLYER | 10 |
| 4 | 9 GRUNT + 4 FLYER | 13 |

### S-SCATTER
Fast/dispersed pressure; generalist/control value rises.

| Players | Recipe | Burst count |
|---|---|---:|
| 2 | 3 GRUNT + 4 RUNNER + 2 FLYER | 9 |
| 3 | 4 GRUNT + 5 RUNNER + 3 FLYER | 12 |
| 4 | 5 GRUNT + 7 RUNNER + 4 FLYER | 16 |

The current candidate does not globally inflate S-unit HP by team size. Only mild tier/intensity scaling is allowed.

---

## 3. E — Elite / Heavy recipes

E should feel like “one or two things suddenly refuse to die”, not like every normal enemy becoming a sponge.

The simulator therefore treats E as an **effective durability budget**, not a frozen literal HP multiplier.

Candidate realization options:

### 2 players
- one Champion BRUTE, or
- two hardened SHIELDs, or
- one BRUTE + one SHIELD.

### 3 players
- one major Champion + one normal/hardened anchor, or
- three hardened SHIELDs.

### 4 players
- one major Champion + one secondary durable threat, or
- one BRUTE + two hardened SHIELDs, or
- three differentiated durable anchors.

Current stress-test envelope produced median effective-threat budgets of approximately:

| Players | E event median threat index |
|---|---:|
| 2 | 12.1 |
| 3 | 21.6 |
| 4 | 32.0 |

These are **stress budgets**, not instructions to give one monster 5× HP. Final production E should split durability between:
- moderate HP increase,
- armor/damage reduction,
- one additional durable target,
- type choice,
rather than overloading a single health bar.

---

## 4. X — Special / Mixed recipes

X is the primary multiplayer scaling language.

### X-LINE
Shielded line / escort pressure.

| Players | Recipe |
|---|---|
| 2 | 1 SHIELD + 3 RUNNER + 2 FLYER |
| 3 | 2 SHIELD + 4 RUNNER + 2 FLYER + 1 BRUTE |
| 4 | 2 SHIELD + 5 RUNNER + 3 FLYER + 2 BRUTE |

### X-CLUSTER
Shielded dense group.

| Players | Recipe |
|---|---|
| 2 | 1 SHIELD + 3 GRUNT + 2 FLYER |
| 3 | 2 SHIELD + 4 GRUNT + 3 FLYER + 1 BRUTE |
| 4 | 2 SHIELD + 5 GRUNT + 4 FLYER + 2 BRUTE |

### X-SPLIT
Two-sided / separated pressure.

| Players | Recipe |
|---|---|
| 2 | 1 SHIELD + 3 RUNNER + 2 FLYER |
| 3 | 2 SHIELD + 5 RUNNER + 3 FLYER + 1 BRUTE |
| 4 | 2 SHIELD + 6 RUNNER + 4 FLYER + 2 BRUTE |

BRUTE/SHIELD members may receive event-specific hardened packages. Ordinary RUNNER/GRUNT/FLYER members should not receive the same durability multiplier by default.

---

## 5. Event-count scaling inside one stage

The number of active pressure **families** and the number of pressure **events** are separate concepts.

A one-pattern stage may repeat the same family several times without becoming a two-pattern stage.

Candidate event-count envelope:

| Players | 1-family stage | 2-family stage | 3-family stage |
|---|---:|---:|---:|
| 2 | 4 events | 5 events | 5 events |
| 3 | 5 events | 6 events | 6 events |
| 4 | 5 events | 6 events | 6 events |

Events are assigned to separated windows selected from roughly:
`early → early/mid → mid → late → late → final`

The same pressure family can recur at different windows, geometries and intensities.

---

## 6. Readability calibration

Across five prototype 50-stage tiers (250 authored grammar samples per team size), the current concrete recipes produced:

| Players | Mean total enemies / stage | P95 total | Mean max spawns in any 4 s | P95 max spawns in 4 s | P95 max spawns in 6 s |
|---|---:|---:|---:|---:|---:|
| 2 | 34.1 | 47.5 | 7.9 | 11 | 13.5 |
| 3 | 57.0 | 79.0 | 11.9 | 15 | 19 |
| 4 | 71.2 | 99.0 | 14.6 | 18 | 24 |

The important constraint is the short-window density, not total stage count.

The current candidate keeps the **95th percentile 4-second burst** around:
- 11 for 2 players,
- 15 for 3 players,
- 18 for 4 players.

This is the present readability envelope to carry into visual playtesting.

---

## 7. Role-opportunity preservation

Concrete recipes were checked against the already established class-response model.

Aggregate opportunity across all five 50-stage prototype tiers:

| Team-size model | Knight | Rogue | Tank | Archer | Mage |
|---|---:|---:|---:|---:|---:|
| 2-player recipe set | 20.5% | 19.0% | 20.2% | 21.1% | 19.2% |
| 3-player recipe set | 20.4% | 19.0% | 20.7% | 21.2% | 18.8% |
| 4-player recipe set | 20.4% | 19.1% | 20.5% | 21.2% | 18.8% |

Tier-local peaks remain:
- T2 raises Rogue value,
- T3 raises Archer value,
- T4 raises Tank value,
- Knight remains stable,
- Mage rises on cluster-heavy stages even when its campaign-wide aggregate is lower.

The goal is not equal damage. The goal is rotating situational value without long-run role starvation.

---

## 8. Not frozen

Still provisional:
- literal Champion HP multiplier,
- literal elite armor multiplier,
- exact stage duration,
- exact per-tier base-flow density,
- exact 2/3/4-player human multiplayer cadence,
- exact Lv11–21 implemented skill formulas,
- boss/checkpoint schedule,
- multiplayer shop/economy rules.

No live code should consume this file as production data yet.
