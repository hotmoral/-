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
12. `legacy-game-structure/90_P4D1_LV31_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md` only for superseded proposal context
13. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
14. `SKILL_PLAN_LV6_31.md`
15. `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
16. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
17. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
18. current production branch head and calibration-harness head
19. older P4-A/P4-B/P3 evidence only as needed for causal context/revalidation triggers

Important:
- proposal 90 is superseded for current direction by approved document 91.
- document 93 is first-pass P4-D2 analytic evidence, not numerical-freeze authority.
- do not re-run closed P1/P2/P3/P4-C1/C2 solely because a new session starts.
- production remains unchanged unless separately authorized.

Live remote always wins.

---

# Branch checkpoints

Planning:
- branch `timing-defense-workspace`
- exact final HEAD must be re-fetched after sync; copied SHA is only a checkpoint.

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
P4-D2 = ACTIVE / FIRST-PASS POWER ENVELOPE COMPLETE / FULL FEEDBACK CONTINUES
production changes = UNAUTHORIZED
```

Current exact next work:
**continue P4-D2 from document 93 into bounded current-roster pressure-response probes.**

No user decision is currently required unless a document-92 stop condition is hit.

---

# P4-D1 approved correction

The user explicitly redirected Lv31 away from a conservative balance-first interpretation.

Approved philosophy:

```text
Lv31 must be spectacular and class-defining
+
finite / deterministic / attributable effect graph
+
Stage46+ pressure rises to require/absorb Lv31 power
```

Do not confuse `bounded graph` with `few attacks`.
A class may have many explicit final-skill projectiles/hits if that is its identity.

Performance must be measured and engineered before being used as a reason to reduce class fantasy.

---

# Stage46+ mastery-gate direction

Approved structure:

```text
Stage41..45 = Lv31 acquisition / transition
Stage46     = major pressure jump
Stage46..47 = power-revelation band
Stage48..49 = mastery-pressure band
Stage50     = full-kit final application
```

A Lv31-less intended-skilled player may be buried by real encounter pressure because Lv26 clearing capacity cannot keep up.
This is allowed.

Do not add a code-level level requirement.

Combo/timing/P×P maintenance is an intended late-game difficulty dimension.

Acquisition fairness requirement:
- 90% Stage46 possession was judged too lenient as an intended-skilled target;
- P4-D2/P4-E may test 97/98/99% Stage46-entry possession checkpoints;
- none is frozen yet;
- class kill-speed/EXP opportunity/team/player-count effects must not make the gate unfair.

---

# Rogue Lv31 — active first-pass bracket

Rogue must culminate its multihit/thrown-projectile fantasy.

P4-D2 sensitivity:

```text
12 / 16 / 20 real Dagger Storm projectiles
working center = 16
```

Using provisional per-projectile coefficient `0.45`:

```text
Lv21 Blade Barrage = 2.80 root-basis package
12 daggers = 5.40 = 1.93× Lv21 package
16 daggers = 7.20 = 2.57× Lv21 package
20 daggers = 9.00 = 3.21× Lv21 package
```

Future 4-Rogue simultaneous event-volume targets implied by this bracket:

```text
48 / 64 / 80 projectiles
```

These are performance-test targets, not automatic nerf triggers.

Structural rules:
- one root-owned finite deterministic storm package;
- real visible/simulated projectiles/hits;
- target persistence while alive;
- deterministic retarget after death/removal;
- no same-target cap;
- boss scalar per realized hit;
- no recursive generator tree.

16 and 0.45 remain provisional.

---

# Other Lv31 first-pass magnitude envelope

Current P4-D2 analytic bracket from document 93:
- Knight second wave `0.75 / 1.00 / 1.25` root basis.
- Tank shockwave `0.50 / 0.75 / 1.00` root basis plus strong control/wall protection.
- Archer starts at `1.00` root basis per intersected target with unlimited strict-line depth.
- Mage three-stage collapse `0.55 / 0.75 / 1.00` root basis per stage, radius tuned independently.

All are provisional P4-D2 sensitivity inputs.

---

# Stage46 pressure-response target

Do not freeze raw monster multipliers first.
Calibrate backlog/reset behavior:

```text
Lv26-only sustained clearing < Stage46+ inflow/pressure
successful Lv31 P×P = unmistakable pressure reset
one missed reset = serious but potentially recoverable pressure
repeated missed resets = burial cascade
```

Required future metrics:

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
STAGE46_LV31_ACQUISITION_FAIRNESS
STAGE46_LV31_ABSENCE_BURIAL_BEHAVIOR
STAGE46_PRESSURE_INSUFFICIENT_FOR_LV31
PXP_COMBO_MAINTENANCE_MASTERY_PRESSURE
ROGUE_DAGGER_STORM_EVENT_VOLUME_PERFORMANCE_WATCH
```

A large Lv31 power cliff is intentional and is not by itself a FAIL.

---

# R2 / EXP state remains unchanged

Pure per-valid-turn EXP remains a provisional diagnostic baseline only.

Not frozen:
- final EXP semantics;
- Stage Quality Budget / Option D;
- exact XP_CREDIT / A31;
- Stage46 possession threshold;
- hidden class/Tier/player-count corrections.

Mandatory P10R remains required after credible multiplayer scaling.

---

# Stop conditions

P4-D2 may iterate without repeated user approval until one of these is required:
- change a class Lv31 identity;
- add code-level Lv31 gate;
- introduce hidden class/player-count EXP correction;
- freeze exact Stage46 possession threshold;
- change final EXP semantics;
- authorize production implementation/numerical freeze.

Otherwise continue bounded P4-D2 work autonomously.

---

# Do not yet

- freeze Rogue at 16 daggers;
- freeze Stage46 at 97/98/99%;
- freeze exact Stage46–50 encounter content;
- change/deploy production gameplay;
- freeze final EXP;
- start P5 before P4-E closure.
