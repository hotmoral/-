# Timing Defense — Player Power Spine Lv6–31 V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL CALIBRATION CANDIDATE / NO EXP FORMULA FREEZE**

Depends on:
- `SKILL_PLAN_LV6_31.md`
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
- `21_MODEL_A_NOVELTY_BUDGET_AND_BOSS_PLACEHOLDERS_V0_1.md`

---

# 0. 목적

50 Stage Tier에서 Lv6/11/16/21/26/31 스킬이 너무 초반에 몰리거나, 반대로 Lv31이 Stage50 직전에만 열리는 문제를 방지한다.

핵심 원칙:
> 각 skill milestone은 unlock 자체보다 **unlock 이후 실제로 사용할 수 있는 play window**까지 포함해서 설계한다.

---

# 1. First reach-band candidate

Exact EXP formula가 아니라 simulation target window다.

| Milestone | SKILLED_V2 reach-band candidate | Structural purpose |
|---|---|---|
| Lv6 | Stage 5–7 | early identity activation |
| Lv11 | Stage 11–14 | early-mid specialization |
| Lv16 | Stage 18–21 | mid-run timing payoff |
| Lv21 | Stage 25–28 | mid-late signature expansion |
| Lv26 | Stage 32–36 | late specialization |
| Lv31 | **Stage 41–45** | final skill acquisition with usable runway |

USER-CONFIRMED fixed direction:
- Lv31 target window = Stage41–45.

나머지 reach bands는 first calibration candidate이며 simulation에 따라 이동 가능하다.

---

# 2. Why this spacing

대략적인 unlock 간격:
- Lv6→11: 4–9 Stages
- Lv11→16: 4–10
- Lv16→21: 4–10
- Lv21→26: 4–11
- Lv26→31: 5–13

의도:
- skill novelty를 50 Stage 전체에 분산
- higher milestone일수록 충분한 anticipation 제공
- Lv26과 Lv31 모두 체감 가능한 구간 확보

등간격 강제는 아니다.

---

# 3. Post-unlock play-window requirement

Stage50까지 남는 최소/최대 범위를 구조적으로 본다.

| Milestone | Candidate unlock | Approx post-unlock runway to Stage50 |
|---|---|---|
| Lv6 | 5–7 | very long |
| Lv11 | 11–14 | long |
| Lv16 | 18–21 | long-mid |
| Lv21 | 25–28 | mid |
| Lv26 | 32–36 | ~14–18 Stage-class window |
| Lv31 | 41–45 | ~5–9 Stage-class window incl. final |

정확한 사용횟수는 Stage 수가 아니라 combat-event 수로도 측정한다.

---

# 4. Late-band split

기존 `Stage41–49 Mastery Exam`을 power-spine 관점에서 둘로 나눈다.

## Stage41–45 — LV31 ASCENSION WINDOW
목적:
- intended SKILLED_V2가 Lv31에 도달
- final skill의 첫 실전 활용
- unlock 직후 즉시 최대압박을 던지지 않음
- 이미 배운 Tier mechanics를 moderate-high pressure에서 재사용

## Stage46–49 — POST-LV31 MASTERY
목적:
- Lv31의 class role이 실제로 유의미한 encounter 제공
- final skill을 여러 번 반복 사용
- Stage50 직전 mastery proof

## Stage50 — TIER FINAL
- Lv31 tutorial 아님
- already-familiar full class kit의 종합 시험

---

# 5. First-time learning vs repeated run power spike

매 Tier에서 run은 Lv1부터 시작하므로 Lv6~31을 매번 다시 unlock한다.
하지만 의미가 다르다.

## Class T1
- 해당 class skill을 처음 배우는 **pedagogic novelty** 가능성이 큼.

## Same class T2+
- 이미 알고 있는 skill이 다시 활성화되는 **power progression event**.

따라서 T2+ new monster first-teach와 familiar skill unlock이 겹쳐도 학습 과부하로 자동 판정하지 않는다.
대신 power spike가 monster difficulty를 가리는지 검사한다.

---

# 6. Milestone role map by class

## Knight
- Lv6: baseline blade-wave uplift
- Lv11: penetration identity 확립
- Lv16: PERFECT payoff
- Lv21: large heavy wave
- Lv26: penetration scaling mastery
- Lv31: battlefield-scale frontline collapse

## Rogue
- Lv6: multihit identity 시작
- Lv11: crit specialization
- Lv16: rhythm/recovery reward
- Lv21: heavy barrage
- Lv26: secondary tracking expansion
- Lv31: high-density dagger storm

## Tank
- Lv6: control identity 강화
- Lv11: wall protection
- Lv16: PERFECT shield
- Lv21: broad heavy control
- Lv26: persistent slow/control zone
- Lv31: field-wide control + barrier

## Archer
- Lv6: penetration identity 시작
- Lv11: base projectile uplift
- Lv16: armor-ignore PERFECT
- Lv21: heavy triple shot
- Lv26: deeper full-damage penetration
- Lv31: battlefield-line penetration

## Mage
- Lv6: AoE identity 시작
- Lv11: area expansion
- Lv16: delayed outer ring
- Lv21: larger heavy orb
- Lv26: chain explosion
- Lv31: large multi-stage collapse

---

# 7. Calibration acceptance metrics

각 milestone별:
- unlock Stage distribution P25/P50/P75/P90
- unlock 후 남은 Stage 수
- unlock 후 meaningful combat-event 수
- pre/post unlock damage/control effectiveness
- clear-rate slope around unlock

특히 Lv31:
- expected SKILLED_V2 unlock은 Stage41–45
- P75가 Stage45를 과도하게 넘기면 WATCH/FAIL candidate
- Stage49/50 first meaningful use = FAIL

정확한 percentile cutoff는 first simulation 후 조정한다.

---

# 8. Failure classifications

- `SKILL_REACH_TOO_EARLY`
- `SKILL_REACH_TOO_LATE`
- `SKILL_WINDOW_COMPRESSED`
- `LV26_WINDOW_COMPRESSED`
- `INSUFFICIENT_LV31_PLAY_WINDOW`
- `LV31_POWER_CLIFF_TOO_HIGH`
- `LV31_CLASS_CLEAR_RATE_DIVERGENCE`
- `SKILL_MONSTER_ATTRIBUTION_COLLISION`

---

# 9. EXP curve design consequence

EXP formula는 기존 legacy 값을 그대로 늘리지 않는다.

목표는:
```text
EXP model
 -> simulated unlock distribution
 -> desired Stage reach bands 충족
```

방향으로 역산한다.

즉 `levelNeed` 공식을 먼저 정하고 Stage를 맞추는 것이 아니라, campaign power-spine을 먼저 정하고 EXP를 calibration한다.

---

# 10. Status

USER-CONFIRMED:
- Lv31 Stage41–45 target window.
- Stage50 전에 충분히 즐길 수 있어야 함.

CANDIDATE:
- Lv6 5–7
- Lv11 11–14
- Lv16 18–21
- Lv21 25–28
- Lv26 32–36

OPEN:
- exact EXP formula
- exact percentile requirements
- class-specific reach variance
- shop/kill/skill interaction with EXP
