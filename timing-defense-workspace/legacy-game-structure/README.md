# Timing Defense — Legacy Game Structure Corpus

Date: 2026-10-22 KST  
Status: **STRUCTURAL CORPUS / SYSTEM DEPENDENCY + RUN-STATE PRE-SYNTHETIC-TIER**

## 0. 목적

This corpus establishes and validates campaign/meta/combat structure before live implementation.

Principles:
- candidate != production authority
- close upstream semantics before detailed numerical tuning
- catch cheap errors with static/machine validation first
- require representative role-expression evidence before exact Stage authoring
- integrate coupled systems progressively rather than balancing them independently and summing later
- re-check upstream invariants whenever a new power layer is added
- do not change live production values before explicit freeze

---

# 1. Current center

Top-level campaign spine:
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

Integrated bounded campaign matrix:
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current execution-order authority:
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `data/system_dependency_calibration_order_v0_1.yaml`

Latest central-skilled structural evidence:
- `66_SKILLED_V2_CENTRAL_DESIGN_PRIOR_AND_HARNESS_CLOSURE_AMENDMENT_V0_1.md`
- `67_SKILLED_V2_CENTRAL_SEQUENCE_MODEL_V0_1.md`
- `68_SKILLED_V2_CENTRAL_ALL20_INTEGRATION_PREFLIGHT_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`

Current monster-role authority/evidence:
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `52_ROLE_METRICS_V0_2_INSTRUMENTATION.md`
- `53_CRITICAL_ROLE_EXPRESSION_V0_2_RERUN_REPORT_V0_1.md`
- `54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`

Current pipeline:

```text
Master Spine / Model A
 -> Layer0 structural PASS
 -> Encounter Envelope PASS
 -> Static/Kinematic/Sensitivity preflight
 -> Class-aware Layer-A
 -> Role-Expression Contract
 -> Critical 10 + All-20 role audits
 -> provisional streak-aware SKILLED_V2_CENTRAL design prior
 -> corrected central All-20 role integration PASS
 -> P1 Run-State Lifecycle Contract
 -> P2 Modifier Pipeline / Power Attribution Contract
 -> P3 10-Stage Persistent Run Kernel
 -> P4 Player-Power Spine
 -> P5 Coin/Shop Candidate
 -> P6 Joint Run-Power Convergence
 -> P7 Boss/Checkpoint Proxy
 -> P8 Solo P0 Full-Tier Baseline
 -> P9 Soft-Wall + Stat Sensitivity
 -> P10 Multiplayer Combat Scaling
 -> P11 Stars-Only Progression
 -> P12 Achievement Cross-Class Graph
 -> P13 Account Route Simulation
 -> P14 Launch Tier Count / Unlock Gate
 -> P15 Exact Campaign/Boss Authoring
 -> P16 Multiplayer Progression-Credit Audit
 -> P17 Full-System Stress / Numerical Freeze
 -> P18 Production Implementation
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
- non-T1 `SKILLED_V2_CENTRAL` full-clear normally <60% as an upper gate
- combo40 is skilled-achievable
- Lv31 target unlock = Stage41–45
- Stage46–49 = post-Lv31 mastery
- Stage50 = final, not Lv31 tutorial
- intended role encounters must not delete a monster before its role becomes meaningfully perceivable

Role-expression semantics:

```text
minimum role expression required
readable counterplay required
full enemy activation not guaranteed
```

Ordinary-skilled design prior currently authorized for bounded simulation:

```text
PERFECT 70%
GOOD    20%
NORMAL  10%
```

This is implemented as a streak-aware deterministic candidate and is **not empirical population telemetry**.
The primary user's observed traces remain separate as `HIGH_MASTERY_STRESS_CANDIDATE` evidence.

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

Important current systems dependency:
- EXP is tied to valid timing events.
- Shop/permanent power can change kill speed and therefore the number of EXP-producing events.
- Skill reach must be revalidated after shop integration and again after permanent-power integration.

---

# 5. Validation status

- Master Campaign Layer-0: PASS
- Encounter Envelope Layer-A0: PASS
- Representative static recipe preflight: PASS
- Kinematic preflight: PASS WITH WATCHES
- Generic DPS sensitivity: COMPLETE
- Class-aware Layer-A V0.1: COMPLETE
- Monster Role Expression Contract: ESTABLISHED
- Fine activation calibration: COMPLETE
- Three-bracket role robustness: COMPLETE
- Passive-role structural anchor audit: COMPLETE
- Role Metrics V0.2 instrumentation: COMPLETE
- Critical 10 V0.2 rerun: PASS_WITH_WATCHES
- Historical All-20 audit: PASS_WITH_WATCHES / 540 OF 540
- High-mastery H0/H3 observed traces: retained as upper-anchor evidence
- H4 stateful-read skill-fit premise: superseded for player-skill calibration under current input semantics
- provisional SKILLED_V2_CENTRAL sequence candidate: ESTABLISHED
- corrected central All-20 integration: PASS_WITH_WATCHES / 540 OF 540
- historical regression after E08/E20 refinements: 540 OF 540
- system dependency / calibration-order review: ACTIVE AUTHORITY

Latest central watches:
- T4 E10/E11/E18/E19 siege wall pressure
- T3 E13 wall pressure
- E20 CHARGER lower-tail readability
- combo40 requires persistent multi-stage evidence, not short encounter rows

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

# 7. Current localized role candidates / watches

Diagnostic only; not production coordinates.

## E08 SPLITTER
Current additional-10 content V0.2 shifts the two representative SPLITTER insertions to:

```text
500ms
2000ms
```

This prevents the provisional central Mage path from erasing parent and newborn children in the same authoritative action while retaining historical role gates.

## E20 SPLITTER + CHARGER
Current bounded re-author candidate:

```text
SPLITTER spawn       = 0ms
SPLITTER relative X  = -0.02
CHARGER spawn        = 2000ms
CHARGER relative X   = -0.50
```

Central and historical role gates remain intact.
CHARGER lower-tail readability remains a WATCH, not a frozen threshold.

Other historical activation candidates remain evidence only and do not become production coordinates automatically.

---

# 8. System dependency authority

The project no longer uses a coarse assumption that all run economy / boss / multiplayer work can be treated as one undifferentiated downstream block.

`70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md` establishes:

- explicit run-state lifecycle before multi-stage simulation;
- explicit modifier operation/stack semantics before reward values;
- EXP/skill ↔ shop ↔ permanent-power feedback rechecks;
- boss/checkpoint proxy before final full-Tier/star calibration;
- multiplayer combat scaling before permanent progression values are finalized;
- multiplayer progression-credit/exploit audit later, after meta candidates exist;
- exact campaign authoring late;
- two-stage freeze policy: structural/semantic first, numerical/content last.

Machine-readable dependency authority:
`data/system_dependency_calibration_order_v0_1.yaml`.

---

# 9. Active document map

## Core structure / governance
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
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`

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
- `53_CRITICAL_ROLE_EXPRESSION_V0_2_RERUN_REPORT_V0_1.md`
- `54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`

## Player calibration / central candidate tranche
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `56_SKILLED_V2_TRACE_COLLECTION_PIPELINE_V0_1.md`
- `57_SKILLED_V2_COLLECTION_READINESS_REVIEW_V0_1.md`
- `58_SKILLED_V2_PLAYABLE_HARNESS_IMPLEMENTATION_CONTRACT_V0_1.md`
- `59_SKILLED_V2_HARNESS_IMPLEMENTATION_PREFLIGHT_V0_1.md`
- `60_SKILLED_V2_HARNESS_IMPLEMENTATION_STATUS_V0_1.md`
- `61_HIGH_MASTERY_PLAYER_ANCHOR_AMENDMENT_V0_1.md`
- `62_SKILLED_V2_CALIBRATION_DEPLOYMENT_READINESS_V0_1.md`
- `63_HIGH_MASTERY_H0_OBSERVED_TRACE_REPORT_V0_1.md`
- `64_HIGH_MASTERY_H3_OBSERVED_TRACE_REPORT_V0_1.md`
- `65_HIGH_MASTERY_H4_OBSERVED_TRACE_INSTRUMENTATION_AUDIT_V0_1.md`
- `66_SKILLED_V2_CENTRAL_DESIGN_PRIOR_AND_HARNESS_CLOSURE_AMENDMENT_V0_1.md`
- `67_SKILLED_V2_CENTRAL_SEQUENCE_MODEL_V0_1.md`
- `68_SKILLED_V2_CENTRAL_ALL20_INTEGRATION_PREFLIGHT_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`

## Machine-readable data
- `data/model_a_campaign_spine_v0_1.yaml`
- `data/model_a_encounter_envelope_v0_1.yaml`
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_kinematic_anchor_v0_1.yaml`
- `data/model_a_combat_sensitivity_anchor_v0_1.yaml`
- `data/model_a_class_action_trace_bracket_v0_1.yaml`
- `data/monster_role_expression_contract_v0_1.yaml`
- `data/model_a_critical_role_expression_candidates_v0_1.yaml`
- `data/model_a_additional10_role_expression_candidates_v0_1.yaml` — content V0.2
- `data/skilled_v2_central_sequence_candidate_v0_1.yaml`
- `data/skilled_v2_controlled_harness_v0_1.yaml`
- `data/skilled_v2_trace_schema_v0_1.yaml`
- `data/system_dependency_calibration_order_v0_1.yaml`

## Analysis tools
- `../tools/validate_campaign_spine.py`
- `../tools/validate_encounter_envelope.py`
- `../tools/analyze_representative_recipes.py`
- `../tools/simulate_recipe_kinematics.py`
- `../tools/simulate_frontmost_dps_sensitivity.py`
- `../tools/simulate_class_aware_layer_a.py`
- `../tools/simulate_class_aware_role_metrics_v0_2.py`
- `../tools/evaluate_role_expression_v0_2.py`
- `../tools/validate_skilled_v2_harness.py`
- `../tools/validate_skilled_v2_trace_dataset.py`
- `../tools/validate_skilled_v2_central_sequence.py`
- `../tools/run_skilled_v2_central_role_probe.py`

---

# 10. Parked / superseded candidates

Historical evidence only:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`
- `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Historical deterministic 600/750/900ms trace brackets remain diagnostic probes and are not current fitted skilled population authority.

Do not resume parked documents as current authority merely because their implementation or numbers are older and concrete.

---

# 11. Exact next layer

Current foundation is closed enough for multi-stage integration, but **do not implement the 10-stage kernel before its state semantics are explicit**.

Next in parallel:

## P1 — Run-State Lifecycle Contract
Define reset/persist/derive/owner semantics for:
- base/wall HP;
- combo;
- charge/heavy;
- level/EXP;
- run coin;
- shop ranks;
- Stage/Tier failure/end;
- reconnect restoration;
- deterministic RNG/replay state.

## P2 — Modifier Pipeline / Power Attribution Contract
Define:
- modifier scopes;
- operation ordering;
- stack policies;
- source/version attribution;
- effective damage/control/wall-event explanation.

Then:

## P3 — 10-Stage Persistent Run Kernel
Purpose:
- state continuity;
- failure semantics;
- base HP persistence;
- combo/charge continuity;
- deterministic replay;
- early skill-window integration.

Do not yet include final permanent values, exact shop curve, final boss novelty or multiplayer progression credit.

---

# 12. Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster coefficients
- production entry coordinates
- exact 200-Stage schedule
- exact EXP formula
- Lv11+ production coefficients
- exact shop cadence/economy
- modifier numerical stack coefficients
- permanent star reward values/milestones
- achievement reward graph/value
- exact boss cadence/design
- detailed multiplayer balance/progression credit

No live gameplay patch is authorized by this corpus tranche.
