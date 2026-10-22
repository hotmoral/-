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

## Exact latest executable checkpoint
- branch `timing-defense-cloudflare-v045-sieger-pass-20261022`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- live run/job `39725993894` / `119649887564`

Stage1–3 remain regression fixtures only. Do not reconstruct legacy Stage4→10 as production content.

---

# ACTIVE PHASE — Legacy Game Structure Corpus

The immediate next boundary is **game-structure design/analysis, not gameplay implementation**.

Canonical structure workspace:
`legacy-game-structure/`

Read in order:
1. `legacy-game-structure/README.md`
2. `legacy-game-structure/01_META_PROGRESSION.md`
3. `legacy-game-structure/02_TIER_SYSTEM.md`
4. `legacy-game-structure/03_STAGE_STRUCTURE_50.md`
5. `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`
6. `legacy-game-structure/05_LEGACY_EVIDENCE_MAP.md`
7. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
8. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`

This corpus is separate from live implementation authority. It organizes recovered legacy evidence, current frozen contracts, user-confirmed structural intent, and open decisions before production authoring/calibration.

---

# User-confirmed meta progression structure

Each of the five classes progresses through Tiers independently.

Each Tier has 50 stages. Attempt star result:
- fail Stage 1–19 -> `0★`
- fail Stage 20–39 -> `1★`
- fail Stage 40–49 -> `2★`
- clear Stage 50 -> `3★`

Each `class x Tier` stores a maximum/best result of 3 stars; repeated attempts do not farm additional stars beyond the best result.

`GlobalStarTotal = sum(bestStars[class][tier])`.

Stars are not a spendable currency. Cumulative stars automatically unlock account-wide permanent stats applied to all classes.

Example: all five classes earn 3★ in Tier1 -> total 15★.

Permanent-stat thresholds and coefficients are **OPEN / NOT NUMERICALLY FROZEN**.

Tier-unlock semantics and multiplayer eligibility rules remain explicit decision gates.

---

# Encounter taxonomy reset

The old `S / E / X` grammar is retained only as `LEGACY_ANALYSIS_REFERENCE`.
It is no longer the production top-level authoring taxonomy because the current 9-monster roster contains distinct special mechanics that `X` over-compresses.

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

Production authoring must additionally model:
- monster type frequency/count,
- encounter archetype,
- formation/frontline order,
- spawn order,
- cadence,
- geometry,
- active concurrency,
- target reorder,
- frontline block time,
- backline exposure/capability uptime.

This is required because direct/AI/passive target acquisition is system-driven/frontmost-first rather than free manual backline selection.

---

# Monster Capability V1 remains frozen structurally

Nine ordinary archetypes:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Their mechanical foundations are authoritative through v0.45.
Production balance coefficients remain provisional unless separately frozen.
Bosses remain a separate layer.

---

# Player skill parity — PARKED, NOT CANCELLED

Authority truth remains:
- Lv6 — **FROZEN+AUTHORITATIVE**
- Lv11/Lv16/Lv21 — **LEGACY-REFERENCE / exact parity candidates**
- Lv26 — **DESIGNED-NOT-AUTHORITATIVE**
- Lv31 — **UNRESOLVED**

The previous P1/P2/P3 parity strategy remains a valid candidate, but it is **not the immediate next implementation task**.

Do not write Lv11+ code until the higher-level game structure has been sufficiently aligned and the user explicitly resumes implementation.

The skill model must later be fed into 50-stage simulation because late-stage power cannot be calibrated credibly with Lv6-only player authority.

---

# Immediate work order

1. Continue structural recovery of legacy run/lobby/shop/result/persistence/boss/progression evidence.
2. Complete Tier-system decisions that can be made structurally without production numbers.
3. Build the new 9-monster encounter-archetype library and synergy/target-order matrix.
4. Define candidate monster introduction/frequency/count/composition/cadence data by Tier and Stage band.
5. Build/adapt deterministic authoring and simulation tooling around the new schema.
6. Run encounter micro-sim before full 50-stage authoring.
7. Run single-Tier 50-stage simulations for class/mastery/team-size/star-outcome distributions.
8. Add account-level star/permanent-stat progression simulation, including first-class vs later-class order effects.
9. Report/classify problems.
10. Freeze only after explicit discussion/decision.
11. Resume targeted live implementation only after the structure gate is closed.

## Do not do yet
- no production monster-number freeze,
- no final Tier count/name freeze,
- no permanent-stat coefficient freeze,
- no final 50-stage live campaign patch,
- no Lv11+ live implementation,
- no automatic promotion of old S/E/X or old Stage1–10 recipes.

## Governance
`recover -> structure -> model -> simulate -> classify -> report -> discuss -> explicit freeze -> implement`.
