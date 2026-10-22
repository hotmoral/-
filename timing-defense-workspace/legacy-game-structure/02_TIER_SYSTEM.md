# Timing Defense — Tier System Structure

Date: 2026-10-22 KST  
Status: **STRUCTURAL FOUNDATION / FINAL TIER IDENTITIES AND NUMBERS OPEN**

## 1. Tier의 역할

Tier는 단순 수치 난이도 단계가 아니다.
각 Tier는 50개의 Stage를 통해 서로 다른 전투 문제를 학습·혼합·강화하는 **campaign unit**이다.

한 Tier가 정의해야 하는 최소 항목:
- identity / tactical theme
- 50-stage difficulty curve
- monster introduction/availability
- monster-type frequency targets
- encounter-archetype frequency targets
- composition complexity
- formation/frontline policy
- spawn cadence profile
- geometry distribution
- active-count/readability envelope
- boss/checkpoint policy
- 2/3/4-player scaling policy
- expected run EXP/skill reach
- expected coin/shop growth
- 0★/1★/2★/3★ outcome distribution

## 2. Tier와 직업 progression

Tier 진행은 직업별 독립이다.

```text
Class A -> T1 -> T2 -> T3 ...
Class B -> T1 -> T2 -> T3 ...
```

한 직업에서 얻은 Tier clear 자체가 다른 직업의 Tier clear를 대체하지 않는다.
단, 별에서 얻은 account-wide permanent stats는 모든 직업에 공유된다.

따라서 Tier 난이도는 두 축을 동시에 고려해야 한다.
- 해당 직업의 자체 Tier 경험/실력
- 계정 전체에서 이미 획득한 permanent progression

## 3. Tier 공통 길이

현재 구조 기준:
- 1 Tier = 50 Stage
- Stage 20~39 실패 = 1★
- Stage 40~49 실패 = 2★
- Stage 50 clear = 3★

이 때문에 Stage 20 / 40 / 50은 단순 번호가 아니라 Tier pacing의 구조적 anchor다.

## 4. Tier difficulty는 여러 축으로 구성

난이도를 global HP/count 증가 하나로 표현하지 않는다.

### 축 A — Population
- 총 spawn 수
- short-window burst 수
- active concurrency
- SPLITTER child 포함 실제 entity volume

### 축 B — Durability
- BRUTE raw HP pressure
- SHIELD mitigation
- hardened/elite package의 제한적 사용

### 축 C — Tempo
- RUNNER 지속 속도
- CHARGER windup/charge
- spawn interval
- overlap 빈도

### 축 D — Geometry
- line
- cluster
- scatter
- split
- FLYER vertical movement

### 축 E — Formation / Target Order
- frontline screen 강도
- backline exposure까지 걸리는 시간
- SHIELD/BRUTE가 SUPPORTER/SIEGER를 가리는 시간
- 타겟 순서가 바뀌는 빈도

### 축 F — Special State Complexity
- charge timing
- split-on-death
- support aura
- siege cycle
- 여러 stateful capability의 결합

### 축 G — Objective Pressure
- wall contact pressure
- SIEGER ranged wall pressure
- team defense/knockback 중요도

## 5. 기존 T1~T5 자료의 취급

기존 `TIER_PRESSURE_GRAMMAR_V1.md`의 T1 Foundations / T2 Breakers / T3 Rushline / T4 Crossfire / T5 Extremes는 **LEGACY_ANALYSIS_REFERENCE**로 보존한다.

그 자료가 제공하는 유효한 아이디어:
- Tier마다 다른 identity가 필요함
- 모든 Stage를 복합 패턴으로 만들지 않음
- 타이밍 위치/geometry/압력 비율로 Tier 체감을 구분함
- 높은 Tier가 반드시 더 많은 pattern을 동시에 써야 하는 것은 아님

그러나 다음은 현재 기준으로 재작성 필요:
- S/E/X 3분류
- 당시 5종 monster roster 기반 조합
- exact prototype distribution
- exact prototype tier names/order/count

따라서 기존 T1~T5는 production blueprint가 아니라 **비교용 prototype hypothesis**다.

## 6. 새로운 Tier identity 작성 방식

각 Tier는 다음과 같은 profile을 가진다.

```text
TierProfile
  identity
  primaryPressureFamilies[]
  secondaryPressureFamilies[]
  monsterAvailability[]
  monsterFrequencyTargets{}
  encounterFrequencyTargets{}
  formationTargets{}
  cadenceProfile
  overlapProfile
  stageBandTargets{}
  teamScalingPolicy{}
```

Tier identity는 “적 HP +N%”가 아니라 다음 문장으로 설명 가능해야 한다.

예시 형식:
- 초반에는 단순 전열과 속공을 읽게 하고 후반에 SHIELD screen을 도입한다.
- 지속적으로 빠른 전선 이동을 강조하고 CHARGER를 드문 burst threat로 사용한다.
- SUPPORTER/SIEGER를 보호하는 formation을 늘려 전열 제거 속도와 관통/AoE 가치가 중요해진다.

위 문장은 형식 예시이며 final Tier 확정안이 아니다.

## 7. Monster introduction 정책

모든 9종을 Tier 1 Stage 1부터 동시에 사용하지 않는다.

각 monster에는 최소 다음 필드를 둔다.
- firstTeachStage
- firstMixedStage
- firstHighPressureStage
- targetFrequencyByBand

새 capability의 도입 순서는 숫자보다 **인지 부하**를 기준으로 설계한다.

예:
1. 단독/단순 조합으로 mechanic 소개
2. 기존 baseline과 함께 사용
3. 다른 special과 결합
4. late-band에서 높은 압력으로 사용

정확한 도입 Stage는 시뮬레이션/authoring 단계에서 결정한다.

## 8. Tier별 빈도 설계

몬스터 빈도는 한 종류의 `%`만 보지 않는다.

각 Tier에서 최소 세 가지를 별도로 계산한다.

### Spawn share
전체 authored spawn 중 해당 type이 차지하는 비율.

### Encounter presence
50개 Stage 중 해당 type이 의미 있는 encounter component로 등장하는 Stage 비율.

### Threat-time share
해당 type/capability가 실제 전투에서 위협 상태로 존재하는 시간 비율.

예를 들어 SIEGER는 spawn share가 낮아도 backline uptime이 길면 threat-time share가 높을 수 있다.
SUPPORTER도 개체 수보다 aura uptime이 중요하다.

## 9. Tier progression과 별 분포 목표

최종 calibration은 단순 clear rate만 보지 않는다.

각 Tier/직업/skill profile에 대해:
- fail 1~19
- fail 20~39 -> 1★
- fail 40~49 -> 2★
- clear 50 -> 3★

분포를 측정한다.

Tier는 20/40/50 boundary를 이용해 다음 질문에 답할 수 있어야 한다.
- 평균 플레이어가 적어도 1★에 도달할 수 있는가?
- 2★는 충분히 의미 있는 숙련 성취인가?
- 3★는 단순 반복 grind가 아니라 실제 mastery/성장 결과인가?
- permanent stars가 쌓였을 때 이전 Tier가 지나치게 무력화되지 않는가?

정확한 목표 확률은 아직 freeze하지 않는다.

## 10. Boss / checkpoint — OPEN_DECISION

기존 10-stage prototype은 Stage 5/10 boss를 사용했다.
50-stage 구조에서는 그대로 복제하지 않는다.

결정해야 할 것:
- boss 빈도
- 10/20/30/40/50 checkpoint와 boss의 관계
- Stage 50 final boss 여부
- boss가 ordinary capability를 조합하는 방식

Boss는 9종 ordinary roster와 별도 layer라는 현재 contract를 유지한다.

## 11. 다음 작업

Tier system 다음 단계는:
1. Stage 1~50 band structure 확정
2. 9종 monster pressure taxonomy 확정
3. encounter archetype library 작성
4. 각 Tier의 monster/encounter frequency candidate 생성
5. deterministic simulation
6. star outcome / permanent progression feedback 검토
7. explicit production freeze
