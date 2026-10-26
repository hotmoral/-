# Timing Defense — T1 Contiguous Stage15-38 E1 Dynamic Admission and Closure V0.1

Date: 2026-10-26 KST  
Status: **E1 TECHNICAL WORK CLOSED / PASS_WITH_WATCHES / STAGE34-36 USER ADOPTION STILL OPEN**

## 0. Authority and scope

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

This work closes technical validation for the Stage34-36 contiguous gap between already-approved exact Stage33 and Stage37-38 Wave A authorities. It does not adopt Stage34-36, change production gameplay, change class/monster scalars, freeze EXP/P×P/shop values, select an exact Lv26 unlock Stage, or freeze the full T1 Stage1-50 recipe.

## 1. E1 v0.1 candidate and why it was superseded

Initial candidate:
`data/t1_contiguous_34_36_e1_candidate_v0_1.yaml`

Static run `40335430803` passed and materialized Stage15-37 exactly. Persistent dynamic run `40335839268` also completed technically:

```text
300/300 completed through Stage37
6900 Stage rows
terminal failures = 0
continuity/replay/settlement = PASS
Stage34-37 wall damage = 0
```

However the Stage35 product intent was not supported:

```text
Stage34 mean actions 8.19 / settle 7.9009s / peakActive 3.653333
Stage35 mean actions 9.56 / settle 9.477033s / peakActive 3.076667
```

Although Stage35 had lower peak active, it required more actions and more settle time than Stage34. Therefore the intended `lower-complexity recovery` was not readable enough. v0.1 is superseded as a **VALID TECHNICAL CANDIDATE WITH PRODUCT-INTENT MISMATCH**, not as a runtime failure.

Only Stage35 exact spawns were revised. Stage34 and Stage36 were preserved semantically exactly.

## 2. E1 v0.2 exact candidate

Plan:
`data/t1_contiguous_34_36_e1_authoring_plan_v0_2.yaml`

Candidate:
`data/t1_contiguous_34_36_e1_candidate_v0_2.yaml`

Candidate SHA256:
`da4624a55c327fa68f71bd92b6626fee5e30fd5ddd2d6369403dd6d8b6715550`

### Stage34 — reorder/control

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

Composition = BRUTE x2 + RUNNER x4 + GRUNT x2.

### Stage35 — revised recovery

```text
E01 / F04 / CD05 / C1 / BASELINE
GRUNT 0ms    y=0.28
GRUNT 800ms  y=0.70
GRUNT 2400ms y=0.40
GRUNT 3200ms y=0.66
```

Composition = GRUNT x4. This is the only exact-spawn revision from E1 v0.1.

### Stage36 — focused heavy-line attribution

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

Composition = BRUTE x3 + GRUNT x4.

## 3. Stage38 continuation correction

Wave A approval doc180 already makes Stage37 and Stage38 canonical exact authorities. Therefore successful adoption of Stage34-36 would close the contiguous exact-authoring window through **Stage38**, not merely Stage37.

The v0.2 materialization and dynamic admission therefore use real Stage15->38 continuity.

## 4. E1 v0.2 static admission

Workflow:
- run `40336925232`
- exact HEAD `06e4c1e44a890a8ef389c80c9123988e88cdb5e2`
- artifact `12657965202`
- artifact ZIP SHA256 `3d29d886fb4677285fa855174189dded130b1c6f8cefe41bff8045ec4f9aadc6`

Result:

```text
PASS
errors = []
warnings = []
referenceIntegrity = PASS
authorityPreserved = true
contiguous15to38 = true
stage35RevisionOnly = true
```

Exact materialized Stage15-38 SHA256:
`58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d`

Static result SHA256:
`f2be496b6b87c48d108584711205d70c3a332547932852dad1c3f600d3f02f94`

Static pressure shape:

```text
Stage33 authored 12 / max4s 8
Stage34 authored 8  / max4s 6
Stage35 authored 4  / max4s 4
Stage36 authored 7  / max4s 6
Stage37 authored 8  / max4s 8
Stage38 authored 8  / max4s 7
```

## 5. Superseded v0.2 first dynamic invocation

Initial v0.2 dynamic run `40336925635` stopped before simulation because the runner contained a stale precomputed materialized SHA constant.

Observed materialized SHA:
`58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d`

Stale runner constant:
`d7dd0c8b5f3593cb0d3cdc6d580c40872dd56ff7c09bd91496f7dcd93bb96d1e`

This is classified as **SUPERSEDED_RUNNER_FIDELITY_CONSTANT_DEFECT_ONLY**. No candidate, plan, static validator, runtime semantics, or balance parameter changed. Only the expected identity constant was corrected.

## 6. Accepted persistent Stage15-38 dynamic admission

Accepted rerun:
- run `40337357872`
- exact HEAD `a66d961285ec40e43c080a1e87e08ce433d4fa38`
- artifact `12658500115`
- artifact ZIP SHA256 `6f2c82bda9120d7b7006f90d9c9149758b6b2022a1fe07e54fedfc72797fc638`
- post-fix runner SHA256 `e28a2fc306c8fe26d3c11d58c868f70f243b3b2aab23d7c21e92ff99d8511428`
- dynamic-result SHA256 `55c95753b669bb861c30d266b8565415a41b17f03d6e081663cbfebaac894bc5`
- materialized Stage15-38 SHA256 `58dbc3109c1b919fed9de48118a88063595b8ef616632ee3c2aa8595ec70925d`

Variants:

```text
Lv16 before Stage18 vs Stage21
x Lv21 before Stage25 vs Stage28
x Lv26 before Stage32 vs Stage34 vs Stage36
x 5 classes
x 5 seeds (101,211,307,409,503)
= 300 cases
```

Admission:

```text
status = PASS_DYNAMIC_DIAGNOSTIC_ONLY
exactMaterializedIdentity = true
persistentStateContinuity = true
deterministicReplay = true
settlementAndCarryInvariants = true
allCasesCompletedThrough38 = true
stage35RecoveryIntentSupported = true
fidelityErrors = []
continuityErrors = []
replayErrors = []
invariantErrors = []
pass = true
```

Completion:

```text
300/300 completed through Stage38
7200 Stage rows
terminal failure rows = 0
```

## 7. Stage33-38 behavior

All-case means:

```text
Stage33 actions 9.086667 / settle 8.969233s / peakActive 6.240000 / wallDamage 0
Stage34 actions 8.190000 / settle 7.900900s / peakActive 3.653333 / wallDamage 0
Stage35 actions 6.210000 / settle 5.799267s / peakActive 2.516667 / wallDamage 0
Stage36 actions 9.743333 / settle 9.781167s / peakActive 4.330000 / wallDamage 0
Stage37 actions 7.283333 / settle 6.915167s / peakActive 5.586667 / wallDamage 0
Stage38 actions 8.196667 / settle 8.046233s / peakActive 4.800000 / wallDamage 0
```

Interpretation:

```text
Stage33 density -> Stage34 reorder = SUPPORTED
Stage34 -> Stage35 readable recovery = SUPPORTED
Stage35 -> Stage36 focused durable re-acceleration = SUPPORTED
Stage36 -> Stage37 split-tempo handoff = SUPPORTED
Stage37 -> Stage38 durable bridge carry-in = SUPPORTED
Stage34-38 objective safety in bounded sample = SUPPORTED
```

Stage35 recovery is also class-robust: Archer, Knight, Mage, Rogue, and Tank all show lower Stage35 mean actions and settle time than Stage34.

## 8. Lv26 interpretation

Lv26 positions Stage32 / Stage34 / Stage36 were diagnostic sensitivity probes only. They do not choose an exact Lv26 unlock Stage or EXP threshold. Existing authority remains:

```text
Lv26 = Stage32-36 calibration-candidate reach band
```

## 9. Watch decision

No new watch is created.

Reason:
- no terminal failures;
- no Stage34-38 wall damage;
- no continuity/replay/settlement defect;
- Stage35 recovery intent now supported;
- no new class-specific objective-pressure failure mode.

All existing watches remain in force.

## 10. Technical closure and user gate

E1 technical result:

```text
PASS_WITH_WATCHES
```

Stage34-36 remain validated candidates, not canonical authoring authority, until explicit user approval.

Current product-authority question:

```text
ADOPT STAGE34-36 E1 V0.2 EXACT SPAWN CANDIDATE
AS CANONICAL T1 AUTHORING BASELINE WITH WATCHES?
```

Evidence recommendation:
`ADOPT_STAGE34_36_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES`

Until approval:
- canonical contiguous exact window remains Stage15-33;
- Stage15-38 is established exact materialized evidence only;
- Stage34-36 candidateAdopted remains false;
- no further authoring package should start.
