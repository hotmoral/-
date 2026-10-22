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
4. `legacy-game-structure/09_TIER_LADDER_CANDIDATE_V0_1.md`
5. `legacy-game-structure/10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
6. `legacy-game-structure/12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
7. `legacy-game-structure/13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
8. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
9. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
10. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
11. `MONSTER_CAPABILITY_CONTRACT_V1.md`

---

# Closed combat/network foundations
- v0.36: exact EXP/N2/Lv6 authority — PASS.
- v0.38: 512-event multiplayer/reconnect kernel — PASS.
- v0.39: N3 frozen and authoritative — PASS.
- v0.40–v0.45: SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER capability authority — FULL PASS.
- Stage1–3 are regression fixtures only, not final campaign recipes.

Nine ordinary archetypes:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Production monster coefficients remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately approved.

---

# Meta progression — current structural truth

## Independent class progression
Knight / Rogue / Tank / Archer / Mage each own independent Tier progression.

## Tier/star rule
Each Tier = 50 stages.

Attempt result:
- fail Stage 1–19 -> 0★
- fail Stage 20–39 -> 1★
- fail Stage 40–49 -> 2★
- clear Stage 50 -> 3★

Derived invariant:
`bestStars[class][tier] = max(previous, attemptStars)`.
Repeated attempts do not farm stars beyond 3★ per class/Tier.

## Global permanent progression
`GlobalStarTotal = sum(bestStars)`.
Stars are non-spendable achievement progression.
Cumulative stars automatically grant account-wide permanent stats applied to all classes.

Open:
- permanent reward thresholds/coefficients,
- exact Tier unlock semantics,
- multiplayer Tier eligibility/credit.

---

# Encounter taxonomy — current structure
Old S/E/X is historical analysis only.

Current vocabulary:
- BASELINE neutral reference
- FLOOD
- RUSH
- BULWARK
- BREACH
- AERIAL
- REPLICATE
- SUPPORT
- SIEGE

Encounter authoring also owns:
- monster count/frequency,
- archetype composition,
- formation/frontline intent,
- spawn order,
- cadence,
- geometry,
- active concurrency,
- target reorder,
- frontline block time,
- backline exposure/capability uptime.

Front/mid/back authoring metadata does **not** override runtime target authority.

---

# Structure consistency governance — ACTIVE
Canonical corpus governance:
`legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`

Required lenses for each tranche:
- product purpose,
- internal consistency,
- cross-category dependencies,
- player learning/readability,
- core target/formation truth,
- class fairness,
- progression/economy snowball,
- multiplayer implications,
- authority boundary,
- deterministic simulation,
- scope/cost control.

Key cross-category gates:
- Tier unlock,
- permanent stat ladder,
- shop cadence,
- EXP/skill reach,
- boss/checkpoint policy,
- multiplayer Tier progression.

---

# First Tier ladder candidate
First full-campaign simulation uses a **5-Tier candidate spine**, not a final Tier-count freeze.

Why Tier count must be simulated:
- minimum successful class-stage volume = `250T`,
- maximum stars = `15T`.

Candidate identities:
- T1 Vocabulary / Field Reading
- T2 Frontline / Breakthrough
- T3 Tempo / Population Shift
- T4 Formation / Objective Pressure
- T5 Mastery / Contrast

Final Tier count/name/order remains OPEN.

---

# T1 structural skeleton — V0.2 PASS
Active candidate:
`legacy-game-structure/13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`

V0.1 was statically audited before revision.

V0.2 properties:
- 9 ordinary capabilities all first taught by Stage26,
- no new core ordinary capability Stage40+,
- 61 encounter occurrences,
- C0 4 / C1 19 / C2 27 / C3 9 / C4 2,
- C0–C2 = 82.0%,
- C4 only Stage49/50,
- SIEGE Stage presence 12 -> 9 versus V0.1,
- SIEGE Stage26~30 five-stage run removed,
- SPLITTER Stage20~22 repetition removed,
- late exam reduced from constant synergy toward focused extremes + selected synergy.

Remaining WATCH:
- BULWARK 19/50 Stage presence,
- Stage20–26 learning density,
- T1 FORTRESS necessity,
- first-class/no-permanent-stat late survivability,
- future geometry-driven class opportunity coverage.

Status: **STRUCTURAL PASS / NUMERIC NOT READY FOR PRODUCTION**.

---

# Player skill authority
- Lv6 — FROZEN+AUTHORITATIVE.
- Lv11/Lv16/Lv21 — exact legacy parity candidates.
- Lv26 — DESIGNED_NOT_AUTHORITATIVE.
- Lv31 — OPEN/UNRESOLVED.

Parity implementation remains parked behind the structure phase.
Late campaign simulation must later include higher-skill candidate modes; Lv6-only calibration is insufficient.

---

# Current exact work boundary
Do not:
- resume legacy Stage4→10 reconstruction,
- start Lv11+ live implementation,
- freeze production monster numbers,
- author all five Tiers numerically at once.

Next bounded tranche:
**T1 2-player candidate numeric authoring envelope**.

Order:
1. authored monster-count ranges per used encounter archetype,
2. effective entity count including SPLITTER children,
3. cadence buckets,
4. concrete formation IDs / arrival-order intent,
5. static peak/4s/6s density calculation,
6. encounter micro-simulation,
7. 10-stage synthetic slice,
8. full T1 simulation only after micro/slice pass,
9. then 3P/4P expansion.

## Governance
`recover -> structure -> static audit -> candidate data -> simulate -> classify -> report -> discuss -> explicit freeze -> implement`.
