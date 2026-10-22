# Timing Defense — Achievement / Title / Cross-Class Progression V0.1

Date: 2026-10-22 KST  
Status: **USER-CONFIRMED DIRECTION + STRUCTURAL CANDIDATE / NO NUMERICAL FREEZE**

## 0. 목적

별 기반 공용 영구 성장 위에 두 번째 메타 성장축을 정의한다.

핵심 의도:

> 한 직업의 성취와 숙련이 그 직업만 강하게 만드는 것이 아니라, 다른 직업의 다음 Tier 도전을 위한 기반으로 연결된다.

즉 이 시스템은 단순 수집형 업적/칭호가 아니라 **Cross-Class Progression Network**다.

현재 확정 방향:
- 직업별 Tier 진행은 독립이다.
- 같은 Tier의 Stage 구성은 직업과 무관하게 동일하게 사용한다.
- 어떤 직업은 신규/저성장 계정에서 특정 Tier를 혼자 밀기 어려울 수 있다.
- 다른 직업에서 Tier/별/업적을 달성해 account-wide 또는 target-class 보너스를 얻는다.
- 그 성장으로 이전에 막힌 직업을 다시 밀어 나갈 수 있어야 한다.

---

# 1. Meta progression에서의 역할 분리

## A. Stars — broad account foundation
별은 모든 직업/Tier의 최고 성취도를 합산하는 **넓은 공용 성장축**이다.

역할:
- 여러 직업을 플레이할 이유를 만든다.
- 전체 계정의 기본 전투 기반을 점진적으로 올린다.
- 특정 직업에만 종속되지 않는다.

## B. Achievements — conditional targeted progression
업적은 특정 플레이 조건을 만족했을 때 열리는 **조건부/표적형 성장축**이다.

예:
- Knight Tier N 달성
- 전 직업 Tier N 달성
- Rogue로 Tier N을 AI 없이 SOLO clear
- 특정 직업으로 특정 별/clear 조건 달성

업적 보상은:
- account-wide stat일 수도 있고,
- 특정 다른 직업의 stat일 수도 있다.

## C. Titles — achievement presentation layer
칭호는 업적의 가시적 표현/수집 요소다.

권장 구조:
- achievement completion이 gameplay reward를 영구 해금한다.
- title은 프로필/로비/결과 화면에 표시할 수 있다.
- title을 장착해야만 능력치가 적용되는 구조는 기본값으로 두지 않는다.

이유:
- 강한 칭호를 강제 장착하게 만들면 cosmetic choice가 사라진다.
- title swap에 따라 전투력이 바뀌면 authoring/simulation state가 불필요하게 복잡해진다.

`title equip affects stats`는 별도 OPEN_DECISION으로 남긴다.

---

# 2. Achievement family V0.1

## A01 — CLASS_TIER_REACH
한 특정 직업이 특정 Tier 진행 조건을 만족.

예시 조건 형식:
- Knight T2 1★
- Mage T3 3★
- Archer T4 clear

정확히 `reach`, `1★`, `3★`, `clear` 중 무엇을 achievement 기준으로 사용할지는 개별 업적 data가 가진다.

## A02 — ALL_CLASS_TIER_REACH
모든 5직업이 동일 Tier의 조건을 만족.

예시:
- 5직업 모두 T1 1★ 이상
- 5직업 모두 T1 clear
- 5직업 모두 T2 3★

이 family는 특정 직업 편향 없이 계정 전반 숙련을 증명한다.

## A03 — SOLO_NO_AI_TIER_CLEAR
특정 직업으로 Tier를 **순수 SOLO / AI 0 / 다른 인간 0** 상태에서 clear.

Structural invariant:
```text
humanPlayerCount = 1
aiCount = 0
selectedClass = achievement.sourceClass
Tier Stage50 clear = true
```

이 조건은 일반 Tier clear보다 높은 개인 숙련 증명으로 취급한다.

사용자 의도상 핵심 보상 방향:
- sourceClass 자신이 아니라 **다른 직업의 특정 능력치**를 영구 강화할 수 있다.

이것이 cross-class progression의 대표적인 연결이다.

## A04 — MULTI_CLASS_MASTERY
여러 직업의 달성을 묶는 종합 업적.

예:
- 서로 다른 3직업 T2 clear
- 모든 직업에서 최소 2★

현재 구조 family만 정의하고 exact list는 추후 authoring한다.

---

# 3. Cross-Class Reward Graph

업적 보상은 단순 배열이 아니라 방향 그래프로 취급한다.

```text
source achievement
   ↓
target class or account
   ↓
stat category
   ↓
permanent modifier
```

예시 형식만 제시:

```text
SOLO_NO_AI_CLEAR(Knight, T2)
  -> target: Rogue
  -> stat: TBD
  -> value: TBD
```

정확한 직업 pair/stat/value는 **미확정**이며 simulation 후 결정한다.

## Graph node
- ACCOUNT
- KNIGHT
- ROGUE
- TANK
- ARCHER
- MAGE

## Edge
`AchievementRewardEdge`

필드:
- sourceAchievementId
- sourceClass|null
- targetClass|ACCOUNT
- statId
- operation
- value
- stackPolicy

---

# 4. 중요한 설계 목적

## 4.1 Soft wall recovery
어떤 직업이 현재 account power에서 특정 Tier에 막혀도:

```text
Class A blocked
 -> Class B/C progresses
 -> stars + achievements
 -> permanent power rises
 -> return to Class A
 -> previously blocked Tier becomes attainable
```

이 루프가 의도된 progression이다.

## 4.2 Different classes can seed each other
한 직업의 숙련은 다른 직업의 미래 진행 기반을 만든다.

따라서 직업 선택은 고립된 다섯 캠페인이 아니라 **서로 연결된 다섯 progression lane**이다.

## 4.3 Same Stage data remains meaningful
직업별로 Stage를 따로 만들 필요가 없다.

같은 Tier/Stage data에서:
- 초기 account에서는 특정 직업이 불리할 수 있고,
- 다른 직업의 성취로 permanent power가 높아진 뒤 다시 도전할 수 있다.

이 구조가 동일 Stage를 공유하면서도 직업별 성장 순서를 의미 있게 만든다.

---

# 5. 반드시 피해야 할 구조적 실패

## 5.1 Circular deadlock
금지 예:
```text
Knight T2 SOLO clear -> Rogue 필수 보너스
Rogue T2 SOLO clear -> Knight 필수 보너스
```

두 직업 모두 해당 보너스 없이는 T2를 사실상 깰 수 없다면 progression graph가 잠긴다.

검사:
- 신규 계정에서 최소 한 개 이상의 합리적인 progression seed path가 존재해야 한다.
- 어떤 reward도 구조적 hard requirement가 되어서는 안 된다.

## 5.2 Mandatory achievement trap
업적 보상이 너무 강하면:
- 업적 = 선택적 mastery reward가 아니라
- campaign 진행을 위한 강제 체크리스트
가 된다.

업적은 soft wall을 완화하고 경로를 넓히되, 한 특정 achievement가 단 하나의 필수 열쇠가 되지 않게 한다.

## 5.3 Solo/co-op value inversion
SOLO_NO_AI 업적 보상이 강하다고 해서 TEAM/AI 플레이가 ‘틀린 방식’처럼 느껴지면 안 된다.

원칙:
- 일반 별/Tier progression은 SOLO/TEAM/AI를 통해 진행 가능.
- AI-free solo clear는 추가 mastery achievement.
- 그 보상은 의미 있어야 하지만 기본 progression 전체를 인질로 잡지 않는다.

## 5.4 Source-class self snowball
특정 직업 SOLO clear가 같은 직업을 계속 직접 강화하면:
```text
strong class -> solo clear -> stronger same class -> easier next solo clear
```
의 일방 snowball이 생길 수 있다.

사용자 의도에 맞게 SOLO mastery reward는 다른 직업/계정 기반으로 연결하는 것을 우선 검토한다.

## 5.5 Dominant progression route
한 직업만 먼저 키우는 것이 모든 경우에서 최적이면 ‘5직업 교차 성장’이 무너진다.

시뮬레이션에서:
- optimal path
- balanced path
- favorite-class-first path
- weak-class-recovery path
을 비교한다.

---

# 6. Achievement reward와 Star reward의 관계

둘은 같은 일을 하면 안 된다.

권장 역할:

### Stars
- broad
- predictable
- account-wide
- progression backbone

### Achievements
- conditional
- milestone/mastery driven
- targeted cross-class or specialized account reward
- alternate progression route

즉:
```text
Stars = floor / foundation
Achievements = bridges / targeted support
```

이렇게 해야 두 시스템이 중복되지 않는다.

---

# 7. Stat category 설계 원칙

아직 정확한 reward stat/value를 정하지 않는다.

후보:
- attack
- critChance
- critDamage
- wallHp
- defense
- knockback/control
- class-specific derived modifier

주의:
- 동일 raw stat도 직업별 기대효율이 다를 수 있다.
- multihit/crit/penetration/AoE 구조 때문에 +1%가 동일 가치가 아닐 수 있다.

따라서 achievement reward는 `표기 수치 동일 = 실제 가치 동일`이라고 가정하지 않는다.

각 edge를 class-specific simulation으로 검증한다.

---

# 8. Solo clear truth contract

`SOLO_NO_AI` achievement가 신뢰 가능하려면 run start부터 clear까지 mode가 검증 가능해야 한다.

최소 기록:
- TierId
- sourceClass
- humanPlayerCount == 1
- aiCount == 0
- no mid-run AI injection
- no remote human join
- runId
- Tier data version/hash
- relevant balance/progression version
- Stage50 clear event

중간에 TEAM/AI로 변환된 run은 SOLO_NO_AI clear로 인정하지 않는다.

Reconnect 자체는 동일한 authoritative run을 복구하는 것이므로 solo 상태를 보존할 수 있다.

---

# 9. Simulation requirements

Achievement layer 추가 후 account progression simulation은 다음을 포함한다.

## Reachability
- 초기 계정에서 성장 경로가 하나 이상 존재하는가
- 특정 class/Tier가 reward cycle 때문에 닫히지 않는가

## Reward leverage
- 한 achievement가 target class의 예상 도달 Stage를 얼마나 이동시키는가
- 여러 achievement가 누적되면 얼마나 이동시키는가

## Route diversity
- 하나의 압도적 최적 class order만 존재하는가
- 여러 합리적 성장 경로가 가능한가

## Soft-wall recovery
- 실패했던 class/Tier에 다른 직업 성취 후 돌아왔을 때 실제 clear probability가 상승하는가

## Snowball
- stars + achievements가 곱해져 후반 Tier를 trivialize하지 않는가

## Solo mastery cost
- AI-free solo clear가 해당 시점에서 얼마나 어려운가
- reward 가치가 난이도와 비례하는가

---

# 10. Achievement authoring schema candidate

```yaml
achievement:
  id: string
  family: class_tier_reach|all_class_tier_reach|solo_no_ai_tier_clear|multi_class_mastery
  displayTitle: string
  sourceClass: classId|null
  tierId: string|null
  condition:
    minStars: integer|null
    requireClear: boolean
    humanCount: integer|null
    aiCount: integer|null
    requiredClasses: [classId]
  rewards:
    - target: ACCOUNT|classId
      statId: string
      operation: add|multiply|other
      value: number|null
  titleUnlockId: string|null
  status: candidate|frozen
```

`value`는 production freeze 전까지 null/parameter로 둘 수 있다.

---

# 11. Title schema candidate

```yaml
title:
  id: string
  sourceAchievementId: string
  displayName: string
  category: class|all_class|solo|mastery|other
  cosmeticOnly: true
```

기본 권장값은 `cosmeticOnly: true`.

Gameplay reward는 achievement completion에 귀속시킨다.

---

# 12. Cross-category dependencies

Achievement reward를 변경하면 반드시 함께 재검토:
- `01_META_PROGRESSION.md`
- Tier clear/star outcome distribution
- permanent star reward ladder
- class viability matrix
- SOLO/TEAM/AI entry rules
- account progression simulation
- late Tier difficulty
- title/profile UX

특히 achievement와 star 보상을 각각 따로 튜닝한 뒤 단순 합산해서는 안 된다.
두 시스템을 동시에 켠 account simulation이 최종 판단 기준이다.

---

# 13. Current freeze boundary

## User-confirmed direction
- 향후 칭호/업적 시스템 도입.
- 직업별 Tier 달성 업적.
- 전 직업 Tier 달성 업적.
- 특정 직업 AI 없이 순수 SOLO clear 업적.
- 특히 SOLO clear 등 일부 업적은 **클리어한 직업 이외의 다른 직업 능력치**를 영구 강화해 cross-class progression을 만든다.

## Not frozen
- achievement 총 개수
- exact Tier milestones
- exact title names
- sourceClass -> targetClass mapping
- exact stat category per achievement
- exact reward amount
- additive/multiplicative rule
- title equip gameplay effect

---

# 14. Next structural boundary

Achievement 숫자를 지금 채우지 않는다.

먼저:
1. T1/Tier ladder의 5-class viability를 계산하고,
2. 어디서 어떤 직업이 soft wall을 경험하는지 찾고,
3. star reward만으로 recovery가 얼마나 되는지 측정한 뒤,
4. 부족하거나 의미 있는 교차 지점에 achievement reward edge를 설계한다.

즉 achievement bonus가 Stage 난이도를 임의로 덮는 것이 아니라 **관측된 cross-class progression gap을 연결하는 도구**가 되어야 한다.
