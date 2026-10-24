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
- deterministic recipes/static preflight: `164_T1_REPRESENTATIVE_TRANSITION_SLICE_RECIPE_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`;
- micro-sim contract: `165_T1_REPRESENTATIVE_TRANSITION_SLICE_MICROSIM_CONTRACT_V0_1.md`;
- runner implementation preflight: `166_T1_TRANSITION_SLICE_MICROSIM_ADAPTER_IMPLEMENTATION_AND_ADMISSION_PREFLIGHT_V0_1.md`;
- recipe data: `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`;
- active plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_45.yaml`.

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
Lower-layer authoring constraints = USER APPROVED WITH T1 BASELINE CORRECTION
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
Representative transition recipes = MATERIALIZED / STATIC PASS
Micro-sim execution contract = COMPLETE
Dedicated transition-slice runner = IMPLEMENTED
Local semantic runner smoke = PASS / ENGINEERING ONLY
Exact canonical-source dynamic execution = PENDING
CURRENT = T1 TRANSITION SLICE MICROSIM EXACT-SOURCE EXECUTION
Full exact T1 Stage1-50 recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Four-Tier authority

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

Historical GRUNT mix contradiction remains closed by the minimal correction:
```text
GRUNT first mixed = Stage8-12
```
Skeleton uses Stage8. Do not reintroduce Stage4-6 or pull RUNNER/BRUTE forward to satisfy the obsolete window.

---

# T1 skeleton / static evidence

Skeleton/audit result:
```text
structural FAIL = 0
verdict = PASS_WITH_WATCHES
pressure = BASELINE22 / FLOOD8 / RUSH16 / BULWARK16
complexity = C0 8 / C1 25 / C2 15 / C3 2 / C4 0
rolling 10-Stage class opportunity = 41/41 PASS
```

Representative deterministic recipe static result:
```text
Stages = 5, 18, 20-23, 39-45, 46-50
RESULT = PASS
errors = 0
warnings = 0
highest authored 4s density = 8
Stage40 max4s = 6
Stage41 max4s = 3
```

This is structural/static evidence only, not dynamic clearability or balance proof.

---

# Dedicated micro-sim runner

Implemented assets:
```text
tools/run_t1_transition_slice_microsim_v0_1.py
tools/t1_transition_microsim_core_v0_1.py
tools/t1_transition_microsim_skills_v0_1.py
tools/t1_transition_microsim_engine_v0_1.py
```

Runner admission covers:
- exact source identity evidence via source/per-recipe SHA256;
- exact Stage/group contract;
- `STAGE_SETTLED` or terminal wall failure;
- no arbitrary timer deletion;
- no enemy carry at settled boundary;
- no Stage-local transient leakage;
- wall deficit/combo/charge continuity;
- deterministic judgment/proc state continuity;
- OFF/ON pair isolation;
- explicit skill-state tracing;
- deterministic replay.

Safety timeout is fail-closed: it raises a runner-fidelity error and never deletes enemies or advances Stage.

Skill authority zoning is explicit:
```text
Lv6 = current frozen combat authority
Lv11/Lv16/Lv21 = legacy parity diagnostic inputs
Lv26 = user-approved structural semantics + provisional diagnostic coefficients
Lv31 = user-approved structural direction + P4D2 provisional diagnostic centers
```
The runner does not convert Lv26/Lv31 diagnostic numbers into production authority.

Local split-runner smoke with seeds `101/211/307` passed syntax, deterministic replay, pair isolation, continuity, no enemy carry and no transient leakage. However the local recipe file was a semantic YAML reconstruction/redump, not the exact canonical bytes, so that run is engineering smoke only and no balance conclusion is adopted from it.

---

# Exact next execution groups

After exact canonical-source admission passes, inspect in order:
```text
A Stage5 Lv6 OFF/ON
B Stage18 Lv16 OFF/ON
C Stage20->23 sequential
D Stage39->45 sequential, Lv31 before 41/43/45
E Stage46->50 sequential, Lv31 active
```

Required output dimensions stay separate:
```text
authored/effective entity count
peak active
4s/6s density
frontline block time
target reorder
backline exposure
spawn-to-first-contact
removal throughput
control value
wall damage/reserve
root timing actions
stage settled time
failure classification
```

Tank objective protection must be interpreted separately from kill output.

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
- encounter family can rotate class advantage;
- one late class ranking is not universal balance evidence;
- `SURVIVAL != CLEAR`;
- Tank kill parity is not required;
- no flat shop->EXP correction;
- final EXP semantics route to P10R.

---

# Current work boundary

Next bounded work:
```text
EXECUTE_DEDICATED_T1_TRANSITION_SLICE_MICROSIM_AGAINST_EXACT_CANONICAL_SOURCE
```

Balance interpretation is forbidden until runner admission passes on the exact canonical inputs.

Still not authorized/frozen:
- all-50 exact recipe freeze;
- monster/shop/EXP/P×P numerical freeze;
- class buffs/nerfs;
- Tank damage normalization;
- boss adoption;
- production gameplay changes.
