# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed implementation gates
1. Cloudflare DO PoC — **PASS**
2. v0.31/v0.32 waiting room — **PASS**
3. v0.33 Stage1 authority — **PASS**
4. v0.34 render/remote projectile parity — **PASS**
5. v0.35 reconnect/Team Shop/Stage2 — **PASS**
6. v0.36 N1/N2 + Lv6 — **FULL PASS**
7. v0.37 Stage3 + BRUTE regression fixture — **FULL PASS**
8. v0.38 larger-party/event kernel — **FULL PASS**
9. v0.39 N3 — **FULL PASS**
10. Monster Capability Foundation V1 — **PASS**
11. v0.40 SHIELD — **FULL PASS**
12. v0.41 FLYER — **FULL PASS**
13. v0.42 CHARGER — **FULL PASS**
14. v0.43 SPLITTER — **FULL PASS**
15. v0.44 SUPPORTER — **FULL PASS**
16. v0.45 SIEGER — **FULL PASS**
17. Player Skill Authority Review — **COMPLETE**
18. Legacy Game Structure Corpus foundation — **COMPLETE**
19. T1 structural skeleton V0.2 — **STRUCTURAL PASS / NUMERIC NOT FROZEN**

## Exact latest executable checkpoint
- branch `timing-defense-cloudflare-v045-sieger-pass-20261022`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- live run/job `39725993894` / `119649887564`

No gameplay/numerical implementation has been authorized after v0.45.
Stage1–3 remain regression fixtures only.
Do not reconstruct legacy Stage4→10 as production content.

---

# ACTIVE PHASE — Structure-first campaign authoring/calibration

Primary corpus:
`legacy-game-structure/`

Read in order:
1. `README.md`
2. `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
3. `01_META_PROGRESSION.md`
4. `02_TIER_SYSTEM.md`
5. `03_STAGE_STRUCTURE_50.md`
6. `04_MONSTER_ENCOUNTER_MODEL.md`
7. `10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
8. `09_TIER_LADDER_CANDIDATE_V0_1.md`
9. `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
10. `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
11. `06_SIMULATION_CALIBRATION_PLAN.md`
12. `07_AUTHORING_DATA_SCHEMA.md`
13. `05_LEGACY_EVIDENCE_MAP.md`

---

# Closed structural decisions

## Meta progression
- 5 classes progress through Tiers independently.
- 1 Tier = 50 stages.
- fail 1–19 -> 0★.
- fail 20–39 -> 1★.
- fail 40–49 -> 2★.
- clear 50 -> 3★.
- repeated attempts preserve `bestStars[class][tier]`, max 3★.
- `GlobalStarTotal = sum(bestStars)`.
- stars are non-spendable account achievement progression.
- cumulative stars automatically grant account-wide permanent stats.

Exact permanent-stat reward ladder remains OPEN.
Tier unlock and multiplayer Tier eligibility remain OPEN.

## Encounter taxonomy
Old S/E/X is legacy analysis only.
Current authoring vocabulary:
- BASELINE neutral reference
- FLOOD
- RUSH
- BULWARK
- BREACH
- AERIAL
- REPLICATE
- SUPPORT
- SIEGE

Encounter authoring must model composition + formation + spawn order + cadence + geometry + concurrency + target order + capability uptime.

## Complexity
- C0 baseline
- C1 single mechanic
- C2 dual readable
- C3 synergy
- C4 multi-state high complexity

Complexity is not equal to difficulty.
Higher Tier must not become constant C3/C4 chaos.

---

# First Tier ladder candidate

First full-campaign simulation spine uses **5 Tier as a bounded candidate only**.
This is NOT final Tier-count freeze.

Reason:
`5 classes × T tiers × 50 stages = 250T minimum successful stage completions`
`MaxStars = 15T`

Candidate identities:
- T1 Vocabulary / Field Reading
- T2 Frontline / Breakthrough
- T3 Tempo / Population Shift
- T4 Formation / Objective Pressure
- T5 Mastery / Contrast

Final Tier count/name/order remains OPEN and must be checked against total progression length and star reward ladder.

---

# T1 structural candidate V0.2 — current active baseline

Source:
`legacy-game-structure/13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`

Key properties:
- all 9 ordinary monster capabilities first taught by Stage26,
- Stage40+ introduces no new core ordinary capability,
- 61 encounter occurrences across 50 stages,
- complexity distribution: C0 4 / C1 19 / C2 27 / C3 9 / C4 2,
- C0–C2 = 82.0%,
- C4 only Stage49/50,
- V0.1 SIEGE 5-stage consecutive run removed,
- SIEGE Stage presence reduced 12 -> 9,
- SPLITTER three-stage teaching repetition removed,
- Stage40–49 final exam uses focused extremes as well as selected synergy.

Remaining WATCH:
- BULWARK stage presence 19/50,
- cognitive load from SPLITTER/SUPPORTER/SIEGER teaching during Stage20–26,
- whether FORTRESS belongs in T1 Stage49/50,
- first-class/no-permanent-stat late-stage survivability,
- class-opportunity coverage once geometry/count data exists.

---

# EXACT NEXT BOUNDARY

Do **not** continue directly to live implementation.
Do **not** freeze production monster numbers.
Do **not** author all five Tiers numerically at once.

Next bounded tranche is **T1 candidate numeric authoring envelope**, in this order:

1. define 2-player baseline authored count ranges for E01–E19 used by T1,
2. separately compute effective entity counts including SPLITTER children,
3. define candidate cadence buckets (not production freeze),
4. define concrete formation IDs / intended arrival order,
5. calculate static peak/burst-density envelopes before combat simulation,
6. run encounter micro-simulation on representative pairs/synergies,
7. correct structure/count/cadence defects,
8. build a 10-stage synthetic slice,
9. only then run full T1 50-stage simulation,
10. only after T1 stabilizes expand to 3P/4P and later Tiers.

## Required review every tranche
Use `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md` and check:
- product purpose
- internal consistency
- cross-category impact
- player learning/readability
- targeting/formation truth
- class fairness
- meta/economy snowball
- multiplayer implications
- authority boundary
- simulation determinism
- scope/cost control

## Parked behind structure phase
- Lv11/Lv16/Lv21 server parity implementation
- Lv26/Lv31 production contract
- permanent stat coefficients
- Tier unlock semantics
- multiplayer Tier eligibility
- shop cadence
- boss cadence

## Governance
`recover -> structure -> static audit -> candidate data -> simulate -> classify -> report -> discuss -> explicit freeze -> implement`.
