# Timing Defense — Meta Progression Structure

Date: 2026-10-22 KST  
Status: **USER_CONFIRMED_STRUCTURE + OPEN NUMERICAL DESIGN**

## 1. 목적

게임 외부/장기 성장 구조를 정의한다.

핵심은 네 계층을 분리하면서 서로 연결하는 것이다.

1. **직업별 독립 Tier 진행**
2. **별 기반 broad account progression**
3. **업적 기반 targeted cross-class progression**
4. **run-local EXP / level / coin / shop progression**

본질:

> 한 직업이 현재 계정 성장도로 특정 Tier에서 막힐 수 있고, 다른 직업을 진행해 별과 업적을 획득한 뒤 공용/교차 영구성장을 통해 원래 막힌 직업으로 돌아와 전진할 수 있어야 한다.

이 의도된 루프를 **Cross-Class Progression Loop**라고 부른다.

```text
Class A blocked
 -> Class B/C/D progresses
 -> stars + achievements
 -> account / target-class permanent power rises
 -> return to Class A
 -> previous soft wall becomes attainable
```

---

# 2. 직업별 독립 Tier 진행

대상 직업:
- Knight
- Rogue
- Tank
- Archer
- Mage

각 직업은 별도의 Tier 진행 상태를 가진다.

예시:

```text
Knight  T1 ★★★  T2 ★★  T3 locked/open TBD
Rogue   T1 ★★★  T2 ★
Tank    T1 ★★
Archer  T1 ★★★  T2 ★★★
Mage    T1 ★
```

한 직업의 Tier 성취가 다른 직업의 Tier clear를 대신하지 않는다.

그러나 한 직업의 성취는 별/업적을 통해 **다른 직업의 미래 진행 기반**을 만들 수 있다.

같은 Tier의 Stage authoring data는 직업별로 따로 만들지 않는 것을 기본 방향으로 한다.
같은 시험을 서로 다른 class kit와 서로 다른 계정 성장상태로 통과한다.

---

# 3. Tier attempt와 별

한 Tier는 50 Stage.

Attempt 종료 시 도달/실패 구간으로 별을 계산한다.

| 종료 결과 | Attempt star result |
|---|---:|
| Stage 1~19 실패 | 0★ |
| Stage 20~39 실패 | 1★ |
| Stage 40~49 실패 | 2★ |
| Stage 50 클리어 | 3★ |

저장 규칙:

```text
classTierBestStars = max(previousBestStars, attemptStars)
```

따라서 동일 `직업 x Tier`는 최대 3★이며, 재도전으로 별을 중복 획득하지 않는다.

---

# 4. Global Star Total

```text
GlobalStarTotal = sum(bestStars[class][tier])
```

별은 **소비하지 않는다**.
별은 계정 성취도의 누적 지표다.

예:
- Tier 1만 존재하고 5직업 모두 3★: 15★
- Tier 1~2에서 5직업 모두 3★: 30★

---

# 5. 별 기반 영구 stat — broad foundation

GlobalStarTotal이 특정 milestone을 넘으면 모든 직업에 적용되는 영구 stat이 자동 해금된다.

후보 stat category:
- base attack
- critical chance
- critical damage
- wall/base HP
- defense
- knockback/control 계열
- 기타 공용 성장 항목

현재 확정하지 않는 것:
- 별 milestone 간격
- 각 milestone의 stat 종류
- 증가량
- additive/multiplicative stacking
- 최대치

중요:
- 별은 자동 보상 구조다.
- 별을 어디에 소비할지 선택하는 currency/skill tree와 동일하게 취급하지 않는다.
- 별 보상의 역할은 특정 직업 하나를 겨냥하기보다 **전체 계정의 바닥 전투력을 넓게 들어 올리는 것**이다.

---

# 6. 업적/칭호 기반 교차 영구성장 — targeted bridges

별 시스템과 별도로 향후 **Achievement / Title** layer를 둔다.

상세 구조:
`15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`

사용자 확정 방향:
- 직업별 특정 Tier 달성 업적
- 전 직업 특정 Tier 달성 업적
- 특정 직업으로 AI 없이 순수 SOLO Tier clear 업적
- 특히 SOLO clear 등 일부 업적은 **클리어한 직업이 아닌 다른 직업의 특정 능력치**를 영구 강화

역할 구분:

```text
Stars        = broad account foundation
Achievements = targeted cross-class bridges
Titles       = achievement presentation/collection layer
```

Achievement reward는 source class와 target class가 다른 방향 edge를 가질 수 있다.

예시 형식:

```text
SOLO_NO_AI_CLEAR(sourceClass=A, tier=T)
 -> targetClass=B
 -> targetStat=TBD
 -> permanentValue=TBD
```

정확한 A->B mapping/stat/value는 아직 freeze하지 않는다.

---

# 7. Run progression과 Permanent progression 분리

## Run-local
Tier attempt 시작 시 초기화되는 계층:
- level
- EXP
- run coin
- stage shop upgrade
- 기타 run-only temporary growth

## Account-permanent
Run 종료 후에도 유지:
- 직업별 Tier 최고 별 기록
- GlobalStarTotal
- GlobalStarTotal에 의해 자동 해금된 broad permanent stats
- achievement completion records
- achievement reward로 해금된 account-wide / target-class permanent modifiers
- unlocked titles

이 둘을 데이터 모델과 시뮬레이터에서 반드시 분리한다.

---

# 8. 의도된 class viability 철학

신규/저성장 계정에서 모든 직업이 같은 Tier를 같은 난이도로 clear할 필요는 없다.

허용:
- 직업마다 같은 Tier에서 상대적 유불리가 있음
- 특정 직업이 현재 account power에서 soft wall을 만남
- 다른 직업 progression 후 permanent growth를 얻고 재도전하여 돌파

금지:
- 특정 직업이 구조적으로 attack/interaction 불가능해서 영구성장과 무관하게 진행 불가
- 특정 업적 하나 없이는 사실상 진행 자체가 닫히는 hard dependency
- 한 직업만 먼저 키우는 것이 모든 상황에서 압도적인 정답이 되는 dominant route

따라서 `hard class lockout` 금지와 `soft progression wall` 허용을 명확히 구분한다.

---

# 9. 파생되는 중요한 밸런스 문제

## 9.1 성장 순서 편향
공용/교차 영구 stat 때문에 플레이 순서가 결과에 영향을 준다.

이것은 전부 제거할 대상이 아니다.
**의도적으로 의미 있는 순서 차이**는 게임 구조의 일부다.

다만 한 경로만 지배적으로 최적이 되지 않게 한다.

시뮬레이션 최소 경로:
- first-class path: 거의 영구 보상 없이 첫 직업 진행
- balanced path: 5직업을 번갈아 진행
- stacked path: 여러 직업의 별을 먼저 확보한 뒤 한 직업 진행
- favorite-class-first path
- weak-class-recovery path
- achievement-focused solo mastery path
- high-mastery path / average path

## 9.2 Snowball risk

별:
```text
별 획득 -> 공용 강화 -> 다음 별 획득 쉬움 -> 추가 강화
```

업적까지 포함하면:
```text
class clear -> stars + achievement
 -> account/other-class 강화
 -> 다른 class clear
 -> additional stars + achievement
 -> further acceleration
```

이 피드백은 의도된 progression engine이지만 runaway가 되면 안 된다.

## 9.3 Class fairness vs class asymmetry
공용 보상은 같은 raw stat이라도 직업별 실제 기대효율이 다를 수 있다.

예:
- crit 보너스가 multihit 구조에 더 높은 기대효율을 낼 수 있음
- knockback 보너스가 Tank/CHARGER interaction에서 더 높은 utility를 낼 수 있음

따라서 `같은 표기 수치 = 같은 class 가치`라고 가정하지 않는다.

## 9.4 Achievement circular deadlock

금지 예:
```text
A 업적이 있어야 B clear 가능
B 업적이 있어야 A clear 가능
```

신규 계정에서 합리적인 seed progression path가 반드시 존재해야 한다.

## 9.5 Solo/co-op incentive balance
AI-free solo achievement는 mastery reward다.

따라서:
- 일반 Tier/star progression은 SOLO/AI/TEAM 구조를 통해 진행 가능
- solo-no-AI 업적은 추가적인 교차 성장 보상
- 너무 강해서 모든 유저에게 사실상 강제되는 구조는 피함

---

# 10. Tier unlock — OPEN_DECISION

사용자 확정 내용은 “각 직업이 독립적으로 Tier를 깨 나간다”까지다.

아직 명문화가 필요한 세부:
- 다음 Tier unlock 조건이 반드시 이전 Tier Stage 50 clear인지
- 1★/2★로도 다음 Tier 진입을 허용하는지
- 한번 unlock한 Tier는 permanent인지
- 최고 unlocked Tier를 lobby default로 어떻게 정하는지

현재 authoring/simulation에서는 parameter로 둔다.
Production 구현 전 반드시 명시적으로 freeze한다.

---

# 11. Multiplayer progression — OPEN_DECISION

서로 다른 직업/Tier 진행도를 가진 플레이어가 TEAM으로 만날 경우 필요한 규칙:
- 방 Tier를 host 기준으로 정할지
- 모든 인간 참가자가 해당 Tier를 unlock해야 하는지
- 낮은 진행도 유저를 허용할지
- 별 판정을 각자의 선택 직업 기록에 동일하게 반영할지
- TEAM clear가 achievement family별로 어떻게 인정되는지

특히 `SOLO_NO_AI_TIER_CLEAR`는 다음을 요구한다.

```text
humanPlayerCount = 1
aiCount = 0
run start -> Stage50 clear 동안 해당 조건 유지
```

Reconnect는 동일 authoritative run 복구라면 solo 상태를 깨는 것으로 보지 않을 수 있다.
정확한 truth contract는 achievement 문서에서 관리한다.

---

# 12. 저장 데이터 최소 모델

```text
AccountProgress
  globalStarTotal  // derived or cached
  accountPermanentStats
  achievementCompletions{}
  achievementPermanentModifiers{}
  unlockedTitles{}

  classes
    knight
      highestUnlockedTier
      classPermanentModifiers{}
      tierRecords
        T1 { bestStars, highestReachedStage, clears, attempts }
        T2 { ... }
    rogue ...
    tank ...
    archer ...
    mage ...
```

`globalStarTotal`은 서버/저장소에서 검증 가능한 파생값이어야 하며 클라이언트 임의 입력을 신뢰하지 않는다.

Achievement completion도 authoritative run/history에서 검증 가능해야 한다.

---

# 13. Meta progression 전체 그래프

```text
COMMON TIER/STAGE CONTENT
        ↓
CLASS-SPECIFIC ATTEMPTS
        ↓
+----------------------+----------------------+
|                                             |
STAR RESULT                                  ACHIEVEMENT CONDITIONS
|                                             |
GLOBAL STAR TOTAL                            CROSS-CLASS REWARD EDGES
|                                             |
BROAD ACCOUNT STATS                          TARGETED ACCOUNT/CLASS STATS
+----------------------+----------------------+
        ↓
NEXT CLASS / RETRY BLOCKED CLASS
        ↓
NEW STARS + NEW ACHIEVEMENTS
```

이 순환은 게임의 장기 progression engine이다.

---

# 14. 다음 설계 입력

이 문서가 요구하는 향후 계산:
- Tier 개수에 따른 최대 별 수
- 별 milestone reward ladder
- achievement family/list 후보
- sourceClass -> targetClass reward graph
- permanent stat 총 누적폭
- first-class vs fifth-class 난이도 차이
- soft-wall recovery 효과
- 1★/2★/3★ 획득 확률 곡선
- 한 Tier에서 평균 attempt 수
- 전체 5직업 progression 시간
- solo-no-AI achievement 난이도/보상비
- progression graph reachability
- dominant route 여부
- stars + achievements combined snowball

Achievement 수치 설계는 Stage 난이도를 임의로 덮는 방식이 아니라, 실제 simulation에서 관측된 cross-class progression gap을 연결하는 방식으로 수행한다.
