# Timing Defense — Tier System Structure

Date: 2026-10-22 KST  
Status: **STRUCTURAL FOUNDATION / MASTER-SPINE ALIGNED / FINAL TIER IDENTITIES AND NUMBERS OPEN**

## 1. Tier의 역할

Tier는 단순 수치 난이도 단계가 아니다.
각 Tier는 50개의 Stage를 통해 서로 다른 전투 문제와 새로운 콘텐츠를 학습·혼합·강화하는 **campaign unit**이다.

상위 기준:
`16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

한 Tier가 정의해야 하는 최소 항목:
- identity / tactical theme
- novelty budget
- new monster introductions
- returning monster reinterpretation
- 50-stage difficulty curve
- monster availability
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
- expected meta-power state
- expected coin/shop growth
- 0★/1★/2★/3★ outcome distribution
- skilled full-clear target envelope

## 2. Tier와 직업 progression

Tier 진행은 직업별 독립이다.

```text
Class A -> T1 -> T2 -> T3 ...
Class B -> T1 -> T2 -> T3 ...
```

같은 Tier/Stage authoring data는 모든 class가 공유한다.
한 직업에서 얻은 Tier clear 자체가 다른 직업의 Tier clear를 대체하지 않는다.

다만:
- stars는 broad account permanent growth를 제공하고,
- achievements는 targeted cross-class growth를 제공한다.

따라서 같은 Tier라도 class kit와 account progression state에 따라 체감 난도가 달라질 수 있다.
이 class asymmetry는 의도될 수 있으나 hard lockout은 금지한다.

## 3. Tier 공통 길이

현재 구조 기준:
- 1 Tier = 50 Stage
- Stage 1~19 실패 = 0★
- Stage 20~39 실패 = 1★
- Stage 40~49 실패 = 2★
- Stage 50 clear = 3★

20 / 40 / 50은 reward anchor다.
Stage design band와 reward band는 분리해서 관리한다.

## 4. Tier difficulty는 여러 축으로 구성

난이도를 global HP/count 증가 하나로 표현하지 않는다.

### Population
- 총 spawn 수
- short-window burst
- active concurrency
- SPLITTER child 포함 effective entity volume

### Durability
- BRUTE raw HP pressure
- SHIELD mitigation
- 제한적 hardened package

### Tempo
- RUNNER sustained speed
- CHARGER burst
- spawn interval
- overlap

### Geometry
- line / cluster / scatter / split
- FLYER Y geometry

### Formation / Target Order
- frontline screen
- backline exposure
- target reorder
- SUPPORTER/SIEGER protection time

### Special State Complexity
- charge
- split
- aura
- siege cycle
- state overlap

### Objective Pressure
- wall contact
- ranged siege
- control/knockback importance

### Player-power context
- run level / skill reach
- star permanent stats
- achievement targeted modifiers

## 5. 기존 T1~T5 자료 취급

기존 `TIER_PRESSURE_GRAMMAR_V1.md`와 옛 T1~T5는 `LEGACY_ANALYSIS_REFERENCE`다.

유효 아이디어:
- Tier identity 필요
- 모든 Stage를 복합 chaos로 만들지 않음
- geometry/timing/pressure 비율로 Tier를 구분
- higher Tier != every Stage maximum complexity

현재 재작성 대상:
- S/E/X 3분류
- 5종 roster 기반 recipe
- exact prototype distribution/name/count/order

## 6. Monster introduction 정책 — 변경된 상위 방향

### 6.1 T1에서 9종 전체를 소진하지 않는다

현재 사용자 확정 방향:

> Tier가 올라갈수록 새로운 monster type이 등장해야 하며, 신규 Tier 진입 자체가 새로운 전투 콘텐츠를 제공해야 한다.

따라서 기존 candidate의 `T1에서 9종 ordinary를 모두 teaching` 원칙은 active direction이 아니다.

T1은 제한된 subset으로 시작한다.
Higher Tier에서 새로운 monster를 도입한다.
정확한 unlock ladder는 Master Campaign Matrix에서 결정한다.

### 6.2 Monster 하나의 도입 단계

각 monster는 최소 다음 lifecycle을 가진다.

```text
first available Tier
 -> first appearance / teach
 -> first mixed use
 -> first high-pressure use
 -> later-Tier reinterpretation
```

필드:
- firstAvailableTier
- firstTeachStage
- firstMixedStage
- firstHighPressureStage
- laterTierRoleTags
- targetFrequencyByBand

### 6.3 Future roster expansion

현재 9종은 final lifetime roster가 아니다.

구조 요구사항:
- `monsterCount == 9` 하드코딩 금지
- Tier data는 monsterId registry reference 사용
- 신규 monster 추가 시 기존 Tier까지 강제 수정할 필요가 없는 구조
- 새 capability가 기존 pressure taxonomy에 맞지 않으면 taxonomy version-up 허용
- future Tier/new campaign extension을 위한 availability slot 유지

## 7. Tier identity 작성 방식

```text
TierProfile
  identity
  noveltyBudget
  introducedMonsterIds[]
  availableMonsterIds[]
  returningMonsterIds[]
  primaryPressureFamilies[]
  secondaryPressureFamilies[]
  encounterFrequencyTargets{}
  formationTargets{}
  cadenceProfile
  stageMacroFlow{}
  expectedRunPowerWindow{}
  expectedMetaPowerWindow{}
  skilledClearTarget{}
  teamScalingPolicy{}
```

Tier identity는 `적 HP +N%`가 아니라:
- 무엇이 처음 등장하는가
- 기존 monster를 어떻게 새롭게 조합하는가
- 어떤 판단을 요구하는가
- player power가 어느 구간에 있는가
로 설명 가능해야 한다.

## 8. Tier별 빈도 설계

몬스터 빈도는 한 종류의 `%`만 보지 않는다.

최소:
- spawn share
- Stage presence
- meaningful threat presence
- threat-time/capability uptime

SIEGER/SUPPORTER 같은 type은 spawn share보다 uptime이 더 중요할 수 있다.

Exact frequency는 monster availability ladder와 Tier novelty budget이 먼저 닫힌 뒤 작성한다.

## 9. Difficulty / clear-rate calibration

사용자 확정 방향:

> Tier1을 제외한 일반 campaign Tier는 **숙련자 full-Tier clear probability가 기본적으로 60% 미만**이어야 한다.

해석:
- 60%는 목표값이 아니라 상한 기준
- 개별 Stage clear rate가 아니라 Stage1→50 Tier attempt clear probability
- 해당 Tier의 `intended-entry progression state`에서 측정
- 과성장 replay account에는 적용하지 않음
- class별 clear rate는 달라도 됨
- 특정 class는 soft wall 때문에 훨씬 낮을 수 있음

Tier1은 onboarding 역할 때문에 더 높은 skilled clear rate를 허용할 수 있다.
Exact T1 target은 OPEN.

숙련자 profile 자체도 재정의해야 한다.
`combo 40`을 high-mastery-only event로 취급하지 않는 `SKILLED_V2`가 필요하다.

## 10. Tier progression과 별 분포

각 Tier / class / mastery / meta-power profile에서 측정:
- fail 1~19 = 0★
- fail 20~39 = 1★
- fail 40~49 = 2★
- clear 50 = 3★

질문:
- 1★가 progression seed 역할을 하는가?
- 2★가 의미 있는 숙련 성취인가?
- 3★가 실제 mastery/growth를 요구하는가?
- 막힌 class가 다른 class stars/achievements 이후 회복되는가?
- 한 route만 압도적인 정답이 되지 않는가?

## 11. Boss / checkpoint — OPEN_DECISION

결정 필요:
- boss 빈도
- 10/20/30/40/50과 boss 관계
- Stage50 final boss 여부
- boss가 Tier novelty를 어떻게 강화하는지

Boss cadence는 Master Campaign Spine과 Tier macro flow 이후 결정한다.

## 12. 현재 작업 순서

1. Tier count 4/5/6 비교
2. Tier별 novelty budget
3. 9종 현재 roster의 unlock ladder candidate
4. future monster expansion contract
5. Tier별 50-Stage macro flow
6. expected run skill-reach window
7. expected meta-power states P0/P1/P2/P3
8. skilled clear-rate envelope
9. cross-document matrix audit
10. 이후 monster frequency/count/composition/cadence
11. deterministic simulation
12. explicit production freeze
