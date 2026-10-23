# Timing Defense — P5 All-Class Fixed-Rank Shop Combat Preflight V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL FIVE-CLASS PREFLIGHT COMPLETE / POST-SHOP LATE-PRESSURE RECONVERGENCE REQUIRED / COMMITTED RUNNER EXACT REPLAY PENDING / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`
- `121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
- `122_P5_TANK_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `123_P5_ALL_CLASS_SHOP_COMBAT_METHOD_FIDELITY_REVIEW_V0_1.md`

Assets:
- `data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json`
- `data/p5_all_class_fixed_rank_shop_stage49_directional_summary_v0_1.json`
- `../../tools/run_p5_all_class_fixed_rank_shop_stage49_probe_v0_1.py`

---

# 0. Scope

The first five-class Stage49 shop-combat integration applies only the stat families that are currently attributable cross-class in the P4 diagnostic kernel:

```text
ATK
FORTIFICATION
DEFENSE
```

Deferred:

```text
KNOCKBACK -> P5_KNOCKBACK_KERNEL_COVERAGE_GAP
CRIT / CRITDMG -> attack-template policy-correct lane required
```

Test matrix:
- five classes;
- `ATTACK_HEAVY / DEFENSE_HEAVY / BALANCED / ROLE_AWARE` Stage49 CENTER50 rank snapshots;
- legacy-relative effect scale `30% / 40% / 50%`;
- all-success / one missed final / two consecutive missed finals / all-finals-missed;
- detailed max-eight consecutive-miss sweep at 40% for BALANCED and ROLE_AWARE;
- Archer/Mage all-finals-missed ATK-vs-FORT-vs-DEF ablation.

Fortification is still modeled as fully retained Stage49 starting reserve. This remains defense-favorable and is not a real purchase-time run history.

---

# 1. Baseline fidelity admission for directional work

The independent all-class reconstruction reproduced the no-shop Stage49 reference before shop effects:

```text
Knight  all-success 1705 / all-finals-missed burial 34.025s
Rogue   all-success 2000 / all-finals-missed burial 29.100s
Tank    all-success 2000 / corrected burial         34.700s
Archer  all-success 2000 / all-finals-missed burial 57.025s
Mage    all-success 2000 / all-finals-missed burial 52.225s
```

This supports directional interpretation.

The newly committed one-command P5 runner has not yet received a checkout/exact-output replay admission. Therefore this document does **not** claim exact committed-runner authority.

---

# 2. 30/40/50 common-scale result

When every Lv31 final is missed from the beginning:

## Knight

Across the four purchase profiles:

```text
30% -> burial 35.20..38.90s
40% -> burial 36.70..39.15s
50% -> burial 39.30..40.50s
```

Knight remains mastery-sensitive under all tested scales.

## Rogue

```text
30% -> burial 34.70..35.73s
40% -> burial 35.43..36.25s
50% -> burial 36.33..38.45s
```

Rogue remains mastery-sensitive under all tested scales.

## Tank

```text
30% -> burial 36.33..37.05s
40% -> burial 36.33..37.23s
50% -> burial 37.08..38.38s
```

Tank remains mastery-sensitive while retaining its larger control/defense budget.

## Archer

Archer survives the 60s all-finals-missed stress in **all** tested 30/40/50 profiles.

End-wall ranges:

```text
30% -> 1632.6..1861
40% -> 1904..2032
50% -> 2054..2140
```

## Mage

Mage also survives the 60s all-finals-missed stress in all tested 30/40/50 profiles.

End-wall ranges:

```text
30% -> 302.5..1087.875
40% -> 978.6..1687.8
50% -> 1442.5..1938.375
```

The Mage 30% low-end reserve is materially damaged, while Archer retains a much healthier reserve.

---

# 3. 40% detailed failure-budget result

At the 40% diagnostic center, BALANCED / ROLE_AWARE max-eight consecutive-miss sweeps show:

### Knight
- several grammar starts bury at 7–8 misses;
- some late CLUSTER/FRONTLINE starts survive eight but carry reduced reserve;
- sustained failure remains dangerous.

### Rogue
- DURABLE can bury at 6;
- LINE/TIME_BUDGET around 7;
- some late starts survive eight with reduced reserve;
- sustained failure remains dangerous.

### Tank
- most tested starts bury around 6–7;
- some BALANCED late starts survive eight with only ~44–84 wall remaining;
- this preserves the intended time-budget identity rather than creating immunity.

### Archer
- no burial within eight consecutive misses for either BALANCED or ROLE_AWARE;
- worst observed eight-miss reserves remain approximately 1255–1509 in TIME_BUDGET and 1655–1796 in DURABLE.

### Mage
- no burial within eight consecutive misses for either BALANCED or ROLE_AWARE;
- many grammar starts retain near-full purchased reserve even after eight misses.

Classification:

```text
KNIGHT / ROGUE / TANK = POST_SHOP MASTERY PRESSURE STILL PRESENT
ARCHER / MAGE = CURRENT STAGE49 PRESSURE MARGIN TOO FORGIVING AFTER SHOP POWER
```

This is not a request for identical mistake budgets.

---

# 4. Archer/Mage ablation — root layer

The all-finals-missed survival shift is driven primarily by **ATK changing kill/order chronology**, not simply by Fortification/DEF.

## Archer BALANCED 30%

```text
NONE      -> burial 57.025s / kills99 / SIEGER shots6 / wall hits16
ATK_ONLY  -> survives / wall1600 / kills130 / SIEGER shots2 / wall hits4
FORT_ONLY -> survives barely / wall115 / kills113 / SIEGER shots7 / wall hits16
DEF_ONLY  -> burial59.325s
FORT+DEF  -> survives barely / wall226.562
FULL      -> survives / wall1861 / kills130 / SIEGER shots2 / wall hits4
```

Interpretation:
- defense reserve alone can move a near-60s cutoff across the line, but leaves a nearly exhausted Stage50 reserve;
- ATK creates the large qualitative change by deleting pressure earlier.

## Mage BALANCED 30%

```text
NONE      -> burial52.225s / kills92 / SIEGER shots16
ATK_ONLY  -> survives / wall455 / kills113 / SIEGER shots9
FORT_ONLY -> burial55.150s
DEF_ONLY  -> burial54.625s
FORT+DEF  -> burial55.525s
FULL      -> survives / wall776.113
```

Mage is even clearer: Fort/DEF alone do not rescue the run; ATK crosses the survival threshold by changing enemy removal and SIEGER exposure.

At 40%, the same pattern strengthens:
- Archer ATK_ONLY -> wall1600;
- Mage ATK_ONLY -> wall825;
- defensive-only Mage lanes still bury around 54.6–55.7s.

---

# 5. Why a single `40%` shop scale is not a final answer

The Tank-only preflight made 40% look plausible because it preserved Tank failure pressure.
The five-class probe shows that the same common scale interacts differently with class attack geometry and kill chronology.

Therefore:

```text
COMMON_40_PERCENT = useful diagnostic center
COMMON_40_PERCENT = NOT production recommendation
```

It would be incorrect to solve the result by assigning hidden class-specific shop prices or class-specific ATK multipliers.

The same universal stat can legitimately have different realized value across classes; late encounter pressure must be calibrated with the shop layer actually present.

---

# 6. Defense-heavy is not universally dominant

The result does not show a simple defensive-build takeover.

Example: Knight at 40%:

```text
DEFENSE_HEAVY starting wall2400
all-success end wall2331 / active backlog20

BALANCED starting wall2320
all-success end wall2320 / active backlog6
```

Lower offense creates real backlog/opportunity cost. Therefore `DEFENSE_HEAVY` cannot be declared dominant from raw HP/DR alone.

This supports the approved design principle that defensive investment must trade against offensive pressure removal.

---

# 7. New active watch

```text
P5_STAGE49_POST_SHOP_PRESSURE_MARGIN_WATCH = HIGH
```

Meaning:
- P4 Stage49 pressure was calibrated before the P5 shop power layer was integrated;
- after ordinary shop ATK is present, Archer/Mage can cross discrete kill-order thresholds that remove SIEGER/wall-contact pressure;
- late pressure must be reconverged after realistic shop purchase history is represented;
- do not nerf Lv31 power fantasy from this evidence;
- do not use hidden class shop compensation.

Keep active:
- `P5_KNOCKBACK_KERNEL_COVERAGE_GAP`
- `FORTIFICATION_ATTRITION_ERASURE`
- `DOMINANT_PURCHASE_POLICY`
- `SHOP_POWER_EXP_FEEDBACK_DISTORTION`
- `STAGE49_TO_50_WALL_RESERVE_CONTINUITY_WATCH`

---

# 8. Correct next order

Do **not** immediately author stronger Stage49 pressure from the current fixed-rank upper-bound lane.

First remove the largest remaining modeling bias:

```text
FULLY_RETAINED_STAGE49_FORTIFICATION
```

Next P5 slice:
1. model Fortification purchases at their actual Stage/shop acquisition times;
2. apply matched repair only at purchase time;
3. carry wall current/max HP continuously through representative multi-stage attrition;
4. measure wasted repair while near full and retained reserve after prior damage;
5. keep ATK purchase timing alongside it because ATK changes pressure chronology;
6. then reconverge Stage46–49 pressure with the realistic shop layer;
7. after combat timing changes, re-measure valid timing-event count / EXP / skill reach.

This ordering prevents over-authoring late pressure against an artificially generous Stage49 starting wall.

---

# 9. Verdict

```text
FIVE_CLASS_FIXED_RANK_SHOP_COMBAT = DIRECTIONAL COMPLETE
NO_SHOP_BASELINE_REPRODUCTION = PASS
KNOCKBACK_CROSS_CLASS_AUTHORITY = DEFERRED
CRIT_CRITDMG_AUTHORITY = DEFERRED
COMMON_30_40_50_SCREEN = INFORMATIVE_NOT_FREEZE
KNIGHT_ROGUE_TANK_SUSTAINED_FAILURE_DANGER = PRESERVED
ARCHER_MAGE_POST_SHOP_PRESSURE_MARGIN = TOO_FORGIVING IN CURRENT STAGE49 FIXTURE
PRIMARY_ARCHER_MAGE_DRIVER = ATK KILL/ORDER CHRONOLOGY
DEFENSE_HEAVY_UNIVERSALLY_DOMINANT = NOT DEMONSTRATED
HIDDEN_PER_CLASS_SHOP_CORRECTION = REJECT AS NEXT LAYER
NEXT = MULTISTAGE PURCHASE-TIME FORTIFICATION + ATK HISTORY
PRODUCTION_CHANGE = NO
```
