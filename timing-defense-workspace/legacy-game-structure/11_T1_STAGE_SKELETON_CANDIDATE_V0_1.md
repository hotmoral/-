# Timing Defense — T1 Stage Skeleton Candidate V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL SIMULATION CANDIDATE / NO PRODUCTION COUNTS OR CADENCE VALUES**

## 0. 목적

T1 50 Stage를 실제 monster count/HP/cadence 숫자를 넣기 전에 **학습 순서, encounter 문제, 복잡도, 별 경계**만으로 배치해 구조적 모순을 찾는다.

이 문서는 production Stage schedule freeze가 아니다.

---

# 1. T1 core objective

T1의 본질:

> 9종 ordinary monster가 만드는 전투 언어를 플레이어가 frontmost system targeting 안에서 읽고, Stage 30 이후에는 새 mechanic tutorial 없이 이미 배운 vocabulary를 조합해서 대응하도록 만든다.

T1은 쉬운 Tier가 아니라 **기본 언어를 배우는 Tier**다.

---

# 2. Monster introduction matrix V0.1

| Monster | First teach | First mixed | First high-pressure candidate | Structural intent |
|---|---:|---:|---:|---|
| GRUNT | 1 | 4~5 | n/a | baseline/reference |
| RUNNER | 4 | 5 | 19 | sustained tempo |
| BRUTE | 7 | 8 | 34 | raw anchor |
| SHIELD | 11 | 12~13 | 34 | mitigation/screen |
| FLYER | 14 | 15 | 35 | Y geometry |
| CHARGER | 17 | 18~19 | 38 | telegraph/burst |
| SPLITTER | 20 | 21 | 31 | population transformation |
| SUPPORTER | 23 | 24 | 32~34 | formation speed support |
| SIEGER | 26 | 27~28 | 33~36 | ranged objective pressure |

Rules:
- first teach는 가능한 C1/낮은 C2.
- first mixed는 teach보다 뒤.
- high-pressure는 mechanic 인지 후 충분한 간격을 둔다.
- Stage 40 이후 first teach 없음.
- T1 candidate에서는 Stage 26에 마지막 신규 ordinary capability가 등장하고 Stage 29까지 vocabulary closure를 수행한다.

---

# 3. Stage 1~10 — Establish

| Stage | Design role | Encounter candidate | Complexity | Main purpose |
|---:|---|---|---:|---|
| 1 | baseline teach | E01 BASELINE_MARCH | C0 | 기본 전선/타게팅 읽기 |
| 2 | baseline cadence variation | E01 variant | C0 | spawn 간격 변화 인지 |
| 3 | baseline formation variation | E01 variant | C0 | 같은 GRUNT도 formation으로 다른 flow 가능 |
| 4 | RUNNER teach | E02 RUSH_WAVE | C1 | sustained speed 소개 |
| 5 | RUNNER mixed | E02 GRUNT+RUNNER variant | C1 | baseline 속 tempo 비교 |
| 6 | recovery/readability | E01 stagger variant | C0 | 신규 mechanic 간 인지 여백 |
| 7 | BRUTE teach | E03 HEAVY_LINE | C1 | raw durability/knock resist 소개 |
| 8 | BRUTE mixed | E03 GRUNT+BRUTE variant | C1 | 느린 heavy body와 filler 비교 |
| 9 | pre-checkpoint contrast | E02 then E03 | C1+C1 | 빠름 vs 무거움 전환 |
| 10 | checkpoint 1 | E02 -> E03 separated | C1+C1 | 첫 3종 이해 확인 |

### Audit
- 신규 capability 2개(RUNNER/BRUTE)를 충분히 분리해서 소개.
- Stage 9~10은 두 문제를 **동시 overlap**시키기보다 순차 contrast로 사용.
- 첫 checkpoint에서 복합 synergy를 요구하지 않음.

---

# 4. Stage 11~19 — Expand

| Stage | Design role | Encounter candidate | Complexity | Main purpose |
|---:|---|---|---:|---|
| 11 | SHIELD teach | E04 SHIELD_SCREEN simple | C1 | armor mitigation 소개 |
| 12 | SHIELD mixed | E04 + baseline followers | C1 | screen 의미 읽기 |
| 13 | BRUTE/SHIELD compare | E05 MIXED_WALL | C2 | raw HP vs mitigation 구분 |
| 14 | FLYER teach | E06 AIR_PRESSURE simple | C1 | Y geometry 소개 |
| 15 | FLYER mixed | E06 ground+air variant | C1 | line/AoE 관계 읽기 |
| 16 | geometry + wall contrast | E06 then E05 | C1+C2 | geometry/전열 문제 전환 |
| 17 | CHARGER teach | E07 CHARGE_BREAK simple | C1 | windup -> charge 소개 |
| 18 | CHARGER mixed | E07 + baseline | C1 | normal flow 속 telegraph 읽기 |
| 19 | first tempo combination | E13 RUSH_BREACH low | C2 | RUNNER 지속속도와 CHARGER burst 구분 |

### Audit
- SHIELD를 BRUTE와 동일한 “튼튼한 몹”으로 가르치지 않음.
- FLYER는 면역이 아니라 geometry 문제로 유지.
- CHARGER first teach에서 screen protection을 붙이지 않음.
- Stage 19는 0★ 구간 마지막 시험이지만 C2까지만 사용.

---

# 5. Stage 20~29 — Synthesis A / vocabulary completion

Stage 20부터 fail 시 1★이므로, 새로운 고급 vocabulary를 배우는 phase 진입 자체가 progression 의미를 가진다.

| Stage | Design role | Encounter candidate | Complexity | Main purpose |
|---:|---|---|---:|---|
| 20 | SPLITTER teach | E08 SPLIT_FLOOD simple | C2 | death -> children 소개 |
| 21 | SPLITTER mixed | E08 baseline variant | C2 | 처치 후 target reorder 읽기 |
| 22 | SPLITTER reinforcement | E08 cadence variant | C2 | authored vs effective entity 차이 체감 |
| 23 | SUPPORTER teach | E09 SUPPORT_COLUMN simple | C2 | aura가 formation tempo를 바꿈 |
| 24 | SUPPORTER mixed | E09 ordinary recipients | C2 | screened aura uptime 기초 |
| 25 | earlier-vocabulary synthesis | E07 -> E08 separated | C1+C2 | burst 후 population shift |
| 26 | SIEGER teach | E10 SIEGE_LINE light | C2 | standoff ranged wall pressure 소개 |
| 27 | SIEGER mixed | E10 light frontline variant | C2 | 전열 처리 지연과 shot timing |
| 28 | first protected siege | E11 ESCORT_SIEGE low | C3 | SHIELD/BRUTE screen이 SIEGER 보호 |
| 29 | vocabulary closure | E09 -> E10 -> E13 separated | C2/C2/C2 | 9종 전체 vocabulary 학습 종료 확인 |

### Audit
- SPLITTER/SUPPORTER/SIEGER를 한 Stage에서 연속 신규 소개하지 않음.
- SUPPORTER first teach는 durable special synergy가 아니라 ordinary recipient 위주.
- SIEGER first teach는 light screen만 사용.
- C3는 Stage 28에서 처음 제한적으로 사용.
- Stage 29까지 모든 9종 ordinary capability가 teaching됨.

---

# 6. Stage 30 — Mid checkpoint

Candidate:

```text
Phase A: E13 RUSH_BREACH low/medium
Phase B: E08 SPLIT_FLOOD medium
Phase C: E11 ESCORT_SIEGE low/medium
```

Rules:
- 세 phase는 기본적으로 시간 분리.
- C4 overlap 없음.
- 신규 capability 없음.
- reward상 Stage30 fail은 1★.

Purpose:
- tempo
- population shift
- screened objective
의 세 가지 큰 문제를 읽을 수 있는지 확인.

---

# 7. Stage 31~39 — Escalate

| Stage | Encounter candidate | Complexity | Escalation axis |
|---:|---|---:|---|
| 31 | E08 SPLIT_FLOOD | C2 | first high-pressure SPLITTER entity volume |
| 32 | E09 SUPPORT_COLUMN | C2 | first high-pressure aura uptime |
| 33 | E10 SIEGE_LINE | C2 | first high-pressure siege shot opportunity |
| 34 | E12 BUFFED_BULWARK | C3 | durable formation + support synergy |
| 35 | E14 AIR_RUSH | C2 | geometry + sustained tempo |
| 36 | E11 ESCORT_SIEGE | C3 | stronger screened firing uptime |
| 37 | E15 REPLICATE_RUSH | C2 | split-created reorder + speed |
| 38 | E17 BREACH_SCREEN | C3 | protected CHARGER trigger |
| 39 | E18 DUAL_AXIS | C3 | ground screen + FLYER + SIEGER divided attention |

### Audit
- Stage 31~33는 각각 하나의 late mechanic을 먼저 강하게 만든 뒤 synergy로 넘어감.
- C3가 증가하지만 C4는 없음.
- 39->40 boundary 직전 모든 high-level interaction이 최소 한 번 경험됨.

---

# 8. Stage 40~49 — Final Examination / 2★ zone

신규 ordinary capability first teach 금지.
이 구간은 이미 배운 문제를 더 엄격한 formation/cadence/intensity로 시험한다.

| Stage | Encounter candidate | Complexity | Exam focus |
|---:|---|---:|---|
| 40 | E05 -> E13 separated | C2 | durable front vs two-mode tempo |
| 41 | E16 CASCADE | C3 | SPLITTER + SUPPORTER synergy |
| 42 | E14 -> E11 | C2+C3 | air/tempo 후 screened siege 전환 |
| 43 | E12 BUFFED_BULWARK | C3 | support-driven screen compression |
| 44 | E15 REPLICATE_RUSH | C2 | population reorder under tempo |
| 45 | E17 BREACH_SCREEN | C3 | protected burst timing |
| 46 | E18 DUAL_AXIS | C3 | geometry + objective pressure |
| 47 | E16 CASCADE stronger variant | C3 | population + aura persistence |
| 48 | E02 extreme -> E03 extreme | C1+C1 | focused extremes / role switching |
| 49 | E19 FORTRESS low bounded form | C4 | first bounded multi-state mastery test |

### Why Stage48 is simple-complexity
Stage48은 높은 Tier/후반 Stage라도 복잡도 자체를 높이지 않고:
- 빠른 RUSH extreme
- 느린 HEAVY extreme
을 연속으로 제시한다.

“후반 = 무조건 복합 chaos” 퇴행을 막는 의도적 contrast Stage다.

### Stage49 C4 guardrail
- FORTRESS는 T1 최초 C4 candidate.
- production 값은 낮은/bounded form부터 simulation.
- SUPPORTER + SIEGER + screen을 최대 강도로 동시에 사용하지 않음.
- Stage49에서 screen duration/siege uptime이 과도하면 C4 자체를 제거/분리할 수 있음.

---

# 9. Stage 50 — T1 final / 3★ clear

목적:
T1 전체 vocabulary를 **한 번에 9종 동시 투입**하는 것이 아니라, 대표 문제를 순차적으로 종합한다.

V0.1 candidate sequence:

```text
Phase 1: E13 RUSH_BREACH
  sustained speed + burst telegraph

Phase 2: E16 CASCADE
  population transformation + formation support

Phase 3: E19 FORTRESS bounded
  frontline screen + support + siege objective
```

Optional geometry insert:
- FLYER는 Phase 간 또는 한 phase의 낮은-intensity geometry modifier로만 검토.
- FLYER를 넣는 이유가 단순히 “9종 모두 넣기 위해서”라면 넣지 않는다.

Rules:
- phase 사이 readability 확보.
- 기본안은 3 phase full-overlap 금지.
- final difficulty는 HP sponge가 아니라 learned-problem execution으로 만든다.

---

# 10. Static consistency audit V0.1

## PASS — introduction ordering
- 9종 last first-teach = Stage26 SIEGER.
- Stage40+ first ordinary capability 없음.

## PASS — learning before synergy
- CHARGER C1 teach -> E13/E17 later.
- SPLITTER simple -> E15/E16 later.
- SUPPORTER simple -> E12/E16/E19 later.
- SIEGER light -> E11/E18/E19 later.

## PASS — complexity ramp
- C4 first candidate = Stage49.
- C3 first limited use = Stage28.
- early bands C0~C2 중심.

## PASS — star boundary semantics
- Stage19: 0★ final pre-boundary test.
- Stage20: 1★ band entry + SPLITTER teaching begins.
- Stage39: 1★ final pre-2★ test.
- Stage40: 2★ final-exam band entry; no new core capability.
- Stage50 clear: 3★.

## WATCH — Stage20~29 cognitive load
세 신규 capability(SPLITTER/SUPPORTER/SIEGER)가 10 Stage 안에 소개됨.
50 Stage 전체 기준으로는 여유가 있으나 device readability test와 learning-profile simulation 필요.

## WATCH — T1 C4 necessity
E19 at 49/50가 T1의 vocabulary exam에 실제 필요한지 simulation에서 검토.
C4가 단지 “마지막이니까 복잡해야 한다”는 이유만 남는다면 제거한다.

## WATCH — SIEGER objective pressure
T1 permanent/run progression이 낮을 때 screened SIEGER가 wall damage cliff를 만들 수 있음.
shot count/uptime을 반드시 측정.

---

# 11. Class-opportunity coverage — structural check

T1 전체에서 각 class의 soft-advantage window가 존재해야 한다.

- Knight: mixed/transition/reorder — Stage16/25/29/30/40+ 등
- Rogue: BRUTE/SHIELD durable bodies — Stage7~13, 34, 43 등
- Tank: CHARGER interrupt / wall control — Stage17+, SIEGER 26+ 등
- Archer: line/screen penetration opportunity — SHIELD/SIEGER formations, line variants
- Mage: cluster/density/SPLITTER children — Stage20+, Cascade 등

정확한 opportunity percentage는 stage geometry/count data가 들어간 후 계산한다.

---

# 12. What is intentionally absent

아직 없음:
- exact monster count
- exact monster HP/speed
- exact spawn gap ms
- Stage duration
- exact overlap seconds
- boss placement
- shop cadence
- Stage reward/coin values
- exact XP curve

이 값을 지금 채우면 구조 문제와 수치 문제를 분리할 수 없으므로 다음 tranche에서 candidate dataset으로 작성한다.

---

# 13. Next tranche

1. 이 50-stage skeleton에서 archetype occurrence count 계산
2. pressure-family occurrence/meaningful-presence 계산
3. monster type stage presence 목표 계산
4. T1 exact candidate spawn-count/cadence envelope 작성
5. 2P baseline candidate부터 micro/Stage simulation
6. 3P/4P scaling 확장
7. fail histogram / 1★·2★·3★ distribution 확인
8. T1 structural revisions

production code는 아직 변경하지 않는다.
