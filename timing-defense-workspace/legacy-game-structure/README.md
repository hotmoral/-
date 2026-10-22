# Timing Defense — Legacy Game Structure Corpus

Date: 2026-10-22 KST  
Status: **STRUCTURAL CORPUS / CRITICAL ROLE-EXPRESSION V0.2 RERUN NEXT**

## 0. 목적

This corpus establishes and validates campaign/meta/combat structure before live implementation.

Principles:
- candidate != production authority
- close upstream structure before detailed authoring
- catch cheap errors with static/machine validation first
- require representative role-expression evidence before exact Stage authoring
- do not change live production values before explicit freeze

---

# 1. Current center

Top-level spine:
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

Integrated campaign matrix:
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current monster-role authority/evidence:
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `48_ROLE_EXPRESSION_FINE_SCAN_REPORT_V0_1.md`
- `50_CROSS_BRACKET_ROLE_EXPRESSION_ROBUSTNESS_V0_1.md`
- `52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`

Pipeline:
```text
Master Spine
 -> Layer0 structural PASS
 -> Encounter Envelope PASS
 -> Static/Kinematic/Sensitivity preflight
 -> Class-aware Layer-A V0.1
 -> Role-Expression Contract
 -> Fine Activation Calibration
 -> Role Metrics V0.2
 -> Critical 10-Recipe Audit
 -> All-20 Audit
 -> Fitted Player Model
 -> Synthetic Slice
 -> Full Tier
 -> Soft-wall/Meta
 -> Explicit Freeze
 -> Live Implementation
```

---

# 2. User-confirmed structure

- 5 classes; independent class Tier records/progression
- same Tier/Stage content shared across classes
- Tier = 50 Stages
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★
- stars = broad account permanent progression
- achievements = targeted cross-class progression
- recoverable soft walls intended; hard class lockout forbidden
- current 9 monsters are V1 foundation, not lifetime final roster
- T1 does not force all 9
- higher Tiers introduce new monsters
- future T5/T6/T7+ expansion open
- fitted non-T1 `SKILLED_V2_CENTRAL` full-clear normally <60%
- combo40 is skilled-achievable
- Lv31 target unlock = Stage41–45
- Stage46–49 = post-Lv31 mastery
- Stage50 = final, not Lv31 tutorial
- intended role encounters must not spawn-delete a monster before its role becomes meaningfully perceivable

Role-expression semantics:
```text
minimum role expression required
readable counterplay required
full enemy activation not guaranteed
```

---

# 3. Current Model A

```text
T1: GRUNT / RUNNER / BRUTE
T2: +SHIELD / +FLYER
T3: +CHARGER / +SPLITTER
T4: +SUPPORTER / +SIEGER
T5+: future content
```

Status:
**default bounded simulation spine / NOT production freeze**.

Fallback Model B remains available only if T4 lower-layer evidence fails.

---

# 4. Player-power candidate

- Lv6 5–7
- Lv11 11–14
- Lv16 18–21
- Lv21 25–28
- Lv26 32–36
- Lv31 **41–45**

Only Lv31 is user-confirmed as a target window.

Late grammar:
```text
31–39 pressure / soft wall
40     2★ gate
41–45  Lv31 Ascension
46–49  Post-Lv31 Mastery
50     Tier Final
```

---

# 5. Validation status

- Master Campaign Layer-0: PASS
- Encounter Envelope Layer-A0: PASS
- Representative static recipe preflight: PASS
- Kinematic preflight: PASS WITH WATCHES
- Generic DPS sensitivity: COMPLETE
- Class-aware Layer-A V0.1 critical subset: COMPLETE
- Monster Role Expression Contract: ESTABLISHED
- Fine CHARGER/SIEGER activation search: COMPLETE
- Three-bracket role robustness probe: COMPLETE
- Passive-role structural anchor audit: COMPLETE
- Role Metrics V0.2 instrumentation: READY
- Critical 10-recipe V0.2 rerun: NEXT

---

# 6. Monster Role Expression Contract

Current minimum expressions:

- GRUNT — baseline exempt
- RUNNER — speed changes arrival/front-order behavior
- BRUTE — meaningful durable frontline/screening
- SHIELD — mitigation changes effective damage/hit investment
- FLYER — vertical geometry changes actual line/splash/target opportunities
- CHARGER — visible windup + readable response window
- SPLITTER — meaningful post-death population/target-state change
- SUPPORTER — non-self aura for meaningful interval
- SIEGER — standoff + readable first-shot opportunity

Future monsters must declare:
`coreMechanic / minimumRoleExpression / readableCounterplay / failureClass / requiredMetrics`.

Do not equate role expression with successful full ability activation.

---

# 7. Current activation candidates

Diagnostic only; not production coordinates.

## E07 CHARGER
- initial search range was too narrow
- three-bracket all-five windup robust around `~0.54`
- broad all-profile expression region observed to about `~0.64`

## E17 CHARGER
- current strong anchor `~0.49`
- CONSERVATIVE/CENTRAL/STRONG all 5/5 windup
- sampled wall damage 0

## E11 SIEGER
- CENTRAL all-five actual-shot window roughly `0.70..0.82`
- low-change candidate near `~0.70`
- delay only the two ordinary GRUNTs by +250ms:
  - SHIELD 0
  - BRUTE 250
  - GRUNT 750
  - GRUNT 1000
  - SIEGER 1550
- CENTRAL: all-five shot expression with ordinary contact leak removed
- STRONG may prevent completed shot after SIEGER becomes readable; valid counterplay
- E11 remains wall-pressure WATCH until V0.2 temporal evidence

## E19 SIEGER
- current lower anchor `~0.70`
- CENTRAL all-five shot expression and no ordinary contact leak at anchor
- STRONG still retains five-class standoff/windup opportunity even when some shots are prevented

---

# 8. Passive identity anchors

Raw mechanics are distinct enough to measure rather than redesign:

- RUNNER speed ~1.93× GRUNT; no-combat wall arrival lead ~6.33s
- BRUTE HP 2.8125× GRUNT; knock displacement response ~44.7% of GRUNT
- SHIELD 28% mitigation under current provisional model; ~750 raw-equivalent durability
- FLYER has distinct Y oscillation; combat geometry value remains measurement-dependent

No production coefficient freeze follows from these anchors.

---

# 9. V0.2 role telemetry

V0.1 simulator remains preserved for reproducibility.

New V0.2 lane:
- `tools/simulate_class_aware_role_metrics_v0_2.py`
- `tools/evaluate_role_expression_v0_2.py`

New outputs include:
- per-type alive/frontline/hit/damage/prevented-damage metrics
- RUNNER distance advanced
- BRUTE frontline/hits/absorbed damage
- SHIELD mitigated hits/prevented damage
- FLYER Archer/Mage geometry opportunity time
- CHARGER windup visible time
- SPLITTER child alive/frontline/reorder/peak-delta
- SUPPORTER alive time, unique aura targets, screened-aura ratio
- SIEGER opportunity entries and visible windup time
- wall damage/hits by source, with `SIEGER_SHOT` separated

Automatic evaluator can require five-class structural role expression.
Exact minimum milliseconds/rates remain open until fitted SKILLED_V2.

---

# 10. Active document map

## Core structure
- `01_META_PROGRESSION.md`
- `02_TIER_SYSTEM.md`
- `03_STAGE_STRUCTURE_50.md`
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `05_LEGACY_EVIDENCE_MAP.md`
- `06_SIMULATION_CALIBRATION_PLAN.md`
- `07_AUTHORING_DATA_SCHEMA.md`
- `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
- `15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

## Master Campaign tranche
- `18_MONSTER_ROSTER_EXTENSIBILITY_AMENDMENT_2026-10-22.md`
- `19_MODEL_A_B_CLASS_ROLE_AND_VOLUME_AUDIT_V0_1.md`
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
- `21_MODEL_A_NOVELTY_BUDGET_AND_BOSS_PLACEHOLDERS_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
- `24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
- `25_MODEL_A_META_PROGRESS_VOLUME_AND_SOFT_WALL_ENVELOPE_V0_1.md`
- `26_MODEL_A_T1_T4_MACRO_SKELETON_V0_1.md`
- `27_MODEL_A_STATIC_MASTER_AUDIT_V0_1.md`
- `28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
- `29_MODEL_A_TIER_PRESSURE_COMPLEXITY_ENVELOPE_V0_1.md`
- `30_LAYER0_MODEL_A_VALIDATION_REPORT_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

## Encounter / Layer-A / role-expression tranche
- `32_MODEL_A_TIER_ENCOUNTER_AVAILABILITY_V0_1.md`
- `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- `34_MODEL_A_FREQUENCY_RANGE_ENVELOPE_V0_1.md`
- `35_LAYERA0_ENCOUNTER_ENVELOPE_VALIDATION_REPORT_V0_1.md`
- `36_REPRESENTATIVE_RECIPE_STATIC_PREFLIGHT_REPORT_V0_1.md`
- `37_REPRESENTATIVE_RECIPE_KINEMATIC_PREFLIGHT_REPORT_V0_1.md`
- `38_FORMATION_DEPTH_SCHEMA_AMENDMENT_V0_1.md`
- `39_FRONTMOST_DPS_SENSITIVITY_REPORT_V0_1.md`
- `40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`
- `41_CLASS_AWARE_ACTION_TRACE_MODEL_V0_1.md`
- `42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
- `43_ABSOLUTE_ENTRY_DEPTH_AMENDMENT_V0_1.md`
- `44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `46_ROLE_EXPRESSION_ADMISSION_AUDIT_V0_1.md`
- `47_ROLE_EXPRESSION_SCHEMA_AMENDMENT_V0_1.md`
- `48_ROLE_EXPRESSION_FINE_SCAN_REPORT_V0_1.md`
- `49_E11_SIEGE_TIMING_ADJUSTMENT_REPORT_V0_1.md`
- `50_CROSS_BRACKET_ROLE_EXPRESSION_ROBUSTNESS_V0_1.md`
- `51_PASSIVE_ROLE_STRUCTURAL_ANCHOR_REPORT_V0_1.md`
- `52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`

## Machine-readable data
- `data/model_a_campaign_spine_v0_1.yaml`
- `data/model_a_encounter_envelope_v0_1.yaml`
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_kinematic_anchor_v0_1.yaml`
- `data/model_a_combat_sensitivity_anchor_v0_1.yaml`
- `data/model_a_class_action_trace_bracket_v0_1.yaml`
- `data/monster_role_expression_contract_v0_1.yaml`
- `data/role_expression_activation_search_v0_1.yaml` — content V0.2
- `data/role_expression_activation_window_candidates_v0_1.yaml`
- `data/model_a_role_expression_geometry_overrides_v0_1.yaml`

## Analysis tools
- `../tools/validate_campaign_spine.py`
- `../tools/validate_encounter_envelope.py`
- `../tools/analyze_representative_recipes.py`
- `../tools/simulate_recipe_kinematics.py`
- `../tools/simulate_frontmost_dps_sensitivity.py`
- `../tools/simulate_class_aware_layer_a.py`
- `../tools/sweep_special_activation_entry_depth.py`
- `../tools/validate_monster_role_expression_contract.py`
- `../tools/evaluate_stateful_role_expression.py`
- `../tools/scan_activation_window_candidates.py`
- `../tools/probe_sieger_readability_budget.py`
- `../tools/probe_passive_role_contract_anchors.py`
- `../tools/simulate_class_aware_role_metrics_v0_2.py`
- `../tools/evaluate_role_expression_v0_2.py`

---

# 11. Parked / superseded candidates

Historical evidence only:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`
- `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Do not resume these as current authority.

---

# 12. Exact next layer

**10-recipe Critical-Set Role-Expression V0.2 Rerun.**

Before synthetic Tier slices:
1. apply current diagnostic geometry overrides to a non-production candidate dataset
2. run 10 critical recipes × 3 brackets × 5 classes through V0.2
3. automatically evaluate all-five minimum expression
4. inspect temporal contact-wall pressure
5. make only localized recipe geometry/cadence changes if needed
6. close critical-set role-expression admission
7. expand V0.2 audit to all 20 recipes
8. only then return to fitted SKILLED_V2 harness

Then:
- synthetic Tier slices
- full Tier simulation
- 5-class soft-wall map
- stars-only recovery
- achievement bridge model
- account simulation

---

# 13. Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster coefficients
- production entry coordinates
- exact 200-Stage schedule
- exact EXP formula
- Lv11+ production coefficients
- permanent star reward values
- achievement reward graph/value
- boss cadence/design
- shop cadence/economy
- detailed multiplayer balance

No live gameplay patch is authorized by this corpus tranche.
