# Timing Defense — Lv31 Mastery Play Window V0.2

Date: 2026-10-22 KST  
Status: **USER-CONFIRMED STRUCTURAL WINDOW / NO EXP NUMERIC FREEZE**

---

# 0. 목적

Lv31 최종 스킬을 Tier 50 Stage의 마지막 순간에만 사용하게 되는 구조를 방지한다.

사용자 의도:

> 기껏 Lv31 스킬을 습득했는데 Stage50에서 한 번 써보고 run이 끝나는 구조는 피한다.  
> Lv31을 획득한 뒤 여러 Stage에서 실제로 사용하고 숙련한 뒤 Tier Final에 들어가야 한다.

따라서 Lv31은 단순한 `final reward`가 아니라 **late-run mastery tool**이다.

---

# 1. 핵심 구조

원하는 경험:

```text
Lv26 late-game growth
 -> Stage41~45 Lv31 unlock
 -> Stage46~49 실전 사용 / 적응 / 숙련
 -> Stage50 Tier Final에서 완성된 활용
```

원하지 않는 경험:

```text
Stage49~50 근처에서 Lv31 unlock
 -> 한두 번 사용
 -> Tier 종료
```

후자는 `INSUFFICIENT_LV31_PLAY_WINDOW` 구조 결함으로 분류한다.

---

# 2. User-confirmed Lv31 target window

Lv31의 목표 획득 구간은 다음으로 확정한다.

```text
Lv31 target unlock window = Stage41..45
```

의도:
- Lv31을 Tier Final 직전의 일회성 보상으로 만들지 않음
- 늦어도 Stage45까지는 획득하여 Stage46~49에서 별도의 실전 사용구간 확보
- Stage50은 첫 사용처가 아니라 이미 사용 경험이 있는 최종 스킬의 종합 활용처

중요:
- `Stage41..45`는 **구조적 목표 획득 window**다.
- 정확한 EXP formula / kill EXP / timing EXP / Stage별 EXP budget은 아직 freeze하지 않는다.
- 추후 EXP curve는 이 window를 만족하도록 calibration한다.
- class별 미세한 도달분포 차이는 허용할 수 있으나, 특정 class가 구조적으로 Stage49~50에서야 Lv31에 도달하는 결과는 허용하지 않는다.

---

# 3. Distribution으로 측정

평균 unlock Stage 하나만 보지 않는다.

Tier simulation은 class/mastery/profile별로 최소 다음을 기록한다.

```text
Lv31 reach probability by Stage
P25 Lv31 unlock Stage
P50 Lv31 unlock Stage
P75 Lv31 unlock Stage
P90 Lv31 unlock Stage
post-Lv31 pre-final Stage count
post-Lv31 combat-event count
```

목적:
- 일부 고숙련 seed만 Stage41~45에 도달하고 대부분은 Stage49에서 도달하는 착시 방지
- class별 EXP/kill 구조 차이로 unlock window가 크게 벌어지는 문제 탐지

초기 simulation 판단:
- `P50`이 Stage41~45 밖으로 벗어나면 원인 분석
- Stage45 이후 도달 비율이 높으면 `LATE_LV31_DISTRIBUTION` 경고
- Stage49~50이 첫 meaningful use가 되는 다수 경로는 FAIL

정확한 percentile cutoff는 simulation 후 freeze한다.

---

# 4. Stage46~49 mastery-use band

Stage46~49는 단순히 적 수치를 올리는 구간이 아니다.

Lv31을 획득한 플레이어가 새 스킬의 성격을 실제로 체감하고 몇 차례 반복해서 사용할 기회를 제공해야 한다.

예:
- Knight: 큰 관통/전열 붕괴 가치를 체감할 line/screen 문제
- Rogue: rapid multi-hit 가치가 드러나는 durable/high-value normal target
- Tank: 광역 control/wall-protection 가치가 드러나는 압박
- Archer: 깊은 line/rear pressure를 관통하는 문제
- Mage: density/chain-explosion 가치가 드러나는 cluster/population 문제

단, 각 Stage가 특정 Lv31 스킬을 **필수 해법으로 요구해서는 안 된다**.
`hard class lockout` 금지 원칙은 유지한다.

Stage41~45는 Lv31 획득 전환구간이므로, 일부 플레이어는 이미 Lv31을 쓰고 일부는 아직 Lv26 이하 상태일 수 있다.
따라서 이 구간의 encounter는 양쪽 상태 모두에서 구조적으로 통과 가능해야 한다.

---

# 5. Stage50과의 관계

Stage50 authoring은 Lv31의 존재를 고려할 수 있다.

하지만 원칙은:

```text
Stage50 = Lv31 첫 체험
```

이 아니라:

```text
Stage50 = Stage41~45에서 획득하고 Stage46~49에서 익힌 Lv31
        + 기존 class kit
        + run growth의 종합 시험
```

이다.

Stage50 difficulty calibration에서:
- intended-entry SKILLED_V2의 Stage50 진입 시 Lv31 보유율
- Stage46~49에서의 Lv31 사용 경험
- class별 Lv31 power spike
를 함께 본다.

---

# 6. Lv26과 Lv31 사이 간격

Lv31을 Stage41~45에 준다고 Lv26의 존재감이 사라져서는 안 된다.

따라서 Player Power Spine은 다음을 동시에 만족해야 한다.

1. Lv26을 획득한 뒤 체감 가능한 사용 구간 존재
2. Lv31은 Stage41~45를 목표 획득구간으로 사용
3. Lv31 획득 뒤 Stage46~49의 체감 가능한 사용 구간 존재
4. Stage50은 Lv31 tutorial이 아님
5. Lv6/11/16/21/26/31 power spikes가 신규 monster teaching과 과도하게 겹치지 않음

즉 EXP curve는 단순 등간격이 아니라 **각 unlock 이후의 실제 play window**를 기준으로 설계한다.

---

# 7. Difficulty target과의 결합

일반 non-T1 Tier의 난도 목표:

```text
intended-entry SKILLED_V2 full-Tier clear probability < 60%
```

Lv31을 Stage41~45에 주는 것은 게임을 쉽게 만들기 위한 조치가 아니다.

오히려:
- Stage46~50은 Lv31 power를 고려해 calibration
- Lv31 획득 전/후 difficulty slope를 별도 측정
- unlock 직후 갑자기 trivialize되는지 검사
- class별 Lv31 효과 차이 때문에 clear-rate 편차가 과도해지는지 검사

해야 한다.

Failure classifications:
- `INSUFFICIENT_LV31_PLAY_WINDOW`
- `LATE_LV31_DISTRIBUTION`
- `LV31_POWER_CLIFF_TOO_HIGH`
- `LV31_CLASS_CLEAR_RATE_DIVERGENCE`
- `LV26_WINDOW_COMPRESSED`

---

# 8. Simulation acceptance inputs

Player Power Spine simulation에서 최소 기록:

- Lv6/11/16/21/26/31 unlock distribution
- 각 skill unlock 후 남은 Stage 수
- 각 skill unlock 후 meaningful combat-event 수
- Lv31 unlock 전 clear/fail rate
- Lv31 unlock 후 clear/fail rate
- Stage41~45 unlock distribution
- Stage46~49 class-opportunity coverage
- Stage50 진입 시 Lv31 보유율

Structural target:
- Lv31 primary unlock band = Stage41~45
- Stage46~49 = explicit post-Lv31 mastery-use band
- Stage50 = final application, not first meaningful use

Exact EXP values and percentile acceptance cutoffs remain simulation outputs/decision inputs.

---

# 9. Cross-category dependencies

이 원칙은 다음과 직접 연결된다.

- Master Campaign Progression Spine
- 50-Stage macro bands
- EXP curve
- class skill authority Lv11~31
- monster novelty timing
- Stage41~45 difficulty transition
- Stage46~49 encounter authoring
- Stage50 difficulty
- shop/run power
- skilled clear-rate target

따라서 EXP curve만 독립적으로 조정하지 않는다.

---

# 10. 현재 결정 상태

USER-CONFIRMED:
- Lv31은 Stage50 한 번 사용용이어서는 안 됨.
- 획득 뒤 충분한 Stage에서 즐길 수 있어야 함.
- **Lv31 목표 획득구간 = Stage41~45.**

STRUCTURAL CONSEQUENCE:
- Stage46~49를 post-Lv31 mastery-use band로 활용.
- Stage50은 Lv31 첫 사용이 아니라 최종 활용 시험.

OPEN:
- exact EXP formula
- class별 unlock distribution 허용폭
- percentile acceptance threshold
- Stage50 Lv31 possession probability threshold

No live gameplay code or production EXP value is authorized by this document.
