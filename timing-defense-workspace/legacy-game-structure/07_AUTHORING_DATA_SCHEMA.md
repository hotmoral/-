# Timing Defense — Authoring Data Schema

Date: 2026-10-22 KST  
Status: **STRUCTURAL SCHEMA DRAFT V0.1 / NO PRODUCTION NUMBERS**

## 1. 목적

Tier/Stage/Encounter/Meta progression 데이터를 나중에 코드에 박아넣지 않고 독립 authoring data로 관리하기 위한 공통 schema다.

현재 단계에서는 필드와 관계만 정의하며 production 값은 넣지 않는다.

## 2. Account progression schema

```yaml
accountProgress:
  version: string
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
          bestStage: 0..50
          clears: integer
          attempts: integer
    rogue: {}
    tank: {}
    archer: {}
    mage: {}
```

`globalStarTotal`은 `sum(bestStars)`에서 파생 가능하다.

## 3. Permanent reward schema

```yaml
permanentRewardTrack:
  version: string
  rewards:
    - starThreshold: integer
      stat: enum
      operation: add|multiply|other
      value: number
```

아직 실제 threshold/value는 미정.

## 4. Tier schema

```yaml
tier:
  id: string
  displayName: string
  stageCount: 50
  identity: string
  monsterAvailability: [monsterId]
  primaryPressureFamilies: [pressureId]
  secondaryPressureFamilies: [pressureId]
  targetDistributions:
    monsterSpawnShare: {}
    encounterPresence: {}
    archetypeShare: {}
    formationShare: {}
    cadenceShare: {}
    geometryShare: {}
  bandPolicy:
    teach: 1-9
    checkpoint1: 10
    expand: 11-19
    star1Zone: 20-29
    checkpoint2: 30
    escalate: 31-39
    star2Zone: 40-49
    final: 50
  teamScalingPolicy: {}
  bossPolicy: {}
```

## 5. Stage schema

```yaml
stage:
  tierId: string
  stageNumber: 1..50
  band: enum
  checkpointType: none|checkpoint|boss|final|other
  expectedDurationSec: number|null
  baseFlow:
    monsterId: string
    count: integer
    cadenceId: string
  encounters:
    - encounterEventId
  rewardProfile: string|null
  shopPolicy: string|null
  teamScalingProfile: string
```

## 6. Encounter event schema

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

## 7. Encounter archetype schema

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
  complexityTier: low|mid|high
```

## 8. Pressure family IDs

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

## 9. Monster role schema

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

## 10. Formation schema

```yaml
formation:
  id: string
  slots:
    - lane: ground|air
      depth: front|mid|back
      offsetY: number|null
      spacing: number|null
  targetOrderIntent: string
```

중요: 실제 authoritative target acquisition을 강제로 지정하는 필드가 아니다.
`targetOrderIntent`는 spawn/position 설계 의도를 기록하는 메타데이터다.

## 11. Cadence schema

```yaml
cadence:
  id: string
  type: drip|wave|burst|escort|stagger|overlap|late_insert
  groupGapMs: number|null
  unitGapMs: number|null
  durationMs: number|null
```

숫자는 calibration 이후 채운다.

## 12. Simulation result schema

```yaml
simulationResult:
  dataVersion: string
  seed: integer
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
    peakActive
    spawn4sMax
    spawn6sMax
    frontlineBlockTime
    backlineExposureTime
    supporterAuraUptime
    siegerShotCount
    chargerCompleted
    chargerInterrupted
    splitterChildren
```

## 13. Validation rules

Authoring data validator는 최소 다음을 검사한다.

- Tier는 정확히 50 Stage를 가져야 함.
- Stage number 중복/누락 금지.
- 존재하지 않는 monster/archetype/formation/cadence reference 금지.
- SPLITTER child를 authored normal spawn으로 잘못 넣지 않도록 구분.
- SUPPORTER aura stacking을 authoring data로 임의 허용하지 않음.
- ordinary monster가 manual-target requirement를 전제로 하지 않음.
- Stage signature exact duplicate 연속 사용 경고.
- short-window density 계산 가능해야 함.
- Stage 20/40/50 star boundary metadata 일관성 검사.

## 14. Versioning

각 authoring set은 독립 version/hash를 가져야 한다.

예:

```text
tier-data-v0.1
encounter-library-v0.1
permanent-reward-v0.1
```

시뮬레이션 report에는 사용한 version/hash를 기록해 결과를 재현 가능하게 한다.

## 15. Live implementation boundary

이 schema는 live server가 즉시 읽도록 연결하지 않는다.
먼저 별도 authoring/simulation lane에서 안정화한 뒤 production freeze 시 data import 경계를 설계한다.
