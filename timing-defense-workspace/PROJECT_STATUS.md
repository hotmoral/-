# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Current validated deployment
- Cloudflare Workers + Durable Objects
- executable checkpoint: v0.45 SIEGER FULL PASS
- deployment HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health: `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

---

# Current planning authority

Active structural phase:
**Master Campaign Progression Spine / Master Campaign Matrix**

Primary docs:
- `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `legacy-game-structure/17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
- `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
- `legacy-game-structure/02_TIER_SYSTEM.md`
- `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`

Current work is no longer T1 micro-tuning.

---

# Core progression truth

- 5 classes progress through Tiers independently.
- Same Tier/Stage content is shared across classes.
- 1 Tier = 50 Stages.
- fail 1–19 = 0★; fail 20–39 = 1★; fail 40–49 = 2★; clear50 = 3★.
- stars = broad account permanent progression.
- achievements = targeted cross-class progression.
- hard class lockout forbidden; recoverable soft walls allowed.

---

# Monster campaign direction

Current mechanical roster:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

But:
- current 9 are not the final lifetime roster,
- T1 should not automatically contain all 9,
- higher Tiers should introduce new monster archetypes,
- reaching a new Tier should create content novelty,
- future monsters must be addable through versioned registry/tier availability,
- no fixed-size roster assumption,
- pressure taxonomy may expand if future capabilities require it.

Old T1-all-9 candidates are PARKED, not deleted:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

---

# Difficulty direction

User-confirmed default:

> non-T1 intended-entry `SKILLED_V2` full-Tier Stage1→50 clear probability should normally be **<60%**.

Interpretation:
- 60% is an upper bound.
- T1 may be easier.
- evaluate the intended entry account state, not an overgrown replay account.
- class-specific clear rates may differ.
- some classes may intentionally hit lower recoverable soft walls.

`SKILLED_V2` must be stronger than the old skilled simulation profile.
Combo 40 should be modeled as achievable skilled play rather than high-mastery-only.
Exact timing/combo probabilities remain open parameters.

---

# Master Campaign Matrix V0.1

Current comparison:

- 4 initial Tiers -> 1000 minimum successful class-stage clears / 60 max stars.
- 5 initial Tiers -> 1250 / 75 stars.
- 6 initial Tiers -> 1500 / 90 stars.

Current structural ranking, NOT frozen:
1. **4 initial Tier + open-ended T5+ expansion**
2. 5 initial Tier + T6+ expansion
3. 6 initial Tier = low priority with current roster

Model A unlock candidate:
- T1 G/R/B
- T2 +SH/F
- T3 +C/SP
- T4 +SUP/SI
- T5+ future expansion

Model B splits late support/siege:
- T4 +SUP
- T5 +SI

---

# Skill authority
- Lv6 current authoritative
- Lv11/Lv16/Lv21 exact legacy parity candidates
- Lv26 designed-not-authoritative
- Lv31 unresolved

Live skill migration remains parked.
Master Campaign Matrix must first define relative skill-reach bands across a 50-stage run.

---

# Exact next work

1. compare 4-Tier Model A vs 5-Tier Model B across all five classes
2. define Tier novelty budgets beyond monster unlocks
3. define boss novelty placeholders
4. refine relative skill-reach bands
5. define SKILLED_V2 parameter test plan
6. estimate total play volume under sub-60 clear target
7. compare repetition / soft-wall / meta-progression room
8. choose a bounded simulation spine
9. only then resume encounter frequency/count/composition/cadence

No production values are frozen by this status update.
