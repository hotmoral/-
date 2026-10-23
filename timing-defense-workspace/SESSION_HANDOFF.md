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
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_17.yaml`
6. `legacy-game-structure/111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
7. `legacy-game-structure/110_P4D2_PROVISIONAL_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`
8. `legacy-game-structure/109_P4D2_EXACT_V05_AND_STAGE49_V02_REPLAY_ADMISSION_V0_1.md`
9. `legacy-game-structure/data/p4d2_v05_and_stage49_v02_exact_replay_admission_v0_1.json`
10. `legacy-game-structure/108_P4D2_STAGE46_LV31_ACQUISITION_FAIRNESS_PRECHECK_V0_1.md`
11. `legacy-game-structure/107_P4D2_ARCHER_SPLITTER_CHRONOLOGY_ROOT_CAUSE_V0_1.md`
12. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
13. `legacy-game-structure/88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
14. `legacy-game-structure/89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
15. `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
16. `legacy-game-structure/96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
17. `legacy-game-structure/99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md`
18. `legacy-game-structure/101_P4D2_ARMORED_DURABLE_PROXY_PRESSURE_PROBE_V0_1.md`
19. `legacy-game-structure/103_P4D2_TANK_BARRIER_FIDELITY_CORRECTION_V0_1.md`
20. `legacy-game-structure/106_P4D2_STAGE49_FULL_ROTATION_DIRECTIONAL_PROBE_V0_1.md`
21. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_5.py`
22. `tools/run_p4d2_stage49_full_rotation_probe_v0_2.py`
23. `tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py`
24. `legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json`
25. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
26. `SKILL_PLAN_LV6_31.md`
27. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
28. `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md` — P5 definition
29. current production/harness heads
30. older P4/P3 evidence only if a concrete P5 feedback or revalidation trigger requires it

Historical runner classification:

```text
v0.2 dynamic = historical pre-Tank-barrier-correction evidence only
v0.3 = failed source-patch guard; do not admit
v0.4 = failed substring-patch guard; do not admit
v0.5 = current exact-admitted fidelity runner
Stage49 v0.1 wrapper = v0.4-dependent historical directional wrapper
Stage49 v0.2 wrapper = current exact-admitted wrapper using v0.5
```

Do not rerun closed P1/P2/P3/P4 merely because a new session starts.

Live remote always wins.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- exact final HEAD must be fetched live after this sync.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- current P4 work did not change it.

---

# Current exact phase / boundary

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4-A = PASS_COMPLETE_MARKER_ONLY
P4-B = COMPLETE_WITH_ACTIVE_EXP_WATCHES / R2 USER APPROVED
P4-C1 = USER_APPROVED_STRUCTURAL_COMPLETE
P4-C2 = COMPLETE / PASS_WITH_WATCHES
P4-D1 = USER_APPROVED_WITH_MODIFICATION
P4-D2 = PROVISIONAL_STRUCTURAL_COMPLETE / PASS_WITH_WATCHES
P4-E = COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 = READY_NEXT_STRUCTURAL_REVIEW
production = UNCHANGED / UNAUTHORIZED
```

No user decision is currently pending before P5 authority recovery/structural review.

---

# P4 closure facts that must not regress

## Lv31 philosophy

```text
strong class-defining finals
+
finite deterministic attributable graphs
+
Stage46+ pressure strong enough to require/absorb them
```

No code-level Lv31 entry gate.

Current provisional centers — not frozen:

```text
Knight second wave1.00
Rogue 16 daggers ×.45
Tank shockwave.75 / KB×2.5 / barrier250-for-6s candidate
Archer2.30 / wider straight MID_ADJACENT diagnostic corridor
Mage stages.75 / radius1.25
```

Archer wider real gameplay corridor is USER APPROVED; do not silently revert it.

## Exact replay authority

```text
Stage46 kernel blob
5965833f80422bd6cae94fea738706baf99a06e8

v0.5 runner blob
8a548184272a71f3b17650f77e6d366533409e0c

v0.5 output SHA-256
29c5c7dc5a6c74f1e67f07d7eb0d8a3235e860817d7559227da26da192e2dae1

Stage49 v0.2 runner blob
1eb644766133d0a4e84130ab4d7be4c727cbee12

Stage49 v0.2 output SHA-256
c033d7fea455476ae2c4b9c0ffe4f770885d135533fd899a04709eb7cd0d6e02
```

Do not use v0.3/v0.4 as replay authority.

## Stage49 exact rotation signal

```text
rotation:
LINE_ESCORT
CLUSTER_RECOVERY
FRONTLINE_BREACH
DURABLE_SCATTER
TIME_BUDGET_SIEGER

all-success wall:
Knight1705 / Rogue2000 / Tank2000 / Archer2000 / Mage2000

all-finals-missed burial:
Knight34.025 / Rogue29.100 / Tank34.575 / Archer57.025 / Mage52.225 seconds
```

Class-specific mistake budgets are intentionally asymmetric.
Tank is a time-budget/control class, not a damage-parity target.

## Durable-pressure boundary

`ARMORED_DURABLE_PROXY` is diagnostic only and is not a tenth monster.
Do not stack extreme HP+armor+knock resistance as a Tank/Mage hard counter.
The BRUTE carrying/using SHIELD-like protection idea is saved for later monster identity/design work only.

## Archer chronology

Root cause explained:

```text
wide successful final kills SPLITTER parent earlier
-> children spawn earlier
-> same snapshotted arrow does not retroactively hit newborn children
-> child pressure clock advances
```

This is deterministic chronology, not an Archer power/width defect.
Keep only an authoring monotonicity watch.

## Stage46 acquisition / EXP

Marker-only P4-A shows Stage41-45 Lv31 acquisition is structurally feasible.
P4-B shows current pure per-turn EXP becomes class-divergent once skill-power feedback changes timing opportunities.

Therefore:

```text
97/98/99 Stage46 possession = sensitivity only
none is frozen
hidden class/Tier XP patch = unauthorized
final EXP/timebase convergence = P10R mandatory
```

P4-E recommendation: do not freeze P25/P75/P90 reach acceptance before P10R.

---

# Active P4 watches carried downstream

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
STAGE46_LV31_ACQUISITION_FAIRNESS
STAGE49_TO_50_WALL_RESERVE_CONTINUITY_WATCH
LV31_ARCHER_SUCCESS_MONOTONICITY_CHRONOLOGY_WATCH_ROOT_CAUSE_EXPLAINED
P4D2_ARCHER_ROLE_PULSE_GEOMETRY_WATCH
ROGUE_DAGGER_STORM_EVENT_VOLUME_PERFORMANCE_WATCH
```

These are carried watches, not reasons to reopen P4 without an actual trigger.

---

# Exact next work — P5

Package:

**RUN COIN / SHOP CANDIDATE — STRUCTURAL REVIEW BEFORE VALUES**

First actions:
1. inspect live legacy/canonical shop/coin documents and production implementation;
2. recover current shop cadence, coin award source/timing, upgrade categories, caps/ranks and BaseHP/DEF semantics;
3. classify each recovered rule by authority/provenance and identify contradictions;
4. do not change production;
5. produce a P5 authority matrix and exact unresolved decision list;
6. if material choices remain, present recommendation + user gate;
7. if not, draft the bounded P5 structural contract before numerical simulation.

P5 simulation later must compare:

```text
ATTACK_HEAVY
CRIT_HEAVY
DEFENSE_HEAVY
BALANCED
SAVE_DELAY
ROLE_AWARE candidate
```

Mandatory P5 feedback loop:

```text
shop power
-> kill speed / wall survival
-> timing-event opportunity
-> EXP / skill reach
```

Do not tune against one shop strategy only.

---

# Do not yet

- tune shop prices/coin income before structural recovery;
- freeze final EXP;
- freeze Stage46 possession97/98/99;
- freeze Stage49->50 wall reserve floor;
- freeze provisional Lv31 coefficients/width;
- promote durable proxy/BRUTE+SHIELD visual concept to an actual monster;
- solve P10 multiplayer scaling early;
- change/deploy production gameplay;
- rerun closed P4 evidence without a concrete P5 feedback trigger.
