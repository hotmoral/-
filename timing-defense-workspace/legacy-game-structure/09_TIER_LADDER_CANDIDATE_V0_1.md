# Timing Defense — Tier Ladder Candidate V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL CANDIDATE / NOT FINAL TIER COUNT OR PRODUCTION BALANCE**

## 0. 목적

최종 Tier 수와 production 수치를 바로 고정하지 않고, 9종 ordinary monster와 50 Stage 구조가 실제 campaign ladder로 연결될 수 있는지 검증하기 위한 첫 structural candidate다.

이 문서는 기존 `T1 Foundations / T2 Breakers / T3 Rushline / T4 Crossfire / T5 Extremes`를 복원하지 않는다.
기존 5-tier 분석은 참고만 하며, 신규 taxonomy와 직업별 독립 progression을 기준으로 재작성한다.

---

# 1. 왜 Tier 수 자체가 메타 밸런스 문제인가

직업은 5개이고 각 Tier는 50 Stage이므로, Tier 수를 `T`라 하면 모든 직업이 각 Tier를 한 번씩 3★ clear하는 최소 성공 Stage volume은:

```text
5 classes × T tiers × 50 stages = 250T successful stage clears
```

예:
- 4 Tier -> 1000 Stage
- 5 Tier -> 1250 Stage
- 6 Tier -> 1500 Stage

실제 플레이는 실패/재도전이 추가되므로 더 길다.

최대 별 수도:

```text
MaxStars = 5 classes × T tiers × 3 = 15T
```

예:
- 4 Tier -> 60★
- 5 Tier -> 75★
- 6 Tier -> 90★

따라서 Tier 수는 단순 콘텐츠 개수가 아니라:
- 총 campaign 길이
- permanent reward ladder 길이
- 직업별 반복 부담
- class replayability
- late-game skill reach
- 최종 난이도 폭
을 동시에 결정한다.

최종 Tier 수는 이 변수들을 함께 계산한 뒤 freeze한다.

---

# 2. 첫 calibration spine — 5 Tier candidate

첫 full-campaign simulation에서는 **5 Tier**를 candidate spine으로 사용한다.

중요:
- final game이 반드시 5 Tier라는 뜻이 아니다.
- 기존 legacy T1~T5를 승인한다는 뜻이 아니다.
- 5 Tier는 `75★ max / 1250 minimum successful class-stage completions`라는 충분히 큰 campaign을 검증하기 위한 첫 bounded candidate다.
- simulation 결과가 지나치게 길거나 짧으면 4/6 Tier alternative를 비교한다.

---

# 3. Tier ladder의 핵심 원칙

## 3.1 Tier 1에서 ordinary vocabulary를 완성

9종 ordinary monster를 여러 Tier에 걸쳐 한 종씩 늦게 unlock하는 방식은 현재 구조에서 기본안으로 사용하지 않는다.

이유:
1. 한 Tier가 이미 50 Stage라 충분한 학습 공간이 있다.
2. 직업별 독립 진행 때문에 각 직업이 다시 T1부터 진행한다.
3. SIEGER/SUPPORTER 같은 핵심 capability가 너무 늦은 Tier에서 처음 나오면 앞 Tier가 지나치게 단순해진다.
4. 높은 Tier는 “새 몬스터를 처음 보는 곳”보다 이미 배운 vocabulary의 새로운 조합/tempo/formation을 시험하는 곳이어야 한다.

따라서 첫 candidate에서는 **T1 Stage 1~29 안에 9종 ordinary capability를 모두 최소 한 번 teaching**하고, Stage 30 이후는 결합/응용으로 전환한다.

## 3.2 Stage 40 이후 신규 핵심 capability 최초 도입 금지

40~49는 2★ Final Examination band다.
여기서 처음 본 mechanic 때문에 실패하게 만들지 않는다.

## 3.3 Higher Tier != constant chaos

높은 Tier에서도:
- 단일 압박 extreme
- recovery/readability stage
- 두 압박의 선명한 조합
이 필요하다.

모든 Stage를 3~4 special state overlap으로 만들지 않는다.

## 3.4 Tier identity는 `무엇을 더 많이 쓰는가 + 어떻게 배치하는가 + 언제 압박하는가`로 정의

단순 HP multiplier로 Tier를 구분하지 않는다.

---

# 4. T1 — Vocabulary / Field Reading

## 핵심 질문
“각 monster가 무엇을 하는지 읽고, frontmost target order 속에서 기본 대응을 할 수 있는가?”

## 주 역할
- 모든 9종 capability의 introduction
- BASELINE / RUSH / BULWARK / AERIAL / BREACH / REPLICATE / SUPPORT / SIEGE vocabulary 습득
- 낮은 overlap
- 단일/2-role encounter 중심

## T1 introduction candidate

### Stage 1~9 — 기본 전선
- GRUNT
- RUNNER
- BRUTE

목표:
- baseline
- sustained speed
- raw durability / knock resistance

### Stage 11~19 — mitigation / geometry / burst
- SHIELD
- FLYER
- CHARGER

목표:
- damage mitigation과 raw HP 차이 인지
- Y geometry
- windup -> charge interrupt window

### Stage 20~29 — population / formation / objective
- SPLITTER
- SUPPORTER
- SIEGER

목표:
- kill -> children
- screened support uptime
- ranged wall pressure

Stage 29까지 9종 ordinary vocabulary가 최소 teaching 완료되는 것을 기본 guardrail로 한다.

### Stage 30~39 — first synthesis
- 2-role combinations
- target reorder
- frontline/backline screening
- low/moderate overlap

### Stage 40~49 — T1 final exam
- 이미 배운 mechanic만 사용
- formation/cadence를 더 엄격하게 조합
- 신규 ordinary capability 최초 도입 없음

### Stage 50
- T1 vocabulary 종합 시험
- 모든 9종을 동시에 넣는 것은 필수 아님
- 2~3개의 명확한 encounter sequence로 주요 학습을 검증하는 방향 우선

## T1 pressure tendency
- BASELINE: high
- RUSH: medium
- BULWARK: medium
- AERIAL: low-medium
- BREACH: low
- REPLICATE: low
- SUPPORT: low
- SIEGE: low

후반으로 갈수록 special family가 증가하되, T1 전체는 readability 우선.

---

# 5. T2 — Frontline / Breakthrough

## 핵심 질문
“전열이 오래 버티거나 순간적으로 무너질 때 처리 순서와 control을 유지할 수 있는가?”

## Primary families
- BULWARK
- BREACH

## Secondary
- RUSH
- SIEGE

## 대표 archetype
- HEAVY_LINE
- SHIELD_SCREEN
- MIXED_WALL
- CHARGE_BREAK
- BREACH_SCREEN
- ESCORT_SIEGE

## 구조적 특징
- BRUTE/SHIELD screen duration 증가
- CHARGER가 보호받거나 staggered timing으로 등장
- SIEGER는 아직 주인공이 아니라 frontline failure consequence로 사용
- raw durability와 armor mitigation을 섞되 같은 문제로 뭉개지 않음

## 피해야 할 퇴행
- 모든 적 HP blanket inflation
- Rogue가 없으면 못 깨는 durability lock
- Tank가 없으면 CHARGER를 막을 수 없는 hard interrupt requirement

---

# 6. T3 — Tempo / Population Shift

## 핵심 질문
“전장이 빠르게 재구성될 때 target order와 처리량을 유지할 수 있는가?”

## Primary families
- RUSH
- REPLICATE

## Secondary
- AERIAL
- BREACH

## 대표 archetype
- RUSH_WAVE
- SPLIT_FLOOD
- RUSH_BREACH
- AIR_RUSH
- REPLICATE_RUSH
- COLLAPSE_CHAIN (제한적)

## 구조적 특징
- RUNNER의 지속 tempo
- SPLITTER death 이후 entity volume 변화
- CHARGER burst와 sustained speed를 구분해 읽어야 함
- FLYER geometry로 straight-line/cluster value를 교란

## 핵심 guardrail
SPLITTER actual entity volume 때문에 authored spawn count만으로 difficulty를 판단하지 않는다.
peak active / 4s / 6s density를 별도 제한한다.

---

# 7. T4 — Formation / Objective Pressure

## 핵심 질문
“자동 전열 타게팅 제약 속에서 보호받는 위협을 통제하고 성벽 압박을 견딜 수 있는가?”

## Primary families
- SUPPORT
- SIEGE
- BULWARK

## Secondary
- AERIAL
- BREACH

## 대표 archetype
- SUPPORT_COLUMN
- SIEGE_LINE
- ESCORT_SIEGE
- BUFFED_BULWARK
- DUAL_AXIS
- FORTRESS (후반 제한)

## 구조적 특징
- backline exposure time 중요
- SUPPORTER screened aura uptime 중요
- SIEGER screened firing uptime 중요
- SHIELD/BRUTE의 존재 자체보다 “얼마나 오래 뒤를 가리느냐”가 난이도 핵심

## 클래스 역할
- Archer penetration opportunity
- Mage cluster opportunity
- Tank knock/reposition value
- Rogue durable frontline value
- Knight mixed/reorder generalist value

어느 한 class도 필수는 아니다.

---

# 8. T5 — Mastery / Contrast

## 핵심 질문
“모든 vocabulary를 알고 있는 상태에서 서로 다른 극단을 빠르게 전환하며 대응할 수 있는가?”

## Primary identity
특정 family 하나가 아니라 **contrast / role switching / focused extremes**.

예:
- 한 Stage는 빠른 RUSH extreme
- 다음은 느리지만 강한 BULWARK/SIEGE
- 다음은 REPLICATE/AERIAL geometry
- 일부 Stage만 high-complexity FORTRESS/COLLAPSE_CHAIN

## 구조적 특징
- 복합 chaos 비율은 높아질 수 있지만 전부 chaos는 아님
- 단일 pressure extreme도 late-game mastery test로 적극 사용
- timing-window shift와 cadence compression으로 같은 조합도 다른 문제로 제시
- final band는 앞선 Tier의 모든 vocabulary를 활용 가능

## 피해야 할 패턴
- “T5니까 모든 Stage에 SUPPORTER+SIEGER+CHARGER+SPLITTER”
- 극단적 HP sponge
- 화면 entity saturation으로 난이도를 대신함

---

# 9. Tier 간 monster 사용 원칙

T1 이후 ordinary monster는 unlock 여부가 아니라 **역할 빈도/조합 방식**으로 Tier identity를 만든다.

예:
- RUNNER는 T1에서도 등장하지만 T3에서 높은 tempo budget을 가짐.
- SHIELD는 T1에서 teaching되지만 T2/T4에서 screen role이 강화됨.
- SPLITTER는 T1에서 단순 teaching되지만 T3에서 population-shift 주역.
- SUPPORTER는 T1에서 단순 formation으로 teaching되지만 T4에서 screened uptime이 핵심.
- SIEGER는 T1에서 단순 wall-pressure teaching, T4에서 protected objective pressure 주역.

이 방식은 “새 monster를 계속 추가해야만 다음 Tier가 새로워지는 구조”를 피한다.

---

# 10. Candidate frequency envelope — qualitative V0.1

정확한 %는 아직 넣지 않는다.
먼저 `LOW / MEDIUM / HIGH / PEAK` envelope로 설계하고 다음 tranche에서 exact candidate count로 변환한다.

| Family | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|
| BASELINE | HIGH | MEDIUM | MEDIUM | LOW-MED | MEDIUM |
| FLOOD | LOW-MED | LOW | HIGH | LOW-MED | MEDIUM |
| RUSH | MEDIUM | MEDIUM | PEAK | LOW-MED | HIGH/variable |
| BULWARK | MEDIUM | PEAK | LOW-MED | HIGH | HIGH/variable |
| BREACH | LOW | HIGH | HIGH | MEDIUM | HIGH/variable |
| AERIAL | LOW-MED | LOW-MED | HIGH | MEDIUM | HIGH/variable |
| REPLICATE | LOW | LOW-MED | PEAK | MEDIUM | HIGH/variable |
| SUPPORT | LOW | LOW-MED | MEDIUM | PEAK | HIGH/variable |
| SIEGE | LOW | MEDIUM | LOW-MED | PEAK | HIGH/variable |

이 표는 production frequency가 아니라 exact dataset 작성 전에 방향 충돌을 검출하기 위한 structural envelope다.

---

# 11. Complexity ladder

Encounter complexity를 monster 종류 수로만 정의하지 않는다.

## C0 — Baseline
- ordinary flow
- no stateful interaction

## C1 — Single mechanic
- 한 pressure mechanic

## C2 — Dual readable
- 두 mechanic이 명확히 분리/결합

## C3 — Synergy
- 하나가 다른 하나의 약점을 보완하거나 screen함

## C4 — Multi-state high complexity
- 세 개 이상 stateful capability가 상호작용

Candidate target:
- T1: C0~C2 중심, C3 소량 late
- T2: C1~C3 중심
- T3: C1~C3 중심, C4 소량 late
- T4: C2~C3 중심, C4 제한적으로 증가
- T5: C1~C4 전체 사용; C4를 기본값으로 만들지 않음

---

# 12. Tier identity validation

각 Tier candidate는 다음 질문을 통과해야 한다.

1. HP/count 수치를 가리고도 어느 Tier인지 설명 가능한가?
2. 주력 pressure family가 실제 encounter archetype에 반영되는가?
3. 주력 family 때문에 특정 class가 필수가 되지 않는가?
4. 50 Stage 안에서 teaching -> synthesis -> exam이 성립하는가?
5. Stage 40 이후 처음 보는 core mechanic이 없는가?
6. 앞 Tier와 monster roster가 같아도 formation/cadence/pressure가 충분히 다른가?
7. higher Tier가 단순히 더 복잡한 것만 의미하지 않는가?
8. 별/permanent progression을 고려해도 first-class path가 성립하는가?

---

# 13. T1 introduction audit — 중요 구조 검토

T1에 9종을 모두 소개하면 인지부하 우려가 있다.
그러나 50 Stage 전체를 이용하면 한 번에 9종을 소개하는 것이 아니다.

Candidate pacing:
- first 9: 3종
- next 9: 3종
- next 10: 3종
- remaining 21: 조합/반복/시험

즉 신규 mechanic introduction보다 실제 응용 Stage가 더 많다.

반대로 여러 Tier에 걸쳐 monster를 잠그면:
- 각 class의 T1 replay가 지나치게 단순
- late Tier가 mechanic tutorial과 mastery exam을 동시에 수행
- final Tier 수 변경 시 monster unlock schedule도 연쇄 재작성
이라는 구조적 비용이 생긴다.

현재 V0.1은 T1 vocabulary-complete 쪽을 우선 candidate로 둔다.

---

# 14. Open decisions intentionally not closed here

- final Tier count: 4/5/6+ 중 무엇인지
- final Tier display names
- exact monster spawn share
- exact encounter frequency
- exact counts/cadence
- boss cadence
- Tier unlock rule
- shop frequency
- permanent stat reward ladder
- final EXP/skill reach

이 항목은 후속 simulation/decision gate에서 닫는다.

---

# 15. Next tranche

이 candidate가 구조적으로 유지된다면 다음은:

1. T1 `firstTeach / firstMixed / firstHighPressure` stage candidate 작성
2. 20 encounter archetype의 C0~C4 complexity tagging
3. T1~T5 qualitative envelope를 exact **candidate counts**로 변환
4. 각 Tier 50-stage signature skeleton 생성
5. monster spawn share와 meaningful threat presence 계산
6. 동일 signature 반복/role starvation 정적 검사
7. micro simulation -> 10-stage synthetic slice -> 50-stage T1 simulation

그 전에는 production monster coefficient나 live campaign code를 변경하지 않는다.
