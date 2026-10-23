# Timing Defense — Next Work Boundary

Updated: 2026-10-24 KST

## Live recovery
Before work:
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_37.yaml`;
5. read `151_P6_ENCOUNTER_FAMILY_ROTATION_AND_TANK_OBJECTIVE_ATTRIBUTION_RESULT_V0_1.md`;
6. read **latest** `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`;
7. for P6-B2, read P4 `79`, `81`, `85`, `111` and P5 shop `116`, `118`, `119`, `123`, `124` before touching a progression model;
8. only then open exact source/evidence for the approved next unit.

Do not rerun closed fidelity, entry charge/combo, P6-S1, P6-A encounter-family, Tank scalar bracket, or P6-B1 shop-ATK attribution without a concrete trigger.

---

# Current phase

```text
P6 = FORMALLY ENTERED / USER APPROVED
P6-S1 = COMPLETE
P6-A encounter-family convergence = COMPLETE
P6-B1 shop ATK -> EXP-opportunity attribution = COMPLETE
CURRENT = P6-B2 METHOD DECISION GATE
Tier count / monster unlock ladder / exact T1 roster = DEFERRED UNTIL P6 CONVERGENCE
production = UNCHANGED / UNAUTHORIZED
```

---

# Tank identity guard — important

The class-selection radar is player-facing identity authority:

```text
Tank ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
```

User clarification:

```text
Tank is not a monster-killing class.
Low removal by itself is not a defect.
Its job is control / defense / wall protection.
```

Therefore current Tank watch is only:

```text
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
```

P6-A already showed push/barriers/Aftershock slow/Iron Wall materially reduce wall pressure.
Do not tune Tank ATK or seek clear-rate parity merely because dense removal-heavy packets produce low Tank completion.

---

# Closed P6-A result

Class ranking rotates by encounter family.

```text
BASELINE dense/aligned:
Mage19 Archer19 Rogue9 Knight7 Tank2

durable/distributed:
Knight20 Mage20 Archer20 Rogue17 Tank3

screened CHARGER:
Knight20 Archer20 Rogue18 Mage18 Tank3
```

This closes the question that the current Stage46/47 ordering might be a universal class-power ranking.
It is not.

Do not equalize one diagnostic packet numerically.

---

# Closed P6-B1 result

Exact run:
```text
40029402035
SHA256 83b5e1630231fb38426ae878cd3f2b6e7f3cd99894a44bac8416d0f23d614788
exact-byte repeat PASS
```

Cumulative summary:
```text
40029618307 PASS
```

Temp lane:
```text
timing-defense-workspace-temp-p6-shop-exp-opportunity
HEAD 7d83360da97cf0add2256c0b391d1dac7e9cd9a6
```

Paired skilled through49:
```text
ATK_OFF 17/100
ATK_ON  48/100
31 survival promotions
0 regressions
```

Same-path clean cumulative cohort (both variants through49):
```text
17 pairs
root actions ~-4.19%
provisional XP_CREDIT ~-3.89%
```

Survival-promotion cohort:
```text
31 pairs
root actions ~+68.66%
provisional XP_CREDIT ~+70.38%
```

Therefore:

```text
SHOP_ATK_TO_EXP_FEEDBACK = BIDIRECTIONAL / OUTCOME-CONDITIONED
```

Two simultaneous paths:
1. faster removal -> fewer valid timing turns -> EXP self-damping;
2. better survival -> later Stages become available -> more total timing turns/EXP opportunity.

Do not use a flat negative shop->EXP multiplier.
Do not project the late ~4% clean compression across Stage1-45.

---

# Historical P4-B reproducibility boundary

The old P4-B evidence remains useful but its dedicated propagation runner was not retained in the historical canonical tree.
Available:
- P4-B result JSON;
- P4-B report;
- P4-A runner/validator;
- P3 and older combat/role simulators.

Not available:
- a dedicated reproducible P4-B full propagation runner.

So exact skill-reach drift cannot be reconstructed by silently inventing a linear formula.

---

# CURRENT USER DECISION REQUIRED — P6-B2 METHOD

Goal:
```text
Estimate Stage1-45
shop history
× skill power
× combat opportunity
× EXP
× skill-reach timing
```
without prematurely freezing exact Tier1 content.

## A — recommended: rebuild a bounded P4-B-style synthetic combat-feedback runner
Then inject P5 stage-by-stage shop trajectories.

Why preferred:
- preserves approved dependency order;
- closest continuity with prior P4-B evidence;
- lets P6 converge before exact Tier1 Stage1-50 authoring;
- can be fidelity-checked against P3/P4-B historical anchors and P6-B1 shop response.

Required safeguards:
- explicit reconstruction contract before treating results as authority;
- reproduce old P4-B known anchors first;
- use current class/skill semantics where authoritative;
- use actual simulated timing-action counts, not a flat reduction multiplier;
- preserve SKILLED_V2 / Heavy one-award EXP semantics;
- inject actual P5 diagnostic stage-by-stage shop trajectories;
- no final EXP/shop numeric freeze.

## B — provisional full Stage1-50 combat fixture first
More direct, but risks violating the approved order by effectively authoring Tier1 before P6 has converged.
Not recommended now.

## C — defer exact skill-reach propagation
Safest from synthetic assumptions but leaves P6 progression convergence unresolved before Tier/unlock work.
Not recommended unless the user wants to postpone the question.

Recommended choice:
```text
A
```

**Do not implement/adopt A until user approval, because rebuilding the missing P4-B propagation model is a new methodology contract.**

---

# Fixed guards

```text
LIVE REMOTE WINS
SKILLED_V2_CENTRAL STAYS FIXED FOR CURRENT CAUSAL COMPARISONS
HEAVY X+Y = ONE EXP AWARD
STAGE_SETTLED REQUIRED
WALL DEFICIT / COMBO / CHARGE PERSIST
SURVIVAL != CLEAR
NO HARD CLASS LOCKOUT
TANK LOW REMOVAL IS INTENTIONAL
NO TANK DAMAGE BUFF FROM CLEAR-RATE EQUALITY PRESSURE
NO FLAT SHOP->EXP MULTIPLIER
NO LINEAR STAGE1-45 PROJECTION FROM LATE-RUN 4% RESULT
NO P×P PROBABILITY PATCH TO FIT CONTENT
NO ARMORED PROXY ADOPTION
NO EXACT TIER1 ROSTER/UNLOCK ASSUMPTION
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```