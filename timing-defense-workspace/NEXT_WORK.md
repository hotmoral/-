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

# ACTIVE PHASE — Structure-first campaign/meta authoring/calibration

Primary corpus:
`legacy-game-structure/`

Critical read order:
1. `README.md`
2. `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
3. `01_META_PROGRESSION.md`
4. `15_ACHIEVEMENT_TITLE_CROSS_CLASS_PROGRESSION_V0_1.md`
5. `02_TIER_SYSTEM.md`
6. `03_STAGE_STRUCTURE_50.md`
7. `04_MONSTER_ENCOUNTER_MODEL.md`
8. `10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
9. `09_TIER_LADDER_CANDIDATE_V0_1.md`
10. `12_T1_STATIC_DISTRIBUTION_AUDIT_V0_1.md`
11. `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
12. `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
13. `06_SIMULATION_CALIBRATION_PLAN.md`
14. `07_AUTHORING_DATA_SCHEMA.md`
15. `05_LEGACY_EVIDENCE_MAP.md`

---

# Structural truth — progression

## Shared content / independent class progress
- same Tier uses the same Stage/encounter authoring data across all classes,
- five classes keep independent Tier records,
- same content may be easier/harder depending on class kit and current account progression,
- hard class lockout is forbidden,
- soft progression walls are intentional and may be recovered through cross-class progression.

## Star progression
- 1 Tier = 50 stages,
- fail 1–19 -> 0★,
- fail 20–39 -> 1★,
- fail 40–49 -> 2★,
- clear 50 -> 3★,
- `bestStars[class][tier] = max(previous, attemptStars)`,
- `GlobalStarTotal = sum(bestStars)`,
- stars are non-spendable,
- cumulative stars grant broad account-wide permanent stats.

## Achievement / title progression
User-confirmed direction:
- class-specific Tier achievements,
- all-class Tier achievements,
- class-specific AI-free pure SOLO Tier-clear achievements,
- some achievements grant permanent stats to **another class**, not the source class.

Intended loop:

```text
Class A blocked
 -> progress B/C/D
 -> gain stars + achievements
 -> broad + targeted permanent growth
 -> return to A
 -> previous soft wall becomes attainable
```

Role split:
```text
Stars        = broad progression foundation
Achievements = targeted cross-class bridges
Titles       = achievement presentation/collection
```

Default structural recommendation:
- gameplay reward unlocks on achievement completion,
- title equip is cosmetic by default,
- title-equipped stats remain OPEN_DECISION.

Do not freeze yet:
- exact achievement list,
- sourceClass -> targetClass mapping,
- exact stat type/value,
- reward stacking rule,
- title names.

---

# Encounter taxonomy
Old S/E/X = legacy analysis only.

Current authoring vocabulary:
- BASELINE
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

Simulator input only.

Candidate readability alerts:
- authored 4s normal target <=8,
- authored 9–10 WATCH,
- authored >10 warning,
- effective 4s normal target <=10,
- effective 11–13 WATCH,
- effective >13 warning,
- peak active mostly 6–8 / WATCH 9–10 / stress 11+.

These are analysis alerts, not runtime hard caps.

---

# Player skill parity — PARKED
- Lv6 current authority.
- Lv11/Lv16/Lv21 exact legacy parity candidates.
- Lv26 designed-not-authoritative.
- Lv31 unresolved.

No Lv11+ live implementation during this structure tranche.

---

# EXACT NEXT BOUNDARY

Next bounded tranche remains **T1 representative encounter micro-simulation preflight**.

Order:
1. map E01–E19 to allowed formation/cadence combinations,
2. choose representative L/M/H recipes actually used by T1 V0.2,
3. generate deterministic spawn schedules,
4. calculate authored 4s/6s burst density,
5. stress SPLITTER child creation,
6. model frontmost arrival/screening for E11/E12/E17/E18/E19,
7. measure SIEGER first-shot/screened firing opportunity,
8. measure SUPPORTER screened aura opportunity,
9. verify CHARGER telegraph concurrency,
10. classify defects and revise envelope,
11. then build 10-stage synthetic slice,
12. then full T1 50-stage simulation,
13. produce **5-class viability / soft-wall map**,
14. measure recovery with stars only,
15. only then place candidate cross-class achievement reward edges into observed gaps,
16. run stars + achievements combined account simulation.

Do not yet:
- assign exact recipe to all 50 stages,
- expand to 3P/4P,
- freeze production values,
- invent achievement reward amounts before soft-wall data exists,
- change live game code.

## Achievement-specific validation later
- progression graph reachability,
- circular deadlock,
- dominant class-order route,
- source-class self snowball,
- target-class isolation,
- solo achievement becoming mandatory progression,
- stars + achievements runaway acceleration.

## Governance
`recover -> structure -> static audit -> candidate data -> micro-sim -> synthetic slice -> full Tier sim -> soft-wall map -> cross-class reward model -> account sim -> report -> explicit freeze -> implement`.
