# Timing Defense — T1 Contiguous Stage15-33 D1 Dynamic Admission and Closure V0.1

Date: 2026-10-26 KST  
Status: **D1 TECHNICAL WORK CLOSED / PASS_WITH_WATCHES / STAGE32 USER ADOPTION STILL OPEN**

## 0. Authority and scope

```text
live remote > canonical documents > exact evidence > handoff > copied SHA/chat/memory
```

This work closes technical validation for the single missing Stage32 between already-approved exact Stage31 and Stage33 authorities. It does not adopt Stage32, change production gameplay, change class/monster scalars, freeze EXP/P×P/shop values, select an exact Lv26 unlock Stage, or freeze the full T1 Stage1-50 recipe.

## 1. D1 exact candidate

Candidate:
`data/t1_contiguous_32_d1_candidate_v0_1.yaml`

Candidate SHA256:
`91909c0b9be28003a8fdcbafd3ad65b325ed9b2247524e810f950bd3541d45d8`

Stage32 signature:

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

Composition = RUNNER ×5 + GRUNT ×4.  
Pattern = three readable 3-unit CD04 bursts.  
Purpose = preserve `Stage31 durable -> Stage32 tempo -> Stage33 density` rotation.

## 2. Static admission

Workflow:
- run `40331569664`
- exact HEAD `20f5a4cc16c920bdfe86b1a0a3110284ff7c4ef4`
- artifact `12653329249`
- artifact ZIP SHA256 `2107ce835dcba4ae1e7cc06bd8baf08f3ab2b907dcdd0db0ea9df9e133700290`

Result:

```text
PASS
errors = []
warnings = []
referenceIntegrity = PASS
authorityPreserved = true
contiguous15to33 = true
rotation31to33Preserved = true
```

Exact materialized Stage15-33 SHA256:
`47f02889b659dcad7988645fcc6e11381de38607657bd7751d7387856dba5466`

Static pressure shape:

```text
Stage31 authored 8 / max4s 8
Stage32 authored 9 / max4s 6 / max6s 9
Stage33 authored 12 / max4s 8
```

Therefore Stage32 raises tempo/count from Stage31 without taking over Stage33's FLOOD-density role.

## 3. Dynamic admission requirement

Dynamic admission was required because Stage32 is the first point of the existing Lv26 Stage32-36 calibration-candidate reach band and persistent run state continues into exact Stage33.

The run executes real Stage15->33 continuity rather than fabricating skipped-stage carry state.

Variants:

```text
Lv16 before Stage18 vs Stage21
× Lv21 before Stage25 vs Stage28
× Lv26 active before Stage32 vs inactive through Stage33
```

Five classes × five seeds (`101,211,307,409,503`) × eight variants = 200 cases.

Lv26 comparison is diagnostic only. It does not select an exact Lv26 unlock Stage or EXP threshold.

## 4. Superseded runner-only failure

Initial dynamic invocation:
- run `40331982731`
- exact HEAD `d7af502296d680b23caea54cc370042315d83596`
- artifact `12654974006`
- artifact ZIP SHA256 `cc6e472af3737e0e40ba7286d97a8551f002535a8995663d5e240ffc11d43403`

The simulation executed, then result assembly failed on two Python metadata literals written as `false` instead of `False`.

```text
NameError: name 'false' is not defined
```

This is classified as **SUPERSEDED_RUNNER_METADATA_DEFECT_ONLY**. Candidate recipe, materialized input, runtime semantics, and balance evidence were not changed. Only those two runner tokens were corrected.

## 5. Accepted dynamic evidence

Accepted rerun:
- run `40332410094`
- exact HEAD `b34bb2432797dc0d6ae5e8135072b19dd3ebaa85`
- artifact `12653794932`
- artifact ZIP SHA256 `bfb0333d7773fee53a03f67025d8a295fee3b332f7a0ded9b6f251853b1aba52`
- post-fix runner SHA256 `1a6a15ae228a3d7c674678479a0049979e40f59f025b09221abceda8b2938a87`
- static-result SHA256 `279d7cced8339cbf3eda401b7e6afdd0b6af029e1b76f6ce05e7f9a1aa77fd0c`
- dynamic-result SHA256 `550271fe67fc46f67a5671276bbec8ebe6e98adbd51a3a3b5ce7f723ed2bb688`
- materialized Stage15-33 SHA256 `47f02889b659dcad7988645fcc6e11381de38607657bd7751d7387856dba5466`

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

Completion:

```text
200 / 200 cases completed through Stage33
3800 Stage rows
terminal failure rows = 0
```

## 6. Stage31-33 behavior

All-case means:

```text
Stage31 actions 7.700 / settle 7.3963s / peakActive 4.510 / wallDamage 0
Stage32 actions 8.305 / settle 8.1189s / peakActive 4.230 / wallDamage 0
Stage33 actions 9.010 / settle 8.9018s / peakActive 6.205 / wallDamage 0
```

Interpretation:

```text
Stage31 -> Stage32 tempo demand increase = SUPPORTED
Stage32 remains below Stage33 density identity = SUPPORTED
Stage32 -> Stage33 density escalation = SUPPORTED
Stage31-33 objective safety in bounded sample = SUPPORTED
```

Stage32 peakActive is intentionally not the local maximum; its identity is burst/scatter tempo. Stage33 has the clear peak-active density step.

## 7. Class and Lv26 sensitivity

Stage32 class means all have zero wall damage. Selected readings:

```text
Rogue Stage32: actions 7.10 / settle 6.9530s / peak 3.40
Tank  Stage32: actions 9.45 / settle 9.2950s / peak 4.40
```

No Stage31-33 case in any class produced wall damage.

Paired Lv26 edge comparison (`Lv26@32 - inactive through Stage33`):

```text
Stage32 mean wall-damage delta = 0.0
Stage32 mean actions delta = -0.21
Stage32 mean settle delta = -0.2260s

Stage33 mean wall-damage delta = 0.0
Stage33 mean actions delta = -0.46
Stage33 mean settle delta = -0.4046s
```

There is no evidence here for an exact Lv26 activation Stage. The existing Stage32-36 calibration-candidate reach band remains unchanged.

## 8. Watch decision

No new watch is created.

Reason:
- no terminal failures;
- no Stage31-33 wall damage;
- no continuity/replay/settlement defect;
- no new class-specific objective-pressure failure mode.

Retain existing watches, including `TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH`.

## 9. Technical closure and user gate

D1 technical result:

```text
PASS_WITH_WATCHES
```

Stage32 remains a validated candidate, not canonical authoring authority, until explicit user approval.

Current product-authority question:

```text
ADOPT STAGE32 EXACT SPAWN CANDIDATE
AS CANONICAL T1 AUTHORING BASELINE WITH WATCHES?
```

Evidence recommendation:
`ADOPT_STAGE32_AS_CANONICAL_T1_AUTHORING_BASELINE_WITH_WATCHES`

Until approval:
- canonical contiguous exact window remains Stage15-31;
- Stage15-33 is an established exact materialized evidence window only;
- Stage32 candidateAdopted remains false.
