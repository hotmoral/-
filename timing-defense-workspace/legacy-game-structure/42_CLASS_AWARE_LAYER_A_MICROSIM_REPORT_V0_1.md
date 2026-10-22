# Timing Defense — Class-Aware Layer-A Micro-Sim Report V0.1

Date: 2026-10-22 KST  
Status: **CURRENT-AUTHORITY MECHANICS PROBE / NOT SKILLED_V2 CALIBRATION**

Inputs:
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_kinematic_anchor_v0_1.yaml`
- `data/model_a_combat_sensitivity_anchor_v0_1.yaml`
- `data/model_a_class_action_trace_bracket_v0_1.yaml`
- `tools/simulate_class_aware_layer_a.py`

Power mode used for headline results:
`CURRENT_AUTHORITY_LV6`

Important:
- trace values are unfitted brackets
- no production difficulty claim is made here
- this report is for structural/mechanics diagnosis

---

# 0. Critical subset

First pass used 10 representative encounters chosen to cover class roles and current special capabilities:

- T1_E03_M — durable frontline
- T2_E14_H — air/rush geometry
- T3_E07_M — exposed CHARGER
- T3_E13_H — rush + CHARGER
- T3_E15_M — SPLITTER + rush
- T3_E17_M — screened CHARGER
- T4_E11_M — escorted SIEGER
- T4_E12_M — SUPPORTER + bulwark
- T4_E16_M — SUPPORTER + SPLITTER cascade
- T4_E19_M — fortress SUPPORTER + SIEGER

3 deterministic trace brackets × 5 classes were run.

Total current-Lv6 critical runs:
`10 × 3 × 5 = 150`.

---

# 1. CENTRAL bracket clear-time diagnostic

Milliseconds; this is **not a balance target**.

| Recipe | Knight | Rogue | Tank | Archer | Mage |
|---|---:|---:|---:|---:|---:|
| T1_E03_M | 8250 | 5305 | 9000 | 5250 | 5250 |
| T2_E14_H | 5250 | 3805 | 5250 | 5250 | 3000 |
| T3_E07_M | 6750 | 3805 | 6750 | 5250 | 3750 |
| T3_E13_H | 5250 | 3805 | 5250 | 3750 | 3000 |
| T3_E15_M | 6750 | 5305 | 8250 | 5250 | 4500 |
| T3_E17_M | 8250 | 5360 | 9000 | 5250 | 4500 |
| T4_E11_M | 10500 | 5305 | 10500 | 6000 | 5250 |
| T4_E12_M | 10500 | 5360 | 12000 | 7500 | 6750 |
| T4_E16_M | 11250 | 6805 | 9750 | 6750 | 5250 |
| T4_E19_M | 8250 | 5305 | 8250 | 6750 | 6000 |

Mean over this critical subset:

| Class | Mean clear time |
|---|---:|
| Mage | 4725 ms |
| Rogue | 5016 ms |
| Archer | 5700 ms |
| Knight | 8100 ms |
| Tank | 8400 ms |

Interpretation:
- clear-time class spread is large already
- do not call this unfairness yet because trace is unfitted and Tank is utility/control oriented
- however any final class-opportunity gate must not use clear time alone

---

# 2. Lv6 effect diagnostic

CENTRAL bracket, comparing same current-authority model with Lv6 OFF vs ON across the 10-recipe subset.

Average clear-time change:

| Class | Mean effect from Lv6 ON |
|---|---:|
| Mage | ~42.9% faster |
| Rogue | ~39.3% faster |
| Archer | ~29.6% faster |
| Knight | ~4.7% faster |
| Tank | ~1.4% slower |

This is not a skill-balance verdict.

Why Tank can be slower:
- extra knockback pushes the target farther from the wall/player side
- control can increase time-to-kill while improving survival/objective control

Therefore Tank requires metrics such as:
- wall-danger time
- CHARGER interrupt opportunity
- minimum enemy X
- prevented wall hits
rather than DPS-only comparison.

The magnitude difference still creates a mandatory WATCH for later Tier/class calibration.

---

# 3. CHARGER result — default geometry FAILS to express capability

Recipes:
- T3_E07_M
- T3_E13_H
- T3_E17_M

Across:
- 3 trace brackets
- 5 classes

Total CHARGER parents observed in the runs:
- 60 erased-before-windup events

Total windups:
```text
0
```

This is a **recipe/entry-geometry FAIL for capability expression under the current bracket**, not a production CHARGER balance verdict.

Consequences:
- Tank interrupt role cannot appear
- telegraph readability cannot be measured
- CHARGER becomes only a normal HP/speed body

Do not patch CHARGER HP globally yet.

First adjustment axis:
- absolute entry depth
- trigger arrival timing
- screen/exposure timing

---

# 4. SIEGER result — default geometry also fails to express objective pressure

Recipes:
- T4_E11_M
- T4_E19_M

Across all 3 trace brackets × 5 classes:

```text
SIEGER total shots = 0
```

This confirms the earlier generic-DPS sensitivity warning with a class-aware mechanics model.

The issue is not only SIEGER HP.
At the current default spawn depth, approach-to-standoff time is long relative to class-aware encounter clear time.

If SIEGER never fires:
- Tank wall-protection value disappears
- Archer screened-backline identity is reduced to raw penetration
- T4 SIEGE identity is not actually experienced

First response must be geometry/timing experiments before numeric durability inflation.

---

# 5. SUPPORTER result — capability exists but is highly class-sensitive

Screened-aura range across all current brackets/classes:

| Recipe | Minimum | Maximum |
|---|---:|---:|
| T4_E12_M | 0.155 s | 11.855 s |
| T4_E16_M | 0.005 s | 4.720 s |
| T4_E19_M | 1.205 s | 5.405 s |

This is useful because SUPPORTER does not disappear universally.
Instead its value varies strongly with:
- class removal speed
- splash/line secondary damage
- front-body lifetime

Required later metric:
`screenedAuraUptime / supporterAliveTime` as well as raw seconds.

---

# 6. SPLITTER result

In T3_E15_M and T4_E16_M:
- parent deaths correctly create children
- across the current bracket set, child wall hits = 0

This means the current representative recipes express population transformation but not meaningful wall leak under these optimistic traces.

Not automatic FAIL.
Layer-A next pass should inspect:
- peak active after split
- child frontline occupancy
- class-specific secondary-hit efficiency
- lower-throughput/fitted traces later

---

# 7. Class-role reading

## Mage
Current Lv6 splash realizes strongly in density/mixed recipes.
It can erase special bodies before capability activation.

## Rogue
Second dagger produces strong single/frontline throughput.
Durable-body role is clearly expressed, but it can also suppress later mechanics too quickly.

## Archer
Line opportunity is recipe-geometry dependent.
Some encounters show large benefit; others show little/no Lv6 gain.
This is desirable only if Tier-wide opportunity coverage remains adequate.

## Knight
Lv6 is mostly broad +12% damage.
Large role differentiation is expected later from penetration skills, so current-Lv6-only results must not be treated as final Knight identity.

## Tank
Current Lv6 utility is not represented adequately because CHARGER windup and wall pressure rarely/never occur in default critical recipes.
This is an **encounter opportunity starvation problem**, not evidence that Tank itself is weak.

---

# 8. Structural conclusion

The class-aware simulator is doing useful work because it found a defect that generic DPS could not localize:

> Current representative recipes begin too far from the wall/trigger/standoff for some stateful capabilities relative to actual class-aware removal speed.

Therefore the next authoring dimension must include **absolute encounter entry depth**, not only relative FRONT/MID/BACK depth.

---

# 9. Status

## Simulator
PASS for bounded mechanics analysis.

## Production SKILLED_V2
NOT CALIBRATED.

## Current representative recipes
- ordinary durability/density: usable as probes
- SUPPORTER: usable with WATCH
- CHARGER: FAIL capability-expression at default entry depth
- SIEGER: FAIL capability-expression at default entry depth

## Next
1. add absolute entry-depth authoring field
2. sweep CHARGER trigger activation depth
3. sweep SIEGER first-shot depth
4. preserve relative screening order
5. test Tank interrupt opportunity after CHARGER activation exists
6. test SIEGER shot visibility across all five classes
7. only after that continue to fitted SKILLED_V2 traces / synthetic slices
