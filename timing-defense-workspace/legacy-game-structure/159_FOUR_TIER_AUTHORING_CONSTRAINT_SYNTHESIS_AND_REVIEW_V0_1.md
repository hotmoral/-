# Timing Defense — Four-Tier Authoring Constraint Synthesis & Review V0.1

Date: 2026-10-24 KST  
Status: **STRUCTURAL REVIEW PACKAGE / USER DECISION REQUIRED FOR LOWER-LAYER DESIGN ADOPTION / NO EXACT STAGE FREEZE**

Depends on:
- `158_INITIAL_FOUR_TIER_CAMPAIGN_AND_MONSTER_AVAILABILITY_APPROVED_CONTRACT_V0_1.md`
- `28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
- `29_MODEL_A_TIER_PRESSURE_COMPLEXITY_ENVELOPE_V0_1.md`
- `32_MODEL_A_TIER_ENCOUNTER_AVAILABILITY_V0_1.md`
- `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- `34_MODEL_A_FREQUENCY_RANGE_ENVELOPE_V0_1.md`
- `35_LAYERA0_ENCOUNTER_ENVELOPE_VALIDATION_REPORT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `148_ENCOUNTER_OPPORTUNITY_DISTRIBUTION_FRAMEWORK_PROPOSAL_V0_1.md`
- P6 results `151`, `152`, `155`, closure `156`

## 1. Purpose

The four-Tier monster ladder is now user-approved.
This review determines what can be carried forward from previously validated Model A assets without repeating closed work, and what still needs a new user decision before exact Stage authoring.

Rule:

```text
approved Tier availability
-> derived legal encounter vocabulary
-> candidate Tier identity / formation / cadence / introduction windows
-> user review
-> only then exact T1 Stage1-50 candidate authoring
```

## 2. Consistency result

No material contradiction was found between the approved four-Tier ladder, the old bounded Model A authoring assets, and P6 causal conclusions.

The existing Layer-A0 envelope had already passed its structural validator after correctly separating encounter-level complexity from whole-Stage complexity:

```text
RESULT=PASS errors=0 warnings=0
```

This historical PASS remains useful as bounded structural evidence. It is not a production balance/readability freeze.

## 3. Derived encounter availability — consequence of approved roster

Because each E01-E20 archetype has explicit monster requirements, the following legal sets follow directly from the approved Tier roster and do not independently choose exact Stage placement or frequency.

### T1 — 3 legal archetypes
```text
E01 BASELINE_MARCH
E02 RUSH_WAVE
E03 HEAVY_LINE
```

### T2 — 7 legal archetypes
Adds:
```text
E04 SHIELD_SCREEN
E05 MIXED_WALL
E06 AIR_PRESSURE
E14 AIR_RUSH
```

### T3 — 13 legal archetypes
Adds:
```text
E07 CHARGE_BREAK
E08 SPLIT_FLOOD
E13 RUSH_BREACH
E15 REPLICATE_RUSH
E17 BREACH_SCREEN
E20 COLLAPSE_CHAIN
```

### T4 — full current E01-E20 library
Adds:
```text
E09 SUPPORT_COLUMN
E10 SIEGE_LINE
E11 ESCORT_SIEGE
E12 BUFFED_BULWARK
E16 CASCADE
E18 DUAL_AXIS
E19 FORTRESS
```

Availability does not mean common use. C3/C4 archetypes are not first-teach defaults.

## 4. Recommended Tier identities — decision item

### T1 — FOUNDATION / TIMING & FRONTLINE
Primary questions:
- basic timing consistency;
- sustained speed vs durable frontline;
- simple line/cluster/scatter reading.

Pressure direction:
```text
BASELINE high
RUSH medium
BULWARK medium
FLOOD low-medium
```

### T2 — MITIGATION / GEOMETRY
Primary questions:
- raw durability vs mitigation;
- ground/air geometry;
- line and spatial opportunity changes.

Pressure direction:
```text
BULWARK high
AERIAL medium-high
BASELINE medium-high
RUSH medium
```

### T3 — BURST / TRANSFORMATION
Primary questions:
- readable interruptible charge timing;
- death-triggered population transformation;
- target-order reset and bounded overlap.

Pressure direction:
```text
BREACH high
REPLICATE high
FLOOD/RUSH medium-high
BULWARK/AERIAL supporting
```

### T4 — FORMATION / SIEGE
Primary questions:
- protected backline threats;
- screening and uptime;
- objective/wall pressure;
- prior mechanics recombined without constant maximum chaos.

Pressure direction:
```text
SUPPORT high
SIEGE high
BULWARK medium-high
prior families medium or lower
```

Important: `SUPPORT high` and `SIEGE high` are Tier-level identities, not a requirement to combine them in every Stage.

## 5. Recommended formation/cadence progression — decision item

### T1
Formation:
`F01 LINE_LIGHT`, `F02 LINE_DURABLE_FRONT`, `F03 CLUSTER_LIGHT`, `F04 SCATTER_LIGHT`; `F08 SPLIT_AXIS` only late/limited.

Cadence:
`CD01 DRIP_SLOW`, `CD02 DRIP`, `CD03 WAVE`; `CD04 BURST_LIGHT` after basics; `CD05 STAGGER` late/limited.

### T2
Adds/expands:
- `F05 AIR_OFFSET`
- wider use of `F08 SPLIT_AXIS`
- limited `CD07 LATE_INSERT`

Backline escort grammar remains reserved.

### T3
Adds/expands:
- `F09 REPLICATION_CLUSTER`
- advanced durable-front protection of CHARGER
- `CD07 LATE_INSERT`
- `CD08 OVERLAP_BOUNDED` late and guarded

`CD06 ESCORT` remains primarily T4 vocabulary.

### T4
All F01-F09 and CD01-CD08 become available.
Key new signatures:
- `F06 SCREEN_BACKLINE`
- `F07 ESCORT_COLUMN`
- `CD06 ESCORT`

SUPPORTER/SIEGER must first appear in simpler readable grammar before full escort/overlap synthesis.

## 6. Recommended monster introduction windows — decision item

These are range constraints, not exact Stage recipes.
Only Lv31 Stage41-45 is already user-confirmed power-window authority; other skill reach bands remain calibration candidates.

| Tier | Monster | First teach | First mixed | First high-pressure |
|---|---|---:|---:|---:|
| T1 | GRUNT | 1-2 | 4-6 | 21-29 |
| T1 | RUNNER | 5-7 | 8-12 | 21-24 |
| T1 | BRUTE | 15-17 | 18-20 | 21-23 |
| T2 | SHIELD | 5-7 | 8-12 | 21-24 |
| T2 | FLYER | 15-17 | 18-22 | 28-31 |
| T3 | CHARGER | 5-7 | 8-14 | 21-24 |
| T3 | SPLITTER | 15-17 | 18-22 | 28-31 |
| T4 | SUPPORTER | 11-13 | 14-19 | 29-31 |
| T4 | SIEGER | 22-24 | 25-29 | 37-39 |

Mandatory guards even if ranges later move:
- first teach <= first mixed <= first high pressure;
- no new core ordinary first teach in Stage41-50;
- no two major unpreviewed first teaches in the same short window;
- CHARGER teach must be readable and survivable without requiring Tank;
- SPLITTER high pressure requires effective child-volume accounting;
- SUPPORTER and SIEGER first teaches stay separated;
- combined SUPPORTER+SIEGER high pressure only after both mixed windows.

## 7. Frequency / complexity envelope — retain as search bounds, not adoption target

The old broad pressure-presence and dominant-complexity ranges remain suitable for candidate generation/search-space control.
They should **not** be promoted to production frequencies at this decision gate.

Key retained guards:
- no same dominant archetype signature for 3 consecutive Stages;
- no identical archetype+formation+cadence consecutive repetition;
- no consecutive C4;
- no more than two C4 in a five-Stage window candidate;
- preserve lower-complexity recovery/focused stages even late;
- Stage20/40 star boundaries must not create arbitrary cliffs;
- Stage41-45 may include relief while Lv31 is acquired.

## 8. Class-opportunity guardrail — recommended adoption

P6 confirms that encounter family can rotate class advantage, so equal class performance per Stage is not the goal.
The correct static guard is role starvation prevention.

Recommended warning rule:

```text
Every rolling 10-Stage window should expose at least one meaningful opportunity tag for each class.
```

Interpretation:
- Knight: line/mixed/reorder
- Rogue: durable-normal/frontline execution
- Tank: control/charge/objective protection
- Archer: line/screened-backline penetration
- Mage: cluster/density/replication

This does not require each class to be favored every ten Stages.
It detects long stretches where a class identity has no authored surface.

## 9. Role-expression guardrail — recommended adoption

For any encounter explicitly teaching/testing a special monster:

```text
readable minimum role-expression opportunity must exist
-> skilled player counterplay may then suppress full activation
```

When expression fails, correction order remains:
1. absolute entry depth;
2. relative front/back depth;
3. spawn order/delay;
4. screen lifetime/composition;
5. cadence/overlap;
6. trigger/standoff exposure timing;
7. only then monster scalar changes.

This prevents using HP inflation as the default readability fix.

## 10. P6-specific guards on this package

- Do not use one encounter family's class ranking as a global buff/nerf signal.
- Do not make T4 a pure damage race; preserve Tank objective-protection surface.
- Do not fit introduction windows to exact provisional EXP milestone outputs.
- Do not apply a flat shop->EXP correction.
- Carry `FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH` into later full-run calibration.

## 11. Recommendation for user decision

Adopt the following as the next structural authoring constraint package:

```text
Tier identities:
T1 Foundation / Timing & Frontline
T2 Mitigation / Geometry
T3 Burst / Transformation
T4 Formation / Siege

Derived legal archetype sets:
T1 3 / T2 7 / T3 13 / T4 20

Formation/cadence vocabulary progression:
as Section 5

Monster teach/mix/high-pressure windows:
as Section 6, range-based only

Class-opportunity starvation guard:
rolling 10-Stage warning

Monster role-expression guard:
readable expression opportunity before counterplay
```

Keep pressure/frequency/complexity numeric ranges as candidate-generation bounds only.
Do not yet freeze exact Stage1-50 compositions, spawn counts, timings, monster scalars, EXP/shop values, or production gameplay.

## 12. Next boundary if approved

After this package is approved:

1. materialize a **T1 Stage1-50 signature skeleton candidate** using only T1 legal vocabulary;
2. check teaching order, repetition, class opportunities, skill-window collisions, star boundaries and late Lv31 runway;
3. inspect candidate before any exact combat scalar tuning;
4. only then deepen into deterministic encounter recipes/micro-simulation where needed.

Exact production values remain downstream.
