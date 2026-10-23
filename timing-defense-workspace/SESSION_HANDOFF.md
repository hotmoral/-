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
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_9.yaml`
6. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
7. `legacy-game-structure/88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
8. `legacy-game-structure/89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
9. `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
10. `legacy-game-structure/92_P4D2_LV31_MASTERY_POWER_AND_STAGE46_PRESSURE_PREFLIGHT_V0_1.md`
11. `legacy-game-structure/93_P4D2_FIRST_PASS_LV31_POWER_ENVELOPE_AND_PRESSURE_TARGETS_V0_1.md`
12. `legacy-game-structure/94_P4D2_LV31_CURRENT_ROSTER_PRESSURE_RESPONSE_PROBE_V0_1.md`
13. `legacy-game-structure/data/p4d2_lv31_pressure_probe_summary_v0_1.json`
14. `legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json`
15. `tools/run_p4d2_lv31_pressure_probe_v0_1.py`
16. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
17. `SKILL_PLAN_LV6_31.md`
18. `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
19. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
20. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
21. current production branch head and calibration-harness head
22. older P4-A/P4-B/P3 evidence only as needed for causal context/revalidation triggers

Historical proposal 90 is now superseded by document 91 wherever they conflict. Read it only for proposal history if needed.

Important:
- do not re-run closed P1/P2/P3/P4-C1/C2 solely because a new session starts;
- document 94 is current P4-D2 bounded evidence, not numerical-freeze authority;
- the historical five-monster `PRESSURE_RECIPES_V1.md` must not be promoted into current nine-roster Stage46 evidence;
- production remains unchanged unless separately authorized.

Live remote always wins.

---

# Branch checkpoints

Planning:
- branch `timing-defense-workspace`
- exact final HEAD must be re-fetched after all handoff-sync commits; any copied SHA is only a checkpoint.

Production:
- branch `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- branch `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- no current planning work changed it.

---

# Current exact phase / boundary

```text
P4-C1 = USER_APPROVED_STRUCTURAL_COMPLETE
P4-C2 = COMPLETE / PASS_WITH_WATCHES
P4-D1 = USER_APPROVED_WITH_MODIFICATION
P4-D2 snapshot/package response = COMPLETE / PASS_WITH_CORRECTION
P4-D2 stateful temporal pressure feedback = NEXT / ACTIVE PHASE
P4-E = BLOCKED_PENDING_P4D2
production changes = UNAUTHORIZED
```

No user decision is currently required.

Current exact next work:
**build/run the bounded stateful temporal current-nine-roster pressure probe described in NEXT_WORK and document 94.**

---

# P4-D1 approved philosophy

User direction:

```text
Lv31 must be spectacular and class-defining
+
finite / deterministic / attributable effect graph
+
Stage46+ pressure rises enough to require and absorb Lv31 power
```

Do not interpret `bounded` as `few hits`.
Many explicit projectiles/hits are valid when they are the class fantasy.

A Lv31-less intended-skilled player may be buried by actual encounter pressure. No code-level Lv31 gate should be added.

Combo/timing/P×P maintenance is an intended late-run difficulty axis.

---

# Stage46+ structure

```text
Stage41..45 = Lv31 acquisition / transition
Stage46     = major pressure jump
Stage46..47 = power revelation
Stage48..49 = mastery pressure / combo-P×P maintenance
Stage50     = full-kit final application
```

Acquisition fairness:
- user judged 90% Stage46-entry Lv31 possession too lenient;
- P4-D2/P4-E may test 97/98/99% checkpoints;
- no exact threshold is frozen;
- class kill-speed / EXP opportunity / team / player-count effects must not unfairly determine whether a skilled player reaches Lv31.

---

# P4-D2 replayable current-roster probe

Committed assets:

```text
tools/run_p4d2_lv31_pressure_probe_v0_1.py
legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json
legacy-game-structure/data/p4d2_lv31_pressure_probe_summary_v0_1.json
```

RNG:
`NONE`

Expected generated full-output SHA-256:

```text
efdb369a6053bb83fcecb057ea733f4bdcabb56a333575dddf2dd4b87913e27d
```

This provides an exact one-command replay path for the current P4-D2 bounded evidence, avoiding the replayability limitation recorded for P4-C2.

The diagnostic snapshots are not exact Stage46 authoring.

---

# Current working Lv31 centers — all provisional

## Knight
- strong bounded two-wave frontline break;
- second-wave center `1.00` root basis;
- center ideal corridor package ≈2× Lv26 one-wave corridor package;
- next evidence must be stateful replenishment / CHARGER-SIEGER interaction, not more static HP-only math.

## Rogue

```text
12 / 16 / 20 real Dagger Storm projectiles
working center = 16
per-dagger continuity anchor = .45
```

Compared with the approved Lv26 P×P package (`3.25` root-basis units):

```text
12 = 5.40 = 1.66× Lv26
16 = 7.20 = 2.22× Lv26
20 = 9.00 = 2.77× Lv26
```

16 remains the working center, not a freeze.
Future 4-Rogue simultaneous 48/64/80 projectile volumes are performance stress targets, not automatic nerf triggers.

## Tank
Working center for temporal probe:

```text
shockwave damage = .75 root basis
knockback = ×2.5
barrier candidate = 250 / 6s
```

Static probe suggests ~1.2–1.3s mean base-translation time gained on survivors, but this understates actual stateful value because CHARGER WINDUP and SIEGER positioning have explicit cancel/reposition semantics.

## Archer — important correction
Approved identity remains:
- one huge strict-line Sky-Piercing Arrow;
- unlimited target count;
- armor ignore;
- no homing/bending/off-line retarget.

Proposal-93 `1.00` per-target center is no longer suitable.

Reason:
- Lv26 Triple Shot aligned durable-target package = `1.00+.65+.65 = 2.30` per target;
- Lv31 at 1.00 would be only 43.5% of that durable-target burst;
- it would need ~12 aligned targets to match the ideal Lv26 five-target package.

Next P4-D2 continuity center:

```text
2.30 root basis per intersected target
```

This preserves Lv26 per-target package continuity and lets **unlimited depth** create the final escalation.
At depth5 = Lv26 ideal package parity; depth8 ≈1.60×; depth12 ≈2.40×.

2.30 is not frozen.

## Mage
Working center:
- direct primary impact;
- fixed three-stage collapse;
- `.75` per stage;
- radius independent;
- one bounded final chain generation.

Static `.55/.75/1.00` often saturates provisional ordinary HP and cannot identify the final coefficient. Temporal replenishment, radius/geometry and SPLITTER chronology must decide it.

---

# Cross-class identity result

Current centers preserve differentiation:

```text
Knight = bounded frontline corridor break
Rogue  = sequential tracking multihit cleanup
Tank   = time/control/wall-safety reset
Archer = strict-line unlimited-depth deletion
Mage   = fixed-area density collapse
```

This is a PASS directionally.
Stage46+ must rotate mixed sequential geometry rather than permanently favor one shape.

---

# High-mastery temporal anchor

Real-device upper-tail stress traces:

```text
H0: 16 completed P×P / ~71.8s   -> ~4.49s per P×P
H3: 14 completed P×P / ~65.649s -> ~4.69s per P×P
```

These are not ordinary-skilled population fits.

Use them only to start the next bounded temporal pressure probe around a **non-frozen 4–5s dangerous-pressure reaccumulation envelope**.

Desired temporal behavior:

```text
Lv26-only -> backlog trends upward / cannot indefinitely stabilize
Lv31 + successful P×P -> clear pressure reset
one missed P×P -> serious backlog, potentially recoverable in 46–47
two/repeated missed P×P -> burial cascade by mastery band intent
```

Do not freeze 4–5s as final spawn cadence.

---

# Next stateful probe must include

1. current nine-monster provisional anchors only;
2. sustained staggered inflow, not a single static snapshot;
3. Lv26-only / Lv31-all-success / one-miss / two-consecutive-miss comparisons;
4. backlog before/after final and reaccumulation time;
5. CHARGER WINDUP cancellation/re-arm;
6. SIEGER standoff/first-shot/reposition;
7. SPLITTER immediate child spawning and chronological later hits;
8. SUPPORTER ×1.18 movement composition;
9. mixed line/cluster/frontline/dispersed geometry;
10. no exact Stage46 content freeze.

Required metrics:

```text
backlog_before_final
backlog_after_final
pressure_reset_fraction
seconds_to_reaccumulate_pre_reset_pressure
lv26_only_backlog_slope
lv31_backlog_slope_between_resets
missed_pxp_recovery_probability
consecutive_missed_pxp_to_burial
wall_hp_delta_between_resets
role_expression_count_before_death
charger_windup_count
charger_interrupt_count
sieger_first_shot_count
sieger_reposition_count
splitter_child_population_delta
```

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
STAGE46_PRESSURE_INSUFFICIENT_FOR_LV31
PXP_COMBO_MAINTENANCE_MASTERY_PRESSURE
ROGUE_DAGGER_STORM_EVENT_VOLUME_PERFORMANCE_WATCH
```

A large Lv31 power cliff is intentional and is not by itself a FAIL.

---

# R2 / EXP remains open

Pure per-valid-turn EXP remains provisional diagnostic baseline only.

Not frozen:
- final EXP semantics;
- Stage Quality Budget / Option D;
- exact XP_CREDIT / A31;
- Stage46 possession threshold;
- hidden class/Tier/player-count corrections.

Mandatory P10R remains required after credible multiplayer scaling.

---

# Stop conditions

P4-D2 may continue autonomously unless evidence requires:
- changing a class Lv31 identity/effect topology;
- adding code-level Lv31 gate;
- hidden class/player-count EXP correction;
- freezing exact Stage46 possession threshold;
- changing final EXP semantics;
- production implementation/numerical freeze.

Provisional magnitude adjustment inside an already-approved identity can remain within P4-D2 as long as it is explicitly unfrozen.

---

# Do not yet

- freeze Archer at 2.30;
- freeze Rogue at 16 daggers;
- freeze Stage46 at 97/98/99%;
- freeze 4–5s as exact spawn cadence;
- freeze exact Stage46–50 encounter content;
- change/deploy production gameplay;
- freeze final EXP;
- start P5 before P4-E closure.
