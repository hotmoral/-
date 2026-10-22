# Timing Defense — Class-Aware Action Trace Model V0.1

Date: 2026-10-22 KST  
Status: **LAYER-A MECHANICS MODEL / TRACE PARAMETERS NOT FITTED**

Depends on:
- `24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
- `40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`
- live `v036` Lv6 authority
- live `v039` N3 authority
- live v0.45 monster capability chain

Machine-readable bracket:
- `data/model_a_class_action_trace_bracket_v0_1.yaml`

Simulator:
- `../tools/simulate_class_aware_layer_a.py`

---

# 0. Purpose

Layer-A에서 generic DPS를 버리고 실제 class combat semantics를 넣기 위한 첫 deterministic model이다.

이 문서의 trace 값은 **SKILLED_V2 production calibration이 아니다.**

목적은:
1. current authority를 정확히 분리
2. class geometry/control 차이를 드러냄
3. representative encounter가 capability를 실제로 표현하는지 검사
4. telemetry fitting 전에도 구조 결함을 찾음

---

# 1. Authority mode

## CURRENT_AUTHORITY_LV1
- base timing attack
- heavy charge rule
- combo bonus
- authoritative N3 milestone attacks
- Lv6 skill OFF
- Lv11+ OFF

## CURRENT_AUTHORITY_LV6
- 위 항목 전부
- validated Lv6 class authority ON
- Lv11+ OFF

Lv11/16/21은 legacy-parity candidate이고, Lv26/31은 current production authority가 아니므로 이번 V0.1 결과에 섞지 않는다.

---

# 2. Base attack semantics reproduced

Raw damage:

```text
NORMAL 100
GOOD 140
PERFECT 200
HEAVY 180
HEAVY+ 230
GREAT 300
SUPER 400
CRITICAL 600
```

Combo damage bonus:

```text
5+  = +5%
10+ = +8%
20+ = +12%
30+ = +15%
```

Heavy:
- charge starts 0
- non-heavy attack increments charge up to 3
- action starting at charge 3 is heavy
- heavy consumes X + Y judgement
- then charge resets 0

---

# 3. Lv6 class authority reproduced

## Knight
- direct base-action raw damage ×1.12
- current server authority does not add Lv11 penetration here

## Rogue
- second dagger at +55 ms
- 55% of primary raw damage
- same target if alive, otherwise frontmost fallback

## Tank
- authoritative hit knockback receives +30% extra layer
- utility is control, not direct DPS

## Archer
- up to 2 line secondaries
- 52% raw damage each
- server line geometry reproduced from slot-1 origin

## Mage
- up to 3 nearby secondaries
- 50% raw damage each
- current splash rectangle/geometry reproduced

No Lv6 class effect recursively triggers itself.

---

# 4. N3 authority reproduced

Milestones:
`5 / 10 / 20 / 30 / every +10`

Budgets:
`60 / 90 / 150 / 210`

Class shapes:
- Knight: 67/33 split wave
- Rogue: milestone-scaled multiple daggers, +55 ms spacing
- Tank: 60/20/20 shock distribution
- Archer: 70/30 line burst
- Mage: 55/15/15/15 area burst

N3 remains:
- no recursive N3
- no recursive Lv6 skill proc
- normal armor / kill semantics
- NORMAL-equivalent generic knock

---

# 5. Trace bracket — important non-authority boundary

Current deterministic probes:

| Trace | action interval | perfect-judge streak | break judge |
|---|---:|---:|---|
| CONSERVATIVE bracket | 900 ms | 40 | GOOD |
| CENTRAL bracket | 750 ms | 55 | GOOD |
| STRONG bracket | 600 ms | 75 | GOOD |

These are **analysis brackets only**.

They are deliberately not called fitted SKILLED_V2 profiles.

Why:
- no controlled telemetry yet
- no measured target-turnover delay
- no context-sensitive degradation fit
- no MISS model fit
- no measured heavy abandonment probability

The bracket exists to expose whether encounter mechanics are robust or vanish across plausible throughput changes.

---

# 6. Optimistic bias

Current bracket has:
- target reacquire delay = 0
- deterministic judge stream
- no UI hesitation
- no pressure-specific accuracy loss

Therefore it is an **upper-throughput mechanics probe**.

If a capability disappears here, that does not automatically mean production failure.
But if it only appears at extremely slow traces, that is a strong authoring WATCH.

---

# 7. Required outputs

Per recipe × class × trace × power mode:
- first kill time
- kill order
- clear/end time
- peak active
- front reorder count
- wall damage
- combo peak
- N3 triggers
- Lv6 skill hits

Special:
- CHARGER windup / complete / interrupt / erased-before-windup
- SPLITTER parent/child/wall leak
- SUPPORTER aura / screened aura
- SIEGER first shot / total shots / screened shots
- FLYER class-skill hit opportunity

---

# 8. Interpretation rule

Do not optimize for shortest clear time alone.

Examples:
- Tank knockback can make clear time longer while reducing objective danger.
- Mage/Rogue may clear fast but can erase the special capability before it becomes readable.
- Archer geometry value depends on actual line alignment, not monster count.

Therefore class opportunity is multi-metric.

---

# 9. Next

Run critical representative recipe subset first.

If the special capability disappears across all classes/traces:
1. inspect entry depth / formation / timing first
2. inspect protection/exposure timing
3. only then consider provisional HP/speed/capability-number changes

Do not patch global HP as first response.
