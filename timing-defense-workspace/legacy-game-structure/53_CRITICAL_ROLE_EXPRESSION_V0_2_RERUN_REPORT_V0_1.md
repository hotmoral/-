# Timing Defense — Critical Role Expression V0.2 Rerun Report V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL PASS WITH WATCHES / NOT SKILLED_V2 / NOT PRODUCTION FREEZE**

Depends on:
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `50_CROSS_BRACKET_ROLE_EXPRESSION_ROBUSTNESS_V0_1.md`
- `52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`
- `data/model_a_critical_role_expression_candidates_v0_1.yaml` — content V0.2

Candidate materialization tool:
- `tools/materialize_critical_role_candidates.py`

Evaluation tool:
- `tools/evaluate_role_expression_v0_2.py`

---

# 0. Admission question

After localized geometry/cadence refinements, can the 10-recipe critical representative set satisfy the Monster Role Expression Contract across:

- 3 deterministic calibration brackets
- all 5 classes
- `CURRENT_AUTHORITY_LV6`

without globally inflating monster HP or changing live gameplay?

## Result

**YES — STRUCTURAL ROLE-EXPRESSION PASS WITH WATCHES.**

This does NOT mean:
- production difficulty is calibrated
- exact readable milliseconds are frozen
- candidate coordinates/timings are production data
- SKILLED_V2 is fitted

---

# 1. Reproducibility cross-check

Before using the extended role telemetry, an independent deterministic semantic mirror of the existing class-aware V0.1 model was cross-checked against the canonical V0.1 CENTRAL report.

Reference set:
- 10 critical recipes
- 5 classes
- 50 CENTRAL clear-time cells

Result:

```text
50 / 50 clear-time cells reproduced exactly
```

Example anchors reproduced exactly include:
- T1_E03 Knight = 8250ms
- T1_E03 Rogue = 5305ms
- T4_E11 default Knight = 10500ms
- T4_E12 default Tank = 12000ms
- T4_E19 default Mage = 6000ms

The role-expression candidate rerun then used the same mechanics semantics plus the V0.2 telemetry fields.

---

# 2. Rerun matrix

Critical recipes:
1. T1_E03_M
2. T2_E14_H
3. T3_E07_M
4. T3_E13_H
5. T3_E15_M
6. T3_E17_M
7. T4_E11_M
8. T4_E12_M
9. T4_E16_M
10. T4_E19_M

Profiles:
- TRACE_BRACKET_CONSERVATIVE
- TRACE_BRACKET_CENTRAL
- TRACE_BRACKET_STRONG

Classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

Total combat rows:

```text
10 × 3 × 5 = 150
```

Role admission is applied only to each recipe's `designatedRoleMonsters`, not mechanically to every incidental body in the composition.

---

# 3. Final localized candidate refinements

All values remain diagnostic candidates.

## T3_E07_M — CHARGER
Refined from the earlier depth-only candidate.

Candidate:
```text
entry shift toward wall ~= 0.44
CHARGER relative X offset = 0.00
CHARGER spawn = 1550ms
```

Reason:
- earlier insertion gives the role a readable state while ordinary GRUNTs still shape the encounter
- removes the need for artificial +0.10 CHARGER back depth

Three-bracket/five-class result:
- minimum CHARGER visible-windup accumulation: ~435ms
- minimum windup entries: 1
- sampled wall damage: 0

Status:
`STRUCTURAL PASS / READABILITY THRESHOLD STILL OPEN`.

## T3_E13_H — CHARGER + RUSH
Candidate:
```text
entry shift toward wall ~= 0.425
CHARGER #1 spawn 760ms
CHARGER #2 spawn 1960ms
relative CHARGER offset = 0.00
```

This is the original CHARGER timing plus +400ms for both CHARGERs.

Result:
- minimum visible-windup accumulation across all 15 class/profile rows: ~430ms
- minimum windup entries: 2
- sampled wall damage: 0

Status:
`STRUCTURAL PASS / READABILITY THRESHOLD STILL OPEN`.

## T3_E17_M — screened CHARGER
Candidate remains near:
```text
entry shift ~= 0.49
CHARGER total relative depth ~= +0.10
```

Result:
- minimum visible windup ~445ms
- minimum windup entries 1
- sampled wall damage 0

Status:
`STRUCTURAL PASS`.

## T4_E11_M — escort siege
Candidate:
```text
entry shift ~= 0.70
SHIELD 0ms
BRUTE 250ms
GRUNT 750ms
GRUNT 1000ms
SIEGER 1250ms
SIEGER total relative depth ~= +0.10
```

Relative to the original representative candidate:
- two ordinary GRUNTs are +250ms later
- SIEGER is -300ms earlier

Result across all 15 rows:
- minimum SIEGER opportunity entries = 1
- minimum accumulated visible windup ~=470ms
- actual completed shot count ranges 0..2

`0 shots` under faster traces is NOT structural failure because the standoff/windup problem was already presented to the player.

CONSERVATIVE ordinary contact pressure remains a WATCH, but timeline inspection shows it is not pre-response damage:
- first SIEGER opportunity begins around 3365ms in the sampled CONSERVATIVE runs
- earliest ordinary contact example occurs around 4215ms
- therefore the earliest sampled ordinary contact occurs ~850ms after the response state begins

Status:
`STRUCTURAL PASS / WALL-PRESSURE WATCH`.

## T4_E12_M — buffed bulwark SUPPORTER
Candidate:
```text
SUPPORTER total relative depth ~= +0.02
SUPPORTER spawn = 1050ms
```

Result:
- minimum aura expression ~=755ms
- minimum screened-aura ratio ~=0.827
- minimum unique aura targets = 5
- sampled wall damage = 0

This is a major improvement over the earlier near-instant support expression cases.

Status:
`STRUCTURAL PASS`.

## T4_E16_M — cascade SUPPORTER
Candidate:
```text
SUPPORTER total relative depth = 0.00
SUPPORTER spawn = 2800ms
```

This is only:
- -200ms timing
- -0.02 relative X-depth
from the prior representative candidate.

Result:
- minimum aura expression ~=955ms
- minimum screened-aura ratio ~=0.389
- sampled wall damage = 0

Status:
`STRUCTURAL PASS / NORMALIZED-AURA WATCH`.

## T4_E19_M — fortress
Candidate remains near:
```text
entry shift ~= 0.70
SIEGER total relative depth ~= +0.10
```

Result:
- SIEGER minimum opportunity entries = 2
- minimum accumulated SIEGER windup ~=535ms
- actual shots range 0..2
- SUPPORTER minimum aura ~=2705ms
- SUPPORTER minimum screened-aura ratio ~=0.734
- minimum aura targets = 4

CONSERVATIVE ordinary contacts occur only after the SIEGER response state begins in the sampled timeline:
- SIEGER opportunity begins around 3590ms
- earliest sampled ordinary contact around 4125ms
- delta ~=535ms

Status:
`STRUCTURAL PASS / WALL-PRESSURE WATCH`.

---

# 4. All designated-role gate result

Using nonzero structural gates only, before any fitted SKILLED_V2 minimum-threshold freeze:

```text
ALL DESIGNATED ROLE GATES = 15 / 15 per role
NO designated role failure rows
```

Representative minimum evidence across the current 15-row per-recipe sweep:

| Recipe / role | Minimum current structural evidence |
|---|---|
| T1_E03 BRUTE | 7 hits; 3005ms frontline; 1800 absorbed across two BRUTEs |
| T2_E14 RUNNER | ~0.164 normalized X advance |
| T2_E14 FLYER | ~255ms line/splash geometry opportunity |
| T3_E07 CHARGER | ~435ms visible windup |
| T3_E13 CHARGER | ~430ms visible windup; >=2 entries |
| T3_E15 SPLITTER | child alive >=1200ms; frontline >=600ms; reorder >=1 |
| T3_E17 SHIELD | >=4 mitigated hits; >=228 prevented raw-damage units |
| T3_E17 BRUTE | >=5 hits; >=870ms frontline |
| T3_E17 CHARGER | >=445ms visible windup |
| T4_E11 SIEGER | >=1 opportunity; >=470ms visible windup |
| T4_E12 SUPPORTER | >=755ms aura; screened ratio >=~0.827 |
| T4_E16 SPLITTER | child alive >=2400ms; frontline >=1170ms; reorder >=3 |
| T4_E16 SUPPORTER | >=955ms aura; screened ratio >=~0.389 |
| T4_E19 SUPPORTER | >=2705ms aura; screened ratio >=~0.734 |
| T4_E19 SIEGER | >=2 opportunities; >=535ms visible windup |

---

# 5. BRUTE evaluator correction

The first V0.2 evaluator required:

```text
frontlineMs > 0 AND hitsReceived > 0
```

This was too strict.

Example:
- T4_E12 CONSERVATIVE Archer
- BRUTE never becomes authoritative frontmost because SHIELD remains ahead
- yet BRUTE receives 7 hits and absorbs its full 900 HP

That is real durable screening expression.

Evaluator V0.2 was corrected to accept:

```text
hitsReceived > 0
AND
(frontlineMs > 0 OR absorbedDamage > 0)
```

This preserves actual frontmost authority while recognizing secondary/screen durability.

---

# 6. Remaining WATCHES

Structural PASS does not close quantitative readability.

## W1 — FLYER short-tail geometry
Minimum current geometry opportunity in T2_E14 is ~255ms.

A positive value proves the role exists, but production minimum readable geometry time remains OPEN.

## W2 — RUNNER short-tail advance
RUNNER structurally advances before deletion in all designated rows.
The smallest current T3_E13 advance is modest (~0.075 normalized X).

Do not freeze a production minimum until fitted player traces exist.

## W3 — E11/E19 conservative wall pressure
Some CONSERVATIVE rows allow ordinary bodies to hit the wall after the SIEGER response state begins.

This is not `PRE_RESPONSE_UNAVOIDABLE_DAMAGE` in the sampled timeline, but final difficulty/pressure calibration is still open.

## W4 — exact readable milliseconds
Current candidate minima around 430–535ms for CHARGER/SIEGER are useful evidence, not a frozen accessibility/readability threshold.

## W5 — current player traces are still optimistic deterministic brackets
No full-Tier difficulty claim follows from this pass.

---

# 7. Admission verdict

Previous:
```text
ROLE_EXPRESSION_ADMISSION = BLOCKED
```

Updated critical-set verdict:

```text
CRITICAL_SET_ROLE_EXPRESSION = PASS_WITH_WATCHES
```

Meaning:
- no critical designated monster is now structurally spawn-deleted before any role opportunity in the current bounded candidates
- all five classes receive structural opportunity across all three current deterministic brackets
- class outcomes remain asymmetric
- full ability success is not forced

This is exactly the intended contract.

---

# 8. Next boundary

The critical set no longer blocks progression to the next bounded layer.

Next:
1. materialize the same candidate overlay reproducibly
2. run the V0.2 role audit across **all 20 representative recipes**
3. define designated-role mappings for the additional 10 recipes
4. reject any new pre-expression deletion
5. preserve PASS_WITH_WATCHES rather than forcing equal outcomes
6. only after all-20 role audit return to fitted `SKILLED_V2` harness work

Do NOT yet:
- freeze these geometry values
- change production monster HP/speed/armor
- author the exact 200-Stage campaign
- claim the <60% skilled full-Tier gate is calibrated
- change live gameplay code

No live gameplay source or production balance coefficient was changed by this rerun.
