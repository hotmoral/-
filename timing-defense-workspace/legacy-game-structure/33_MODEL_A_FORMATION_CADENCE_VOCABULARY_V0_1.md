# Timing Defense — Model A Formation & Cadence Vocabulary V0.1

Date: 2026-10-22 KST  
Status: **BOUNDED AUTHORING VOCABULARY / NO TIMING NUMERIC FREEZE**

Depends on:
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- reusable vocabulary from parked `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

---

# 0. 목적

Tier가 올라갈수록 monster뿐 아니라 formation/cadence 언어도 확장되게 한다.
단, 높은 Tier = 모든 고급 formation/cadence 동시 사용으로 만들지 않는다.

기존 14 문서의 ID는 useful vocabulary로 재사용하되 old T1-all-9 recipe 수치는 계승하지 않는다.

---

# 1. Formation IDs

## F01 LINE_LIGHT
- 가벼운 직선 정렬
- penetration value 확인

## F02 LINE_DURABLE_FRONT
- durable unit이 앞을 잡는 line
- frontline dwell / screen

## F03 CLUSTER_LIGHT
- 밀집
- Mage/AoE opportunity

## F04 SCATTER_LIGHT
- 분산
- cluster specialist value 감소 / timing focus

## F05 AIR_OFFSET
- FLYER와 ground의 Y offset

## F06 SCREEN_BACKLINE
- durable/light screen 뒤 protected threat

## F07 ESCORT_COLUMN
- front screen -> protected objective/support unit

## F08 SPLIT_AXIS
- 공간/시간적으로 둘 이상 축

## F09 REPLICATION_CLUSTER
- SPLITTER parent/child density를 읽기 위한 cluster intent

중요:
formation은 target override가 아니다.
Runtime target authority는 actual X/validity.

---

# 2. Cadence IDs

## CD01 DRIP_SLOW
- teaching/recovery
- wide spacing

## CD02 DRIP
- standard sustained flow

## CD03 WAVE
- clear group boundaries

## CD04 BURST_LIGHT
- short-window tempo pressure

## CD05 STAGGER
- type/group timing offset
- target-order transition 유도

## CD06 ESCORT
- screen 먼저, protected unit 뒤

## CD07 LATE_INSERT
- encounter 후반에 key threat 삽입

## CD08 OVERLAP_BOUNDED
- previous encounter 생존 중 next encounter 진입
- explicit active-count guardrail 필요

Exact ms is not frozen.

---

# 3. T1 vocabulary

Allowed formation:
- F01 LINE_LIGHT
- F02 LINE_DURABLE_FRONT
- F03 CLUSTER_LIGHT
- F04 SCATTER_LIGHT
- F08 SPLIT_AXIS — late/limited candidate

Allowed cadence:
- CD01 DRIP_SLOW
- CD02 DRIP
- CD03 WAVE
- CD04 BURST_LIGHT — after basic timing established
- CD05 STAGGER — late/limited

Not default:
- F05/F06/F07/F09
- CD06/CD07/CD08

Purpose:
3 monsters만으로도 formation/cadence variety를 확보하면서 advanced backline grammar를 조기 소비하지 않는다.

---

# 4. T2 vocabulary

New formation:
- F05 AIR_OFFSET
- F08 SPLIT_AXIS usage expanded

Returning:
F01–F04.

Cadence:
- CD01–CD05
- CD07 LATE_INSERT limited candidate for geometry transition

Still avoid as standard:
- F06/F07/F09
- CD06 ESCORT
- CD08 OVERLAP_BOUNDED

Purpose:
mitigation/geometry를 읽게 하고 backline-objective grammar는 T4에 남긴다.

---

# 5. T3 vocabulary

New/expanded formation:
- F09 REPLICATION_CLUSTER
- F08 SPLIT_AXIS expanded
- F02 durable-front screen can protect CHARGER as advanced use

Cadence:
- CD01–CD05
- CD07 LATE_INSERT
- CD08 OVERLAP_BOUNDED — late bounded only

CD06 ESCORT는 아직 T4 signature로 보존하는 것을 기본값으로 한다.

Purpose:
- burst timing
- population rebound
- target reorder
- bounded overlap

Guardrail:
SPLITTER effective entity volume 때문에 CD08은 authored count만 보고 허용하지 않는다.

---

# 6. T4 vocabulary

All F01–F09 available.

Key new signature:
- F06 SCREEN_BACKLINE
- F07 ESCORT_COLUMN

All CD01–CD08 available.

Key new signature:
- CD06 ESCORT
- CD08 OVERLAP_BOUNDED expanded but still guarded

T4 teaching order:
- SUPPORTER teach: F03/F02 + CD01/02/03
- SIEGER teach: F01/F06 light + CD01/05
- mixed later: F06/F07 + CD06/07
- mastery: selected CD08 overlap

Do not first-teach SUPPORTER/SIEGER inside FORTRESS-like full escort overlap.

---

# 7. Anti-progression-collapse rule

A later Tier should not feel different only because monster roster changed.
Formation/cadence grammar도 단계적으로 확장한다.

But earlier vocabulary remains useful:
- T4 still uses simple LINE/DRIP focused extreme/recovery
- higher Tier does not retire readable simple patterns

---

# 8. Readability rules

- CD08 always requires peak-active simulation
- F06/F07 require measured backline exposure/screen uptime
- F09 requires effective child entity count
- F05 requires actual authoritative Y geometry
- F08 requires clear spatial/temporal separation, not visual clutter

---

# 9. Class opportunity

Formation/cadence rotation should produce:
- Knight: F01/F02/F06 line/reorder
- Rogue: F02 durable front
- Tank: CD05/CD07, breach/objective control
- Archer: F01/F06/F07 penetration
- Mage: F03/F09 density

No Tier should use only one geometry that permanently favors one class.

---

# 10. Status

This vocabulary is admitted for bounded recipe authoring.
Exact spacing/group size/overlap timing remains simulation candidate.
