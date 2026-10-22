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

Primary current documents:
1. `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
2. `legacy-game-structure/17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
3. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
4. `legacy-game-structure/02_TIER_SYSTEM.md`
5. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
6. `legacy-game-structure/01_META_PROGRESSION.md`
7. `legacy-game-structure/15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
8. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`

---

# Structural truth

## Shared Stage / independent class progress
- same Tier/Stage content across all classes
- independent class progression records
- soft walls allowed
- hard class lockout forbidden
- stars/achievements may help a blocked class progress later

## Stars / achievements
- Tier = 50 Stage
- fail 1–19 0★ / 20–39 1★ / 40–49 2★ / clear50 3★
- stars = broad account permanent growth
- achievements = targeted cross-class growth
- exact values/mappings remain OPEN

---

# Monster progression — USER CONFIRMED

Current 9 ordinary monsters are not the final lifetime roster.

Rules:
- do not force all 9 into T1
- new monsters should appear as Tiers rise
- new Tier entry should provide real content novelty
- future monster additions must not require structural rewrite
- no fixed `monsterCount==9` assumptions
- taxonomy may version-up for future capabilities

Old candidates based on `T1 teaches all 9` are PARKED:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

---

# Difficulty — USER CONFIRMED

General Tier calibration:

> intended-entry `SKILLED_V2` Stage1→50 full-Tier clear probability should normally be **below 60%**.

- 60% = upper bound, not midpoint
- T1 may be higher
- measure full-Tier 3★ clear, not single Stage pass
- overgrown replay accounts excluded from this gate
- class rates may differ

`SKILLED_V2` must be stronger than old skilled assumptions:
- combo 40 is achievable skilled play
- stronger combo maintenance/timing/heavy completion
- HIGH_MASTERY_STRESS remains above it

Exact probability parameters remain OPEN.

---

# Master Campaign Matrix V0.1

Tier-count comparison:

| Model | Minimum successful class-stage volume | Max stars | Current rank |
|---|---:|---:|---|
| 4 initial Tier + T5+ expansion | 1000 | 60★ | 1 |
| 5 initial Tier + T6+ expansion | 1250 | 75★ | 2 |
| 6 initial Tier | 1500 | 90★ | low priority |

Current structural front-runner, NOT frozen:
**4 initial Tier + open-ended T5+ expansion**.

Model A monster unlock candidate:
- T1: GRUNT / RUNNER / BRUTE
- T2: +SHIELD / +FLYER
- T3: +CHARGER / +SPLITTER
- T4: +SUPPORTER / +SIEGER
- T5+: future monster/content expansion

Model B remains viable:
- T1 G/R/B
- T2 +SH/F
- T3 +C/SP
- T4 +SUP
- T5 +SI
- T6+ future

No monster unlock is frozen yet.

---

# Current exact next boundary

Do not return to T1 count/cadence micro-tuning yet.

Next:
1. compare Model A vs B against all 5 class roles
2. define Tier novelty budgets beyond monster unlock count
3. define boss novelty placeholders by Tier
4. refine relative run skill-reach bands
5. define `SKILLED_V2` parameter test plan
6. estimate play-volume under `<60%` skilled full-clear target
7. compare repetition / soft-wall / meta-progression room
8. choose one bounded campaign simulation spine
9. only then reopen encounter frequency/count/composition/cadence

## Do not yet
- freeze final initial Tier count
- freeze exact monster unlock Stage/Tier
- freeze production monster values
- freeze star/achievement values
- resume Lv11+ live implementation
- expand detailed 3P/4P recipes

## Governance
`master spine -> campaign matrix -> candidate authoring -> deterministic simulation -> classify -> revise -> explicit freeze -> implementation`.
