# Timing Defense — T1 Stage26-28 Exact-Spawn Authoring Baseline User Approved V0.1

Date: 2026-10-26 KST  
Status: **USER APPROVED / CANONICAL T1 AUTHORING BASELINE WITH WATCHES / NO PRODUCTION OR NUMERICAL FREEZE**

## 0. Decision

The user explicitly approved the C1 Stage26-28 exact-spawn candidate after static and persistent dynamic admission closed PASS_WITH_WATCHES.

Approved decision:

```text
ADOPT_STAGE26_28_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES
```

This closes:

```text
T1_C1_STAGE26_28_AUTHORING_ADOPTION_DECISION_GATE
```

Authority remains:

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

## 1. Exact candidate identity

Candidate:
`data/t1_contiguous_26_28_c1_candidate_v0_1.yaml`

Candidate SHA256:
`63e40e635b47c54876778a1c64809e961b3929062e3279ea4a805fdf9d8760e4`

Materialized Stage15-31 SHA256:
`284426b71fe03e9838ae141d90422d3d0dec55ad55c71466a4a28bc1fc91297c`

Technical closure:
`183_T1_CONTIGUOUS_15_31_C1_DYNAMIC_ADMISSION_AND_CLOSURE_V0_1.md`

## 2. Canonical exact Stage26-28 authoring

### Stage26

```text
E03 / F01 / CD02 / C1 / BULWARK
BRUTE  0ms    y=0.46
GRUNT  800ms  y=0.44
GRUNT  1600ms y=0.48
BRUTE  2400ms y=0.45
GRUNT  3200ms y=0.47
```

### Stage27

```text
E02 / F04 / CD03 / C1 / RUSH
RUNNER 0ms    y=0.28
GRUNT  250ms  y=0.70
RUNNER 500ms  y=0.40
GRUNT  2000ms y=0.66
RUNNER 2250ms y=0.32
GRUNT  3750ms y=0.74
RUNNER 4000ms y=0.44
```

### Stage28

```text
E01 / F03 / CD03 / C1 / BASELINE + FLOOD
GRUNT 0ms    y=0.43
GRUNT 250ms  y=0.46
GRUNT 500ms  y=0.49
GRUNT 2000ms y=0.44
GRUNT 2250ms y=0.47
GRUNT 2500ms y=0.45
```

Exact spawn count, timestamp, monster type and Y placement above are now canonical T1 authoring authority WITH WATCHES.

## 3. Retained evidence

Static admission:

```text
run 40324812125
artifact 12651020986
exact HEAD 1acff948c6b8ff67f0cdaa1dd4c0e080e47c0346
status PASS
referenceIntegrity PASS
authorityPreserved true
contiguous15to31 true
```

Dynamic admission:

```text
run 40325507618
artifact 12651550217
exact HEAD 80a4b42134100693fe161e02ef4e0c3828974ead
100/100 completed through Stage31
1700 Stage rows
terminal failures 0
persistent continuity PASS
deterministic replay PASS
settlement/carry invariants PASS
```

Behavioral interpretation retained:

```text
Stage26 re-acceleration = SUPPORTED
Stage27 tempo focus = SUPPORTED WITH bounded Tank objective contact
Stage28 decompression = SUPPORTED
Stage29 C2 synthesis step-up = SUPPORTED
```

No new watch is created. The bounded Tank Stage27 contact remains covered by `TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`.

## 4. Canonical consequence

The canonical contiguous exact-authoring window is now:

```text
Stage15-31
```

Previously canonical Stage15-25 remains unchanged; Stage26-28 are appended between the already-approved Stage25 and Stage29-31 authorities.

## 5. Approval boundary

This approval does **not** authorize:

- production deployment;
- class or monster scalar changes;
- shop / EXP / P×P numerical changes;
- an exact Lv21 activation Stage;
- a final player-visible EXP scale;
- full T1 Stage1-50 exact recipe freeze.

Lv21 remains only a Stage25-28 calibration-candidate reach band.

## 6. Next bounded package

The next smallest contiguous exact-authoring gap is Stage32:

```text
left exact anchor  = Stage31
right exact anchor = Stage33
missing gap        = Stage32 only
future contiguous window after adoption = Stage15-33
```

Next package:

```text
T1_D1_STAGE32_SINGLE_GAP_AUTHORING_PREFLIGHT
```

Stage32 exact content is **not** approved or materialized by this document.
