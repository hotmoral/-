# Timing Defense — P4-B Multiplayer / Timebase Precheck V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED DIAGNOSTIC COMPLETE / PREVIOUS D RECOMMENDATION NO LONGER SUFFICIENT / NO NEW EXP SEMANTICS AUTHORIZED**

Depends on:
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `82_P4B_EXP_STABILIZATION_DECISION_PROPOSAL_V0_1.md`
- `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `../combat_exact_v016.py`
- `../pressure_recipe_sim_v1.py`
- `data/skilled_v2_central_sequence_candidate_v0_1.yaml`

Machine-readable diagnostic:
- `data/p4b_multiplayer_timebase_precheck_v0_1.json`

---

# 0. Why this precheck was required

P4-B first found a large solo feedback loop:

```text
class skill raises combat efficiency
 -> fewer valid local timing turns
 -> less EXP opportunity
 -> later skill reach shifts
```

That evidence was real, but it did not prove the same magnitude in multiplayer.
In a shared fight, several players attack the same enemy pool, so one player's class efficiency changes the **team** clear time and therefore affects everyone's opportunity.

The user explicitly challenged two missing perspectives:
1. mixed-team play may compress individual class progression differences;
2. Stage-based progression differences may shrink when measured per real minute because fast teams clear Stages faster.

This precheck tests those points before any Stage Quality Budget decision.

---

# 1. Evidence boundary

This is a **bounded structural precheck**, not current production multiplayer balance.

The current 9-monster roster does not yet have a frozen 2P/3P/4P full-Tier scaling authority.
Therefore the precheck reuses the historical player-count-scaled 5-monster pressure lane only to test directionality.

Inputs:
- legacy player-count-scaled 2P/3P/4P encounter generator;
- current `SKILLED_V2_CENTRAL` streak-aware judgment stream;
- exact Lv6/Lv11/Lv16/Lv21 v0.16 formulas as simulation parity candidates;
- all team slots modeled as human central-skilled players;
- pure per-valid-turn `XP_CREDIT` semantics retained;
- fixed-level snapshots at Lv6/11/16/21;
- T1–T4 sampled;
- player action phase/order randomized and rotated to remove fixed-slot bias.

Volume:

```text
2P: 8 seeds per Tier × composition × level
3P: 8 seeds per Tier × composition × level
4P: 12 seeds per Tier × composition × level
```

Absolute XP/min, clear rate and Stage duration are not production targets.

---

# 2. First important correction — solo divergence does not transfer 1:1

The shared multiplayer enemy pool materially compresses the solo effect.

A strong Mage/Archer/Rogue no longer shortens only its own fight. It shortens the same Stage for teammates too.
Therefore the earlier solo conclusion:

```text
Mage kills faster -> Mage alone loses most later turns
```

becomes in multiplayer:

```text
Mage contributes to faster team kill
 -> all teammates lose some available time/turns
```

So the first P4-B solo divergence remains a valid **SOLO_PROGRESSION_DIVERGENCE_WATCH**, but it is not by itself proof of a universal multiplayer EXP-system failure.

---

# 3. 4P Lv21 team-level comparison

Representative all-human central-skilled results across T1–T4:

| Team | Stage time | XP credit/player/Stage | XP credit/player/min | Clear |
|---|---:|---:|---:|---:|
| TTTT | 48.25 s | 77.73 | 96.66 | 100% |
| RRRR | 46.73 s | 68.31 | 87.72 | 100% |
| AAAA | 47.02 s | 62.92 | 80.30 | 100% |
| MMMM | 46.46 s | 68.12 | 87.98 | 100% |
| TRAM | 47.12 s | 66.73 | 84.98 | 100% |

Legend: T=Tank, R=Rogue, A=Archer, M=Mage.

Two observations matter simultaneously.

## A. Stage-based differences remain
Tank-heavy teams obtain more attacks/credit per Stage because combat takes longer or leaves more target opportunity.

## B. Real-time normalization does not erase the difference
At Lv21 the strong teams do **not** turn their extra damage into proportionally more Stages per minute.
Most sampled Stage durations converge near roughly 46–48 seconds because authored spawn timing/cadence creates a floor.
Extra damage often becomes no-target/down-time rather than a proportionally faster next Stage.

Thus:

```text
higher team DPS
 != automatically equal XP/min through faster Stage throughput
```

---

# 4. Mixed team — individual progression is closer, but not equal

For 4P `TRAM` at Lv21, individual XP credit/min was:

```text
Tank    91.83
Rogue   93.53
Archer  79.32
Mage    75.06
```

Max/min spread: about **24.6%**.

This is much less extreme than directly extrapolating the solo feedback model, so the user's compression hypothesis is supported.
But mixed-team membership does not make all players level at the same speed.

Remaining causes include:
- class action cadence differences;
- class-specific recovery effects such as Rogue Lv16;
- target availability at each player's action instant;
- geometry/coverage causing some players to create or encounter no-target windows sooner;
- shared kill timing.

At earlier milestones the mixed-team spread was smaller in this lane:

```text
TRAM Lv6   ~11.1%
TRAM Lv11  ~12.6%
TRAM Lv16  ~17.0%
TRAM Lv21  ~24.6%
```

So multiplayer compresses the solo split, but skill divergence can reappear as the run develops.

---

# 5. Same class, different teammates

The user also identified a second issue: the same class may level differently depending on team composition.

At 4P Lv21, the observed XP/min range for the **same class** across tested compositions was:

| Class | Min | Max | Relative range |
|---|---:|---:|---:|
| Knight | 89.06 | 101.74 | 14.25% |
| Rogue | 87.44 | 93.53 | 6.96% |
| Tank | 90.14 | 96.62 | 7.19% |
| Archer | 75.13 | 80.29 | 6.86% |
| Mage | 73.68 | 88.00 | 19.45% |

Therefore the progression question is not only:

```text
class -> XP speed
```

It is also:

```text
class × teammates × player-count scaling × encounter cadence -> XP speed
```

This is a distinct dependency that the solo-only P4-B decision packet did not cover.

---

# 6. Player count also changes progression opportunity

The reused pressure lane intentionally scales workload with player count.
At Lv21, Tank-only examples were:

```text
2P TT   ~81.24 credit/min/player
3P TTT  ~93.42
4P TTTT ~96.66
```

Archer-only:

```text
2P AA   ~68.29
3P AAA  ~78.81
4P AAAA ~80.30
```

These absolute numbers are not current production balance.
They demonstrate a structural point:

> Any future multiplayer HP/count/spawn scaling policy can materially change per-player EXP opportunity even when the EXP formula itself is unchanged.

Therefore final EXP semantics cannot be judged independently from multiplayer combat scaling.

Classification:

`PLAYER_COUNT_SCALING_XP_DEPENDENCY`

---

# 7. More EXP opportunity can coincide with worse practical progression

The Tank homogeneous lane is an important counterexample to judging XP in isolation.

In the historical 4P pressure lane:

```text
TTTT Lv6  clear ~68.8%, credit/min ~112.2
TTTT Lv11 clear ~64.6%, credit/min ~111.7
TTTT Lv16 clear ~60.4%, credit/min ~111.4
TTTT Lv21 clear 100%,   credit/min ~96.7
```

The early Tank-only team has high EXP opportunity because fights last longer, but it also fails more often under this old pressure envelope.

Thus a higher `credit/min while fighting` does not automatically mean faster practical campaign progression.
A full run must jointly evaluate:
- clear/fail probability;
- wall attrition;
- Stage throughput;
- retry cost;
- XP/min;
- skill reach.

This is another reason not to patch EXP from the solo result alone.

---

# 8. Reassessment of Option D

The previous document 82 recommended `Stage Quality Budget + raw-turn hybrid` before this multiplayer/timebase comparison existed.

That recommendation is now **insufficiently supported for immediate approval**.

Why:
1. multiplayer materially compresses the solo class split;
2. team composition creates a different progression dependency;
3. real-time normalization helps, but does not fully equalize progression;
4. player-count encounter scaling itself changes XP opportunity;
5. clear/failure risk can oppose the raw XP advantage;
6. current 9-monster 3P/4P full-Tier scaling is not yet authoritative.

This does **not** prove Option D is wrong.
It means the evidence is not yet sufficient to change the already-approved pure per-turn EXP semantics.

---

# 9. Current classifications

Keep all of these simultaneously:

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
```

Do not collapse them into one metric.

---

# 10. Recommended interpretation

For now:
- retain pure per-valid-turn EXP as the **provisional diagnostic baseline**, because it is the last user-approved semantic;
- do not numerically freeze it as final;
- do not activate Option D yet;
- do not add class/Tier multipliers;
- continue using encounter authoring to fix genuinely bad combat pacing, not to hide progression bias;
- treat final EXP convergence as dependent on a later current-roster multiplayer scaling pass.

The next planning decision should separate:
1. **skill-contract work** (Lv26/Lv31 identities can be reviewed structurally), from
2. **final progression convergence** (must be rechecked after credible multiplayer scaling exists).

Production remains untouched.
