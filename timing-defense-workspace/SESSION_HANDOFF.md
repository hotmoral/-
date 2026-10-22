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
- run/job `39725993894` / `119649887564`

No gameplay/numerical implementation has been authorized after this checkpoint.

---

# Critical direction
The project is in a **structure-first campaign/meta authoring and calibration phase**.

Do not immediately:
- implement Lv11+,
- reconstruct legacy Stage4→10,
- freeze production monster numbers,
- promote old S/E/X recipes,
- assign exact recipes to all 50 stages,
- expand to 3P/4P before 2P structure is stable.

Required order:
`structure -> static consistency audit -> candidate authoring data -> micro-sim -> synthetic slice -> full Tier sim -> explicit freeze -> live implementation`.

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
14. `legacy-game-structure/14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
15. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
16. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
17. `legacy-game-structure/05_LEGACY_EVIDENCE_MAP.md`
18. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
19. `MONSTER_CAPABILITY_CONTRACT_V1.md`

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

# Encounter model truth
Old S/E/X = legacy analysis only.

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

Formation/front/mid/back is authoring intent, not target override.
Actual targeting remains runtime system-driven/frontmost/validity based.

Complexity:
- C0 baseline
- C1 single mechanic
- C2 dual readable
- C3 synergy
- C4 multi-state high complexity

Complexity != difficulty.

---

# Governance
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
- deterministic simulation,
- scope/cost control.

Cross-category decisions requiring linked review:
- Tier unlock,
- permanent stat ladder,
- shop cadence,
- EXP/skill reach,
- boss/checkpoint policy,
- multiplayer Tier progression.

---

# Tier ladder candidate
First bounded full-campaign simulation spine = **5 Tier candidate**, not final Tier-count freeze.

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

# T1 structural work

## V0.1 skeleton
Static audit found:
- SIEGE Stage26–30 five-stage run,
- SIEGE 12/50 Stage presence,
- SPLITTER E08 Stage20–22 repetition,
- late synergy concentration.

## V0.2 active skeleton
`13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`

Result:
- last first-teach Stage26,
- no new core ordinary capability Stage40+,
- 61 encounter occurrences,
- C0 4 / C1 19 / C2 27 / C3 9 / C4 2,
- C0–C2 = 82.0%,
- SIEGE Stage presence 12 -> 9,
- repetition defects corrected,
- C4 Stage49/50 only.

Status:
**T1 STRUCTURAL PASS / NUMERIC PRODUCTION VALUES NOT FROZEN**.

---

# T1 2P authoring envelope V0.1
`14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

Status:
**SIMULATION CANDIDATE / NOT PRODUCTION BALANCE**.

Completed:
- E01–E19 L/M/H/X candidate compositions,
- authored/effective count separation,
- SPLITTER child-volume accounting,
- T1 one-SUPPORTER default package,
- T1 one-SIEGER default package,
- E19 T1 bounded L/M policy,
- cadence IDs CD01–CD08,
- formation IDs F01–F09,
- initial static readability alerts.

Historical old 5-monster 2P reference:
- P95 4s ≈11,
- P95 6s ≈13.5.

New candidate authoring alerts:
- authored 4s normal <=8 / WATCH 9–10 / warning >10,
- effective 4s normal <=10 / WATCH 11–13 / warning >13,
- peak active target mostly 6–8 / WATCH 9–10 / stress 11+.

These are not runtime hard caps.

WATCH:
- E08/E15/E16 SPLITTER X effective volume 13–14,
- SIEGER actual shot uptime still unknown,
- SUPPORTER actual aura uptime still unknown,
- CHARGER telegraph overlap still unmeasured.

---

# Player skill truth
- Lv6: FROZEN+AUTHORITATIVE.
- Lv11/Lv16/Lv21: exact legacy parity candidates.
- Lv26: DESIGNED_NOT_AUTHORITATIVE.
- Lv31: OPEN/UNRESOLVED.

Parity implementation remains parked.
Late 50-stage simulation must later include higher-skill candidate modes.

---

# Exact next boundary
Continue corpus analysis/simulation, not live code.

Next bounded tranche:
**T1 representative encounter micro-simulation preflight**.

Order:
1. map E01–E19 to allowed formation/cadence combinations,
2. select representative L/M/H recipes actually needed by T1 V0.2,
3. generate deterministic spawn schedules,
4. compute authored 4s/6s burst density,
5. stress SPLITTER child creation,
6. model frontmost arrival/screening for E11/E12/E17/E18/E19,
7. measure SIEGER first-shot/screened firing opportunity,
8. measure SUPPORTER screened aura opportunity,
9. inspect CHARGER telegraph concurrency,
10. revise authoring envelope,
11. only after PASS build a 10-stage synthetic slice.

Do not yet freeze:
- production monster coefficients,
- final Tier count,
- permanent stat thresholds,
- shop cadence,
- boss cadence,
- Lv11+ implementation.

---

# New-session recovery rule
Do not trust this handoff alone.
Always re-read live `timing-defense-workspace` HEAD and current files first.
Live remote wins over chat/memory/handoff.

When a work group closes, synchronize:
- `PROJECT_STATUS.md`
- `NEXT_WORK.md`
- `SESSION_HANDOFF.md`
- active corpus evidence/audit files.
