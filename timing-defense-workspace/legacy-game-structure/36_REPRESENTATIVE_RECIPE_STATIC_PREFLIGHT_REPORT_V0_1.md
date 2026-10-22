# Timing Defense — Representative Recipe Static Preflight Report V0.1

Date: 2026-10-22 KST  
Status: **STATIC PREFLIGHT PASS / REPRESENTATIVE RECIPES ONLY**

Inputs:
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_encounter_envelope_v0_1.yaml`
- `tools/analyze_representative_recipes.py`

---

# 0. 목적

Model A lower-layer simulation 전에 대표 encounter recipe들이:
- Tier legal archetype/formation/cadence를 지키는지
- authored spawn density가 과도하지 않은지
- SPLITTER 즉시 child stress를 넣어도 effective entity burst가 초기 guardrail 안인지
정적으로 확인한다.

---

# 1. Representative set

총 20 recipes.

## T1 — 3
- E01 baseline
- E02 rush
- E03 heavy

## T2 — 4
- E04 shield
- E05 mixed wall
- E06 air
- E14 air-rush high

## T3 — 6
- E07 charger
- E08 splitter
- E13 rush-breach high
- E15 replicate-rush
- E17 breach-screen
- E20 collapse-chain low stress

## T4 — 7
- E09 support
- E10 siege
- E11 escort-siege
- E12 buffed-bulwark
- E16 cascade
- E18 dual-axis
- E19 fortress bounded

---

# 2. Vocabulary consistency catch

Initial recipe draft에서:
```text
T3_E17_M -> CD06 ESCORT
```
가 사용되었다.

하지만 current vocabulary는 CD06 ESCORT를 T4 signature로 보존한다.
따라서 static validation 전에:
```text
T3_E17_M: CD06 -> CD07 LATE_INSERT
```
로 수정했다.

이 변경은 T4 cadence novelty를 T3가 선소비하지 않게 한다.

---

# 3. Static density guardrails

Candidate analysis alerts:
- authored 4s normal <=8
- authored 4s WATCH 9–10
- effective 4s normal <=10
- effective 4s WATCH 11–13

SPLITTER stress rule:
- parent spawn 1개
- 즉시 사망한다고 가정
- 같은 timestamp에 2 child 생성

즉 실제 kill timing보다 더 보수적으로 entity creation을 압축한다.

---

# 4. Tier summary

| Tier | Recipes | Max authored 4s | Max authored 6s | Max effective 4s | Max effective 6s | Max effective package |
|---|---:|---:|---:|---:|---:|---:|
| T1 | 3 | 6 | 7 | 6 | 7 | 7 |
| T2 | 4 | 7 | 7 | 7 | 7 | 7 |
| T3 | 6 | 6 | 6 | 9 | 9 | 9 |
| T4 | 7 | 6 | 6 | 10 | 10 | 10 |

Result:
- authored 4s WATCH 없음
- effective 4s WATCH 없음
- over-watch 없음

---

# 5. SPLITTER-sensitive recipes

| Recipe | Authored | Conservative effective max | Effective 4s |
|---|---:|---:|---:|
| T3_E08_M | 5 | 9 | 9 |
| T3_E15_M | 5 | 9 | 9 |
| T3_E20_L | 4 | 6 | 6 |
| T4_E16_M | 6 | 10 | 10 |

T4 E16 reaches the current normal upper edge exactly but does not enter WATCH.

Interpretation:
- suitable for micro-sim
- not evidence that H/X CASCADE is safe
- higher SPLITTER intensities remain blocked until child-timing/kill simulation

---

# 6. Per-recipe highlights

- T2 E14_H authored 4s = 7: high tempo but still below initial density warning.
- T3 E13_H authored 4s = 6: CHARGER danger comes from state timing, not raw count.
- T4 E19_M authored/effective = 5: FORTRESS complexity comes from protection/uptime, not entity spam.
- T4 E16_M effective = 10: population transformation remains the main static volume watch.

---

# 7. What this PASS does not prove

Static density PASS does not prove:
- readable telegraphs in real combat
- clear-rate correctness
- screen duration correctness
- SUPPORTER aura balance
- SIEGER shot balance
- actual SPLITTER child timing under player damage
- class fairness

These move to kinematic and combat micro simulation.

---

# 8. Verdict

**REPRESENTATIVE RECIPE STATIC PREFLIGHT = PASS**

Current representative recipes may proceed to movement/geometry preflight and then Layer-A combat micro-simulation.
