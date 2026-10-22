# Timing Defense — 50 Stage Structure

Date: 2026-10-22 KST  
Status: **STRUCTURAL FOUNDATION / EXACT STAGE DATA OPEN**

## 1. 기본 구조

한 Tier는 50개의 Stage로 구성한다.
Stage는 단순히 숫자가 커질수록 HP/count를 올리는 방식이 아니라, 학습 -> 조합 -> 압박 -> 종합 시험으로 전개한다.

중요: **Stage design band와 star reward band는 서로 다른 분류**다.
Stage 30처럼 design상 checkpoint이면서 reward상 1★ 구간인 Stage가 존재하므로 하나의 enum으로 합치지 않는다.

---

# 2. Star reward band — USER_CONFIRMED_STRUCTURE

Attempt outcome 기준:
- Stage 1~19에서 실패: 0★
- Stage 20~39에서 실패: 1★
- Stage 40~49에서 실패: 2★
- Stage 50 클리어: 3★

정확한 계산:

```text
if tierCleared(Stage50): 3
else if failedStage >= 40: 2
else if failedStage >= 20: 1
else: 0
```

따라서 20/40/50은 reward progression의 구조적 anchor다.

---

# 3. Stage design bands

정확한 encounter는 미정이지만 50 Stage authoring은 다음 band를 기본 골격으로 사용한다.

### Stage 1~9 — Teach / Establish
- Tier identity 소개
- 신규 monster/capability를 한 번에 너무 많이 겹치지 않음
- baseline + 단일 pressure 위주
- target-order/formation 읽기 학습

### Stage 10 — First Checkpoint
- 1~9에서 학습한 핵심 mechanic 확인
- 반드시 boss일 필요 없음

### Stage 11~19 — Expand
- 2종/복합 조합 증가
- formation과 cadence 변화
- Stage 20 직전 첫 meaningful pressure ramp

### Stage 20~29 — Synthesis A
- reward상 1★ 구간
- Tier의 주요 encounter archetype을 본격적으로 조합
- 단순 소개보다 실제 대응 능력 확인

### Stage 30 — Mid Checkpoint
- design상 중간 전환점
- reward상 여전히 1★ 구간
- 후반 mechanic 조합으로 넘어가기 전 검증

### Stage 31~39 — Escalate
- reward상 1★ 구간
- overlap, backline protection, stateful threat 조합 증가
- Stage 40 진입이 명확한 성취가 되도록 난이도 상승

### Stage 40~49 — Final Examination
- reward상 2★ 구간
- Tier identity의 고난도 조합
- 단순 수치 폭증보다 이미 배운 문제를 더 짧은 판단 시간/강한 formation/더 복합 cadence로 제시
- Tier의 핵심 ordinary capability를 **처음 소개하는 구간으로 사용하지 않는 것**을 기본 guardrail로 한다

### Stage 50 — Tier Clear / 3★
- 해당 Tier의 최종 시험
- clear 시 3★
- boss/final composition 여부는 별도 decision

## T1 candidate의 추가 guardrail
`09_TIER_LADDER_CANDIDATE_V0_1.md`에서는 T1의 9종 ordinary vocabulary teaching을 Stage 29까지 완료하는 방향을 첫 candidate로 둔다.
이는 T1 candidate이지 모든 Tier의 절대 규칙은 아니다.

---

# 4. Stage lifecycle

강한 legacy reference:

```text
Stage intro
 -> combat
 -> stage clear
 -> inter-stage progression/shop
 -> next stage intro
```

현재 canonical combat rule에서 Stage intro 동안:
- movement/spawn 없음
- AI/passive 없음
- Timing input 없음

새 Timing turn은 visible target이 있을 때만 시작하며 이미 시작된 valid turn은 마지막 적이 사라져도 완료할 수 있다.

### Shop frequency는 OPEN_DECISION
Legacy v0.35에는 Stage 1 clear -> team shop -> READY -> next Stage 흐름이 실제 구현되었다.
그러나 50 Stage Tier에서 매 Stage마다 shop을 강제하면 최대 49회의 interruption이 생길 수 있다.

따라서 production에서는 다음 후보를 별도 비교한다.
- every-stage shop
- checkpoint shop
- selected-stage shop
- fast auto-continue + optional shop

기존 구현을 이유로 빈도를 자동 freeze하지 않는다.
Shop cadence는 `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`의 cross-category Gate G3로 관리한다.

---

# 5. Stage authoring 최소 필드

각 Stage는 최소 다음 데이터를 가진다.

```text
stageNumber
designBand
rewardBand
expectedDuration
baseFlow
encounters[]
monsterTypeCounts{}
monsterSpawnShare{}
activeConcurrencyPolicy
spawnCadence
formationProfile
geometryProfile
overlapPolicy
checkpointType
bossPolicy
teamScaling
rewardProfile
shopPolicy
```

`designBand`와 `rewardBand`를 별도 저장한다.

---

# 6. Encounter event 최소 필드

```text
EncounterEvent
  timeWindow
  archetypeId
  composition
  formation
  spawnOrder
  cadence
  geometry
  intensity
  overlapWith
```

`composition`만으로는 부족하다.
전열 자동 타게팅 때문에 `spawnOrder`와 `formation`이 실제 전술을 바꾼다.

예:

```text
SHIELD -> BRUTE -> SIEGER
```

와

```text
SIEGER -> SHIELD -> BRUTE
```

는 같은 3종 조합이어도 위협 구조가 다르다.

단, FRONT/MID/BACK은 고정 aggro slot이 아니다.
실제 runtime target은 authoritative X/validity 규칙을 따른다.
Formation depth는 의도된 arrival/screening order를 표현한다.

---

# 7. Stage에서 측정할 개수/빈도

### Total authored spawn
Stage data가 직접 생성하도록 작성한 entity 수.
SPLITTER child는 authored spawn에 포함하지 않는다.

### Effective entity count
parent death -> child spawn 등 실제 전투 중 생성된 총 entity 수.

### Peak active count
동시에 살아 있는 최대 monster 수.

### Short-window spawn density
- max 4-second spawns
- max 6-second spawns

과거 concrete recipe 분석의 4s P95 수치는 historical readability reference로만 보존한다. 현재 9종 roster로 다시 측정한다.

### Type presence
각 monster type이 Stage에 존재하는지.

### Meaningful threat presence
단순 filler가 아니라 해당 capability가 실제 문제를 만드는지.

### Capability threat-time
해당 capability가 유효 위협 상태로 존재한 시간.
특히 SUPPORTER/SIEGER는 spawn share보다 이 값이 중요할 수 있다.

---

# 8. Target-order metrics

현재 전투는 system-driven frontmost target acquisition이 핵심 제약이다.
따라서 각 Stage에서 다음을 측정한다.

- frontline block time
- target reorder count
- backline exposure time
- SUPPORTER aura uptime while screened
- SIEGER firing uptime while screened
- CHARGER windup interrupt opportunity count
- SPLITTER child-created frontline occupancy
- FLYER line/AoE geometry opportunities

이 지표가 없으면 같은 spawn count라도 실제 난이도 차이를 설명할 수 없다.

---

# 9. Anti-repetition

50 Stage가 반복적으로 느껴지지 않도록 구조적 제약을 둔다.

- 동일 encounter signature 연속 반복 금지/억제
- 동일 monster composition이라도 formation/cadence/geometry를 바꾸어 다른 문제로 만들 수 있음
- 같은 주 pressure를 같은 time window에 장기간 반복하지 않음
- 특수 monster를 모든 Stage에 의무적으로 넣지 않음
- high Tier도 모든 Stage를 복합 chaos로 만들지 않음

---

# 10. Difficulty ramp 원칙

Stage difficulty는 다음을 서로 독립적으로 조정한다.
- quantity
- durability
- speed/tempo
- formation protection
- capability overlap
- cadence compression
- geometry difficulty
- objective pressure

한 Stage에서 모든 축을 동시에 최대화하는 것은 예외로 취급한다.

---

# 11. Stage reward / EXP / skill reach

50 Stage authoring은 encounter만 봐서는 안 된다.
Stage별로 함께 계산해야 한다.
- timing event 수
- EXP 획득량
- 예상 level
- Lv6/11/16/21/26/31 도달 시점
- kill coin
- clear reward
- shop purchasing power

현재 Lv6만 current authoritative이며 Lv11~21은 exact legacy parity candidate, Lv26/31은 미확정이므로 late-stage 최종 calibration은 해당 skill authority decision과 연결한다.
EXP/skill reach는 governance Gate G4다.

---

# 12. Failure/Star analytics

각 Stage simulation 결과는 최종적으로 다음 Tier outcome bucket으로 집계한다.

```text
FAIL_EARLY      = failedStage 1..19  -> 0★
FAIL_STAR1      = failedStage 20..39 -> 1★
FAIL_STAR2      = failedStage 40..49 -> 2★
CLEAR_TIER      = Stage50 clear      -> 3★
```

Stage별 fail histogram을 통해 난이도 cliff를 찾는다.
특히 19->20, 39->40, 49->50에서 별 boundary 때문에 인위적인 벽이 생기지 않는지 별도로 검사한다.

---

# 13. 다음 작업

다음은 `04_MONSTER_ENCOUNTER_MODEL.md`와 `09_TIER_LADDER_CANDIDATE_V0_1.md`를 이용해:
- T1 firstTeach/firstMixed/firstHighPressure candidate
- encounter complexity tagging
- Tier별 frequency envelope -> exact simulation candidate count
- 50-stage signature skeleton
- team-size recipe
를 생성하는 단계다.
