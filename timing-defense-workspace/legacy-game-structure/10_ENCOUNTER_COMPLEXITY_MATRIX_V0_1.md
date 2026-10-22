# Timing Defense — Encounter Complexity Matrix V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL CANDIDATE / NO PRODUCTION COUNTS**

## 0. 목적

Encounter의 복잡도를 “몬스터 종류가 몇 종인가”가 아니라 **동시에 읽어야 하는 상태 변화와 상호작용 수**로 분류한다.
이 분류는 Tier/Stage가 높은 난이도를 만들 때 무조건 많은 monster type을 섞는 퇴행을 막기 위한 것이다.

---

# 1. Complexity definitions

## C0 — Baseline
특수 상태 상호작용 없음.
전선/타이밍 시스템 자체를 읽는 구간.

## C1 — Single mechanic
한 개의 핵심 capability가 전투 문제를 만든다.
다른 monster는 filler/reference 역할.

## C2 — Dual readable
두 압박 또는 한 특수 mechanic + 명확한 보조 조건.
두 문제를 플레이어가 분리해서 읽을 수 있다.

## C3 — Synergy
한 구성 요소가 다른 구성 요소를 **보호/가속/지연/증폭**하여 단순 합보다 강한 상호작용을 만든다.

## C4 — Multi-state high complexity
세 개 이상 stateful/formation capability가 동시에 또는 연속적으로 얽혀 target order와 objective pressure를 크게 바꾼다.
일상 Stage의 기본값이 아니라 제한적 mastery test다.

---

# 2. Archetype matrix

| ID | Archetype | Complexity | Core interaction | Primary risk |
|---|---|---:|---|---|
| E01 | BASELINE_MARCH | C0 | GRUNT baseline flow | boredom if overused |
| E02 | RUSH_WAVE | C1 | sustained speed | reaction-time compression |
| E03 | HEAVY_LINE | C1 | raw durability / knock resist | long frontline dwell |
| E04 | SHIELD_SCREEN | C1 | armor mitigation | effective damage suppression |
| E05 | MIXED_WALL | C2 | BRUTE raw anchor + SHIELD mitigation | durability interpretation |
| E06 | AIR_PRESSURE | C1 | FLYER Y geometry | line/AoE instability |
| E07 | CHARGE_BREAK | C1 | windup -> burst charge | missed interrupt window |
| E08 | SPLIT_FLOOD | C2 | parent death -> 2 children + population | entity rebound |
| E09 | SUPPORT_COLUMN | C2 | SUPPORTER + ordinary recipients | formation tempo increase |
| E10 | SIEGE_LINE | C2 | SIEGER + light frontline | ranged wall uptime |
| E11 | ESCORT_SIEGE | C3 | durable screen protects SIEGER | screened firing uptime |
| E12 | BUFFED_BULWARK | C3 | SUPPORTER accelerates durable formation | screen compression |
| E13 | RUSH_BREACH | C2 | RUNNER sustained speed + CHARGER burst | two tempo modes |
| E14 | AIR_RUSH | C2 | ground speed + Y geometry | target/geometry switching |
| E15 | REPLICATE_RUSH | C2 | split population + fast advance | reorder after split |
| E16 | CASCADE | C3 | SPLITTER population + SUPPORTER aura | post-kill tempo amplification |
| E17 | BREACH_SCREEN | C3 | durable screen protects CHARGER trigger | protected burst threat |
| E18 | DUAL_AXIS | C3 | FLYER geometry + SIEGER objective + ground screen | spatial/objective split attention |
| E19 | FORTRESS | C4 | BULWARK + SUPPORT + SIEGE | prolonged protected objective pressure |
| E20 | COLLAPSE_CHAIN | C4 | SPLITTER + CHARGER + fast/baseline flow | population/tempo state cascade |

---

# 3. Complexity does not equal difficulty

C4가 항상 C1보다 어려워야 하는 것은 아니다.

예:
- 매우 약한 C4 teaching composition은 강한 C1 RUSH extreme보다 쉬울 수 있다.
- high Tier는 C1/C2의 intensity extreme으로도 충분히 높은 난이도를 만들 수 있다.

따라서 simulator에서는:

```text
Difficulty != Complexity only
Difficulty = quantity + durability + tempo + formation + geometry + objective + overlap + complexity
```

로 본다.

---

# 4. Tier candidate complexity envelope

| Tier | 중심 | 제한적 사용 | 금지/경계 |
|---|---|---|---|
| T1 | C0/C1/C2 | C3 late | C4는 Stage49/50 수준의 극소수 후보 |
| T2 | C1/C2/C3 | C4 late | C4 연속 반복 금지 |
| T3 | C1/C2/C3 | C4 late | entity saturation 경계 |
| T4 | C2/C3 | C4 selected | C4 default화 금지 |
| T5 | C1~C4 contrast | C4 selected | 모든 Stage C3/C4화 금지 |

T5에 C1이 남는 이유는 focused extreme이 복합 chaos와 다른 mastery problem이기 때문이다.

---

# 5. Introduction rule

신규 ordinary capability teaching은 가능한 한 C1 또는 낮은 C2로 시작한다.

예:
- CHARGER first teach: E07 C1
- SPLITTER first teach: E08 C2지만 SUPPORTER/CHARGER와 동시에 섞지 않음
- SUPPORTER first teach: E09 C2, ordinary recipients 위주
- SIEGER first teach: E10 C2, light frontline만 사용

C3/C4 archetype에서 capability를 처음 소개하지 않는다.

---

# 6. Synergy audit questions

C3/C4 encounter를 추가할 때 반드시 확인:

1. 어떤 monster가 누구를 보호/증폭하는가?
2. system target order 때문에 그 interaction이 실제로 발생하는가?
3. formation이 조금 바뀌면 synergy가 사라지는가?
4. 특정 class만 사실상 해결할 수 있는가?
5. SUPPORTER/SIEGER uptime이 과도하게 길어지지 않는가?
6. SPLITTER child 때문에 active count가 예상보다 폭증하지 않는가?
7. CHARGER telegraph가 다른 VFX/entity에 가려지지 않는가?
8. 동일 문제를 이미 다른 archetype이 더 단순하게 제공하지 않는가?

---

# 7. Redundancy test

새 encounter archetype은 최소 하나가 기존 library와 달라야 한다.

- tactical question
- target-order transition
- capability interaction
- geometry demand
- objective pressure
- cadence problem

단지 monster를 한 종류 다른 것으로 바꾼 조합은 새 archetype으로 만들지 않는다.
variant로 관리한다.

---

# 8. Static authoring checks

50-stage skeleton 생성 시 자동 검사 후보:
- 동일 archetype exact signature 연속 반복
- C4 연속 배치
- 5-Stage window 내 C3/C4 과다 밀집
- teaching 전에 C3/C4 synergy 사용
- 특정 class-opportunity tag 장기 부재
- 같은 pressure family + same cadence + same geometry 장기 반복

정확한 threshold는 첫 skeleton 데이터에서 분포를 본 뒤 결정한다.

---

# 9. Next

이 matrix를 `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`의 Stage 1~50 배치에 적용하고:
- 모든 capability가 단순 형태로 먼저 teaching되는지
- C3/C4가 너무 일찍/자주 나오지 않는지
- 40~50이 신규 capability tutorial이 아니라 종합 시험인지
정적 검사한다.
