# Timing Defense — Model A T1–T4 Macro Skeleton V0.1

Date: 2026-10-22 KST  
Status: **BOUNDED SIMULATION SKELETON CANDIDATE / NO EXACT ENCOUNTER COUNTS**

Depends on:
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
- `21_MODEL_A_NOVELTY_BUDGET_AND_BOSS_PLACEHOLDERS_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`

---

# 0. 목적

Model A의 4 Tier를 실제 50-Stage 시간축에 얕게 펼쳐, 이후 encounter authoring이 사용할 macro skeleton을 만든다.

이 문서는 아직 정하지 않는다.
- exact monster count
- HP/speed/armor
- exact cadence ms
- exact boss design
- exact EXP formula
- shop cadence

---

# 1. Common late-band structure

모든 Tier에서 후반은 다음으로 분리한다.

```text
31–39  PRESSURE / SOFT-WALL BUILD
40     STAR GATE B
41–45  LV31 ASCENSION WINDOW
46–49  POST-LV31 MASTERY
50     TIER FINAL
```

Stage41–45는 단순 peak difficulty band가 아니다.
Lv31 획득/첫 활용을 위한 controlled high-pressure 구간이다.

---

# 2. Common skill-reach overlay candidate

- Lv6: 5–7
- Lv11: 11–14
- Lv16: 18–21
- Lv21: 25–28
- Lv26: 32–36
- Lv31: 41–45

T1에서는 learning novelty, T2+에서는 주로 repeated power progression event.

---

# 3. T1 — Foundation / Timing & Frontline

Available:
- GRUNT
- RUNNER
- BRUTE

Primary purpose:
- core timing game 이해
- class identity 학습
- speed vs durability 읽기
- formation/cadence 기초

## Stage windows

### 1–3 — Core baseline
- GRUNT only or near-only
- timing/targeting 기본
- no boss novelty

### 4–9 — Tempo introduction
- RUNNER first appearance/teach/mix
- Lv6 reach overlaps; encounter intensity conservative
- basic line/wave

### 10 — Checkpoint A
- GRUNT/RUNNER read check
- boss not required

### 11–14 — Skill specialization runway
- Lv11 expected
- returning G/R combinations
- avoid major new monster in first part

### 15–19 — Durability introduction
- BRUTE first teach/mix
- Lv16 begins near end

### 20 — Star Gate A
- first meaningful 1★ boundary
- G/R/B basic synthesis

### 21–29 — Foundation synthesis
- BRUTE high-pressure candidate
- RUNNER tempo contrast
- formation variety
- Lv21 around25–28
- do not use maximal complexity during first-time Lv21 learning

### 30 — Checkpoint B
- synthesis checkpoint
- optional boss-preview only if it uses known grammar

### 31–39 — Pressure / first soft-wall formation
- stronger timing discipline
- line/cluster/scatter rotation
- Lv26 32–36
- class role differences become visible

### 40 — Star Gate B
- 2★ zone entry

### 41–45 — Lv31 Ascension
- Lv31 target
- no new monster
- controlled high-pressure

### 46–49 — Post-Lv31 mastery
- class-specific opportunity rotation
- high difficulty without hard class lockout

### 50 — T1 Final
- known G/R/B grammar
- first Tier final/boss candidate
- T1 may be easier than later Tier targets

---

# 4. T2 — Mitigation / Geometry

New:
- SHIELD
- FLYER

Returning:
- G/R/B

### 1–4 — Returning baseline re-establish
- familiar roster
- establish T2 higher pressure without novelty overload

### 5–9 — SHIELD teach
- mitigation vs raw HP contrast
- Lv6 power spike monitored

### 10 — Checkpoint A
- G/B/SH comparison check

### 11–13 — mixed consolidation
- familiar skill Lv11 power progression

### 14–18 — FLYER teach
- Y/geometry introduction
- low overlap with SHIELD first

### 19–20 — first combined gate
- SHIELD + FLYER light synthesis
- Stage20 1★ boundary

### 21–29 — Geometry/mitigation deepen
- AIR_OFFSET
- durable front + air relation
- Lv21 power spike observed

### 30 — Checkpoint B / optional boss signature preview
- if Stage50 boss has unique mandatory decision, preview here

### 31–39 — T2 soft-wall band
- stronger geometry + screen interactions
- Lv26 32–36

### 40 — Star Gate B

### 41–45 — Lv31 Ascension
- no new core mechanic
- moderate-high T2 mastery with Lv31 acquisition

### 46–49 — Post-Lv31 mastery
- hard geometry/mitigation combinations

### 50 — T2 Final
- full T2 vocabulary + previewed boss signature only

---

# 5. T3 — Burst / Population Transformation

New:
- CHARGER
- SPLITTER

Returning:
- G/R/B/SH/F

### 1–4 — returning tempo recap

### 5–9 — CHARGER teach
- windup/interrupt readable at low intensity
- no class mandatory counter

### 10 — Checkpoint A
- CHARGER read check

### 11–14 — CHARGER mixed consolidation

### 15–19 — SPLITTER teach
- parent death -> children
- effective entity count explained/readable

### 20 — Star Gate A
- first C/SP light synthesis

### 21–29 — stateful deepen
- CHARGER/SPLITTER separately then mixed
- Lv21 around25–28
- maximal overlap avoided during power transition

### 30 — Checkpoint B / optional boss preview

### 31–39 — T3 soft wall
- burst + population + returning durability/geometry
- Lv26 32–36
- WATCH replication density

### 40 — Star Gate B

### 41–45 — Lv31 Ascension
- known stateful vocabulary only
- no new spawn grammar

### 46–49 — Post-Lv31 mastery
- high turnover/density/control tests

### 50 — T3 Final
- known state transitions under strong but readable constraints

---

# 6. T4 — Formation Support / Siege Objective

New:
- SUPPORTER
- SIEGER

Returning:
- all previous 7

### 1–9 — returning formation recap
- screen/backline concepts without new T4 units
- prepare target-order reading

### 10 — Checkpoint A

### 11–15 — SUPPORTER first teach
- speed aura
- low screen complexity initially

### 16–19 — SUPPORTER mixed
- durable/tempo escorts
- first meaningful screened aura exposure

### 20 — Star Gate A
- SUPPORTER-focused check

### 21 — transition/recovery
- no new major rule

### 22–25 — SIEGER first teach
- standoff/windup/ranged wall attack
- Lv21 power window overlaps only at tail; low intensity

### 26–29 — SIEGER mixed
- screen/escort relation
- no full SUPPORTER+SIEGER peak yet

### 30 — Checkpoint B
- synthesis checkpoint
- boss-only novelty LOW

### 31–33 — first combined support/siege
- low/moderate combined pressure

### 34–36 — Lv26 transition observation
- measure how late specialization changes screening/siege uptime

### 37–39 — post-Lv26 high-pressure synthesis
- T4 first real combined wall

### 40 — Star Gate B
- 2★ entry

### 41–45 — Lv31 Ascension
- SUPPORTER/SIEGER already known
- no new ordinary mechanic
- not maximum T4 pressure every Stage
- class final skills become available

### 46–49 — Post-Lv31 T4 mastery
- strong fortress/escort/objective patterns
- rotate class opportunity
- no hard counter

### 50 — T4 Final
- current launch-campaign mastery candidate
- final uses known support/siege/formation vocabulary
- unpreviewed boss-only mandatory mechanic prohibited

---

# 7. Class-opportunity rotation requirement

Late bands must not repeat only the naturally favored class problem.

Examples:
- durable screens -> Rogue opportunity
- long line/backline -> Archer/Knight
- dense escort -> Mage
- charge/objective/control -> Tank

각 Tier 31–49에서 최소한 모든 class가 의미 있는 opportunity signature를 여러 번 가져야 한다.
Exact quota는 later authoring.

---

# 8. Soft-wall placement

기본 soft wall은:
- 31–39에서 형성 시작
- 40+에서 class/meta 차이가 더 분명

Stage1–19을 ordinary soft-wall 기본 위치로 사용하지 않는다.
초반 실패가 너무 많으면 star progression이 죽기 때문이다.

---

# 9. Boss placement placeholder

- Stage10: boss optional / default checkpoint
- Stage30: optional preview slot
- Stage50: Tier final boss candidate

Boss-specific mandatory rule이 Stage50에 있다면 Stage30 또는 earlier safe context에서 preview 필요.

---

# 10. Static verdict

Model A T1–T4는 50-Stage macro level에서 구조적으로 배치 가능하다.

Main WATCH:
- T1 first-time class skill learning density
- T3 stateful C/SP overlap
- T4 SUP/SI + late Lv26/31 power transitions

No macro structural FAIL found.
