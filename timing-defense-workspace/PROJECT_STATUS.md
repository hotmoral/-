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

## Current planning phase
The project has entered a **structure-first campaign/meta design phase** before further gameplay implementation.

Primary planning corpus:
`legacy-game-structure/`

Read first:
1. `NEXT_WORK.md`
2. `legacy-game-structure/README.md`
3. `legacy-game-structure/01_META_PROGRESSION.md`
4. `legacy-game-structure/02_TIER_SYSTEM.md`
5. `legacy-game-structure/03_STAGE_STRUCTURE_50.md`
6. `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`
7. `legacy-game-structure/05_LEGACY_EVIDENCE_MAP.md`
8. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
9. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
10. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
11. `MONSTER_CAPABILITY_CONTRACT_V1.md`
12. `CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`

---

# Closed combat/network foundations
- v0.36: exact EXP/N2/Lv6 authority — PASS.
- v0.38: 512-event multiplayer/reconnect kernel — PASS.
- v0.39: N3 frozen and authoritative — PASS.
- v0.40–v0.45: SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER capability authority — FULL PASS.
- Stage1–3 are regression fixtures only, not final campaign recipes.

## Lv6 authoritative summary
- Knight +12% damage.
- Rogue second dagger +55ms at 55%.
- Tank +30% knockback.
- Archer up to 2 strict-line additional hits at 52%.
- Mage up to 3 nearby splash hits at 50%.

## N3 frozen summary
- milestones 5 / 10 / 20 / 30 / every +10 thereafter.
- budgets 60 / 90 / 150 / 210.
- no generated EXP / charge / combo / ordinary crit / recursive skill / recursive N3.
- normal armor / kill / kill coin / contribution and frozen boss scalars retained.

---

# Monster Capability V1 — mechanical foundation complete
Nine ordinary archetypes:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Structure is frozen V1 and current Cloudflare mechanical authority exists through v0.45.
Production balance coefficients remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately approved.

Bosses remain a separate capability-composition layer.

---

# Campaign/meta structure — NEW ACTIVE AUTHORITY DIRECTION

## Class-independent Tier progression
Each of the five classes progresses through Tiers independently.

## Tier length and stars
Each Tier has 50 stages.

Attempt result:
- fail Stage 1–19 -> 0★
- fail Stage 20–39 -> 1★
- fail Stage 40–49 -> 2★
- clear Stage 50 -> 3★

Each `class x Tier` stores a maximum best result of 3★.
Repeated attempts do not farm stars beyond that best result.

## Global permanent progression
`GlobalStarTotal` is the sum of all class/Tier best-star records.
Stars are non-spendable achievement progression.
Cumulative star milestones automatically grant account-wide permanent stats that apply to all classes.

Example: all five classes clear Tier1 at 3★ -> 15★ total.

Permanent-stat thresholds and coefficients are not yet frozen.

Tier unlock semantics and multiplayer Tier eligibility remain open decisions.

---

# Encounter taxonomy — S/E/X demoted
The old S/E/X grammar is retained as historical analysis only.
It is no longer sufficient as the main production taxonomy for the 9-monster roster.

New pressure vocabulary:
- BASELINE
- FLOOD
- RUSH
- BULWARK
- BREACH
- AERIAL
- REPLICATE
- SUPPORT
- SIEGE

Encounter authoring must also track:
- monster type counts/frequencies,
- archetype composition,
- formation/frontline order,
- spawn order,
- cadence,
- geometry,
- active concurrency,
- target reorder,
- frontline block time,
- backline exposure/capability uptime.

This reflects the actual system-driven/frontmost target model and prevents false assumptions about free backline targeting.

---

# Player Skill Authority Review
Current truth remains:
- Lv6 — **FROZEN+AUTHORITATIVE**
- Lv11/Lv16/Lv21 — **LEGACY-REFERENCE / exact parity candidates**
- Lv26 — **DESIGNED-NOT-AUTHORITATIVE**
- Lv31 — **UNRESOLVED**

The previous Lv11/Lv16/Lv21 parity slices remain candidates, but implementation is parked during the structure-first phase.

Late 50-stage calibration must eventually include the higher skill curve; Lv6-only calibration is not sufficient.

---

# Current work boundary
Do **not** resume legacy Stage4→10 reconstruction.
Do **not** begin Lv11+ implementation yet.
Do **not** freeze new production values yet.

Current work is:
1. expand and audit the legacy game-structure evidence,
2. define Tier/Stage/encounter authoring structure,
3. create 9-monster frequency/count/composition/cadence candidates,
4. model class-independent star progression and account-wide permanent growth,
5. run deterministic encounter -> Stage -> Tier -> account progression simulations,
6. classify/report/discuss,
7. explicitly freeze,
8. only then apply to the current Cloudflare game.

## Governance
`recover -> structure -> model -> simulate -> classify -> report -> discuss -> explicit freeze -> implement`.
