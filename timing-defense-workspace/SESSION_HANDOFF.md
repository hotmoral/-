# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory, copied SHA values or this file alone.
Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_10.yaml`
6. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
7. `legacy-game-structure/88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
8. `legacy-game-structure/89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
9. `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
10. `legacy-game-structure/92_P4D2_LV31_MASTERY_POWER_AND_STAGE46_PRESSURE_PREFLIGHT_V0_1.md`
11. `legacy-game-structure/94_P4D2_LV31_CURRENT_ROSTER_PRESSURE_RESPONSE_PROBE_V0_1.md`
12. `legacy-game-structure/95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
13. `legacy-game-structure/data/p4d2_stage46_temporal_pressure_summary_v0_1.json`
14. `legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json`
15. `tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py`
16. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
17. `SKILL_PLAN_LV6_31.md`
18. `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
19. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
20. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
21. current production branch head and calibration-harness head
22. older P4-A/P4-B/P3 evidence only as needed for causal context/revalidation triggers

Historical proposal 90 is superseded by approved document 91 wherever they conflict.
Historical five-monster `PRESSURE_RECIPES_V1.md` is not current-nine-roster Stage46 balance evidence.

Do not re-run closed P1/P2/P3/P4-C1/C2 solely because a new session starts.
Live remote always wins.

---

# Branch checkpoints

Planning:
- branch `timing-defense-workspace`
- exact HEAD must be re-fetched after final sync; copied SHA is only a checkpoint.

Production:
- branch `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- branch `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- current P4-D2 planning work did not change it.

---

# Current exact phase / boundary

```text
P4-C1 = USER_APPROVED_STRUCTURAL_COMPLETE
P4-C2 = COMPLETE / PASS_WITH_WATCHES
P4-D1 = USER_APPROVED_WITH_MODIFICATION
P4-D2 current-roster static probe = COMPLETE
P4-D2 stateful temporal pressure probe = COMPLETE / CANDIDATE PRESSURE ENVELOPE FOUND
P4-D2 Archer gameplay-width structure = USER DECISION PENDING
P4-E = BLOCKED_PENDING_P4D2
production changes = UNAUTHORIZED
```

Current exact next action:
**user decision on Archer Lv31 wider-straight gameplay-corridor principle.**

---

# User-approved late-run philosophy

```text
Lv31 must be spectacular and class-defining
+
finite / deterministic / attributable effect graph
+
Stage46+ pressure rises enough to require and absorb Lv31 power
```

A Lv31-less intended-skilled player may be buried by actual encounter pressure.
Do not add a code-level Lv31 requirement.
Combo/timing/P×P maintenance is an intended late-run difficulty axis.

Stage structure:

```text
41..45 acquisition / transition
46 major pressure jump
46..47 power revelation
48..49 mastery pressure
50 final full-kit application
```

Acquisition fairness remains open. 97/98/99% Stage46 possession checkpoints may be tested; none is frozen.

---

# Replayable temporal evidence

Assets:

```text
tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py
legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json
legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json
legacy-game-structure/data/p4d2_stage46_temporal_pressure_summary_v0_1.json
```

RNG: `NONE`

Runner Git blob SHA:
`5965833f80422bd6cae94fea738706baf99a06e8`

Expected full output SHA-256:
`110ea2beb87dabb41b4d8dd48af61bbe97e21666413481a9f19df95507c75e75`

The runner blob was checked against the locally validated runner and matches exactly.

---

# Gate separation result

Same deterministic 60s stress envelope:

## Lv26 + all PERFECT

```text
Rogue  28.65s burial
Tank   33.25s
Knight 35.80s
Archer 52.65s
Mage   56.25s
```

## Lv31 + every P×P successful

```text
Knight survives / wall1175
Rogue  survives / wall1330
Tank   survives / wall2000
Archer survives / wall2000
Mage   survives / wall2000
```

Therefore a combat-based Lv31 mastery gate is structurally feasible with current nine-roster grammar.

Do not freeze the diagnostic pressure recipe as exact Stage46 content.

---

# Current working centers — provisional only

## Knight
`second wave = 1.00`.
0.75 nearly collapses in temporal stress; 1.25 mostly saturates.

## Rogue

```text
12 -> buried41.90s
16 -> survives / wall1330
20 -> largely dominates / wall2000 / only5 active
```

16 remains preferred working center. No performance-based nerf is justified yet.

## Tank

```text
shockwave .75
KB ×2.5
barrier250 / 6s candidate
```

Targeted CHARGER/SIEGER state alignment still required.

## Mage

```text
three stages .75
radius center1.25
```

1.00 mostly saturates; larger radius is not monotonically better because chronology/target order changes.

## Archer
Per-target continuity center remains `2.30` because Lv26 Triple Shot aligned package is `1.00+.65+.65=2.30`.

New temporal geometry finding:
- narrow ordinary-width Lv31 ray fails at coeff1.00/1.50/2.00/2.30, all burial52.65s;
- modest wider straight corridor survives.

This means the dominant missing axis is width, not damage.

---

# Archer material decision

Candidate principle:

For Lv31 `Sky-Piercing Arrow` only:
- gameplay collision corridor is wider than ordinary/Lv26 arrows;
- still one locked straight projectile/ray;
- no homing;
- no bending;
- no off-line retarget;
- unlimited depth only inside the corridor;
- exact width stays P4-D2 provisional calibration.

Why this is a user gate:
proposal 90 explicitly said visual size should not automatically widen gameplay collision. The new evidence now supports reopening only that clause.

Options:

```text
A approve wider-straight gameplay corridor principle
B reject width increase / keep huge visual-only
C request further geometry analysis
```

Do not silently approve A.

---

# Miss-severity evidence / next work after Archer decision

One miss:

```text
Knight wall900
Rogue wall175
Tank wall1981
Archer wall2000
Mage wall2000
```

Two consecutive misses:

```text
Knight wall255
Rogue buried49.70s
Tank wall1837
Archer wall1940
Mage wall2000
```

This class divergence is an **encounter-grammar problem first**, not a reason for hidden class-specific buffs/XP correction or immediate nerfs.

After Archer decision, continue P4-D2 with:
1. targeted CHARGER WINDUP interrupt/re-arm alignment;
2. targeted SIEGER standoff/windup/reposition alignment;
3. Stage48–49 mixed-geometry miss-severity repair;
4. Mage/SPLITTER chronology;
5. Stage46 acquisition fairness;
6. later Rogue multiplayer projectile-volume stress;
7. no final EXP claim before P10R.

---

# Active watches

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
LV26_T4_ROLE_EXPRESSION_WATCH
LV26_MAGE_SPLITTER_ORDERING_WATCH
LV26_TANK_MOVEMENT_COMPOSITION_WATCH
LV31_CLASS_CLEAR_RATE_DIVERGENCE
LV31_ROLE_EXPRESSION_ERASURE
LV31_POWER_FANTASY_UNDERSHOOT
LV31_ARCHER_MAGNITUDE_CONTINUITY_WATCH
LV31_ARCHER_GAMEPLAY_WIDTH_DECISION
STAGE46_LV31_ACQUISITION_FAIRNESS
STAGE46_LV31_ABSENCE_BURIAL_BEHAVIOR
PXP_COMBO_MAINTENANCE_MASTERY_PRESSURE
STAGE48_49_MISS_SEVERITY_CLASS_DIVERGENCE
ROGUE_DAGGER_STORM_EVENT_VOLUME_PERFORMANCE_WATCH
```

---

# Do not yet

- approve/freeze Archer wider collision corridor without user decision;
- freeze Archer2.30;
- freeze Rogue16;
- freeze Stage46 97/98/99%;
- freeze 4.6s pressure cycle or exact Stage46–50 content;
- change/deploy production gameplay;
- freeze final EXP;
- begin P5 before P4-E closure.
