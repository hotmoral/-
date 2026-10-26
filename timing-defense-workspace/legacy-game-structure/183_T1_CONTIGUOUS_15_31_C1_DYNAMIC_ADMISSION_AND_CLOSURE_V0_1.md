# Timing Defense — T1 Contiguous Stage15-31 C1 Dynamic Admission and Closure V0.1

Date: 2026-10-26 KST  
Status: **C1 TECHNICAL WORK CLOSED / PASS_WITH_WATCHES / STAGE26-28 USER ADOPTION STILL OPEN**

## 0. Authority boundary

This document closes the bounded C1 technical evidence package for Stage26-28. It does **not** adopt the Stage26-28 exact authoring candidate.

Authority order remains:

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

Closed B1, Wave A, and Stage49-50 evidence remain unchanged. Stage15-25 was executed here only as the unchanged persistent prefix required to reach the changed Stage26-31 tail with real carried state; this is not a reopening of B1.

No production gameplay change, class/monster scalar change, shop/EXP/P×P change, exact Lv21 unlock freeze, or full T1 Stage1-50 exact recipe freeze is authorized.

---

## 1. C1 exact candidate

Candidate:
`data/t1_contiguous_26_28_c1_candidate_v0_1.yaml`

Candidate SHA256:
`63e40e635b47c54876778a1c64809e961b3929062e3279ea4a805fdf9d8760e4`

Bounded authoring plan SHA256:
`3ed5001b7755a5b0f9805d67a40abf78e7309845473253b01142a0fa20370a18`

### Stage26 — durable focus

```text
E03 / F01 / CD02 / C1 / BULWARK
BRUTE  0ms    y=0.46
GRUNT  800ms  y=0.44
GRUNT  1600ms y=0.48
BRUTE  2400ms y=0.45
GRUNT  3200ms y=0.47
authored = 5
```

### Stage27 — tempo scatter

```text
E02 / F04 / CD03 / C1 / RUSH
RUNNER 0ms    y=0.28
GRUNT  250ms  y=0.70
RUNNER 500ms  y=0.40
GRUNT  2000ms y=0.66
RUNNER 2250ms y=0.32
GRUNT  3750ms y=0.74
RUNNER 4000ms y=0.44
authored = 7
```

### Stage28 — density recall / Lv21 settle

```text
E01 / F03 / CD03 / C1 / BASELINE + FLOOD
GRUNT 0ms    y=0.43
GRUNT 250ms  y=0.46
GRUNT 500ms  y=0.49
GRUNT 2000ms y=0.44
GRUNT 2250ms y=0.47
GRUNT 2500ms y=0.45
authored = 6
```

Adjacent approved anchor counts remain:

```text
Stage25 = 4 / C0 relief buffer
Stage26 = 5 / C1 durable
Stage27 = 7 / C1 tempo
Stage28 = 6 / C1 density recall
Stage29 = 9 / C2 split-axis synthesis
```

Stage29 remains a clear complexity/pressure step-up.

---

## 2. Reference-integrity correction

The initial C1 plan referenced a nonexistent static-audit filename. The reference was corrected before candidate materialization:

```text
wrong: ../162_T1_STAGE1_50_SIGNATURE_SKELETON_STATIC_AUDIT_V0_1.md
live:  ../162_T1_STAGE_SIGNATURE_STATIC_CONSISTENCY_AUDIT_V0_1.md
```

No recipe/scalar was changed to obtain this correction.

---

## 3. Static admission

Workflow:
`Timing Defense T1 Contiguous 26-28 C1 Static Preflight`

```text
run       40324812125
artifact  12651020986
exact HEAD 1acff948c6b8ff67f0cdaa1dd4c0e080e47c0346
artifact ZIP SHA256
e28b8bc65560907a953fb5f6cfbcf4d93266e3795cab4f866ee1d2761fec6335

candidate SHA256
63e40e635b47c54876778a1c64809e961b3929062e3279ea4a805fdf9d8760e4

materialized Stage15-31 SHA256
284426b71fe03e9838ae141d90422d3d0dec55ad55c71466a4a28bc1fc91297c

result.json SHA256
0c237f9d7843f32aa9a08ad28ff430be12d794cb0aff2bb91cf4dae206c69393
```

Result:

```text
status = PASS
errors = []
warnings = []
referenceIntegrity = PASS
authorityPreserved = true
contiguous15to31 = true
```

C1 static density:

```text
S26 authored 5 / max4s 5
S27 authored 7 / max4s 6
S28 authored 6 / max4s 6
S29 authored 9 / max4s 6
```

The normal authored-4s guard (`<=8`) is preserved.

---

## 4. Why dynamic admission was required

Static PASS alone cannot establish the main C1 claim because:

1. C1 extends a persistent lifecycle from Stage15 through Stage31.
2. Stage26-28 cover the tail of the still-unfrozen Lv21 Stage25-28 calibration-candidate reach band.
3. Base HP deficit, combo, charge, judgment RNG and combat-proc RNG are persistent across settled Stage boundaries.
4. A Stage15-31 continuity claim cannot be made by fabricating skipped-Stage state.

Therefore Stage15-25 was reused unchanged as a required prefix and Stage26-31 was evaluated in the same persistent run.

---

## 5. Dynamic admission design

Workflow:
`Timing Defense T1 Contiguous 15-31 C1 Dynamic Admission V0.1`

Exact dynamic source:

```text
HEAD 80a4b42134100693fe161e02ef4e0c3828974ead
runner SHA256
b633a29644b9ff3bca956140302cf99da1ce74ec2c175c11dad76fe566c1e8c9
materialized Stage15-31 SHA256
284426b71fe03e9838ae141d90422d3d0dec55ad55c71466a4a28bc1fc91297c
```

Sensitivity variants:

```text
Lv16 before Stage18 × Lv21 before Stage25
Lv16 before Stage18 × Lv21 before Stage28
Lv16 before Stage21 × Lv21 before Stage25
Lv16 before Stage21 × Lv21 before Stage28
```

Classes:

```text
Knight / Rogue / Tank / Archer / Mage
```

Seeds:

```text
101 / 211 / 307 / 409 / 503
```

Total:

```text
4 variants × 5 classes × 5 seeds = 100 persistent cases
```

These are reach-band edge sensitivity states only. They do not freeze EXP thresholds or exact unlock Stages.

---

## 6. Dynamic result

```text
run       40325507618
artifact  12651550217
exact HEAD 80a4b42134100693fe161e02ef4e0c3828974ead
artifact ZIP SHA256
ccb3a07f326ce57d3b9dd3056773e89cb5fc0fc790f6b542d62d3c1f15945b24

dynamic-result.json SHA256
11e183e23039eecc0ca1c3b2452f6f822e31f15b246db3b20c2cedd55e9a1dbc
```

Admission:

```text
status = PASS_DYNAMIC_DIAGNOSTIC_ONLY
exactMaterializedIdentity = true
persistentStateContinuity = true
deterministicReplay = true
settlementAndCarryInvariants = true
fidelityErrors = []
continuityErrors = []
replayErrors = []
invariantErrors = []
pass = true
```

Coverage:

```text
cases = 100
completedThrough31 = 100
Stage rows = 1700
terminal failure rows = 0
```

---

## 7. C1 behavioral interpretation

All-case means:

| Stage | Mean actions | Mean settled time | Mean peak active | Mean wall damage |
|---|---:|---:|---:|---:|
| 25 | 7.06 | 7.1277s | 1.68 | 0.00 |
| 26 | 7.75 | 7.3919s | 3.67 | 0.00 |
| 27 | 7.93 | 7.6269s | 3.38 | 1.08 |
| 28 | 5.24 | 4.6966s | 3.77 | 0.00 |
| 29 | 11.73 | 11.7463s | 5.24 | 0.00 |
| 30 | 7.93 | 7.6640s | 4.24 | 0.00 |
| 31 | 7.70 | 7.3963s | 4.51 | 0.00 |

Interpretation:

```text
Stage25 -> 26 = readable re-acceleration, no objective damage
Stage27 = tempo focus, bounded objective contact only
Stage28 = clear decompression/settle point
Stage28 -> 29 = strong, consistent C2 synthesis step-up
Stage29-31 = no terminal or wall-damage failure in bounded sample
```

Stage28 therefore does not erase Stage29's synthesis identity.

### Tank-specific Stage27 observation

Across the 20 Tank cases:

```text
Stage27 mean wall damage = 5.4
nonzero cases = 2 / 20
both nonzero rows = seed503 + Lv21-before-25
damage per nonzero row = 54
```

The corresponding late-Lv21(Stage28) paired cases had zero Stage27 wall damage.

This is materially below the already-retained Stage21-24 Tank objective-pressure skew and does not justify a new watch or scalar change. It remains covered by:

`TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`

No other class had Stage25-31 wall damage.

### Lv21 reach-band sensitivity

Early Lv21(Stage25) generally reduces action/settle demand through Stage26-28 for several classes. The only adverse objective delta in the paired edge comparison is the bounded Tank seed503 Stage27 row described above.

This is sensitivity evidence, **not** authority to choose Stage25 or Stage28 as the exact Lv21 unlock Stage.

---

## 8. Closure classification

C1 technical evidence is classified:

```text
STATIC = PASS
DYNAMIC = PASS_WITH_WATCHES
PERSISTENT Stage15-31 EXECUTION = ESTABLISHED
Stage26-28 candidate adoption = NOT YET
```

No new watch is added.

Retain all existing watches, especially:

```text
T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH
T1_RUNNER_HIGH_PRESSURE_LV16_TAIL_WATCH
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
```

---

## 9. Exact decision gate

The remaining product-authority question is:

```text
ADOPT STAGE26 + STAGE27 + STAGE28 EXACT SPAWN CANDIDATE
AS CANONICAL T1 AUTHORING BASELINE WITH WATCHES?
```

Recommended disposition from the current evidence:

```text
ADOPT_STAGE26_28_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES
```

If explicitly approved:

- exact count/timestamp/type/Y for Stage26-28 become canonical authoring authority;
- the canonical contiguous exact authoring window extends from Stage15-25 to Stage15-31;
- existing watches remain;
- active plan advances immutably;
- PROJECT_STATUS / NEXT_WORK / SESSION_HANDOFF are synchronized to the next bounded package.

Approval does **not** authorize production deployment, scalar changes, final EXP/P×P/shop values, exact Lv21 unlock Stage, or full T1 Stage1-50 exact freeze.

If rejected, retain all C1 evidence and revise only the specifically rejected authoring property.
