# Timing Defense — Next Work Boundary

Updated: 2026-10-25 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_47.yaml`;
5. read `169_T1_STAGE49_50_CLASS_ROTATION_AND_SUSTAIN_DIAGNOSTIC_RESULT_V0_1.md`;
6. read compact summary `legacy-game-structure/data/t1_stage49_50_class_rotation_diagnostic_center_summary_v0_1.json`;
7. inspect v0.2 recipe `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`;
8. preserve `168` pressure/duration result and `167` exact baseline result;
9. preserve runner contract/implementation `165/166`, settlement bridge, Mage Lv31 fidelity bridge and Archer diagnostic width bridge;
10. preserve T1 skeleton/static authority `160-164` and P6 closure `156`;
11. verify production/harness heads.

Do not rerun closed P6, the full T1 skeleton audit, baseline exact-source diagnostics, or the completed Stage49-50 order/sustain search without a concrete trigger.

---

# Current phase

```text
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
baseline representative recipe = STATIC PASS / EXACT-SOURCE EXECUTED
micro-sim runner = EXACT-SOURCE ADMISSION PASS AFTER SETTLEMENT CORRECTION
v0.2 pressure-shape candidate = STATIC PASS / DYNAMIC DIAGNOSTIC ONLY
Stage41 relief = RECONFIRMED
v0.2 Stage46-50 Lv31 absence = TOO SAFE
pressure duration lever = SUPPORTED
uniform pulse repetition = CLASS-SKEWED / NOT ADOPTED
Stage49-50 class-rotation diagnostic = PASS_WITH_WATCH
DIAGNOSTIC CENTER = STAGGER_1800
objective-pressure rotation = STILL SKEWED TOWARD TANK
CURRENT = STAGE49-50 AUTHORING-CANDIDATE MATERIALIZATION + STATIC PREFLIGHT
full 50-Stage exact recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Evidence to preserve

## Stage49-50 exact diagnostic center
Exact green run:
```text
run 40153142570
artifact 12583341810
head 5eb71a861b1226887a8ec09dce98641c0dfff817
artifact sha256 ab31640122bd1d00179d5af62104368cb46ad4e5d4137fb8922d561ebbfcacf5
fidelityErrors = []
```

Diagnostic order:
```text
Stage49: DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE
Stage50: DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE -> LINE_REPRISE
CLUSTER: BRUTE / GRUNT / BRUTE / GRUNT / BRUTE / GRUNT
```

Diagnostic timing center:
```text
STAGGER_1800 offsets = 0 / 360 / 720 / 1080 / 1440 / 1800 ms
phase gap = 5500 ms
```

Static diagnostic evidence:
```text
Stage49 authored 24 / max4s 6 / max6s 11
Stage50 authored 30 / max4s 6 / max6s 9
Y spread 0.18..0.82
```

Role-facing Lv31 OFF->ON direction:
```text
Knight +43.03%
Rogue +30.07%
Tank +27.37% + 3 unresolved reduced
Archer +1.72%
Mage +9.42%
```

Tank objective protection:
```text
OFF wall damage 1358
ON wall damage 164
```

Residual watch:
```text
material wall pressure appears only in Tank cases in this exact sample
```
This is not a demand for equal wall damage. It means the authoring candidate must be checked for accidental Tank-only punishment.

## Fidelity cautions
Mage Lv31 bridge is a semantic fidelity correction, not a numerical freeze.

Archer Lv31 `yTolerance=0.20` is diagnostic only. Do not encode it as production authority in the recipe.

---

# Exact next bounded task

Materialize a **Stage49-50-only authoring candidate** derived from `STAGGER_1800`, then run static preflight.

This is candidate materialization, not adoption.

Required content direction:
```text
Stage49:
DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE

Stage50:
DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE -> LINE_REPRISE

CLUSTER durable center:
BRUTE / GRUNT / BRUTE / GRUNT / BRUTE / GRUNT

CLUSTER offsets:
0 / 360 / 720 / 1080 / 1440 / 1800 ms
```

Do not invent new monster types or scalar values.

---

# Static preflight gates

The materialized candidate must prove:

```text
1. source/schema parse PASS;
2. only Stage49 and Stage50 differ from v0.2;
3. Stage5 / Stage18 / Stage41 byte/semantic content unchanged;
4. T1 vocabulary = GRUNT/RUNNER/BRUTE only;
5. physical entry remains right-edge / no midfield pop-in;
6. authored 4-second density <= 8;
7. Stage49/50 authored count matches intended materialization;
8. Y spread and split-axis geometry remain intentional;
9. grammar order and phase separation match the diagnostic center;
10. no monster/class/shop/EXP/P×P scalar mutation;
11. T1 skeleton pressure/complexity intent not contradicted;
12. candidate clearly labelled NON_PRODUCTION / NO_NUMERICAL_FREEZE.
```

If any static gate fails, repair the minimum authoring defect before dynamic execution.

---

# What comes after static PASS

Only after static PASS:
- run a narrow exact-source Stage49-50 dynamic admission against the materialized candidate;
- compare to v0.2 and the `STAGGER_1800` diagnostic evidence;
- confirm the materialized data reproduces the intended role-facing shape without introducing a new lifecycle/source mismatch.

Do **not** jump directly to full Stage1-50 authoring.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE49-50 ONLY
PRESERVE STAGE5 / STAGE18 / STAGE41
NO FULL-50 EXACT AUTHORING YET
NO CLASS BUFF/NERF FROM THIS SLICE
SURVIVAL != CLEAR
TANK KILL PARITY NOT REQUIRED
AUTHORED 4s DENSITY <= 8
NO MONSTER/CLASS SCALAR CHANGE
NO SHOP/EXP/P×P PROBABILITY CHANGE
NO FLAT SHOP->EXP MULTIPLIER
FINAL EXP ROUTING = P10R
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```
