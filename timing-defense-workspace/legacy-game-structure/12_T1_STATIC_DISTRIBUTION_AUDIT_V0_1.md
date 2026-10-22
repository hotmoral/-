# Timing Defense — T1 Static Distribution Audit V0.1

Date: 2026-10-22 KST  
Status: **STATIC STRUCTURAL AUDIT / NO COMBAT SIMULATION YET**

Source candidate:
`11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`

## 0. 목적

실제 monster count/HP/cadence를 넣기 전에 Stage skeleton만으로:
- archetype repetition
- pressure-family 과대표현
- complexity concentration
- teaching 순서
- star-boundary 구조
를 검사한다.

숫자 밸런스 시뮬레이션보다 먼저 발견 가능한 오류를 지금 제거한다.

---

# 1. Event occurrence count

V0.1은 50 Stage에 총 **63 encounter occurrences**를 가진다.
한 Stage에 여러 separated phase가 있으면 각각 occurrence로 센다.

| Archetype | Occurrences |
|---|---:|
| E01 BASELINE_MARCH | 4 |
| E02 RUSH_WAVE | 5 |
| E03 HEAVY_LINE | 5 |
| E04 SHIELD_SCREEN | 2 |
| E05 MIXED_WALL | 3 |
| E06 AIR_PRESSURE | 3 |
| E07 CHARGE_BREAK | 3 |
| E08 SPLIT_FLOOD | 6 |
| E09 SUPPORT_COLUMN | 4 |
| E10 SIEGE_LINE | 4 |
| E11 ESCORT_SIEGE | 4 |
| E12 BUFFED_BULWARK | 2 |
| E13 RUSH_BREACH | 5 |
| E14 AIR_RUSH | 2 |
| E15 REPLICATE_RUSH | 2 |
| E16 CASCADE | 3 |
| E17 BREACH_SCREEN | 2 |
| E18 DUAL_AXIS | 2 |
| E19 FORTRESS | 2 |
| E20 COLLAPSE_CHAIN | 0 |

### Interpretation
- 모든 archetype을 T1에 억지로 넣지 않은 점은 PASS.
- E20 C4를 T1에서 사용하지 않은 것은 적절.
- E08이 가장 자주 등장하는 이유는 SPLITTER teaching/reinforcement가 연속 배치되기 때문이며 재검토 대상.

---

# 2. Complexity distribution

63 occurrences 기준:

| Complexity | Count | Share |
|---|---:|---:|
| C0 | 4 | 6.3% |
| C1 | 18 | 28.6% |
| C2 | 26 | 41.3% |
| C3 | 13 | 20.6% |
| C4 | 2 | 3.2% |

전체 분포 자체는 T1 candidate로 수용 가능하다.
C0~C2가 `48/63 = 76.2%`로 중심이다.

### Late concentration watch
Stage 40~50에서는 C3/C4가 상대적으로 집중된다.
Final Examination이므로 증가 자체는 의도와 맞지만, T1이 갑자기 T4형 formation/siege Tier처럼 변하지 않는지 조정 필요.

---

# 3. Pressure-family Stage presence

중요:
`BASELINE`은 neutral flow/reference이므로 pressure family와 같은 방식으로 비교하지 않는다.
GRUNT filler prevalence는 별도 monster spawn share에서 측정해야 한다.

V0.1에서 해당 family가 최소 한 occurrence 존재하는 Stage 수:

| Family | Stage presence | 50 Stage share |
|---|---:|---:|
| BULWARK | 20 | 40% |
| RUSH | 14 | 28% |
| SIEGE | 12 | 24% |
| REPLICATE | 11 | 22% |
| BREACH | 10 | 20% |
| SUPPORT | 10 | 20% |
| AERIAL | 7 | 14% |
| FLOOD | 6 | 12% |

Neutral pure BASELINE archetype stage presence = 4 Stage.
이는 GRUNT가 다른 encounter의 filler로 사용되는 Stage를 포함하지 않으므로 “baseline monster frequency”가 8%라는 뜻이 아니다.

---

# 4. Finding F1 — SIEGE overrepresentation relative to T1 identity

`09_TIER_LADDER_CANDIDATE_V0_1.md`는 T1 SIEGE를 `LOW`로 두었다.
그러나 V0.1 skeleton은 SIEGE를 12/50 Stage에 사용한다.

더 큰 문제:
- Stage 26
- 27
- 28
- 29
- 30

에서 **5 Stage 연속** SIEGE family가 존재한다.

이는 T1의 “9종 vocabulary 학습”보다 SIEGE curriculum처럼 체감될 위험이 있다.
또 T4 `Formation / Objective Pressure` identity를 미리 소모한다.

Classification: `STRUCTURAL_MISMATCH`

Action:
- Stage29 SIEGE review 제거 후보
- Stage30 checkpoint에서 SIEGE를 필수 phase로 두지 않는 후보
- Final Examination에서도 SIEGE를 every-few-stage default로 만들지 않음

---

# 5. Finding F2 — BULWARK concentration

BULWARK Stage presence = 20/50 = 40%.

원인:
1. BRUTE/SHIELD teaching block Stage7~13
2. SIEGER protection archetype E11
3. SUPPORTER+BULWARK E12
4. BREACH screen E17
5. FORTRESS E19

BULWARK는 core target-order 학습에 중요하므로 높은 presence 자체가 defect는 아니다.
다만 T2가 Frontline/Breakthrough identity를 가져야 하므로 T1 후반이 durable-screen 문제로 과포화되면 Tier differentiation이 약해진다.

Classification: `WATCH`

Action:
- T1 Final Examination에서 일부 C3 screen Stage를 C1/C2 focused extreme으로 대체
- screen duration/intensity는 T2보다 명확히 낮게 calibration

---

# 6. Finding F3 — BASELINE metric semantics

T1 qualitative envelope에 `BASELINE HIGH`라고 쓰면 pressure-family presence와 혼동될 수 있다.

실제 의도:
- GRUNT/reference flow는 T1 전체에서 많이 사용 가능
- 그러나 BASELINE은 압박 family가 아니라 neutral filler/reference

Classification: `TERMINOLOGY_RISK`

Action:
- pressure family frequency와 `baselineFlowPrevalence`를 분리
- exact data schema에서 GRUNT spawn share/baseFlow를 별도 측정

---

# 7. Finding F4 — SPLITTER teaching repetition

V0.1:
- Stage20 E08
- Stage21 E08
- Stage22 E08

세 Stage 연속 REPLICATE+FLOOD.
Teaching reinforcement으로 설명 가능하지만, 신규 vocabulary 구간에서 동일 problem이 연속될 위험이 있다.

Classification: `MINOR_REPETITION_RISK`

Action:
- Stage22를 이전 vocabulary recall/geometry Stage로 대체 후보
- SPLITTER high-pressure는 Stage31에 유지

---

# 8. Finding F5 — Final Examination synergy density

V0.1 Stage40~50은 C3/C4가 많이 집중되어 있다.

문제 가능성:
- T1 후반이 갑자기 “복합 특수몹을 많이 넣는 것이 어려움”으로 변질
- T5의 contrast/focused-extreme 철학과도 불일치

Classification: `WATCH`

Action:
- Stage41을 C3 CASCADE 대신 C2 SPLIT_FLOOD extreme 후보
- Stage42의 E11 제거 후보
- Stage46 DUAL_AXIS 대신 focused SIEGE_LINE 후보
- Stage48 C1+C1 contrast는 유지
- C4 FORTRESS는 49/50 bounded only 유지

---

# 9. Findings that PASS

## P1 — Introduction order
Last first-teach Stage26. Stage40+ 신규 ordinary capability 없음.

## P2 — Learning before high synergy
C3 first appears only after individual special capability teaching has begun.
C4 first appears Stage49.

## P3 — Reward/design band consistency
- Stage19 fail -> 0★
- Stage20 fail -> 1★
- Stage39 fail -> 1★
- Stage40 fail -> 2★
- Stage50 clear -> 3★

## P4 — E20 omitted
COLLAPSE_CHAIN C4를 T1에 억지로 넣지 않음.

## P5 — No all-nine simultaneous mandate
Stage50은 sequence 방식이며 9종 simultaneous spawn을 목표로 하지 않음.

---

# 10. V0.2 revision requirements

V0.2는 최소 다음을 만족해야 한다.

1. SIEGE Stage26~30 5연속 제거
2. SPLITTER E08 Stage20~22 3연속 제거
3. Stage40~50 C3/C4 비중 완화
4. T1에서 T2/T4 identity를 과도하게 선점하지 않음
5. T1 전체 9종 teaching은 유지
6. Stage26 last first-teach 유지 가능
7. Stage40+ no-new-core-mechanic 유지
8. Stage48 focused-extreme contrast 유지
9. Stage49/50 FORTRESS는 bounded candidate로만 유지

---

# 11. Next

위 static finding을 반영한 `T1_STAGE_SKELETON_CANDIDATE_V0_2`를 작성하고 같은 정적 분포 검사를 반복한다.
V0.2가 structural PASS가 되기 전 exact monster count/cadence simulation으로 넘어가지 않는다.
