# Timing Defense — T1 Stage34-36 Exact-Spawn Authoring Baseline User Approved V0.1

Date: 2026-10-26 KST  
Status: **USER APPROVED / CANONICAL T1 AUTHORING BASELINE WITH WATCHES / NO PRODUCTION OR NUMERICAL FREEZE**

## 0. Decision

The user explicitly approved the final E1 v0.2 Stage34-36 exact-spawn candidate after static and persistent Stage15->38 dynamic admission closed `PASS_WITH_WATCHES`.

Approved decision:

```text
ADOPT_STAGE34_36_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES
```

This closes:

```text
T1_E1_STAGE34_36_AUTHORING_ADOPTION_DECISION_GATE
```

Authority remains:

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

## 1. Exact candidate identity

Plan:
`data/t1_contiguous_34_36_e1_authoring_plan_v0_2.yaml`

Candidate:
`data/t1_contiguous_34_36_e1_candidate_v0_2.yaml`

Candidate SHA256:
`da4624a55c327fa68f71bd92b6626fee5e30fd5ddd2d6369403dd6d8b6715550`

Materialized Stage15-38 SHA256:
`58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d`

Technical closure:
`187_T1_CONTIGUOUS_15_38_E1_DYNAMIC_ADMISSION_AND_CLOSURE_V0_1.md`

## 2. Canonical exact Stage34-36 authoring

### Stage34 — target reorder / control

```text
E03+E02 / F02 / CD05 / C2 / BULWARK
BRUTE  0ms    y=0.46
RUNNER 550ms  y=0.42
GRUNT  1100ms y=0.49
RUNNER 1650ms y=0.44
BRUTE  3300ms y=0.46
RUNNER 3850ms y=0.50
GRUNT  4400ms y=0.43
RUNNER 4950ms y=0.48
```

### Stage35 — lower-complexity recovery

```text
E01 / F04 / CD05 / C1 / BASELINE
GRUNT 0ms    y=0.28
GRUNT 800ms  y=0.70
GRUNT 2400ms y=0.40
GRUNT 3200ms y=0.66
```

### Stage36 — focused durable attribution

```text
E03 / F01 / CD03 / C1 / BULWARK
BRUTE 0ms    y=0.46
GRUNT 250ms  y=0.44
GRUNT 500ms  y=0.48
BRUTE 2800ms y=0.46
GRUNT 3050ms y=0.45
GRUNT 3300ms y=0.47
BRUTE 6000ms y=0.46
```

Exact counts, timestamps, monster types and Y placements above are now canonical T1 authoring authority WITH WATCHES.

## 3. Retained evidence

Static admission:

```text
run 40336925232
artifact 12657965202
exact HEAD 06e4c1e44a890a8ef389c80c9123988e88cdb5e2
artifact ZIP SHA256 3d29d886fb4677285fa855174189dded130b1c6f8cefe41bff8045ec4f9aadc6
status PASS
reference integrity PASS
authority preserved true
contiguous Stage15-38 true
```

Accepted persistent dynamic admission:

```text
run 40337357872
artifact 12658500115
exact HEAD a66d961285ec40e43c080a1e87e08ce433d4fa38
artifact ZIP SHA256 6f2c82bda9120d7b7006f90d9c9149758b6b2022a1fe07e54fedfc72797fc638
300/300 completed through Stage38
7200 Stage rows
terminal failures 0
Stage34-38 wall damage 0
persistent continuity PASS
deterministic replay PASS
settlement/carry invariants PASS
Stage35 recovery intent SUPPORTED
```

Behavioral means retained:

```text
S33 actions 9.0867 / settle 8.9692s / peak 6.2400
S34 actions 8.1900 / settle 7.9009s / peak 3.6533
S35 actions 6.2100 / settle 5.7993s / peak 2.5167
S36 actions 9.7433 / settle 9.7812s / peak 4.3300
S37 actions 7.2833 / settle 6.9152s / peak 5.5867
S38 actions 8.1967 / settle 8.0462s / peak 4.8000
```

No new watch is created.

## 4. Superseded evidence

E1 v0.1 remains historical evidence only. It passed runtime invariants, but Stage35 did not behave as the intended recovery because actions and settle time exceeded Stage34. Only Stage35 exact spawns were revised in v0.2; Stage34 and Stage36 were preserved.

The first v0.2 dynamic run `40336925635` is also superseded because its runner contained only a stale expected materialized-SHA constant. It has no candidate/runtime authority.

## 5. Canonical consequence

The canonical contiguous exact-authoring window is now:

```text
Stage15-38
```

Stage37 and Stage38 were already user-approved Wave A exact authorities, so adoption of Stage34-36 closes the entire gap through Stage38.

## 6. Progression boundary

Lv26 remains only:

```text
Stage32-36 calibration-candidate reach band
```

Diagnostic Lv26 positions at Stage32/34/36 do not select an exact activation Stage or EXP threshold.

## 7. Approval boundary

This approval does **not** authorize:

- production deployment;
- class or monster scalar changes;
- shop / EXP / P×P numerical changes;
- an exact Lv26 activation Stage;
- a final player-visible EXP scale;
- full T1 Stage1-50 exact recipe freeze.

## 8. Next bounded package

Stage39 and Stage40 already exist as exact candidates in the representative transition-slice source. Therefore the next step is evidence recovery and promotion preflight, not reauthoring.

```text
canonical left anchor = Stage38
existing exact candidates = Stage39, Stage40
candidate source = data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml
future contiguous window if later adopted = Stage15-40
```

Next package:

```text
T1_F1_STAGE39_40_EXISTING_EXACT_PROMOTION_PREFLIGHT
```

No Stage39/40 adoption is made by this document.
