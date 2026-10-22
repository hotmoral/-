# Timing Defense — Legacy Game Structure Corpus

Date: 2026-10-22 KST  
Status: **STRUCTURAL CORPUS / SEPARATE FROM LIVE IMPLEMENTATION AUTHORITY**

## 0. 목적

이 디렉터리는 지금까지 여러 버전, 구현 보고서, 시뮬레이션 문서, 현재 canonical contract, 사용자 확정 의도에 흩어져 있던 **게임 전체 구조**를 한 곳에서 관리하기 위한 별도 자료군이다.

이 자료군의 이름은 **레거시 구조자료 (Legacy Game Structure Corpus)** 로 통일한다.

중요:
- 과거 구현을 그대로 복원하는 문서가 아니다.
- 과거 구현/분석은 근거로 보존하되, 현재 9종 몬스터·50 Stage Tier·직업별 독립 Tier 진행·별/업적 기반 교차 영구 성장 구조에 맞게 재정리한다.
- 이 자료군 자체가 live code patch나 production numeric freeze를 자동 승인하지 않는다.
- 구현보다 먼저 구조를 계산·시뮬레이션하고, 결과를 토대로 명시적 decision/freeze 후 적용한다.

---

# 1. 근거 상태 분류

모든 규칙/수치/구조에는 다음 공통 enum 중 하나를 사용한다.

1. `CURRENT_FROZEN_STRUCTURE`
2. `CURRENT_AUTHORITATIVE`
3. `USER_CONFIRMED_STRUCTURE`
4. `DERIVED_INVARIANT`
5. `LEGACY_IMPLEMENTED_REFERENCE`
6. `LEGACY_ANALYSIS_REFERENCE`
7. `DESIGNED_NOT_AUTHORITATIVE`
8. `OPEN_DECISION`
9. `SUPERSEDED`

상세 우선순위와 교차검토 규칙은 `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`를 따른다.

---

# 2. 현재 구조의 최상위 그래프

```text
ACCOUNT
  ├─ broad permanent progression
  │    └─ total stars -> automatic account-wide stats
  │
  ├─ targeted permanent progression
  │    └─ achievements -> account/class-specific reward edges
  │
  ├─ titles / presentation
  │    └─ achievement display/collection layer
  │
  └─ CLASS x5
       └─ independent Tier progression
            └─ TIER
                 ├─ shared 50-stage content
                 ├─ class-specific best star result 0..3
                 └─ run attempts
                      ├─ Stage combat
                      ├─ run EXP / level / class skills
                      ├─ run coin / upgrades
                      └─ failure or Tier clear
```

의도된 장기 progression loop:

```text
Class A blocked
 -> progress B/C/D
 -> gain stars + achievements
 -> broad + targeted permanent power
 -> return to A
 -> previous soft wall becomes attainable
```

전투 authoring 그래프:

```text
Tier identity
 -> Stage band/pacing
 -> Encounter archetype
 -> Monster composition
 -> Formation/frontline order
 -> Spawn cadence
 -> Geometry
 -> Active-count/readability envelope
 -> Target-order interaction
 -> Class opportunity
```

---

# 3. 현재 사용자 확정 구조

## 직업별 독립 진행
5개 직업은 각각 독립된 Tier 진행 기록을 가진다.

## 공통 Stage content
같은 Tier의 Stage 구성은 직업에 따라 따로 만들지 않는 방향을 기본으로 한다.
동일한 encounter를 서로 다른 class kit/영구성장 상태로 통과한다.

## 한 Tier = 50 Stage
Tier 내 Stage는 1~50으로 구성한다.

## 별 판정
- Stage 1~19에서 실패: 0★
- Stage 20~39에서 실패: 1★
- Stage 40~49에서 실패: 2★
- Stage 50 클리어: 3★

## 별 기반 공용 영구 성장
누적 별 수에 따라 **모든 직업에 적용되는 영구 stat**을 자동 획득한다.
예:
- 5개 직업이 모두 Tier 1을 3★ -> 총 15★.

## 업적/칭호 기반 교차 성장
향후:
- 직업별 Tier 달성 업적
- 전 직업 Tier 달성 업적
- 특정 직업 AI 없이 순수 SOLO Tier clear 업적
- 일부 업적은 source class가 아닌 **다른 직업의 특정 stat**을 영구 강화

이 시스템의 목적은 한 직업의 숙련이 다른 직업의 Tier 진행 기반으로 이어지게 하는 것이다.

정확한 achievement list / class-to-class mapping / stat/value는 아직 freeze하지 않는다.

---

# 4. 확정 구조에서 파생되는 invariant

## `직업 × Tier` 최대 3★
한 `직업 × Tier` 기록은 0..3 범위다.

## 최고 기록 저장

```text
bestStars[class][tier] = max(previousBestStars, attemptStars)
```

## GlobalStarTotal

```text
GlobalStarTotal = sum(bestStars[class][tier])
```

별은 소비 currency가 아니라 account achievement 총량이다.

## Hard class lockout 금지 / soft wall 허용
신규 계정에서 어떤 직업이 같은 Tier를 상대적으로 더 어렵게 느끼는 것은 허용한다.
다른 직업 progression과 permanent growth를 통해 나중에 돌파하는 것이 의도된 구조다.

그러나 특정 class가 mechanic상 절대 진행할 수 없는 hard lockout은 금지한다.

---

# 5. 현재 encounter 재정립 원칙

기존 `S / E / X` 3분류는 역사적 분석 문법으로 보존하되 production authoring 주 분류로 사용하지 않는다.

현재는 9종 ordinary monster capability가 존재하며, 전열 우선 system targeting 때문에 다음 항목을 별도 축으로 관리한다.

- pressure family
- encounter archetype
- monster type frequency
- monster count
- composition
- formation / frontline order
- spawn cadence
- geometry
- active concurrency
- target-order transition
- backline uptime

세부 정의는 `04_MONSTER_ENCOUNTER_MODEL.md`에 둔다.

---

# 6. 문서 구성

- `01_META_PROGRESSION.md` — 직업별 Tier/별/교차 영구 성장
- `02_TIER_SYSTEM.md` — Tier identity와 Tier progression
- `03_STAGE_STRUCTURE_50.md` — 50 Stage pacing과 Stage authoring
- `04_MONSTER_ENCOUNTER_MODEL.md` — 9종 몬스터 조합/빈도/배치/주기 체계
- `05_LEGACY_EVIDENCE_MAP.md` — 과거/현재 근거의 상태 분류
- `06_SIMULATION_CALIBRATION_PLAN.md` — 적용 전 계산·시뮬레이션 절차
- `07_AUTHORING_DATA_SCHEMA.md` — Tier/Stage/Encounter/Meta/Achievement 공통 schema
- `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md` — 구조 변경의 정합성/모순/범위 검토 규칙
- `09_TIER_LADDER_CANDIDATE_V0_1.md` — 5-Tier 첫 simulation spine
- `10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md` — encounter complexity 정의
- `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md` — 최초 T1 skeleton, history
- `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md` — V0.1 정적 감사
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md` — 현재 T1 structural candidate
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md` — 현재 T1 2P count/cadence simulation envelope
- `15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md` — 업적/칭호/직업 간 영구성장 구조

---

# 7. 작업 원칙

1. 구조와 수치를 분리한다.
2. legacy 구현값을 production 값으로 자동 승격하지 않는다.
3. 신규 수치는 먼저 authoring data / simulator에서만 사용한다.
4. 9종 몬스터 capability contract는 존중한다.
5. manual target selection을 암묵적으로 가정하지 않는다.
6. 직업별 역할 차이는 유지하고 soft wall은 허용하되 hard class lockout은 금지한다.
7. 별과 achievement를 따로 튜닝한 뒤 단순 합산하지 않고 combined account simulation으로 검증한다.
8. achievement reward graph의 순환 deadlock / dominant route / runaway snowball을 검사한다.
9. 2/3/4-player scaling은 단순 global HP 배율보다 encounter composition/cadence로 우선 해결한다.
10. 모든 Tier/Stage 구조는 deterministic simulation으로 검증한다.
11. 결과를 보고한 뒤 명시적으로 freeze된 항목만 live 구현으로 이동한다.
12. 후행 계층이 선행 계층의 구조를 편의상 바꾸지 않는다.
13. 불필요한 반복 검토와 범위 확장을 피하되 dependency가 연결된 항목은 반드시 함께 검토한다.

---

# 8. 현재 active structural candidates

## Tier ladder
`09_TIER_LADDER_CANDIDATE_V0_1.md`는 첫 full-campaign simulation을 위한 **5-Tier bounded candidate**다.
Final Tier count freeze가 아니다.

Tier 수 `T`에 대해:

```text
minimum successful class-stage volume = 250T
maximum stars = 15T
```

## T1 Stage skeleton
현재 active structural candidate:
`13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`

## T1 2P authoring envelope
현재 active 2P candidate:
`14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

## Achievement layer
현재 structural candidate:
`15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`

숫자 reward는 아직 비워둔다.
먼저 T1/Tier simulation으로 실제 soft wall과 class sensitivity를 찾은 뒤 reward edge를 배치한다.

---

# 9. 현재 하지 않는 것

- production HP/armor/speed 수치 확정
- 영구 stat 별 threshold/증가량 확정
- achievement exact reward amount 확정
- sourceClass -> targetClass reward mapping freeze
- final title list/name freeze
- final Tier 개수/명칭 확정
- final 50-stage schedule freeze
- exact monster frequency/count/cadence freeze
- boss cadence freeze
- live gameplay patch

---

# 10. 다음 단계

1. T1 2P encounter micro-simulation input 구체화
2. formation/cadence/intensity 조합 정적 검사
3. 9종 target-order/screening micro-simulation
4. 10-stage synthetic slice
5. full T1 50-stage simulation
6. **5-class viability / soft-wall map 생성**
7. star-only progression으로 recovery 정도 측정
8. 관측된 gap에 achievement reward graph 후보 배치
9. stars + achievements combined account simulation
10. 2/3/4-player 확장
11. 결과 보고/decision 후에만 freeze
