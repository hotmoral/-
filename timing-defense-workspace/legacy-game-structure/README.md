# Timing Defense — Legacy Game Structure Corpus

Date: 2026-10-22 KST  
Status: **STRUCTURAL CORPUS / SEPARATE FROM LIVE IMPLEMENTATION AUTHORITY**

## 0. 목적

이 디렉터리는 지금까지 여러 버전, 구현 보고서, 시뮬레이션 문서, 현재 canonical contract, 사용자 확정 의도에 흩어져 있던 **게임 전체 구조**를 한 곳에서 관리하기 위한 별도 자료군이다.

이 자료군의 이름은 **레거시 구조자료 (Legacy Game Structure Corpus)** 로 통일한다.

중요:
- 이 자료군은 과거 구현을 그대로 복원하는 문서가 아니다.
- 과거 구현/분석은 근거로 보존하되, 현재 9종 몬스터·50 Stage Tier·직업별 독립 Tier 진행·별 기반 공용 영구 성장 구조에 맞게 재정리한다.
- 이 자료군 자체가 live code patch나 production numeric freeze를 자동 승인하지 않는다.
- 구현보다 먼저 구조를 계산·시뮬레이션하고, 그 결과를 토대로 명시적 decision/freeze 후 적용한다.

## 1. 근거 상태 분류

모든 규칙/수치/구조에는 다음 공통 enum 중 하나를 사용한다.

1. `CURRENT_FROZEN_STRUCTURE`
   - 현재 canonical contract에서 구조가 이미 고정됨.
2. `CURRENT_AUTHORITATIVE`
   - 현재 Cloudflare/server authority 구현까지 존재함.
3. `USER_CONFIRMED_STRUCTURE`
   - 사용자가 직접 확정한 현재 게임 구조 의도. 아직 구현되지 않았을 수 있음.
4. `DERIVED_INVARIANT`
   - 사용자 확정/frozen 구조에서 논리적으로 필수로 따라오는 규칙.
5. `LEGACY_IMPLEMENTED_REFERENCE`
   - 과거 실제 playable 구현에 존재. 현재 production으로 자동 승격하지 않음.
6. `LEGACY_ANALYSIS_REFERENCE`
   - 과거 시뮬레이션/설계 가설. 실험자료로만 보존.
7. `DESIGNED_NOT_AUTHORITATIVE`
   - 명시적인 설계는 있으나 authoritative 구현/최종 freeze가 없음.
8. `OPEN_DECISION`
   - 구조 또는 수치가 아직 결정되지 않음.
9. `SUPERSEDED`
   - 역사적 근거는 남기되 현재 목표 구조에는 사용하지 않음.

상세 우선순위와 교차검토 규칙은 `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`를 따른다.

## 2. 현재 구조의 최상위 그래프

```text
ACCOUNT
  ├─ shared permanent progression
  │    └─ total stars -> automatic permanent stats
  │
  └─ CLASS x5
       └─ independent Tier progression
            └─ TIER
                 ├─ 50 stages
                 ├─ best star result 0..3
                 └─ run attempts
                      ├─ Stage combat
                      ├─ run EXP / level / class skills
                      ├─ run coin / upgrades
                      └─ failure or Tier clear
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

## 3. 현재 사용자 확정 구조

### 직업별 독립 진행
5개 직업은 각각 독립된 Tier 진행 기록을 가진다.

### 한 Tier = 50 Stage
Tier 내 Stage는 1~50으로 구성한다.

### 별 판정
Tier attempt 종료 결과:
- Stage 1~19에서 실패: 0★
- Stage 20~39에서 실패: 1★
- Stage 40~49에서 실패: 2★
- Stage 50 클리어: 3★

### 공용 영구 성장
누적 별 수에 따라 **모든 직업에 적용되는 영구 stat**을 자동 획득한다.
예:
- 5개 직업이 모두 Tier 1을 3★ -> 총 15★.

영구 stat 종류/별 threshold/증가량은 아직 수치 확정하지 않는다.

## 4. 확정 구조에서 파생되는 invariant

### `직업 × Tier` 최대 3★
한 Tier 클리어에서 최대 3★이므로 한 `직업 × Tier` 기록은 0..3 범위다.

### 최고 기록 저장
반복 도전으로 동일 Tier의 별을 계속 더하면 “한 Tier 최대 3★”와 전체 별 성취 구조가 깨진다.
따라서:

```text
bestStars[class][tier] = max(previousBestStars, attemptStars)
```

로 저장한다.
이 항목은 `USER_CONFIRMED_STRUCTURE` 자체가 아니라 그 구조에서 필수로 따라오는 `DERIVED_INVARIANT`로 관리한다.

### GlobalStarTotal

```text
GlobalStarTotal = sum(bestStars[class][tier])
```

별은 소비 currency가 아니라 account achievement 총량이다.

## 5. 현재 encounter 재정립 원칙

기존 `S / E / X` 3분류는 역사적 분석 문법으로 보존하되, 현재 production authoring의 주 분류로 사용하지 않는다.

현재는 9종 ordinary monster capability가 존재하며, 전열 우선 system targeting 때문에 다음 항목을 별도 축으로 관리해야 한다.

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

## 6. 문서 구성

- `01_META_PROGRESSION.md` — 직업별 Tier/별/영구 성장
- `02_TIER_SYSTEM.md` — Tier identity와 Tier progression
- `03_STAGE_STRUCTURE_50.md` — 50 Stage pacing과 Stage authoring
- `04_MONSTER_ENCOUNTER_MODEL.md` — 9종 몬스터 조합/빈도/배치/주기 체계
- `05_LEGACY_EVIDENCE_MAP.md` — 과거/현재 근거의 상태 분류
- `06_SIMULATION_CALIBRATION_PLAN.md` — 적용 전 계산·시뮬레이션 절차
- `07_AUTHORING_DATA_SCHEMA.md` — Tier/Stage/Encounter 데이터를 저장할 공통 schema
- `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md` — 모든 구조 변경의 정합성/모순/범위 검토 규칙
- `09_TIER_LADDER_CANDIDATE_V0_1.md` — 5-Tier 첫 simulation spine과 신규 Tier identity candidate

## 7. 작업 원칙

1. 구조와 수치를 분리한다.
2. legacy 구현값을 production 값으로 자동 승격하지 않는다.
3. 신규 수치는 먼저 authoring data / simulator에서만 사용한다.
4. 9종 몬스터 capability contract는 존중한다.
5. manual target selection을 암묵적으로 가정하지 않는다.
6. 직업별 역할 차이는 유지하되 hard class lockout은 금지한다.
7. 2/3/4-player scaling은 단순 global HP 배율보다 encounter composition/cadence로 우선 해결한다.
8. 모든 Tier/Stage 구조는 deterministic simulation으로 검증한다.
9. 결과를 보고한 뒤 명시적으로 freeze된 항목만 live 구현으로 이동한다.
10. 후행 계층이 선행 계층의 구조를 편의상 바꾸지 않는다.
11. 불필요한 반복 검토와 범위 확장을 피하되, dependency가 연결된 항목은 반드시 함께 검토한다.

## 8. 현재 active structural candidate

`09_TIER_LADDER_CANDIDATE_V0_1.md`는 첫 full-campaign simulation을 위한 **5-Tier bounded candidate**다.

이것은 final Tier count freeze가 아니다.
Tier 수 `T`에 대해:

```text
minimum successful class-stage volume = 250T
maximum stars = 15T
```

이므로 4/5/6+ Tier를 최종 결정할 때 총 play volume과 permanent progression을 함께 비교한다.

Candidate V0.1의 핵심 방향:
- T1 Stage 1~29에서 9종 ordinary vocabulary teaching 완료
- T2 frontline/breakthrough
- T3 tempo/population shift
- T4 formation/objective pressure
- T5 mastery/contrast
- higher Tier를 constant chaos로 만들지 않음

## 9. 현재 하지 않는 것

- production HP/armor/speed 수치 확정
- 영구 stat 별 threshold/증가량 확정
- final Tier 개수/명칭 확정
- final 50-stage schedule freeze
- exact monster frequency/count/cadence freeze
- boss cadence freeze
- live gameplay patch

## 10. 다음 단계

1. 첫 cross-document mismatch를 schema에 반영
2. T1 monster introduction exact candidate 작성
3. encounter archetype complexity tagging
4. T1~T5 qualitative frequency envelope를 exact **simulation candidate** count로 변환
5. 50-stage signature skeleton 생성
6. static consistency/repetition/class-opportunity 검사
7. micro simulation -> synthetic slice -> full T1 simulation
8. 결과 보고/decision 후에만 다음 freeze 단계로 이동
