# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Canonical recovery rule
Always re-read live `timing-defense-workspace` HEAD first.
Live remote wins over memory/chat/handoff.

## Current executable checkpoint
- Cloudflare Workers + Durable Objects
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
3. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
4. `legacy-game-structure/02_TIER_SYSTEM.md`
5. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
6. `legacy-game-structure/01_META_PROGRESSION.md`
7. `legacy-game-structure/15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
8. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`

Do not immediately:
- resume T1 micro-sim
- tune exact monster counts/cadence
- implement Lv11+
- reconstruct legacy Stage4→10
- freeze production monster values
- expand detailed 3P/4P content

Required order:
`master spine -> campaign matrix -> candidate authoring -> deterministic simulation -> explicit freeze -> live implementation`.

---

# User-confirmed progression truth

## Class / Tier
- five classes progress independently through Tiers
- same Tier/Stage combat content is shared across all classes
- class asymmetry is allowed
- hard class lockout is forbidden
- recoverable soft walls are intended

## Stars
- Tier = 50 Stage
- fail 1–19 = 0★
- fail 20–39 = 1★
- fail 40–49 = 2★
- Stage50 clear = 3★
- bestStars only
- stars = broad account-wide permanent growth

## Achievements
- targeted cross-class progression
- class Tier / all-class Tier / pure SOLO AI0 etc.
- some achievements may permanently strengthen another class
- exact reward graph/value remains OPEN until soft-wall data exists

Intended loop:

```text
Class A blocked
 -> progress B/C/D
 -> earn stars + achievements
 -> broad + targeted permanent growth
 -> return to A
 -> old soft wall becomes attainable
```

---

# Master Campaign principle

Central coordinate:

```text
Tier × Stage1..50 × Content Novelty × Player Power × Meta Progression
```

Monster, skills, stars and achievements are not independent centers.
The campaign spine is the common coordinate system.

Work method:
- align the whole campaign shallowly first
- close upstream dependencies
- then increase lower-level precision
- simulate and revise the spine

Do not precision-tune downstream data while upstream premises are open.

---

# Monster progression — USER CONFIRMED

Current mechanically-authoritative ordinary set:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

But the current 9 are **not the final lifetime roster**.

Rules:
- do not force all 9 into T1
- higher Tiers should introduce new monster archetypes
- new Tier entry should provide actual content novelty
- returning monsters can gain new roles through formations/combinations/cadence
- future monsters can extend T5/T6/T7... or later campaign content
- no fixed `monsterCount == 9` assumption
- use versioned MonsterRegistry / Tier availability
- pressure taxonomy can version-up if a future capability requires it

Old T1-all-9 candidates are PARKED:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

Keep as evidence/reference; do not continue them as active authority.

---

# Difficulty target — USER CONFIRMED

Default non-T1 campaign target:

> **intended-entry `SKILLED_V2` full-Tier Stage1→50 clear probability should normally be below 60%.**

Interpretation:
- 60% is an upper bound, not target midpoint
- T1 may be easier because it is onboarding/first contact
- measure full Tier 3★ clear probability, not individual Stage pass rate
- evaluate at expected progression state when that Tier is first seriously attempted
- overgrown/replay accounts are separate
- class clear rates may differ
- some classes may intentionally be much lower and require cross-class progression recovery

## Skilled profile reset
Old skilled assumptions are too weak for the desired game.

`SKILLED_V2` must:
- treat combo 40 as achievable skilled play, not extreme mastery
- assume stronger combo maintenance/timing/heavy completion than old skilled
- keep `HIGH_MASTERY_STRESS` as a separate higher profile

Exact timing distributions/combo survival remain OPEN parameters pending measurement.

---

# Master Campaign Matrix V0.1

Tier-count comparison:

| Initial Tier count | Minimum successful class-stage volume | Max stars |
|---:|---:|---:|
| 4 | 1000 | 60★ |
| 5 | 1250 | 75★ |
| 6 | 1500 | 90★ |

Current ranking, NOT frozen:
1. **4 initial Tiers + open-ended T5+ expansion**
2. 5 initial Tiers + T6+ expansion
3. 6 initial Tiers = low priority with current 9-monster roster

## Model A — current front-runner
- T1: GRUNT / RUNNER / BRUTE
- T2: +SHIELD / +FLYER
- T3: +CHARGER / +SPLITTER
- T4: +SUPPORTER / +SIEGER
- T5+: future monster/content expansion

Risk:
- T4 learning density may be high because SUPPORTER + SIEGER are both stateful/backline-oriented.
- If this is too dense, Model B splits them across T4/T5.

## Model B
- T1 G/R/B
- T2 +SH/F
- T3 +C/SP
- T4 +SUP
- T5 +SI
- T6+ future

No unlock is frozen yet.

---

# 50-Stage macro grammar candidate

```text
1–9   Establish
10    Checkpoint A
11–19 Introduce & Mix
20    Star Gate A
21–29 Deepen
30    Checkpoint B
31–39 Pressure / Soft Wall
40    Star Gate B
41–49 Mastery Exam
50    Tier Final
```

Exact monster first appearance can move within the early/mid bands depending on Tier novelty budget.
Stage40+ should normally not introduce a core mechanic for the first time.

---

# Run skill-power spine candidate

Legacy EXP pacing is not assumed final for 50-stage campaign.
Desired relative progression, NOT exact Stage freeze:

- Lv6: early
- Lv11: early-mid
- Lv16: mid
- Lv21: mid-late
- Lv26: late
- Lv31: final/mastery band

Goal:
- class power novelty spans the 50-stage run
- major skill unlocks do not all happen in the opening 20%
- monster novelty and skill novelty do not overload the same band

---

# Meta-power profiles

- P0 FRESH
- P1 BALANCED
- P2 STAR_GROWN
- P3 ACHIEVEMENT_ASSISTED
- OVERGROWN replay/stress profile

Expected scenario coverage candidate:
- T1 mostly P0
- T2 P0–P1
- T3 P1–P2
- T4 P1–P3
- T5+ P2–P3/future

These are scenario coverage bands, not exact star thresholds.

---

# Exact next boundary

1. compare Model A vs Model B against all five class roles
2. define Tier novelty budgets beyond monster count
3. define boss novelty placeholders
4. refine relative skill-reach bands
5. define SKILLED_V2 parameter test plan
6. estimate play-volume under sub-60 clear target
7. compare repetition / soft-wall / meta-progression room
8. select one bounded campaign simulation spine
9. only then reopen encounter frequency/count/composition/cadence

Do not yet freeze:
- initial Tier count
- exact monster unlock points
- production monster coefficients
- star reward coefficients
- achievement reward graph/value
- shop cadence
- boss cadence
- Lv11+ implementation

---

# Handoff discipline

New session must:
1. check live branch HEAD
2. read this handoff
3. read PROJECT_STATUS / NEXT_WORK
4. read Master Spine + Matrix + Governance
5. verify no newer remote changes

When a group closes, sync:
- `PROJECT_STATUS.md`
- `NEXT_WORK.md`
- `SESSION_HANDOFF.md`
- active corpus docs

Current tranche changed planning/corpus docs only.
No live gameplay code or production balance number was changed.
