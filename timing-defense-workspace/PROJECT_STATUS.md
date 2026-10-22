# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# Current planning phase

**Monster Role-Expression / Activation-Window Calibration**

Upstream campaign structure remains sufficiently closed.
Model A remains the default bounded simulation spine, not a production freeze.

Primary campaign authority:
- `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current role-expression authority:
- `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `legacy-game-structure/46_ROLE_EXPRESSION_ADMISSION_AUDIT_V0_1.md`
- `legacy-game-structure/47_ROLE_EXPRESSION_SCHEMA_AMENDMENT_V0_1.md`

Supporting Layer-A evidence:
- `41_CLASS_AWARE_ACTION_TRACE_MODEL_V0_1.md`
- `42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
- `43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
- `44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`

---

# Core user-confirmed truth

- 5 classes progress independently through Tiers.
- Same Tier/Stage combat content is shared across classes.
- 1 Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intentional; hard class lockout forbidden.
- current 9 ordinary monsters are not lifetime final roster.
- T1 does not teach all 9; higher Tiers introduce new monsters.
- future Tier/monster expansion open.
- non-T1 intended-entry fitted `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 is skilled-achievable.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery.
- Stage50 is final, not Lv31 tutorial.
- intended encounters must not allow a monster to spawn and disappear before its role is meaningfully perceivable.

Role-expression interpretation:
- minimum expression opportunity required
- full ability completion not always required
- skilled counterplay after readable expression is valid
- pre-expression deletion without readable counterplay is invalid authoring

---

# Model A

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

Fallback Model B remains available only if T4 lower-layer evidence fails.

---

# Validation chain

- Master Campaign Layer-0: PASS, errors=0 warnings=0
- Encounter Envelope Layer-A0: PASS, errors=0 warnings=0
- Representative recipe static preflight: PASS
- Kinematic preflight: PASS WITH WATCHES
- Generic DPS sensitivity: COMPLETE
- Class-aware CURRENT_AUTHORITY micro-sim V0.1: COMPLETE for critical subset
- Absolute entry-depth activation diagnostic: COMPLETE
- Monster Role Expression Contract V0.1: ESTABLISHED
- Role-expression critical admission: BLOCKED pending localized fixes/instrumentation

---

# Monster role-expression contract

Current nine:
- GRUNT — baseline reference, exempt from special expression gate
- RUNNER — speed must create observable arrival/front-order difference
- BRUTE — must meaningfully hold/absorb frontline attention
- SHIELD — mitigation must change effective damage/hit investment
- FLYER — vertical geometry must create a real opportunity/targeting difference
- CHARGER — visible windup + readable response window
- SPLITTER — split must produce meaningful post-death population/target-state change
- SUPPORTER — aura must affect at least one non-self target for a meaningful interval
- SIEGER — standoff + readable first-shot opportunity

Every future monster must declare:
`coreMechanic / minimumRoleExpression / readableCounterplay / failureClass / requiredMetrics`.

---

# Current role-expression admission

```text
ROLE_EXPRESSION_ADMISSION = BLOCKED
```

Per monster:
- GRUNT: BASELINE_EXEMPT
- RUNNER: MEASUREMENT_REQUIRED
- BRUTE: PRELIMINARY_ROLE_PRESENT / METRIC_REQUIRED
- SHIELD: MEASUREMENT_REQUIRED
- FLYER: MEASUREMENT_REQUIRED
- CHARGER: FAIL_DEFAULT_GEOMETRY
- SPLITTER: PARTIAL_PASS / WATCH
- SUPPORTER: PASS_WITH_WATCH
- SIEGER: FAIL_DEFAULT_GEOMETRY

This is not a request for broad campaign redesign.
It is localized encounter geometry + simulation observability work.

---

# Stateful capability evidence

CHARGER default critical T3 recipes:
- 60 pre-windup erasures
- 0 windups in prior 3-profile × 5-class critical sweep

SIEGER default E11/E19:
- 0 shots in prior critical class/trace sweep

SUPPORTER:
- role expression exists
- screened aura duration varies strongly by class/throughput

SPLITTER:
- parent -> two-child transformation works
- meaningful child lifetime/frontline impact still under-instrumented

No global HP buff is authorized from these findings.

---

# Activation-window search

Absolute entry depth and relative screen depth are separate variables.
Capability activation is non-monotonic.

Current diagnostic anchors only:
- E07 CHARGER useful activation evidence begins around ~0.25; interruption around ~0.30
- E17 CHARGER all-five windup visibility around ~0.45
- E11 SIEGER all-five actual-shot visibility around ~0.70–0.80; collapse near ~0.85
- E19 SIEGER all-five actual-shot visibility around ~0.75–0.80; collapse near ~0.85

Fine scan configuration now exists at 0.01 steps in:
`data/role_expression_activation_search_v0_1.yaml`.

These are not production coordinates.

---

# Current tools/data

Data:
- `data/monster_role_expression_contract_v0_1.yaml`
- `data/role_expression_activation_search_v0_1.yaml`
- `data/model_a_class_action_trace_bracket_v0_1.yaml`
- `data/model_a_representative_recipes_v0_1.yaml`

Tools:
- `validate_monster_role_expression_contract.py`
- `evaluate_stateful_role_expression.py`
- `scan_activation_window_candidates.py`
- `simulate_class_aware_layer_a.py`
- `sweep_special_activation_entry_depth.py`

---

# Player-trace authority boundary

Current deterministic trace bracket remains:
- 900 ms / PERFECT streak 40 then GOOD
- 750 ms / PERFECT streak 55 then GOOD
- 600 ms / PERFECT streak 75 then GOOD

Status:
**CALIBRATION BRACKET NOT FITTED**

Do not use it to claim production SKILLED_V2 clear probability.

---

# Current exact work

Now allowed:
1. critical-set role-expression calibration
2. fine CHARGER/SIEGER activation-window scanning
3. SIEGER standoff/windup/first-shot-opportunity instrumentation
4. SPLITTER child lifetime/frontline/population-delta instrumentation
5. SUPPORTER normalized aura metrics
6. RUNNER/BRUTE/SHIELD/FLYER passive-role instrumentation
7. repeat CURRENT_AUTHORITY five-class critical micro-sim
8. expand to all 20 recipes only after critical-set admission improves to PASS/acceptable WATCH

Not allowed yet:
- exact 200-Stage schedule
- production monster coefficient or coordinate freeze
- fitted SKILLED_V2 claims from current brackets
- live campaign patch
- final Tier count
- exact EXP/star/achievement values
- boss/shop freeze
- detailed 3P/4P production balance

No live gameplay source or production balance value was changed by this tranche.
