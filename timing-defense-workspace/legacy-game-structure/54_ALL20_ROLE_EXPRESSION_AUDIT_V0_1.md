# Timing Defense — All-20 Role Expression Audit V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL PASS WITH WATCHES / ALL REPRESENTATIVE RECIPES / NOT SKILLED_V2 / NOT PRODUCTION FREEZE**

Depends on:
- `53_CRITICAL_ROLE_EXPRESSION_V0_2_RERUN_REPORT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`
- `data/model_a_critical_role_expression_candidates_v0_1.yaml` — content V0.2
- `data/model_a_additional10_role_expression_candidates_v0_1.yaml`

Reproducibility tools:
- `tools/materialize_critical_role_candidates.py` — generalized to critical/additional role overlays
- `tools/evaluate_role_expression_v0_2.py` — generalized to `criticalRecipes` or `roleRecipes`

---

# 0. Admission question

Can the complete 20-recipe Model-A representative library satisfy the Monster Role Expression Contract across:

- 3 deterministic calibration brackets
- all 5 classes
- `CURRENT_AUTHORITY_LV6`

without global HP inflation or live gameplay changes?

## Result

**YES — ALL-20 STRUCTURAL ROLE-EXPRESSION PASS WITH WATCHES.**

This is a lower-layer authoring admission only.
It does not calibrate production difficulty or exact readable-time thresholds.

---

# 1. Audit population

Representative recipes:
`20`.

Combat rows:

```text
20 recipes × 3 trace brackets × 5 classes = 300 rows
```

Designated recipe-role pairs:
- critical 10 set: 23
- additional 10 set: 13
- total: 36

Structural role-gate checks:

```text
36 designated recipe-role pairs × 15 class/profile rows = 540 checks
```

Result:

```text
540 / 540 structural role gates PASS
0 designated failure rows
```

T1_E01 is the neutral GRUNT baseline and has no special role gate.

---

# 2. Initial additional-10 failures before refinement

The first default-geometry additional-10 audit localized failures to only three recipes:

## T3_E20_L
- CHARGER: 0/15 role-expression pass
- SPLITTER: 14/15; STRONG Mage could erase both children in the same authoritative combat tick as the parent death

## T4_E10_M
- SIEGER: 0/15 first-shot-opportunity expression

## T4_E18_M
- SIEGER: 0/15
- FLYER: 13/15 geometry expression

All other additional recipes passed their designated structural roles at default representative geometry.

This confirmed that the problem remained localized rather than requiring campaign or monster-system redesign.

---

# 3. T3_E20_L — COLLAPSE_CHAIN

Problem:
- moving the whole formation forward to activate CHARGER interfered with the SPLITTER state
- STRONG Mage could erase SPLITTER children within the same authoritative tick

Resolution uses the archetype's existing `LATE_INSERT` semantics instead of a whole-formation shift.

Diagnostic candidate:
```text
common formation entry remains unchanged
SPLITTER spawn -> 1400ms
CHARGER spawn -> 2350ms
CHARGER relative X offset -> -0.46
```

Interpretation:
- SPLITTER is delayed enough that STRONG Mage no longer collapses the split consequence in the same tick
- CHARGER alone enters deeper in the field as a late insert near its trigger grammar
- no global CHARGER HP/speed/trigger change is required

Current minimum evidence across all 15 rows:
- SPLITTER child alive time >= ~1690ms
- child frontline time >= ~900ms
- split-driven target reorder >=1
- peak-active delta >=1
- CHARGER windup entries >=1
- CHARGER accumulated visible windup >=~250ms
- sampled wall damage = 0

Status:
`STRUCTURAL PASS / CHARGER READABILITY WATCH`.

The ~250ms lower tail is not promoted to a production-readable threshold.
It remains a WATCH for fitted player/accessibility calibration.

---

# 4. T4_E09_M — SUPPORT_COLUMN quality refinement

E09 passed the nonzero structural gate by default, but its shortest aura case was only about 105ms with a very low screened-aura ratio.

That was judged too fragile for the spirit of the role-expression contract even though it was technically nonzero.

Localized candidate:
```text
SUPPORTER total relative X depth = 0.00
SUPPORTER spawn = 800ms
```

Result across all 15 rows:
- minimum aura ~=1005ms
- minimum screened-aura ratio ~=0.735
- minimum unique aura targets = 4
- sampled wall damage = 0

Status:
`STRONG STRUCTURAL CANDIDATE`.

---

# 5. T4_E10_M — SIEGE_LINE

Default geometry produced no SIEGER opportunity.

Because E10 is the focused/unscreened SIEGER case, its solution should not depend on a deep escort screen.

Diagnostic candidate:
```text
entry shift toward wall ~= 0.70
SIEGER total relative depth = 0.00
SIEGER spawn = 900ms
```

The SIEGER enters directly into a readable standoff problem.

Result across all 15 rows:
- minimum SIEGER opportunity entries = 2
- minimum accumulated visible windup ~=1275ms
- actual completed shots range 0..2

CONSERVATIVE sample timeline:
- first SIEGER opportunity around 900ms
- first actual shot around 1700ms
- earliest ordinary GRUNT contact examples occur around ~3890–3965ms

Thus ordinary contact pressure occurs far after the player has already received the SIEGER response state.

Status:
`STRUCTURAL PASS`.

---

# 6. T4_E18_M — DUAL_AXIS

Default geometry failed SIEGER role expression and two FLYER geometry rows.

Localized candidate:
```text
entry shift toward wall ~= 0.685
SIEGER total relative depth = 0.00
SIEGER spawn = 2300ms
```

Result across all 15 rows:
- FLYER geometry opportunity >=~300ms
- SHIELD mitigated hits >=2
- SHIELD prevented raw damage >=~215
- SIEGER opportunity entries >=2
- SIEGER accumulated visible windup >=~1230ms
- actual completed SIEGER shots range 0..3

Sample CONSERVATIVE timeline:
- SIEGER opportunity begins around ~2525ms
- first shot around ~3325ms for several classes
- earliest ordinary GRUNT contact around ~4155–4250ms

Again, ordinary contact happens after the SIEGER response state is already visible.

Status:
`STRUCTURAL PASS / FLYER QUANTITATIVE READABILITY WATCH`.

---

# 7. Additional default-pass roles

No geometry rewrite was required for the following additional recipes:

## T1_E02_M — RUNNER
Minimum sampled X advance:
`~0.097` normalized X.

## T2_E04_M — SHIELD
Minimum:
- mitigated hits >=4
- prevented raw damage >=~230

## T2_E05_M — MIXED_WALL
BRUTE minimum:
- hits >=4
- frontline >=~1205ms
- absorbed damage >=900

SHIELD minimum:
- hits >=2
- prevented raw damage >=~230

## T2_E06_M — FLYER
Minimum geometry opportunity:
`~325ms`.

## T3_E08_M — SPLITTER
Minimum:
- child alive >=~1200ms
- child frontline >=~600ms
- target reorders >=2
- peak-active delta >=1

These remain bounded structural metrics, not production thresholds.

---

# 8. Full 20-recipe verdict

Combining:
- the refined critical 10 candidates from Report 53
- the additional 10 audit/refinements in this report

produces:

```text
ALL20_ROLE_EXPRESSION = PASS_WITH_WATCHES
```

Meaning:
- no designated representative monster role is now routinely erased before any structural expression opportunity under the current three deterministic brackets
- all five classes receive the designated structural opportunity
- full enemy ability success remains class-/trace-dependent
- class asymmetry is preserved
- no global monster-stat inflation was required

---

# 9. Remaining WATCHES before fitted player modeling

## W1 — exact readable-time threshold
Current lower tails include roughly:
- E20 CHARGER ~250ms
- T2/T4 FLYER geometry ~255–325ms
- critical CHARGER candidates ~430–445ms
- SIEGER candidates generally >=~470ms and often much larger

Do not freeze a universal minimum from unfitted deterministic traces.

## W2 — RUNNER minimum meaningful advance
All designated RUNNER rows move before deletion, but some lower tails remain modest.
Production meaningful-distance thresholds require fitted player traces.

## W3 — conservative wall pressure after role expression
Some siege candidates allow ordinary bodies to contact the wall under CONSERVATIVE traces.
Current sampled timelines show those contacts after SIEGER response states begin, so they are not pre-response structural failures.
They remain difficulty/balance WATCHES.

## W4 — FLYER opportunity semantics
The current V0.2 geometry metric is a bounded solo-slot line/splash proxy.
Final geometry coverage should include later class skills and fitted action traces.

## W5 — current trace brackets are not population models
Nothing in this report satisfies the non-T1 `<60%` full-Tier gate yet.

---

# 10. Admission consequence

The representative encounter library no longer has a role-expression blocker before player-model calibration.

Previous sequence:
```text
critical role audit -> all-20 role audit -> fitted player model
```

Updated state:
```text
critical role audit PASS_WITH_WATCHES
 -> all-20 role audit PASS_WITH_WATCHES
 -> FITTED SKILLED_V2 HARNESS / PLAYER MODEL NEXT
```

The next work is no longer more encounter-geometry search unless fitted player evidence reopens a WATCH.

---

# 11. Explicit non-goals

Do NOT use this audit to:
- freeze the candidate X offsets/timings
- freeze monster HP/speed/armor
- guarantee every special attack succeeds
- equalize all five class outcomes
- author the exact 200-Stage launch campaign
- claim production difficulty is calibrated
- change live gameplay code

No live gameplay source or production balance coefficient was changed by the all-20 audit.
