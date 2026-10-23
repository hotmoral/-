# Timing Defense — P5 Economy-Only Policy Preflight V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL PREFLIGHT PASS / WORKING CENTER IDENTIFIED / NO COMBAT AUTHORITY / NO NUMERICAL FREEZE**

Inputs:
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
- `data/p5_shop_economy_spend_capacity_fixture_v0_1.json`
- `tools/run_p5_shop_economy_spend_capacity_probe_v0_1.py`

---

# 0. Scope

This probe tests **purchase-capacity geometry only**.

It does not yet claim:
- combat optimality;
- final coin values;
- final shop prices/effects;
- final class kill-share;
- Fortification/DEF combat balance;
- EXP/skill-reach closure.

---

# 1. Exact reference rounding correction

The live prototype cost function uses positive-value JavaScript `Math.round`.
The exact nominal legacy Rank10 reference is therefore:

```text
ATK 2725
CRIT 3000
CRITDMG 2725
FORT 2455
DEF 3000
KNOCK 2455
TOTAL 16360
```

The earlier 16350 precheck number is superseded for numerical reference purposes.
The 10-unit correction does not change any structural conclusion.

---

# 2. Spend-capacity brackets

```text
LOW45    7362 nominal units
CENTER50 8180
HIGH55   8998
```

All are normalized sensitivity budgets, not production coin values.

---

# 3. Saturation result

Across tested policies at 45/50/55%:

```text
ALL_SIX_MAXED = false in every tested run
```

45%:
- no tested strategy maxes even one track by Stage49.

50%:
- DEFENSE_HEAVY maxes FORT around Stage45;
- ROLE_AWARE Knight/Tank may max KNOCK around Stage45–46;
- ROLE_AWARE Rogue/Mage may max ATK around Stage49;
- BALANCED maxes no track and ends around Rank7–8.

55%:
- some strongly favored tracks max around Stage45–49;
- nonfavored tracks remain materially incomplete;
- BALANCED still ends around Rank7–8 and maxes no track.

This is compatible with the approved intent:

```text
specialization can cap a selected axis late
but whole-shop completion remains unavailable/routine-false
```

---

# 4. Stage49 rank shapes at CENTER

```text
ATTACK_HEAVY
ATK9 / CRIT6 / CRITDMG9 / FORT7 / DEF6 / KNOCK7

CRIT_HEAVY
ATK8 / CRIT9 / CRITDMG8 / FORT6 / DEF6 / KNOCK7

DEFENSE_HEAVY
ATK6 / CRIT6 / CRITDMG6 / FORT10 / DEF8 / KNOCK8

BALANCED
ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8

SAVE_DELAY
ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8
```

Diagnostic role-aware examples:

```text
Knight ATK8 / CRIT6 / CRITDMG6 / FORT8 / DEF6 / KNOCK10
Rogue  ATK10 / CRIT7 / CRITDMG7 / FORT7 / DEF6 / KNOCK7
Tank   ATK6 / CRIT6 / CRITDMG6 / FORT8 / DEF8 / KNOCK10
Archer ATK9 / CRIT6 / CRITDMG9 / FORT7 / DEF6 / KNOCK7
Mage   ATK10 / CRIT7 / CRITDMG7 / FORT7 / DEF6 / KNOCK7
```

These priorities are diagnostic only.

---

# 5. Kill-credit wallet perturbation

Around CENTER, the first kill-share wallet sensitivity uses:

```text
LOW-KILL WALLET  = 47% full-shop capacity
CENTER           = 50%
HIGH-KILL WALLET = 53%
```

This approximates a modest ±6% whole-wallet shift around CENTER, consistent with an economy in which kill coin is a minority/secondary share of total income and last-hit distribution differs moderately.

Balanced Stage49 remains in the same broad Rank7–8 band across 47/50/53%.

Result:

```text
KILLER_ONLY_COIN_FIRST_ORDER_SATURATION_DEFECT = NOT SHOWN
TOTAL_ECONOMY_SCALE_REMAINS_PRIMARY_FIRST_ORDER_CONTROL
```

Actual class kill-share remains a combat-integrated watch.

---

# 6. Working recommendation

Admit for the next P5 analysis layer:

```text
WORKING_SPEND_CAPACITY_CENTER = 50% of full-shop reference cost
SENSITIVITY_BAND = 45% .. 55%
```

This is **not a production numerical freeze**.
It is a normalized economy design center.

Reason:
- 45% may be restrictive enough that no specialization ever completes a track;
- 55% remains safe from total saturation but is more generous;
- 50% gives late visible specialization completion while preserving broad tradeoffs.

---

# 7. Next layer — income source composition

Keep total CENTER fixed initially, then vary how much comes from predictable Stage-clear floor vs killer-only enemy rewards.

Recommended first sensitivity:

```text
CLEAR / KILL
80 / 20
70 / 30  <- working center candidate
60 / 40
```

Why:
- higher clear share limits class/last-hit wallet divergence;
- meaningful kill share preserves personal performance reward;
- 70/30 naturally turns a ±20% relative deviation in kill share into only about ±6% total-wallet deviation, matching the observed early sensitivity scale.

Do not freeze this split before testing encounter composition and player count.

---

# 8. Next boundary

1. test 80/20, 70/30, 60/40 income-source mixes at 45/50/55 total capacity;
2. perturb kill-share by class/player-count sensitivity;
3. reject mixes that create persistent multi-rank class divergence;
4. then integrate Fortification/DEF with wall-pressure combat;
5. then recheck P4 EXP/skill reach.

Production remains unchanged.