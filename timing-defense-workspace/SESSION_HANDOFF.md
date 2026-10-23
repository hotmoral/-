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
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_11.yaml`
6. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
7. `legacy-game-structure/88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
8. `legacy-game-structure/89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
9. `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
10. `legacy-game-structure/92_P4D2_LV31_MASTERY_POWER_AND_STAGE46_PRESSURE_PREFLIGHT_V0_1.md`
11. `legacy-game-structure/94_P4D2_LV31_CURRENT_ROSTER_PRESSURE_RESPONSE_PROBE_V0_1.md`
12. `legacy-game-structure/95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
13. `legacy-game-structure/96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
14. `legacy-game-structure/97_P4D2_ROLE_ALIGNMENT_AND_ARCHER_WIDTH_PROBE_V0_1.md`
15. `legacy-game-structure/98_P4D2_STAGE48_49_GRAMMAR_RESET_PROXY_V0_1.md`
16. `legacy-game-structure/data/p4d2_stage46_temporal_pressure_summary_v0_1.json`
17. `legacy-game-structure/data/p4d2_archer_width_role_alignment_v0_1.json`
18. `legacy-game-structure/data/p4d2_stage48_49_grammar_reset_proxy_v0_1.json`
19. `tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py`
20. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
21. `SKILL_PLAN_LV6_31.md`
22. `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
23. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
24. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
25. current production branch head and calibration-harness head
26. older P4-A/P4-B/P3 evidence only as needed for causal context/revalidation triggers

Historical proposal 90 is superseded wherever it conflicts with approved documents 91 and 96.
Historical five-monster `PRESSURE_RECIPES_V1.md` is not current-nine-roster Stage46+ balance evidence.

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
P4-D2 Stage46 temporal pressure = COMPLETE / CANDIDATE PRESSURE ENVELOPE FOUND
P4-D2 Archer wider gameplay corridor = USER APPROVED
P4-D2 role-alignment / width proxy = COMPLETE
P4-D2 Stage48–49 static grammar reset proxy = COMPLETE / DIRECTION SUPPORTED
P4-D2 dynamic repeated-miss grammar rotation = NEXT ACTIVE WORK
P4-E = BLOCKED_PENDING_P4D2
production changes = UNAUTHORIZED
```

No user decision is currently pending.

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

# Stage46 gate-separation evidence

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

```text
Knight  second wave1.00
Rogue   16 daggers × .45
Tank    shockwave.75 / KB×2.5 / barrier250-for-6s candidate
Archer  per-target2.30 / wider straight corridor / MID_ADJACENT diagnostic center
Mage    three stages.75 / radius1.25
```

Rogue 16 is supported by temporal sensitivity but not frozen.

---

# Archer Lv31 structural amendment — APPROVED

The user explicitly approved Option A.

`Sky-Piercing Arrow` now structurally means:
- one locked straight final shot;
- no homing;
- no bending;
- no off-line retarget;
- unlimited depth within the actual straight corridor;
- **authoritative gameplay corridor wider than ordinary/Lv26 Archer arrows**.

Exact width remains provisional.

Current five-band diagnostic center:
`MID_ADJACENT`.

Reason:
- catches near-line bodies as a huge arrow should;
- preserves off-corridor SUPPORTER/SIEGER positioning;
- does not become full-screen AoE.

Do not reopen this principle without new material evidence/user gate.

---

# Role-alignment interpretation

CHARGER:
- visible WINDUP followed by Knight/Tank final interrupt is valid mastery counterplay.
- routine deletion before any readable WINDUP remains bad authoring.

SIEGER:
- standoff/windup must expose a readable decision opportunity.
- Knight/Tank may force reposition.
- Archer may delete through earned alignment, but not off-corridor for free.

SPLITTER:
- successful Mage collapse may suppress rebound inside its package.
- missed P×P, off-circle, or late-arriving SPLITTERs should remain rebound-pressure tools.

Do not solve role-expression by inflating monster HP first.

---

# Stage48–49 grammar-reset direction

Four pressure families:

```text
LINE_ESCORT
CLUSTER_CASCADE
FRONTLINE_BREACH
DURABLE_SCATTER
```

Static proxy classification:
`ROTATING_GRAMMAR_CAN_DISTRIBUTE_CLASS_VULNERABILITY`.

Key implication:
one generic mixed recipe should not define late-game miss severity.
Rotate geometries so each class has premium reset windows and recurring vulnerability windows.

---

# Exact next work

Build/run a bounded dynamic rotating-grammar repeated-miss probe:

1. rotate LINE / CLUSTER / FRONTLINE / DURABLE-SCATTER over time;
2. compare all-P×P, one miss, and two consecutive misses;
3. record burial/end-wall/backlog/recovery;
4. record CHARGER/SIEGER/SPLITTER role opportunities;
5. repair encounter grammar/ordering before class coefficients;
6. do not freeze exact Stage48–49 campaign content;
7. do not make final EXP claims.

After that, reassess whether P4-D2 has enough evidence to close provisionally into P4-E or whether one more bounded probe is necessary.

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
STAGE46_LV31_ACQUISITION_FAIRNESS
STAGE46_LV31_ABSENCE_BURIAL_BEHAVIOR
PXP_COMBO_MAINTENANCE_MASTERY_PRESSURE
STAGE48_49_MISS_SEVERITY_CLASS_DIVERGENCE
ROGUE_DAGGER_STORM_EVENT_VOLUME_PERFORMANCE_WATCH
```

---

# Do not yet

- freeze Archer2.30 or exact gameplay width;
- freeze Rogue16;
- freeze Stage46 at 97/98/99%;
- freeze 4.6s pressure cycle or exact Stage46–50 content;
- change/deploy production gameplay;
- freeze final EXP;
- start P5 before P4-E closure.
