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
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_60.yaml`;
5. `legacy-game-structure/183_T1_CONTIGUOUS_15_31_C1_DYNAMIC_ADMISSION_AND_CLOSURE_V0_1.md`;
6. Stage16/17 approval doc182;
7. B1 closure doc181;
8. Wave A approval doc180;
9. Stage49-50 approval doc174.

Do not reconstruct state from copied SHA/chat when live canonical sources are available.

## 2. Current macro state

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 shop = USER APPROVED
P5 class identity group = DIRECTIONALLY CLOSED
P5->P6 fidelity bridge = EXACT TEMP PASS
P6 = USER_APPROVED STRUCTURAL CLOSED WITH WATCHES

Initial campaign = 4 Tiers / USER APPROVED
T1 roster = GRUNT / RUNNER / BRUTE / USER APPROVED
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES

Stage49-50 = USER APPROVED AUTHORING BASELINE WITH WATCHES
Wave A = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage16/17 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage15-25 = CANONICAL CONTIGUOUS EXACT AUTHORING WINDOW

C1 Stage26-28 static = PASS
C1 persistent Stage15-31 dynamic = PASS_WITH_WATCHES
C1 user adoption = PENDING

production gameplay = UNCHANGED / UNAUTHORIZED
full Stage1-50 exact recipe freeze = DEFERRED

CURRENT = T1_C1_STAGE26_28_AUTHORING_ADOPTION_DECISION_GATE
```

## 3. Branch checkpoints

Canonical/planning:
- `timing-defense-workspace`
- fetch live HEAD first;
- exact C1 dynamic evidence HEAD: `80a4b42134100693fe161e02ef4e0c3828974ead`;
- later canonical-doc synchronization commits may be newer and should win.

Shared production:
- `timing-defense-cloudflare-do-poc`
- last verified `224dce9170aa9a45ed932b2ee97f3e1ea42d0558`
- Timing Defense production change remains unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`.

## 4. C1 exact candidate

Path:
`legacy-game-structure/data/t1_contiguous_26_28_c1_candidate_v0_1.yaml`

SHA256:
`63e40e635b47c54876778a1c64809e961b3929062e3279ea4a805fdf9d8760e4`

Stage26:

```text
2 BRUTE + 3 GRUNT
0 / 800 / 1600 / 2400 / 3200ms
Y 0.46 / 0.44 / 0.48 / 0.45 / 0.47
E03 / F01 / CD02 / C1 / BULWARK
```

Stage27:

```text
4 RUNNER + 3 GRUNT
0 / 250 / 500 / 2000 / 2250 / 3750 / 4000ms
Y 0.28 / 0.70 / 0.40 / 0.66 / 0.32 / 0.74 / 0.44
E02 / F04 / CD03 / C1 / RUSH
```

Stage28:

```text
GRUNT ×6
0 / 250 / 500 / 2000 / 2250 / 2500ms
Y 0.43 / 0.46 / 0.49 / 0.44 / 0.47 / 0.45
E01 / F03 / CD03 / C1 / BASELINE + FLOOD
```

The candidate is validated but **not adopted**.

## 5. C1 static evidence

```text
run 40324812125
artifact 12651020986
head 1acff948c6b8ff67f0cdaa1dd4c0e080e47c0346
artifact SHA256
e28b8bc65560907a953fb5f6cfbcf4d93266e3795cab4f866ee1d2761fec6335

candidate SHA256
63e40e635b47c54876778a1c64809e961b3929062e3279ea4a805fdf9d8760e4

materialized Stage15-31 SHA256
284426b71fe03e9838ae141d90422d3d0dec55ad55c71466a4a28bc1fc91297c
```

Result:

```text
PASS
errors = []
warnings = []
referenceIntegrity = PASS
authorityPreserved = true
contiguous15to31 = true
```

## 6. C1 dynamic evidence

```text
run 40325507618
artifact 12651550217
head 80a4b42134100693fe161e02ef4e0c3828974ead
artifact SHA256
ccb3a07f326ce57d3b9dd3056773e89cb5fc0fc790f6b542d62d3c1f15945b24
dynamic-result SHA256
11e183e23039eecc0ca1c3b2452f6f822e31f15b246db3b20c2cedd55e9a1dbc
```

Variants:

```text
Lv16@18 vs Lv16@21
×
Lv21@25 vs Lv21@28
```

5 classes × 5 seeds => 100 cases.

Admission:

```text
PASS_DYNAMIC_DIAGNOSTIC_ONLY
100/100 complete through Stage31
1700 Stage rows
terminal failures = 0
exact materialized identity = PASS
persistent continuity = PASS
deterministic replay = PASS
settlement/carry invariants = PASS
all fidelity/continuity/replay/invariant error arrays = []
```

## 7. Behavioral interpretation

All-case Stage25-31:

```text
S25 wall 0.00 / actions 7.06 / settle 7.1277 / peak 1.68
S26 wall 0.00 / actions 7.75 / settle 7.3919 / peak 3.67
S27 wall 1.08 / actions 7.93 / settle 7.6269 / peak 3.38
S28 wall 0.00 / actions 5.24 / settle 4.6966 / peak 3.77
S29 wall 0.00 / actions 11.73 / settle 11.7463 / peak 5.24
S30 wall 0.00 / actions 7.93 / settle 7.6640 / peak 4.24
S31 wall 0.00 / actions 7.70 / settle 7.3963 / peak 4.51
```

Therefore:

```text
S25->26 readable re-acceleration = SUPPORTED
S27 tempo focus = SUPPORTED WITH bounded Tank contact
S28 decompression = SUPPORTED
S28->29 strong C2 synthesis step-up = SUPPORTED
```

Tank-specific:
- only seed503 with Lv21 active from Stage25 produced S27 wall damage;
- 2 rows, 54 each, across the two Lv16 variants;
- Tank S27 mean across 20 cases = 5.4;
- other classes S25-31 wall damage = 0;
- no new watch required; retain `TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`.

## 8. Progression authority

```text
Lv16 = Stage18-21 calibration-candidate band
Lv21 = Stage25-28 calibration-candidate band
```

C1 tests both Lv21 band edges. It does not select an exact EXP threshold.

## 9. Current decision gate

Ask exactly:

```text
ADOPT STAGE26 + STAGE27 + STAGE28 EXACT SPAWN CANDIDATE
AS CANONICAL T1 AUTHORING BASELINE WITH WATCHES?
```

Current evidence recommendation:
`ADOPT`

Do **not** infer approval from this handoff or from a request to continue/review. Explicit approval is required.

If approved:
- create user-approved Stage26-28 baseline source;
- promote canonical contiguous exact window to Stage15-31;
- retain watches;
- advance plan;
- sync canonical docs;
- then choose the next smallest bounded package.

Approval does not authorize production, scalar changes, final EXP/P×P/shop values, exact Lv21 unlock Stage, or full T1 Stage1-50 exact freeze.

## 10. Active watches

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

No new C1 watch was added.
