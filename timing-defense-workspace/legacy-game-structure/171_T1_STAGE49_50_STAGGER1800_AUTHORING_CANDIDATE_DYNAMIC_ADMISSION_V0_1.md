# T1 Stage49-50 STAGGER1800 Authoring Candidate Dynamic Admission v0.1

Date: 2026-10-25 KST

Status:
**DYNAMIC ADMISSION PASS_WITH_WATCH / MATERIALIZATION REPRODUCED / NO AUTHORING ADOPTION / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

## 1. Purpose

Verify that the explicit Stage49-50 authoring candidate from doc170 reproduces the already-established doc169 diagnostic behavior under the exact lifecycle-faithful runner.

This is an admission/reproduction step, not a new search.

## 2. Exact source

Candidate:
`data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml`

Candidate SHA256:
`c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3`

Base v0.2 SHA256:
`3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf`

Workflow:
`.github/workflows/timing-defense-t1-stage49-50-authoring-dynamic-admission.yml`

Exact run:
```text
run      40156895093
artifact 12585270921
head     cd5d28ac6748a65b8e46c8c664954223a8cf5ef3
artifact digest sha256 9f1ca98b624c31ffce1beefc5ca8dc17cbcdd2309d2db8abec7eb92cb66ebe8c
seeds    101,211,307,409,503
```

## 3. Exact reproduction gates

```text
status = PASS
errors = []
fidelityErrors = []
Stage49 spawnEquivalentToDiagnosticGenerator = true
Stage50 spawnEquivalentToDiagnosticGenerator = true
```

Stage46-48 remained exact v0.2 lead-in, preserving the same persistent combo/charge/RNG entry path.

Paired OFF/ON lifecycle and deterministic replay passed for every class/seed.

Archer width bridge remained:
```text
yTolerance = 0.20
DIAGNOSTIC_ONLY_NOT_FROZEN
```

Mage Lv31 bridge remained semantic fidelity only; no numerical coefficient was changed.

## 4. Role-facing reproduction

Lv31 OFF -> ON target-grammar clear-latency result exactly reproduced doc169:

```text
Knight: +3408.0 ms / +43.0303%
Rogue : +1635.9 ms / +30.0662%
Tank  : +3813.333 ms / +27.3684% plus 3 unresolved reduced
Archer: +73.333 ms / +1.7241%
Mage  : +404.0 ms / +9.4216%
```

All five role directions remained positive.

## 5. Objective-protection reproduction

```text
Lv31 OFF total wall damage = 1358
Lv31 ON  total wall damage = 164
reduction                  = 1194
OFF mean final Base HP     = 1945.68
ON  mean final Base HP     = 1993.44
OFF wall-pressure classes = 1
ON  wall-pressure classes = 1
fail/incomplete            = 0 / 0
```

Therefore authoring materialization did not worsen the already-known objective-pressure skew. It reproduced it exactly.

## 6. Whole-window consequence review

The exact reproduction exposes a second-order issue that target-grammar role metrics alone do not capture.

Mean Stage49-50 late settle / backline exposure:

```text
Knight OFF 51.480s / 20.178s -> ON 47.992s / 13.138s
Rogue  OFF 53.272s / 18.260s -> ON 48.756s / 13.408s
Tank   OFF 71.720s / 42.617s -> ON 60.808s / 34.065s
Archer OFF 46.640s / 16.787s -> ON 46.420s / 17.203s
Mage   OFF 48.320s / 15.880s -> ON 48.792s / 13.811s
```

Interpretation:
- Knight/Rogue: role benefit translates strongly into whole-window pressure reduction.
- Tank: role benefit translates strongly into whole-window pressure and objective protection.
- Archer: target-line benefit exists but whole-window settle changes only 0.22s and backline exposure slightly worsens.
- Mage: target CLUSTER benefit is +9.42% and backline exposure improves, but whole-window settle is 0.472s slower.

Per-stage settle mean OFF->ON:

```text
Archer Stage49: +0.220s faster
Archer Stage50: 0.000s
Mage   Stage49: 0.364s slower
Mage   Stage50: 0.108s slower
```

## 7. Residual diagnosis

Current authored phases start on fixed 5500ms anchors.

A class can clear its role grammar materially faster but still wait for the next fixed authored phase. That creates a plausible masking path where role-local improvement does not shorten Stage settlement or create additional objective consequence.

Classification:
```text
ROLE_SIGNAL_TO_STAGE_CONSEQUENCE_MASKING_WATCH
```

This does **not** justify a scalar change.

It also means the existing objective-pressure watch should not be interpreted as "make every class take wall damage." The cheaper question is whether role grammar chronology can make Archer/Mage mastery expression causally visible at Stage outcome level.

## 8. Current conclusion

```text
MATERIALIZATION_FIDELITY = PASS
STATIC_AUTHORING_LEGALITY = PASS
DYNAMIC_REPRODUCTION = PASS
ROLE_ROTATION_SIGNAL = PASS_WITH_WATCH
OBJECTIVE_PRESSURE_ROTATION = STILL_SKEWED_TOWARD_TANK
ARCHER_WHOLE_WINDOW_TRANSLATION = WEAK
MAGE_WHOLE_WINDOW_TRANSLATION = MIXED
SCALAR_CHANGE_REQUIRED = NOT SHOWN
AUTHORING_ADOPTION = NOT YET
```

## 9. Next bounded diagnostic

Preserve Stage49 exactly.

For Stage50 only, test one minimal chronology variant that moves the existing `DURABLE_CORE_3 / STAGGER_1800` CLUSTER to the **final grammar position**, while preserving:
- the same five grammar templates;
- the same 5500ms phase anchors;
- the same monster bodies/Y geometry inside each grammar;
- the same candidate metadata;
- the same Stage46-48 lead-in;
- all monster/class/shop/EXP/P×P scalars.

Proposed diagnostic order:
```text
Stage49 unchanged:
DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE

Stage50 consequence-translation probe:
DURABLE_SCATTER -> FRONTLINE -> LINE -> LINE_REPRISE -> CLUSTER
```

Purpose:
- test whether placing Mage's role grammar at Stage termination converts local +9.42% role signal into whole-Stage consequence;
- observe whether Stage49's final LINE remains sufficient Archer consequence;
- ensure Knight/Rogue/Tank signals are not destroyed;
- reject if it merely shifts punishment or creates a new class-skew problem.

This is diagnostic only. Do not adopt the order without subsequent evidence/approval.
