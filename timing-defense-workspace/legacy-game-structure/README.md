# Timing Defense — Legacy Game Structure Corpus

Date: 2026-10-22 KST  
Status: **STRUCTURAL CORPUS / SEPARATE FROM LIVE IMPLEMENTATION AUTHORITY**

## 0. 목적

이 자료군은 여러 버전/보고서/시뮬레이션/현재 contract/사용자 확정 의도에 흩어진 게임 전체 구조를 한 곳에서 관리한다.

중요:
- 과거 구현 복원이 목적이 아니다.
- current structure와 legacy evidence를 분리한다.
- candidate numeric은 live authority가 아니다.
- 구현보다 구조/시뮬레이션이 먼저다.

---

# 1. 현재 중심축

최상위 active structure:
`16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

핵심:

```text
Tier × 50 Stage
  × Content Novelty
  × Player Power
  × Meta Progression
```

몬스터/스킬/별/업적 중 하나를 중심으로 두지 않는다.
**Campaign Progression Spine**을 공통 좌표계로 사용한다.

설계 방식은:
`전체를 얕게 정렬 -> dependency 높은 축 확정 -> candidate authoring -> simulation -> spine 보정 -> 더 깊게 진행`.

---

# 2. 근거 상태

- CURRENT_FROZEN_STRUCTURE
- CURRENT_AUTHORITATIVE
- USER_CONFIRMED_STRUCTURE
- DERIVED_INVARIANT
- LEGACY_IMPLEMENTED_REFERENCE
- LEGACY_ANALYSIS_REFERENCE
- DESIGNED_NOT_AUTHORITATIVE
- OPEN_DECISION
- SUPERSEDED

Governance:
`08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`

---

# 3. 사용자 확정 상위 구조

## Class/Tier
- 5개 class
- class별 독립 Tier progression
- 동일 Tier/Stage content는 모든 class 공용
- 1 Tier = 50 Stage

## Stars
- fail 1–19 = 0★
- fail 20–39 = 1★
- fail 40–49 = 2★
- Stage50 clear = 3★
- best result only
- GlobalStarTotal = sum(bestStars)
- stars = broad account-wide permanent growth

## Achievements
- targeted cross-class progression
- class Tier / all-class Tier / pure SOLO AI0 등
- 일부 보상은 source class가 아닌 다른 class 강화
- titles는 기본적으로 display/collection layer

## Class viability
- soft progression wall 허용
- 다른 class stars/achievements로 막힌 class를 다시 밀 수 있어야 함
- hard class lockout 금지

---

# 4. Monster progression 방향

현재 9종 ordinary mechanical foundation은 유지한다.
그러나 **현재 9종은 final lifetime roster가 아니다.**

새 방향:
- T1에서 9종 전체를 강제로 공개하지 않음
- Tier가 올라가며 신규 monster가 등장
- 신규 Tier 진입 자체가 content novelty를 제공
- 기존 monster도 higher Tier에서 새로운 formation/cadence/composition으로 재해석
- future monster 추가 가능성을 data/schema에서 확실히 열어둠
- `monsterCount == 9` 하드코딩 금지
- 신규 capability가 기존 pressure taxonomy에 맞지 않으면 taxonomy version-up 허용

---

# 5. Difficulty direction

User-confirmed calibration rule:

> **일반 Tier는 intended-entry `SKILLED_V2` 기준 full-Tier 3★ clear probability가 기본적으로 60% 미만이어야 한다.**

- 60%는 목표 중앙값이 아니라 상한
- T1은 onboarding 때문에 더 높게 허용 가능
- 개별 Stage 통과율이 아니라 Stage1→50 full-run clear probability
- 과성장 replay account에는 동일 기준을 적용하지 않음
- class별 clear rate 차이는 허용

`SKILLED_V2`도 재정의한다.
- combo 40을 high-mastery-only event로 두지 않음
- 기존 skilled보다 강한 combo maintenance/timing profile 사용
- HIGH_MASTERY_STRESS는 별도 상위 profile

상세:
`06_SIMULATION_CALIBRATION_PLAN.md`

---

# 6. Current document map

Core:
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

Historical / parked candidates:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`
- `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

`09/13/14`는 유효한 분석 아이디어를 보존하지만 **T1에서 9종 전체를 teaching하는 전제 때문에 active continuation 대상이 아니다.**
Master Spine 정립 후 필요한 부분만 재사용한다.

---

# 7. Current master dependency

```text
Core premise
  ↓
MASTER CAMPAIGN PROGRESSION SPINE
  ├─ Tier count / novelty budget
  ├─ monster unlock ladder
  ├─ future monster expansion
  ├─ 50-Stage macro flow
  ├─ run skill/power windows
  ├─ star/meta-power windows
  └─ achievement progression envelope
        ↓
Encounter authoring
        ↓
Run economy / boss / multiplayer
        ↓
Deterministic simulation
        ↓
Spine revision / freeze
        ↓
Live implementation
```

---

# 8. Exact next task

`Master Campaign Matrix`를 만든다.

순서:
1. Tier count 후보 4/5/6 비교
2. Tier별 novelty budget
3. 현재 9종 monster Tier unlock ladder candidate
4. future monster expansion contract
5. Tier별 50-Stage macro flow
6. Tier별 expected run skill-reach window
7. P0 FRESH / P1 BALANCED / P2 STAR_GROWN / P3 ACHIEVEMENT_ASSISTED 정의
8. Tier별 SKILLED_V2 clear target envelope
9. 전체 cross-category static audit
10. 그 뒤 encounter frequency/count/composition/cadence로 재진입

이 단계가 닫히기 전 T1 micro-sim을 더 세밀화하지 않는다.

---

# 9. 현재 하지 않는 것

- final Tier count freeze
- monster unlock exact freeze
- production HP/armor/speed freeze
- exact Stage recipes
- permanent stat coefficients
- achievement exact reward graph/value
- boss cadence
- shop cadence
- Lv11+ live implementation
- 3P/4P detailed expansion
