# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Canonical recovery rule
Always fetch live `timing-defense-workspace` HEAD first.
Live remote wins over memory/chat/handoff.

## Current executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

---

# CURRENT PHASE

**Monster Role-Expression / Activation-Window Calibration**

Broad campaign redesign is not the blocker.
Current work is localized to encounter role expression, geometry, and simulation observability before synthetic Tier slices.

Read first:
1. `PROJECT_STATUS.md`
2. `NEXT_WORK.md`
3. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
4. `legacy-game-structure/46_ROLE_EXPRESSION_ADMISSION_AUDIT_V0_1.md`
5. `legacy-game-structure/47_ROLE_EXPRESSION_SCHEMA_AMENDMENT_V0_1.md`
6. `legacy-game-structure/44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`
7. `legacy-game-structure/42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
8. `legacy-game-structure/43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
9. `legacy-game-structure/41_CLASS_AWARE_ACTION_TRACE_MODEL_V0_1.md`
10. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
11. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`

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

# USER-CONFIRMED STRUCTURAL TRUTH

- 5 classes; independent class Tier progress.
- Same Tier/Stage combat content across all classes.
- Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear Stage50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
- T1 does not expose all 9; higher Tiers introduce new monsters.
- future T5/T6/T7+ monster expansion remains open.
- fitted non-T1 `SKILLED_V2_CENTRAL` full-clear should normally be <60%.
- combo40 is skilled-achievable, not high-mastery-only.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery.
- Stage50 is final application, not Lv31 tutorial.
- **intended encounters must not let monsters spawn and disappear before their role becomes meaningfully perceivable.**

---

# MONSTER ROLE-EXPRESSION RULE

Three distinct concepts must never be collapsed:

```text
1. MINIMUM ROLE EXPRESSION
   the mechanic becomes perceivable

2. READABLE COUNTERPLAY
   the player has a meaningful response window

3. FULL ACTIVATION
   the enemy mechanic succeeds/completes
```

Rules:
- #1 and #2 are structurally required in intended role-expression encounters.
- #3 is not guaranteed; skilled counterplay may prevent it.
- `PRE_EXPRESSION_DEATH_WITHOUT_READABLE_COUNTERPLAY` is invalid authoring.
- do not solve role disappearance by global HP inflation first.
- geometry/cadence/screen timing are first-line authoring controls.

Examples:
- CHARGER visible windup -> player interrupts = valid
- CHARGER dies before any windup = invalid designated CHARGER encounter
- SIEGER enters first-shot windup -> player breaks screen/kills it = valid
- SIEGER routinely dies before a real first-shot opportunity = invalid

---

# CURRENT NINE-MONSTER CONTRACT

- GRUNT: baseline exempt
- RUNNER: speed changes arrival/front-order behavior
- BRUTE: meaningful durable frontline/screening
- SHIELD: mitigation changes effective damage/hit investment
- FLYER: vertical geometry creates actual line/splash/target-order difference
- CHARGER: visible windup + readable response window
- SPLITTER: split causes meaningful post-death population/target-state change
- SUPPORTER: non-self aura for meaningful interval
- SIEGER: standoff + readable first-shot opportunity

Future monsters must define:
`coreMechanic / minimumRoleExpression / readableCounterplay / failureClass / requiredMetrics`.

---

# MODEL A

Default bounded simulation spine:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

NOT production frozen.
Model B remains fallback only if T4 lower-layer evidence fails.

---

# COMPLETED VALIDATION CHAIN

```text
Master Campaign Layer-0 PASS
 -> Encounter Envelope Layer-A0 PASS
 -> Static recipe PASS
 -> Kinematic PASS WITH WATCHES
 -> Generic DPS sensitivity COMPLETE
 -> Layer-A admission PASS
 -> Class-aware CURRENT_AUTHORITY micro-sim V0.1 COMPLETE
 -> Absolute entry-depth activation diagnostic COMPLETE
 -> Monster Role Expression Contract V0.1 ESTABLISHED
 -> Critical role-expression audit COMPLETE / BLOCKED
```

---

# CRITICAL ROLE-EXPRESSION STATUS

```text
ROLE_EXPRESSION_ADMISSION = BLOCKED
```

Per monster:
- GRUNT = BASELINE_EXEMPT
- RUNNER = MEASUREMENT_REQUIRED
- BRUTE = PRELIMINARY_ROLE_PRESENT / METRIC_REQUIRED
- SHIELD = MEASUREMENT_REQUIRED
- FLYER = MEASUREMENT_REQUIRED
- CHARGER = FAIL_DEFAULT_GEOMETRY
- SPLITTER = PARTIAL_PASS / WATCH
- SUPPORTER = PASS_WITH_WATCH
- SIEGER = FAIL_DEFAULT_GEOMETRY

This is a localized lower-layer block, not an upstream campaign failure.

---

# CLASS-AWARE ACTION MODEL

Current exact authority included:
- base timing/heavy/combo damage
- Lv6 class authority
- N3 milestone authority
- current provisional v0.45 monster capability semantics

Excluded from headline V0.1:
- Lv11/16/21 parity candidate
- Lv26/31 future placeholder
- production meta/shop modifiers

Current trace bracket:
- CONSERVATIVE: 900 ms, 40 PERFECT judge streak then GOOD
- CENTRAL: 750 ms, 55 PERFECT judge streak then GOOD
- STRONG: 600 ms, 75 PERFECT judge streak then GOOD

These are **not fitted SKILLED_V2**.
They are deterministic optimistic mechanics probes.

---

# CURRENT STATEFUL EVIDENCE

## CHARGER
Prior default critical T3 recipes:
- 60 pre-windup erasures
- 0 windups across current class/trace critical sweep

Current diagnosis:
`FAIL_DEFAULT_GEOMETRY`.

Coarse search anchors only:
- E07 useful windup evidence begins around ~0.25; first interrupt evidence around ~0.30
- E17 all-five windup visibility around ~0.45

## SIEGER
Prior default E11/E19:
- 0 shots across critical class/trace sweep

Current diagnosis:
`FAIL_DEFAULT_GEOMETRY`.

Coarse search anchors only:
- E11 all-five actual-shot visibility ~0.70–0.80; collapse near ~0.85
- E19 all-five actual-shot visibility ~0.75–0.80; collapse near ~0.85

## SUPPORTER
Minimum aura expression exists, but screened aura is highly class/throughput sensitive.
Need normalized `screenedAuraUptime / supporterAliveTime`.

## SPLITTER
Parent -> two children works.
Need child lifetime/frontline/population-delta metrics to prove meaningful post-split state.

---

# ABSOLUTE ENTRY DEPTH

Keep separate:

```text
relative depth = FRONT/MID/BACK relation inside formation
absolute entry depth = where whole encounter starts on X
```

Activation is non-monotonic.
Too far can cause pre-expression deletion; too close can expose the special or create unavoidable wall pressure.

Do not interpret closer as a universal difficulty scalar.

---

# FINE SEARCH SET

Current diagnostic search configuration:

- E07 CHARGER: shift 0.20–0.40, step .01
- E17 CHARGER: 0.35–0.55, step .01
- E11 SIEGER: 0.65–0.84, step .01
- E19 SIEGER: 0.68–0.84, step .01

Stored in:
`data/role_expression_activation_search_v0_1.yaml`.

The scanner prefers contiguous all-five expression windows with lower wall pressure, but does not freeze coordinates.

---

# EXACT NEXT BOUNDARY

Proceed with **critical-set role-expression calibration**.

Order:
1. run fine CHARGER E07/E17 activation-window scans
2. preserve readable windup and interruption opportunity across all five classes
3. reject unavoidable wall-pressure ranges
4. run fine SIEGER E11/E19 scans
5. instrument SIEGER standoff/windup/first-shot-opportunity separately from actual shot
6. add SPLITTER child lifetime/frontline/population-delta metrics
7. add SUPPORTER normalized aura metrics
8. add RUNNER/BRUTE/SHIELD/FLYER passive-role metrics
9. rerun the 10-recipe critical set
10. require role-expression PASS/acceptable WATCH before all-20 expansion
11. expand to all 20 representative recipes
12. only then return to fitted SKILLED_V2 harness and synthetic Tier slices

Do NOT yet:
- author exact 200 launch stages
- freeze production monster coefficients or entry coordinates
- freeze current trace brackets as SKILLED_V2
- freeze final Tier count
- freeze EXP/star/achievement values
- change live gameplay code
- freeze boss/shop cadence
- start detailed 3P/4P production balance

---

# HANDOFF DISCIPLINE

New session must:
1. fetch live `timing-defense-workspace` HEAD
2. read this handoff + PROJECT_STATUS + NEXT_WORK
3. read docs 45–47, then 42–44
4. inspect machine-readable role contract and fine-search data
5. verify no newer remote changes
6. continue only from critical role-expression calibration

Current tranche changes planning/corpus/data/analysis tools only.
No live gameplay source or production balance value was changed.
