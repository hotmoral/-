# Timing Defense — Legacy Game Structure Corpus

Date: 2026-10-22 KST  
Status: **STRUCTURAL CORPUS / ROLE-EXPRESSION CALIBRATION ACTIVE**

## 0. 목적

이 자료군은 Timing Defense의 campaign/meta/combat 구조를 live 구현보다 먼저 정립·검증하기 위한 canonical planning corpus다.

핵심 원칙:
- candidate와 production authority를 분리한다.
- 상위 구조를 먼저 닫는다.
- 정적/machine validation으로 싼 오류를 먼저 제거한다.
- representative simulation을 통과한 뒤에만 exact Stage authoring으로 내려간다.
- explicit freeze 전 live production 수치를 바꾸지 않는다.

---

# 1. Current center

Top-level principle:
`16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

Current integrated matrix:
`31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current monster-role authority:
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `46_ROLE_EXPRESSION_ADMISSION_AUDIT_V0_1.md`
- `47_ROLE_EXPRESSION_SCHEMA_AMENDMENT_V0_1.md`

Common coordinate:
```text
Tier × Stage1..50 × Content Novelty × Player Power × Meta Progression
```

Current pipeline:
```text
Master Spine
 -> Layer0 structural PASS
 -> Encounter Envelope PASS
 -> Static/Kinematic/Sensitivity preflight
 -> Class-aware Layer-A
 -> Role-Expression Contract
 -> Activation Window Calibration
 -> All-20 Representative Audit
 -> Fitted Player Model
 -> Synthetic Slice
 -> Full Tier
 -> Soft-wall/Meta
 -> Explicit Freeze
 -> Live Implementation
```

---

# 2. User-confirmed structure

- 5 classes, independent Tier records/progression
- same Tier/Stage combat content shared across classes
- one Tier = 50 Stages
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★
- stars = broad account permanent growth
- achievements = targeted cross-class growth
- recoverable soft walls intended; hard class lockout forbidden
- current 9 monsters are V1 foundation, not lifetime final roster
- T1 does not force all 9
- higher Tiers introduce new monsters
- future T5/T6/T7+ expansion open
- fitted non-T1 SKILLED_V2_CENTRAL full-clear normally <60%
- combo40 is skilled-achievable
- Lv31 target unlock = Stage41–45
- Stage46–49 = post-Lv31 mastery
- Stage50 = final, not Lv31 tutorial
- intended encounter에서 monster가 role을 보여주기 전에 spawn-delete 되는 구조는 허용하지 않음

Role-expression interpretation:
```text
minimum expression opportunity = required
readable counterplay = required
full enemy activation = not guaranteed
```

---

# 3. Current Model A

```text
T1: GRUNT / RUNNER / BRUTE           Foundation / Timing & Frontline
T2: +SHIELD / +FLYER                 Mitigation / Geometry
T3: +CHARGER / +SPLITTER             Burst / Transformation
T4: +SUPPORTER / +SIEGER             Formation / Siege
T5+: future content                  Expansion
```

Status:
**default bounded simulation spine / NOT production freeze**

Fallback Model B:
- T4 +SUPPORTER
- T5 +SIEGER
- only if T4 lower-layer evidence fails

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

## Master Campaign Layer-0
`PASS errors=0 warnings=0`

## Encounter Envelope Layer-A0
`PASS errors=0 warnings=0`

## Representative Recipe Static Preflight
PASS.
- 20 deterministic recipes
- max authored 4s = 7
- max conservative effective 4s = 10

## Kinematic Preflight
PASS WITH WATCHES.

Important discovery:
- BACK cannot rely on delayed spawn only
- relative X-depth is required

## Generic DPS Sensitivity
COMPLETE.

Important discovery:
- special capability uptime is strongly throughput-sensitive
- CHARGER/SIEGER can disappear before expressing their mechanic

## Class-aware Layer-A V0.1
COMPLETE for 10-recipe critical subset.

Important discovery:
- default CHARGER critical recipes produced 0 windups
- default E11/E19 SIEGER produced 0 shots
- SUPPORTER role exists with high class sensitivity
- SPLITTER transforms, but meaningful child lifetime is under-instrumented

## Role-expression admission
`BLOCKED` pending localized calibration/instrumentation.

---

# 6. Monster Role Expression Contract

Current minimum expressions:

- GRUNT — baseline exempt
- RUNNER — speed changes arrival/front-order behavior
- BRUTE — meaningful durable frontline/screening
- SHIELD — mitigation changes effective damage/hit investment
- FLYER — vertical geometry creates real line/splash/target-order difference
- CHARGER — visible windup + readable response window
- SPLITTER — meaningful post-death population/target-state change
- SUPPORTER — non-self aura for meaningful interval
- SIEGER — standoff + readable first-shot opportunity

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

Future monsters must define:
`coreMechanic / minimumRoleExpression / readableCounterplay / failureClass / requiredMetrics`.

---

# 7. Activation-window search

Absolute entry depth is independent from relative FRONT/MID/BACK depth.
Activation is non-monotonic.

Current diagnostic anchors only:
- E07 CHARGER: useful evidence begins around ~0.25; interrupt around ~0.30
- E17 CHARGER: all-five windup visibility around ~0.45
- E11 SIEGER: all-five actual-shot visibility around ~0.70–0.80; collapse near ~0.85
- E19 SIEGER: all-five actual-shot visibility around ~0.75–0.80; collapse near ~0.85

Fine search set:
- E07 0.20–0.40
- E17 0.35–0.55
- E11 0.65–0.84
- E19 0.68–0.84
- step .01

These are search ranges, not production coordinates.

---

# 8. Active document map

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

## Encounter / Layer-A tranche
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

## Machine-readable data
- `data/model_a_campaign_spine_v0_1.yaml`
- `data/model_a_encounter_envelope_v0_1.yaml`
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_kinematic_anchor_v0_1.yaml`
- `data/model_a_combat_sensitivity_anchor_v0_1.yaml`
- `data/model_a_class_action_trace_bracket_v0_1.yaml`
- `data/monster_role_expression_contract_v0_1.yaml`
- `data/role_expression_activation_search_v0_1.yaml`

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

---

# 9. Parked / superseded candidates

Historical evidence only:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`
- `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Do not resume these as current authority.

---

# 10. Exact next layer

**Critical-set role-expression calibration.**

Before synthetic Tier slices:
1. fine-scan CHARGER E07/E17 windows
2. fine-scan SIEGER E11/E19 windows
3. reject unavoidable wall-pressure ranges
4. instrument first-shot-opportunity separately from actual SIEGER shot
5. instrument SPLITTER child meaningful lifetime/frontline effect
6. normalize SUPPORTER aura metrics
7. add RUNNER/BRUTE/SHIELD/FLYER role metrics
8. rerun 10-recipe critical subset
9. expand to all 20 only after critical role-expression PASS/acceptable WATCH
10. fit SKILLED_V2 only after role-expression structure is stable

Then:
- synthetic Tier slices
- full Tier simulation
- 5-class soft-wall map
- stars-only recovery
- achievement bridge model
- account simulation

---

# 11. Still not frozen

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
