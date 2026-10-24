# 168 — T1 Pressure Shape v0.2 / Lv31 Absence / Duration Sensitivity Result v0.1

Status: **DIAGNOSTIC RESULT / V0.2 BASE STILL UNDERSHOOT / DURATION LEVER CONFIRMED / UNIFORM REPETITION CLASS-SKEWED / NO AUTHORING ADOPTION / NO NUMERICAL FREEZE**

## 1. Purpose

Continue the bounded diagnosis from `167` without opening full Stage1-50 exact authoring or changing combat scalars.

Questions:

1. can Stage20-23 / 39-45 / 46-50 gain meaningful pressure through composition/cadence/overlap only?
2. does the revised Stage46-50 pressure distinguish Lv31 OFF from Lv31 ON?
3. if not, can increased pressure **duration** create the intended mastery-gate separation while preserving the 4-second density guard?
4. does a uniform duration increase preserve class-opportunity rotation, or does it over-punish a subset of classes?

---

## 2. Candidate under test

Source:
`data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`

Status remains:

```text
DIAGNOSTIC_PRESSURE_SHAPE_REVISION_CANDIDATE_NO_PRODUCTION_FREEZE
```

Scope:
- Stage5 unchanged byte-semantically;
- Stage18 unchanged byte-semantically;
- Stage41 unchanged byte-semantically;
- revised only Stage20-23, 39-40 and 42-50;
- no monster scalar change;
- no class scalar change;
- no shop/EXP change;
- normal right-edge entry retained;
- authored 4s normal cap remains 8.

Exact recipe SHA256:

```text
3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
```

---

## 3. Exact-source evidence

Final comprehensive run for this work group:

```text
workflow run = 40075651830
job = 120818295930
artifact = 12553201879
head SHA = bd1959c73235255e9de8a103295d95aa260d69fd
artifact ZIP SHA256 = a60523c6ed34d58e02aafe6fffffb8f997b2d4d28bf03d8b275c3847ae3da008
main A-E JSON SHA256 = a87ad2bf30342ccf18db576b130bf70c6a2504335605a5d425448a6f311e178b
Lv31 absence JSON SHA256 = 314f3caa53a41cc30e4b463607c932f56ee0b02523c52a12bfb253710138bf79
duration search JSON SHA256 = 7c9547252160584917694c6bd2b071ef4120d0181c81ea66225d5bd8c530fba9
seeds = 101 / 211 / 307
```

Machine-readable compact summary:
`data/t1_pressure_shape_v0_2_and_duration_sensitivity_summary_v0_1.json`

Admission remains PASS:

```text
exactRecipeIdentity = PASS
stageSettledOrTerminalFailure = PASS
noEnemyCarryAtSettledBoundary = PASS
noTransientLeakageAtSettledBoundary = PASS
persistentStateContinuity = PASS
deterministicReplay = PASS
pairedIsolation = PASS
explicitSkillStateTrace = PASS
lifecycleFailures = 0
pairFailures = 0
replayFailures = 0
```

The settlement correction from `167` remains active. No result below uses the superseded false-pass lifecycle interpretation.

---

## 4. Static pressure-shape gate

v0.2 exact-source static result:

```text
Stage  authored  max4s  max6s
5      4         4      4
18     6         6      6
20     10        6      9
21     12        8      12
22     10        6      6
23     12        6      9
39     14        8      12
40     11        6      9
41     5         3      4
42     8         5      8
43     8         6      6
44     10        8      10
45     12        6      9
46     13        7      10
47     14        8      12
48     16        8      12
49     15        8      10
50     18        8      12
```

Therefore:

```text
max authored 4s density <= 8 = PASS
Stage5 unchanged = PASS
Stage18 unchanged = PASS
Stage41 unchanged = PASS
Stage41 relief density 3 < Stage40 density 6 = PASS
```

A first naive repetition search at 6/8/10-second spacing was rejected because Stage49/50 and other late Stages exceeded the 4-second density cap. Those candidates were not dynamically interpreted.

---

## 5. v0.2 A/B isolation result

Because Stage5 and Stage18 were intentionally unchanged, their exact A/B result remains the same as `167`.

This matters methodologically: the pressure-repair experiment did not contaminate the existing Lv6/Lv16 collision questions.

```text
Stage5 Lv6 watch = unchanged / WATCH_NOT_FAIL
Stage18 Lv16 watch = unchanged / MATERIAL_WATCH
```

No class buff/nerf inference is introduced here.

---

## 6. v0.2 sequential pressure result

### Stage20-23

v0.1 had zero wall-pressure rows.

v0.2 creates a small amount of real objective pressure:

```text
wall-damage-positive rows = 2 / 60
total wall damage = 246 diagnostic HP
```

Observed rows:
- Tank seed101 Stage20: 82
- Tank seed307 Stage23: 164

Interpretation:
- composition/cadence extension can break the previous zero-pressure saturation;
- but the signal is sparse and class-skewed;
- Stage20-23 is improved directionally, not yet authoring-frozen.

### Stage39-45

All rows still settle with zero wall damage.

However the dynamic shape is stronger than v0.1:

```text
Stage39 mean settled 15.271 s / peak active 6.133
Stage40 mean settled  9.172 s / peak active 4.200
Stage41 mean settled  7.359 s / peak active 1.733
Stage42 mean settled  7.890 s / peak active 2.600
Stage43 mean settled  9.307 s / peak active 3.200
Stage44 mean settled  6.919 s / peak active 5.089
Stage45 mean settled 11.059 s / peak active 4.111
```

Stage41 relief remains clearly visible:

```text
Stage39 peak 6.133
Stage40 peak 4.200
Stage41 peak 1.733
```

Decision:

```text
Stage41 relief shape = RECONFIRMED
Stage39-45 objective-pressure calibration = still underpowered / not resolved
```

### Stage46-50 with Lv31 active

Mean settled times rose materially from v0.1:

```text
Stage46: Archer 8.800 / Knight 11.827 / Mage 11.240 / Rogue 12.358 / Tank 15.400
Stage47: Archer 9.267 / Knight  8.473 / Mage  8.767 / Rogue  8.575 / Tank  8.900
Stage48: Archer 8.567 / Knight  8.240 / Mage  8.867 / Rogue  8.575 / Tank  8.333
Stage49: Archer13.933 / Knight 12.240 / Mage 11.493 / Rogue 12.275 / Tank 14.300
Stage50: Archer11.533 / Knight 12.340 / Mage 13.160 / Rogue 11.605 / Tank 17.600
```

Yet:

```text
wall-damage-positive rows = 0 / 75
```

This alone does not prove failure, because successful Lv31 play may legitimately protect the wall. Therefore an explicit Lv31-absence comparison was required before increasing pressure again.

---

## 7. Lv31 absence probe — decisive v0.2 base finding

Exact paired Stage46-50 probe:

```text
classes = 5
seeds = 3
cases = 15 paired OFF/ON
same initial lifecycle state = required
Lv6/11/16/21/26 active on both sides
only Lv31 differs
```

Result:

```text
Lv31 OFF:
  Stage46-50 completed = 15/15
  wall-damage-positive = 0/15
  failures = 0
  mean final Base HP = 2000

Lv31 ON:
  Stage46-50 completed = 15/15
  wall-damage-positive = 0/15
  failures = 0
  mean final Base HP = 2000
```

Therefore v0.2 base is not merely `Lv31-success-safe`; it is also `Lv31-absence-safe` under the current diagnostic player model.

Classification:

```text
V02_STAGE46_50_MASTERY_GATE = NOT YET PRESENT
PRESSURE_DURATION_OR_SHAPE_MUST DEEPEN BEFORE SCALAR TUNING
```

This directly answers the ambiguity left by the first v0.2 run.

---

## 8. Pressure-duration sensitivity

To avoid arbitrary count inflation, the next probe kept:
- the same monster anchors;
- the same class/skill anchors;
- the same within-pulse composition/order;
- the same 4-second density cap;
- the same right-edge entry;

and varied only how many copies of the existing Stage46-50 pulse continued later in time.

First, 6-10 second spacing was rejected by the static density guard.

A widened 11/12/14/16-second spacing search admitted all tested candidates while keeping:

```text
Stage46 max4 <= 7
Stage47 max4 <= 8
Stage48 max4 <= 8
Stage49 max4 <= 8
Stage50 max4 <= 8
```

### Representative sensitivity points

#### One additional pulse / 11s spacing

```text
OFF wall-positive 3/15
ON  wall-positive 1/15
OFF failures 0
ON  failures 0
OFF total wall damage 1740
ON  total wall damage 408
```

#### Two additional pulses / 11s spacing

```text
OFF wall-positive 5/15
ON  wall-positive 4/15
OFF failures 1
ON  failures 0
OFF total wall damage 6184
ON  total wall damage 777
OFF mean final Base HP 1590.067
ON  mean final Base HP 1948.200
```

#### Three additional pulses / 11s spacing

```text
OFF wall-positive 10/15
ON  wall-positive 9/15
OFF failures 3
ON  failures 0
OFF total wall damage 9556
ON  total wall damage 4400
```

The same broad OFF>ON wall-damage direction appears across the 11-16s spacing grid.

Therefore:

```text
PRESSURE_DURATION_IS_A_REAL_MASTERY_GATE_LEVER = SUPPORTED
SCALAR_INCREASE_REQUIRED = NOT SHOWN
```

---

## 9. Why no duration candidate is adopted

The uniform-repeat sensitivity exposes a second-order problem.

At `COPY2_SHIFT11000`, wall pressure is concentrated mainly in Tank and Rogue, especially Stage49-50:

```text
Tank OFF:
  Stage47 56 total across seeds
  Stage48 408
  Stage49 1606
  Stage50 2554
  one failure

Tank ON:
  Stage48 2
  Stage49 28
  Stage50 597
  no failures

Rogue OFF Stage50 = 1350 in one seed
Rogue ON  Stage50 = 150 in one seed
Knight receives a smaller Stage50 signal.
Archer/Mage remain effectively protected in this candidate.
```

This is useful evidence that Lv31 has real value, especially for Tank, but it is not an acceptable reason to freeze the uniform repetition pattern.

Reason:
- Tank's control/defense identity must not be interpreted through kill parity;
- a mastery gate should arise from class-readable pressure, not merely punish the slower remover;
- Archer strict-line and Mage density strengths need spatially meaningful counter-pressure as well;
- one universal repeated pulse risks converting the encounter into a raw throughput test.

Classification:

```text
UNIFORM_LATE_PULSE_REPETITION = DIAGNOSTICALLY_USEFUL / NOT AUTHORING-CANDIDATE-READY
```

---

## 10. Cross-system consistency result

No contradiction was found with:
- T1 G/R/B vocabulary;
- Stage41 relief contract;
- Stage46+ mastery-gate direction;
- right-edge spawn rule;
- STAGE_SETTLED lifecycle;
- class identity / no forced parity;
- Tank objective-protection interpretation;
- 4-second authored density guard.

One important negative result remains:
- increasing duration uniformly can create the desired mastery separation **but** rotates pressure poorly across classes.

Therefore the next fix must stay in encounter shape before scalars.

---

## 11. Exact next bounded work

Do not add another universal pulse and do not change monster HP/speed/wall damage yet.

Next diagnostic scope:

```text
Stage49-50 only
```

Construct a bounded **distributed durable / split-axis pressure-shape candidate** that:

1. uses only GRUNT/RUNNER/BRUTE;
2. keeps right-edge entry;
3. keeps authored 4-second density <= 8;
4. uses split-axis/distributed geometry so Archer strict-line and Mage local-density advantages are not automatically global answers;
5. retains enough durable/frontline time for Rogue's durable-normal identity to matter;
6. allows Tank's global/control/defense Lv31 identity to protect the objective rather than requiring Tank kill parity;
7. does not change Stage41 or earlier teaching;
8. does not change class/monster scalars;
9. is compared against v0.2 and the duration-sensitivity envelope, not immediately adopted.

Only if composition/geometry/chronology cannot generate a reasonable multi-class pressure rotation should exact scalar sensitivity be reopened.

---

## 12. Decision state

```text
v0.2 pressure-shape candidate = DIAGNOSTIC ONLY
exact-source admission = PASS
Stage41 relief = RECONFIRMED
v0.2 Stage46-50 Lv31 absence = TOO SAFE
pressure duration as a lever = SUPPORTED
6-10s naive repetition = REJECTED BY DENSITY GUARD
11-16s spaced repetition = DYNAMICALLY INFORMATIVE
uniform repetition = CLASS-SKEWED / NOT ADOPTED
next = STAGE49_50_DISTRIBUTED_DURABLE_SPLIT_AXIS_CANDIDATE
full T1 exact recipe freeze = DEFERRED
monster/class scalar freeze = NO
production gameplay change = UNAUTHORIZED
```
