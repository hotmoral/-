# Timing Defense — Model A/B Class-Role & Volume Audit V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL AUDIT / NO FINAL TIER FREEZE**

Compares:
- Model A = 4 initial Tiers + T5+ expansion
- Model B = 5 initial Tiers + T6+ expansion

Depends on:
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
- `SKILL_PLAN_LV6_31.md`
- `MONSTER_CAPABILITY_CONTRACT_V1.md`
- `18_MONSTER_ROSTER_EXTENSIBILITY_AMENDMENT_2026-10-22.md`

---

# 0. Audit question

Model A가 campaign length를 줄인 대신 T4에 SUPPORTER + SIEGER를 같이 넣어 학습밀도/직업편향을 과도하게 만들지 않는가?

Model B는 이를 분리하지만 250 successful class-stage volume과 15★를 추가하는 만큼 실제 content value가 있는가?

---

# 1. Class role reference

## Knight
- generalist
- penetration
- frontline destabilization

## Rogue
- multihit / crit
- durable normal execution

## Tank
- knockback / wall protection / crowd control
- CHARGER interrupt value

## Archer
- straight-line penetration
- screened rear-target value

## Mage
- area damage
- density / child-cluster value

Goal:
- Tier마다 모든 class를 동일하게 강하게 만들지 않는다.
- 그러나 Tier 전체에서 한 class의 역할이 사실상 사라지지 않게 한다.

---

# 2. Model A — class-opportunity audit

## T1 — G / R / B

Combat vocabulary:
- GRUNT baseline
- RUNNER sustained tempo
- BRUTE raw durability

### Knight
PASS candidate.
- mixed baseline 대응
- line/penetration authoring으로 역할 확보 가능

### Rogue
STRONG opportunity.
- BRUTE가 durable-normal identity를 직접 제공

### Tank
PASS candidate.
- RUNNER/BRUTE control
- knockback value를 formation/cadence로 표현 가능

### Archer
WATCH but solvable.
- special backline monster가 아직 없어도 G/R/B line formation으로 penetration value 제공 가능
- T1 authoring이 cluster/scatter만 많으면 starvation 위험

### Mage
WATCH but solvable.
- GRUNT/RUNNER cluster density로 AoE 가치 제공 필요
- 몬스터 종류보다 formation authoring이 중요

Verdict:
**3 monster만으로도 5-class opportunity를 만들 수 있다.**
T1 variety를 monster count만으로 해결할 필요가 없다.

---

## T2 — +SHIELD / +FLYER

New problems:
- mitigation
- vertical/spatial geometry

### Knight
PASS.
- mixed line/frontline handling

### Rogue
PASS/WATCH.
- SHIELD armor 때문에 raw hit efficiency는 달라질 수 있으나 hard lockout 아님
- BRUTE가 returning roster로 유지되어 durable target opportunity 계속 제공되어야 함

### Tank
PASS.
- mitigation/geometry 자체보다 frontline control에서 가치 유지

### Archer
STRONG opportunity.
- line/penetration + FLYER geometry

### Mage
STRONG opportunity.
- mixed ground/air cluster authoring

Verdict:
T2는 class-role coverage가 자연스럽다.

---

## T3 — +CHARGER / +SPLITTER

New problems:
- telegraphed burst
- death-triggered population transformation

### Knight
PASS.
- reorder/generalist/penetration

### Rogue
WATCH.
- 신규 둘만 과도하게 집중하면 durable-target identity가 약해질 수 있음
- BRUTE/SHIELD returning presence가 필수에 가까운 authoring support

### Tank
STRONG opportunity.
- CHARGER interrupt/control

### Archer
PASS.
- split/reorder 이후 line opportunities author 가능

### Mage
STRONG opportunity.
- SPLITTER child density

Verdict:
T3는 Tank/Mage spike가 자연스럽다.
Rogue starvation 방지를 위해 durable returning pressure를 유지해야 한다.

---

## T4 — +SUPPORTER / +SIEGER

New problems:
- formation amplification
- ranged objective pressure

### Knight
PASS/STRONG.
- screened formation penetration/generalist response

### Rogue
WATCH.
- new special 자체는 Rogue signature target이 아님
- BRUTE/SHIELD screen을 SUPPORTER/SIEGER 앞에 배치하면 durable frontline execution 역할을 유지할 수 있음

### Tank
STRONG.
- movement control
- wall protection
- SIEGER reposition/pressure mitigation

### Archer
STRONG.
- screened backline penetration value

### Mage
PASS/STRONG depending formation.
- clustered escort/support formation에 AoE 가치
- SIEGER 단독형 stage만 많으면 역할 감소 가능

Verdict:
**class coverage는 성립 가능.**
문제는 class lockout보다 learning density다.

---

# 3. T4 learning-density audit

SUPPORTER와 SIEGER는 둘 다 stateful/backline-oriented라 같은 Tier에서 동시에 처음 가르치면 과밀할 수 있다.

그러나 50 Stage 안에서 다음처럼 분리 가능하다.

Candidate pacing:

```text
Stage 1–9
  returning formation recap

Stage 10
  checkpoint

Stage 11–19
  SUPPORTER teach + mixed

Stage 20
  first gate

Stage 21–29
  SIEGER teach + mixed

Stage 30
  synthesis checkpoint

Stage 31–39
  SUPPORTER/SIEGER with returning screens

Stage 40–49
  mastery combinations

Stage 50
  Tier final
```

이렇게 하면:
- SUPPORTER와 SIEGER를 같은 날 동시에 teach하지 않음
- 각 mechanic이 최소 8~9 Stage의 isolated/mixed window를 가짐
- synergy는 30+ 이후로 늦출 수 있음

Current classification:
**T4 overload risk = WATCH, not structural FAIL.**

---

# 4. Model B — class-opportunity audit

Model B는 T4 SUPPORTER, T5 SIEGER로 분리한다.

장점:
- 각 late mechanic에 50 Stage 전체를 사용할 수 있음
- T4 formation-support / T5 siege-objective identity가 선명
- class-role rotation을 더 세밀하게 만들 수 있음

단점:
- T4와 T5 각각 신규 monster가 1종뿐
- 50 Stage를 정당화하려면 boss/formation/cadence/player-skill novelty가 충분해야 함
- content가 늘어난 것이 아니라 기존 T4를 두 조각으로 늘린 느낌이 날 위험

Class coverage 자체는 Model A보다 명확히 우월하다고 보기 어렵다.
주 차이는 **learning density vs campaign length**다.

---

# 5. Attempt-volume sensitivity

단순 sensitivity 계산.

가정:
- 모든 class×Tier를 결국 3★ clear한다고 가정
- 각 Tier full-clear probability q가 attempt마다 동일한 단순 geometric model
- 실제 game에서는 stars/meta growth/fail stage가 달라지므로 이것은 rough comparison only

Expected full-Tier attempts per 3★ clear:

```text
E[attempts] = 1/q
```

전체 class×Tier 3★ completion에 필요한 expected attempt count:

| q | 4 Tier / 20 records | 5 Tier / 25 records | 6 Tier / 30 records |
|---:|---:|---:|---:|
| 0.59 | 33.90 | 42.37 | 50.85 |
| 0.55 | 36.36 | 45.45 | 54.55 |
| 0.50 | 40.00 | 50.00 | 60.00 |
| 0.45 | 44.44 | 55.56 | 66.67 |
| 0.40 | 50.00 | 62.50 | 75.00 |

주의:
- 실패 attempt는 Stage50까지 가지 않을 수 있으므로 total Stage play volume과 같지 않음.
- meta growth가 q를 변화시킴.
- 단순 비교 목적.

하지만 한 가지는 분명하다.
`SKILLED_V2 <60%` 목표와 결합하면 **Tier 하나 추가의 실제 반복량 비용이 작지 않다.**

---

# 6. Novelty-budget comparison

## Model A

### T1
- 3 foundational monster vocabularies
- low state complexity

### T2
- 2 new monsters
- mitigation + geometry

### T3
- 2 new monsters
- burst + population transform

### T4
- 2 new monsters
- support formation + siege objective

Pattern:
`3 / 2 / 2 / 2`

Novelty density는 높지만 균형적.

## Model B

Pattern:
`3 / 2 / 2 / 1 / 1`

Late campaign에서 monster novelty density가 낮아진다.
이를 정당화하려면:
- boss novelty
- stronger formation grammar
- skill reach novelty
- achievement/meta novelty
가 충분해야 한다.

현재 이 하위 시스템들은 아직 freeze되지 않았다.

---

# 7. Structural verdict

## Model A
Status: **PREFERRED CANDIDATE / WATCH T4 LEARNING DENSITY**

장점:
- compact initial campaign
- strong Tier novelty
- current roster evenly consumed
- T5+ future expansion room
- 1000 successful Stage floor already substantial

필수 guardrail:
- T4 SUPPORTER teach and SIEGER teach를 시간적으로 분리
- T4 late synergy only after isolated learning
- Rogue/Mage opportunity를 returning BRUTE/SHIELD/cluster formation으로 유지

## Model B
Status: **VALID FALLBACK / USE IF T4 OVERLOAD FAILS**

채택 조건 후보:
- T4 two-monster teaching이 simulation/playtest에서 과부하
- launch content에 충분한 boss/formation novelty가 있어 T5 50 Stage를 정당화
- 1250+ successful Stage floor가 retention 목표에 적합

---

# 8. Current decision recommendation

아직 final freeze하지 않는다.

다음 bounded simulation spine은 **Model A를 우선 후보로 사용**하고:

1. T4 novelty-load static audit
2. skill-reach collision audit
3. class-role opportunity matrix
4. SKILLED_V2 play-volume sensitivity

를 먼저 돌린다.

이 단계에서 FAIL하면 Model B로 split한다.

즉:

```text
Model A = default test hypothesis
Model B = pre-defined fallback
```

이 방식이 불필요하게 5 Tier를 먼저 확정하는 것보다 비용이 낮다.
