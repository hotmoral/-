# Timing Defense — Legacy Game Structure Corpus

Date: 2026-10-22 KST  
Status: **STRUCTURAL CORPUS / MODEL A ADMITTED TO CLASS-AWARE LAYER-A**

## 0. 목적

이 자료군은 Timing Defense의 campaign/meta/combat 구조를 live 구현보다 먼저 정립하고 검증하기 위한 canonical planning corpus다.

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

Current lower-layer admission:
`40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`

Common coordinate:
```text
Tier × Stage1..50 × Content Novelty × Player Power × Meta Progression
```

Current pipeline:
```text
Master Spine
 -> Layer0 structural PASS
 -> Encounter Envelope PASS
 -> Static Recipe PASS
 -> Kinematic PASS/WATCH
 -> Generic DPS Sensitivity
 -> Class-aware Layer-A
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
- non-T1 intended-entry SKILLED_V2_CENTRAL full-clear normally <60%
- combo40 is skilled-achievable
- **Lv31 target unlock = Stage41–45**
- Stage46–49 = post-Lv31 mastery
- Stage50 = final, not Lv31 tutorial

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
- only if T4 lower-layer evidence fails.

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
- 20 representative deterministic recipes
- max authored 4s = 7
- max conservative effective 4s = 10
- no density WATCH/ERROR

## Kinematic Preflight
PASS WITH WATCHES.

Confirmed:
- representative CHARGER windup concurrency <=1
- E10 focused siege vs E11 escorted siege distinct under actual movement
- E19 can produce durable-screened siege
- E09/E16 produce bounded support interaction

Discovered:
- BACK cannot be represented reliably by delayed spawn alone when unit speeds differ
- formation needs explicit geometric X-depth capability

## Generic DPS Sensitivity
Diagnostic complete.

Finding:
- special capability uptime is strongly dependent on frontline removal speed
- SIEGER can be erased before firing
- CHARGER can be erased before windup
- SUPPORTER aura duration can collapse or persist based on screen removal
- SPLITTER wall pressure changes with throughput

No numeric patch is authorized from this diagnostic.

## Layer-A Admission
**ADMIT TO CLASS-AWARE LAYER-A COMBAT MICRO-SIMULATION**

---

# 6. Current active documents

## Core structure
- `01_META_PROGRESSION.md`
- `02_TIER_SYSTEM.md`
- `03_STAGE_STRUCTURE_50.md` — V0.2 Model-A/Lv31 aligned
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `05_LEGACY_EVIDENCE_MAP.md`
- `06_SIMULATION_CALIBRATION_PLAN.md` — V0.2
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

## Encounter authoring / preflight tranche
- `32_MODEL_A_TIER_ENCOUNTER_AVAILABILITY_V0_1.md`
- `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- `34_MODEL_A_FREQUENCY_RANGE_ENVELOPE_V0_1.md`
- `35_LAYERA0_ENCOUNTER_ENVELOPE_VALIDATION_REPORT_V0_1.md`
- `36_REPRESENTATIVE_RECIPE_STATIC_PREFLIGHT_REPORT_V0_1.md`
- `37_REPRESENTATIVE_RECIPE_KINEMATIC_PREFLIGHT_REPORT_V0_1.md`
- `38_FORMATION_DEPTH_SCHEMA_AMENDMENT_V0_1.md`
- `39_FRONTMOST_DPS_SENSITIVITY_REPORT_V0_1.md`
- `40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`

## Machine-readable data
- `data/model_a_campaign_spine_v0_1.yaml`
- `data/model_a_encounter_envelope_v0_1.yaml`
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_kinematic_anchor_v0_1.yaml`
- `data/model_a_combat_sensitivity_anchor_v0_1.yaml`

## Analysis tools
- `../tools/validate_campaign_spine.py`
- `../tools/validate_encounter_envelope.py`
- `../tools/analyze_representative_recipes.py`
- `../tools/simulate_recipe_kinematics.py`
- `../tools/simulate_frontmost_dps_sensitivity.py`

---

# 7. Formation depth amendment

Current design direction adds a formation-authoring capability equivalent to:
```yaml
spawnXOffset: number|null
```

Purpose:
- create real front/back geometry
- avoid label-only BACK intent
- preserve actual frontmost targeting authority

Current X offsets are simulation candidates only, not production coordinates.

---

# 8. Parked / superseded active candidates

Historical evidence only:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`
- `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Do not resume these as current authority.

---

# 9. Exact next layer

**Class-aware Layer-A combat micro-simulation.**

Required before synthetic Tier slices:
- deterministic action traces
- SKILLED_V2 conservative/central/strong model inputs
- class normal/heavy/P×P behavior
- explicit CURRENT_AUTHORITY / LEGACY_PARITY_CANDIDATE / FUTURE_SKILL_PLACEHOLDER modes
- special capability activation/uptime under real class behavior
- class opportunity/starvation analysis

After Layer-A PASS:
- synthetic Tier slices
- full Tier simulation
- 5-class soft-wall map
- stars-only recovery
- achievement bridge model
- account simulation

---

# 10. Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster coefficients
- exact 200-Stage schedule
- exact EXP formula
- Lv11+ production coefficients
- permanent star reward values
- achievement reward graph/value
- boss cadence/design
- shop cadence/economy
- detailed multiplayer balance

No live gameplay patch is authorized by this corpus tranche.
