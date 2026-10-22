# Timing Defense — Lv31 Mastery Play Window V0.1

Date: 2026-10-22 KST  
Status: **USER-CONFIRMED DIRECTION + CALIBRATION HYPOTHESIS / NO EXP NUMERIC FREEZE**

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
 -> Lv31 unlock
 -> 여러 Stage에서 실전 사용
 -> class-specific mastery/opportunity 확인
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

# 2. First calibration hypothesis

Exact EXP / Stage reach는 아직 freeze하지 않는다.

첫 simulation hypothesis:

```text
SKILLED_V2 expected Lv31 reach window ~= Stage38..42
```

의도:
- Stage50 이전 약 8~12 Stage의 meaningful use opportunity 확보
- Stage41~49 Mastery Exam band에서 Lv31을 반복 사용
- Stage50은 첫 사용처가 아니라, 이미 익숙해진 최종 스킬을 종합적으로 활용하는 곳

중요:
- `38..42`는 production freeze가 아니라 initial calibration window다.
- 실제 EXP/encounter/kill-event 구조에 따라 이동 가능하다.
- 그러나 `Lv31이 사실상 Stage49/50에서 처음 활성화`되는 결과는 기본적으로 FAIL로 취급한다.

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
post-Lv31 meaningful Stage count
post-Lv31 combat-event count
```

목적:
- 일부 고숙련 seed만 일찍 Lv31에 도달하고 대부분은 Stage49에서 도달하는 착시 방지
- class별 EXP/kill 구조 차이로 unlock window가 크게 벌어지는 문제 탐지

---

# 4. Mastery-band authoring consequence

Stage41~49는 단순히 적 수치를 올리는 구간이 아니다.

Lv31을 획득한 플레이어가 새 스킬의 성격을 실제로 체감할 기회를 포함해야 한다.

예:
- Knight: 큰 관통/전열 붕괴 가치를 체감할 line/screen 문제
- Rogue: rapid multi-hit 가치가 드러나는 durable/high-value normal target
- Tank: 광역 control/wall-protection 가치가 드러나는 압박
- Archer: 깊은 line/rear pressure를 관통하는 문제
- Mage: density/chain-explosion 가치가 드러나는 cluster/population 문제

단, 각 Stage가 특정 Lv31 스킬을 **필수 해법으로 요구해서는 안 된다**.
`hard class lockout` 금지 원칙은 유지한다.

---

# 5. Stage50과의 관계

Stage50 authoring은 Lv31의 존재를 고려할 수 있다.

하지만 원칙은:

```text
Stage50 = Lv31 첫 체험
```

이 아니라:

```text
Stage50 = 이미 여러 번 사용한 Lv31 + 기존 class kit + run growth의 종합 시험
```

이다.

Stage50 difficulty calibration에서:
- intended-entry SKILLED_V2가 Lv31을 이미 습득했을 확률
- Lv31 사용 경험 Stage 수
- class별 Lv31 power spike
를 함께 본다.

---

# 6. Lv26과 Lv31 사이 간격

Lv31을 일찍 준다고 Lv26의 존재감이 사라져서는 안 된다.

따라서 Player Power Spine은 다음을 동시에 만족해야 한다.

1. Lv26을 획득한 뒤 체감 가능한 사용 구간 존재
2. Lv31을 획득한 뒤에도 체감 가능한 사용 구간 존재
3. Lv31이 Stage50 직전에 몰리지 않음
4. Lv6/11/16/21/26/31 power spikes가 신규 monster teaching과 과도하게 겹치지 않음

즉 EXP curve는 단순 등간격이 아니라 **각 unlock 이후의 실제 play window**를 기준으로 설계한다.

---

# 7. Difficulty target과의 결합

일반 non-T1 Tier의 난도 목표:

```text
intended-entry SKILLED_V2 full-Tier clear probability < 60%
```

Lv31을 Stage38~42에 주는 것은 게임을 쉽게 만들기 위한 조치가 아니다.

오히려:
- 후반 Stage는 Lv31 power를 전제로 다시 calibration
- Lv31 획득 전/후 difficulty slope를 별도 측정
- unlock 직후 갑자기 trivialize되는지 검사
- class별 Lv31 효과 차이 때문에 clear-rate 편차가 과도해지는지 검사

해야 한다.

새 failure classifications:
- `INSUFFICIENT_LV31_PLAY_WINDOW`
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
- Stage41~49 class-opportunity coverage
- Stage50 진입 시 Lv31 보유율

First calibration guardrail:
- SKILLED_V2 median Lv31 unlock이 Stage38~42 근처인지 확인
- 대부분의 serious Stage50 attempts에서 Lv31을 이미 여러 Stage 사용한 상태인지 확인

Exact cutoffs는 simulation 후 결정한다.

---

# 9. Cross-category dependencies

이 원칙은 다음과 직접 연결된다.

- Master Campaign Progression Spine
- 50-Stage macro bands
- EXP curve
- class skill authority Lv11~31
- monster novelty timing
- Stage41~49 encounter authoring
- Stage50 difficulty
- shop/run power
- skilled clear-rate target

따라서 EXP curve만 독립적으로 조정하지 않는다.

---

# 10. 현재 결정 상태

USER-CONFIRMED:
- Lv31은 Stage50 한 번 사용용이어서는 안 됨.
- 획득 뒤 충분한 Stage에서 즐길 수 있어야 함.

CALIBRATION HYPOTHESIS:
- SKILLED_V2 Lv31 expected reach `Stage38..42`
- Stage41~49 = Lv31 mastery-use band 역할 포함
- 대략 8~12 Stage의 후반 사용기회 확보를 첫 목표로 검증

OPEN:
- exact EXP formula
- exact Stage unlock distribution
- class별 동일/상이 unlock timing 허용폭
- exact minimum post-Lv31 Stage count
- Stage50 Lv31 possession probability threshold

No live gameplay code or production EXP value is authorized by this document.
