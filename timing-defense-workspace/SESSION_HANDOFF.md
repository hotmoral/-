# Timing Defense — Session Handoff

Updated: 2026-10-26 KST

## 0. Authority rule

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

Always fetch live `timing-defense-workspace` before acting. A new session is not a reason to rerun closed evidence.

## 1. Recovery order

1. live `timing-defense-workspace` HEAD;
2. `PROJECT_STATUS.md`;
3. `NEXT_WORK.md`;
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_62.yaml`;
5. D1 closure doc185;
6. C1 approval doc184 and closure doc183;
7. Stage16/17 approval doc182;
8. B1 closure doc181;
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
Stage15-31 = CANONICAL CONTIGUOUS EXACT AUTHORING WINDOW

D1 Stage32 candidate static = PASS
D1 persistent Stage15-33 dynamic = PASS_WITH_WATCHES
D1 user adoption = PENDING

production gameplay = UNCHANGED / UNAUTHORIZED
full Stage1-50 exact recipe freeze = DEFERRED

CURRENT = T1_D1_STAGE32_AUTHORING_ADOPTION_DECISION_GATE
```

## 3. D1 exact candidate

Path:
`legacy-game-structure/data/t1_contiguous_32_d1_candidate_v0_1.yaml`

SHA256:
`91909c0b9be28003a8fdcbafd3ad65b325ed9b2247524e810f950bd3541d45d8`

```text
Stage32
E02 / F04 / CD04 / C2 / RUSH
RUNNER 0ms    y=.28
GRUNT  180ms  y=.70
RUNNER 360ms  y=.42
GRUNT  2200ms y=.66
RUNNER 2380ms y=.32
GRUNT  2560ms y=.74
RUNNER 4700ms y=.40
GRUNT  4880ms y=.68
RUNNER 5060ms y=.30
```

The candidate is validated but **not adopted**.

## 4. Static evidence

```text
run 40331569664
artifact 12653329249
exact HEAD 20f5a4cc16c920bdfe86b1a0a3110284ff7c4ef4
artifact SHA256 2107ce835dcba4ae1e7cc06bd8baf08f3ab2b907dcdd0db0ea9df9e133700290
candidate SHA256 91909c0b9be28003a8fdcbafd3ad65b325ed9b2247524e810f950bd3541d45d8
materialized Stage15-33 SHA256 47f02889b659dcad7988645fcc6e11381de38607657bd7751d7387856dba5466

PASS
errors=[] warnings=[]
referenceIntegrity=PASS
authorityPreserved=true
contiguous15to33=true
rotation31to33Preserved=true
```

Static counts:

```text
S31 8 / max4s 8
S32 9 / max4s 6
S33 12 / max4s 8
```

## 5. Dynamic evidence

Accepted run:

```text
run 40332410094
artifact 12653794932
exact HEAD b34bb2432797dc0d6ae5e8135072b19dd3ebaa85
artifact SHA256 bfb0333d7773fee53a03f67025d8a295fee3b332f7a0ded9b6f251853b1aba52
runner SHA256 1a6a15ae228a3d7c674678479a0049979e40f59f025b09221abceda8b2938a87
dynamic-result SHA256 550271fe67fc46f67a5671276bbec8ebe6e98adbd51a3a3b5ce7f723ed2bb688
```

Variants:

```text
Lv16@18 vs Lv16@21
× Lv21@25 vs Lv21@28
× Lv26@32 vs inactive through Stage33
```

5 classes × 5 seeds × 8 variants = 200 cases.

Admission:

```text
PASS_DYNAMIC_DIAGNOSTIC_ONLY
200/200 complete through Stage33
3800 Stage rows
terminal failures = 0
exact materialized identity PASS
persistent continuity PASS
deterministic replay PASS
settlement/carry invariants PASS
all error arrays = []
```

Stage31-33:

```text
S31 wall 0 / actions 7.700 / settle 7.3963 / peak 4.510
S32 wall 0 / actions 8.305 / settle 8.1189 / peak 4.230
S33 wall 0 / actions 9.010 / settle 8.9018 / peak 6.205
```

Therefore:

```text
S31->32 tempo demand increase SUPPORTED
S32 tempo role distinct from S33 density SUPPORTED
S32->33 density escalation SUPPORTED
objective safety in bounded sample SUPPORTED
```

Paired Lv26@32 minus inactive-through-33:

```text
S32 wall delta 0 / actions -0.21 / settle -0.2260s
S33 wall delta 0 / actions -0.46 / settle -0.4046s
```

This does not freeze the exact Lv26 activation Stage.

## 6. Superseded first dynamic invocation

Run `40331982731` failed only after simulation because two result-metadata Python literals used `false` instead of `False`. The candidate/runtime were not changed. The corrected accepted run above supersedes it.

## 7. Progression authority

```text
Lv16 = Stage18-21 calibration-candidate band
Lv21 = Stage25-28 calibration-candidate band
Lv26 = Stage32-36 calibration-candidate band
```

No exact EXP threshold is frozen.

## 8. Active watches

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

No new D1 watch was added.

## 9. Current decision gate

Ask exactly:

```text
ADOPT STAGE32 EXACT SPAWN CANDIDATE
AS CANONICAL T1 AUTHORING BASELINE WITH WATCHES?
```

Evidence recommendation:
`ADOPT`

If approved:
- create user-approved Stage32 baseline source;
- promote canonical contiguous exact window to Stage15-33;
- retain watches;
- advance the active plan;
- sync canonical docs;
- then select the next smallest bounded exact-authoring gap from live authority.

Approval does not authorize production, scalar changes, exact Lv26 unlock Stage, final EXP/P×P/shop values, or full T1 Stage1-50 exact freeze.
