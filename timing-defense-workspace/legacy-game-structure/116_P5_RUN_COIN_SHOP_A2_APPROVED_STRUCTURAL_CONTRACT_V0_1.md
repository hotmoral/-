# Timing Defense — P5 Run Coin / Shop A2 Approved Structural Contract V0.1

Date: 2026-10-23 KST  
Status: **USER_APPROVED STRUCTURAL CONTRACT / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `112_P5_RUN_COIN_SHOP_AUTHORITY_RECOVERY_V0_1.md`
- `114_P5_RUN_COIN_SHOP_QUANTITATIVE_PRECHECK_V0_1.md`
- `115_P5_RUN_COIN_SHOP_REVISED_STRUCTURAL_PROPOSAL_V0_2.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`

Supersession:
- this document approves Package A2;
- where older P5 proposal doc113 conflicts with doc115 or this contract, this contract wins;
- older documents remain design history.

---

# 0. User approval

The user explicitly approved **A2** and additionally confirmed that a 50-Stage run economy where the player can routinely max all six shop tracks is undesirable.

Approved direction:

```text
EVERY-STAGE FAST/NONBLOCKING SHOP
+
PERSONAL WALLETS
+
PERSONAL KILLER-ONLY ORDINARY-MONSTER COIN BASELINE
+
ALL-HUMAN STAGE-CLEAR INCOME FLOOR CANDIDATE
+
FORTIFICATION = MAX HP + MATCHED CURRENT REPAIR
+
PERSONAL OFFENSE/CONTROL + SHARED WALL CONTRIBUTIONS
+
SIX SHOP CATEGORIES
```

No exact coin, price, rank-effect, cap or timer is approved by this contract.

---

# 1. Shop cadence — APPROVED STRUCTURE

After every cleared Stage except the Tier final Stage:

```text
Stage clear
-> lightweight shop/intermission opportunity
-> purchase optional
-> immediate READY / CONTINUE permitted
-> next Stage
```

Structural requirement:
- the mechanic is available every Stage;
- the UX must not require 49 long mandatory menu stops;
- exact quick-buy/preset/timeout/host behavior remains downstream implementation work.

---

# 2. Coin ownership — APPROVED BASELINE

## 2.1 Personal wallets
Each human player owns a personal run-local coin balance.

Coin:
- persists within the Tier attempt;
- resets on a new attempt according to P1;
- is restored with the same authoritative run state on reconnect.

## 2.2 Ordinary-monster kill coin
Baseline structural candidate approved for P5 simulation:

```text
ordinary enemy dies
-> killing human receives that enemy's kill-coin reward
```

This is **not** assumed fair by construction.
It remains subject to measured watches:
- class/team kill-share distribution;
- duration of shop-rank separation;
- kill-steal incentive;
- whether Tank/control-oriented contribution becomes materially underfunded.

The earlier proposal to automatically grant every kill reward to every human is **not** the approved baseline.

## 2.3 Stage-clear income floor
An all-human Stage-clear reward remains an approved **income-source candidate**.
Its exact formula and magnitude are open.

Purpose:
- provide predictable spend capacity independent of kill ownership;
- prevent unusual encounter composition from making the economy entirely volatile.

---

# 3. Fortification — APPROVED SEMANTIC

A WALL HP purchase is explicitly a Fortification event:

```text
wallMaxHp += realized purchased max-HP increase
wallCurrentHp += same realized increase
clamp current to new max
```

It is:
- explicit purchased repair;
- persistent run growth.

It is not:
- automatic Stage heal;
- refill-to-full;
- hidden between-Stage restoration.

Exact magnitude, cost, rank cap and multiplayer contribution scaling remain open.

---

# 4. Shared wall ownership — APPROVED STRUCTURE

```text
ATTACK / CRIT / CRIT DAMAGE / KNOCKBACK
= personal player run modifiers

FORTIFICATION / DEFENSE
= personal purchase decisions contributing to the one shared wall state
```

P2 remains authoritative for modifier composition.
Unique class/team defensive effects remain distinct from generic shop DEF.

Final 2/3/4P scaling, shared-wall normalization and generic-DR cap remain P10 dependencies.

---

# 5. Six-category shop — APPROVED FIRST CONTRACT

Retain:

```text
ATTACK
CRIT CHANCE
CRIT DAMAGE
FORTIFICATION
DEFENSE
KNOCKBACK
```

Structural rules:
- finite ranks;
- monotonically increasing marginal cost;
- ranks persist within one Tier attempt;
- ranks reset on a new attempt;
- no seventh category is introduced before evidence requires it.

Exact max rank is open.
Legacy Rank10 is a sensitivity seed only.

---

# 6. New economy constraint — APPROVED DIRECTION

The user explicitly rejected a routine economy in which all six shop categories can be maxed during the same ordinary successful Tier run.

Canonical design constraint:

```text
NO_ROUTINE_FULL_SHOP_MAXOUT_BY_STAGE49
```

Interpretation:
- intended-entry / ordinary successful runs must preserve meaningful allocation tradeoffs into the late Tier;
- a balanced build should still have useful purchase decisions in the late run;
- specialization may max or nearly max selected tracks if it sacrifices others;
- the economy must not make six-track maxout the expected or routine outcome before Stage50.

This contract does **not yet** freeze an absolute mathematical impossibility for every extreme high-kill/high-mastery outlier. That stronger boundary may be decided after P5 sensitivity simulation.

---

# 7. Legacy numerical values — explicitly NOT approved

The legacy prototype values are not carried over as production authority.

Known reason:
- Stage1..49 common clear reward under the old formula ~= 17,395;
- six legacy Rank10 tracks cost ~= 16,350 total;
- therefore clear reward alone could approximately full-max the entire shop by Stage48;
- individual tracks saturated around Stage16–18.

This violates the new late-run choice constraint.

---

# 8. Required P5 simulation

Compare at minimum:

```text
ATTACK_HEAVY
CRIT_HEAVY
DEFENSE_HEAVY
BALANCED
SAVE_DELAY
ROLE_AWARE
```

Required outputs:
- income by source;
- kill-share distribution;
- rank trajectory by Stage;
- first/maxed-track timing;
- total shop cost consumed / full-shop cost ratio;
- remaining meaningful purchase options at Stages 40/45/49;
- wall reserve and Fortification repair leverage;
- generic DEF leverage;
- clear/fail / clear time once combat integration is active;
- valid timing-action count and P4 skill-reach drift.

Mandatory watches:

```text
SHOP_SATURATION_TOO_EARLY
FULL_SHOP_MAXOUT_ROUTINE
DOMINANT_PURCHASE_POLICY
FORTIFICATION_ATTRITION_ERASURE
SHARED_DEF_PLAYER_COUNT_LEVERAGE
COIN_INCOME_CLASS_DIVERGENCE
SHOP_POWER_EXP_FEEDBACK_DISTORTION
```

---

# 9. Boundary after approval

P5 structural semantics are approved.

Next:
1. derive a bounded 50-Stage spend-capacity envelope;
2. run economy-only purchase-policy preflight;
3. choose/refine candidate income/cost curves;
4. only then integrate shop power with combat/EXP feedback.

Production gameplay remains unchanged and unauthorized.