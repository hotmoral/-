# Timing Defense — Simulation & Calibration Plan

Date: 2026-10-22 KST  
Status: **PRE-IMPLEMENTATION ANALYSIS PLAN / MASTER-SPINE ALIGNED**

## 1. 목적

Production 설계 승격 전 전체 게임을 여러 층으로 나눠 deterministic하게 계산·시뮬레이션한다.

상위 기준:
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`

핵심 절차:

```text
master spine
 -> campaign matrix
 -> authoring data
 -> deterministic simulation
 -> failure classification
 -> report
 -> discussion
 -> explicit freeze
 -> live implementation
```

현재는 이전 T1 micro-sim보다 **Master Campaign Matrix 선행**이 우선이다.

---

# 2. Simulation layer 0 — Campaign Spine validation

세부 encounter 전에 먼저 검증한다.

입력:
- Tier count candidate: 4 / 5 / 6
- Tier novelty budget
- monster availability/unlock ladder
- 50-Stage macro role
- expected run skill-reach window
- expected meta-power state
- skilled clear-rate target envelope

출력:
- total successful Stage volume
- max stars
- monster novelty spacing
- empty/overloaded Tier detection
- skill-novelty collision
- meta-progression room
- future monster expansion room

이 layer가 통과하지 않으면 T1 exact monster count/cadence를 더 세밀화하지 않는다.

---

# 3. Simulation layer A — Encounter micro simulation

목적:
- 한 encounter 조합이 실제 target-order에서 어떤 문제를 만드는지 확인.

입력:
- monster composition
- formation
- spawn order
- spawn cadence
- movement/capability candidate values
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
- CHARGER completed/interrupted ratio
- SPLITTER child active/frontline occupancy
- FLYER geometry exposure

---

# 4. Simulation layer B — Stage simulation

입력:
- base flow
- encounter events
- Stage rewards
- run level/EXP
- shop upgrades
- class
- mastery profile
- team size
- meta-power profile

출력:
- clear/fail
- clear time
- base HP remaining
- damage/kills
- EXP/level/skill reach
- coin/spend capacity
- monster actual count
- peak active
- 4s/6s density
- pressure/capability uptime

---

# 5. Simulation layer C — 50 Stage Tier simulation

Stage1~50을 이어서 실행한다.

필수 출력:
- failure histogram by Stage
- 0★ fail 1~19
- 1★ fail 20~39
- 2★ fail 40~49
- 3★ clear 50
- full-Tier clear probability
- level distribution
- Lv6/11/16/21/26/31 reach distribution
- coin/upgrades curve
- encounter repetition
- monster-type actual frequency
- class opportunity coverage

별 boundary 별도 검사:
- 19→20
- 39→40
- 49→50

---

# 6. Difficulty calibration — USER-CONFIRMED TARGET

## 6.1 기본 목표

Tier1을 제외한 일반 campaign Tier의 기본 calibration rule:

> **SKILLED_V2 기준 full-Tier clear probability < 60%.**

60%는 목표 중앙값이 아니라 **상한 기준**이다.
특별한 제품 의도가 없는데 60% 이상이면 `TOO_EASY_FOR_SKILLED`로 분류한다.

## 6.2 T1 exception

T1은 onboarding/first-contact 역할 때문에 숙련자 clear rate를 더 높게 허용할 수 있다.
T1 exact target은 OPEN_DECISION이다.

다만 prototype처럼 숙련자에게 사실상 자동 clear가 되는 수준은 지양한다.

## 6.3 측정 단위

기본 clear rate:

```text
attempt starts Stage1
 -> continuous Tier run
 -> Stage50 clear
```

즉 개별 Stage clear rate가 아니라 **Tier 3★ full-run probability**다.

## 6.4 평가 progression state

다음 상태에서 측정한다.
- 해당 Tier를 처음 의미 있게 공략하는 intended-entry account state
- 해당 class의 예상 star/achievement support 범위
- intended run skill progression

과성장 replay account는 별도 `OVERGROWN` profile로 본다.

## 6.5 Class asymmetry

모든 class가 같은 clear rate일 필요는 없다.
일부 class가 훨씬 낮아 soft wall을 만드는 것은 허용한다.

단:
- hard interaction lockout 금지
- stars/achievements로 회복 가능한 경로 필요

---

# 7. Mastery profiles — 재정의

기존 profile을 그대로 쓰지 않는다.

최소 profile:
- LEARNING
- AVERAGE
- SKILLED_V2
- HIGH_MASTERY_STRESS

## SKILLED_V2 philosophy

사용자 직접 플레이 관찰을 calibration evidence로 반영한다.
- 집중하면 combo 40은 쉽게 달성 가능한 수준
- 현재 prototype Stage 난도는 너무 낮았음

따라서:
- combo 40을 high-mastery-only event로 취급하지 않는다.
- high combo maintenance probability를 기존 skilled보다 높게 잡는다.
- timing accuracy / heavy completion / recovery discipline도 재산정한다.
- HIGH_MASTERY_STRESS는 SKILLED_V2보다 명확히 상위다.

아직 freeze하지 않는 parameter:
- PERFECT/GOOD/NORMAL distribution
- combo survival model
- miss/error rate
- heavy completion rate
- reaction/cadence distribution

이 값은 실제 플레이 데이터/테스트를 받아 parameterize한다.

---

# 8. Simulation layer D — Account/meta progression

Stars + achievements를 함께 본다.

최소 path:
- FIRST_CLASS
- BALANCED_FIVE_CLASS
- STAR_STACKED
- FAVORITE_CLASS_FIRST
- WEAK_CLASS_RECOVERY
- ACHIEVEMENT_FOCUSED_SOLO
- HIGH_MASTERY

출력:
- stars over time
- permanent milestones
- achievement completions
- target-class modifiers
- class clear order
- first-class vs later-class difficulty
- repeat attempts
- account progression time
- snowball coefficient
- dominant-route detection
- graph reachability

---

# 9. Simulation layer E — Multiplayer

2/3/4-player에서:
- active count/readability
- kill speed scaling
- wall pressure
- composition viability
- AI/human mix
- shared wall upgrade impact
- specialist starvation

Scaling priority:
1. event budget
2. composition
3. specialist count
4. cadence/overlap
5. limited durability adjustment

Global HP inflation은 후순위다.
Solo campaign spine을 먼저 닫은 뒤 확장한다.

---

# 10. Skill authority modes

현재:
- Lv6 authoritative
- Lv11/16/21 exact legacy parity candidate
- Lv26 designed-not-authoritative
- Lv31 unresolved

Modes:
- CURRENT_AUTHORITY
- LEGACY_PARITY_CANDIDATE
- FUTURE_SKILL_PLACEHOLDER

Late Tier production freeze는 Lv6-only 결과에 의존하지 않는다.

---

# 11. Permanent stat / achievement calibration

Stars:
- broad foundation
- expected soft-wall shift를 기준으로 reward ladder 설계

Achievements:
- targeted cross-class bridge
- 실제 soft-wall map이 나온 뒤 reward edge 배치

검사:
- first class가 불합리하게 막히지 않는가
- later class가 trivial해지지 않는가
- 특정 class가 shared stat에서 과효율을 얻지 않는가
- stars + achievements가 multiplicative runaway를 만들지 않는가
- 한 achievement가 mandatory key가 되지 않는가

---

# 12. Encounter frequency calibration

Tier별 비교:
- monster spawn share
- Stage presence
- meaningful threat presence
- pressure family presence
- archetype frequency
- formation/cadence/geometry frequency
- backline-screen time
- capability uptime

단순 monster % 하나로 Tier identity를 판정하지 않는다.

---

# 13. Readability guardrail

Historical 5-monster 4s/6s density는 reference only.
새 roster unlock ladder가 정해진 뒤 Tier별로 새로 측정한다.

SPLITTER:
- authored count
- effective entity count
- peak active

SUPPORTER/SIEGER:
- count보다 capability uptime 중시

---

# 14. Determinism

동일:
- campaign spine version
- roster registry version
- Tier/Stage data version
- seed
- class/team
- mastery profile
- meta-power profile
- shop policy
이면 동일 결과가 재현되어야 한다.

Report 필수:
- data version/hash
- registry version
- seed range
- run count
- model mode
- mastery profile version

---

# 15. Failure classification

- CAMPAIGN_SPINE_EMPTY_TIER
- NOVELTY_OVERLOAD
- NOVELTY_STARVATION
- TOO_EASY_FOR_SKILLED
- TOO_MANY_ENTITIES
- FRONTLINE_SCREEN_TOO_LONG
- SIEGE_UPTIME_TOO_HIGH
- CHARGE_WINDOW_UNREADABLE
- REPLICATION_EXPLOSION
- DURABILITY_SPIKE
- CADENCE_COMPRESSION
- CLASS_STARVATION
- HARD_CLASS_LOCKOUT
- SKILL_POWER_SPIKE
- SHOP_SNOWBALL
- PERMANENT_STAT_SNOWBALL
- ACHIEVEMENT_ROUTE_DEADLOCK
- DOMINANT_PROGRESSION_ROUTE
- STAR_BOUNDARY_CLIFF
- TEAM_SCALING_DEFECT

한 원인을 global HP/count patch로 덮지 않는다.

---

# 16. Revised execution order

1. Master Campaign Matrix
2. Tier count 4/5/6 comparison
3. Tier novelty budget
4. current 9-monster unlock ladder
5. future monster expansion contract
6. Tier 50-Stage macro flow
7. run skill-reach windows
8. meta-power P0/P1/P2/P3
9. skilled clear target envelopes
10. cross-category static audit
11. encounter micro-sim
12. synthetic slice
13. full Tier sim
14. 5-class soft-wall map
15. stars-only recovery
16. achievement bridge modeling
17. account progression sim
18. 2/3/4P expansion
19. report / explicit freeze
20. live implementation

---

# 17. Freeze gate

Simulation만으로 자동 freeze하지 않는다.

- final Tier count
- monster unlock ladder
- future monster release cadence
- production monster numbers
- encounter frequencies
- star reward thresholds/coefficients
- achievement reward graph/value
- shop cadence/economy
- boss cadence
- Lv26/31 skill contract

Simulation은 decision support다.
