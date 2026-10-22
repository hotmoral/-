# Timing Defense — Model A Tier Pressure & Complexity Envelope V0.1

Date: 2026-10-22 KST  
Status: **SIMULATION ENVELOPE / QUALITATIVE FREQUENCY, NO PRODUCTION COUNTS**

Depends on:
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
- `28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`

---

# 0. 목적

Model A 각 Tier의 identity를 monster unlock만이 아니라 pressure family와 complexity 분포로 정의한다.

이 문서의 LOW/MED/HIGH는 exact spawn %가 아니다.
Tier 전체에서 얼마나 자주/의미 있게 해당 문제를 다룰지 나타내는 qualitative envelope다.

---

# 1. Pressure family reference

- BASELINE — neutral/reference flow
- FLOOD — entity/count pressure
- RUSH — sustained tempo
- BULWARK — durable/mitigation frontline
- BREACH — burst breakthrough / charge
- AERIAL — geometry/Y pressure
- REPLICATE — death-triggered population shift
- SUPPORT — formation amplification
- SIEGE — ranged objective pressure

---

# 2. T1 envelope — Foundation / Timing & Frontline

Available: G/R/B

| Pressure | Target envelope |
|---|---|
| BASELINE | HIGH |
| FLOOD | LOW–MED |
| RUSH | MED |
| BULWARK | MED |
| BREACH | NONE |
| AERIAL | NONE |
| REPLICATE | NONE |
| SUPPORT | NONE |
| SIEGE | NONE |

Identity:
- simple readable frontline
- timing consistency
- speed vs durability

Complexity target:
- C0: meaningful presence
- C1: dominant
- C2: moderate late
- C3: rare/optional late synthesis
- C4: not needed

Guardrail:
T1 difficulty should not require high special-state complexity.

---

# 3. T2 envelope — Mitigation / Geometry

Available: G/R/B/SH/F

| Pressure | Target envelope |
|---|---|
| BASELINE | MED–HIGH |
| FLOOD | LOW–MED |
| RUSH | MED |
| BULWARK | HIGH |
| BREACH | NONE |
| AERIAL | MED–HIGH |
| REPLICATE | NONE |
| SUPPORT | NONE |
| SIEGE | NONE |

Identity:
- raw HP vs armor mitigation
- line/air geometry

Complexity:
- C0: low
- C1: high
- C2: high
- C3: low/moderate late
- C4: not required

Guardrail:
AERIAL + BULWARK가 매 Stage 동시 등장하지 않게 한다.

---

# 4. T3 envelope — Burst / Transformation

Available: previous 5 + C/SP

| Pressure | Target envelope |
|---|---|
| BASELINE | MED |
| FLOOD | MED–HIGH |
| RUSH | MED–HIGH |
| BULWARK | MED |
| BREACH | HIGH |
| AERIAL | MED |
| REPLICATE | HIGH |
| SUPPORT | NONE |
| SIEGE | NONE |

Identity:
- telegraphed burst
- kill 이후 population change
- target-order 재구성

Complexity:
- C0: rare recovery
- C1: moderate
- C2: dominant
- C3: meaningful late
- C4: rare bounded late/final only

Guardrail:
- REPLICATE pressure는 authored count가 아니라 effective entity volume으로 측정
- BREACH+REPLICATE high-high 동시 최대화 금지

---

# 5. T4 envelope — Formation / Siege

Available: all current 9

| Pressure | Target envelope |
|---|---|
| BASELINE | LOW–MED |
| FLOOD | LOW–MED |
| RUSH | MED |
| BULWARK | MED–HIGH |
| BREACH | MED |
| AERIAL | MED |
| REPLICATE | MED |
| SUPPORT | HIGH |
| SIEGE | HIGH |

Identity:
- protected threats
- screen/backline uptime
- wall/objective pressure

Complexity:
- C0: rare recovery
- C1: moderate focused challenge
- C2: high
- C3: high late
- C4: bounded, primarily Stage46–50 candidate

Important:
`SUPPORT HIGH` + `SIEGE HIGH` means Tier 전체 identity가 강하다는 뜻이지 매 Stage 둘을 동시에 넣는다는 뜻이 아니다.

Guardrail:
- Stage11–29 isolated teaching dominates
- combined support/siege high pressure mainly 31+
- Stage41–45 Lv31 Ascension 동안 C4 연속 사용 금지
- Stage46–49에서 bounded mastery C4 가능

---

# 6. Complexity != difficulty

Higher Tier가 반드시 C3/C4만 사용하는 구조를 금지한다.

예:
- T4 C1 SIEGE focused extreme
- T4 C1 durable screen extreme
도 충분히 어려울 수 있다.

Difficulty axes:
- quantity
- durability
- tempo
- geometry
- formation protection
- capability uptime
- objective pressure

Complexity는 그중 하나일 뿐이다.

---

# 7. Recovery stages

각 Tier 후반에도 lower-complexity focused Stage를 유지한다.
목적:
- cognitive recovery
- single-axis mastery 확인
- class role rotation
- constant-chaos fatigue 방지

권장 구조:
- 31–39 중 최소 몇 개의 C1/C2 focused stage 유지
- 46–49도 모두 C4로 만들지 않음

Exact quota는 later frequency authoring.

---

# 8. Tier identity anti-collapse rules

## T1→T2
T2가 단순 T1 HP inflation으로 느껴지면 FAIL.
SHIELD/FLYER meaningful threat presence 필요.

## T2→T3
CHARGER/SPLITTER가 filler 수준이면 FAIL.
BREACH/REPLICATE가 실제 전투 결정을 바꿔야 함.

## T3→T4
SUPPORTER/SIEGER spawn share가 낮더라도 aura/firing uptime이 Tier identity를 만들어야 함.

---

# 9. Future expansion

T5+ 신규 monster가 추가되면:
- existing pressure family에 자연스럽게 매핑하거나
- 필요한 경우 new pressure family 추가

현재 9-family 표는 lifetime fixed enum이 아니다.

---

# 10. Static verdict

Model A pressure identity는 4 Tier 간 충분히 구분된다.

- T1 basic frontline
- T2 mitigation/geometry
- T3 burst/transformation
- T4 support/objective

**No novelty starvation detected at qualitative envelope level.**
