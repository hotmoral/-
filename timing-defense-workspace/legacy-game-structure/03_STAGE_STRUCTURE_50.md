# Timing Defense — 50 Stage Structure V0.2

Date: 2026-10-22 KST  
Status: **STRUCTURAL FOUNDATION / MODEL-A ALIGNED / EXACT STAGE DATA OPEN**

## 1. 기본 구조

한 Tier는 50개의 Stage로 구성한다.
Stage는 단순 HP/count 증가가 아니라:

```text
establish/teach
 -> mix
 -> deepen
 -> pressure/soft wall
 -> Lv31 ascension
 -> post-Lv31 mastery
 -> final
```

으로 전개한다.

중요:
**Stage design band와 star reward band는 서로 다른 분류다.**

---

# 2. Star reward band — USER_CONFIRMED

Attempt outcome:
- Stage1–19 실패: 0★
- Stage20–39 실패: 1★
- Stage40–49 실패: 2★
- Stage50 clear: 3★

```text
if tierCleared(Stage50): 3
else if failedStage >= 40: 2
else if failedStage >= 20: 1
else: 0
```

20 / 40 / 50은 reward anchors다.

---

# 3. Current common macro grammar

Model A bounded simulation에서 사용할 공통 뼈대:

## Stage1–9 — Establish / first teaching
- returning baseline 또는 Tier 첫 신규 mechanic 소개
- 한 번에 여러 major mechanic 겹침 억제
- low/moderate complexity

## Stage10 — Checkpoint A
- 1–9 read check
- boss optional
- unpreviewed boss novelty 금지에 가까운 기본값

## Stage11–19 — Introduce & Mix
- 신규 monster/mechanic second teaching window 가능
- first mixed use
- Stage20 1★ boundary 준비

## Stage20 — Star Gate A
- 1★ zone entry
- 첫 meaningful Tier synthesis

## Stage21–29 — Deepen
- first high-pressure windows
- returning + new monster 조합
- Lv21 power window와 attribution collision 관리

## Stage30 — Checkpoint B / optional Boss Preview
- mid synthesis
- Stage50 boss가 mandatory unique decision grammar를 가진다면 여기서 낮은 강도로 preview 가능
- boss preview는 optional

## Stage31–39 — Pressure / Soft-Wall Build
- class asymmetry가 본격적으로 드러남
- formation/cadence pressure 강화
- Lv26 Stage32–36 candidate
- ordinary soft wall의 기본 형성 구간

## Stage40 — Star Gate B
- 2★ zone entry
- late mastery transition

## Stage41–45 — Lv31 Ascension Window — USER-CONFIRMED DIRECTION
- Lv31 target unlock Stage41–45
- 새 core ordinary capability first-teach 금지
- unpreviewed mandatory boss mechanic 금지
- 모든 Stage를 peak complexity로 만들지 않음
- known mechanics를 moderate/high pressure에서 사용하며 Lv31 first-use runway 제공

## Stage46–49 — Post-Lv31 Mastery
- Lv31 반복 사용/숙련
- class opportunity rotation
- high difficulty 가능
- C4는 bounded하게 사용 가능
- hard class lockout 금지

## Stage50 — Tier Final / 3★
- Lv31 tutorial 아님
- already-familiar full kit 종합 시험
- boss candidate
- core ordinary mechanic first introduction 금지
- mandatory boss-only grammar가 있다면 earlier preview 필요

---

# 4. Monster introduction policy

현재 active direction은 **T1에서 9종 전부를 teaching하지 않는다.**

Model A bounded spine:
```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future expansion
```

각 new monster lifecycle:
```text
firstTeach
 -> firstMixed
 -> firstHighPressure
 -> later-Tier reinterpretation
```

Current range candidates는:
`28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`를 따른다.

---

# 5. Player power overlay

First calibration candidate:
- Lv6: Stage5–7
- Lv11: 11–14
- Lv16: 18–21
- Lv21: 25–28
- Lv26: 32–36
- Lv31: **41–45**

Only Lv31 window is user-confirmed.
Others remain simulation candidates.

Important distinction:
- class T1에서는 skill unlock이 pedagogic novelty일 수 있음
- same-class T2+에서는 familiar run-local power spike인 경우가 많음

따라서 `skill learning collision`과 `power attribution collision`을 분리한다.

---

# 6. Stage lifecycle / inter-stage flow

Strong legacy reference:
```text
Stage intro
 -> combat
 -> stage clear
 -> inter-stage progression/shop
 -> next stage
```

Stage intro 동안 현재 canonical behavior reference:
- movement/spawn 없음
- AI/passive 없음
- Timing input 없음

### Shop cadence remains OPEN
Legacy every-stage shop을 50 Stage에 자동 복제하지 않는다.
Candidate later comparison:
- every-stage
- checkpoint
- selected-stage
- optional/fast continue

Gate G3에서 별도 검토.

---

# 7. Stage authoring fields

```text
stageNumber
designBand
rewardBand
expectedDuration
baseFlow
encounters[]
monsterTypeCounts{}
monsterSpawnShare{}
activeConcurrencyPolicy
spawnCadence
formationProfile
geometryProfile
overlapPolicy
checkpointType
bossPolicy
teamScaling
rewardProfile
shopPolicy
expectedSkillWindow
```

Design/reward band를 분리 저장한다.

---

# 8. Encounter event fields

```text
EncounterEvent
  timeWindow
  archetypeId
  composition
  formation
  spawnOrder
  cadence
  geometry
  intensity
  overlapWith
```

전열 자동 타게팅 때문에 composition만으로는 부족하다.
FRONT/MID/BACK은 authoring intent이며 runtime target authority를 덮지 않는다.

---

# 9. Required metrics

## Entity/readability
- authored spawn count
- effective entity count
- peak active
- max 4s/6s density

## Target order
- frontline block time
- target reorder count
- backline exposure
- SUPPORTER screened aura uptime
- SIEGER screened firing uptime
- CHARGER windup/interrupt opportunities
- SPLITTER child frontline occupancy
- FLYER geometry opportunity

## Power progression
- EXP
- level distribution
- skill unlock distribution P25/P50/P75/P90
- post-unlock meaningful Stage/event count
- pre/post skill clear-rate slope

---

# 10. Difficulty / soft wall

General non-T1 user target:
```text
intended-entry SKILLED_V2_CENTRAL full-Tier clear <60%
```

But desired difficulty를 대부분 Stage1–19 failure로 만들지 않는다.

Preferred ordinary soft-wall shape:
- Stage31+에서 pressure 증가
- 1★/2★를 확보할 수 있는 진행 경로 유지
- 다른 class progression 후 재도전 가치 제공

Fail histogram을 반드시 본다.

---

# 11. Anti-repetition

- identical encounter signature 연속 반복 억제
- formation/cadence/geometry variation
- special monster every Stage 강제 금지
- higher Tier constant C3/C4 chaos 금지
- recovery/focused challenge 유지

---

# 12. Boss placeholder

Current structural candidate:
- Stage10 checkpoint / boss optional
- Stage30 optional boss-signature preview
- Stage50 boss candidate

Final boss의 mandatory unique decision grammar는 Stage50에서 처음 공개하지 않는다.

---

# 13. Current exact downstream

Master Campaign Layer-0 has passed.

Next:
- Tier-specific encounter archetype availability
- formation/cadence availability
- pressure/complexity bounded frequency ranges
- representative deterministic recipes
- micro simulation

Do not yet author exact 200 launch Stages or freeze production numbers.
