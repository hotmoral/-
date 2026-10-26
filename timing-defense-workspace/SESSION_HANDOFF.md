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
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_65.yaml`;
5. E1 approval doc188;
6. E1 closure doc187;
7. D1 approval/closure docs186/185;
8. C1 approval/closure docs184/183;
9. Stage16/17 approval doc182 and B1 closure doc181;
10. Wave A approval doc180;
11. Stage49-50 approval doc174;
12. F1 plan `legacy-game-structure/data/t1_stage39_40_existing_exact_promotion_preflight_v0_1.yaml`.

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
Stage34/35/36 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage15-38 = CANONICAL CONTIGUOUS EXACT AUTHORING WINDOW

E1 persistent Stage15-38 dynamic = PASS_WITH_WATCHES
production gameplay = UNCHANGED / UNAUTHORIZED
full Stage1-50 exact recipe freeze = DEFERRED

CURRENT = T1_F1_STAGE39_40_EXISTING_EXACT_PROMOTION_PREFLIGHT
```

## 3. E1 approved exact authority

Approval:
`legacy-game-structure/188_T1_STAGE34_36_EXACT_SPAWN_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`

Plan:
`legacy-game-structure/data/t1_contiguous_34_36_e1_authoring_plan_v0_2.yaml`

Candidate:
`legacy-game-structure/data/t1_contiguous_34_36_e1_candidate_v0_2.yaml`

Candidate SHA256:
`da4624a55c327fa68f71bd92b6626fee5e30fd5ddd2d6369403dd6d8b6715550`

Materialized Stage15-38 SHA256:
`58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d`

Canonical exact recipes:

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

## 4. E1 retained evidence

E1 v0.1 passed technical invariants but Stage35 failed the intended recovery role because its action/settle demand exceeded Stage34. Only Stage35 was revised; Stage34 and Stage36 remained unchanged.

Accepted v0.2 static:

```text
run 40336925232
artifact 12657965202
exact HEAD 06e4c1e44a890a8ef389c80c9123988e88cdb5e2
PASS
candidate SHA da4624a55c327fa68f71bd92b6626fee5e30fd5ddd2d6369403dd6d8b6715550
materialized Stage15-38 SHA 58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d
```

First v0.2 dynamic invocation `40336925635` is superseded because of a stale expected materialized-SHA constant in the runner only.

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

## 7. Current F1 package

Plan:
`legacy-game-structure/data/t1_stage39_40_existing_exact_promotion_preflight_v0_1.yaml`

The next two contiguous Stages already have exact candidates in:
`legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`

They are not user-approved canonical authority.

Current known candidate identities:

```text
S39 = E02+E03 / R+B / F08 / CD05 / C3 / RUSH+BULWARK
      rare late-T1 synthesis peak
      9 authored units

S40 = E01+E02+E03 / G+R+B / F01+F03 / CD03 / C2 / BASELINE
      Star Gate B broad known-vocabulary check
      10 authored units
```

F1 is an **existing-authority recovery/promotion preflight**, not a new-authoring package.

Required sequence:

```text
1. recover current Stage39/40 exact source identity from live remote
2. recover historical representative exact/pressure-shape evidence and identify the latest applicable authority
3. verify skeleton/signature/density/reference integrity
4. preserve Stage15-38 canonical authority unchanged
5. if valid, materialize Stage15-40
6. decide minimum persistent dynamic admission needed for promotion
7. if required, execute real Stage15-40 lifecycle with STAGE_SETTLED boundaries
8. only then open explicit Stage39/40 user adoption gate
```

Do not reauthor Stage39/40 unless a concrete mismatch requires it. Any canonical promotion requires explicit user approval. If later adopted, the contiguous exact-authoring window becomes Stage15-40.

## 8. Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE15-38 IS CANONICAL EXACT AUTHORITY
STAGE_SETTLED REQUIRES DELAYED EVENT QUEUE DRAINAGE
AUTHORED 4s NORMAL DENSITY <= 8
NO STAGE39/40 REAUTHORING WITHOUT EVIDENCE MISMATCH
NO CLASS/MONSTER SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO EXACT LV26 UNLOCK FREEZE
NO PRODUCTION GAMEPLAY CHANGE
NO FULL T1 STAGE1-50 EXACT FREEZE
```
