# Timing Defense — Skill × Monster Novelty Collision Audit V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL AUDIT / MODEL A**

Depends on:
- `21_MODEL_A_NOVELTY_BUDGET_AND_BOSS_PLACEHOLDERS_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`

---

# 0. 목적

신규 monster teaching과 class skill unlock이 같은 구간에 겹치면서:
- 플레이어가 무엇 때문에 전투가 달라졌는지 이해하지 못하거나,
- skill power spike가 신규 monster 난도를 가려버리거나,
- 반대로 신규 monster 압박이 skill 획득의 보상감을 지워버리는 문제
를 사전에 찾는다.

---

# 1. Collision type

## P — Pedagogic collision
두 개 이상의 **처음 배우는 규칙**이 짧은 구간에 중첩.

가장 중요:
- class T1
- new monster first teach
- first-time skill explanation

## C — Calibration collision
이미 아는 skill이라도 power spike가 monster difficulty 측정을 왜곡.

가장 중요:
- T2+
- first high-pressure monster use
- Lv21/26/31 spike

## R — Reward masking
새 skill을 얻었는데 곧바로 hard counter-like encounter를 던져 보상감이 사라짐.

---

# 2. Player power candidate windows

- Lv6: 5–7
- Lv11: 11–14
- Lv16: 18–21
- Lv21: 25–28
- Lv26: 32–36
- Lv31: 41–45

---

# 3. Model A monster teaching windows candidate

정확한 Stage freeze가 아니라 collision audit용 window다.

## T1
- GRUNT baseline: 1–3
- RUNNER first teach: 6–9
- BRUTE first teach: 15–18
- first high-pressure BRUTE/RUNNER combinations: 21–29

## T2
- SHIELD first teach: 5–9
- FLYER first teach: 14–18
- high-pressure geometry/mitigation combinations: 23–31

## T3
- CHARGER first teach: 5–9
- SPLITTER first teach: 15–19
- high-pressure stateful combinations: 24–31

## T4
- returning formation recap: 1–9
- SUPPORTER first teach: 11–15
- SUPPORTER mixed: 16–19
- SIEGER first teach: 22–25
- SIEGER mixed: 26–29
- combined support/siege pressure: 31–39
- Lv31 Ascension: 41–45
- post-Lv31 mastery: 46–49

---

# 4. T1 audit

T1은 skill 자체도 처음 배우므로 pedagogic collision이 가장 중요하다.

### Lv6 5–7 × RUNNER 6–9
Collision: **WATCH**.

둘 다 비교적 단순하다.
- Lv6는 class identity 강화
- RUNNER는 지속 speed pressure

Guardrail:
- RUNNER first appearance 직후 수량/tempo를 낮게 유지
- Lv6 tutorial/presentation을 짧고 명확하게

### Lv11 11–14 × BRUTE 15–18
Collision: **PASS**.
명확히 분리 가능.

### Lv16 18–21 × BRUTE mixed/high-pressure transition
Collision: **WATCH calibration**.
Lv16 power spike가 BRUTE difficulty를 갑자기 낮출 수 있음.

### Lv21 25–28 × first high-pressure combination
Collision: **WATCH**.
T1에서는 처음 배우는 Lv21이므로 encounter signature를 지나치게 복잡하게 하지 않는다.

### Lv26 32–36
새 core monster teaching 없음.
Collision: **PASS**.

### Lv31 41–45
new ordinary teaching 없음.
Collision: **PASS / desired**.

T1 conclusion:
- pedagogic novelty가 가장 높은 Tier지만 현재 spacing으로 구조적으로 수용 가능.
- Stage25–28은 first-time Lv21 때문에 encounter complexity cap을 두는 것이 좋다.

---

# 5. T2 audit

Skills are mostly familiar power spikes.

### SHIELD 5–9 × Lv6 5–7
Pedagogic collision: LOW.
Calibration collision: WATCH.

Lv6 강화 직후 SHIELD armor를 경험하면 class별 체감이 크게 갈릴 수 있으므로 SHIELD production armor 수치는 Lv6-on 상태를 기준으로도 분석.

### FLYER 14–18 × Lv11/Lv16 boundary
Pedagogic collision: low.
Geometry teaching은 skill power와 독립성이 높아 비교적 안정적.

### High-pressure T2 23–31 × Lv21 25–28
Calibration collision: WATCH.
First high-pressure FLYER/SHIELD composition을 Lv21 exact unlock과 같은 1–2 Stage에 고정하지 않는다.

T2 conclusion: **PASS candidate**.

---

# 6. T3 audit

### CHARGER 5–9 × Lv6
WATCH.
Lv6 Tank knockback 등 class skill에 따라 CHARGER interrupt 성공률이 크게 달라질 수 있으므로 teaching encounter는 Lv6 유무와 무관하게 읽을 수 있어야 함.

### SPLITTER 15–19 × Lv16 18–21
WATCH.
Mage/area skill spike와 child density가 겹치면 SPLITTER가 특정 class에서 너무 쉬워질 가능성.

### Combined pressure 24–31 × Lv21 25–28
WATCH/HIGH.
CHARGER+SPLITTER synergy를 Lv21 획득 바로 직후 maximal intensity로 올리지 않는다.

T3 conclusion:
**PASS with explicit power-spike calibration.**

---

# 7. T4 audit

### SUPPORTER 11–19 × Lv11/Lv16
Skills familiar.
Pedagogic collision low, calibration collision moderate.

### SIEGER 22–29 × Lv21 25–28
Calibration collision: **HIGH WATCH**.
Lv21 heavy upgrades가 screen removal / siege exposure 속도를 크게 바꿀 수 있음.

Guardrail:
- SIEGER first teach는 low-intensity before Lv21 median.
- first meaningful high-pressure SIEGER package는 Lv21 window 직후 별도 Stage에서 측정.

### combined SUPPORTER/SIEGER 31–39 × Lv26 32–36
Calibration collision: **HIGH WATCH**.
Lv26 class별 late specialization이 support/siege uptime을 크게 바꿀 수 있음.

Guardrail:
- 31–33: low/moderate combined
- 34–36: power-transition observation
- 37–39: post-Lv26 high-pressure comparison

### Lv31 41–45
SUPPORTER/SIEGER first-teach already closed.
This is intentional.

Guardrail:
- Stage41–45를 campaign peak-pressure로 만들지 않는다.
- unlock acquisition + controlled mastery runway.

### Stage46–49
Lv31 assumed/familiarizing.
- high-pressure support/siege mastery 가능
- 각 class Lv31 opportunity를 rotating encounters로 제공

T4 conclusion:
**WATCH but PASSABLE.**
가장 중요한 collision은 Lv26/Lv31과 late support/siege pressure의 관계다.

---

# 8. General spacing rule

## First teach rule
Major new monster first teach와 major first-time class skill learning은 가능한 한 같은 Stage에 배치하지 않는다.

## High-pressure rule
New monster `firstHighPressureStage`는 major power milestone median의 ±2 Stage를 기본적으로 피한다.
예외 시 별도 calibration justification 필요.

## Ascension rule
Stage41–45:
- Lv31 acquisition window
- new core ordinary first-teach 금지
- unpreviewed boss mechanic 금지
- maximum-complexity composition을 연속 배치하지 않음

---

# 9. Audit verdict

Model A skill×monster novelty collision result:
- T1: WATCH, manageable
- T2: PASS
- T3: PASS/WATCH
- T4: WATCH/HIGH but manageable with phased late band

**No structural FAIL found.**

Model A는 이 관점에서 bounded simulation candidate로 유지 가능하다.
