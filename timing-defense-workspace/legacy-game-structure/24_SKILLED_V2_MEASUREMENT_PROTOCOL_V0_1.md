# Timing Defense — SKILLED_V2 Measurement Protocol V0.1

Date: 2026-10-22 KST  
Status: **CALIBRATION PROTOCOL / NO PLAYER-SKILL NUMERIC FREEZE**

Depends on:
- `06_SIMULATION_CALIBRATION_PLAN.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`

---

# 0. 목적

`숙련자 full-Tier clear <60%`라는 난도 목표가 의미 있으려면, 먼저 simulation의 `숙련자`가 실제 숙련 플레이를 충분히 강하게 모델링해야 한다.

기존 skilled profile은 사용자의 실제 플레이 감각에 비해 낮았을 가능성이 있다.

User calibration evidence:
- 집중하면 combo 40은 쉽게 달성 가능
- 현재 prototype stages는 체감상 너무 쉬웠음

따라서 기존 skilled를 그대로 사용하지 않고 `SKILLED_V2`를 재정의한다.

---

# 1. 핵심 철학

SKILLED_V2는:
- 초보/평균보다 명확히 강함
- combo 40이 극단적 tail event가 아님
- PERFECT/GOOD를 안정적으로 만들어냄
- heavy completion을 의도적으로 활용
- recovery/target turnover에 익숙함
- 하지만 실수 0%, 무한 combo, perfect-only bot은 아님

`HIGH_MASTERY_STRESS`는 별도 상위 profile이다.

---

# 2. 단일 확률벡터로 모델링하지 않는다

단순히:
```text
PERFECT 70 / GOOD 20 / NORMAL 10
```
같은 iid 분포 하나만으로 숙련자를 만들지 않는다.

실전에서는:
- 압박이 높을수록 timing error 증가
- target turnover에서 rhythm이 깨질 수 있음
- combo가 길어질수록 집중 유지가 달라짐
- heavy pair는 단일 입력과 다른 성공확률을 가짐

따라서 profile은 **context-sensitive parameters**를 가진다.

---

# 3. 측정해야 할 최소 변수

## Timing outcome
- PERFECT share
- GOOD share
- NORMAL share
- MISS/invalid share

## Combo
- combo 10 reach rate
- combo 20 reach rate
- combo 40 reach rate
- combo 60+ reach rate
- longest combo distribution
- combo break causes

## Heavy / P×P
- heavy opportunity count
- heavy completion rate
- P×P completion rate
- heavy attempt abandonment/error

## Pressure sensitivity
동일 플레이어에서:
- low pressure
- tempo pressure
- density pressure
- stateful pressure
에 따른 timing degradation.

## Recovery / target turnover
- next valid turn reacquisition
- target death/reorder 이후 첫 입력 accuracy
- no-target wait 이후 rhythm recovery

---

# 4. Calibration harness set

실제 campaign 전체를 이용해 skilled profile을 역추정하지 않는다.
작은 controlled harness를 먼저 둔다.

## H0 — Timing Baseline
- 단순 GRUNT
- low cadence
- geometry 없음

목적:
순수 timing ceiling 측정.

## H1 — Sustained Tempo
- RUNNER / faster cadence

목적:
지속 pressure에서 accuracy/combo 유지 측정.

## H2 — Durable Rhythm
- BRUTE 중심

목적:
긴 target exposure에서 combo/heavy behavior 측정.

## H3 — Turnover / Density
- 다수 low-durability target

목적:
target reorder/kill turnover가 rhythm에 미치는 영향.

## H4 — Stateful Read
- CHARGER-like telegraph 또는 equivalent sandbox

목적:
입력 timing과 전술 판단을 동시에 요구할 때 degradation 측정.

## H5 — Mixed Pressure
- 2종 이상 mixed

목적:
campaign에 가까운 context sensitivity 측정.

---

# 5. Combo 40 anchor

User-confirmed qualitative anchor:
> 집중하면 combo 40은 쉽게 달성 가능.

따라서 SKILLED_V2에서 combo40은:
- ultra-rare event로 모델링 금지
- HIGH_MASTERY_STRESS 전용으로 분류 금지
- representative stable encounter에서 중앙/일상 숙련 range 안에 있어야 함

Exact probability는 telemetry 없이 지금 freeze하지 않는다.

First sweep에서는 최소 3개 sub-profile을 사용한다.

```text
SKILLED_V2_CONSERVATIVE
SKILLED_V2_CENTRAL
SKILLED_V2_STRONG
```

각 profile은 combo40 commonness와 timing accuracy를 달리하여 campaign 난도 결과의 민감도를 본다.

Production difficulty gate는 최종 CENTRAL profile 기준으로 판단한다.

---

# 6. 숙련자 난도 gate와의 결합

일반 non-T1 Tier:
```text
P(full clear Stage1→50 | intended-entry SKILLED_V2_CENTRAL) < 0.60
```

하지만 다음도 함께 본다.
- STRONG이 100%에 가까워지는가
- CONSERVATIVE가 거의 0%가 되는가
- class별 차이가 너무 극단적인가

즉 중앙값 하나만 맞추고 distribution을 망치지 않는다.

---

# 7. T1 exception

T1은 onboarding 역할 때문에 >60% 허용.

그러나 SKILLED_V2_CENTRAL이:
- 거의 항상 full HP
- combo 유지 실패 거의 없음
- 모든 class에서 90~100%에 가까운 full clear
이라면 난도가 너무 낮은 후보로 본다.

T1 exact acceptable range는 later decision.

---

# 8. Skill unlock timing measurement

Mastery profile은 EXP 획득량에도 영향을 주므로 다음을 함께 기록한다.

- Lv6 reach distribution
- Lv11 reach
- Lv16 reach
- Lv21 reach
- Lv26 reach
- Lv31 reach

특히:
- SKILLED_V2 Lv31 target window = Stage41–45
- HIGH_MASTERY가 지나치게 일찍 Lv31을 열어 후반을 trivialize하는지도 검사

---

# 9. Anti-overfit

한 사용자의 플레이만 그대로 simulator에 복제하지 않는다.
사용자 관찰은 기존 skilled가 낮다는 **강한 calibration anchor**지만, production profile은 여러 trace / sensitivity sweep으로 robust하게 만든다.

따라서:
1. qualitative anchor 적용
2. controlled trace 수집
3. parameter fitting
4. conservative/central/strong sweep
5. campaign sensitivity
순으로 간다.

---

# 10. Required output

SKILLED_V2 profile report는 최소:

```text
profileVersion
harnessVersion
sampleCount
PERFECT/GOOD/NORMAL/MISS by context
combo10/20/40/60 reach
longestCombo distribution
heavy completion
PP completion
pressure degradation
turnover degradation
Lv milestone reach distribution
```

을 제공한다.

---

# 11. Failure classifications

- `SKILLED_PROFILE_TOO_WEAK`
- `SKILLED_PROFILE_TOO_STRONG`
- `COMBO40_MODELED_AS_OUTLIER`
- `PRESSURE_DEGRADATION_UNMODELED`
- `HEAVY_USAGE_UNMODELED`
- `PROFILE_OVERFIT_SINGLE_TRACE`
- `DIFFICULTY_GATE_PROFILE_UNSTABLE`

---

# 12. 현재 상태

USER-CONFIRMED:
- 숙련자 기준을 기존보다 높게 잡아야 함.
- combo40은 숙련자에게 충분히 달성 가능한 수준.
- non-T1 숙련자 full-clear <60%.

OPEN:
- exact timing distribution
- combo survival values
- heavy completion values
- exact T1 target

이 문서는 수치를 임의로 확정하지 않고, 올바른 수치를 얻는 측정 절차를 고정한다.
