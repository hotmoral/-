# Timing Defense — P5 Fortification Damage-Deficit Invariance Correction V0.1

Date: 2026-10-23 KST  
Status: **STRUCTURAL INTERPRETATION CORRECTION / SUPERSEDES CONFLICTING ATTRITION-ERASURE LANGUAGE / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `120_P5_FORTIFICATION_DEFENSE_LEVERAGE_UPPER_BOUND_V0_1.md`
- `122_P5_TANK_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`

Supersession rule:
- where docs120/122/124 or current handoff text imply that the approved Fortification formula can reduce/erase an already-existing absolute damage deficit merely because it adds current HP, this document wins;
- prior numerical leverage observations remain valid where they concern total reserve, not deficit erasure.

---

# 0. Approved formula

A Fortification purchase realizes:

```text
wallMaxHp += delta
wallCurrentHp += delta
clamp current to new max
```

Given the valid precondition:

```text
wallCurrentHp <= wallMaxHp
```

then after purchase:

```text
newMax     = oldMax + delta
newCurrent = oldCurrent + delta
```

because `oldCurrent + delta <= oldMax + delta`.

---

# 1. Damage-deficit invariant

Define accumulated absolute wall damage deficit:

```text
D = wallMaxHp - wallCurrentHp
```

After Fortification:

```text
D' = (wallMaxHp + delta) - (wallCurrentHp + delta)
   = wallMaxHp - wallCurrentHp
   = D
```

Therefore:

```text
FORTIFICATION_PURCHASE_DOES_NOT_REDUCE_EXISTING_ABSOLUTE_DAMAGE_DEFICIT
```

Example:

```text
before: max2000 / current1500 / deficit500
buy +100 Fortification

after:  max2100 / current1600 / deficit500
```

The purchase adds 100 usable reserve, but it does not heal the prior 500 damage.

---

# 2. Correct semantic language

The approved `matched current increase` remains intentional because a purchased max-HP upgrade must be immediately usable.

However it should not be described as:
- refill-to-full;
- healing away old attrition;
- reducing prior damage deficit;
- repair whose value is wasted when bought at full HP.

More precise interpretation:

```text
FORTIFICATION = PURCHASED DURABILITY GROWTH
max capacity +delta
current usable durability +delta
existing absolute deficit unchanged
```

The project may still use the word `repair` in UI/product language if desired, but simulation/governance must use the invariant above.

---

# 3. Purchase timing consequence

For Fortification **alone**, if the same total ranks are eventually bought and the incoming-damage history is otherwise identical:

```text
final absolute deficit is independent of Fort purchase timing
```

Buying +100 before or after an unrelated 300 damage event yields the same final max/current pair modulo the ordering of death checks.

Important exception:
- if the wall would hit zero before a later Fort purchase can occur, order obviously matters because the run has already ended;
- ATK/DEF purchase timing changes future incoming-damage history, so the full shop system still requires temporal integration.

---

# 4. Correction to the fixed-rank Stage49 interpretation

The fixed-rank Stage49 probes start at:

```text
current wall = new max wall = 2000 + realized Fort flat
```

They are still defense-favorable upper-bound lanes, but **not because Fortification timing erased prior attrition**.

The true optimistic assumption is:

```text
PRE_STAGE49_DAMAGE_DEFICIT = 0
```

A real Tier run carries Stage1–48 damage into Stage49.

Therefore the next temporal layer must model/parameterize the inherited pre-Stage49 deficit produced by earlier combat and by earlier ATK/DEF acquisition timing.

---

# 5. Watch correction

The prior broad watch:

```text
FORTIFICATION_ATTRITION_ERASURE
```

is structurally misleading under the approved formula and is superseded by:

```text
FORTIFICATION_TOTAL_RESERVE_LEVERAGE
PRE_STAGE49_DAMAGE_DEFICIT_CONTINUITY
FORTIFICATION_DEATH_CHECK_TIMING
SHARED_FORTIFICATION_PLAYER_COUNT_LEVERAGE
```

Fortification can still be numerically too strong by adding too much total reserve for its cost. It simply does not do so by deleting existing damage deficit.

---

# 6. Downstream implication

Do not build a complex purchase-time `repair wastage` simulator for Fortification itself.

Instead:
1. recover/estimate the wall deficit entering late stages;
2. model ATK/DEF acquisition timing because they change future damage chronology;
3. apply Fortification as deterministic max+current growth with invariant deficit;
4. test death before later purchase opportunities;
5. reconverge Stage46–49 pressure with the resulting shop power and carried deficit.

This is cheaper and more faithful than simulating a nonexistent attrition-heal mechanism.

---

# 7. Verdict

```text
FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE = CONFIRMED
FORTIFICATION_ERASES_PRIOR_ATTRITION = FALSE
FORTIFICATION_ADDS_USABLE_RESERVE = TRUE
FIXED_RANK_STAGE49_ZERO_PRIOR_DEFICIT = OPTIMISTIC ASSUMPTION
PURCHASE_TIME_FORT_REPAIR_WASTAGE_MODEL = NOT NEEDED
ATK_DEF_TEMPORAL_FEEDBACK = STILL NEEDED
PRODUCTION_CHANGE = NO
```
