# Timing Defense — Authoring Data Schema

Date: 2026-10-22 KST  
Status: **STRUCTURAL SCHEMA DRAFT V0.2 / NO PRODUCTION NUMBERS**

## 1. 목적

Tier/Stage/Encounter/Meta progression 데이터를 코드에 하드코딩하지 않고 독립 authoring data로 관리하기 위한 공통 schema다.

현재 단계에서는 필드와 관계를 정의하며 production 값은 넣지 않는다.
이 schema는 `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`의 정합성 규칙을 따른다.

---

# 2. Common status enum

문서/authoring metadata가 사용할 수 있는 구조 상태:

```text
CURRENT_FROZEN_STRUCTURE
CURRENT_AUTHORITATIVE
USER_CONFIRMED_STRUCTURE
DERIVED_INVARIANT
LEGACY_IMPLEMENTED_REFERENCE
LEGACY_ANALYSIS_REFERENCE
DESIGNED_NOT_AUTHORITATIVE
OPEN_DECISION
SUPERSEDED
```

---

# 3. Account progression schema

```yaml
accountProgress:
  version: string
  permanentRewardTrackVersion: string
  permanentStats:
    attack: number
    critChance: number
    critDamage: number
    wallHp: number
    defense: number
    knockback: number
  classes:
    knight:
      highestUnlockedTier: string|null
      tierRecords:
        T1:
          bestStars: 0..3
          highestReachedStage: 0..50
          clears: integer
          attempts: integer
    rogue: {}
    tank: {}
    archer: {}
    mage: {}
```

`globalStarTotal`은 authoritative stored input이 아니라 원칙적으로 `sum(bestStars)`에서 파생한다.
캐시할 경우 source records와 검증 가능해야 한다.

`bestStars = max(previous, attemptStars)`는 `DERIVED_INVARIANT`다.

---

# 4. Attempt outcome / star schema

```yaml
attemptOutcome:
  tierId: string
  classId: string
  clearedTier: boolean
  failedStage: integer|null
  reachedStage: integer
  attemptStars: 0..3
```

Validation:

```text
clearedTier == true  -> reachedStage=50, failedStage=null, attemptStars=3
failedStage 40..49   -> attemptStars=2
failedStage 20..39   -> attemptStars=1
failedStage 1..19    -> attemptStars=0
```

---

# 5. Permanent reward schema

```yaml
permanentRewardTrack:
  version: string
  status: enum
  rewards:
    - starThreshold: integer
      stat: enum
      operation: add|multiply|other
      value: number
```

아직 실제 threshold/value는 미정.
Reward track 변경은 meta/Tier/run-economy/class-sensitivity를 함께 검토하는 governance Gate G2 대상이다.

---

# 6. Tier schema

```yaml
tier:
  id: string
  displayName: string
  status: enum
  stageCount: 50
  identity: string
  monsterAvailability: [monsterId]
  primaryPressureFamilies: [pressureId]
  secondaryPressureFamilies: [pressureId]

  monsterIntroduction:
    monsterId:
      firstTeachStage: integer|null
      firstMixedStage: integer|null
      firstHighPressureStage: integer|null
      targetFrequencyByDesignBand: {}

  targetDistributions:
    monsterSpawnShare: {}
    monsterStagePresence: {}
    meaningfulThreatPresence: {}
    capabilityThreatTimeShare: {}
    encounterArchetypeShare: {}
    formationShare: {}
    cadenceShare: {}
    geometryShare: {}
    complexityShare: {}

  designBandPolicy:
    teach: 1-9
    checkpoint1: 10
    expand: 11-19
    synthesisA: 20-29
    checkpoint2: 30
    escalate: 31-39
    finalExamination: 40-49
    final: 50

  rewardBandPolicy:
    zeroStarFail: 1-19
    oneStarFail: 20-39
    twoStarFail: 40-49
    threeStarClear: 50

  teamScalingPolicy: {}
  bossPolicy: {}
```

`designBandPolicy`와 `rewardBandPolicy`를 절대로 하나의 band enum으로 합치지 않는다.

---

# 7. Stage schema

```yaml
stage:
  tierId: string
  stageNumber: 1..50
  designBand: teach|checkpoint1|expand|synthesisA|checkpoint2|escalate|finalExamination|final
  rewardBand: zeroStar|oneStar|twoStar|threeStarClear
  checkpointType: none|checkpoint|boss|final|other
  expectedDurationSec: number|null

  baseFlow:
    - monsterId: string
      count: integer
      cadenceId: string
      formationId: string|null

  encounters:
    - encounterEventId

  activeConcurrencyPolicy:
    softTarget: integer|null
    hardLimit: integer|null

  rewardProfile: string|null
  shopPolicy: string|null
  teamScalingProfile: string
```

`baseFlow`는 하나의 monster type만 허용하지 않고 list로 둔다.

---

# 8. Encounter event schema

```yaml
encounterEvent:
  id: string
  archetypeId: string
  timeWindow:
    mode: normalized|absolute|triggered
    value: number|string
  composition:
    - monsterId: string
      count: integer
      role: front|mid|back|air|free
  formationId: string
  spawnOrder: [monsterId|groupId]
  cadenceId: string
  geometryId: string
  intensity: number
  overlapPolicy: string
  notes: string
```

`role=front|mid|back`은 aggro 강제값이 아니다.
Authoring intent이며 실제 target order는 runtime authoritative position/validity에서 결정된다.

---

# 9. Encounter archetype schema

```yaml
encounterArchetype:
  id: string
  displayName: string
  pressureFamilies: [pressureId]
  requiredMonsterRoles: []
  optionalMonsterRoles: []
  allowedFormations: []
  allowedCadences: []
  tacticalQuestion: string
  classOpportunityTags: []
  complexityTier: C0|C1|C2|C3|C4
```

Complexity 의미:
- C0 baseline
- C1 single mechanic
- C2 dual readable
- C3 synergy
- C4 multi-state high complexity

---

# 10. Pressure family IDs

```text
BASELINE
FLOOD
RUSH
BULWARK
BREACH
AERIAL
REPLICATE
SUPPORT
SIEGE
```

`BASELINE`은 neutral reference로 별도 취급 가능.

---

# 11. Monster role schema

한 monster는 base archetype과 encounter role을 분리한다.

```yaml
monsterRole:
  monsterId: shield
  encounterRole: front
  tacticalRole: armor_screen
```

예:
- BRUTE -> front/raw_anchor
- SHIELD -> front/armor_screen
- SUPPORTER -> mid|back/formation_support
- SIEGER -> back/objective_pressure
- CHARGER -> front|mid/burst_breach

---

# 12. Formation schema

```yaml
formation:
  id: string
  slots:
    - lane: ground|air
      depth: front|mid|back
      offsetY: number|null
      spacing: number|null
      arrivalOffsetMs: number|null
  targetOrderIntent: string
```

중요:
- 실제 authoritative target acquisition을 강제로 지정하는 필드가 아니다.
- `targetOrderIntent`는 spawn/position 설계 의도를 기록하는 metadata다.
- simulation은 실제 movement/position으로 intended order가 실제 성립하는지 검증해야 한다.

---

# 13. Cadence schema

```yaml
cadence:
  id: string
  type: drip|wave|burst|escort|stagger|overlap|late_insert
  groupGapMs: number|null
  unitGapMs: number|null
  durationMs: number|null
```

숫자는 candidate simulation data로 먼저 작성하고 production freeze 전에는 live authority로 취급하지 않는다.

---

# 14. Simulation result schema

```yaml
simulationResult:
  dataVersion: string
  dataHash: string
  seed: integer
  modelMode: CURRENT_AUTHORITY|LEGACY_PARITY_CANDIDATE|FUTURE_SKILL_PLACEHOLDER
  tierId: string
  stageNumber: integer|null
  classId: string
  teamSize: integer
  masteryProfile: string
  permanentProfile: string

  outcome:
    cleared: boolean
    failedStage: integer|null
    stars: 0..3

  metrics:
    clearTime
    baseHpRemaining
    xp
    level
    coin
    authoredSpawnCount
    effectiveEntityCount
    peakActive
    spawn4sMax
    spawn6sMax
    frontlineBlockTime
    targetReorderCount
    backlineExposureTime
    meaningfulThreatPresence
    capabilityThreatTime
    supporterAuraUptime
    supporterScreenedAuraUptime
    siegerShotCount
    siegerScreenedFiringUptime
    chargerWindups
    chargerCompleted
    chargerInterrupted
    splitterParents
    splitterChildren
    splitterChildFrontlineTime
    flyerGeometryOpportunityTime
    classOpportunityCoverage
```

---

# 15. Validation rules

Authoring data validator는 최소 다음을 검사한다.

## Referential
- Tier는 정확히 50 Stage를 가져야 함.
- Stage number 중복/누락 금지.
- 존재하지 않는 monster/archetype/formation/cadence reference 금지.

## Star/reward
- Stage 1-19 rewardBand=zeroStar
- Stage 20-39 rewardBand=oneStar
- Stage 40-49 rewardBand=twoStar
- Stage 50 rewardBand=threeStarClear
- designBand와 rewardBand를 혼동하지 않음.

## Monster capability
- SPLITTER child를 authored normal spawn으로 잘못 넣지 않음.
- SUPPORTER aura stacking을 authoring data로 임의 허용하지 않음.
- ordinary monster가 manual-target requirement를 전제로 하지 않음.
- SIEGER/SUPPORTER/CHARGER 등 stateful capability가 contract를 authoring data로 재정의하지 않음.

## Introduction
- `firstTeachStage <= firstMixedStage <= firstHighPressureStage`가 기본 기대값.
- 예외는 justification 필요.
- Stage 40-49에 core ordinary capability를 처음 teaching하는 경우 warning/error policy 적용.

## Repetition/readability
- Stage signature exact duplicate 연속 사용 경고.
- short-window density 계산 가능해야 함.
- effective entity count 계산 가능해야 함.

## Target-order
- formation intent와 실제 simulated target order 차이를 검출할 수 있어야 함.

---

# 16. Versioning

각 authoring set은 독립 version/hash를 가져야 한다.

예:

```text
tier-data-v0.1
encounter-library-v0.1
permanent-reward-v0.1
```

시뮬레이션 report에는 사용한 version/hash, modelMode, seed range, run count를 기록한다.

---

# 17. Live implementation boundary

이 schema는 live server가 즉시 읽도록 연결하지 않는다.
먼저 별도 authoring/simulation lane에서 안정화한 뒤 production freeze 시 data import 경계를 설계한다.
