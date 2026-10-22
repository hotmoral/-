# Timing Defense — Master Campaign Matrix V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL COMPARISON CANDIDATE / NO FINAL TIER OR MONSTER-UNLOCK FREEZE**

Depends on:
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `02_TIER_SYSTEM.md`
- `06_SIMULATION_CALIBRATION_PLAN.md`

---

# 0. 목적

Master Campaign Spine을 실제 비교 가능한 matrix로 처음 펼친다.

이번 문서의 목적:
- 4/5/6 initial Tier 후보 비교
- current 9-monster unlock pacing 후보 비교
- future Tier/monster expansion room 확인
- 50-Stage macro flow와 player-power spine 정렬
- 난도 기준과 meta progression의 구조적 충돌 사전 탐지

아직 정하지 않는다:
- production monster HP/count
- exact Stage recipe
- exact skill unlock Stage
- exact star/achievement stat value
- final launch Tier count

---

# 1. Initial campaign Tier count vs lifetime Tier namespace

중요한 구조 분리:

```text
initialCampaignTierCount != lifetimeFinalTierCount
```

초기 출시/첫 calibration campaign은 4/5/6 Tier 중 하나를 선택할 수 있다.
하지만 Tier namespace는 open-ended로 둔다.

예:
```text
initial: T1..T4
future expansion: T5, T6, T7 ...
```

이 구조는 신규 monster가 나중에 추가될 때 자연스러운 content expansion point를 제공한다.

---

# 2. 4 / 5 / 6 Tier volume comparison

5 classes × 50 Stage 기준.

| Initial Tier count | Minimum successful class-stage volume | Max stars | Structural note |
|---:|---:|---:|---|
| 4 | 1000 | 60★ | already large; strong expansion room |
| 5 | 1250 | 75★ | longer initial campaign; slower novelty pacing possible |
| 6 | 1500 | 90★ | very large before retries; novelty starvation risk |

이 수치는 실패/재도전을 제외한 최소 성공 Stage량이다.

난도 목표가 일반 Tier `SKILLED_V2 <60% full-clear`이므로 실제 attempt volume은 훨씬 커질 수 있다.
따라서 Tier를 많이 만드는 것 자체가 곧 content value가 되는 것은 아니다.

---

# 3. Current structural front-runner

현재 **front-runner candidate**:

> **Initial 4 Tier + open-ended T5+ expansion**

이유:
1. 4 Tier만으로도 5직업 기준 최소 성공 Stage 1000개.
2. sub-60% skilled clear target 때문에 retry/soft-wall progression이 추가됨.
3. current 9-monster roster를 Tier마다 의미 있게 새로 소개하기 쉬움.
4. T5+를 future monster/content expansion에 보존 가능.
5. launch campaign을 과도하게 길게 만들지 않으면서 장기 확장성 유지.

이것은 final decision이 아니다.
T4 cognitive load와 T5 launch-value를 비교한 후 5-Tier candidate가 더 나을 수 있다.

---

# 4. Monster unlock ladder candidates

현재 roster:
G=GRUNT / R=RUNNER / B=BRUTE / SH=SHIELD / F=FLYER / C=CHARGER / SP=SPLITTER / SUP=SUPPORTER / SI=SIEGER

## Model A — 4 initial Tiers

| Tier | New monsters | Available roster after unlock | Core novelty |
|---|---|---|---|
| T1 | G / R / B | 3 | baseline / speed / durability |
| T2 | +SH / +F | 5 | mitigation / spatial geometry |
| T3 | +C / +SP | 7 | burst state / population transformation |
| T4 | +SUP / +SI | 9 | formation amplification / objective siege |
| T5+ | future monster(s) | 10+ | expansion |

Pros:
- strong novelty every launch Tier
- current 9종을 4 Tier에 자연스럽게 분배
- future T5 has clear expansion purpose

Risk:
- T4 introduces two high-state-complexity backline types.
- SUPPORTER와 SIEGER teaching을 50 Stage 내부에서 충분히 분리해야 함.

## Model B — 5 initial Tiers

| Tier | New monsters | Available roster after unlock |
|---|---|---|
| T1 | G / R / B | 3 |
| T2 | +SH / +F | 5 |
| T3 | +C / +SP | 7 |
| T4 | +SUP | 8 |
| T5 | +SI | 9 |
| T6+ | future | 10+ |

Pros:
- late complexity를 더 천천히 teach
- T4 support formation, T5 siege objective를 각각 독립 identity로 만들기 쉬움

Risk:
- 1250 minimum successful class-stage volume
- T4/T5에 신규 monster 1종씩만 있어 novelty budget이 빈약할 수 있음
- 반복 피로를 encounter/boss/player-skill novelty로 보완해야 함

## Model C — 6 initial Tiers

Example spacing:
- T1 G/R/B
- T2 +SH
- T3 +F/+C
- T4 +SP
- T5 +SUP
- T6 +SI

Pros:
- 매우 느린 학습곡선

Risks:
- 1500 minimum successful class-stage volume before retries
- current 9종으로는 Tier별 novelty가 너무 얇아질 가능성
- 높은 난도 목표와 결합하면 progression length가 과도해질 위험

Current classification:
**Model C = low priority unless future monster roster is substantially larger before launch.**

---

# 5. Monster unlock rule

한 monster는 unlock된 순간부터 모든 Stage에 난입하지 않는다.

각 Tier 내부 lifecycle:

```text
1. first appearance
2. isolated teach
3. mixed use
4. high-pressure use
5. later-Tier reinterpretation
```

예: Model A T2의 FLYER는 T2 early/mid에서 teach하고, T3에서는 RUNNER/CHARGER와 결합한 새로운 geometry problem으로 재사용 가능.

---

# 6. Future monster expansion slots

Future content는 두 방식 모두 허용한다.

## A. New Tier expansion
```text
T5/T6/... + new monster
```
가장 선호되는 기본 확장 경로.

## B. Existing higher-Tier retrofit
특정 신규 monster가 기존 campaign의 빈 공간을 개선할 때 higher Tier 일부에 추가 가능.
단 기존 clear history/난도/achievement 의미를 바꾸므로 별도 migration/version policy 필요.

기본값은 A.

---

# 7. Common 50-Stage macro grammar V0.1

모든 Tier가 같은 monster를 쓰지는 않지만 기본 진행 문법은 공유 가능하다.

| Stage | Macro role | Purpose |
|---|---|---|
| 1–9 | Establish | returning vocabulary / Tier identity setup |
| 10 | Checkpoint A | first read check |
| 11–19 | Introduce & Mix | new Tier monster/mechanic teaching |
| 20 | Star Gate A | first meaningful threshold / 1★ zone entry |
| 21–29 | Deepen | new + returning combinations |
| 30 | Checkpoint B | mid-Tier synthesis |
| 31–39 | Pressure / Soft Wall | class asymmetry begins to matter strongly |
| 40 | Star Gate B | 2★ zone entry |
| 41–49 | Mastery Exam | learned vocabulary under stronger constraints |
| 50 | Tier Final | 3★ full-clear gate |

Exact new-monster first appearance can move within 1–19 by Tier novelty budget.
Stage40+ 신규 핵심 mechanic 최초 소개는 기본적으로 피한다.

---

# 8. Run skill-power spine V0.1

현재 exact EXP curve는 재설계 필요.
Legacy skilled player가 Stage10 부근에 Lv21에 도달하던 모델은 50-Stage campaign에서 player power가 너무 빨리 소진될 가능성이 있다.

따라서 exact Stage number가 아니라 **relative reach bands**를 먼저 둔다.

| Skill milestone | Desired relative band candidate |
|---|---|
| Lv6 | early |
| Lv11 | early-mid |
| Lv16 | mid |
| Lv21 | mid-late |
| Lv26 | late |
| Lv31 | final/mastery band |

목표:
- 50 Stage 동안 class power novelty도 단계적으로 유지
- all meaningful skill power가 초반 20%에 몰리지 않음
- monster novelty와 skill novelty가 같은 Stage에 과도하게 겹치지 않음

Exact EXP/Stage는 별도 G4 gate.

---

# 9. Meta-power state by campaign depth

## P0 FRESH
- minimal permanent growth
- first class / first campaign entry

## P1 BALANCED
- multiple classes에서 일부 stars 확보
- broad permanent growth 시작

## P2 STAR_GROWN
- broad star reward가 soft wall을 유의미하게 이동

## P3 ACHIEVEMENT_ASSISTED
- targeted cross-class reward 적용

Candidate expectation:

| Tier depth | Likely relevant states |
|---|---|
| T1 | P0 primarily |
| T2 | P0–P1 |
| T3 | P1–P2 |
| T4 | P1–P3 |
| T5+ | P2–P3 / future |

이 table은 exact star threshold가 아니라 simulation scenario coverage다.

---

# 10. Difficulty envelope

User-confirmed global rule:
- non-T1 intended-entry SKILLED_V2 full-Tier clear probability <60%

Matrix placeholder:

| Tier | SKILLED_V2 intended-entry clear target |
|---|---|
| T1 | >60% allowed; exact TBD |
| T2 | <60% |
| T3 | <60% |
| T4 | <60% |
| T5+ | <60% unless explicit special design |

Important:
- exact 45%, 50%, 55% 등은 아직 정하지 않는다.
- class마다 동일할 필요 없음.
- soft-wall class는 훨씬 낮을 수 있음.
- overgrown replay는 이 gate 대상이 아님.

---

# 11. SKILLED_V2 prerequisite

Difficulty simulation 전에 skilled profile을 먼저 재정의해야 한다.

Requirements:
- combo 40 achievable without classifying player as extreme outlier
- high combo maintenance
- competent heavy completion
- timing error distribution stronger than old skilled profile

Exact numeric profile remains OPEN until measured.

Without this profile, `<60%` target is meaningless.

---

# 12. Cross-category risk audit

## Risk A — 4 Tier T4 overload
SUPPORTER + SIEGER를 같은 Tier에서 도입하면 learning density가 높아질 수 있음.
Mitigation candidate:
- SUPPORTER teach first half
- SIEGER teach second half
- combined FORTRESS-type encounter only late

## Risk B — 5/6 Tier repetition
Monster novelty가 너무 얇으면 50 Stage × many classes 반복감이 증가.

## Risk C — skill novelty collision
신규 monster와 major class skill unlock이 같은 Stage band에 몰리면 학습 attribution이 어려움.

## Risk D — meta snowball
P2/P3가 너무 강하면 intended-entry clear target 자체가 무너짐.

## Risk E — future monster insertion
기존 Tier를 retrofit하면 old clear/star/title 의미가 변할 수 있음.
Prefer new Tier expansion by default.

---

# 13. Current preliminary ranking

Structural ranking before simulation:

1. **Model A: 4 initial Tier + T5+ expansion** — strongest current candidate
2. **Model B: 5 initial Tier + T6+ expansion** — viable if T4 overload or content cadence demands separation
3. **Model C: 6 initial Tier** — low priority with current 9-monster roster

No freeze.

---

# 14. Next matrix work

1. audit Model A/B against 5-class skill roles
2. define Tier novelty budget beyond monster count
3. identify which Tier should own each boss novelty slot
4. refine relative skill reach bands
5. define SKILLED_V2 parameter test plan
6. estimate play-volume under sub-60 clear target
7. compare Model A vs B for repetition and meta progression room
8. choose one simulation spine
9. only then author Tier-specific monster frequencies/compositions
