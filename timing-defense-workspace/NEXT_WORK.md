# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# ACTIVE PHASE — Master Campaign Spine

Read first:
1. `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
2. `legacy-game-structure/17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
3. `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
4. `legacy-game-structure/19_MODEL_A_B_CLASS_ROLE_AND_VOLUME_AUDIT_V0_1.md`
5. `legacy-game-structure/18_MONSTER_ROSTER_EXTENSIBILITY_AMENDMENT_2026-10-22.md`
6. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
7. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
8. `legacy-game-structure/02_TIER_SYSTEM.md`
9. `legacy-game-structure/01_META_PROGRESSION.md`

---

# User-confirmed structural direction

- same Tier/Stage content across all classes
- independent class progression
- recoverable soft walls allowed
- hard class lockout forbidden
- stars = broad permanent growth
- achievements = targeted cross-class growth
- current 9 monsters are not lifetime final roster
- T1 should not force all 9
- higher Tiers should introduce new monsters
- future monster/Tier expansion must remain open
- Lv31 must be obtained early enough to be used and enjoyed across multiple late-run Stages before Stage50
- **Lv31 target unlock window = Stage41–45**

---

# Difficulty target

General non-T1:

> intended-entry `SKILLED_V2` full-Tier Stage1→50 clear probability <60%.

- 60% is upper bound
- T1 may be higher
- overgrown replay excluded
- class clear rates may differ
- combo 40 must be treated as achievable skilled play, not extreme mastery

---

# Current campaign-model result

## Model A — preferred test hypothesis
**4 initial Tiers + open-ended T5+ expansion**

- T1: GRUNT / RUNNER / BRUTE
- T2: +SHIELD / +FLYER
- T3: +CHARGER / +SPLITTER
- T4: +SUPPORTER / +SIEGER
- T5+: future monster/content expansion

Class-role audit result:
- T1 can support all 5 class roles through formations even with 3 monsters
- T2 role coverage strong
- T3 Tank/Mage naturally spike; maintain returning BRUTE/SHIELD for Rogue value
- T4 Knight/Tank/Archer strong; Rogue/Mage opportunities preserved through durable screens/clusters
- T4 SUPPORTER+SIEGER learning density = WATCH, not FAIL

T4 mitigation:
- SUPPORTER teach in one window
- SIEGER teach later
- combined synergy only after both are learned

## Model B — fallback
5 initial Tiers:
- T4 +SUPPORTER
- T5 +SIEGER

Use if Model A T4 learning-density testing fails.

---

# Lv31 mastery play-window — REQUIRED GUARDRAIL

Canonical:
`legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`

User-confirmed:
- Lv31 is not a Stage50-only reward.
- **target unlock window = Stage41–45.**
- Stage46–49 should provide repeated real-use/mastery opportunities.
- Stage50 should be final application of an already-familiar Lv31 skill.

Structural consequence:
- Stage41–45 is the unlock-transition band.
- Stage46–49 is the explicit post-Lv31 mastery-use band.
- Stage50 is not the Lv31 tutorial.

Failure conditions:
- intended-entry skilled distribution drifts materially beyond Stage45
- Lv31 first meaningful use occurs at Stage49/50
- Lv31 power spike trivializes the final band
- Lv26 use window is compressed away

Exact EXP formula and percentile cutoffs remain OPEN.

---

# Play-volume sensitivity

If all class×Tier records are eventually 3★ and full-clear probability q is treated as a simple constant for rough comparison:

- q=.59: 4 Tier ~33.9 full attempts / 5 Tier ~42.4 / 6 Tier ~50.9
- q=.50: 4 Tier 40 / 5 Tier 50 / 6 Tier 60
- q=.40: 4 Tier 50 / 5 Tier 62.5 / 6 Tier 75

This is comparison only, not production prediction.
It confirms that adding a Tier is expensive under the desired difficulty.

---

# PARKED

Do not continue as active authority:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

Reason: old T1-all-9 premise.

---

# Exact next boundary

Use Model A as the **default test hypothesis**, not a freeze.

Next:
1. define novelty budget per T1–T4 beyond monster count
2. place boss novelty placeholders
3. refine relative Lv6/11/16/21/26/31 reach bands around the fixed Lv31 Stage41–45 target window
4. explicitly preserve meaningful Lv26 play window before Lv31
5. reserve Stage46–49 as post-Lv31 mastery-use territory
6. audit skill-novelty collision by Tier/Stage band
7. define SKILLED_V2 parameter-measurement plan
8. estimate progression/play volume under stars/soft walls
9. static audit Model A campaign matrix
10. if PASS, choose Model A as bounded simulation spine
11. if T4 overload FAIL, switch to Model B
12. only then reopen encounter frequency/count/composition/cadence

No production values freeze yet.
