# Timing Defense — P4-D2 Stage49 Full Rotation Directional Probe V0.1

Date: 2026-10-23 KST  
Status: **PROMISING FULL-ROTATION DIRECTIONAL RESULT / EXACT V0.4 COMMITTED REPLAY PENDING / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority / context:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md`
- `101_P4D2_ARMORED_DURABLE_PROXY_PRESSURE_PROBE_V0_1.md`
- `102_P4D2_DURABLE_TEMPORAL_PRESSURE_DIRECTIONAL_PROBE_V0_1.md`
- `103_P4D2_TANK_BARRIER_FIDELITY_CORRECTION_V0_1.md`
- `104_P4D2_STAGE49_TANK_TIME_BUDGET_ROLE_PULSE_PREFLIGHT_V0_1.md`
- `105_P4D2_V03_REPLAY_FAILURE_AND_V04_RUNNER_CORRECTION_V0_1.md`

Replay assets:
- `../../tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_4.py`
- `../../tools/run_p4d2_stage49_full_rotation_probe_v0_1.py`
- `data/p4d2_stage49_full_rotation_fixture_v0_1.json`
- `data/p4d2_stage49_full_rotation_directional_summary_v0_1.json`

---

# 0. Purpose

The previous work found useful pressure pieces separately:
- line pressure;
- cluster recovery;
- frontline breach;
- distributed durable pressure;
- Tank time-budget SIEGER pulse.

The question here is whether they can coexist in one rotating Stage49-like stress without:
- making Knight/Rogue the first casualties of blanket escalation;
- removing Tank's control identity;
- making Mage permanently bad against durable pressure;
- turning Archer into screen-wide AoE;
- requiring hidden class compensation.

Answer:

**YES — a promising bounded full-rotation candidate exists.**

It is not final Stage49 authoring.

---

# 1. Method / fidelity

Primary class lanes:

```text
Knight  COMMON_1P125_NO_BANK
Rogue   ROGUE_RECOVERY_DELTA_78MS_NO_BANK
Tank    COMMON_1P125_NO_BANK + v0.4 shared-barrier non-downgrade
Archer  COMMON_1P125_NO_BANK
Mage    COMMON_1P125_NO_BANK
```

The source-equivalent local reconstruction was first checked against the existing canonical v0.2 directional evidence and reproduced:
- all-success wall results;
- one-miss ranges;
- two-miss ranges;
- Rogue recovered-cadence burial range;
- all-finals-missed burial times.

Therefore it is admitted for **directional** work.

Exact committed v0.4 one-command checkout execution remains required before regression/freeze authority.

---

# 2. Full rotation candidate

Five grammar families rotate:

```text
LINE_ESCORT
CLUSTER_RECOVERY
FRONTLINE_BREACH
DURABLE_SCATTER
TIME_BUDGET_SIEGER
```

Important authoring detail:
- `DURABLE_SCATTER` uses only one diagnostic armored-durable proxy plus ordinary BRUTE/SHIELD/role bodies;
- `TIME_BUDGET_SIEGER` uses one durable proxy plus four readable SIEGER placements after the initial reset window;
- this is deliberately lighter than the rejected blanket durable+role pressure recipe.

The proxy remains diagnostic only and is not a new-monster approval.

---

# 3. All-success result

Using the current provisional Lv31 centers:

| Class | End wall | End active |
|---|---:|---:|
| Knight | **1705** | 21 |
| Rogue | **2000** | 16 |
| Tank | **2000** | 11 |
| Archer | **2000** | 6 |
| Mage | **2000** | 3 |

All five survive.

This is materially better than the first over-aggressive integrated attempt, which drove Knight/Rogue too hard.

The maximum all-success wall loss is now:

```text
Knight: 295 / 2000 = 14.75%
```

No exact acceptable Stage49 wall-reserve floor is frozen.

---

# 4. Stage continuity changes the interpretation

P1 run-state authority says BaseHP persists across stages and there is no automatic stage heal.

Therefore Stage49 cannot be judged only by:

```text
buried / not buried
```

A player who survives Stage49 at very low wall HP carries that damage into Stage50.

New watch:

```text
STAGE49_TO_50_WALL_RESERVE_CONTINUITY_WATCH
```

This is especially important when comparing large class-specific mistake budgets.

---

# 5. One missed final

Across all five grammar-aligned start points:

```text
Knight  survives all / wall970..1595
Rogue   survives all / wall1385..1705
Tank    survives all / wall2000
Archer  survives all / wall1740..2000
Mage    survives all / wall1890..2000
```

This is a good mastery shape:
- one isolated mistake is recoverable for every class;
- the penalty differs by class/active grammar rather than hidden compensation.

---

# 6. Two consecutive missed finals

All five classes still survive the bounded two-miss suites:

```text
Knight  wall820..1045
Rogue   wall340..1050
Tank    wall1725..2000
Archer  wall1700..2000
Mage    wall1890..2000
```

The important result is not identical wall loss.

Interpretation:
- Rogue can survive two misses but may enter Stage50 nearly exhausted;
- Knight receives meaningful attrition;
- Tank retains the largest immediate defensive budget;
- Archer/Mage remain more tolerant at two misses but are tested through longer repeated-failure windows.

This is preferable to mechanically forcing every class to die after exactly two mistakes.

---

# 7. Consecutive-miss error budgets

First burial count by grammar start within the bounded sweep:

## Knight

```text
LINE 4
CLUSTER 4
FRONTLINE 3
DURABLE 6
TIME_BUDGET 4
```

## Rogue — recovered 78ms lane

```text
LINE 3
CLUSTER 4
FRONTLINE 4
DURABLE 3
TIME_BUDGET 3
```

## Tank — barrier-corrected

```text
LINE 6
CLUSTER 6
FRONTLINE 5
DURABLE 5
TIME_BUDGET 4
```

This supports Tank's intended role:
- isolated/repeated mistakes consume the time budget more slowly;
- sustained failure still collapses the run.

## Archer

No burial inside the bounded eight-consecutive-miss sweep.
However Stage50 reserve becomes severe in several starts:

```text
DURABLE_SCATTER -> wall345
TIME_BUDGET_SIEGER ->785
CLUSTER_RECOVERY ->960
LINE_ESCORT ->1195
FRONTLINE_BREACH ->1650
```

Thus `not buried` does not mean `healthy` under persistent BaseHP.

## Mage

`TIME_BUDGET_SIEGER` buries at eight consecutive misses.
Other eight-miss starts survive with:

```text
LINE 355
CLUSTER 575
FRONTLINE 975
DURABLE 940
```

Again the Stage50 reserve is already seriously damaged.

---

# 8. All-finals-missed stress

When every available final opportunity is missed from the beginning:

```text
Knight  buried 34.025s
Rogue   buried 29.100s
Tank    buried 34.575s
Archer  buried 57.025s
Mage    buried 52.225s
```

Therefore:

```text
ALL_FIVE_CAN_IGNORE_LV31_PXP_INDEFINITELY = FALSE
```

This restores the desired late mastery property while preserving class asymmetry.

---

# 9. Archer monotonicity

In this full-rotation candidate, the bounded one-miss and two-miss suites produced:

```text
successMonotonicityWatchCount = 0 for all five classes
```

This is encouraging because the prior rotating grammar had Archer paths where a missed final could finish with more wall HP than the all-success path.

However the older Archer chronology watch is **not closed yet**.
The specific SPLITTER/target-order path still needs direct tracing before removing:

```text
LV31_ARCHER_SUCCESS_MONOTONICITY_CHRONOLOGY_WATCH
```

Do not alter Archer power/width from this result.

---

# 10. Why the full rotation works better

The candidate does not solve late difficulty with one global scalar.

It rotates distinct pressure questions:

```text
LINE_ESCORT
-> reward Archer line deletion / test deep line handling

CLUSTER_RECOVERY
-> give Mage a deliberate recovery/payoff window

FRONTLINE_BREACH
-> pressure frontline control/chunking

DURABLE_SCATTER
-> retain distributed durability without stacking several proxies every cycle

TIME_BUDGET_SIEGER
-> spend the time Tank buys and pressure off-corridor cleanup
```

This produces a more useful asymmetry than simply increasing HP/spawn count globally.

---

# 11. Verdict

```text
STAGE49_FULL_ROTATION_DIRECTION = PROMISING
ALL_SUCCESS_SURVIVES_ALL_FIVE = YES
ISOLATED_MISS_RECOVERABLE_ALL_FIVE = YES
ALL_FINALS_MISSED_BURIES_ALL_FIVE = YES
TANK_TIME_BUDGET_IDENTITY = PRESERVED
MAGE_CLUSTER_RECOVERY = PRESERVED
ROGUE_RECOVERED_CADENCE = PRESERVED
ARCHER_ONE_TWO_MISS_NONMONOTONICITY_IN_THIS_FIXTURE = NOT OBSERVED
STAGE49_TO_50_WALL_RESERVE = NEW ACTIVE WATCH
NEW_MONSTER_APPROVED = NO
NUMERICAL_FREEZE = NO
PRODUCTION_CHANGE = NO
```

---

# 12. Exact next boundary

Before P4-D2 provisional closure:

1. execute v0.4 + Stage49 full-rotation committed runners in a repository checkout and compare exact output;
2. trace the historical Archer SPLITTER/target-order nonmonotonic path directly;
3. carry the new Stage49->50 wall-reserve continuity watch into final authoring;
4. return to the remaining Stage46 Lv31 acquisition-distribution fairness work;
5. keep multiplayer/event-volume and P10R EXP/timebase watches active.

No user decision is required by this result.
