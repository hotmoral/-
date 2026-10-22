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

# Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/README.md`
5. `legacy-game-structure/01_META_PROGRESSION.md`
6. `legacy-game-structure/02_TIER_SYSTEM.md`
7. `legacy-game-structure/03_STAGE_STRUCTURE_50.md`
8. `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`
9. `legacy-game-structure/05_LEGACY_EVIDENCE_MAP.md`
10. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
11. `legacy-game-structure/07_AUTHORING_DATA_SCHEMA.md`
12. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
13. `MONSTER_CAPABILITY_CONTRACT_V1.md`
14. `CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`

---

# Critical session direction
The project is currently in a **structure-first design/calibration phase**.

Do not immediately:
- implement Lv11+,
- reconstruct legacy Stage4→10,
- author final live 50-stage content,
- freeze production monster numbers,
- promote old S/E/X recipes into production.

First complete:
`legacy structure recovery -> Tier/meta structure -> encounter model -> candidate authoring data -> deterministic simulation -> explicit freeze`.

Only after that should the current Cloudflare game be changed.

---

# Closed foundations
- v0.36: exact EXP/N2/Lv6 authority.
- v0.38: 512-event multiplayer/reconnect kernel.
- v0.39: N3 frozen and authoritative.
- Monster Capability V1: all nine ordinary archetypes mechanically authoritative through v0.45.

Nine ordinary archetypes:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Current monster capability coefficients are still **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN**.

Stage1–3 are regression fixtures only.

---

# New Legacy Game Structure Corpus
Directory:
`legacy-game-structure/`

Purpose:
- stop repeatedly scraping scattered old files,
- preserve evidence status,
- build one structural model before further implementation,
- separate frozen structure from provisional numeric balance.

Status labels used:
- CURRENT_FROZEN_STRUCTURE
- CURRENT_AUTHORITATIVE
- USER_CONFIRMED_STRUCTURE
- LEGACY_IMPLEMENTED_REFERENCE
- LEGACY_ANALYSIS_REFERENCE
- SUPERSEDED
- OPEN_DECISION

---

# User-confirmed progression structure

## Independent class progression
Knight / Rogue / Tank / Archer / Mage each own an independent Tier progression record.

## Tier and star rule
Each Tier = 50 stages.

Attempt result:
- fail Stage 1–19 -> 0★
- fail Stage 20–39 -> 1★
- fail Stage 40–49 -> 2★
- clear Stage 50 -> 3★

A `class x Tier` stores the best result only, maximum 3★.
Repeated attempts do not create unlimited stars.

## Global stars / permanent stats
`GlobalStarTotal = sum(bestStars across all class x Tier records)`.

Stars are not spent.
Cumulative star thresholds automatically grant permanent account-wide stats applied to all classes.

Example:
- all five classes obtain 3★ in Tier1 -> total 15★.

Exact permanent-stat thresholds, categories and coefficients are not yet production frozen.

Open decisions:
- next-Tier unlock condition,
- multiplayer Tier eligibility/host rules.

---

# Encounter model reset
Old `S / E / X` remains historical analysis only.

New top-level pressure vocabulary:
- BASELINE
- FLOOD
- RUSH
- BULWARK
- BREACH
- AERIAL
- REPLICATE
- SUPPORT
- SIEGE

Encounter design additionally owns:
- monster count/frequency,
- composition,
- formation/frontline order,
- spawn order,
- cadence,
- geometry,
- active concurrency,
- target reorder,
- frontline block time,
- backline exposure/capability uptime.

Reason: the current combat does not assume free manual target selection. Basic direct/AI/passive targeting is system-driven/frontmost-first; penetration/AoE are class-specific soft advantages.

Initial structural encounter library is documented in:
`legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`.

---

# Player skill authority truth
- Lv6: **FROZEN+AUTHORITATIVE**.
- Lv11/Lv16/Lv21: exact v0.16 **LEGACY-REFERENCE / parity candidates**.
- Lv26: **DESIGNED-NOT-AUTHORITATIVE**.
- Lv31: **UNRESOLVED**.

The old proposed P1/P2/P3 parity migration remains valid as a later candidate but is now **parked behind the structure phase**.

50-stage final calibration eventually requires a credible higher-skill progression model; current Lv6-only authority cannot represent late-campaign player power.

---

# Exact next boundary
Continue the corpus, not live code.

Next work sequence:
1. finish source-level audit of legacy run/lobby/shop/result/persistence/boss/progression flows,
2. fill Tier structure with candidate identities and monster availability,
3. create Tier/Stage monster frequency/count/composition/cadence candidates using the 9-monster taxonomy,
4. build target-order/screening-aware encounter micro-simulation,
5. expand to 50-stage Tier simulation,
6. add 2/3/4-player scaling,
7. add 5-class account star/permanent-stat progression simulation,
8. check order dependence/snowball/star-boundary cliffs/class opportunity,
9. report and explicitly decide/freeze,
10. only then resume gameplay implementation.

## Validation/governance
`recover -> structure -> model -> simulate -> classify -> report -> discuss -> explicit freeze -> implement`.
