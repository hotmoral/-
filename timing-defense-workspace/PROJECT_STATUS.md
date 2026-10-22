# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Current validated deployment
- architecture: Cloudflare Workers + Durable Objects
- executable checkpoint: v0.45 SIEGER FULL PASS
- deployment HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health: `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

Stage1–3 remain regression fixtures only.

---

# Current planning phase

The project is now in a **Master Campaign Progression Spine** phase.

Primary document:
`legacy-game-structure/16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`

The current center is no longer T1 encounter micro-tuning.
First align:
- Tier count
- Tier novelty
- monster unlock ladder
- 50-Stage macro flow
- run skill reach
- meta-power state
- difficulty targets

Then return to encounter detail.

---

# Structural truth

## Shared content / independent class progress
- same Tier/Stage content for all classes
- Knight/Rogue/Tank/Archer/Mage keep independent Tier records
- class asymmetry allowed
- hard class lockout forbidden
- recoverable soft walls are intended

## Stars
- Tier = 50 stages
- fail 1–19 = 0★
- fail 20–39 = 1★
- fail 40–49 = 2★
- clear 50 = 3★
- bestStars only
- cumulative stars = broad account-wide permanent growth

## Achievements
- targeted cross-class progression
- some achievements may strengthen another class
- exact reward graph/value remains open until class soft-wall data exists

---

# Monster roster / campaign novelty direction

Current 9 ordinary monster capabilities are mechanically authoritative through v0.45:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Important current direction:
- these 9 are **not** the final lifetime roster
- Tier1 should not consume all 9 by default
- new monster archetypes should appear as Tiers rise
- later Tiers should also reinterpret existing monsters through new combinations/formations/cadence
- authoring/schema must allow future monster additions without redesigning the campaign model
- no fixed `monsterCount == 9` assumptions
- taxonomy may expand/version when future mechanics require it

Because of this, prior candidates that taught all 9 in T1 are PARKED:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

They remain evidence/reference only.

---

# Difficulty target — USER CONFIRMED

General campaign target:

> intended-entry `SKILLED_V2` full-Tier Stage1→50 clear probability should normally be **below 60%**.

Interpretation:
- 60% = upper bound, not midpoint
- T1 may be easier because it is the entry/onboarding Tier
- measure full Tier clear probability, not isolated Stage pass probability
- evaluate at the Tier's intended account progression state
- overgrown/replay accounts are separate
- class clear rates can differ
- low class rate can be an intentional recoverable soft wall

## Skilled profile reset
The old `skilled` simulation assumptions are too weak for the desired game.

New profile `SKILLED_V2`:
- combo 40 should be considered achievable skilled play
- stronger combo maintenance/timing/heavy completion than old skilled
- `HIGH_MASTERY_STRESS` remains a separate upper profile
- exact probabilities remain parameterized until measured

---

# Master Campaign Matrix — exact next work

1. compare 4/5/6 Tier campaign size candidates
2. define Tier novelty budgets
3. allocate current 9-monster availability/unlock candidates across Tiers
4. define future monster expansion contract
5. define Tier-by-Tier 50-Stage macro flow
6. align expected Lv6/11/16/21/26/31 reach windows
7. define meta-power profiles P0/P1/P2/P3
8. define Tier-specific SKILLED_V2 clear-rate envelopes
9. cross-audit all of the above
10. only then reopen monster frequency/count/composition/cadence work

---

# Player skill authority
- Lv6 current authoritative
- Lv11/Lv16/Lv21 exact legacy parity candidates
- Lv26 designed-not-authoritative
- Lv31 unresolved

Live parity implementation remains parked behind the campaign-structure phase.

---

# Governance

`master spine -> campaign matrix -> candidate authoring -> deterministic simulation -> classify -> report -> explicit freeze -> implementation`

No new production numbers are frozen by this status document.
