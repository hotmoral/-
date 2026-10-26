# Timing Defense — T1 Stage32 Exact-Spawn Authoring Baseline User Approved V0.1

Date: 2026-10-26 KST  
Status: **USER APPROVED / CANONICAL T1 AUTHORING BASELINE WITH WATCHES / NO PRODUCTION OR NUMERICAL FREEZE**

## 0. Decision

The user explicitly approved the D1 Stage32 exact-spawn candidate after static and persistent Stage15->33 dynamic admission closed `PASS_WITH_WATCHES`.

Approved decision:

```text
ADOPT_STAGE32_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES
```

This closes:

```text
T1_D1_STAGE32_AUTHORING_ADOPTION_DECISION_GATE
```

Authority remains:

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

## 1. Exact candidate identity

Candidate:
`data/t1_contiguous_32_d1_candidate_v0_1.yaml`

Candidate SHA256:
`91909c0b9be28003a8fdcbafd3ad65b325ed9b2247524e810f950bd3541d45d8`

Materialized Stage15-33 SHA256:
`47f02889b659dcad7988645fcc6e11381de38607657bd7751d7387856dba5466`

Technical closure:
`185_T1_CONTIGUOUS_15_33_D1_DYNAMIC_ADMISSION_AND_CLOSURE_V0_1.md`

## 2. Canonical exact Stage32 authoring

```text
E02 / F04 / CD04 / C2 / RUSH
RUNNER 0ms    y=0.28
GRUNT  180ms  y=0.70
RUNNER 360ms  y=0.42
GRUNT  2200ms y=0.66
RUNNER 2380ms y=0.32
GRUNT  2560ms y=0.74
RUNNER 4700ms y=0.40
GRUNT  4880ms y=0.68
RUNNER 5060ms y=0.30
```

Composition = RUNNER x5 + GRUNT x4.  
Exact spawn count, timestamp, monster type and Y placement above are now canonical T1 authoring authority WITH WATCHES.

## 3. Retained evidence

Static admission:

```text
run 40331569664
artifact 12653329249
exact HEAD 20f5a4cc16c920bdfe86b1a0a3110284ff7c4ef4
status PASS
referenceIntegrity PASS
authorityPreserved true
contiguous15to33 true
rotation31to33Preserved true
```

Dynamic admission:

```text
run 40332410094
artifact 12653794932
exact HEAD b34bb2432797dc0d6ae5e8135072b19dd3ebaa85
200/200 completed through Stage33
3800 Stage rows
terminal failures 0
persistent continuity PASS
deterministic replay PASS
settlement/carry invariants PASS
```

The earlier run `40331982731` is superseded as a runner metadata defect only (`false` vs Python `False`) and has no candidate/runtime authority.

Behavioral interpretation retained:

```text
Stage31 -> Stage32 tempo demand increase = SUPPORTED
Stage32 remains below Stage33 density identity = SUPPORTED
Stage32 -> Stage33 density escalation = SUPPORTED
Stage31-33 objective safety = SUPPORTED in bounded sample
```

No new watch is created.

## 4. Canonical consequence

The canonical contiguous exact-authoring window is now:

```text
Stage15-33
```

Previously canonical Stage15-31 remains unchanged; approved Stage32 bridges directly into the already-approved Stage33 Wave A authority.

## 5. Progression boundary

Lv26 remains only:

```text
Stage32-36 calibration-candidate reach band
```

The diagnostic comparison of Lv26 active before Stage32 vs inactive through Stage33 does not select an exact activation Stage or EXP threshold.

## 6. Approval boundary

This approval does **not** authorize:

- production deployment;
- class or monster scalar changes;
- shop / EXP / P×P numerical changes;
- an exact Lv26 activation Stage;
- a final player-visible EXP scale;
- full T1 Stage1-50 exact recipe freeze.

## 7. Next bounded package

The next contiguous exact-authoring gap is Stage34-36:

```text
left exact anchor  = Stage33
missing gap        = Stage34, Stage35, Stage36
right exact anchor = Stage37
future contiguous window after adoption = Stage15-37
```

Next package:

```text
T1_E1_STAGE34_36_CONTIGUOUS_GAP_PREFLIGHT
```

Stage34-36 exact content is not approved or materialized by this document.
