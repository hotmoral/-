# 165 — T1 Representative Transition Slice Micro-Sim Contract v0.1

Status: **DIAGNOSTIC EXECUTION CONTRACT / RUNNER IMPLEMENTATION REQUIRED / NO BALANCE FREEZE**

## 1. Purpose

Define the minimum executable contract required to interpret dynamic combat behavior for the T1 representative transition recipes materialized in `164_T1_REPRESENTATIVE_TRANSITION_SLICE_RECIPE_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`.

The runner must consume the exact recipe source:

- `data/t1_representative_transition_slice_recipes_v0_1.yaml`

No legacy late-stage fixture, recipe substitution, or silent normalization may replace those recipes.

Execution is admitted only after the static preflight remains:

```text
RESULT=PASS errors=0 warnings=0
```

This contract does not authorize production gameplay changes, class buffs/nerfs, EXP/shop changes, or a full T1 Stage1-50 recipe freeze.

---

## 2. Authority chain

### Campaign / authoring authority

- `160_FOUR_TIER_AUTHORING_CONSTRAINT_APPROVED_WITH_T1_BASELINE_CORRECTION_V0_1.md`
- `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`
- `163_T1_REPRESENTATIVE_TRANSITION_SLICE_PREFLIGHT_V0_1.md`
- `164_T1_REPRESENTATIVE_TRANSITION_SLICE_RECIPE_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`

### Lifecycle / deterministic execution authority

- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
- `144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`

### Class / skill authority

- existing approved class packages and radar invariants;
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`;
- `96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`;
- later fidelity corrections such as `103_P4D2_TANK_BARRIER_FIDELITY_CORRECTION_V0_1.md` and `121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md` where the affected mechanic is exercised.

P4D2 numerical anchors remain diagnostic/provisional unless separately approved. Their existence does not make them production balance authority.

---

## 3. Runner admission gates

Dynamic combat output is interpretable only if all gates below pass.

### 3.1 Exact recipe identity

The runner must ingest the exact recipe object from:

`data/t1_representative_transition_slice_recipes_v0_1.yaml`

It must report recipe id and a deterministic source digest or equivalent immutable identity evidence for every executed Stage.

Any substitution is:

```text
RUNNER_FIDELITY_FAIL
```

### 3.2 Stage lifecycle

Every sequential Stage must terminate only at `STAGE_SETTLED`:

```text
last authored spawn complete
+ zero live Stage-owned enemy
+ authorized effects drained
+ no unresolved delayed Stage transient
```

Forbidden:

- arbitrary timer deletion;
- enemy carry into the next Stage;
- unresolved Stage-owned transient carry;
- Stage advance at last-spawn time alone.

### 3.3 Persistent run state

Within sequential slices, the following persist across Stage/shop/intermission according to approved authority:

```text
wall HP deficit
combo
charge
```

The runner must trace entry and exit values for each Stage.

An unauthorized reset is:

```text
LIFECYCLE_INVARIANT_FAIL
```

### 3.4 Determinism and pairing

Use deterministic RNG/player-model substreams.

Paired OFF/ON comparisons must share:

- exact recipe object;
- exact seed and deterministic substreams;
- same player-model realization;
- same initial lifecycle state;
- same non-tested skill state.

Only the tested skill activation may differ.

### 3.5 Explicit skill-state trace

For every Stage record:

- class;
- active milestone skills;
- tested skill enabled/disabled state;
- Lv31 activation position where applicable.

A reported result without explicit skill-state evidence is not admissible for collision interpretation.

---

## 4. Execution groups

Execution order is fixed so fidelity defects are found before longer sequential runs.

### Group A — Stage5 RUNNER teach × Lv6

Exact recipe:

`T1_S05_RUNNER_TEACH`

Paired comparison:

```text
Lv6 OFF
vs
Lv6 ON
```

Purpose: distinguish readable RUNNER teaching from a skill-acquisition collision.

Do not fit EXP to force one side of the pair.

### Group B — Stage18 BRUTE first mixed × Lv16

Exact recipe:

`T1_S18_BRUTE_FIRST_MIX`

Paired comparison:

```text
Lv16 OFF
vs
Lv16 ON
```

Purpose: determine whether BRUTE first-mixed readability survives the provisional Lv16 reach region.

### Group C — Stage20→23 gate / first high-pressure ramp

Sequential execution:

```text
20 -> 21 -> 22 -> 23
```

State persists continuously across the slice.

Purpose:

- inspect Stage20 star-gate transition;
- inspect Stage21 RUNNER first high pressure;
- inspect Stage22 BRUTE first high pressure;
- inspect Stage23 mixed RUSH+BULWARK;
- detect wall/combo/charge accumulation effects that isolated recipes cannot show.

### Group D — Stage39→45 2★ gate / Lv31 ascension

Sequential execution:

```text
39 -> 40 -> 41 -> 42 -> 43 -> 44 -> 45
```

Run three diagnostic activation-position variants:

```text
Lv31 activates before Stage41
Lv31 activates before Stage43
Lv31 activates before Stage45
```

These variants answer a reach-position sensitivity question only.

They **must not** be interpreted as an EXP formula freeze or proof of actual launch reach.

### Group E — Stage46→50 post-Lv31 mastery / final

Sequential execution:

```text
46 -> 47 -> 48 -> 49 -> 50
```

Lv31 is active for the whole slice.

Purpose: test recombination of already taught T1 vocabulary after the confirmed ascension window without adding new ordinary mechanics.

---

## 5. Required metrics

Keep dimensions separate. Do not collapse them into one fairness score.

At minimum record per Stage / class / variant:

```text
authoredSpawnCount
effectiveEntityCount
peakActive
max4sDensity
max6sDensity
frontlineBlockTime
targetReorderCount
backlineExposure where applicable
spawnToFirstContact
removalThroughput
controlValue
wallDamage
wallReserve
rootTimingActionCount
stageSettledTime
failureClassification
```

Also record directional class-opportunity / weakness observations.

### Tank-specific attribution

Tank must be assessed for objective protection, not kill parity.

When relevant, record the amount/direction of wall-pressure reduction attributable to:

- push/control;
- barrier/defense;
- slowdown/space creation;
- other approved Tank control effects.

Low removal alone is not a Tank defect.

---

## 6. Failure classification

At minimum support:

```text
RUNNER_FIDELITY_FAIL
LIFECYCLE_INVARIANT_FAIL
AUTHORING_COLLISION
CLASS_OPPORTUNITY_WEAKNESS
CHRONOLOGY_ORDERING_EFFECT
SCALAR_SENSITIVITY_CANDIDATE
PASS_WITH_WATCH
```

Classification is causal, not cosmetic.

The interpretation order is mandatory:

```text
runner/source fidelity
-> lifecycle/state
-> encounter composition / geometry / chronology
-> skill/class-package interaction
-> shop/EXP feedback only if actually coupled
-> scalar sensitivity last
```

Do not recommend scalar changes before earlier causes are excluded.

---

## 7. Paired-comparison interpretation

For Groups A/B:

- compare identical recipe + identical deterministic state;
- report absolute values and directional deltas;
- report target-order or chronology changes explicitly;
- do not assume a monotonic effect merely because a skill is stronger;
- do not overstate small deterministic samples as population balance.

A legitimate discrete chronology exception is not automatically a validator failure. It must be classified and explained.

---

## 8. Runner reuse boundary

### Not admissible as-is

`tools/simulate_class_aware_layer_a.py` is not admissible for Groups C/D/E because its isolated-recipe lifecycle does not preserve the required sequential run state and its skill surface is insufficient for the current Lv16/Lv31 contract.

### Reference-only reuse

Later P5/P6 runners may be reused as implementation references for:

- persistent state semantics;
- `STAGE_SETTLED`;
- class packages;
- wall-pressure attribution;
- deterministic tracing.

They may not silently inject their historical late-stage fixtures into current T1 recipes.

### Required implementation

Build a small dedicated adapter/runner that:

1. reads the exact T1 transition recipe YAML;
2. reuses approved lifecycle/class/skill semantics rather than recreating them inconsistently;
3. supports paired skill toggles and Lv31 activation-position variants;
4. emits the required metrics and invariant evidence;
5. fails closed on recipe/lifecycle mismatch.

---

## 9. Prohibited inferences / changes

This diagnostic does not authorize:

- final EXP formula or milestone reach freeze;
- shop numerical changes or freeze;
- class buffs/nerfs;
- Tank damage normalization;
- P×P / timing-judgment probability changes;
- monster scalar freeze;
- boss adoption;
- production gameplay changes;
- full T1 Stage1-50 exact recipe freeze;
- a target that all classes must clear at equal rates;
- treating survival as clear.

---

## 10. Stop conditions

Stop dynamic interpretation immediately if any of the following occurs:

- recipe identity mismatch;
- unauthorized state reset;
- Stage advances before `STAGE_SETTLED`;
- enemy/transient leakage between Stages;
- tested paired variants differ in more than the intended skill state;
- deterministic replay of the same input diverges materially.

Fix the runner/fidelity issue before continuing balance interpretation.

---

## 11. Decision

```text
microSimContract = COMPLETE
staticRecipePreflight = PASS
runnerImplementation = REQUIRED_NEXT
microSimExecution = NOT_STARTED
fullT1ExactRecipeFreeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```
