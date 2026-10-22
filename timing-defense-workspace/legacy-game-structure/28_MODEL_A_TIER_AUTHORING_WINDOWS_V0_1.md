# Timing Defense — Model A Tier Authoring Windows V0.1

Date: 2026-10-22 KST  
Status: **SIMULATION AUTHORING CANDIDATE / RANGE-BASED, NOT EXACT STAGE FREEZE**

---

# 0. 목적

Model A의 각 신규 monster가 Tier 안에서 언제:
- 처음 보이고
- 기존 적과 섞이고
- 본격 압박으로 승격되는지
range 수준에서 정의한다.

Exact Stage recipe가 아니라 authoring window다.

---

# 1. Common skill overlay

- Lv6: 5–7
- Lv11: 11–14
- Lv16: 18–21
- Lv21: 25–28
- Lv26: 32–36
- Lv31: 41–45

firstHighPressure는 major milestone median ±2와 겹치지 않는 방향을 우선한다.
GRUNT처럼 capability novelty가 없는 baseline pressure는 이 경고에서 별도 취급한다.

---

# 2. T1 introduction windows

Available after Tier start:
- GRUNT
- RUNNER
- BRUTE

| Monster | First teach candidate | First mixed candidate | First high-pressure candidate | Note |
|---|---|---|---|---|
| GRUNT | 1–2 | 4–6 | 21–29 | neutral baseline; skill-collision warning exempt |
| RUNNER | 5–7 | 8–12 | 21–24 | Lv6 overlap; first teach conservative |
| BRUTE | 15–17 | 18–20 | 21–23 | high-pressure before Lv21 window; later 24–29 can mix without first-pressure attribution |

Guardrail:
- Stage1–3 no unnecessary special grammar
- Stage41+ no new monster teaching

---

# 3. T2 introduction windows

New:
- SHIELD
- FLYER

Returning G/R/B available from Stage1.

| Monster | First teach | First mixed | First high-pressure | Note |
|---|---|---|---|---|
| SHIELD | 5–7 | 8–12 | 21–24 | durability vs mitigation contrast |
| FLYER | 15–17 | 18–22 | 28–31 | geometry first, then harder mixed use |

Guardrail:
- first FLYER does not require class-specific vertical counter
- high-pressure SHIELD and FLYER need not occur simultaneously

---

# 4. T3 introduction windows

New:
- CHARGER
- SPLITTER

Returning G/R/B/SH/F available.

| Monster | First teach | First mixed | First high-pressure | Note |
|---|---|---|---|---|
| CHARGER | 5–7 | 8–14 | 21–24 | windup readability first |
| SPLITTER | 15–17 | 18–22 | 28–31 | authored vs effective entity separation |

Guardrail:
- CHARGER first teach survivable without Tank
- SPLITTER high pressure after child-volume model verified
- maximal C+SP overlap not during Lv21 transition

---

# 5. T4 introduction windows

New:
- SUPPORTER
- SIEGER

Returning previous 7 available.

| Monster | First teach | First mixed | First high-pressure | Note |
|---|---|---|---|---|
| SUPPORTER | 11–13 | 14–19 | 29–31 | first high-pressure before Lv26 median; combined synergy can continue later |
| SIEGER | 22–24 | 25–29 | 37–39 | objective pressure after Lv26 transition |

Required:
- SUPPORTER and SIEGER first-teach separated
- SUPPORTER-focused high pressure can occur before combined support/siege peak
- combined high-pressure only after both mixed windows
- Stage41–45 no new core mechanic

---

# 6. Returning monster reinterpretation

Unlock된 monster는 later Tier에서 단순 반복하지 않는다.

Examples:
- BRUTE: T1 raw durable target -> T2 SHIELD contrast -> T4 screen anchor
- RUNNER: T1 tempo -> T3 CHARGER sustained-vs-burst contrast -> T4 SUPPORTER aura carrier
- FLYER: T2 geometry -> T3 tempo/population geometry -> T4 split-axis distraction
- SHIELD: T2 mitigation -> T4 protected backline screen
- SPLITTER: T3 population -> T4 escort/density pressure

---

# 7. Introduction validator rules

For every new ordinary monster:
```text
firstTeach <= firstMixed <= firstHighPressure
```

Warnings:
- firstTeach Stage40+
- firstHighPressure before readable mixed use
- two major new firstTeach events within same 3-Stage window
- non-baseline firstHighPressure within major skill median ±2 without justification

---

# 8. Layer-0 precheck revision note

Initial automatic precheck found:
- T1 BRUTE first-high-pressure too close to Lv21
- T4 SUPPORTER first-high-pressure too close to Lv26

V0.1 windows were adjusted:
- BRUTE 24–29 -> **21–23**
- SUPPORTER 31–33 -> **29–31**

This does not freeze exact Stage recipes. It reduces attribution ambiguity before simulation.

---

# 9. Status

These ranges are the **default authoring candidate for bounded simulation**.
They are not production Stage locks.

If simulation/playtest shows overload, ranges can move while preserving:
- Tier monster unlock ladder
- Lv31 Stage41–45
- no new core teaching in final band
