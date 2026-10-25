# Timing Defense — Project Status

Updated: 2026-10-25 KST

## Production / harness
- production branch `timing-defense-cloudflare-do-poc`
- verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- calibration harness `timing-defense-skilled-v2-harness-v01`
- verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- production gameplay/numerical changes remain unauthorized.

## Canonical authority chain
Live remote always wins.

Current key chain:
- P6 closure: `156_P6_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`;
- four-Tier adoption: `158_INITIAL_FOUR_TIER_CAMPAIGN_AND_MONSTER_AVAILABILITY_APPROVED_CONTRACT_V0_1.md`;
- approved lower-layer constraints/correction: `160_FOUR_TIER_AUTHORING_CONSTRAINT_APPROVED_WITH_T1_BASELINE_CORRECTION_V0_1.md`;
- T1 Stage1-50 signature skeleton: `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`;
- static skeleton audit: `162_T1_STAGE_SIGNATURE_STATIC_CONSISTENCY_AUDIT_V0_1.md`;
- representative-slice preflight/materialization: `163` / `164`;
- micro-sim contract/adapter: `165` / `166`;
- exact-source baseline result: `167_T1_TRANSITION_SLICE_EXACT_SOURCE_MICROSIM_RESULT_V0_1.md`;
- v0.2 pressure/Lv31-absence/duration result: `168_T1_PRESSURE_SHAPE_V0_2_LV31_ABSENCE_AND_DURATION_SENSITIVITY_RESULT_V0_1.md`;
- Stage49-50 class-rotation/sustain result: `169_T1_STAGE49_50_CLASS_ROTATION_AND_SUSTAIN_DIAGNOSTIC_RESULT_V0_1.md`;
- compact Stage49-50 summary: `legacy-game-structure/data/t1_stage49_50_class_rotation_diagnostic_center_summary_v0_1.json`;
- active plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_47.yaml`.

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
pressure duration lever = SUPPORTED
uniform late-pulse repetition = CLASS-SKEWED / NOT ADOPTED
Stage49-50 class-rotation diagnostic = PASS_WITH_WATCH / DIAGNOSTIC CENTER SELECTED
DIAGNOSTIC CENTER = STAGGER_1800
objective-pressure rotation = STILL SKEWED TOWARD TANK
CURRENT = STAGE49-50 AUTHORING-CANDIDATE MATERIALIZATION + STATIC PREFLIGHT
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

# T1 structural/static authority

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

# Runner fidelity authority

The first exact-source execution exposed a false PASS because Stage-local wall shield/Aftershock was incorrectly allowed to delay `STAGE_SETTLED`.

Correct settlement ordering:
```text
authored spawns complete
+ zero live Stage-owned enemy
+ delayed combat-event queue drained
=> STAGE_SETTLED
=> Stage-local passive temporary residue clears
```

Minimal bridge:
`tools/run_t1_transition_slice_microsim_settlement_fix_v0_1.py`

Exact-source admission after correction remains PASS for:
- recipe identity;
- settlement/terminal result;
- no enemy carry;
- no transient leakage;
- persistent state continuity;
- deterministic replay;
- paired isolation;
- explicit skill-state trace.

During Stage49-50 diagnosis a second fidelity issue was found in Mage Lv31 staged-collapse semantics. The diagnostic bridge restores inherited Y radius and full-package hit exclusion. This is a semantic fidelity correction, not a production numerical freeze.

Archer Lv31 uses a diagnostic width bridge `yTolerance=0.20`; exact width remains unfrozen.

---

# v0.2 / duration result — doc168

v0.2 preserves Stage5 / Stage18 / Stage41 and all current monster/class/shop/EXP scalars.

Key result:
```text
Stage46-50 Lv31 ON: 15/15 clear, zero wall damage
Stage46-50 Lv31 OFF: 15/15 clear, zero wall damage
V02_STAGE46_50_MASTERY_GATE = NOT PRESENT
```

Legal pressure-duration repetition proved that duration can create OFF>ON mastery separation without scalar inflation, but uniform repetition over-punished Tank/Rogue and under-exposed Archer/Mage.

Therefore:
```text
PRESSURE_DURATION_IS_A_REAL_MASTERY_GATE_LEVER = SUPPORTED
UNIFORM_REPETITION = CLASS_SKEWED_NOT_ADOPTED
SCALAR_INCREASE_REQUIRED = NOT SHOWN
```

---

# Stage49-50 class-rotation diagnostic — doc169

Exact green evidence:
```text
run      40153142570
artifact 12583341810
head     5eb71a861b1226887a8ec09dce98641c0dfff817
artifact sha256 ab31640122bd1d00179d5af62104368cb46ad4e5d4137fb8922d561ebbfcacf5
seeds    101,211,307,409,503
fidelityErrors = []
```

Diagnostic grammar:
```text
Stage49 = DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE
Stage50 = DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE -> LINE_REPRISE
CLUSTER = BRUTE / GRUNT / BRUTE / GRUNT / BRUTE / GRUNT
```

Compared:
```text
STAGGER_1800 = 0/360/720/1080/1440/1800 ms
SUSTAIN_3000 = 0/600/1200/1800/2400/3000 ms
```

Both static PASS:
```text
Stage49 max4s = 6
Stage50 max4s = 6
Y spread = 0.18..0.82
```

`STAGGER_1800` role-facing Lv31 OFF->ON direction:
```text
Knight +43.03% faster
Rogue  +30.07% faster
Tank   +27.37% faster + 3 unresolved reduced
Archer +1.72% faster
Mage   +9.42% faster
```

Tank objective protection:
```text
OFF wall damage 1358
ON  wall damage 164
reduction 1194
```

Interpretation:
```text
ROLE_ROTATION_SIGNAL = IMPROVED
OBJECTIVE_PRESSURE_ROTATION = STILL_SKEWED_TOWARD_TANK
DIAGNOSTIC_CENTER = STAGGER_1800
AUTHORING_ADOPTION = NOT YET
NUMERICAL_FREEZE = NO
```

`STAGGER_1800` is preferred over `SUSTAIN_3000` because it achieves the same qualitative five-class role direction with a smaller chronology/cadence change; Mage signal is also slightly stronger (9.42% vs 8.96%).

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
T1_STAGE49_50_OBJECTIVE_PRESSURE_ROTATION_WATCH
```

The new watch is concrete: current exact Stage49-50 sample still produces material wall pressure only for Tank. Do not interpret it as a demand for equal wall damage across classes.

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
MATERIALIZE_STAGE49_50_ONLY_AUTHORING_CANDIDATE_AND_RUN_STATIC_PREFLIGHT
```

Use the `STAGGER_1800` diagnostic center as input, not as frozen content.

Must preserve:
```text
Stage5
Stage18
Stage41
monster HP/speed/wall damage
class coefficients
shop/EXP/P×P probabilities
right-edge spawn
4s density <= 8
```

Static preflight must check:
- exact source/schema identity;
- only Stage49/50 changed from v0.2;
- T1 monster vocabulary legality;
- authored count/density;
- Y spread/right-edge entry;
- grammar order/phase separation;
- T1 skeleton pressure/complexity consistency;
- no accidental numerical freeze.

Still not authorized/frozen:
- full 50-Stage exact recipe freeze;
- monster/class/shop/EXP/P×P numerical freeze;
- class buffs/nerfs;
- Tank damage normalization;
- boss adoption;
- production gameplay changes.
