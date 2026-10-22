# Timing Defense — Monster Encounter Model

Date: 2026-10-22 KST  
Status: **NEW STRUCTURAL TAXONOMY / S-E-X DEMOTED TO LEGACY MAPPING**

## 1. 목적

현재 9종 ordinary monster를 기준으로 Tier/Stage별:
- 종별 빈도
- 개수
- 조합
- 전열/후열 배치
- 등장 순서
- spawn cadence
- geometry
- target-order 변화
를 구조적으로 authoring하기 위한 공통 언어를 정의한다.

## 2. 왜 S/E/X를 주 분류에서 내리는가

기존 `S / E / X`는 5종 roster 시절에는 유용한 압축 문법이었다.
그러나 현재 `X` 하나에 FLYER/CHARGER/SPLITTER/SUPPORTER/SIEGER처럼 전혀 다른 mechanic이 뭉개지고, BRUTE/SHIELD 차이와 전열 screening 효과도 충분히 표현하지 못한다.

따라서:
- 기존 S/E/X = `LEGACY_ANALYSIS_REFERENCE`
- 신규 authoring = **Pressure Family + Encounter Archetype + Formation + Cadence**

## 3. Monster roster — CURRENT_FROZEN_STRUCTURE

9 ordinary archetypes:
- GRUNT — baseline/reference
- RUNNER — sustained speed
- BRUTE — raw durability + knock resistance
- SHIELD — damage mitigation
- FLYER — authoritative vertical geometry
- CHARGER — telegraphed burst movement
- SPLITTER — death -> 2 nonrecursive children
- SUPPORTER — nonstacking movement-speed aura
- SIEGER — standoff repeated ranged wall attack

Boss는 별도 composition layer다.

## 4. Targeting constraint — 핵심 전제

현재 core combat은 free manual targeting이 아니다.
기본 direct attack/AI/passive는 system-driven target acquisition을 사용하며, 실질적으로 가장 전열에 가까운 valid target이 우선된다.

따라서 encounter의 난이도는 단순 monster list가 아니라 **누가 앞에 있고 누가 얼마나 오래 가려지는가**에 크게 좌우된다.

예:
- SHIELD + SIEGER: SHIELD가 전열을 잡는 동안 SIEGER가 후열에서 wall pressure를 유지할 수 있음.
- BRUTE + SUPPORTER: BRUTE의 높은 체류시간이 SUPPORTER exposure를 늦춤.
- SPLITTER가 전열에서 사망: 두 child가 새 전열 점유를 만들 수 있음.

직업 스킬의 penetration/AoE는 이 규칙을 우회하는 `soft advantage`이지 manual target selection이 아니다.

## 5. 신규 Pressure Family

`BASELINE`은 중립 filler/reference이며 pressure family count에서 별도 취급할 수 있다.

| Code | 이름 | 전술 문제 | 대표 기여 monster |
|---|---|---|---|
| BASELINE | 기본 진군 | 중립 기준/혼합 가독성 | GRUNT |
| FLOOD | 물량 압박 | 전열이 계속 채워지고 처리량 요구 증가 | GRUNT, SPLITTER children |
| RUSH | 속공 압박 | 반응 시간과 전선 여유 감소 | RUNNER |
| BULWARK | 방벽 압박 | 전열 체류시간 증가, 후열 screening | BRUTE, SHIELD |
| BREACH | 돌파 압박 | telegraph 후 순간적 전선 붕괴 위험 | CHARGER |
| AERIAL | 공중/공간 압박 | Y geometry 변화, line/AoE 관계 변화 | FLYER |
| REPLICATE | 증식 압박 | 처치가 즉시 entity 감소로 이어지지 않음 | SPLITTER |
| SUPPORT | 지원진형 압박 | formation 전체 이동 tempo 강화 | SUPPORTER |
| SIEGE | 공성 압박 | 후열에서 base를 반복 공격 | SIEGER |

한 monster는 encounter 문맥상 복수 family에 기여할 수 있다.
예: SPLITTER 다수는 REPLICATE이면서 FLOOD를 만든다.

## 6. BULWARK 세부분류

BRUTE와 SHIELD를 같은 이름으로 뭉개지 않도록 하위 role을 구분한다.

- `RAW_ANCHOR` — BRUTE 중심. HP/knock resistance로 전열 체류.
- `ARMOR_SCREEN` — SHIELD 중심. mitigation으로 전열 체류.
- `MIXED_WALL` — BRUTE + SHIELD.

Stage authoring은 BULWARK 빈도뿐 아니라 어느 subtype인지 기록한다.

## 7. Formation vocabulary

### FRONT
가장 먼저 system target이 되는 전열.

### MID
전열 제거 후 노출되는 중열.

### BACK
SUPPORTER/SIEGER 등 장시간 보호 시 효과가 커지는 후열.

### AIR OFFSET
FLYER의 authoritative Y geometry를 이용하는 상대적 공간층.

### LINE
관통 가치가 높은 정렬.

### CLUSTER
AoE 가치가 높은 밀집.

### SCATTER
특정 specialist geometry가 덜 안정적인 분산.

### SPLIT
시간/공간적으로 분리된 두 묶음 이상.

## 8. Spawn cadence vocabulary

- `DRIP` — 일정한 저밀도 지속 spawn
- `WAVE` — 구분 가능한 묶음 단위
- `BURST` — 짧은 시간 다수 spawn
- `ESCORT` — 보호 대상과 screen이 의도된 순서로 spawn
- `STAGGER` — 종류별 간격을 두어 target order 변화 유도
- `OVERLAP` — 이전 encounter가 살아 있는 상태에서 다음 encounter 진입
- `LATE_INSERT` — 후반에 SUPPORTER/SIEGER/CHARGER 등 핵심 threat 추가

정확한 ms/sec 값은 Tier/Stage data에서 calibration한다.

## 9. Encounter Archetype library v0.1

아래는 **구조 archetype**이며 exact count/수치는 아직 freeze하지 않는다.

### E01 — BASELINE_MARCH / 기본 진군
- core: GRUNT
- purpose: 기준 flow, recovery/readability

### E02 — RUSH_WAVE / 속공 파도
- core: RUNNER + optional GRUNT
- pressure: RUSH
- key variable: spawn spacing / peak active

### E03 — HEAVY_LINE / 중장 전열
- core: BRUTE
- pressure: BULWARK:RAW_ANCHOR

### E04 — SHIELD_SCREEN / 방패막
- core: SHIELD + ordinary followers
- pressure: BULWARK:ARMOR_SCREEN
- key: screen duration

### E05 — MIXED_WALL / 혼합 방벽
- core: BRUTE + SHIELD
- pressure: BULWARK

### E06 — AIR_PRESSURE / 공중 압박
- core: FLYER + baseline ground
- pressure: AERIAL
- key: Y geometry and line/AoE opportunity

### E07 — CHARGE_BREAK / 돌파 충격
- core: CHARGER + baseline
- pressure: BREACH
- key: windup opportunity and interruption rate

### E08 — SPLIT_FLOOD / 분열 범람
- core: SPLITTER + GRUNT
- pressure: REPLICATE + FLOOD
- key: post-kill entity volume

### E09 — SUPPORT_COLUMN / 지원 종대
- core: SUPPORTER + ordinary formation
- pressure: SUPPORT
- key: aura uptime while screened

### E10 — SIEGE_LINE / 공성선
- core: SIEGER + light frontline
- pressure: SIEGE
- key: first-shot time / firing uptime

### E11 — ESCORT_SIEGE / 호위 공성
- core: SHIELD or BRUTE frontline + SIEGER backline
- pressure: BULWARK + SIEGE
- key: backline protection duration

### E12 — BUFFED_BULWARK / 강화 방벽
- core: BRUTE/SHIELD + SUPPORTER
- pressure: BULWARK + SUPPORT
- key: support aura effect on screen durability-through-time

### E13 — RUSH_BREACH / 속공 돌파
- core: RUNNER + CHARGER
- pressure: RUSH + BREACH
- key: sustained speed + burst timing separation

### E14 — AIR_RUSH / 공중 속공
- core: RUNNER + FLYER
- pressure: RUSH + AERIAL

### E15 — REPLICATE_RUSH / 증식 속공
- core: SPLITTER + RUNNER
- pressure: REPLICATE + RUSH
- key: target reorder after split

### E16 — CASCADE / 연쇄 증식
- core: SPLITTER + SUPPORTER
- pressure: REPLICATE + SUPPORT
- key: child population and aura interaction

### E17 — BREACH_SCREEN / 돌파 엄호
- core: BRUTE/SHIELD screen + CHARGER
- pressure: BULWARK + BREACH
- key: whether CHARGER trigger occurs while protected

### E18 — DUAL_AXIS / 이중축 압박
- core: FLYER + SIEGER + ground screen
- pressure: AERIAL + SIEGE
- key: spatial geometry plus objective uptime

### E19 — FORTRESS / 요새
- core: SHIELD/BRUTE + SUPPORTER + SIEGER
- pressure: BULWARK + SUPPORT + SIEGE
- high-complexity archetype; late use only unless intentionally tutorialized

### E20 — COLLAPSE_CHAIN / 붕괴 연쇄
- core: SPLITTER + CHARGER + fast/baseline support
- pressure: REPLICATE + BREACH + optional FLOOD/RUSH
- high-complexity archetype

이 library는 확장 가능하지만, 새 archetype은 기존 것과 실제 player problem이 달라야 한다.

## 10. Encounter signature

Stage 반복 판정은 단순 monster type set이 아니라 다음 signature를 사용한다.

```text
signature =
  archetypeId
  + composition bucket
  + formation
  + cadence
  + geometry
  + timing window
  + intensity bucket
```

같은 `SHIELD + SIEGER`라도:
- screen이 먼저 도착하는 escort
- 거의 동시 도착하는 cluster
- SIEGER late insert
는 서로 다른 encounter다.

## 11. 빈도/개수 데이터

각 Tier/Stage에서 monster type마다 최소 다음 지표를 가진다.

- authoredSpawnCount
- effectiveSpawnCount (SPLITTER child 포함)
- spawnShare
- stagePresence
- meaningfulThreatPresence
- meanConcurrent
- peakConcurrent
- survivalTime
- frontlineTime
- backlineTime
- capabilityUptime

특수 지표:
- CHARGER: windups / completed charges / interrupted charges
- SPLITTER: parents / children / child frontline time
- SUPPORTER: aura uptime / screened aura uptime
- SIEGER: windups / shots / screened firing uptime
- FLYER: line/cluster geometry opportunity time

## 12. Team-size scaling

2/3/4-player scaling 우선순위:
1. encounter event budget
2. composition complexity
3. specialist threat count
4. cadence/overlap
5. 필요할 때만 제한적 durability adjustment

모든 monster에 동일한 global HP multiplier를 먼저 적용하지 않는다.

읽기 가능성은 total count보다 short-window density와 active concurrency로 제한한다.

## 13. Class opportunity mapping

Hard lockout 없이 soft advantage만 만든다.

- Knight: mixed/reordering/generalist/penetration
- Rogue: durable normal / high-value frontline body
- Tank: knockback, CHARGER interrupt, wall pressure control
- Archer: aligned line / screened backline penetration opportunity
- Mage: cluster / SPLITTER children / density

이 mapping은 encounter authoring 검사에 사용하되 모든 Stage에서 모든 직업을 동일하게 강하게 만들지는 않는다.

## 14. 기존 S/E/X mapping

역사 자료를 새 구조로 읽기 위한 대략적 mapping:
- old S -> FLOOD / RUSH 중심
- old E -> BULWARK 중심
- old X -> AERIAL / BREACH / REPLICATE / SUPPORT / SIEGE 및 mixed

이는 변환 참고용이며 신규 authoring ID로 사용하지 않는다.

## 15. 다음 단계

1. 각 Tier의 available archetype set 정의
2. 50 Stage에 encounter archetype frequency 후보 배정
3. monster type frequency와 effective entity count 계산
4. target-order/backline uptime micro-sim
5. 2/3/4-player density simulation
6. class opportunity starvation 검사
7. 결과 보고 후 frequency/count/cadence freeze
