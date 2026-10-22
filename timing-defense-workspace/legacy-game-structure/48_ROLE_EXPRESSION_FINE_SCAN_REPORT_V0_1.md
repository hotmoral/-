# Timing Defense — Role Expression Fine Scan Report V0.1

Date: 2026-10-22 KST  
Status: **BOUNDED CLASS-AWARE DIAGNOSTIC / NOT PRODUCTION COORDINATE FREEZE**

Depends on:
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `46_ROLE_EXPRESSION_ADMISSION_AUDIT_V0_1.md`
- `44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`
- `data/role_expression_activation_search_v0_1.yaml`
- `tools/scan_activation_window_candidates.py`

Probe mode:
- `CURRENT_AUTHORITY_LV6`
- `TRACE_BRACKET_CENTRAL`
- five classes
- 0.01 X diagnostic steps

Important:
- trace bracket is not fitted `SKILLED_V2`
- all coordinates below are search-space evidence only
- no HP/speed/trigger/standoff coefficient is frozen or changed

---

# 0. Question

Can the current CHARGER/SIEGER representative recipes satisfy the new role-expression contract through encounter geometry before changing monster durability?

Answer:

**Mostly yes, but E11 still has a wall-leak WATCH and none of these ranges is production-ready.**

---

# 1. CHARGER — E07 exposed/baseline case

The initial fine-search range `0.20..0.40` was too narrow.

Within that old range:
- all-five role expression did not appear
- around `0.35`, only Knight/Tank began to see windup in the current deterministic probe

The search was therefore extended.

Extended result:
- all-five windup visibility begins around `shiftTowardWall ~= 0.53`
- a contiguous zero-contact-wall-leak band is observable approximately `0.53..0.64`
- at the lower edge, the five classes can all observe at least one windup without requiring a global HP increase

Interpretation:
- E07 is **not structurally impossible**
- the earlier apparent failure was partly a search-envelope failure
- do not delete/rewrite E07 yet
- its first candidate band should be tested around the lower portion of this activation range to preserve reaction time

Current status:
`CANDIDATE_ROLE_EXPRESSION_WINDOW_FOUND / NOT ADMITTED`

---

# 2. CHARGER — E17 screened case

Fine scan result:
- 3/5 classes around `0.35`
- 4/5 around `0.39`
- 5/5 begins around `0.43`
- all-five visibility continues through the current scan stop `0.55`

A comparatively clean zero-contact-wall-leak interval appears approximately:
`0.43..0.50`.

Current-class examples near the lower edge include different valid outcomes:
- windup -> charge completion
- windup -> interrupt
- windup -> deletion before charge completion

That diversity is desirable because the role contract requires a readable opportunity, not guaranteed charge success.

Current status:
`STRONG_CANDIDATE_WINDOW / NOT PRODUCTION FREEZE`

---

# 3. SIEGER — E11 escort siege

Fine scan result:
- 2/5 actual-shot visibility around `0.65`
- 3/5 around `0.67`
- 5/5 begins around `0.70`
- all-five actual-shot visibility remains through approximately `0.82`
- falls to 4/5 around `0.83`
- collapses sharply by `0.84`

Thus the current deterministic all-five actual-shot window is roughly:
`0.70..0.82`.

However total wall damage must be decomposed.
A SIEGER shot is intended objective pressure; ordinary contact wall hits are not equivalent.

At the lowest all-five sample around `0.70`:
- most classes show only intended siege-shot wall pressure
- Archer additionally allows approximately one GRUNT-equivalent contact leak in this probe

Therefore E11 is **not yet role-expression admitted**.
The next adjustment should target:
- ordinary-unit spawn timing
- relative screen spacing
- entry depth
without deleting the first-shot opportunity.

Do not fix this by simply adding HP to SIEGER.

Current status:
`ACTIVATION_WINDOW_FOUND / CONTACT_WALL_LEAK_WATCH`

---

# 4. SIEGER — E19 fortress

Fine scan result:
- 4/5 actual-shot visibility around `0.68`
- 5/5 begins around `0.70`
- all-five visibility persists through approximately `0.83`
- collapses to 0/5 by `0.84`

Current deterministic all-five window:
`0.70..0.83`.

At approximately `0.70`:
- all five classes observe SIEGER actual-shot expression
- current decomposition shows no ordinary contact wall leak in the five-class probe
- wall damage is attributable to intended SIEGER shots

This makes `~0.70` a useful **diagnostic anchor**, not a production coordinate.

Current status:
`STRONG_CANDIDATE_WINDOW / NOT PRODUCTION FREEZE`

---

# 5. Important non-monotonic confirmation

All four searches reinforce the same rule:

```text
too far
 -> role erased before activation

bounded activation window
 -> role visible + counterplay exists

too far forward
 -> wall/contact pressure or special exposure rises
 -> activation may collapse again
```

Therefore entry depth is an encounter grammar axis, not a scalar difficulty knob.

---

# 6. Wall-pressure metric correction

Previous scanner used total wall damage as one number.
That is insufficient for SIEGER because:

```text
siege-shot wall damage = intended role expression
contact wall damage = possible encounter-authoring leak
```

`scan_activation_window_candidates.py` V0.2 now reports both:
- `specialAbilityWallDamage`
- `contactWallDamage`

Admission should prioritize low/zero **contact wall damage** while still preserving readable special-role opportunity.

---

# 7. Bounded candidate bands for the next pass

These are deliberately narrower than the full observed activation ranges.
They exist only to reduce the next search cost.

```text
E07 CHARGER: 0.53..0.60 focus band
E17 CHARGER: 0.43..0.50 focus band
E11 SIEGER:  0.69..0.73 focus band + spawn/spacing adjustment
E19 SIEGER:  0.69..0.72 focus band
```

Rationale:
- prefer the earliest/lower-pressure portion of the activation range
- retain more player reaction time
- avoid using the most aggressive forward-entry samples

These are NOT production coordinates.

---

# 8. Admission impact

This report removes one earlier uncertainty:

> CHARGER/SIEGER capability expression can be restored without first globally inflating HP.

But critical-set admission remains blocked because:
1. E11 ordinary contact wall leak still needs adjustment
2. SIEGER `first-shot opportunity` vs actual-shot success needs explicit instrumentation
3. RUNNER/BRUTE/SHIELD/FLYER direct role metrics remain incomplete
4. SPLITTER child meaningful-state duration needs direct measurement
5. SUPPORTER normalized aura ratio still needs explicit reporting

---

# 9. Next exact work

1. search E11 spawn-time/spacing variants inside the lower activation band
2. add `firstShotOpportunity` instrumentation separate from `shotCount`
3. add passive-role metrics for RUNNER/BRUTE/SHIELD/FLYER
4. add SPLITTER child lifetime/frontline/reorder metrics
5. add SUPPORTER alive-time + normalized aura ratios
6. rerun the 10 critical recipes under the role-expression contract
7. require critical-set PASS before expanding to all 20 recipes

No live gameplay code or production balance coefficient is changed by this report.
