# Timing Defense — Balance Simulation v5: Tier Pressure Grammar / Role Opportunity

Date: 2026-10-20 KST
Status: **REPORT ONLY — no playable/live balance values changed**

## Goal

Test the newly agreed encounter-pressure philosophy:

- `X` special/elite composition is the normal base pressure language,
- `S` swarm pressure and `E` extreme durability pressure are inserted at different times rather than globally applied all stage long,
- a stage may use 1, 2 or 3 pressure families,
- 3-pattern stages must remain a minority overall,
- each 50-stage tier should have a recognizable identity through pattern frequency, internal ratios, geometry and timing.

The full structural grammar is documented in `TIER_PRESSURE_GRAMMAR_V1.md`.

## Important modeling boundary

v5 is **not yet a final combat-clear-rate simulation**.

It is a structural encounter-model pass that answers:
1. can 50-stage tiers stay varied without repeating S+E+X every stage?
2. can different tiers create different class-opportunity profiles while preserving all five roles across the larger campaign?
3. can a higher tier become harder without monotonically increasing pattern count?
4. does the proposed grammar create obvious structural starvation for any class before exact spawn recipes are authored?

No class damage coefficient, Stage 1–10 live rule, boss resistance, EXP rule or live code is changed here.

---

# 1. Prototype tier-complexity distribution

Five representative 50-stage tier identities were generated.

| Tier | 1-pattern | 2-pattern | 3-pattern |
|---|---:|---:|---:|
| T1 Foundations | 30 | 17 | 3 |
| T2 Breakers | 21 | 23 | 6 |
| T3 Rushline | 17 | 25 | 8 |
| T4 Crossfire | 11 | 25 | 14 |
| T5 Extremes | 23 | 19 | 8 |

Across all 250 prototype stages:
- 1-pattern: **102 = 40.8%**
- 2-pattern: **109 = 43.6%**
- 3-pattern: **39 = 15.6%**

Therefore **84.4% of stages use only one or two pressure families**.

This directly addresses the repetition concern. A 3-pattern stage can remain memorable because it is not the default grammar.

T5 is especially important: despite being the highest of these prototype tiers, it intentionally returns from T4's 28% triple-pattern rate to 16% and raises the share of focused 1-pattern stages again. Difficulty is produced by **extreme intensity / timing / internal ratios**, not just by adding more pattern types.

---

# 2. Pattern identity by tier

Pattern occurrences:

| Tier | Swarm S | Elite E | Special X |
|---|---:|---:|---:|
| T1 | 25 (34.2%) | 24 (32.9%) | 24 (32.9%) |
| T2 | 24 (28.2%) | **37 (43.5%)** | 24 (28.2%) |
| T3 | **40 (44.0%)** | 19 (20.9%) | 32 (35.2%) |
| T4 | 32 (31.1%) | 28 (27.2%) | **43 (41.7%)** |
| T5 | 30 (35.3%) | **31 (36.5%)** | 24 (28.2%) |

Interpretation:
- **T1** is deliberately balanced and readable.
- **T2** clearly reads as the durability/elite tier.
- **T3** clearly reads as the swarm + tempo tier.
- **T4** clearly reads as the mixed-special / rapid role-switch tier.
- **T5** is not simply "more T4". It returns to focused stages and alternates large swarm extremes with high-durability extremes, with more late/final pressure.

---

# 3. Geometry is required to keep Archer and Mage distinct

The grammar does not model S or X as one generic multi-target pressure.

Exact prototype formation allocations:

## S formations
| Tier | line | cluster | scatter |
|---|---:|---:|---:|
| T1 | 8 | 11 | 6 |
| T2 | 7 | 11 | 6 |
| T3 | **22** | 10 | 8 |
| T4 | 8 | 10 | **14** |
| T5 | 9 | **17** | 4 |

## X formations
| Tier | line | cluster | split |
|---|---:|---:|---:|
| T1 | 7 | 6 | 11 |
| T2 | 5 | 6 | 13 |
| T3 | **14** | 5 | 13 |
| T4 | 9 | 8 | **26** |
| T5 | 6 | 6 | 12 |

This lets T3 create many Archer-friendly line events while T5 can create many Mage-friendly cluster swarms, and T4 creates many Tank/generalist split-pressure situations.

---

# 4. Role-opportunity calculation

To avoid pretending that a structural grammar is already a full combat-DPS simulator, v5 uses a **pressure-coverage model**, not raw damage.

Each geometry/pressure archetype is assigned a role-response vector derived from the already observed v1/v4 behavior:

- E: Rogue is primary; Knight/Archer remain useful.
- S-line: Archer primary.
- S-cluster: Mage primary.
- S-scatter: Knight/Tank/general coverage rises.
- X-line: Archer primary with Tank support.
- X-cluster: Mage/Tank share value.
- X-split: Tank primary, Knight/Archer secondary.

A cooperative coverage function values the strongest response plus smaller second/third contributions. Exact Shapley allocation across the five classes is then used to assign each pressure budget fairly among the roles.

This metric is **not a claim about final damage share**. It measures how much of the encounter-problem space each class helps cover.

### Per-archetype Shapley role shares

| Pressure archetype | Knight | Rogue | Tank | Archer | Mage |
|---|---:|---:|---:|---:|---:|
| S-line | 16.9% | 9.1% | 14.6% | **40.7%** | 18.7% |
| S-cluster | 16.2% | 9.1% | 17.7% | 15.4% | **41.5%** |
| S-scatter | **25.6%** | 12.0% | 23.7% | 21.9% | 16.8% |
| E | 18.3% | **39.5%** | 14.2% | 16.6% | 11.4% |
| X-line | 18.1% | 12.1% | 21.4% | **34.3%** | 14.2% |
| X-cluster | 18.3% | 12.5% | 26.1% | 16.0% | **27.2%** |
| X-split | 19.9% | 12.4% | **33.6%** | 18.7% | 15.4% |

The important property is not equality. It is that **different encounter geometries naturally rotate the high-value class**.

---

# 5. Tier-level class opportunity

Using each tier's exact S/E/X frequency, internal pressure ratios, formation quotas and timing/intensity budgets:

| Tier | Knight | Rogue | Tank | Archer | Mage |
|---|---:|---:|---:|---:|---:|
| T1 Foundations | 18.5% | 20.9% | 19.8% | 21.7% | 19.1% |
| T2 Breakers | 18.6% | **26.8%** | 18.8% | 19.1% | 16.7% |
| T3 Rushline | 18.6% | 14.0% | 20.5% | **26.9%** | 20.0% |
| T4 Crossfire | 19.0% | 17.0% | **24.0%** | 21.5% | 18.4% |
| T5 Extremes | 18.1% | 22.1% | 18.7% | 21.1% | 20.1% |

This is exactly the behavior the pressure grammar is intended to create:
- T2 gives Rogue a visible durability-specialist season.
- T3 gives Archer a visible line/tempo-specialist season.
- T4 raises Tank value under split/special pressure.
- T5 alternates focused extremes instead of assigning one class permanent ownership.
- Knight remains unusually stable across every tier, consistent with the generalist role.

### Aggregate across all 250 prototype stages

| Knight | Rogue | Tank | Archer | Mage |
|---:|---:|---:|---:|---:|
| **18.6%** | **20.1%** | **20.4%** | **22.0%** | **18.9%** |

The entire 250-stage prototype opportunity range is only **3.4 percentage points** from lowest to highest class, despite strong tier-specific peaks.

That is a useful result: the system can create locally strong class moments without structurally starving a class over the larger campaign.

---

# 6. Timing identity

Prototype timing biases:

| Tier | early | mid | late | final |
|---|---:|---:|---:|---:|
| T1 | 22% | 34% | 28% | 16% |
| T2 | 14% | 36% | 34% | 16% |
| T3 | 16% | 25% | 34% | 25% |
| T4 | 18% | 28% | 30% | 24% |
| T5 | 10% | 24% | 30% | **36%** |

This means "same pattern" does not automatically mean "same stage".

Example:
- T1 S-only can be a mid-stage learning burst.
- T5 S-only can be a long quiet lead-in followed by an extreme final flood.

The pressure family remains S, but the experience is different.

---

# 7. Pair/triple internal ratios prevent formulaic stages

The model also varies **how much of the stage pressure budget each active pattern owns**.

Examples:
- T1 pair ≈ 55/45.
- T2 E-pair ≈ 65/35 in E's favor.
- T3 triple ≈ S45/E15/X40.
- T4 triple ≈ S25/E20/X55.
- T5 pair ≈ 70/30 and triple stages rotate one ~60% dominant pattern.

So two stages can both be `S+E` but still ask for different play:
- one can be a mostly-E assassination check with a small cleanup swarm,
- another can be a swarm stage with one hard anchor target.

This substantially increases the number of distinct encounter shapes without adding new monster systems.

---

# 8. Anti-repetition check

The generated prototype schedules enforce stage-signature variation.

Result:
- exact same signature back-to-back: **0** in all five 50-stage prototype schedules.
- higher complexity may intentionally persist across adjacent stages in T4, but the actual signature / ratio / geometry / timing changes.

This is important because complexity alone is not the variety metric. `S+X` line-late and `E+X` split-mid are both 2-pattern stages but play differently.

---

# 9. What v5 supports

The proposed pressure-grammar concept is structurally sound enough to continue.

Supported conclusions:
1. 1/2/3-pattern mixing can avoid the "every stage uses all three tricks" problem.
2. higher tiers do not need monotonically more pattern types; focused extreme stages remain viable.
3. class opportunity can rotate strongly by situation while remaining broadly balanced over many stages.
4. geometry must be authored as part of pressure, not treated as cosmetic placement.
5. timing position and internal pressure ratio are major identity axes and should be stored in stage data.

---

# 10. What v5 does NOT authorize

Do **not** implement the exact prototype counts as final production data yet.

Not frozen:
- final number of tiers,
- final tier names/order,
- exact monster count per S budget,
- exact HP/armor multiplier per E budget,
- exact enemy recipes for X,
- 2/3/4-player pressure multipliers,
- exact stage length,
- final boss/checkpoint schedule.

No live code or balance patch was changed by v5.

---

# 11. Next analysis boundary

The next useful step is to translate these abstract pressure budgets into **concrete spawn recipes** using the current monster roster:
- GRUNT
- RUNNER
- BRUTE
- SHIELD
- FLYER

Then simulate 2/3/4-player teams under the same generated grammar and calibrate how team size changes:
- extra elite count,
- elite durability,
- swarm burst size,
- special composition density,
- event overlap,
while preserving battlefield readability.

Class coefficients should remain unchanged during that calibration unless a separate reported/approved balance decision is made.
