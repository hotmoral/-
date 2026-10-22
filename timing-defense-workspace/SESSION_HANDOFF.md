# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Canonical recovery rule
Do not trust this handoff alone.
Always re-read live `timing-defense-workspace` HEAD first.
Live remote wins over memory/chat/handoff.

## Current executable checkpoint
- architecture: Cloudflare Workers + Durable Objects
- last validated executable: v0.45 SIEGER FULL PASS
- deployment branch: `timing-defense-cloudflare-do-poc`
- validated deployment HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health: `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

---

# CRITICAL CURRENT DIRECTION

The project is in a **Master Campaign Progression Spine** phase.

Do NOT resume:
- T1 encounter micro-sim
- exact T1 recipe tuning
- Lv11+ live implementation
- old Stage4→10 reconstruction
- production monster-number freeze
- detailed 3P/4P expansion
until the Master Campaign Matrix is aligned.

Primary current authority:
`legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

Required order:

```text
master spine
 -> campaign matrix
 -> monster availability / novelty
 -> 50-Stage macro flow
 -> player power spine
 -> meta-power states
 -> difficulty envelope
 -> encounter authoring
 -> deterministic simulation
 -> explicit freeze
 -> implementation
```

---

# Read first
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
12. older T1/encounter documents only as reference

---

# User-confirmed core progression

## Class / Tier
- five classes progress through Tiers independently
- same Tier/Stage content is shared by all classes
- class-specific ease/difficulty differences are intentional
- hard class lockout is forbidden
- recoverable soft progression walls are desirable

## Tier / Stars
- one Tier = 50 stages
- fail Stage1–19 = 0★
- fail Stage20–39 = 1★
- fail Stage40–49 = 2★
- clear Stage50 = 3★
- store bestStars only
- stars are non-spendable
- stars grant broad account-wide permanent growth

## Cross-class progression
Intended loop:

```text
Class A blocked
 -> progress B/C/D
 -> earn stars + achievements
 -> broad + targeted permanent growth
 -> return to A
 -> old soft wall becomes attainable
```

Achievements may include:
- class Tier milestones
- all-class Tier milestones
- pure SOLO / AI0 clear
- rewards that strengthen a different class

Exact reward graph/value remains OPEN until soft-wall data exists.

---

# NEW MASTER CAMPAIGN PRINCIPLE

Monster / skill / stars / achievements are not separate centers.
The central coordinate is:

```text
Tier × Stage1..50 × Content Novelty × Player Power × Meta Progression
```

Use progressive deepening:
- align whole campaign shallowly first
- close the most upstream dependencies
- only then increase numeric/detail precision

Do not precision-tune a lower layer while its upstream premise is still changing.

---

# Monster progression — USER CONFIRMED

## Current 9 are not the final lifetime roster
Current mechanical roster:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

But campaign structure must remain expandable.

Rules:
- do NOT force all 9 into Tier1
- higher Tiers should introduce new monster archetypes
- reaching a new Tier should provide actual content novelty
- returning monsters can gain new role through composition/formation/cadence
- future monsters may be added beyond the current 9
- no schema/code assumption `monsterCount == 9`
- MonsterRegistry/versioned availability should be used
- pressure taxonomy may expand/version if a future monster does not fit existing families

This direction supersedes the active use of the old `T1 teaches all 9` candidate premise.

---

# Parked historical candidates

Keep for evidence/reuse, but DO NOT continue them as active campaign authority:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

Reason:
They assume all current 9 ordinary monsters are taught inside Tier1.
That premise is no longer the active campaign direction.

Do not delete their useful calculations; reuse only after the new unlock ladder is defined.

---

# Difficulty target — USER CONFIRMED

General Tier calibration rule:

> **intended-entry `SKILLED_V2` full-Tier Stage1→50 clear probability should normally be below 60%.**

Interpretation:
- 60% is an upper bound, not a target midpoint
- Tier1 may be higher because it is onboarding / first contact
- this is full Tier 3★ clear probability, not individual Stage pass rate
- evaluate at the expected account state when that Tier is first seriously attempted
- do not apply the same threshold to overgrown replay accounts
- class-specific clear rates may differ
- some classes may be substantially below 60% to create recoverable soft walls

## Skilled profile must be stronger than prior simulator assumptions
User calibration evidence:
- combo 40 is easy to reach with concentration
- current prototype stages felt much too easy

Therefore `SKILLED_V2` must:
- treat combo 40 as achievable skilled play, not high-mastery-only
- use stronger combo maintenance/timing/heavy-completion assumptions than old skilled
- keep `HIGH_MASTERY_STRESS` as a separate upper profile

Exact PERFECT/GOOD/NORMAL distributions and combo survival probabilities are still OPEN and must be parameterized from testing rather than guessed/frozen.

---

# Current Master Campaign Matrix task

Exact next tranche:

1. compare Tier count candidates 4 / 5 / 6
2. define novelty budget for each Tier
3. distribute current 9 monsters across Tier availability/unlock candidates
4. define future-monster expansion contract/slots
5. define each Tier's 50-Stage macro flow
6. align expected Lv6/11/16/21/26/31 reach windows
7. define meta-power profiles:
   - P0 FRESH
   - P1 BALANCED
   - P2 STAR_GROWN
   - P3 ACHIEVEMENT_ASSISTED
8. define Tier-specific SKILLED_V2 clear-rate envelopes
9. static cross-audit novelty × monsters × skills × stars × achievements × difficulty
10. only after PASS resume encounter frequency/count/composition/cadence authoring

---

# Player skill authority truth
- Lv6 = current authoritative
- Lv11/Lv16/Lv21 = exact legacy parity candidates
- Lv26 = designed-not-authoritative
- Lv31 = unresolved

These remain parked from live implementation, but their expected reach windows must be modeled in the Master Campaign Matrix.

---

# Handoff discipline

When a work group closes, synchronize:
- `PROJECT_STATUS.md`
- `NEXT_WORK.md`
- `SESSION_HANDOFF.md`
- relevant corpus docs

Always record:
- live canonical HEAD
- executable checkpoint
- active structure tranche
- user-confirmed decisions
- parked/superseded candidates
- open decisions
- exact next boundary
- whether live code/numbers changed

Current tranche changes structure documents only; no live gameplay or production balance values have been changed.
