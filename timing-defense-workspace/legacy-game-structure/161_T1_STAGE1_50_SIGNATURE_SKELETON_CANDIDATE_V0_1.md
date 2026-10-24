# Timing Defense — T1 Stage1-50 Signature Skeleton Candidate V0.1

Date: 2026-10-24 KST  
Status: **AUTHORING CANDIDATE / STRUCTURAL SIGNATURES ONLY / NO EXACT SPAWN OR COMBAT SCALAR FREEZE**

Depends on:
- `158_INITIAL_FOUR_TIER_CAMPAIGN_AND_MONSTER_AVAILABILITY_APPROVED_CONTRACT_V0_1.md`
- `160_FOUR_TIER_AUTHORING_CONSTRAINT_APPROVED_WITH_T1_BASELINE_CORRECTION_V0_1.md`
- `03_STAGE_STRUCTURE_50.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
- `32_MODEL_A_TIER_ENCOUNTER_AVAILABILITY_V0_1.md`
- `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- `34_MODEL_A_FREQUENCY_RANGE_ENVELOPE_V0_1.md`
- `148_ENCOUNTER_OPPORTUNITY_DISTRIBUTION_FRAMEWORK_PROPOSAL_V0_1.md`

## 1. Scope

This file materializes the first full T1 50-Stage **signature skeleton**.

It chooses only:
- Stage purpose;
- legal encounter/archetype family;
- formation/cadence vocabulary;
- dominant complexity bucket;
- meaningful pressure-family tags;
- intended class-opportunity tags;
- teaching / gate / skill-window relationship.

It does **not** choose:
- monster count;
- HP / speed / damage;
- spawn milliseconds;
- exact overlap duration;
- exact Stage duration;
- exact shop/EXP value;
- boss mechanics;
- production implementation.

Legend:
```text
G = GRUNT
R = RUNNER
B = BRUTE
E01 = BASELINE_MARCH
E02 = RUSH_WAVE
E03 = HEAVY_LINE
SYNTH = multiple already-taught legal archetypes in one Stage
K/Rg/T/A/M = Knight / Rogue / Tank / Archer / Mage opportunity tag
```

## 2. Stage1-50 candidate

| Stage | Band | Signature / monsters | Formation | Cadence | Cx | Meaningful pressure | Primary purpose / watch | Opportunity |
|---:|---|---|---|---|---:|---|---|---|
| 1 | Establish | E01 / G | F01 | CD01 | C0 | BASELINE | GRUNT teach 1; pure timing baseline | K,A |
| 2 | Establish | E01 / G | F03 | CD01 | C0 | BASELINE | GRUNT teach 2; light density read | M |
| 3 | Establish | E01 / G | F04 | CD02 | C0 | BASELINE | scatter timing contrast | Rg |
| 4 | Establish | E01 / G | F01 | CD03 | C0 | BASELINE | first clear wave boundary | K,A |
| 5 | Establish | E02 / R | F01 | CD01 | C1 | RUSH | RUNNER first teach; **Lv6 collision WATCH** | Rg,T,A |
| 6 | Establish | E01 / G | F03 | CD02 | C1 | BASELINE,FLOOD | Lv6 identity/buffer; no new monster mix | M |
| 7 | Establish | E02 / R | F04 | CD02 | C1 | RUSH | RUNNER focused verify | Rg,T |
| 8 | Establish | E02 / G+R | F01 | CD03 | C1 | RUSH | RUNNER first mixed + corrected GRUNT first mixed | K,Rg,T,A |
| 9 | Establish | E01 / G | F03 | CD01 | C0 | BASELINE | recovery / density recall | M |
| 10 | Checkpoint A | E02 / G+R | F01 | CD03 | C1 | RUSH | read check; no new grammar | K,Rg,T,A |
| 11 | Introduce & Mix | E01 / G | F03 | CD04 | C1 | BASELINE,FLOOD | light burst after basics; Lv11 band begins | M |
| 12 | Introduce & Mix | E02 / G+R | F04 | CD03 | C1 | RUSH | sustained tempo in scatter | Rg,T |
| 13 | Introduce & Mix | E01 / G | F01 | CD03 | C1 | BASELINE | line mastery / skill attribution space | K,A |
| 14 | Introduce & Mix | E01 / G | F04 | CD01 | C0 | BASELINE | recovery before BRUTE introduction | Rg |
| 15 | Introduce & Mix | E03 / B | F01 | CD01 | C1 | BULWARK | BRUTE first teach | K,Rg,A |
| 16 | Introduce & Mix | E03 / B | F02 | CD02 | C1 | BULWARK | BRUTE durable-front verify | K,Rg,T,A |
| 17 | Introduce & Mix | E01 / G | F01 | CD03 | C1 | BASELINE | deliberate contrast/recovery before BRUTE mix | K,A |
| 18 | Introduce & Mix | E03 / G+B | F02 | CD03 | C1 | BULWARK | BRUTE first mixed; **Lv16 collision WATCH** | K,Rg,T,A |
| 19 | Introduce & Mix | E03+E02 / B+R | F02 | CD05 | C2 | BULWARK | first target-order/stagger contrast | K,Rg,T,A |
| 20 | Star Gate A | SYNTH E01+E02+E03 / G+R+B | F01/F02 | CD03 | C2 | BASELINE | first meaningful T1 synthesis; no arbitrary 1★ cliff | K,Rg,T,A |
| 21 | Deepen | E02 / G+R | F03 | CD04 | C2 | RUSH,FLOOD | RUNNER first high-pressure | Rg,T,M |
| 22 | Deepen | E03 / G+B | F02 | CD03 | C2 | BULWARK | BRUTE first high-pressure | K,Rg,T,A |
| 23 | Deepen | E02+E03 / R+B | F02 | CD04 | C2 | RUSH,BULWARK | speed-vs-durability contrast peak | K,Rg,T,A |
| 24 | Deepen | E01 / G | F03 | CD04 | C1 | BASELINE,FLOOD | GRUNT baseline high-pressure / density | M |
| 25 | Deepen | E01 / G | F04 | CD01 | C0 | BASELINE | **Lv21 first-time reward buffer** | Rg |
| 26 | Deepen | E03 / G+B | F01 | CD02 | C1 | BULWARK | known durable focus; no new attribution | K,Rg,A |
| 27 | Deepen | E02 / G+R | F04 | CD03 | C1 | RUSH | known tempo focus | Rg,T |
| 28 | Deepen | E01 / G | F03 | CD03 | C1 | BASELINE,FLOOD | density recall while Lv21 settles | M |
| 29 | Deepen | E02+E03 / G+R+B | F08 | CD05 | C2 | RUSH,BULWARK | late/limited split-axis synthesis | K,Rg,T,A |
| 30 | Checkpoint B | E01+E03 / G+B | F01 | CD03 | C1 | BASELINE | mid synthesis / optional boss-preview slot only | K,Rg,A |
| 31 | Pressure / Soft Wall | E03 / G+B | F02 | CD04 | C1 | BULWARK | focused durable pressure; difficulty via intensity not complexity | K,Rg,T,A |
| 32 | Pressure / Soft Wall | E02 / G+R | F04 | CD04 | C2 | RUSH | Lv26-band tempo pressure | Rg,T |
| 33 | Pressure / Soft Wall | E01 / G | F03 | CD04 | C2 | BASELINE,FLOOD | density pressure / Mage expression | M |
| 34 | Pressure / Soft Wall | E03+E02 / G+B+R | F02 | CD05 | C2 | BULWARK | target reorder / control opportunity | K,Rg,T,A |
| 35 | Pressure / Soft Wall | E01 / G | F04 | CD05 | C1 | BASELINE | lower-complexity timing/reorder recovery | K,Rg |
| 36 | Pressure / Soft Wall | E03 / G+B | F01 | CD03 | C1 | BULWARK | focused heavy line / Lv26 attribution space | K,Rg,A |
| 37 | Pressure / Soft Wall | E02 / G+R | F08 | CD04 | C2 | RUSH | bounded split-axis tempo | Rg,T |
| 38 | Pressure / Soft Wall | E01+E03 / G+B | F02 | CD03 | C1 | BULWARK | mixed durable focused challenge | K,Rg,T,A |
| 39 | Pressure / Soft Wall | E02+E03 / R+B | F08 | CD05 | C3 | RUSH,BULWARK | rare late T1 synthesis peak | K,Rg,T,A |
| 40 | Star Gate B | SYNTH E01+E02+E03 / G+R+B | F01+F03 | CD03 | C2 | BASELINE | 2★ transition; broad known-vocabulary check, not cliff | K,Rg,T,A,M |
| 41 | Lv31 Ascension | E01 / G | F01 | CD01 | C0 | BASELINE | controlled runway / Lv31 acquisition relief | K,A |
| 42 | Lv31 Ascension | E02 / G+R | F04 | CD02 | C1 | RUSH | known tempo, no new grammar | Rg,T |
| 43 | Lv31 Ascension | E03 / G+B | F02 | CD02 | C1 | BULWARK | known durable, class-role read | K,Rg,T,A |
| 44 | Lv31 Ascension | E01 / G | F03 | CD04 | C1 | BASELINE,FLOOD | familiar density / Mage Lv31 expression surface | M |
| 45 | Lv31 Ascension | E02+E03 / R+B | F01 | CD05 | C2 | RUSH | moderate mixed mastery; still no peak complexity | K,Rg,T,A |
| 46 | Post-Lv31 Mastery | E03+E01 / G+B | F02 | CD04 | C2 | BULWARK | durable mastery / objective-control proxy surface | K,Rg,T,A |
| 47 | Post-Lv31 Mastery | E02 / G+R | F04 | CD03 | C1 | RUSH | focused tempo mastery / recovery from mixed peak | Rg,T |
| 48 | Post-Lv31 Mastery | E01+E02 / G+R | F03 | CD04 | C2 | BASELINE,FLOOD | density+tempo mastery | M,T |
| 49 | Post-Lv31 Mastery | E02+E03 / R+B | F08 | CD05 | C2 | RUSH,BULWARK | pre-final split-axis mastery | K,Rg,T,A |
| 50 | Tier Final | SYNTH E01+E02+E03 / G+R+B | MULTI | CD03 | C3 | BASELINE | full learned-vocabulary synthesis; **no unpreviewed core mechanic** | K,Rg,T,A,M |

## 3. Deliberate exceptions / watches

### 3.1 Stage1-4 archetype repetition
Only GRUNT is taught/readable before RUNNER introduction, so E01 repetition is structurally unavoidable.
The onboarding exception from doc160 applies.
Formation/cadence varies across the four Stages.

### 3.2 RUNNER × Lv6
RUNNER first teach at Stage5 intentionally sits inside the candidate Lv6 Stage5-7 reach band.
This remains a pedagogic WATCH, not a reason to move the approved monster ladder or fit EXP numerically.

### 3.3 BRUTE mixed × Lv16
BRUTE first mixed at Stage18 overlaps the candidate Lv16 Stage18-21 band.
The Stage is kept at C1 and uses already-readable E03 semantics to limit attribution ambiguity.

### 3.4 Lv21 Stage25-28
No new monster teach or first-high-pressure event occurs in Stage25-28.
The band deliberately alternates recovery/focused known problems so the first-time Lv21 reward is visible.

### 3.5 Lv31 Stage41-45
No new ordinary mechanic is introduced.
Complexity sequence is:
```text
C0, C1, C1, C1, C2
```
This creates an acquisition runway before Stage46-49 mastery.

## 4. Candidate pressure-presence totals

Meaningful Stage presence in this skeleton:
```text
BASELINE = 22
FLOOD    = 8
RUSH     = 16
BULWARK  = 16
BREACH/AERIAL/REPLICATE/SUPPORT/SIEGE = 0
```

This fits the retained T1 search envelope:
```text
BASELINE 19-30
FLOOD 5-11
RUSH 9-17
BULWARK 9-17
```

These are candidate-stage presence counts, not production spawn shares.

## 5. Candidate dominant-complexity totals

```text
C0 = 8
C1 = 25
C2 = 15
C3 = 2
C4 = 0
Total = 50
```

This fits the retained T1 search envelope:
```text
C0 8-14
C1 22-30
C2 8-15
C3 0-4
C4 0
```

## 6. Status

This skeleton is ready for static consistency audit.

Do not convert it directly to production Stage data yet.
First inspect:
- rolling class-opportunity coverage;
- repetition;
- macro-band / star boundary shape;
- skill collision;
- no-hard-lockout risk;
- late Lv31 runway;
- whether any candidate correction is cheaper at signature level than after exact spawn authoring.
