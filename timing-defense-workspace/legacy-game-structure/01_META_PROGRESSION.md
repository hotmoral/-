# Timing Defense — Meta Progression Structure

Date: 2026-10-22 KST  
Status: **USER_CONFIRMED_STRUCTURE + OPEN NUMERICAL DESIGN**

## 1. 목적

게임 외부/장기 성장 구조를 정의한다.
핵심은 **직업별 독립 Tier 진행**과 **전체 계정 공유 별 기반 영구 성장**을 분리하는 것이다.

## 2. 직업별 독립 Tier 진행

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

## 3. Tier attempt와 별

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

## 4. Global Star Total

```text
GlobalStarTotal = sum(bestStars[class][tier])
```

별은 **소비하지 않는다**.
별은 계정 성취도의 누적 지표다.

예:
- Tier 1만 존재하고 5직업 모두 3★: 15★
- Tier 1~2에서 5직업 모두 3★: 30★

## 5. 영구 stat

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

중요: 별은 자동 보상 구조이므로 사용자가 별을 어디에 소비할지 선택하는 skill tree/currency와 동일하게 취급하지 않는다.

## 6. Run progression과 Permanent progression 분리

### Run-local
Tier attempt 시작 시 초기화되는 계층:
- level
- EXP
- run coin
- stage shop upgrade
- 기타 run-only temporary growth

### Account-permanent
Run 종료 후에도 유지:
- 직업별 Tier 최고 별 기록
- GlobalStarTotal
- GlobalStarTotal에 의해 자동 해금된 permanent stats

이 둘을 데이터 모델과 시뮬레이터에서 반드시 분리한다.

## 7. 파생되는 중요한 밸런스 문제

### 7.1 성장 순서 편향
공용 영구 stat 때문에 플레이 순서가 결과에 영향을 줄 수 있다.

예:
1. Knight를 먼저 진행할 때는 permanent bonus가 적다.
2. 다른 4직업에서 별을 많이 모은 뒤 Knight를 시작하면 같은 Tier가 더 쉬워질 수 있다.

따라서 단일 직업 clear rate만 보면 안 된다.
시뮬레이션에서 최소 다음 경로를 비교한다.
- first-class path: 거의 영구 보상 없이 첫 직업 진행
- balanced path: 5직업을 번갈아 진행
- stacked path: 여러 직업의 별을 먼저 확보한 뒤 한 직업 진행
- high-mastery path / average path

### 7.2 Snowball risk
영구 stat이 너무 크면:
`별 획득 -> 공용 강화 -> 다음 별 획득 쉬움 -> 추가 강화`
의 양성 피드백이 지나치게 커진다.

### 7.3 Class fairness
공용 보상은 모든 직업에 동일하게 적용되므로, 특정 stat이 어떤 직업에 지나치게 큰 효율을 주는지 확인해야 한다.
예: crit 계열이 특정 multihit class에 더 큰 기대값을 줄 가능성.

## 8. Tier unlock — OPEN_DECISION

사용자 확정 내용은 “각 직업이 독립적으로 Tier를 깨 나간다”까지다.

아직 명문화가 필요한 세부:
- 다음 Tier unlock 조건이 반드시 이전 Tier Stage 50 clear인지
- 1★/2★로도 다음 Tier 진입을 허용하는지
- 한번 unlock한 Tier는 permanent인지
- 최고 unlocked Tier를 lobby default로 어떻게 정하는지

현재 authoring/simulation에서는 이 값을 parameter로 둔다.
Production 구현 전 반드시 명시적으로 freeze한다.

## 9. Multiplayer progression — OPEN_DECISION

서로 다른 직업/Tier 진행도를 가진 플레이어가 TEAM으로 만날 경우 필요한 규칙:
- 방 Tier를 host 기준으로 정할지
- 모든 인간 참가자가 해당 Tier를 unlock해야 하는지
- 낮은 진행도 유저를 허용할지
- 별 판정을 각자의 선택 직업 기록에 동일하게 반영할지

이는 encounter scaling과 별 progression에 직접 영향을 주므로 별도 decision gate로 관리한다.

## 10. 저장 데이터 최소 모델

```text
AccountProgress
  permanentStats
  globalStarTotal  // derived or cached
  classes
    knight
      highestUnlockedTier
      tierRecords
        T1 { bestStars, bestStage, clears, attempts }
        T2 { ... }
    rogue ...
    tank ...
    archer ...
    mage ...
```

`globalStarTotal`은 서버/저장소에서 검증 가능한 파생값이어야 하며 클라이언트 임의 입력을 신뢰하지 않는다.

## 11. 다음 설계 입력

이 문서가 고정한 구조를 바탕으로 이후 다음을 계산한다.
- Tier 개수에 따른 최대 별 수
- 별 milestone reward ladder
- permanent stat 총 누적폭
- first-class vs fifth-class 난이도 차이
- 1★/2★/3★ 획득 확률 곡선
- 한 Tier에서 평균 attempt 수
- 전체 5직업 progression 시간
