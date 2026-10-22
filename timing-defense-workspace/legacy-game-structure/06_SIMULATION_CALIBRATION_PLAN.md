# Timing Defense — Simulation & Calibration Plan

Date: 2026-10-22 KST  
Status: **PRE-IMPLEMENTATION ANALYSIS PLAN**

## 1. 목적

레거시 구조자료를 실제 production 설계로 승격하기 전에, 전체 게임을 여러 층으로 나눠 계산·시뮬레이션한다.

핵심 원칙:

```text
structure
 -> authoring data
 -> deterministic simulation
 -> failure classification
 -> report
 -> discussion
 -> explicit freeze
 -> live implementation
```

## 2. Simulation layer A — Encounter micro simulation

목적:
- 한 encounter 조합이 실제 target-order에서 어떤 문제를 만드는지 확인.

입력:
- monster composition
- formation
- spawn order
- spawn cadence
- movement/capability test values
- player class/skill state

출력:
- frontline block time
- target reorder count
- backline exposure time
- peak active count
- short-window spawn density
- kill order
- wall pressure
- class-specific opportunity

특수 metric:
- SUPPORTER screened aura uptime
- SIEGER screened firing uptime / shot count
- CHARGER windup completed/interrupted ratio
- SPLITTER child-created active count and frontline occupancy
- FLYER geometry exposure

## 3. Simulation layer B — Stage simulation

한 Stage의 전체 encounter sequence를 반복 실행한다.

입력:
- base flow
- encounter events
- Stage rewards
- current run level/EXP
- shop upgrades
- class
- mastery profile
- team size

출력:
- Stage clear/fail
- clear time
- base HP remaining
- damage dealt
- kills
- EXP gain
- level/skill milestones reached
- coin gain/spend capacity
- monster-type actual count
- max active count
- 4s/6s burst density
- pressure/capability uptime

## 4. Simulation layer C — 50 Stage Tier simulation

Stage 1~50을 이어서 실행한다.

필수 출력:
- failure histogram by Stage
- 0★ rate: fail 1~19
- 1★ rate: fail 20~39
- 2★ rate: fail 40~49
- 3★ rate: clear 50
- level distribution by Stage
- Lv6/11/16/21/26/31 reach distribution
- coin/upgrades curve
- encounter repetition score
- monster-type frequency actuals
- class opportunity coverage

별 boundary 주변에서 별도 검사:
- Stage 19 -> 20
- Stage 39 -> 40
- Stage 49 -> 50

여기서 artificial difficulty cliff가 있는지 확인한다.

## 5. Simulation layer D — Account/meta progression simulation

이 게임에서는 Tier simulation만으로 충분하지 않다.
별이 account-wide permanent stats를 자동 증가시키므로 **계정 progression path**를 시뮬레이션해야 한다.

### Path A — First-class
한 직업을 거의 permanent bonus 없이 먼저 진행.

### Path B — Balanced five-class
5직업을 번갈아 플레이.

### Path C — Star-stacked
여러 직업에서 먼저 별을 얻은 후 특정 직업 진행.

### Path D — High mastery
높은 timing mastery가 빠른 별 획득과 permanent bonus snowball을 만드는지 확인.

출력:
- 별 총량 over time
- permanent stat milestones reached
- class별 Tier clear order
- first-class vs fifth-class effective difficulty
- repeat attempts per star band
- account progression time
- snowball coefficient / runaway detection

## 6. Simulation layer E — Multiplayer

2/3/4-player에서 각각 수행.

검사:
- active count/readability
- kill speed scaling
- wall pressure
- class composition
- encounter archetype viability
- human+AI mix
- shared wall upgrade impact
- class specialist starvation
- reconnect/event determinism과 독립적인 gameplay determinism

Team scaling은 먼저:
- event budget
- composition
- specialist count
- cadence/overlap
을 조절하고 global HP inflation은 후순위로 둔다.

## 7. Mastery profiles

기존 simulation profile을 참고하되 final calibration profile은 다시 정의한다.

최소 profile:
- lower/learning
- average
- skilled
- high mastery stress

각 profile은:
- NORMAL/GOOD/PERFECT distribution
- input cadence
- heavy completion
- combo maintenance
을 명시적으로 가진다.

## 8. Skill authority mismatch 처리

현재:
- Lv6 authoritative
- Lv11/16/21 exact legacy parity candidate
- Lv26 design-only
- Lv31 unresolved

따라서 simulation은 mode를 분리한다.

### MODE CURRENT_AUTHORITY
현재 live authority만 반영.
장점: 현재 구현과 정확히 비교 가능.
한계: 50-stage late progression 분석 불충분.

### MODE LEGACY_PARITY_CANDIDATE
Lv11/16/21 exact legacy formulas 포함.
목적: parity 적용 시 campaign 영향 예측.

### MODE FUTURE_SKILL_PLACEHOLDER
Lv26/31을 production 숫자로 가정하지 않고 구조적 power budget 범위로만 stress-test.
결과는 freeze 근거가 아니라 decision input이다.

## 9. Permanent stat calibration

영구 stat은 별도 parameter sweep으로 결정한다.

평가 기준:
- 새 계정 첫 직업이 불합리하게 어렵지 않은가
- 5번째 직업이 지나치게 trivial해지지 않는가
- Tier 하나를 3★로 만든 보상이 체감되는가
- 별 milestone 사이 공백이 너무 길지 않은가
- 특정 class가 shared stat에서 과도한 효율을 얻지 않는가
- crit/damage/defense가 multiplicative snowball을 만들지 않는가

구체 threshold와 수치는 sweep 결과 후 제안한다.

## 10. Encounter frequency calibration

Tier별로 다음 target/actual을 비교한다.

- monster spawn share
- encounter presence share
- pressure-family presence
- archetype frequency
- formation frequency
- cadence frequency
- geometry frequency
- backline-screen time
- capability uptime

단순 `% 몬스터 수` 하나로 Tier identity를 판정하지 않는다.

## 11. Readability guardrail

과거 5종 recipe의 4s/6s burst density는 historical benchmark로 보존하되 현재 9종 roster로 새로 측정한다.

특히 SPLITTER는 authored spawn보다 actual entity volume이 커지므로:
- authored spawn count
- effective spawn count
- peak active count
을 분리한다.

SUPPORTER/SIEGER는 개체 수보다 uptime이 더 중요하므로 별도 pressure-time metric을 사용한다.

## 12. Determinism

동일:
- Tier data version
- Stage data
- seed
- class/team
- mastery profile
- permanent stats
- shop policy
이면 동일 결과를 재현 가능해야 한다.

시뮬레이션 report에는 반드시:
- data version/hash
- seed range
- number of runs
- model mode
를 기록한다.

## 13. Failure classification

수정 전에 실패 원인을 분류한다.

- TOO_MANY_ENTITIES
- FRONTLINE_SCREEN_TOO_LONG
- SIEGE_UPTIME_TOO_HIGH
- CHARGE_WINDOW_UNREADABLE
- REPLICATION_EXPLOSION
- DURABILITY_SPIKE
- CADENCE_COMPRESSION
- CLASS_STARVATION
- SKILL_POWER_SPIKE
- SHOP_SNOWBALL
- PERMANENT_STAT_SNOWBALL
- STAR_BOUNDARY_CLIFF
- TEAM_SCALING_DEFECT

한 원인을 global HP/count patch로 덮지 않는다.

## 14. 첫 simulation tranche

구조 문서 완료 후 첫 실행은 production 250-stage 전체가 아니라 다음 순서가 안전하다.

1. 9종 pair/synergy micro encounter
2. 20개 encounter archetype smoke simulation
3. 10-stage synthetic Tier slice
4. 50-stage single Tier candidate
5. 2/3/4-player expansion
6. 5-class account star progression
7. multiple Tier campaign

각 tranche가 구조적으로 통과한 뒤 범위를 늘린다.

## 15. Freeze gate

다음 항목은 simulation만으로 자동 freeze하지 않는다.
- monster production numbers
- encounter frequencies
- Tier identities
- star permanent-stat thresholds
- permanent-stat coefficients
- shop frequency/economy
- boss cadence
- Lv26/31 skill contract

시뮬레이션은 decision support이며 최종 production 변경은 명시적 승인 후 수행한다.
