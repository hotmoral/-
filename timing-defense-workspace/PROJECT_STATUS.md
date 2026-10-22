# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# Current planning authority

Active phase:
**Master Campaign Progression Spine / Master Campaign Matrix**

Primary docs:
- `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `legacy-game-structure/17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
- `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
- `legacy-game-structure/19_MODEL_A_B_CLASS_ROLE_AND_VOLUME_AUDIT_V0_1.md`
- `legacy-game-structure/18_MONSTER_ROSTER_EXTENSIBILITY_AMENDMENT_2026-10-22.md`
- `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
- `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`

---

# Core structural truth

- 5 classes progress through Tiers independently.
- Same Tier/Stage content is shared across classes.
- 1 Tier = 50 Stage.
- 0/1/2/3★ boundaries remain 1–19 / 20–39 / 40–49 / Stage50 clear.
- stars = broad account growth.
- achievements = targeted cross-class growth.
- recoverable soft walls are intentional.
- hard class lockout forbidden.
- Lv31 must have a meaningful multi-Stage play window before Stage50.
- **Lv31 target unlock window is Stage41–45.**

---

# Monster campaign direction

Current 9 mechanically-authoritative ordinary monsters remain stable V1 IDs/roles.
But they are not the lifetime final roster.

- T1 should not contain all 9 by default.
- Higher Tiers should introduce new monster types.
- Future T5/T6/T7... expansion must remain open.
- MonsterRegistry/Tier availability is versioned.
- `monsterCount==9` hardcoding is forbidden.
- pressure taxonomy may version-up for new capabilities.

Interpretation of V1 roster freeze is clarified by:
`18_MONSTER_ROSTER_EXTENSIBILITY_AMENDMENT_2026-10-22.md`.

---

# Difficulty target

General non-T1 target:

> intended-entry `SKILLED_V2` full-Tier clear probability <60%.

- 60% upper bound
- T1 can be easier
- overgrown replay excluded
- class rates may differ
- combo 40 = achievable skilled play, not high-mastery-only

---

# Current campaign candidate ranking

## Model A — preferred test hypothesis
4 initial Tiers + T5+ expansion.

- T1 G/R/B
- T2 +SH/F
- T3 +C/SP
- T4 +SUP/SI
- T5+ future content

Class-role audit: structurally viable.
T4 SUPPORTER+SIEGER learning density = WATCH, not FAIL.
Use separated teaching windows and late synergy.

## Model B — fallback
5 initial Tiers, splitting SUPPORTER and SIEGER across T4/T5.
Use if Model A T4 overload fails testing.

6 initial Tiers currently low priority because campaign length and novelty starvation risk are high with the current roster.

---

# Run skill-power spine — Lv31 structural window

Exact EXP curve remains open.

User-confirmed requirement:
- Lv31 should not unlock only at the very end.
- **Lv31 target unlock window = Stage41–45.**
- Stage46–49 should provide repeated post-unlock use/mastery opportunities.
- Stage50 should test an already-familiar Lv31 skill, not introduce it.

Structural interpretation:
- Stage41–45 = Lv31 acquisition-transition band
- Stage46–49 = explicit Lv31 mastery-use band
- Stage50 = final application

Simulation must detect:
- unlock distribution drifting materially beyond Stage45
- insufficient post-Lv31 play window
- Lv31 power cliff that trivializes late stages
- class clear-rate divergence caused by unequal Lv31 power
- Lv26 window being compressed away

Canonical detail:
`legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`.

Exact EXP formula and percentile acceptance cutoffs are not frozen.

---

# Parked old candidates

- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

They assumed T1 teaches all 9 current monsters.
Retain as evidence only.

---

# Exact next work

1. define novelty budget for T1–T4
2. place boss novelty placeholders
3. refine Lv6/11/16/21/26 reach bands around the fixed Lv31 Stage41–45 target
4. preserve a meaningful Lv26 use window
5. reserve Stage46–49 for post-Lv31 mastery opportunities
6. audit skill novelty vs monster novelty collisions
7. define SKILLED_V2 measurement/parameter plan
8. estimate stars/soft-wall progression play volume
9. static audit Model A
10. if PASS, use Model A as bounded simulation spine
11. if T4 overload FAIL, switch to Model B
12. then resume encounter authoring

No production numbers are frozen.
