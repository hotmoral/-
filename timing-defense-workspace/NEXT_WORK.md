# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed implementation gates
- Cloudflare DO PoC through v0.45 SIEGER — **FULL PASS**.
- Player Skill Authority Review — **COMPLETE**.
- No gameplay/numerical implementation authorized after v0.45.

## Latest executable checkpoint
- branch `timing-defense-cloudflare-v045-sieger-pass-20261022`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health `0.45-cf.1`
- run/job `39725993894` / `119649887564`

Stage1–3 remain regression fixtures only.
Do not reconstruct legacy Stage4→10 as production content.

---

# ACTIVE PHASE — Structure-first campaign authoring/calibration

Primary corpus:
`legacy-game-structure/`

Critical read order:
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
11. `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
12. `06_SIMULATION_CALIBRATION_PLAN.md`
13. `07_AUTHORING_DATA_SCHEMA.md`
14. `05_LEGACY_EVIDENCE_MAP.md`

---

# Structural truth

## Meta progression
- five classes progress through Tiers independently,
- 1 Tier = 50 stages,
- fail 1–19 -> 0★,
- fail 20–39 -> 1★,
- fail 40–49 -> 2★,
- clear 50 -> 3★,
- `bestStars[class][tier] = max(previous, attemptStars)`,
- `GlobalStarTotal = sum(bestStars)`,
- stars are non-spendable account achievement progression,
- cumulative stars grant account-wide permanent stats.

Open:
- permanent reward ladder,
- Tier unlock semantics,
- multiplayer Tier eligibility/credit.

## Encounter taxonomy
Old S/E/X = legacy analysis only.

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

Complexity:
- C0 baseline
- C1 single mechanic
- C2 dual readable
- C3 synergy
- C4 multi-state high complexity

Complexity != difficulty.

---

# Tier ladder candidate
First full-campaign simulation spine uses **5 Tier as a bounded candidate**, not final freeze.

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

# T1 structural candidate V0.2 — PASS

Source:
`13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`

- last first-teach = Stage26 SIEGER,
- no new core ordinary capability Stage40+,
- 61 encounter occurrences,
- C0 4 / C1 19 / C2 27 / C3 9 / C4 2,
- C0–C2 = 82.0%,
- C4 only Stage49/50,
- V0.1 SIEGE overconcentration/repetition corrected,
- SPLITTER three-stage teaching repetition corrected.

Remaining WATCH:
- BULWARK 19/50 Stage presence,
- Stage20–26 cognitive load,
- T1 FORTRESS necessity,
- first-class/no-permanent-stat late survivability,
- geometry-driven class opportunity.

---

# T1 2-player authoring envelope V0.1 — CANDIDATE READY

Source:
`14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`

This is simulator input, not production balance.

## Count rules
- each E01–E19 used by T1 now has L/M/H/X candidate composition,
- authored count and effective entity count are separate,
- SPLITTER children count toward effective entity volume,
- T1 SUPPORTER package defaults to one SUPPORTER,
- T1 SIEGER package defaults to one SIEGER,
- T1 E19 FORTRESS uses L/M first even at Stage49/50.

## Candidate readability alerts
Historical old 5-monster 2P reference: P95 4s ≈11 / 6s ≈13.5.

New candidate starts conservatively:
- authored 4s normal target <=8,
- authored 9–10 WATCH,
- authored >10 warning,
- effective 4s normal target <=10,
- effective 11–13 WATCH,
- effective >13 warning,
- peak active candidate target mostly 6–8 / WATCH 9–10 / stress 11+.

These are analysis alerts, not runtime hard caps.

## Cadence candidate IDs
- CD01 DRIP_SLOW
- CD02 DRIP
- CD03 WAVE
- CD04 BURST_LIGHT
- CD05 STAGGER
- CD06 ESCORT
- CD07 LATE_INSERT
- CD08 OVERLAP_BOUNDED

## Formation candidate IDs
- F01 LINE_LIGHT
- F02 LINE_DURABLE_FRONT
- F03 CLUSTER_LIGHT
- F04 SCATTER_LIGHT
- F05 AIR_OFFSET
- F06 SCREEN_BACKLINE
- F07 ESCORT_COLUMN
- F08 SPLIT_AXIS
- F09 REPLICATION_CLUSTER

---

# Player skill parity — PARKED
- Lv6 current authority.
- Lv11/Lv16/Lv21 exact legacy parity candidates.
- Lv26 designed-not-authoritative.
- Lv31 unresolved.

No Lv11+ live implementation during this structure tranche.

---

# EXACT NEXT BOUNDARY

Next bounded tranche = **T1 representative encounter micro-simulation preflight**, not full 50-stage simulation.

Order:
1. map each E01–E19 to allowed formation/cadence combinations,
2. choose representative L/M/H recipes actually used by T1 V0.2,
3. generate deterministic spawn schedules for those recipes,
4. statically calculate authored 4s/6s burst density,
5. stress SPLITTER child creation separately,
6. model frontmost arrival/screening for E11/E12/E17/E18/E19,
7. measure SIEGER first-shot/screened firing opportunity,
8. measure SUPPORTER screened aura opportunity,
9. verify CHARGER telegraph concurrency,
10. classify defects and revise envelope,
11. only after this passes build a 10-stage synthetic slice.

Do not yet:
- assign exact recipe to all 50 stages,
- expand to 3P/4P,
- freeze production values,
- change live game code.

## Governance
`recover -> structure -> static audit -> candidate data -> micro-sim -> synthetic slice -> full Tier sim -> report -> explicit freeze -> implement`.
