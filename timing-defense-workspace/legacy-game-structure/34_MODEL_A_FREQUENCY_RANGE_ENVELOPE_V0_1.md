# Timing Defense — Model A Frequency Range Envelope V0.1

Date: 2026-10-22 KST  
Status: **BOUNDED FREQUENCY CANDIDATE / NOT PRODUCTION DISTRIBUTION**

Depends on:
- `29_MODEL_A_TIER_PRESSURE_COMPLEXITY_ENVELOPE_V0_1.md`
- `32_MODEL_A_TIER_ENCOUNTER_AVAILABILITY_V0_1.md`
- `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`

---

# 0. 목적

LOW/MED/HIGH 같은 qualitative envelope를 first deterministic authoring에 사용할 수 있는 **넓은 Stage-presence range**로 변환한다.

이 값은 production target이 아니다.
50 Stage exact schedule을 만들기 전에 candidate generator/search space를 제한하는 용도다.

Pressure family는 한 Stage에 복수 존재할 수 있으므로 합계가 50을 넘을 수 있다.

---

# 1. Qualitative -> Stage-presence range

50 Stage 기준 meaningful threat presence candidate:

| Label | Stage presence range | Approx share |
|---|---:|---:|
| NONE | 0 | 0% |
| LOW | 2–5 | 4–10% |
| LOW_MED | 5–11 | 10–22% |
| MED | 9–17 | 18–34% |
| MED_HIGH | 14–22 | 28–44% |
| HIGH | 19–30 | 38–60% |

주의:
- spawn share가 아니다.
- meaningful pressure presence다.
- one Stage can count toward multiple families.

---

# 2. T1 pressure range

| Pressure | Candidate Stage presence |
|---|---:|
| BASELINE | 19–30 |
| FLOOD | 5–11 |
| RUSH | 9–17 |
| BULWARK | 9–17 |
| BREACH | 0 |
| AERIAL | 0 |
| REPLICATE | 0 |
| SUPPORT | 0 |
| SIEGE | 0 |

Intent:
- baseline readability
- speed/durability contrast
- no stateful late-roster leakage

---

# 3. T2 pressure range

| Pressure | Candidate Stage presence |
|---|---:|
| BASELINE | 14–22 |
| FLOOD | 5–11 |
| RUSH | 9–17 |
| BULWARK | 19–30 |
| AERIAL | 14–22 |
| BREACH | 0 |
| REPLICATE | 0 |
| SUPPORT | 0 |
| SIEGE | 0 |

Guardrail:
BULWARK+AERIAL overlap should not consume most Stages; some focused single-axis stages remain.

---

# 4. T3 pressure range

| Pressure | Candidate Stage presence |
|---|---:|
| BASELINE | 9–17 |
| FLOOD | 14–22 |
| RUSH | 14–22 |
| BULWARK | 9–17 |
| BREACH | 19–30 |
| AERIAL | 9–17 |
| REPLICATE | 19–30 |
| SUPPORT | 0 |
| SIEGE | 0 |

Guardrail:
BREACH high + REPLICATE high는 Tier identity를 뜻하며 같은 Stage에서 high-high 동시 최대화하라는 뜻이 아니다.

---

# 5. T4 pressure range

| Pressure | Candidate Stage presence |
|---|---:|
| BASELINE | 5–11 |
| FLOOD | 5–11 |
| RUSH | 9–17 |
| BULWARK | 14–22 |
| BREACH | 9–17 |
| AERIAL | 9–17 |
| REPLICATE | 9–17 |
| SUPPORT | 19–30 |
| SIEGE | 19–30 |

Required:
- SUPPORT 19–30 and SIEGE 19–30 do not imply 19+ simultaneous overlap Stages.
- isolated/focused support and siege stages count separately.
- full fortress synergy remains bounded.

---

# 6. Dominant Stage complexity ranges

Each Stage gets one `dominantComplexity` for static distribution auditing.
Exact counts later must sum to 50.

## T1
- C0: 8–14
- C1: 22–30
- C2: 8–15
- C3: 0–4
- C4: 0

## T2
- C0: 4–8
- C1: 15–22
- C2: 18–25
- C3: 4–8
- C4: 0–2

## T3
- C0: 2–5
- C1: 10–16
- C2: 19–26
- C3: 8–14
- C4: 0–3

## T4
- C0: 2–4
- C1: 8–14
- C2: 16–22
- C3: 14–20
- C4: 1–4

T4 C4는 기본적으로 late/bounded이며 Stage41–45에 연속 배치하지 않는다.

---

# 7. Archetype occurrence range philosophy

Archetype exact count는 pressure target에서 역으로 자동 고정하지 않는다.
하나의 archetype이 여러 pressure에 기여하기 때문이다.

대신 generator는:
1. Tier legal archetype set만 사용
2. pressure presence range 만족
3. complexity range 만족
4. teaching dependency 만족
5. repetition/class-opportunity guardrail 만족
하도록 후보를 생성한다.

---

# 8. Repetition guardrails

First authoring search constraints:
- same archetype dominant signature 3 consecutive Stages 금지 candidate
- same archetype + same formation + same cadence consecutive repeat 금지
- C4 consecutive Stage 금지
- 5-Stage window에 C4 2개 초과 금지 candidate
- 5-Stage window가 모두 C3+가 되는 경우 warning
- recovery/focused C0–C2 Stage를 후반에도 남김

Exact threshold can be revised after generated distribution inspection.

---

# 9. Class-opportunity guardrail

10-Stage rolling window에서 각 class가 최소 한 번 이상 meaningful opportunity tag를 가져야 하는 것을 first candidate warning rule로 둔다.

이것은 class가 매 10 Stage마다 유리해야 한다는 뜻이 아니다.
장기간 `role starvation`을 탐지하기 위한 static warning이다.

---

# 10. Star-boundary guardrail

Stage19→20 / 39→40 difficulty가 보상 boundary 때문에 기계적으로 폭증하지 않게 한다.

- Stage20 = first meaningful gate, arbitrary spike 금지
- Stage40 = 2★ entry, intended late progression but cliff audit 필수

Stage41–45는 Lv31 acquisition 때문에 Stage40보다 무조건 연속 상승만 해야 하는 구간이 아니다.

---

# 11. Status

These ranges are now suitable for:
- candidate Stage-signature generation
- static distribution search
- representative recipe selection

They are not production encounter frequencies.
