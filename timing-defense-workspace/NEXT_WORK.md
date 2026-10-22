# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed implementation checkpoint
- Cloudflare DO through v0.45 SIEGER — FULL PASS
- executable HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

Stage1–3 are regression fixtures only.
Do not reconstruct legacy Stage4→10 as production content.

---

# ACTIVE PHASE — Master Campaign Progression Spine

Primary authority for current planning:
`legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

Read order:
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/README.md`
5. `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
6. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
7. `legacy-game-structure/01_META_PROGRESSION.md`
8. `legacy-game-structure/02_TIER_SYSTEM.md`
9. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
10. `legacy-game-structure/15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
11. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
12. encounter/legacy evidence only as needed

---

# Structural truth

## Shared Stage / independent class progress
- same Tier/Stage content across all classes
- class records independent
- soft walls allowed
- hard class lockout forbidden
- other-class stars/achievements should help recover blocked classes

## Stars
- Tier = 50 Stage
- fail 1–19 0★
- fail 20–39 1★
- fail 40–49 2★
- clear 50 3★
- bestStars only
- stars = broad account permanent growth

## Achievements
- targeted cross-class progression
- class Tier / all-class Tier / pure SOLO AI0 etc.
- exact reward graph/value remains open until soft-wall data exists

---

# Monster progression direction — USER CONFIRMED

Current 9 ordinary monsters are **not** final lifetime roster.

Rules:
- do not force all 9 into Tier1
- higher Tiers should introduce new monster archetypes
- new Tier entry should provide content novelty, not only higher HP/count
- existing monsters gain new formations/combinations/cadence in later Tiers
- future monsters must be addable without structural rewrite
- no `monsterCount==9` hardcoding
- pressure taxonomy may version-up if future capability needs it

Therefore old candidates based on `T1 teaches all 9` are PARKED:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

Retain as historical/candidate evidence only.

---

# Difficulty direction — USER CONFIRMED

General Tier calibration:

> intended-entry `SKILLED_V2` full-Tier Stage1→50 clear probability should normally be **below 60%**.

Interpretation:
- 60% is an upper bound, not the target midpoint
- Tier1 may be higher for onboarding
- measure full Tier 3★ clear, not single Stage pass rate
- evaluate at intended-entry progression state, not overgrown replay account
- class clear rates may differ
- some classes may intentionally hit recoverable soft walls

## Skilled profile reset
Existing skilled assumptions are too weak for the desired difficulty.

`SKILLED_V2` must treat:
- combo 40 as achievable skilled play, not high-mastery-only
- stronger combo maintenance/timing/heavy completion than prior profile
- `HIGH_MASTERY_STRESS` remains above SKILLED_V2

Exact timing/combo probabilities remain calibration parameters, not frozen now.

---

# Exact next boundary — Master Campaign Matrix

Do **not** continue T1 micro-simulation yet.

Order:
1. compare Tier-count candidates 4 / 5 / 6
2. define novelty budget per Tier
3. design current 9-monster Tier availability/unlock candidates
4. define future-monster expansion contract/slots
5. define 50-Stage macro role per Tier
6. map expected Lv6/11/16/21/26/31 reach windows
7. define meta-power states:
   - P0 FRESH
   - P1 BALANCED
   - P2 STAR_GROWN
   - P3 ACHIEVEMENT_ASSISTED
8. define Tier-by-Tier SKILLED_V2 clear-rate envelopes
9. cross-audit novelty × monster × skills × meta growth × difficulty
10. only then return to encounter frequency/count/composition/cadence

## Do not yet
- freeze final Tier count
- freeze exact monster unlock points
- freeze production monster values
- freeze star/achievement values
- resume Lv11+ live implementation
- expand detailed 3P/4P recipes

## Governance
`master spine -> campaign matrix -> candidate authoring -> simulation -> classify -> revise -> explicit freeze -> implementation`.
