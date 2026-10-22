# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Current validated deployment
Primary architecture: **Cloudflare Workers + Durable Objects event-driven multiplayer**.

- public: `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- validated HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health: `0.45-cf.1`
- last executable checkpoint: **v0.45 SIEGER FULL PASS**
- checkpoint: `timing-defense-cloudflare-v045-sieger-pass-20261022`
- live run/job: `39725993894` / `119649887564`

No gameplay/numerical implementation has been authorized after v0.45.

---

# Current planning phase
The project is in a **structure-first campaign/meta authoring and calibration phase**.

Primary corpus:
`legacy-game-structure/`

Critical current documents:
1. `NEXT_WORK.md`
2. `legacy-game-structure/README.md`
3. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
4. `legacy-game-structure/01_META_PROGRESSION.md`
5. `legacy-game-structure/15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
6. `legacy-game-structure/09_TIER_LADDER_CANDIDATE_V0_1.md`
7. `legacy-game-structure/10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
8. `legacy-game-structure/13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
9. `legacy-game-structure/14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
10. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
11. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
12. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
13. `MONSTER_CAPABILITY_CONTRACT_V1.md`

---

# Closed implementation foundations
- v0.36 exact EXP/N2/Lv6 authority — PASS.
- v0.38 larger-party event/reconnect kernel — PASS.
- v0.39 N3 — PASS.
- v0.40–v0.45 monster capabilities — FULL PASS.

Nine ordinary archetypes:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Mechanical structure is authoritative.
Production monster coefficients remain provisional unless separately frozen.
Stage1–3 remain regression fixtures only.

---

# Meta progression structural truth

## Shared Tier content / independent class records
- same Tier/Stage authoring data is shared across all classes,
- each class has independent Tier progression and best-star records,
- class-specific difficulty differences are allowed,
- hard class lockout is forbidden,
- soft walls recoverable through cross-class progression are intentional.

## Stars — broad account growth
- 1 Tier = 50 stages,
- fail 1–19 -> 0★,
- fail 20–39 -> 1★,
- fail 40–49 -> 2★,
- clear 50 -> 3★,
- `bestStars[class][tier] = max(previous, attemptStars)`,
- `GlobalStarTotal = sum(bestStars)`,
- stars are non-spendable,
- cumulative stars grant broad account-wide permanent stats.

## Achievements — targeted cross-class growth
User-confirmed future direction:
- class-specific Tier milestone achievements,
- all-class Tier milestone achievements,
- class-specific pure SOLO / AI 0 Tier-clear achievements,
- some achievement rewards strengthen a **different class** from the source class.

Intended progression loop:
```text
Class A blocked
 -> progress other classes
 -> gain stars + achievements
 -> broad + targeted permanent growth
 -> return to A
 -> previous soft wall becomes attainable
```

Titles are the presentation/collection layer. Current structural default is gameplay reward on achievement completion and cosmetic title equip; title-equipped stats remain open.

Not frozen:
- achievement catalog,
- exact title names,
- sourceClass -> targetClass edges,
- stat type/value,
- stacking rules.

---

# Encounter structure
Old S/E/X is legacy analysis only.

Current vocabulary:
BASELINE / FLOOD / RUSH / BULWARK / BREACH / AERIAL / REPLICATE / SUPPORT / SIEGE.

Encounter authoring tracks composition, formation/frontline intent, spawn order, cadence, geometry, active concurrency, target reorder, frontline block time and backline/capability uptime.

Formation metadata does not override runtime target authority.
Complexity C0–C4 is separate from difficulty.

---

# Structure governance
Canonical:
`legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`

Required review lenses:
- product purpose,
- internal consistency,
- cross-category dependencies,
- learning/readability,
- target/formation truth,
- class asymmetry vs hard lockout,
- stars/achievement snowball,
- progression graph reachability,
- multiplayer implications,
- authority boundary,
- deterministic simulation,
- scope/cost control.

---

# Tier ladder candidate
First full-campaign simulation spine uses **5 Tier as a bounded candidate only**.

`minimum successful class-stage volume = 250T`
`maximum stars = 15T`

Candidate identities:
- T1 Vocabulary / Field Reading
- T2 Frontline / Breakthrough
- T3 Tempo / Population Shift
- T4 Formation / Objective Pressure
- T5 Mastery / Contrast

Final Tier count/name/order remains OPEN.

---

# T1 structural skeleton V0.2 — STRUCTURAL PASS
Source:
`legacy-game-structure/13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`

- last first-teach Stage26,
- no new core ordinary capability Stage40+,
- 61 encounter occurrences,
- C0 4 / C1 19 / C2 27 / C3 9 / C4 2,
- C0–C2 = 82.0%,
- C4 Stage49/50 only,
- V0.1 SIEGE/SPLITTER repetition issues corrected.

---

# T1 2P Authoring Envelope V0.1 — SIMULATION CANDIDATE
Source:
`legacy-game-structure/14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

Completed:
- L/M/H/X candidate compositions for E01–E19,
- authored vs effective entity count separation,
- SPLITTER child-volume accounting,
- conservative single-SUPPORTER/single-SIEGER T1 package policy,
- cadence IDs CD01–CD08,
- formation IDs F01–F09,
- first static readability alert envelope.

Candidate alerts:
- authored 4s normal <=8 / WATCH 9–10 / warning >10,
- effective 4s normal <=10 / WATCH 11–13 / warning >13,
- peak active mostly 6–8 / WATCH 9–10 / stress 11+.

Not production caps.

---

# Player skill authority
- Lv6 current authority.
- Lv11/Lv16/Lv21 exact legacy parity candidates.
- Lv26 designed-not-authoritative.
- Lv31 unresolved.

Parity implementation remains parked behind structure/calibration.

---

# Current exact work boundary
Do not:
- resume legacy Stage4→10 reconstruction,
- start Lv11+ implementation,
- freeze production monster numbers,
- freeze achievement reward values,
- assign exact recipes to all 50 stages yet,
- expand to 3P/4P yet.

Next bounded tranche:
**T1 representative encounter micro-simulation preflight**.

After micro-sim and T1 full simulation:
1. generate 5-class viability / soft-wall map,
2. simulate stars-only recovery,
3. place cross-class achievement edges only where progression structure benefits,
4. verify reward-graph reachability / circular deadlock / dominant route / snowball,
5. run stars + achievements combined account simulation,
6. only then discuss/freeze reward mappings and values.

## Governance
`recover -> structure -> static audit -> candidate data -> micro-sim -> synthetic slice -> full Tier sim -> soft-wall map -> cross-class reward model -> account sim -> report -> explicit freeze -> implement`.
