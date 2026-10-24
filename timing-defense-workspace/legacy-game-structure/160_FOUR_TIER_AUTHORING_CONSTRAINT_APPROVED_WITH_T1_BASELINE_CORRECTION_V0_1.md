# Timing Defense — Four-Tier Authoring Constraint Approved With T1 Baseline Correction V0.1

Date: 2026-10-24 KST  
Status: **USER APPROVED / STRUCTURAL AUTHORING AUTHORITY / ONE MINIMAL CONSISTENCY CORRECTION / NO EXACT COMBAT SCALAR FREEZE**

Depends on:
- `158_INITIAL_FOUR_TIER_CAMPAIGN_AND_MONSTER_AVAILABILITY_APPROVED_CONTRACT_V0_1.md`
- `159_FOUR_TIER_AUTHORING_CONSTRAINT_SYNTHESIS_AND_REVIEW_V0_1.md`
- `03_STAGE_STRUCTURE_50.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
- `28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
- P6 closure `156_P6_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`

## 1. User approval

On 2026-10-24 the user instructed the project to continue under the explicit operating rule that every step must be checked for consistency, mismatch and contradiction from multiple viewpoints while avoiding unnecessary repetition and scope expansion.

The lower-layer authoring package proposed in doc159 is therefore adopted, subject to the minimal T1 baseline correction in Section 3 below.

## 2. Adopted structural package

Tier identities:
```text
T1 = Foundation / Timing & Frontline
T2 = Mitigation / Geometry
T3 = Burst / Transformation
T4 = Formation / Siege
```

Derived legal encounter availability remains:
```text
T1 = E01-E03 / 3 legal archetypes
T2 = 7 legal archetypes
T3 = 13 legal archetypes
T4 = full current E01-E20 library
```

Formation/cadence progression from doc159 Section 5 is adopted as structural authoring vocabulary.

Range-based monster teach/mix/high-pressure windows from doc159 Section 6 are adopted as authoring constraints **except for the corrected T1 GRUNT first-mixed range below**.

Adopted guards:
- rolling 10-Stage class-opportunity starvation warning;
- readable minimum special-monster role-expression opportunity before skilled counterplay suppresses activation;
- no new core ordinary first-teach in Stage41-50;
- SUPPORTER and SIEGER isolated teaching before combined high pressure;
- pressure/frequency/complexity numerical ranges remain candidate-generation/search bounds, not production targets.

## 3. T1 GRUNT first-mixed contradiction found and corrected

Prior candidate table contained:
```text
GRUNT first mixed = Stage4-6
RUNNER first teach = Stage5-7
RUNNER first mixed = Stage8-12
BRUTE first teach = Stage15-17
```

Under the approved T1 roster, no second ordinary monster is legitimately mixed with GRUNT during Stage4-6 unless RUNNER is mixed before RUNNER's own Stage8-12 mixed window.

That creates a lower-layer dependency contradiction.

Minimal correction:
```text
GRUNT first teach = Stage1-2  (unchanged)
GRUNT first mixed = Stage8-12 (corrected; aligns to first legal RUNNER mixed exposure)
GRUNT first high pressure = Stage21-29 (unchanged / baseline-special handling preserved)
```

Why this is the least-cost correction:
- GRUNT is neutral baseline vocabulary, not a capability novelty that needs an independent mixed-teaching deadline;
- RUNNER learning separation remains intact;
- BRUTE timing remains intact;
- no Tier availability, P6 conclusion, class identity, skill contract or production value changes.

Do **not** solve this by prematurely mixing RUNNER in Stage6 or by introducing BRUTE early.

## 4. Early anti-repetition reconciliation

The broad candidate guard against three consecutive stages with the same dominant archetype cannot be applied literally before the second T1 monster is taught, because only GRUNT is available as readable taught vocabulary.

Therefore the guard is interpreted operationally as:
```text
before second-monster first teach:
  archetype repetition is allowed when structurally unavoidable,
  but formation/cadence/geometry signatures must vary;

after second-monster first teach:
  normal archetype repetition guard applies.
```

This is a bounded onboarding exception, not permission for later repetitive authoring.

## 5. T1 collision watches preserved

Known and accepted WATCH items:
- RUNNER first-teach Stage5-7 overlaps candidate Lv6 reach Stage5-7;
- BRUTE first-mixed Stage18-20 overlaps candidate Lv16 reach Stage18-21;
- first high-pressure combinations must stay clear enough around first-time Lv21 learning Stage25-28;
- Lv31 Stage41-45 remains the only fixed power-window authority and receives no new ordinary mechanic teaching.

These are attribution/readability watches, not current structural FAILs.

## 6. Still not frozen

This contract does not freeze:
- exact Stage recipes or spawn events;
- exact monster counts;
- spawn milliseconds;
- HP/speed/damage/capability coefficients;
- exact pressure-family production frequency;
- exact EXP formula or non-Lv31 reach distributions;
- shop values;
- class buffs/nerfs;
- P×P probability;
- boss mechanics;
- production gameplay.

## 7. Next work boundary

Proceed to a **T1 Stage1-50 signature skeleton candidate**, then run static consistency checks before any deterministic exact recipe or scalar tuning.

Required checks:
```text
roster/archetype legality
teach -> mix -> high-pressure ordering
skill-novelty collision watches
50-stage macro-band purpose
star-boundary cliff risk
complexity search-envelope fit
pressure-family search-envelope fit
anti-repetition
rolling 10-stage class-opportunity coverage
no-hard-lockout risk
Lv31 Stage41-45 runway
Stage46-49 post-Lv31 mastery
Stage50 no-unpreviewed-core-mechanic rule
```
