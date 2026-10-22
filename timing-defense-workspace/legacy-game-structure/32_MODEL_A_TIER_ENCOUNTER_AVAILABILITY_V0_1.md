# Timing Defense — Model A Tier Encounter Availability V0.1

Date: 2026-10-22 KST  
Status: **BOUNDED AUTHORING ENVELOPE / NO FREQUENCY FREEZE**

Depends on:
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

---

# 0. 목적

E01–E20 encounter archetype 중 어떤 것을 각 Tier에서 합법적으로 사용할 수 있는지 monster availability 기준으로 정의한다.

원칙:
- required monster가 unlock되기 전 archetype 사용 금지
- later Tier에서 earlier archetype은 계속 사용 가능
- availability != frequency
- availability != difficulty

---

# 1. Archetype requirement map

| ID | Core requirement | Complexity | Earliest Model A Tier |
|---|---|---:|---|
| E01 BASELINE_MARCH | G | C0 | T1 |
| E02 RUSH_WAVE | R (+G) | C1 | T1 |
| E03 HEAVY_LINE | B | C1 | T1 |
| E04 SHIELD_SCREEN | SH | C1 | T2 |
| E05 MIXED_WALL | B+SH | C2 | T2 |
| E06 AIR_PRESSURE | F | C1 | T2 |
| E07 CHARGE_BREAK | C | C1 | T3 |
| E08 SPLIT_FLOOD | SP | C2 | T3 |
| E09 SUPPORT_COLUMN | SUP | C2 | T4 |
| E10 SIEGE_LINE | SI | C2 | T4 |
| E11 ESCORT_SIEGE | SI + B/SH screen | C3 | T4 |
| E12 BUFFED_BULWARK | SUP + B/SH | C3 | T4 |
| E13 RUSH_BREACH | R+C | C2 | T3 |
| E14 AIR_RUSH | R+F | C2 | T2 |
| E15 REPLICATE_RUSH | SP+R | C2 | T3 |
| E16 CASCADE | SP+SUP | C3 | T4 |
| E17 BREACH_SCREEN | C + B/SH | C3 | T3 |
| E18 DUAL_AXIS | F+SI+ground | C3 | T4 |
| E19 FORTRESS | B/SH+SUP+SI | C4 | T4 |
| E20 COLLAPSE_CHAIN | SP+C+baseline/fast | C4 | T3 |

---

# 2. T1 availability

Roster:
G/R/B

Allowed:
- E01 BASELINE_MARCH
- E02 RUSH_WAVE
- E03 HEAVY_LINE

Not allowed:
E04–E20 unless a future variant is formally defined without the locked monster; do not silently substitute monster types and keep the same archetype ID.

Design consequence:
T1 variety must come from:
- formation
- cadence
- intensity
- geometry/spacing within ground plane
- class skill progression
not from prematurely unlocking later monsters.

---

# 3. T2 availability

Roster:
G/R/B/SH/F

Newly legal:
- E04 SHIELD_SCREEN
- E05 MIXED_WALL
- E06 AIR_PRESSURE
- E14 AIR_RUSH

Plus T1:
E01/E02/E03.

Total legal set:
```text
E01 E02 E03 E04 E05 E06 E14
```

Guardrail:
E14 is mixed synthesis and should not teach FLYER before E06.

---

# 4. T3 availability

Roster:
G/R/B/SH/F/C/SP

Newly legal:
- E07 CHARGE_BREAK
- E08 SPLIT_FLOOD
- E13 RUSH_BREACH
- E15 REPLICATE_RUSH
- E17 BREACH_SCREEN
- E20 COLLAPSE_CHAIN

Plus prior legal:
E01/E02/E03/E04/E05/E06/E14.

Total legal set:
```text
E01 E02 E03 E04 E05 E06 E07 E08
E13 E14 E15 E17 E20
```

E20 C4 rule:
- legal does not mean early/common
- only after CHARGER and SPLITTER individually taught/mixed
- bounded late T3 candidate

---

# 5. T4 availability

Roster:
all current V1 9.

Newly legal:
- E09 SUPPORT_COLUMN
- E10 SIEGE_LINE
- E11 ESCORT_SIEGE
- E12 BUFFED_BULWARK
- E16 CASCADE
- E18 DUAL_AXIS
- E19 FORTRESS

Plus all prior legal archetypes.

Therefore T4 has access to the full current E01–E20 library.

Teaching order still constrains use:
- E09 before E12/E16
- E10 before E11/E18/E19
- E19 only after SUP/SI mixed understanding

---

# 6. Earliest-use rule by complexity

Even after roster unlock:

## C0/C1
Can be used for first teach if it represents the new mechanic cleanly.

## C2
May be first teach only when one side is ordinary/filler and the new mechanic remains clearly readable.
Examples:
- E08 SPLIT_FLOOD
- E09 SUPPORT_COLUMN
- E10 SIEGE_LINE

## C3/C4
Never first-teach core capability by default.
Requires prior lower-complexity exposure.

---

# 7. Dependency chain examples

## T2 Flyer
```text
E06 AIR_PRESSURE
 -> E14 AIR_RUSH
```

## T3 Charger
```text
E07 CHARGE_BREAK
 -> E13 RUSH_BREACH
 -> E17 BREACH_SCREEN
 -> E20 COLLAPSE_CHAIN (late)
```

## T3 Splitter
```text
E08 SPLIT_FLOOD
 -> E15 REPLICATE_RUSH
 -> E20 COLLAPSE_CHAIN (late)
```

## T4 Supporter
```text
E09 SUPPORT_COLUMN
 -> E12 BUFFED_BULWARK
 -> E16 CASCADE
 -> E19 FORTRESS
```

## T4 Sieger
```text
E10 SIEGE_LINE
 -> E11 ESCORT_SIEGE
 -> E18 DUAL_AXIS
 -> E19 FORTRESS
```

---

# 8. Class-opportunity requirement

Tier legal set를 사용할 때:
- Knight: line/mixed/reorder opportunities
- Rogue: durable-normal opportunities
- Tank: control/charge/objective opportunities
- Archer: line/screened-backline opportunities
- Mage: cluster/density/replication opportunities

특정 Tier에서 legal archetype set이 넓더라도 한 class opportunity를 장기간 굶기면 authoring FAIL candidate다.

---

# 9. Future monsters / future archetypes

T5+ new monster가 등장하면:
- 기존 E01–E20 variant로 충분한지 먼저 redundancy test
- 실제 tactical question이 다르면 E21+ 추가
- new pressure family가 필요하면 taxonomy version-up

E01–E20은 lifetime closed list가 아니다.

---

# 10. Verdict

Model A roster ladder는 encounter library와 구조적으로 정합적이다.

- T1 legal 3
- T2 legal 7
- T3 legal 13
- T4 legal 20

이 단계에서는 frequency/count를 아직 freeze하지 않는다.
