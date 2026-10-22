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
8. `legacy-game-structure/14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
9. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
10. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
11. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
12. `MONSTER_CAPABILITY_CONTRACT_V1.md`

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
- five classes progress through Tiers independently,
- 1 Tier = 50 stages,
- fail 1–19 -> 0★,
- fail 20–39 -> 1★,
- fail 40–49 -> 2★,
- clear 50 -> 3★,
- `bestStars[class][tier] = max(previous, attemptStars)`,
- `GlobalStarTotal = sum(bestStars)`,
- stars are non-spendable achievement progression,
- cumulative stars grant account-wide permanent stats.

Open:
- permanent reward ladder,
- Tier unlock semantics,
- multiplayer Tier eligibility/credit.

---

# Encounter structure
Old S/E/X is legacy analysis only.

Current vocabulary:
BASELINE neutral reference / FLOOD / RUSH / BULWARK / BREACH / AERIAL / REPLICATE / SUPPORT / SIEGE.

Encounter authoring tracks:
- monster count/frequency,
- composition,
- formation/frontline intent,
- spawn order,
- cadence,
- geometry,
- active concurrency,
- target reorder,
- frontline block time,
- backline exposure/capability uptime.

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
- player learning/readability,
- targeting/formation truth,
- class fairness,
- progression/economy snowball,
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

Remaining WATCH:
- BULWARK 19/50 Stage presence,
- Stage20–26 learning density,
- T1 FORTRESS necessity,
- first-class/no-permanent-stat survivability,
- class opportunity after geometry/count authoring.

---

# T1 2P Authoring Envelope V0.1 — SIMULATION CANDIDATE
Source:
`legacy-game-structure/14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

Completed:
- L/M/H/X candidate compositions for T1-used E01–E19,
- authored vs effective entity count separation,
- SPLITTER child-volume accounting,
- conservative single-SUPPORTER/single-SIEGER T1 package policy,
- cadence IDs CD01–CD08,
- formation IDs F01–F09,
- first static readability alert envelope.

Historical old 5-monster 2P reference:
- P95 4s spawn ≈11,
- P95 6s ≈13.5.

New T1 candidate analysis targets:
- authored 4s normal <=8 / WATCH 9–10 / warning >10,
- effective 4s normal <=10 / WATCH 11–13 / warning >13,
- peak active target mostly 6–8 / WATCH 9–10 / stress 11+.

These are simulator/authoring alerts, not production hard caps.

Key guardrails:
- T1 E10/E11/E18/E19 default one SIEGER package,
- T1 E09/E12/E16/E19 default one SUPPORTER package,
- E19 Stage49/50 starts L/M despite C4 complexity,
- SPLITTER X packages remain stress-only until micro-sim.

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
- assign exact recipes to all 50 stages yet,
- expand to 3P/4P yet.

Next bounded tranche:
**T1 representative encounter micro-simulation preflight**.

Order:
1. E01–E19 allowed formation/cadence matrix,
2. representative L/M/H recipe set,
3. deterministic spawn schedules,
4. static authored 4s/6s density,
5. SPLITTER child burst stress,
6. screen/arrival-order model for E11/E12/E17/E18/E19,
7. SIEGER screened first-shot/shot-uptime analysis,
8. SUPPORTER screened aura analysis,
9. CHARGER telegraph concurrency analysis,
10. revise candidate envelope,
11. then 10-stage synthetic slice.

## Governance
`recover -> structure -> static audit -> candidate data -> micro-sim -> synthetic slice -> full Tier sim -> report -> explicit freeze -> implement`.
