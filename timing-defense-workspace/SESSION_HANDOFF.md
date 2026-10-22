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
- freeze achievement rewards,
- expand to 3P/4P before 2P structure is stable.

Required order:
`structure -> static consistency audit -> candidate authoring data -> micro-sim -> synthetic slice -> full Tier sim -> class soft-wall map -> cross-class reward model -> account sim -> explicit freeze -> live implementation`.

---

# Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/README.md`
5. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
6. `legacy-game-structure/01_META_PROGRESSION.md`
7. `legacy-game-structure/15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
8. `legacy-game-structure/02_TIER_SYSTEM.md`
9. `legacy-game-structure/03_STAGE_STRUCTURE_50.md`
10. `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`
11. `legacy-game-structure/10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
12. `legacy-game-structure/09_TIER_LADDER_CANDIDATE_V0_1.md`
13. `legacy-game-structure/12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
14. `legacy-game-structure/13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
15. `legacy-game-structure/14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
16. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
17. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
18. `legacy-game-structure/05_LEGACY_EVIDENCE_MAP.md`
19. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
20. `MONSTER_CAPABILITY_CONTRACT_V1.md`

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

## Shared Stage content / independent class progression
Same Tier uses the same Stage/encounter data for all classes.
Knight / Rogue / Tank / Archer / Mage keep independent Tier records.

Class asymmetry is intended:
- a class may hit a soft wall earlier than another class,
- other-class progression may provide permanent growth,
- returning later should make the old wall attainable.

Hard class lockout remains forbidden.

## Star progression
One Tier = 50 stages.

Attempt result:
- fail Stage 1–19 -> 0★
- fail Stage 20–39 -> 1★
- fail Stage 40–49 -> 2★
- clear Stage 50 -> 3★

Derived invariant:
`bestStars[class][tier] = max(previous, attemptStars)`.

`GlobalStarTotal = sum(bestStars)`.
Stars are non-spendable.
Cumulative stars automatically grant broad account-wide permanent stats.

## Achievement / title progression
User-confirmed future structure:
- class-specific Tier achievement,
- all-class Tier achievement,
- specific class pure SOLO / AI 0 Tier clear achievement,
- some achievement rewards permanently raise a **different class's** specific stat.

Intended loop:

```text
Class A blocked
 -> progress B/C/D
 -> stars + achievements
 -> account + targeted class growth
 -> return to A
 -> previous soft wall becomes attainable
```

Role split:
- stars = broad foundation,
- achievements = targeted cross-class bridges,
- titles = display/collection layer.

Current structural default:
- achievement completion owns gameplay reward,
- title equip is cosmetic,
- title-equipped stat effect remains OPEN_DECISION.

Open:
- exact achievement catalog,
- title names,
- sourceClass -> targetClass graph,
- stat type/value,
- stacking policy,
- permanent star reward track,
- Tier unlock,
- multiplayer Tier eligibility/credit.

---

# Achievement structural guardrails
Canonical:
`legacy-game-structure/15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`

Must validate:
- progression graph reachability,
- no circular deadlock,
- no single mandatory achievement key,
- no one-class dominant progression route,
- no same-class mastery snowball unless explicitly intended,
- no target class permanently isolated from reward graph,
- AI-free SOLO achievement remains mastery reward rather than mandatory baseline path,
- stars + achievements combined snowball does not trivialize late Tiers.

`SOLO_NO_AI_TIER_CLEAR` truth requires at minimum:
```text
humanPlayerCount = 1
aiCount = 0
no remote human during run
no AI during run
Stage50 clear
```

Reconnect of the same authoritative run may preserve solo truth.

---

# Encounter model truth
Old S/E/X = legacy analysis only.

Current vocabulary:
BASELINE / FLOOD / RUSH / BULWARK / BREACH / AERIAL / REPLICATE / SUPPORT / SIEGE.

Formation/front/mid/back is authoring intent, not target override.
Actual targeting remains runtime system-driven/frontmost/validity based.

Complexity C0–C4 is separate from difficulty.

---

# Governance
Canonical:
`legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`

Every tranche checks:
- product purpose,
- internal consistency,
- cross-category dependencies,
- learning/readability,
- target/formation truth,
- class asymmetry vs hard lockout,
- stars/achievement snowball,
- reward-graph reachability,
- multiplayer implications,
- authority boundary,
- deterministic simulation,
- scope/cost control.

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

## V0.2 active skeleton
`13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`

- last first-teach Stage26,
- no new core ordinary capability Stage40+,
- 61 encounter occurrences,
- C0 4 / C1 19 / C2 27 / C3 9 / C4 2,
- C0–C2 = 82.0%,
- C4 Stage49/50 only,
- prior SIEGE/SPLITTER repetition defects corrected.

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
- one-SUPPORTER / one-SIEGER default T1 packages,
- cadence IDs CD01–CD08,
- formation IDs F01–F09,
- initial readability alerts.

Candidate alerts:
- authored 4s normal <=8 / WATCH 9–10 / warning >10,
- effective 4s normal <=10 / WATCH 11–13 / warning >13,
- peak active mostly 6–8 / WATCH 9–10 / stress 11+.

Not runtime hard caps.

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
1. E01–E19 allowed formation/cadence combinations,
2. representative L/M/H recipe set,
3. deterministic spawn schedules,
4. authored 4s/6s density,
5. SPLITTER child stress,
6. frontmost arrival/screening E11/E12/E17/E18/E19,
7. SIEGER screened first-shot/shot uptime,
8. SUPPORTER screened aura uptime,
9. CHARGER telegraph concurrency,
10. revise authoring envelope,
11. 10-stage synthetic slice,
12. full T1 simulation,
13. 5-class viability / soft-wall map,
14. stars-only recovery analysis,
15. candidate cross-class achievement reward edges,
16. stars + achievements combined account simulation.

Do not yet freeze:
- production monster coefficients,
- final Tier count,
- permanent stat thresholds,
- achievement values/mappings,
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
