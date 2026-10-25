# T1 Stage49-50 Class-Rotation / Sustain Diagnostic Result v0.1

Date: 2026-10-25 KST

Status:
**PASS_WITH_WATCH / DIAGNOSTIC CENTER SELECTED / NO AUTHORING ADOPTION / NO NUMERICAL FREEZE**

## 1. Scope

This result closes the bounded Stage49-50 diagnostic that followed the v0.2 pressure-shape and duration-sensitivity work.

It does **not** freeze production recipes, monster/class coefficients, P×P probabilities, shop/EXP values, Archer Lv31 width, Mage Lv31 numerical centers, or full T1 Stage1-50 authoring.

Preserved throughout:
- Stage5 unchanged;
- Stage18 unchanged;
- Stage41 unchanged;
- GRUNT/RUNNER/BRUTE only;
- right-edge spawning;
- authored 4-second normal density cap <= 8;
- production branch untouched.

## 2. Runner-fidelity corrections found before balance interpretation

### Mage Lv31
The T1 transition runner under-represented the approved Lv31 staged-collapse semantics in two ways:
1. Y radius did not inherit the earlier Lv11 radius expansion before the Lv21/Lv31 growth;
2. the final chain did not exclude the complete hit set accumulated across all preceding AoE stages.

Minimal diagnostic bridge:
`tools/t1_transition_microsim_mage_lv31_fidelity_bridge_v0_1.py`

Bridge status:
- production gameplay change: false;
- numerical freeze: false;
- semantic fidelity correction only.

After correction, Mage ROT0 Lv31 benefit increased materially, but ROT1/2/3 chronology sensitivity did not disappear. Therefore the remaining effect is not explained away by the fidelity defect.

### Archer Lv31
Latest structural authority requires a materially wider straight corridor than ordinary/Lv26 line behavior, while exact width remains unfrozen.

For this bounded diagnostic only, the existing Archer width bridge used:
`yTolerance = 0.20`

Status:
`DIAGNOSTIC_ONLY_NOT_FROZEN`

Do not promote 0.20 to production authority from this result.

## 3. Root-cause decomposition

### Archer
The main instability was not demonstrated to be a damage-coefficient problem.

When a BRUTE from the preceding `DURABLE_SCATTER` grammar remained frontmost, system targeting anchored Sky-Piercing Arrow to that older Y axis. A subsequent LINE grammar could then receive little value even though the P×P activation occurred during the nominal LINE phase.

Classification:
`PREVIOUS_GRAMMAR_FRONTMOST_TARGET_CONTAMINATION`

Cheapest correction direction:
- encounter chronology / grammar transition;
- not an Archer buff.

### Mage
The main instability was not demonstrated to be a damage-coefficient problem.

A burst CLUSTER could have all authored enemies spawned but already be mostly resolved by the time the next P×P arrived. In those cases Lv31 technically fired but behaved like a one-target finisher instead of a density-collapse package.

Classification:
`PXP_PHASE_ALIGNMENT_AND_CLUSTER_LIFETIME_SENSITIVITY`

A durable center was required. Pure GRUNT speed-matching dissolved too quickly. BRUTE2 improved expression; BRUTE3 was the first tested durable core to restore positive Mage role expression in the integrated class-rotation shape.

## 4. Integrated diagnostic shape

Diagnostic grammar order:

```text
Stage49:
DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE

Stage50:
DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE -> LINE_REPRISE
```

Diagnostic CLUSTER morphology:

```text
BRUTE / GRUNT / BRUTE / GRUNT / BRUTE / GRUNT
```

The two final sustain timings compared were:

```text
STAGGER_1800 offsets = 0 / 360 / 720 / 1080 / 1440 / 1800 ms
SUSTAIN_3000 offsets = 0 / 600 / 1200 / 1800 / 2400 / 3000 ms
```

Both retained:
- Stage49 authored count 24;
- Stage50 authored count 30;
- max4s = 6 on Stage49;
- max4s = 6 on Stage50;
- Y spread 0.18..0.82;
- no static errors.

## 5. Exact-source green evidence

Workflow:
`.github/workflows/timing-defense-t1-stage49-50-sustain-integration-compare.yml`

Exact green run:

```text
run      40153142570
artifact 12583341810
head     5eb71a861b1226887a8ec09dce98641c0dfff817
artifact digest sha256 ab31640122bd1d00179d5af62104368cb46ad4e5d4137fb8922d561ebbfcacf5
recipe sha256          3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
seeds                  101,211,307,409,503
```

Fidelity/static gate:

```text
fidelityErrors = []
STAGGER_1800 staticErrors = []
SUSTAIN_3000 staticErrors = []
max4s <= 8 = PASS
same deterministic lifecycle / paired isolation = PASS
```

## 6. STAGGER_1800 result

Role-facing clear-latency direction, Lv31 OFF -> ON:

```text
Knight: 7920.0 -> 4512.0 ms   improvement 43.03%
Rogue : 5441.0 -> 3805.1 ms   improvement 30.07%
Tank  : 13933.3 -> 10120.0 ms improvement 27.37% + 3 unresolved reduced
Archer: 4253.3 -> 4180.0 ms   improvement 1.72%
Mage  : 4288.0 -> 3884.0 ms   improvement 9.42%
```

Tank objective-protection signal:

```text
Lv31 OFF total wall damage = 1358
Lv31 ON  total wall damage = 164
wall-damage reduction      = 1194
OFF wall-positive cases    = 2/5
ON wall-positive cases     = 1/5
fail/incomplete cases      = 0 on both sides
```

Whole Stage49-50 paired window:

```text
OFF total wall damage = 1358 / mean final Base HP 1945.68
ON  total wall damage = 164  / mean final Base HP 1993.44
```

## 7. Why STAGGER_1800 is the diagnostic center

`SUSTAIN_3000` also produced positive role-facing direction for all five classes and passed the same static/fidelity guards.

However:
- Mage improvement was slightly smaller: 8.96% vs 9.42%;
- the 3.0-second spread changes F03 cluster cadence more materially;
- STAGGER_1800 achieves the same qualitative class-direction result with the smaller chronology change.

Therefore:

```text
DIAGNOSTIC_CENTER = STAGGER_1800
```

This is a minimality decision, not a production freeze.

## 8. Residual watch / why this is not authoring adoption yet

The diagnostic solved several role-expression problems but did **not** prove fully distributed objective pressure.

In STAGGER_1800:
- wall damage remains concentrated in Tank cases;
- Archer/Mage/Knight/Rogue show role-facing timing/exposure differences without wall damage;
- Tank remains the only class with material wall-pressure evidence in this exact sample.

Therefore the correct interpretation is:

```text
ROLE_ROTATION_SIGNAL = IMPROVED
OBJECTIVE_PRESSURE_ROTATION = STILL_SKEWED
SCALAR_CHANGE_REQUIRED = NOT SHOWN
AUTHORING_ADOPTION = NOT YET
```

Do not equalize wall damage across classes as a target. The next authoring candidate should preserve real class strengths/weaknesses while checking that the diagnostic shape is structurally legal and does not simply encode a Tank-only punishment.

## 9. Next boundary

Materialize a **Stage49-50-only authoring candidate** from the STAGGER_1800 diagnostic center and run static preflight before any wider exact dynamic authoring.

The candidate must remain diagnostic/non-production and preserve:
- Stage5 / Stage18 / Stage41;
- current monster/class scalars;
- shop/EXP/P×P probabilities;
- right-edge entry;
- 4-second authored density <= 8;
- no full-50 recipe freeze.

The static preflight must check at minimum:
- schema/source identity;
- monster vocabulary legality;
- Stage49/50 authored count and density;
- Y spread / right-edge entry;
- grammar order and phase separation;
- no accidental edits outside Stage49/50;
- consistency with T1 skeleton pressure/complexity intent.
