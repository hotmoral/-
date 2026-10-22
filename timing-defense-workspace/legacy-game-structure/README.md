# Timing Defense — Legacy Game Structure Corpus

Date: 2026-10-22 KST  
Status: **STRUCTURAL CORPUS / MODEL A ADMITTED FOR BOUNDED SIMULATION**

## 0. 목적

이 자료군은 게임 전체 campaign/meta/combat 구조를 live 구현보다 먼저 정립하고 검증하기 위한 canonical planning corpus다.

핵심:
- 과거 구현 복원이 목적이 아니다.
- candidate와 production authority를 분리한다.
- 상위 구조를 먼저 닫고, deterministic simulation으로 검증한 뒤에만 수치/구현을 승격한다.

---

# 1. 현재 중심축

최상위 원칙:
`16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

현재 active integrated matrix:
`31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

공통 좌표:
```text
Tier × Stage1..50 × Content Novelty × Player Power × Meta Progression
```

설계 방식:
```text
shallow whole-campaign alignment
 -> upstream dependency closure
 -> candidate authoring
 -> machine/static validation
 -> deterministic simulation
 -> spine revision
 -> explicit freeze
 -> live implementation
```

---

# 2. 현재 user-confirmed 구조

- 5 classes, class별 independent Tier progress
- 동일 Tier/Stage content는 모든 class 공용
- 1 Tier = 50 Stage
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★
- stars = broad account permanent growth
- achievements = targeted cross-class growth
- recoverable soft wall 허용
- hard class lockout 금지
- 현재 9 monsters는 lifetime final roster가 아님
- T1에서 9종 전체 공개 금지 방향
- higher Tier에서 신규 monster 등장
- future monster/Tier expansion open
- non-T1 intended-entry SKILLED_V2 full-clear <60%
- combo40 = skilled-achievable, not extreme-only
- **Lv31 target unlock window = Stage41–45**
- Stage46–49 = post-Lv31 mastery-use band
- Stage50 = already-familiar Lv31을 사용하는 final

---

# 3. Current Model A

Status:
**default bounded simulation spine / NOT production freeze**

```text
T1: GRUNT / RUNNER / BRUTE
T2: +SHIELD / +FLYER
T3: +CHARGER / +SPLITTER
T4: +SUPPORTER / +SIEGER
T5+: future expansion
```

Model B fallback:
- T4 +SUPPORTER
- T5 +SIEGER

Use Model B only if lower-layer evidence shows Model A T4 cannot remain readable/stable.

---

# 4. Current player-power spine candidate

- Lv6: Stage5–7
- Lv11: 11–14
- Lv16: 18–21
- Lv21: 25–28
- Lv26: 32–36
- Lv31: **41–45**

Only Lv31 target window is user-confirmed here.
Other windows remain simulation candidates.

Late grammar:
```text
31–39 pressure / soft wall
40     2★ gate
41–45  Lv31 Ascension
46–49  Post-Lv31 Mastery
50     Tier Final
```

---

# 5. Current validation status

Machine-readable data:
`data/model_a_campaign_spine_v0_1.yaml`

Validator:
`../tools/validate_campaign_spine.py`

Report:
`30_LAYER0_MODEL_A_VALIDATION_REPORT_V0_1.md`

Current result:
```text
RESULT=PASS errors=0 warnings=0
```

Meaning:
- Model A may proceed to bounded simulation authoring.
- It is not final campaign freeze.

---

# 6. Active document map

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

## Current Master Campaign tranche
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
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md` — **current integrated authority for bounded simulation**

## Machine-readable
- `data/model_a_campaign_spine_v0_1.yaml`
- `../tools/validate_campaign_spine.py`

---

# 7. Parked / historical candidates

Do not continue as active authority:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`
- `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Reason:
- 09/13/14 assumed T1-all-9.
- 17 is superseded for active planning by Matrix V0.2 after the large static/Layer-0 audit tranche.

Historical analysis may still be reused where compatible.

---

# 8. Exact next layer

The Master Campaign Spine is sufficiently closed for bounded simulation authoring.

Next order:
1. Tier-specific encounter archetype availability
2. pressure envelope -> candidate frequency bands/count ranges
3. Tier formation/cadence availability
4. deterministic encounter recipe candidates
5. Layer-A micro simulation
6. synthetic slices
7. full Tier simulation
8. 5-class soft-wall map
9. stars-only recovery
10. achievement bridge model
11. account progression simulation

---

# 9. Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster HP/speed/armor/etc
- exact monster Stage recipe
- exact EXP formula
- Lv11+ production coefficients
- permanent star reward values
- achievement reward graph/value
- boss cadence/design
- shop cadence/economy
- multiplayer progression policy

No live gameplay patch is authorized by this corpus tranche.
