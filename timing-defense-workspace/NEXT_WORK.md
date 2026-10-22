# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# ACTIVE PHASE — Monster Role-Expression / Activation-Window Calibration

Completed chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> Tier encounter envelope PASS
 -> static recipe preflight PASS
 -> kinematic preflight PASS WITH WATCHES
 -> generic DPS sensitivity COMPLETE
 -> Layer-A admission PASS
 -> class-aware CURRENT_AUTHORITY micro-sim V0.1 COMPLETE
 -> absolute entry-depth activation diagnostic COMPLETE
 -> Monster Role Expression Contract V0.1 ESTABLISHED
 -> critical-set role-expression audit COMPLETE / ADMISSION BLOCKED
```

Read first:
1. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
2. `legacy-game-structure/46_ROLE_EXPRESSION_ADMISSION_AUDIT_V0_1.md`
3. `legacy-game-structure/47_ROLE_EXPRESSION_SCHEMA_AMENDMENT_V0_1.md`
4. `legacy-game-structure/44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`
5. `legacy-game-structure/42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
6. `legacy-game-structure/43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
7. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
8. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`

Machine-readable:
- `legacy-game-structure/data/monster_role_expression_contract_v0_1.yaml`
- `legacy-game-structure/data/role_expression_activation_search_v0_1.yaml`
- `legacy-game-structure/data/model_a_class_action_trace_bracket_v0_1.yaml`
- `legacy-game-structure/data/model_a_representative_recipes_v0_1.yaml`
- `legacy-game-structure/data/model_a_kinematic_anchor_v0_1.yaml`
- `legacy-game-structure/data/model_a_combat_sensitivity_anchor_v0_1.yaml`

Tools:
- `tools/validate_monster_role_expression_contract.py`
- `tools/evaluate_stateful_role_expression.py`
- `tools/scan_activation_window_candidates.py`
- `tools/simulate_class_aware_layer_a.py`
- `tools/sweep_special_activation_entry_depth.py`

---

# User-confirmed structural truth

Existing truth remains:
- 5 classes, independent Tier progression
- same Tier/Stage combat content across classes
- Tier = 50 Stage
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★
- stars = broad account growth; achievements = targeted cross-class growth
- recoverable soft walls allowed; hard class lockout forbidden
- current 9 monsters are V1 foundation, not lifetime final roster
- T1 does not expose all 9; higher Tiers introduce new monsters
- T5+ monster/Tier expansion remains open
- fitted non-T1 `SKILLED_V2_CENTRAL` full-clear should normally remain <60%
- combo40 is skilled-achievable
- Lv31 target unlock window = Stage41–45
- Stage46–49 = post-Lv31 mastery; Stage50 = final application

Newly explicit user-confirmed monster rule:

> intended encounters must not let a monster spawn and disappear before its role is meaningfully perceivable.

This means:
- minimum role-expression opportunity is required
- successful full activation is not always required
- skilled counterplay after readable expression is valid
- `PRE_EXPRESSION_DEATH_WITHOUT_READABLE_COUNTERPLAY` is invalid authoring

---

# Role-expression contract — current nine

- GRUNT: baseline exempt
- RUNNER: speed must change arrival/front-order behavior
- BRUTE: must meaningfully hold/absorb frontline attention
- SHIELD: mitigation must change effective damage/hit investment
- FLYER: vertical geometry must create actual opportunity difference
- CHARGER: visible windup + response window required
- SPLITTER: split must create meaningful post-death population/target-state change
- SUPPORTER: aura must reach at least one non-self target for a meaningful interval
- SIEGER: standoff + readable first-shot opportunity required

Future monsters must declare the same contract fields before admission.

---

# Current admission status

```text
ROLE_EXPRESSION_ADMISSION = BLOCKED
```

Current status:
- GRUNT = BASELINE_EXEMPT
- RUNNER = MEASUREMENT_REQUIRED
- BRUTE = PRELIMINARY_ROLE_PRESENT / METRIC_REQUIRED
- SHIELD = MEASUREMENT_REQUIRED
- FLYER = MEASUREMENT_REQUIRED
- CHARGER = FAIL_DEFAULT_GEOMETRY
- SPLITTER = PARTIAL_PASS / WATCH
- SUPPORTER = PASS_WITH_WATCH
- SIEGER = FAIL_DEFAULT_GEOMETRY

This is localized encounter/simulation work. No broad campaign redesign is required.

---

# Known activation search anchors — diagnostic only

CHARGER:
- E07: first useful windup evidence begins around ~0.25; interrupt evidence around ~0.30
- E17: all-five windup visibility around ~0.45

SIEGER:
- E11: all-five actual-shot visibility around ~0.70–0.80; collapse near ~0.85
- E19: all-five actual-shot visibility around ~0.75–0.80; collapse near ~0.85

These are **search anchors, not production coordinates**.

Fine-search data now bounds:
- E07 0.20–0.40
- E17 0.35–0.55
- E11 0.65–0.84
- E19 0.68–0.84
- step 0.01

---

# EXACT NEXT BOUNDARY

Next bounded tranche = **critical-set role-expression calibration**.

Order:
1. fine-scan E07/E17 CHARGER activation windows
2. find a window with visible windup + real interrupt opportunity across all five classes
3. reject windows that make wall pressure unavoidable before response
4. fine-scan E11/E19 SIEGER windows
5. prefer contiguous all-five activation regions with lower wall pressure, not a single coordinate
6. add SIEGER standoff/windup/first-shot-opportunity instrumentation so zero-shot can be separated from skilled counterplay
7. add SPLITTER child lifetime/frontline/population-delta metrics
8. add SUPPORTER normalized aura ratio metrics
9. add RUNNER/BRUTE/SHIELD/FLYER passive-role metrics
10. rerun the 10-recipe critical subset under CURRENT_AUTHORITY
11. require critical-set role-expression PASS/WATCH acceptable state
12. then expand to all 20 representative recipes
13. only after all-20 role audit return to fitted SKILLED_V2 harness and synthetic Tier slices

Do NOT yet:
- author exact 200 launch stages
- freeze production HP/speed/armor/entry coordinates/trigger/standoff values
- promote current deterministic trace brackets to SKILLED_V2
- freeze final Tier count
- freeze EXP/star/achievement values
- change live gameplay code
- freeze boss/shop cadence
- start detailed 3P/4P production balance

Governance:
`structure -> encounter envelope -> role-expression contract -> activation window -> class-aware role audit -> fitted player model -> synthetic slice -> full Tier -> meta recovery -> explicit freeze -> implementation`.
