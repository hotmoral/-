# Timing Defense — T1 Stage Skeleton Candidate V0.2

Date: 2026-10-22 KST  
Status: **STRUCTURAL CANDIDATE AFTER V0.1 STATIC AUDIT / NO PRODUCTION NUMBERS**

Supersedes as active candidate:
- `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`

Evidence:
- `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`

V0.1은 역사/비교용으로 보존한다.

---

# 1. V0.2 revision goals

V0.1에서 발견한 구조 문제를 수정한다.

1. Stage26~30 SIEGE 5연속 제거
2. SPLITTER E08 Stage20~22 3연속 제거
3. T1 Final Examination의 C3/C4 과집중 완화
4. T2/T4 identity를 T1이 과도하게 선점하지 않도록 함
5. 9종 ordinary teaching은 Stage26까지 완료 유지
6. Stage40+ 신규 core capability 없음 유지
7. focused-extreme Stage 유지

---

# 2. Monster introduction matrix

V0.1의 기본 introduction order는 유지한다.

| Monster | First teach | First mixed | First high-pressure candidate |
|---|---:|---:|---:|
| GRUNT | 1 | 4~5 | n/a |
| RUNNER | 4 | 5 | 19 |
| BRUTE | 7 | 8 | 34 |
| SHIELD | 11 | 12~13 | 34 |
| FLYER | 14 | 15 | 35 |
| CHARGER | 17 | 18~19 | 38 |
| SPLITTER | 20 | 21 | 31 |
| SUPPORTER | 23 | 24 | 32~34 |
| SIEGER | 26 | 27~28 | 33~36 |

Last first-teach = Stage26.

---

# 3. Stage 1~19

V0.1 유지.

| Stage | Encounter candidate | Complexity | Purpose |
|---:|---|---:|---|
| 1 | E01 BASELINE_MARCH | C0 | baseline |
| 2 | E01 cadence variant | C0 | baseline cadence |
| 3 | E01 formation variant | C0 | baseline formation |
| 4 | E02 RUSH_WAVE | C1 | RUNNER teach |
| 5 | E02 GRUNT+RUNNER | C1 | RUNNER mixed |
| 6 | E01 stagger variant | C0 | recovery |
| 7 | E03 HEAVY_LINE | C1 | BRUTE teach |
| 8 | E03 GRUNT+BRUTE | C1 | BRUTE mixed |
| 9 | E02 -> E03 | C1+C1 | tempo/durability contrast |
| 10 | E02 -> E03 | C1+C1 | checkpoint 1 |
| 11 | E04 SHIELD_SCREEN simple | C1 | SHIELD teach |
| 12 | E04 baseline followers | C1 | SHIELD mixed |
| 13 | E05 MIXED_WALL | C2 | BRUTE vs SHIELD |
| 14 | E06 AIR_PRESSURE | C1 | FLYER teach |
| 15 | E06 ground+air | C1 | FLYER mixed |
| 16 | E06 -> E05 | C1+C2 | geometry/frontline contrast |
| 17 | E07 CHARGE_BREAK | C1 | CHARGER teach |
| 18 | E07 + baseline | C1 | CHARGER mixed |
| 19 | E13 RUSH_BREACH low | C2 | sustained vs burst tempo |

---

# 4. Stage 20~29 — revised vocabulary completion

| Stage | Encounter candidate | Complexity | V0.2 intent |
|---:|---|---:|---|
| 20 | E08 SPLIT_FLOOD simple | C2 | SPLITTER teach |
| 21 | E08 baseline variant | C2 | SPLITTER mixed |
| 22 | **E06 AIR_PRESSURE recall** | C1 | SPLITTER 3연속 제거 / earlier geometry recall |
| 23 | E09 SUPPORT_COLUMN simple | C2 | SUPPORTER teach |
| 24 | E09 ordinary recipients | C2 | SUPPORTER mixed |
| 25 | E07 -> E08 separated | C1+C2 | burst -> population contrast |
| 26 | E10 SIEGE_LINE light | C2 | SIEGER teach |
| 27 | E10 light-frontline variant | C2 | SIEGER mixed |
| 28 | E11 ESCORT_SIEGE low | C3 | first durable-screen siege synergy |
| 29 | **E05 -> E14 separated** | C2+C2 | SIEGE 연속 제거 / wall+air-tempo recall |

Key change:
- SIEGE run ends at 26/27/28 instead of 26~30 five consecutive.
- Stage29 returns to previously learned vocabulary rather than repeating objective pressure.

---

# 5. Stage 30 — revised midpoint checkpoint

V0.2:

```text
Phase A: E13 RUSH_BREACH
Phase B: E08 SPLIT_FLOOD
Phase C: E09 SUPPORT_COLUMN
```

Complexity:
- C2 / C2 / C2
- time-separated by default

Purpose:
- tempo
- population
- support formation
을 검증.

V0.1의 E11 ESCORT_SIEGE를 제거해 SIEGE concentration을 낮춘다.
Stage30 fail reward는 여전히 1★.

---

# 6. Stage 31~39

| Stage | Encounter | Complexity | Purpose |
|---:|---|---:|---|
| 31 | E08 SPLIT_FLOOD high | C2 | SPLITTER high-pressure |
| 32 | E09 SUPPORT_COLUMN high | C2 | SUPPORTER high-pressure |
| 33 | E10 SIEGE_LINE high | C2 | SIEGER focused high-pressure |
| 34 | E12 BUFFED_BULWARK | C3 | support + durable formation |
| 35 | E14 AIR_RUSH | C2 | aerial tempo |
| 36 | E11 ESCORT_SIEGE | C3 | protected siege |
| 37 | E15 REPLICATE_RUSH | C2 | population + tempo |
| 38 | E17 BREACH_SCREEN | C3 | protected charge |
| 39 | E18 DUAL_AXIS | C3 | aerial + siege divided attention |

V0.2에서도 31~39는 C2/C3 synthesis band이며 C4는 없음.

---

# 7. Stage 40~49 — revised Final Examination

| Stage | Encounter | Complexity | Revision rationale |
|---:|---|---:|---|
| 40 | E05 -> E13 | C2+C2 | durable vs tempo contrast |
| 41 | **E08 SPLIT_FLOOD extreme** | C2 | V0.1 CASCADE C3 제거; focused population exam |
| 42 | **E14 AIR_RUSH high** | C2 | V0.1 E11 제거; aerial/tempo focused exam |
| 43 | E12 BUFFED_BULWARK | C3 | selected synergy |
| 44 | E15 REPLICATE_RUSH | C2 | readable dual pressure |
| 45 | E17 BREACH_SCREEN | C3 | selected protected burst |
| 46 | **E10 SIEGE_LINE focused extreme** | C2 | V0.1 DUAL_AXIS C3 제거; objective focused extreme |
| 47 | E16 CASCADE | C3 | selected population/support synergy |
| 48 | E02 extreme -> E03 extreme | C1+C1 | focused-extreme contrast |
| 49 | E19 FORTRESS bounded | C4 | only bounded pre-final C4 |

Structural intent:
- final band가 C3/C4 연속 도배가 되지 않음.
- Stage41/42/46은 complexity를 낮추고 intensity/clarity로 시험.
- Stage48의 단일 극단 contrast 유지.

---

# 8. Stage 50

V0.1의 3-phase sequence 유지:

```text
Phase 1: E13 RUSH_BREACH       C2
Phase 2: E16 CASCADE           C3
Phase 3: E19 FORTRESS bounded  C4
```

Rules:
- 기본안은 phase-separated.
- 3개 phase full overlap 금지.
- 9종 simultaneous requirement 없음.
- FLYER는 단순 roster-completion 목적으로 강제 추가하지 않음.

---

# 9. V0.2 static distribution

총 encounter occurrences: **61**.

## Archetype occurrences

| Archetype | Count |
|---|---:|
| E01 | 4 |
| E02 | 5 |
| E03 | 5 |
| E04 | 2 |
| E05 | 4 |
| E06 | 4 |
| E07 | 3 |
| E08 | 6 |
| E09 | 4 |
| E10 | 4 |
| E11 | 2 |
| E12 | 2 |
| E13 | 4 |
| E14 | 3 |
| E15 | 2 |
| E16 | 2 |
| E17 | 2 |
| E18 | 1 |
| E19 | 2 |
| E20 | 0 |

## Complexity

| Complexity | Count | Share |
|---|---:|---:|
| C0 | 4 | 6.6% |
| C1 | 19 | 31.1% |
| C2 | 27 | 44.3% |
| C3 | 9 | 14.8% |
| C4 | 2 | 3.3% |

`C0~C2 = 50/61 = 82.0%`.

V0.1:
- C0~C2 = 76.2%
- C3 = 20.6%

V0.2는 T1 readability 쪽으로 이동했다.

---

# 10. Pressure family Stage presence V0.2

BASELINE neutral flow는 pressure family 비교에서 제외한다.

| Family | Stage count | Share |
|---|---:|---:|
| BULWARK | 19 | 38% |
| RUSH | 14 | 28% |
| REPLICATE | 10 | 20% |
| BREACH | 9 | 18% |
| SUPPORT | 9 | 18% |
| SIEGE | 9 | 18% |
| AERIAL | 8 | 16% |
| FLOOD | 6 | 12% |

V0.1 SIEGE = 12 Stage (24%).
V0.2 SIEGE = 9 Stage (18%).

주의:
이 수치는 family가 Stage에 의미 있게 등장하는지 여부이지 monster spawn share가 아니다.

---

# 11. Consecutive-pressure audit

## SIEGE
V0.1: Stage26~30 5연속.

V0.2:
- 26/27/28 teaching cluster
- 33
- 36
- 39
- 46
- 49/50 final cluster

Teaching 목적 3연속과 final 목적 2연속을 제외하면 장기 연속 제거.

## REPLICATE
- 20/21 teaching pair
- 25
- 30/31 checkpoint->high pair
- 37
- 41
- 44
- 47
- 50

V0.1의 20/21/22 3연속 제거.

---

# 12. Cross-category consistency

## Meta/star
PASS.
Reward boundaries 변경 없음.

## Tier identity
PASS with WATCH.
T1은 vocabulary/readability 중심으로 유지.
BULWARK 38% presence는 여전히 상대적으로 높으므로 exact count/intensity에서 T2 identity를 침범하지 않는지 WATCH.

## Encounter taxonomy
PASS.
새 archetype을 임의 생성하지 않고 기존 E01~E20으로 표현.

## Complexity
PASS.
C4는 49/50 only.

## Target-order
PASS structurally.
SIEGE/SUPPORT synergy는 manual target을 가정하지 않음.

## Simulation readiness
STRUCTURAL PASS / NUMERIC NOT READY.
다음에는 count/cadence candidate가 필요.

---

# 13. Remaining WATCH items

1. BULWARK 19/50 Stage presence가 T1에서 실제 체감상 과한지
2. Stage20~26에 SPLITTER/SUPPORTER/SIEGER 3개 신규 capability가 여전히 7 Stage 안에 들어오는 인지부하
3. Stage49/50 FORTRESS C4가 T1에 필요한지
4. SIEGER focused Stage46의 wall-pressure cliff 가능성
5. permanent stat 없는 first-class path에서 Stage40+ survivability
6. Archer/Mage opportunity를 geometry data로 실제 보장할 수 있는지

이 항목은 exact candidate counts/cadence와 micro simulation에서 검증한다.

---

# 14. Next boundary

V0.2는 **T1 structural skeleton candidate로 채택하여 다음 simulation-authoring 단계로 이동 가능**.

다음은 production freeze가 아니라:
1. monster type authored count envelope
2. effective entity count envelope
3. cadence bucket 후보
4. formation IDs
5. 2-player baseline candidate
6. static density calculation
7. encounter micro simulation
순서다.

live code/numerical production patch는 아직 금지.
