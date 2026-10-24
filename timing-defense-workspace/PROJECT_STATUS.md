# Timing Defense — Project Status

Updated: 2026-10-24 KST

## Production / harness
- production branch `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- calibration harness `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- production gameplay/numerical changes remain unauthorized.

## Canonical authority chain
Live remote always wins.
Current key chain:
- P6 closure: `156_P6_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`;
- four-Tier adoption: `158_INITIAL_FOUR_TIER_CAMPAIGN_AND_MONSTER_AVAILABILITY_APPROVED_CONTRACT_V0_1.md`;
- approved lower-layer constraints/correction: `160_FOUR_TIER_AUTHORING_CONSTRAINT_APPROVED_WITH_T1_BASELINE_CORRECTION_V0_1.md`;
- T1 Stage1-50 signature skeleton: `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`;
- static skeleton audit: `162_T1_STAGE_SIGNATURE_STATIC_CONSISTENCY_AUDIT_V0_1.md`;
- representative-slice preflight: `163_T1_REPRESENTATIVE_TRANSITION_SLICE_PREFLIGHT_V0_1.md`;
- deterministic recipe/static preflight: `164_T1_REPRESENTATIVE_TRANSITION_SLICE_RECIPE_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`;
- micro-sim contract: `165_T1_REPRESENTATIVE_TRANSITION_SLICE_MICROSIM_CONTRACT_V0_1.md`;
- runner implementation preflight: `166_T1_TRANSITION_SLICE_MICROSIM_ADAPTER_IMPLEMENTATION_AND_ADMISSION_PREFLIGHT_V0_1.md`;
- exact-source baseline result: `167_T1_TRANSITION_SLICE_EXACT_SOURCE_MICROSIM_RESULT_V0_1.md`;
- pressure-shape/Lv31-absence/duration result: `168_T1_PRESSURE_SHAPE_V0_2_LV31_ABSENCE_AND_DURATION_SENSITIVITY_RESULT_V0_1.md`;
- baseline recipe: `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`;
- v0.2 diagnostic pressure-shape recipe: `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`;
- active plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_46.yaml`.

---

# Current phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 shop = USER APPROVED
P5 class identity group = DIRECTIONALLY CLOSED
P5->P6 fidelity bridge = EXACT TEMP PASS
P6 = USER_APPROVED STRUCTURAL CLOSED WITH WATCHES
Initial campaign = FOUR TIER / USER APPROVED
Monster availability ladder = USER APPROVED
T1 roster = GRUNT / RUNNER / BRUTE / USER APPROVED
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
Representative baseline recipe = STATIC PASS / EXACT-SOURCE DYNAMIC EXECUTED
Dedicated transition runner = IMPLEMENTED / EXACT-SOURCE ADMISSION PASS
Settlement ordering defect = FOUND / CORRECTED / SUPERSEDED FALSE PASS
v0.2 pressure-shape candidate = DIAGNOSTIC ONLY / STATIC PASS / EXACT-SOURCE EXECUTED
Stage41 relief = RECONFIRMED
v0.2 Stage46-50 Lv31 absence = TOO SAFE
pressure duration as mastery-gate lever = SUPPORTED
uniform late-pulse repetition = CLASS-SKEWED / NOT ADOPTED
CURRENT = STAGE49-50 CLASS-ROTATION PRESSURE-SHAPE DIAGNOSTIC
Full exact T1 Stage1-50 recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Fixed campaign authority

```text
T1 = GRUNT / RUNNER / BRUTE
T2 = + SHIELD / FLYER
T3 = + CHARGER / SPLITTER
T4 = + SUPPORTER / SIEGER
T5+ = future expansion
```

Tier identities:
```text
T1 Foundation / Timing & Frontline
T2 Mitigation / Geometry
T3 Burst / Transformation
T4 Formation / Siege
```

Historical GRUNT-mix contradiction remains closed:
```text
obsolete = GRUNT first mixed Stage4-6
canonical = GRUNT first mixed Stage8-12
```
Skeleton uses Stage8. Do not pull RUNNER or BRUTE earlier to satisfy the obsolete window.

---

# T1 structural/static evidence

Skeleton/static audit:
```text
structural FAIL = 0
verdict = PASS_WITH_WATCHES
pressure = BASELINE22 / FLOOD8 / RUSH16 / BULWARK16
complexity = C0 8 / C1 25 / C2 15 / C3 2 / C4 0
rolling 10-Stage class opportunity = 41/41 PASS
```

Baseline representative recipe static result:
```text
Stages = 5, 18, 20-23, 39-45, 46-50
RESULT = PASS
errors = 0
warnings = 0
highest authored 4s density = 8
Stage40 max4s = 6
Stage41 max4s = 3
```

---

# Exact-source runner result

The first exact-source execution appeared to pass admission but manual causal review found a runner defect:
- Tank Stage18 Lv16 ON was delayed by ~3 seconds because Stage-local wall shield/Aftershock was incorrectly required to expire before `STAGE_SETTLED`.

Classification:
```text
FALSE_PASS_SETTLEMENT_ORDERING
```

Minimal correction:
`tools/run_t1_transition_slice_microsim_settlement_fix_v0_1.py`

Correct semantics:
- authored spawns complete;
- zero live Stage-owned enemy;
- delayed combat-event queue drained;
- then Stage-local passive temporary residue clears at the boundary instead of holding an empty Stage open.

Corrected baseline exact run:
```text
run 40074583842
job 120815112194
artifact 12552383686
head 61a4dc2fbef1bcf9bf6c48bee857bdbf2304d0d3
```

Admission PASS:
```text
exactRecipeIdentity
stageSettledOrTerminalFailure
noEnemyCarryAtSettledBoundary
noTransientLeakageAtSettledBoundary
persistentStateContinuity
deterministicReplay
pairedIsolation
explicitSkillStateTrace
```

Baseline dynamic findings:
- Stage5 Lv6 collision = WATCH, not fail;
- Stage18 Lv16 collision = MATERIAL WATCH, especially Archer/Mage compression;
- Stage41 relief shape = supported;
- Stage20-23, 39-45, 46-50 objective-pressure capacity = undershoot;
- baseline Stage46-50 never damaged the wall.

---

# v0.2 pressure-shape diagnostic

Source:
`data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`

Boundary:
- Stage5 unchanged;
- Stage18 unchanged;
- Stage41 unchanged;
- no monster/class/shop/EXP scalar changes;
- right-edge entry retained;
- authored 4s density normal cap 8 retained.

Static gate:
```text
PASS
max4s <= 8 on every representative Stage
Stage40 max4s = 6
Stage41 max4s = 3
```

Final comprehensive exact-source evidence:
```text
run 40075651830
job 120818295930
artifact 12553201879
head bd1959c73235255e9de8a103295d95aa260d69fd
artifact SHA256 a60523c6ed34d58e02aafe6fffffb8f997b2d4d28bf03d8b275c3847ae3da008
```

v0.2 findings:
- Stage20-23 breaks zero-pressure saturation slightly: 2/60 wall-positive rows, total 246 diagnostic wall damage;
- Stage39-45 still has zero wall damage but Stage41 relief is stronger/readable;
- Stage46-50 with Lv31 active has longer interactions but still zero wall damage;
- paired Lv31 absence probe: OFF 15/15 and ON 15/15 both clear Stage46-50 with zero wall damage.

Therefore:
```text
V02_STAGE46_50_MASTERY_GATE = NOT PRESENT
```

---

# Pressure-duration sensitivity

Naive 6/8/10-second pulse repetition was rejected before dynamic interpretation because it violated the authored 4-second density cap.

Wider 11/12/14/16-second spacing remained within the 4-second cap and showed real Lv31 OFF>ON separation without scalar changes.

Representative point:
```text
COPY2_SHIFT11000
Lv31 OFF: wall-positive 5/15 / failures 1 / total wall damage 6184
Lv31 ON : wall-positive 4/15 / failures 0 / total wall damage 777
```

Conclusion:
```text
PRESSURE_DURATION_IS_A_REAL_MASTERY_GATE_LEVER = SUPPORTED
SCALAR_INCREASE_REQUIRED = NOT SHOWN
```

However uniform repetition is not adopted because pressure is class-skewed:
- Tank and Rogue absorb disproportionate late wall pressure;
- Archer/Mage often remain almost untouched;
- this risks becoming a raw-throughput test rather than class-rotating mastery pressure.

---

# Active watches

```text
T1_RUNNER_LV6_PEDAGOGIC_COLLISION_WATCH
T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH
T1_RUNNER_HIGH_PRESSURE_LV16_TAIL_WATCH
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
T4_SUPPORTER_SIEGER_LEARNING_DENSITY_WATCH
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
```

Do not add watches without a concrete failure mode.

---

# Binding interpretation rules

```text
runner/source fidelity
-> lifecycle/state
-> encounter composition / geometry / chronology
-> class/package interaction
-> shop/EXP only if actually coupled
-> exact scalar last
```

Also preserve:
- one encounter ranking is not universal class balance evidence;
- `SURVIVAL != CLEAR`;
- Tank objective protection/control is primary; kill parity is not required;
- no flat shop->EXP correction;
- final EXP semantics route to P10R.

---

# Current work boundary

Next bounded work:
```text
BUILD_STAGE49_50_DISTRIBUTED_DURABLE_SPLIT_AXIS_CANDIDATE
```

Purpose:
- reduce the Tank/Rogue skew created by uniform pulse repetition;
- create spatial/distributed pressure that Archer/Mage cannot solve globally by default;
- preserve Tank control/objective-protection identity;
- use only GRUNT/RUNNER/BRUTE;
- keep right-edge entry and authored 4s density <= 8;
- modify composition/geometry/chronology before any scalar change.

Preserve unchanged during this next slice:
```text
Stage5
Stage18
Stage41
```

Still not authorized/frozen:
- full 50-Stage exact recipe freeze;
- monster/class/shop/EXP/P×P numerical freeze;
- class buffs/nerfs;
- Tank damage normalization;
- boss adoption;
- production gameplay changes.
