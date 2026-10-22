# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Current architecture
Primary lane: **Cloudflare Workers + Durable Objects event-driven multiplayer**.

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- validated HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`

Last executable checkpoint:
- **v0.45 SIEGER FULL PASS**
- branch `timing-defense-cloudflare-v045-sieger-pass-20261022`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- live run/job `39725993894` / `119649887564`

No gameplay/numerical implementation has been authorized after this checkpoint.

---

# Critical direction
The project is in a **structure-first campaign/meta authoring and calibration phase**.

Do not immediately:
- implement Lv11+,
- reconstruct legacy Stage4→10,
- freeze production monster numbers,
- promote old S/E/X recipes,
- numerically author all Tiers at once.

Required order:
`structure -> static consistency audit -> candidate authoring data -> deterministic simulation -> explicit freeze -> live implementation`.

---

# Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/README.md`
5. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
6. `legacy-game-structure/01_META_PROGRESSION.md`
7. `legacy-game-structure/02_TIER_SYSTEM.md`
8. `legacy-game-structure/03_STAGE_STRUCTURE_50.md`
9. `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`
10. `legacy-game-structure/10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
11. `legacy-game-structure/09_TIER_LADDER_CANDIDATE_V0_1.md`
12. `legacy-game-structure/12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
13. `legacy-game-structure/13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
14. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
15. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
16. `legacy-game-structure/05_LEGACY_EVIDENCE_MAP.md`
17. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
18. `MONSTER_CAPABILITY_CONTRACT_V1.md`

---

# Closed implementation foundations
- v0.36 exact EXP/N2/Lv6 authority — PASS.
- v0.38 event/reconnect/larger-party kernel — PASS.
- v0.39 N3 — PASS.
- v0.40–v0.45 monster capabilities — FULL PASS.

Nine ordinary archetypes:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Mechanical structure is authoritative; production coefficients remain provisional.
Stage1–3 are regression fixtures only.

---

# Meta progression truth

Five classes progress through Tiers independently.

One Tier = 50 stages.

Attempt star result:
- fail Stage 1–19 -> 0★
- fail Stage 20–39 -> 1★
- fail Stage 40–49 -> 2★
- clear Stage 50 -> 3★

Derived invariant:
`bestStars[class][tier] = max(previous, attemptStars)`.

`GlobalStarTotal = sum(bestStars)`.
Stars are non-spendable achievement progression.
Cumulative stars automatically grant account-wide permanent stats.

Open decisions:
- permanent reward track,
- next-Tier unlock,
- multiplayer Tier eligibility/credit.

---

# Encounter taxonomy truth

Old S/E/X = `LEGACY_ANALYSIS_REFERENCE` only.

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

Formation/front/mid/back is authoring intent, not a target override.
Actual targeting remains runtime system-driven/frontmost/validity based.

Complexity:
- C0 baseline
- C1 single mechanic
- C2 dual readable
- C3 synergy
- C4 multi-state high complexity

Complexity != difficulty.

---

# Governance now frozen for corpus work
Canonical:
`legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`

Every tranche must check:
- product purpose,
- internal consistency,
- cross-category dependencies,
- learning/readability,
- target/formation truth,
- class fairness,
- meta/economy snowball,
- multiplayer implications,
- authority boundary,
- simulation determinism,
- scope/cost control.

Cross-category decisions that cannot be made in isolation:
- Tier unlock,
- permanent stat ladder,
- shop cadence,
- EXP/skill reach,
- boss/checkpoint policy,
- multiplayer Tier progression.

---

# Tier ladder candidate
First bounded full-campaign simulation spine = **5 Tier candidate**, NOT final Tier-count freeze.

Formulas:
- minimum successful class-stage volume = `250T`
- max stars = `15T`

Candidate identities:
- T1 Vocabulary / Field Reading
- T2 Frontline / Breakthrough
- T3 Tempo / Population Shift
- T4 Formation / Objective Pressure
- T5 Mastery / Contrast

Final Tier count/name/order remains open.

---

# T1 structural work completed this tranche

## V0.1 skeleton
`11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md`

Static audit found:
- SIEGE Stage26–30 five-stage run,
- SIEGE 12/50 Stage presence despite T1 LOW intention,
- SPLITTER E08 Stage20–22 repetition,
- late C3/C4 concentration.

Audit:
`12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`

## V0.2 active candidate
`13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`

Structural result:
- last first-teach = Stage26 SIEGER,
- no new core ordinary capability Stage40+,
- 61 encounter occurrences,
- C0 4 / C1 19 / C2 27 / C3 9 / C4 2,
- C0–C2 = 82.0%,
- SIEGE Stage presence 12 -> 9,
- SIEGE five-stage run removed,
- SPLITTER three-stage repetition removed,
- C4 only Stage49/50,
- Final Examination includes focused extremes instead of constant synergy.

Status:
**T1 STRUCTURAL PASS / NUMERIC CANDIDATE DATA NOT YET AUTHORED**.

Remaining WATCH:
- BULWARK 19/50 Stage presence,
- Stage20–26 teaching density,
- FORTRESS necessity at T1 49/50,
- no-permanent-stat first-class survivability,
- class opportunity after geometry/count authoring.

---

# Player skill truth
- Lv6: FROZEN+AUTHORITATIVE.
- Lv11/Lv16/Lv21: exact legacy parity candidates.
- Lv26: DESIGNED_NOT_AUTHORITATIVE.
- Lv31: OPEN/UNRESOLVED.

Parity implementation is parked.
Late 50-stage simulation must later include higher-skill candidate modes.

---

# Exact next boundary
Continue corpus authoring, not live code.

Next bounded tranche:
**T1 2-player candidate numeric authoring envelope**.

Order:
1. E01–E19 T1-used archetypes: authored monster count ranges,
2. effective entity volume incl. SPLITTER children,
3. cadence bucket candidate values,
4. concrete formation IDs / arrival-order intent,
5. static active/4s/6s density calculation,
6. representative encounter micro-simulation,
7. fix defects before expanding scope,
8. 10-stage synthetic slice,
9. full T1 50-stage simulation only after slice passes,
10. 3P/4P scaling only after 2P structure stabilizes.

Do not yet freeze:
- production HP/speed/armor/reward,
- permanent stat thresholds,
- final Tier count,
- shop cadence,
- boss cadence,
- Lv11+ implementation.

---

# New-session recovery rule
Do not trust this handoff alone.
Always re-read the live `timing-defense-workspace` branch HEAD and current files first.
Live remote wins over chat/memory/handoff text.

When a work group closes, sync:
- `PROJECT_STATUS.md`
- `NEXT_WORK.md`
- `SESSION_HANDOFF.md`
- active corpus evidence/audit documents
before moving to a new session.
