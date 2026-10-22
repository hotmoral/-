# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Canonical recovery rule
Always re-read live `timing-defense-workspace` HEAD first.
Live remote wins over memory/chat/handoff.

## Current executable checkpoint
- last validated executable: v0.45 SIEGER FULL PASS
- deployment HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health: `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

---

# CRITICAL CURRENT DIRECTION

The project is in a **Master Campaign Progression Spine / Master Campaign Matrix** phase.

Primary current docs:
1. `legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
2. `legacy-game-structure/17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
3. `legacy-game-structure/19_MODEL_A_B_CLASS_ROLE_AND_VOLUME_AUDIT_V0_1.md`
4. `legacy-game-structure/18_MONSTER_ROSTER_EXTENSIBILITY_AMENDMENT_2026-10-22.md`
5. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
6. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
7. `legacy-game-structure/02_TIER_SYSTEM.md`
8. `legacy-game-structure/01_META_PROGRESSION.md`

Do not resume detailed T1 monster-count/cadence work until this spine is closed.

---

# User-confirmed progression truth

- 5 classes progress independently through Tiers.
- Same Tier/Stage combat content is shared by all classes.
- Tier = 50 Stage.
- fail 1–19 = 0★; fail 20–39 = 1★; fail 40–49 = 2★; Stage50 clear = 3★.
- stars = broad account-wide permanent growth.
- achievements = targeted cross-class progression.
- a class may hit a recoverable soft wall.
- other-class stars/achievements should help that class later.
- hard class lockout is forbidden.

---

# Master Campaign principle

Central coordinate:

```text
Tier × Stage1..50 × Content Novelty × Player Power × Meta Progression
```

Use progressive deepening:
1. align whole campaign shallowly
2. close upstream dependencies
3. add candidate detail
4. simulate
5. revise the spine
6. only then increase precision

---

# Monster progression — USER CONFIRMED

Current mechanically-authoritative V1 set:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Important interpretation:
- V1 roster = fixed current capability foundation
- lifetime/final roster cap = NOT fixed

Canonical clarification:
`18_MONSTER_ROSTER_EXTENSIBILITY_AMENDMENT_2026-10-22.md`

Rules:
- do not force all 9 into T1
- higher Tiers should introduce new monster archetypes
- new Tier entry should deliver real content novelty
- returning monsters can be reinterpreted by formation/composition/cadence
- T5/T6/T7... future expansion remains open
- no `monsterCount==9` hardcoding
- MonsterRegistry / Tier availability are versioned
- taxonomy may expand if future capabilities need new pressure language

---

# Difficulty target — USER CONFIRMED

General non-T1 target:

> intended-entry `SKILLED_V2` full-Tier Stage1→50 clear probability should normally be **below 60%**.

Interpretation:
- 60% is an upper bound
- T1 may be easier
- measure full Tier 3★ clear probability
- evaluate at the expected progression state for first serious Tier attempts
- do not use overgrown replay accounts for this gate
- class clear rates may differ
- soft-wall classes may be far lower

## Skilled profile reset
- combo 40 should be achievable skilled play, not high-mastery-only
- stronger combo maintenance/timing/heavy-completion than old skilled
- HIGH_MASTERY_STRESS remains a separate upper profile
- exact timing/combo probabilities remain OPEN until measured

---

# Master Campaign Matrix V0.1

## Model A — preferred test hypothesis
**4 initial Tiers + open-ended T5+ expansion**

- T1: GRUNT / RUNNER / BRUTE
- T2: +SHIELD / +FLYER
- T3: +CHARGER / +SPLITTER
- T4: +SUPPORTER / +SIEGER
- T5+: future monster/content expansion

## Model B — fallback
5 initial Tiers:
- T1 G/R/B
- T2 +SH/F
- T3 +C/SP
- T4 +SUP
- T5 +SI
- T6+ future

## 6-Tier model
Currently low priority with the current 9-monster roster because of campaign-length and novelty-starvation risk.

---

# Model A/B audit result

Canonical audit:
`19_MODEL_A_B_CLASS_ROLE_AND_VOLUME_AUDIT_V0_1.md`

Key results:
- T1 with G/R/B can still support all 5 class roles through formation/cadence authoring.
- T2 role coverage is naturally strong.
- T3 strongly rewards Tank/Mage; returning BRUTE/SHIELD should preserve Rogue durable-target value.
- T4 strongly rewards Tank/Archer; Rogue/Mage value must be preserved through durable screens/cluster formations.
- SUPPORTER + SIEGER in the same T4 is a **WATCH, not FAIL**.

T4 learning-density mitigation:
```text
1–9   returning formation recap
10    checkpoint
11–19 SUPPORTER teach/mix
20    first gate
21–29 SIEGER teach/mix
30    synthesis checkpoint
31–39 combined formation/objective pressure
40–49 mastery
50    final
```

If this proves too dense in simulation/playtest, use Model B and split SIEGER into T5.

---

# Play-volume sensitivity

Rough geometric comparison only, assuming eventual 3★ on all class×Tier records:

| full-clear q | 4 Tier | 5 Tier | 6 Tier |
|---:|---:|---:|---:|
| .59 | 33.9 attempts | 42.4 | 50.9 |
| .50 | 40.0 | 50.0 | 60.0 |
| .40 | 50.0 | 62.5 | 75.0 |

This is not production prediction because fail Stage and meta growth vary.
It demonstrates that one extra Tier is expensive under the desired difficulty.

---

# Parked historical candidates

Do not continue as active authority:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

Reason: old assumption that T1 teaches all current 9 monsters.
Preserve for reusable analysis only.

---

# Run skill-power spine candidate

Exact EXP curve remains open.
Desired relative reach:
- Lv6 early
- Lv11 early-mid
- Lv16 mid
- Lv21 mid-late
- Lv26 late
- Lv31 final/mastery band

Legacy pacing that reaches Lv21 around old Stage10 cannot be assumed final for a 50-Stage run.

---

# Meta-power scenario profiles

- P0 FRESH
- P1 BALANCED
- P2 STAR_GROWN
- P3 ACHIEVEMENT_ASSISTED
- OVERGROWN replay/stress

Candidate coverage:
- T1 primarily P0
- T2 P0–P1
- T3 P1–P2
- T4 P1–P3
- T5+ P2–P3/future

---

# Exact next boundary

Use Model A as the default test hypothesis, not a freeze.

Next:
1. define novelty budget for T1–T4 beyond monster count
2. place boss novelty placeholders
3. refine relative skill-reach bands
4. audit monster-novelty vs skill-novelty collisions
5. define SKILLED_V2 parameter measurement plan
6. estimate stars/soft-wall progression play volume
7. static audit Model A campaign matrix
8. if PASS, choose Model A as bounded simulation spine
9. if T4 overload FAIL, switch to Model B
10. only then resume encounter frequency/count/composition/cadence

Do not yet freeze:
- initial Tier count
- exact monster unlock points
- production monster coefficients
- star reward coefficients
- achievement reward graph/value
- shop cadence
- boss cadence
- Lv11+ live implementation

---

# Handoff discipline

New session must:
1. check live branch HEAD
2. read this handoff
3. read PROJECT_STATUS / NEXT_WORK
4. read Master Spine + Matrix + Model audit + Governance
5. verify no newer remote changes

Current tranche changed planning/corpus docs only.
No live gameplay code or production balance number was changed.
