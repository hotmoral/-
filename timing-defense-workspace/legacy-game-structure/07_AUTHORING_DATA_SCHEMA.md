# Timing Defense — Authoring Data Schema

Date: 2026-10-22 KST  
Status: **STRUCTURAL SCHEMA DRAFT V0.4 / NO PRODUCTION NUMBERS**

## 1. 목적

Campaign/Tier/Stage/Encounter/Meta progression을 코드에 하드코딩하지 않고 versioned authoring data로 관리한다.

상위 기준:
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`

---

# 2. Common status enum

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

# 3. Campaign spine schema

```yaml
campaignSpine:
  version: string
  status: enum
  initialTierCountCandidate: integer|null
  tierNamespaceOpenEnded: true
  monsterRegistryVersion: string
  masteryProfileVersion: string

  tierOrder: [tierId]

  globalRules:
    stagesPerTier: 50
    skilledFullClearUpperBound: 0.60
    tier1DifficultyExceptionAllowed: true
```

`initialTierCountCandidate`는 launch/initial campaign 후보 수다.
Lifetime final Tier count를 의미하지 않는다.

`tierNamespaceOpenEnded: true`를 기본 구조로 두어 T6/T7/... 확장을 허용한다.

---

# 4. Monster registry — future expansion contract

```yaml
monsterRegistry:
  version: string
  monsters:
    - id: string
      status: enum
      capabilityContractVersion: string|null
      pressureFamilies: [pressureId]
      introducedInRegistryVersion: string
      retired: boolean
```

Validation:
- `monsterCount == 9` 같은 상수 의존 금지
- Tier/Encounter는 항상 monsterId reference 사용
- 신규 monster는 registry version-up으로 추가 가능
- 기존 pressure taxonomy로 설명 불가하면 taxonomy version-up 허용

현재 9종은 registry V1의 initial mechanically-authoritative set일 뿐 lifetime final roster가 아니다.

---

# 5. Account progression schema

```yaml
accountProgress:
  version: string
  permanentRewardTrackVersion: string
  achievementCatalogVersion: string

  accountPermanentStats: {}
  achievementCompletions: [achievementId]
  unlockedTitles: [titleId]

  classes:
    classId:
      highestUnlockedTier: string|null
      classPermanentModifiers: {}
      tierRecords:
        tierId:
          bestStars: 0..3
          highestReachedStage: 0..50
          clears: integer
          attempts: integer
```

`globalStarTotal = sum(bestStars)`에서 파생.

---

# 6. Attempt outcome / star schema

```yaml
attemptOutcome:
  runId: string
  tierId: string
  classId: string
  clearedTier: boolean
  failedStage: integer|null
  reachedStage: integer
  attemptStars: 0..3

  modeTruth:
    humanPlayerCount: integer
    aiCount: integer
    hadRemoteHumanAtAnyPoint: boolean
    hadAiAtAnyPoint: boolean
```

Rules:
```text
Stage50 clear -> 3★
fail 40..49 -> 2★
fail 20..39 -> 1★
fail 1..19 -> 0★
```

---

# 7. Permanent star reward schema

```yaml
permanentRewardTrack:
  version: string
  rewards:
    - starThreshold: integer
      stat: string
      operation: add|multiply|other
      value: number|null
```

Stars = broad account foundation.
Exact threshold/value는 OPEN.

---

# 8. Achievement / title / cross-class reward

```yaml
achievement:
  id: string
  family: class_tier_reach|all_class_tier_reach|solo_no_ai_tier_clear|multi_class_mastery|other
  sourceClass: classId|null
  tierId: string|null
  condition: {}
  rewards:
    - target: ACCOUNT|classId
      statId: string
      operation: add|multiply|other
      value: number|null
      stackPolicy: unique|additive|highest|other
  titleUnlockId: string|null
```

```yaml
title:
  id: string
  sourceAchievementId: string
  displayName: string
  cosmeticOnly: boolean
```

```yaml
achievementRewardEdge:
  sourceAchievementId: string
  sourceClass: classId|null
  target: ACCOUNT|classId
  statId: string
  operation: add|multiply|other
  value: number|null
```

Graph validation:
- reachability
- cycle detection
- hard-dependency deadlock detection
- dominant-route detection

---

# 9. Tier schema

```yaml
tier:
  id: string
  displayName: string
  status: enum
  stageCount: 50
  identity: string
  noveltyBudget: {}

  roster:
    registryVersion: string
    availableMonsterIds: [monsterId]
    introducedMonsterIds: [monsterId]
    returningMonsterIds: [monsterId]

  monsterIntroduction:
    monsterId:
      firstAvailableTier: string
      firstTeachStage: integer|null
      firstMixedStage: integer|null
      firstHighPressureStage: integer|null
      laterTierRoleTags: [string]

  expectedRunPowerWindow:
    expectedLevelByBand: {}
    expectedSkillReach: {}

  expectedMetaPowerWindow:
    allowedProfiles: [P0_FRESH|P1_BALANCED|P2_STAR_GROWN|P3_ACHIEVEMENT_ASSISTED|OVERGROWN]

  difficultyTarget:
    masteryProfile: SKILLED_V2
    fullTierClearUpperBound: number|null
    tier1Exception: boolean

  targetDistributions: {}
  designBandPolicy: {}
  rewardBandPolicy: {}
  teamScalingPolicy: {}
  bossPolicy: {}
```

Important:
- T1에 모든 registry monster를 넣을 필요 없음
- 신규 monster unlock은 Tier novelty budget과 함께 관리

---

# 10. Stage schema

```yaml
stage:
  tierId: string
  stageNumber: 1..50
  designBand: string
  rewardBand: zeroStar|oneStar|twoStar|threeStarClear
  checkpointType: none|checkpoint|boss|final|other
  expectedDurationSec: number|null
  baseFlow: []
  encounters: [encounterEventId]
  activeConcurrencyPolicy: {}
  rewardProfile: string|null
  shopPolicy: string|null
  teamScalingProfile: string
```

---

# 11. Encounter schema

```yaml
encounterEvent:
  id: string
  archetypeId: string
  timeWindow: {}
  composition:
    - monsterId: string
      count: integer
      role: front|mid|back|air|free
  formationId: string
  spawnOrder: []
  cadenceId: string
  geometryId: string
  intensity: number
  overlapPolicy: string
```

```yaml
encounterArchetype:
  id: string
  pressureFamilies: [pressureId]
  requiredMonsterRoles: []
  optionalMonsterRoles: []
  allowedFormations: []
  allowedCadences: []
  tacticalQuestion: string
  classOpportunityTags: []
  complexityTier: C0|C1|C2|C3|C4
```

---

# 12. Pressure taxonomy

Current IDs:
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

이 list는 lifetime final enum으로 하드코딩하지 않는다.
Future monster capability가 요구하면 taxonomy version-up 가능.

---

# 13. Formation / cadence

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

```yaml
cadence:
  id: string
  type: drip|wave|burst|escort|stagger|overlap|late_insert
  groupGapMs: number|null
  unitGapMs: number|null
  durationMs: number|null
```

FRONT/MID/BACK은 target override가 아니라 authoring intent다.

---

# 14. Mastery profile schema

```yaml
masteryProfile:
  id: LEARNING|AVERAGE|SKILLED_V2|HIGH_MASTERY_STRESS
  version: string
  timingDistribution: {}
  comboModel: {}
  heavyCompletionModel: {}
  inputErrorModel: {}
```

`SKILLED_V2` requirement:
- combo 40을 high-mastery-only로 모델링하지 않음
- old skilled보다 높은 combo maintenance/timing competence

Exact probabilities are OPEN until measured.

---

# 15. Meta-power profile schema

```yaml
metaPowerProfile:
  id: P0_FRESH|P1_BALANCED|P2_STAR_GROWN|P3_ACHIEVEMENT_ASSISTED|OVERGROWN
  starRange: {}
  achievementSet: []
  accountPermanentStats: {}
  classPermanentModifiers: {}
```

`OVERGROWN` replay profile은 standard skilled difficulty target에서 제외한다.

---

# 16. Simulation result schema

```yaml
simulationResult:
  campaignSpineVersion: string
  monsterRegistryVersion: string
  tierDataVersion: string
  dataHash: string
  seed: integer
  modelMode: CURRENT_AUTHORITY|LEGACY_PARITY_CANDIDATE|FUTURE_SKILL_PLACEHOLDER
  masteryProfile: string
  metaPowerProfile: string
  tierId: string
  stageNumber: integer|null
  classId: string
  teamSize: integer

  outcome:
    cleared: boolean
    failedStage: integer|null
    stars: 0..3

  metrics: {}
```

Tier aggregate report must include:
- fullTierClearProbability
- failureHistogram
- classVariance
- skillReachDistribution
- starOutcomeDistribution
- softWallLocations

---

# 17. Account progression simulation

```yaml
accountSimulation:
  campaignSpineVersion: string
  monsterRegistryVersion: string
  routePolicy: first_class|balanced|stacked|favorite_first|weak_class_recovery|achievement_focus|optimizer
  masteryProfile: string
  stateTimeline: []
  outputs:
    firstClearStepByClassTier: {}
    attemptsByClassTier: {}
    softWallRecoveryEvents: []
    unreachableNodes: []
    dominantRouteScore: number|null
    snowballMetric: number|null
```

---

# 18. Validation rules

## Campaign / roster
- Tier exactly 50 stages
- monster reference must exist in registry version
- no assumption that registry size is 9
- introducedMonsterIds must be subset of availableMonsterIds
- future Tier IDs permitted beyond initial campaign candidate

## Difficulty
- non-T1 standard Tier with intended-entry SKILLED_V2 full-clear >=0.60 -> warning/classification `TOO_EASY_FOR_SKILLED` unless explicitly justified
- OVERGROWN replay result does not satisfy/fail this gate

## Star
- reward band boundaries exact
- bestStars invariant

## Achievement
- SOLO_NO_AI truth verifiable
- reward graph reachability/cycle/deadlock analysis possible

## Monster capability
- SPLITTER child accounting
- SUPPORTER stacking contract respected
- no manual-target assumption

## Target order
- authoring intent vs simulated actual order measurable

---

# 19. Versioning

At minimum:
```text
campaign-spine-v0.x
monster-registry-vN
pressure-taxonomy-vN
mastery-profile-vN
tier-data-v0.x
encounter-library-v0.x
permanent-reward-v0.x
achievement-catalog-v0.x
cross-class-reward-graph-v0.x
```

All simulation reports record these versions/hashes.

---

# 20. Live implementation boundary

이 schema는 live server에 즉시 연결하지 않는다.
Authoring/simulation lane에서 안정화하고 explicit production freeze 이후 import boundary를 설계한다.
