# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Always fetch live remote first. Do not reconstruct current state from chat, memory or copied SHA alone.

Read/check in this order:
1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CHARACTER_PROFILE_RADAR_V1.md`
5. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
6. `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
7. `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
8. `legacy-game-structure/data/system_dependency_calibration_order_v0_29.yaml`
9. `legacy-game-structure/137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
10. `tools/run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1.py`
11. `legacy-game-structure/136_P5_IDENTITY_AWARE_STAGE46_49_INTEGRATED_RUNNER_PREFLIGHT_V0_1.md`
12. `tools/run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py`
13. `legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json`
14. `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
15. `legacy-game-structure/134_P5_KNIGHT_PENETRATION_ROBUST_IDENTITY_PROBE_V0_1.md`
16. `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
17. `legacy-game-structure/132_P5_TANK_CONTROL_CLEAR_PARETO_DIRECTION_V0_1.md`
18. `legacy-game-structure/133_P5_ROGUE_DAGGER_STORM_BROAD_CLEANUP_BREAKPOINT_V0_1.md`
19. `legacy-game-structure/131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`
20. `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
21. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
22. `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
23. `legacy-game-structure/127_P5_STAGE46_49_RIGHT_EDGE_TRAVEL_LEAD_PREFLIGHT_V0_1.md`
24. current production/harness heads

Live remote always wins.
Do not rerun closed P1/P2/P3/P4 or the class-identity diagnostic group wholesale because of session restart.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- fetch exact live HEAD after recovery; never trust the handoff SHA as current truth.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- unchanged by current P5 planning work.

A temporary diagnostic execution branch was used only for exact GitHub-checkout runs:
- `timing-defense-p5-integrated-exec-temp-20261023`
- it has no planning or production authority.

---

# Current exact phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE / STAGE_SETTLED transition authority
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 = USER_APPROVED
P5 class identity diagnostic group = DIRECTIONALLY CLOSED
P5 integrated runner = CHECKOUT-EXACT PASS / DETERMINISTIC
P5 60s boundary backlog discard = MATERIAL / INVALID FOR STAGE-CLEAR RESERVE
P5 Stage46-49 interpretation = STAGE_SETTLED REQUIRED
P5 current Stage48 proxy packet = NOT ADMISSION-READY
P5 simple BRUTE/SHIELD substitution = INSUFFICIENT
P5 next = REAL-MONSTER ESCORT CHRONOLOGY BOUNDED SEARCH
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No new Stage48 packet is approved.
No Tank scalar is selected.
No numerical value is frozen.

---

# Structural flow that must remain in mind

Do not treat skills, shop, encounters or wall state as isolated systems.
For every active P5 change/probe, review at least:

```text
class identity
-> action/skill behavior
-> shop growth direction
-> enemy chronology/frontmost geometry
-> wall contact/SIEGER exposure
-> Stage clear condition
-> STAGE_SETTLED transition
-> persistent wall deficit
-> Stage46 power revelation / Stage47 recovery / Stage48 pulse / Stage49 escalation
-> downstream P6 readiness
```

At each slice check:
- upstream contract consistency;
- downstream impact;
- feedback loops and nonlinear breakpoints;
- class asymmetry/fairness;
- determinism/replay attribution;
- scope/cost;
- production boundary.

Use bounded probes before broad re-audits.
Do not reopen a closed result unless a concrete trigger exists.

---

# Stable P5 A2 truth

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ordinary-monster coin baseline
ALL-HUMAN Stage-clear income-floor candidate
FORTIFICATION = max HP + matched current increase
ATK/CRIT/CRITDMG/KNOCK personal
FORTIFICATION/DEF purchases contribute to shared wall
six categories retained
NO_ROUTINE FULL-SHOP MAXOUT BY STAGE49
```

Working diagnostics only:

```text
full-shop Rank10 reference = 16360
spend capacity center = 50%
income source center = 70/30
cross-class ATK/FORT/DEF diagnostic magnitude = 40% legacy-relative
```

The integrated runner uses a fixed representative late-segment shop snapshot only to isolate identity/chronology/wall-deficit behavior.
Do not reinterpret it as an approved purchase history.

---

# Stage transition authority

Approved P3 semantics:

```text
last authored Stage spawn occurred
+ no live Stage-owned enemy remains
+ no new current-Stage player turn accepted
+ already-authorized action/effect drained
+ no unresolved half-Heavy/delayed hit/transient
= STAGE_SETTLED
```

Then and only then:

```text
Stage clear
-> shop/progression
-> Stage-local enemy/transient reset
-> next Stage
```

Persistent run state such as current/max wall HP and absolute damage deficit carries forward as already contracted.

Reject both shortcuts:

```text
60s -> delete living enemies -> next Stage      = WRONG
60s -> carry living enemies into next Stage     = WRONG
```

---

# Exact integrated runner admission

Asset:
`tools/run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py`

Exact checkout run:

```text
run id 39949346908
repeat output SHA256
0d08f52ad5a25049e3379831bb4a41e7dc63256d7675d3743a1891dfba35a45b
```

PASS:
- import/source patch;
- deterministic repeat;
- normal right-edge physical spawnX 0.92;
- no mid-field pop-in.

Targeted exact identity references:

```text
Knight BALANCED       aligned 8.080 / dispersed 10.331
Knight DEFENSE_HEAVY  aligned 8.226 / dispersed 12.728
Archer BALANCED       aligned 3.580 / scatter 8.075
Archer ATTACK_HEAVY   aligned 3.580 / scatter 8.075
Mage BALANCED         cluster 3.780 / distributed 8.080
Tank finite mixed:
  .20 21.578s
  .25 18.209s
  .30 14.829s
```

These do not trigger wholesale class-identity reopening.

---

# Rogue watch

At 40% diagnostic shop scale:

```text
fresh GRUNT  = one Dagger Storm dagger can kill
fresh RUNNER = one dagger can kill
fresh SHIELD = not one-dagger killed
```

Exact integrated telemetry shows broad distinct-target cleanup in some Storms.

Keep:
`ROGUE_STORM_SINGLE_DAGGER_ORDINARY_ONESHOT_NOT_ROUTINE`.

Do not remove deterministic retarget as first repair.

---

# Stage-boundary exact result

The exact 60s integrated runner had material `endActive` at many synthetic Stage boundaries, especially Tank.

Therefore:

```text
P5_STAGE_BOUNDARY_BACKLOG_DISCARD_BIAS = TRIGGERED
```

Do not use its final wall reserve as exact Stage-clear reserve.

Canonical follow-up runner:
`tools/run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1.py`

Exact evidence run used the same tested algorithm before promotion:

```text
run id 39950165809
repeat output SHA256
2680ec99b9aecbc27eca9c647b6c95057780306eab2acf884b511581d3a95e0d
```

---

# Stage48 failure and root cause

Current Stage48 repeated diagnostic packet contains approximately:

```text
23 ARMORED_DURABLE_PROXY
10 CHARGER
10 RUNNER
11 SIEGER
```

`ARMORED_DURABLE_PROXY` is not a production monster.
It was created in the Knight identity lane only:

```text
HP 1600
armor 0.55
```

Under correct STAGE_SETTLED semantics:

```text
Mage BALANCED      buried ~67.375s
Mage ATTACK_HEAVY  buried ~76.100s
Mage DEFENSE_HEAVY buried ~71.200s
Mage ROLE_AWARE    survives but ends ~226.1 wall
```

Meanwhile Knight/Rogue/Archer are often nearly untouched.
This is a packet cross-contamination problem, not evidence to buff Mage.

Factor isolation exact run:

```text
run id 39951028213
repeat SHA256
a8e303f35b2e713cf7f7d1e2d1f98b91f865631c39c2f81bbd4157bc49e057f3
```

Findings:
- current proxy pressure mostly comes from proxy wall contact/durability threshold, not SIEGER uptime;
- BRUTE substitution -> nearly harmless, SIEGER 0 shots;
- SHIELD substitution -> nearly harmless, SIEGER 0 shots;
- BRUTE+SHIELD -> same;
- slower SHIELD cycle -> same;
- half proxy repetition -> all survive but Mage still uniquely loses large reserve;
- one proxy row -> pressure nearly disappears.

Conclusion:

```text
SIMPLE_BODY_SUBSTITUTION = NOT THE REPAIR
NEXT_REPAIR_AXIS = RELATIVE ENTRY TIMING / FRONTMOST SCREENING / CHRONOLOGY
```

Do not inflate real-monster stats merely to recreate proxy pressure.

---

# Class identity authority — preserve

Radar:

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Interpretation:
- high axes must remain reasons for success;
- low axes must remain limitations after growth;
- `SURVIVAL != CLEAR`.

Tank:
- .20/.25/.30 remain diagnostic only;
- .25 working center only;
- preserve knockback/slow/barrier/Iron Wall;
- do not select scalar until Stage48 contamination is removed.

Archer:
- no global nerf;
- old late issue remains chronology-sensitive.

Mage:
- cluster/density identity exact regression passed;
- do not buff to compensate for proxy contamination.

---

# Exact next boundary

1. fetch live workspace and confirm no newer relevant commit;
2. read doc137 and v0.29 before touching Stage48;
3. run a **bounded** Stage48 search with existing real monster archetypes only;
4. keep physical spawnX 0.92 and no mid-field pop-in;
5. change relative entry timing/frontmost ordering/band separation before stats;
6. look for actual SIEGER role uptime, not merely wall damage from escorts;
7. require successful representative survival with usable reserve across all classes/build directions;
8. preserve DEFENSE_HEAVY Knight viability, Mage density identity, Tank slow-clear identity, Rogue low-AOE weakness, Archer line identity;
9. after one or a few promising candidates, run Stage46→49 using STAGE_SETTLED semantics;
10. present the candidate/evidence/tradeoffs to the user **before adopting it as the working Stage48 direction**;
11. only after approval proceed to Stage49 chronology and later Tank scalar choice;
12. later KNOCK, CRIT/CRITDMG, real shop acquisition timing/EXP feedback, P10/P10R.

No production change is authorized.
No Stage48 candidate adoption is authorized yet.
