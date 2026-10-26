# Timing Defense — Project Status

Updated: 2026-10-26 KST

## Authority rule

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

A new session is not a reason to rerun closed work. Reopen only on a concrete trigger: relevant source/commit change, exact-byte requirement, mismatch, active-watch materialization, coupled-layer change, or contradictory evidence.

## Branch authority

- canonical/planning: `timing-defense-workspace` — fetch live HEAD first.
- shared production: `timing-defense-cloudflare-do-poc` — last verified `224dce9170aa9a45ed932b2ee97f3e1ea42d0558`.
- calibration harness: `timing-defense-skilled-v2-harness-v01` — last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`.
- Timing Defense production gameplay changes remain unauthorized.

## Canonical late-T1 chain

```text
174  Stage49-50 user-approved structural authoring baseline
180  Wave A exact-spawn authoring baseline user approval
181  contiguous Stage15-25 B1 dynamic admission and closure
182  Stage16-17 exact-spawn authoring baseline user approval
183  contiguous Stage15-31 C1 static/dynamic admission and closure
184  Stage26-28 exact-spawn authoring baseline user approval
185  contiguous Stage15-33 D1 static/dynamic admission and closure
186  Stage32 exact-spawn authoring baseline user approval
187  contiguous Stage15-38 E1 technical admission and closure
```

Active plan:
`legacy-game-structure/data/system_dependency_calibration_order_v0_64.yaml`

## Current phase

```text
Initial campaign = FOUR TIER / USER APPROVED
T1 roster = GRUNT / RUNNER / BRUTE / USER APPROVED
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES

Stage49-50 = USER APPROVED AUTHORING BASELINE WITH WATCHES
Wave A [1,4,8,15,19,24,25,29,30,31,33,37,38] = USER APPROVED AUTHORING BASELINE WITH WATCHES
Stage16/17 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage26/27/28 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage32 = USER APPROVED EXACT-SPAWN AUTHORING BASELINE WITH WATCHES
Stage15-33 contiguous exact authoring window = CANONICAL

E1 Stage34-36 v0.2 = TECHNICALLY VALIDATED / USER ADOPTION PENDING
Stage15-38 exact materialized evidence = PASS_WITH_WATCHES
full exact T1 Stage1-50 recipe freeze = DEFERRED
production semantics = UNCHANGED / UNAUTHORIZED

CURRENT = T1_E1_STAGE34_36_AUTHORING_ADOPTION_DECISION_GATE
```

## E1 validated candidate

Plan:
`legacy-game-structure/data/t1_contiguous_34_36_e1_authoring_plan_v0_2.yaml`

Candidate:
`legacy-game-structure/data/t1_contiguous_34_36_e1_candidate_v0_2.yaml`

```text
candidate SHA256
da4624a55c327fa68f71bd92b6626fee5e30fd5ddd2d6369403dd6d8b6715550

materialized Stage15-38 SHA256
58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d
```

Exact candidate summary:

```text
S34 = B,R,G,R,B,R,G,R @ 0,550,1100,1650,3300,3850,4400,4950ms
S35 = G,G,G,G         @ 0,800,2400,3200ms
S36 = B,G,G,B,G,G,B   @ 0,250,500,2800,3050,3300,6000ms
```

Exact Y placements are in candidate v0.2 and doc187.

E1 v0.1 was technically valid but superseded because Stage35 did not behave as recovery. v0.2 changes Stage35 only.

Retained evidence:

```text
static run 40336925232 / artifact 12657965202 = PASS
dynamic run 40337357872 / artifact 12658500115 = PASS_WITH_WATCHES
300/300 completed Stage15->38
7200 Stage rows
terminal failures = 0
Stage34-38 wall damage = 0
continuity/replay/settlement errors = 0
Stage35 recovery intent = SUPPORTED
```

No new watch was created by E1.

## Progression authority

```text
Lv16 = Stage18-21 calibration-candidate reach band
Lv21 = Stage25-28 calibration-candidate reach band
Lv26 = Stage32-36 calibration-candidate reach band
```

Lv26 Stage32/34/36 positions were diagnostic only; no exact EXP unlock Stage is frozen.

## Active watches

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

## Current decision gate

```text
E1 technical = CLOSED / PASS_WITH_WATCHES
Stage34-36 candidateAdopted = false
user adoption = PENDING
canonical contiguous exact window = Stage15-33
validated materialized evidence window = Stage15-38
```

If the user adopts Stage34-36 v0.2, the canonical contiguous exact-authoring window becomes **Stage15-38**, because Stage37 and Stage38 are already user-approved Wave A exact authorities.

Recommendation:
`ADOPT_STAGE34_36_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES`

No further authoring package begins before this decision.
