# Timing Defense — Master Campaign Progression Spine V0.1

Date: 2026-10-22 KST  
Status: **USER-CONFIRMED DIRECTION + STRUCTURAL MASTER CANDIDATE / NO NUMERICAL FREEZE**

---

# 0. 목적

Timing Defense의 전체 구조를 설계할 때 무엇을 중심축으로 삼고 어떤 순서로 결정할지 정의한다.

핵심 결론:

> 몬스터 / 스킬 / 별 / 업적 중 하나를 중심으로 두지 않는다.  
> **Tier × 50 Stage를 시간축으로 한 Campaign Progression Spine**을 공통 좌표계로 두고, 모든 전투·성장·메타 시스템을 그 위에 정렬한다.

중심 질문:

> 플레이어가 전체 캠페인의 어느 Tier / 어느 Stage 구간에 있고, 그 시점에 무엇을 새로 경험하며, 어느 정도의 전투력을 갖고 있어야 하는가?

공통 좌표:

```text
Tier
  × Stage 1..50
  × Content Novelty
  × Player Power
  × Meta Progression
```

이 문서는 기존 T1 세부 authoring보다 상위 계층이다.

---

# 1. 이미 고정된 상위 본질

현재 구조에서 변경 대상으로 보지 않는 항목:

- 5 classes: Knight / Rogue / Tank / Archer / Mage
- class별 독립 Tier progression
- 같은 Tier/Stage combat content는 모든 class가 공유
- 1 Tier = 50 Stage
- fail Stage1–19 = 0★
- fail Stage20–39 = 1★
- fail Stage40–49 = 2★
- clear Stage50 = 3★
- stars = broad account-wide permanent progression
- achievements = targeted cross-class progression
- run은 Lv1에서 시작
- timing/EXP 기반 run level progression
- class skill milestones 존재
- system-driven/frontmost target acquisition
- hard class lockout 금지
- soft progression wall 허용
- 다른 class progression으로 막힌 class를 다시 밀 수 있어야 함

---

# 2. 설계 방식 — waterfall도, 무질서한 동시설계도 금지

모든 시스템을 하나씩 완전히 닫고 다음으로 가는 순수 waterfall은 사용하지 않는다.
서로 순환 의존성이 있기 때문이다.

반대로 monster / skill / star / achievement를 동시에 세부 수치까지 만드는 것도 금지한다.
상위 전제가 바뀌면 하위 정밀작업이 폐기되기 때문이다.

사용할 방식:

```text
1. 전체 캠페인을 얕게 정렬
2. dependency가 높은 축부터 구조 확정
3. 하위 authoring candidate 생성
4. deterministic simulation
5. 상위 spine 보정
6. 다시 한 단계 깊게 내려감
```

즉 **progressive deepening / iterative convergence** 방식으로 간다.

---

# 3. Layer A — Campaign Spine

가장 먼저 정립할 중심 계층이다.

각 Tier마다 최소 다음을 정의한다.

```text
Tier
  purpose
  noveltyBudget
  newMonsterIntroductions
  existingMonsterReinterpretation
  primaryCombatQuestions
  50StageMacroFlow
  expectedRunPowerWindow
  expectedMetaPowerWindow
  softWallIntent
  bossPlaceholder
  multiplayerPlaceholder
```

이 단계에서는 exact monster count / HP / spawn ms를 정하지 않는다.

---

# 4. Tier count는 별도 상위 결정

Tier 수는 단순 content count가 아니다.

Tier 수 = T일 때:

```text
successful class-stage volume floor = 5 classes × T × 50 = 250T
max stars = 5 classes × T × 3 = 15T
```

따라서 Tier count는 동시에 다음을 결정한다.

- campaign total length
- max star count
- permanent stat ladder length
- achievement volume
- monster introduction pacing
- skill progression/repetition burden
- later content expansion room

초기 비교 후보:
- 4 Tier
- 5 Tier
- 6 Tier

현재 5 Tier는 과거 candidate일 뿐 final freeze가 아니다.

---

# 5. Novelty Budget

각 Tier는 단순 수치 상승이 아니라 **새로운 경험 단위**여야 한다.

Tier마다 새로 줄 수 있는 항목:

- new monster archetype
- new monster combination
- new formation grammar
- new cadence problem
- new objective pressure
- new boss behavior
- new player skill reach window
- new meta progression expectation

원칙:
- 한 Tier에 너무 많은 신규 mechanic을 동시에 투입하지 않는다.
- 신규 monster 자체가 가장 강한 novelty asset 중 하나다.
- later Tier가 단순히 “기존 monster 더 많이/더 세게”가 되지 않도록 한다.

---

# 6. Monster Availability Ladder — USER-CONFIRMED DIRECTION

## 6.1 T1에서 9종 전부를 강제로 공개하지 않는다

현재 9종 ordinary roster 전체를 Tier1에서 모두 teach하는 기존 candidate는 active direction이 아니다.

새 원칙:

> Tier가 올라갈수록 새로운 monster archetype이 등장하여 campaign progression 자체가 새로운 전투 vocabulary를 제공해야 한다.

T1은 제한된 subset으로 시작한다.
Higher Tier에서 새로운 monster가 unlock되며, 기존 monster도 새로운 formation/cadence/composition으로 재해석한다.

정확히 어떤 monster가 어느 Tier에서 unlock되는지는 아직 OPEN.

## 6.2 Future monster expansion — 반드시 열어둔다

현재 9종은 현재 mechanical foundation roster이지 final lifetime roster가 아니다.

Campaign/data 구조는 다음을 금지한다.
- `monsterCount == 9` 하드코딩
- Tier schema에 9종 고정 column 박기
- pressure taxonomy가 신규 monster를 억지로 기존 family에 끼워 맞추도록 강제
- final Tier가 현재 9종 소진과 동시에 구조적으로 닫히는 설계

대신:

```text
MonsterRegistry(version)
  monsterId[]

TierProfile
  availableMonsterIds[]
  introducedMonsterIds[]
  returningMonsterIds[]
```

형태로 확장 가능하게 한다.

신규 monster가 기존 pressure family로 충분히 설명되지 않으면 taxonomy도 version-up할 수 있다.

## 6.3 Monster introduction 단계

Monster 하나가 Tier에 들어올 때:

```text
unlock/first appearance
 -> teach
 -> mixed
 -> high-pressure
 -> later-Tier reinterpretation
```

순서를 기본으로 한다.

---

# 7. Layer B — Player Power Spine

Campaign Spine 옆에 같은 중요도로 맞춘다.

## 7.1 Run-local power

필수 추적:
- Stage별 expected EXP
- expected level distribution
- Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31 reach window
- run coin
- shop purchasing power

Skill 자체의 효과뿐 아니라 **언제 도달하는가**가 encounter authoring의 선행 입력이다.

## 7.2 Meta power states

같은 class/Tier도 account progression에 따라 난도가 달라지는 것이 의도다.

최소 profile:

### P0 FRESH
- 해당 campaign phase에 처음 진입하는 저메타 계정

### P1 BALANCED
- 여러 class에서 일부 stars 확보

### P2 STAR_GROWN
- 다른 class stars가 충분히 쌓여 broad permanent stats가 상승

### P3 ACHIEVEMENT_ASSISTED
- targeted cross-class achievement bonus까지 적용

Old Tier replay나 과성장 account는 별도 OVERGROWN/STRESS profile로 분리할 수 있다.

---

# 8. Difficulty Calibration Principle — USER-CONFIRMED

## 8.1 기본 난도 상한

사용자가 원하는 일반 campaign 난도:

> **숙련자 simulation 기준 Tier full-clear probability는 기본적으로 60% 미만이어야 한다.**

이 `60%`는 목표 중앙값이 아니라 **기본 상한선**이다.
60%를 넘으면 특별한 의도가 없는 한 너무 쉬운 후보로 분류한다.

## 8.2 T1 예외

Tier1은 게임 첫 진입/학습 역할 때문에 숙련자 clear rate를 더 높게 둘 수 있다.

T1 exact target은 별도로 정한다.
단, T1도 현재 prototype처럼 사실상 자동 clear가 되는 수준을 목표로 하지 않는다.

## 8.3 Clear-rate 측정 단위

기본 clear rate는 개별 Stage 통과율이 아니라:

```text
Tier attempt start
 -> Stage1
 -> ...
 -> Stage50 clear
```

의 **Tier full-run 3★ clear probability**를 뜻한다.

## 8.4 평가 account state

60% 기준을 이미 과성장한 account replay에 적용하지 않는다.

기본 평가 시점:
- 해당 Tier를 처음 의미 있게 공략하는 expected progression state
- 해당 class의 예상 star/achievement support 범위
- intended run skill progression

즉 `Tier N intended-entry power`를 기준으로 평가한다.

## 8.5 Class asymmetry

모든 class가 같은 clear rate일 필요는 없다.

허용:
- 일부 class는 60%보다 훨씬 낮아 soft wall을 만남
- 다른 class progress → stars/achievements → 재도전

금지:
- structural hard lockout
- 어떤 meta 성장으로도 회복되지 않는 사실상 불가능 상태

---

# 9. Skilled profile 재정의 필요

기존 simulation의 `skilled`는 현재 목표 난도 기준으로 너무 낮은 숙련을 모델링했을 가능성이 높다.

사용자 직접 플레이 기준:
- 집중하면 combo 40은 쉽게 달성 가능한 수준
- 현재 test stages는 체감상 너무 낮은 난도

따라서 새 `SKILLED_V2` profile은 최소 다음 철학을 가진다.

- high combo maintenance는 숙련자에게 비현실적 rare event로 두지 않음
- combo 40 도달 가능성을 high-mastery 전용으로 밀어내지 않음
- timing accuracy / recovery / heavy completion도 기존 skilled보다 강하게 재산정
- `HIGH_MASTERY_STRESS`는 SKILLED_V2보다 별도 상위 profile로 유지

정확한 PERFECT/GOOD/NORMAL 확률, combo survival model, input error distribution은 관측/테스트 후 parameterize한다.
지금 숫자를 임의 freeze하지 않는다.

---

# 10. Layer C — 50-Stage Macro Flow

Tier마다 세부 monster는 달라도 공통 authoring 문법을 가질 수 있다.

초기 macro candidate:

```text
1–10   establish / introduce
11–20  mix / verify
21–30  tier identity establishment
31–40  pressure / soft-wall formation
41–49  mastery examination
50     tier final
```

현재 기존 design band는 참고하되 Master Spine에서 다시 검토한다.

중요:
- 신규 monster introduction은 Tier 전체 novelty budget과 연동한다.
- Stage 40+는 해당 Tier에서 이미 학습한 문제를 시험하는 쪽을 우선한다.

---

# 11. Layer D — Meta Progression Envelope

구조는 먼저 존재하지만 exact reward는 뒤에서 정한다.

## Stars
역할:
- broad account foundation
- predictable progression backbone

먼저 정할 것:
- 한 Tier에서 expected 0/1/2/3★ distribution
- stars가 soft wall을 어느 정도 이동시켜야 하는지

나중에 정할 것:
- exact threshold
- exact stat value

## Achievements
역할:
- targeted cross-class bridges

먼저 정할 것:
- achievement family
- progression graph philosophy

나중에 정할 것:
- exact sourceClass -> targetClass edge
- exact stat/value

실제 class soft-wall map이 나온 뒤 reward graph를 배치한다.

---

# 12. Layer E — Encounter Authoring

이 단계에서 비로소 세부화한다.

- monster frequency
- monster counts
- composition
- formation
- cadence
- spawn timing
- geometry
- active concurrency
- target-order behavior

상위 Spine이 바뀌면 세부 authoring은 candidate로만 유지한다.

---

# 13. Layer F — Economy / Boss / Multiplayer

## Run economy
- EXP
- coin
- shop cadence
- upgrade curve

Player Power Spine과 함께 calibration.

## Boss
Campaign/Tier identity가 먼저 잡힌 뒤 배치.
Boss cadence가 Stage macro를 선행해서 결정하지 않는다.

## Multiplayer
Solo/shared campaign spine이 먼저 성립한 뒤 2/3/4-player scaling 확장.
Team scaling 때문에 solo campaign identity가 바뀌지 않게 한다.

---

# 14. Dependency graph

```text
                 ┌─ Monster availability / novelty
                 │
MASTER CAMPAIGN ─┼─ 50-Stage macro pacing
PROGRESSION SPINE│
                 ├─ Run skill/power curve
                 │
                 ├─ Star progression envelope
                 │
                 └─ Achievement progression envelope
                         ↓
                 Encounter authoring
                         ↓
                 Run economy / boss / multiplayer
                         ↓
                 Deterministic simulation
                         ↓
                 Spine revision / freeze
```

Master Spine이 중심이고 나머지 시스템은 그 주변에서 함께 맞춘다.

---

# 15. 현재 기존 candidate의 상태 변경

다음 자료는 삭제하지 않지만 **active continuation 대상에서 PARKED**한다.

- `09_TIER_LADDER_CANDIDATE_V0_1.md`
  - T1에서 9종 전체 teaching 전제가 새 방향과 충돌.
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
  - 위 전제를 기반으로 함.
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
  - T1 roster/Stage skeleton이 재정립되기 전 더 세밀화하지 않음.

이 문서들의 유효 아이디어/계산은 추후 재사용할 수 있으나 active campaign authority가 아니다.

---

# 16. Exact next structural task

세부 micro-simulation을 일시 중단한다.

다음 순서:

1. Tier-count 후보 4/5/6의 campaign-volume 비교
2. 각 Tier의 novelty budget 정의
3. 현재 9종의 Tier별 monster availability/unlock 후보 작성
4. future monster expansion slot/contract 정의
5. 각 Tier 50-Stage macro role 작성
6. 각 Tier의 expected run skill-reach window 작성
7. P0/P1/P2/P3 meta-power state 정의
8. 각 Tier skilled clear-rate target envelope 작성
9. 전체 matrix 교차검토
10. 그 뒤에 encounter frequency/count/composition으로 다시 내려간다.

이 작업을 `Master Campaign Matrix`로 관리한다.
