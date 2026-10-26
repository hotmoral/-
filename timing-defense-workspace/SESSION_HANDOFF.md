# Timing Defense — Session Handoff

Updated: 2026-10-26 KST

## 0. Authority rule

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

Always fetch the live branch before acting. A fresh session is not a reason to rerun accepted work.

## 1. Recovery order

1. live `timing-defense-workspace`;
2. `PROJECT_STATUS.md`;
3. `NEXT_WORK.md`;
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_64.yaml`;
5. E1 closure doc187;
6. D1 approval doc186 and closure doc185;
7. C1 approval/closure docs184/183;
8. Stage16/17 approval doc182 and B1 closure doc181;
9. Wave A approval doc180;
10. Stage49-50 approval doc174.

## 2. Current macro state

```text
Initial campaign = 4 Tiers / USER APPROVED
T1 roster = GRUNT / RUNNER / BRUTE / USER APPROVED
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES

Stage49-50 = USER APPROVED AUTHORING BASELINE WITH WATCHES
Wave A = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage16/17 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage26/27/28 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage32 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage15-33 = CANONICAL CONTIGUOUS EXACT AUTHORING WINDOW

E1 Stage34-36 v0.2 = TECHNICALLY CLOSED / PASS_WITH_WATCHES / USER ADOPTION PENDING
Stage15-38 = VALIDATED EXACT MATERIALIZED EVIDENCE WINDOW ONLY
production gameplay = UNCHANGED / UNAUTHORIZED
full Stage1-50 exact recipe freeze = DEFERRED

CURRENT = T1_E1_STAGE34_36_AUTHORING_ADOPTION_DECISION_GATE
```

## 3. E1 v0.2 candidate

Plan:
`legacy-game-structure/data/t1_contiguous_34_36_e1_authoring_plan_v0_2.yaml`

Candidate:
`legacy-game-structure/data/t1_contiguous_34_36_e1_candidate_v0_2.yaml`

Candidate SHA256:
`da4624a55c327fa68f71bd92b6626fee5e30fd5ddd2d6369403dd6d8b6715550`

Materialized Stage15-38 SHA256:
`58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d`

Exact candidate:

```text
S34: B,R,G,R,B,R,G,R
T  : 0,550,1100,1650,3300,3850,4400,4950ms
Y  : .46,.42,.49,.44,.46,.50,.43,.48

S35: G,G,G,G
T  : 0,800,2400,3200ms
Y  : .28,.70,.40,.66

S36: B,G,G,B,G,G,B
T  : 0,250,500,2800,3050,3300,6000ms
Y  : .46,.44,.48,.46,.45,.47,.46
```

## 4. E1 evidence and supersession chain

E1 v0.1:
- static and lifecycle invariants passed;
- 300/300 through Stage37;
- but Stage35 recovery product intent failed because actions/settle exceeded Stage34;
- v0.1 superseded without changing Stage34 or Stage36.

E1 v0.2 static:

```text
run 40336925232
artifact 12657965202
exact HEAD 06e4c1e44a890a8ef389c80c9123988e88cdb5e2
PASS
candidate SHA da4624a55c327fa68f71bd92b6626fee5e30fd5ddd2d6369403dd6d8b6715550
materialized Stage15-38 SHA 58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d
```

First v0.2 dynamic invocation `40336925635` was superseded before simulation due only to a stale expected materialized-SHA constant in the runner.

Accepted v0.2 dynamic:

```text
run 40337357872
artifact 12658500115
exact HEAD a66d961285ec40e43c080a1e87e08ce433d4fa38
300/300 complete Stage15->38
7200 Stage rows
terminal failures 0
continuity/replay/settlement errors 0
Stage34-38 wall damage 0
Stage35 recovery intent SUPPORTED
```

All-case means:

```text
S33 actions 9.0867 / settle 8.9692 / peak 6.2400
S34 actions 8.1900 / settle 7.9009 / peak 3.6533
S35 actions 6.2100 / settle 5.7993 / peak 2.5167
S36 actions 9.7433 / settle 9.7812 / peak 4.3300
S37 actions 7.2833 / settle 6.9152 / peak 5.5867
S38 actions 8.1967 / settle 8.0462 / peak 4.8000
```

No new E1 watch was added.

## 5. Progression authority

```text
Lv16 = Stage18-21 calibration-candidate band
Lv21 = Stage25-28 calibration-candidate band
Lv26 = Stage32-36 calibration-candidate band
```

Lv26 positions 32/34/36 are diagnostic only. No exact EXP threshold or unlock Stage is frozen.

## 6. Active watches

```text
T1_RUNNER_LV6_PEDAGOGIC_COLLISION_WATCH
T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH
T1_RUNNER_HIGH_PRESSURE_LV16_TAIL_WATCH
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
T4_SUPPORTER_SIEGER_LEARNING_DENSITY_WATCH
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
T1_STAGE49_50_OBJECTIVE_PRESSURE_ROTATION_WATCH
```

## 7. Current product-authority gate

```text
ADOPT STAGE34-36 E1 V0.2 EXACT SPAWN CANDIDATE
AS CANONICAL T1 AUTHORING BASELINE WITH WATCHES?
```

Recommendation:
`ADOPT_STAGE34_36_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES`

Until explicit approval:
- canonical contiguous exact window remains Stage15-33;
- Stage15-38 remains validated evidence only;
- candidateAdopted = false;
- do not start another authoring package.

If approved, Stage37 and Stage38 are already Wave A user-approved exact authorities, so the canonical contiguous exact-authoring window becomes Stage15-38 immediately.

## 8. Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE_SETTLED REQUIRES DELAYED EVENT QUEUE DRAINAGE
AUTHORED 4s NORMAL DENSITY <= 8
NO CLASS/MONSTER SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO EXACT LV26 UNLOCK FREEZE
NO PRODUCTION GAMEPLAY CHANGE
NO FULL T1 STAGE1-50 EXACT FREEZE
```
