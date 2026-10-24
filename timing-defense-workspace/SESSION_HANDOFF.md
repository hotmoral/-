# Timing Defense — Session Handoff

Updated: 2026-10-24 KST

## 0. Recovery rule — mandatory
Always fetch live remote first. Never reconstruct current state from chat, memory or copied SHA. Live GitHub canonical state wins.

Do not make the user re-explain project state, dependency order or review philosophy.

---

# 1. Mandatory recovery order

1. live `timing-defense-workspace` HEAD;
2. `PROJECT_STATUS.md`;
3. `NEXT_WORK.md`;
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_46.yaml`;
5. `legacy-game-structure/168_T1_PRESSURE_SHAPE_V0_2_LV31_ABSENCE_AND_DURATION_SENSITIVITY_RESULT_V0_1.md`;
6. `legacy-game-structure/data/t1_pressure_shape_v0_2_and_duration_sensitivity_summary_v0_1.json`;
7. v0.2 diagnostic recipe `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`;
8. exact baseline result `167_T1_TRANSITION_SLICE_EXACT_SOURCE_MICROSIM_RESULT_V0_1.md`;
9. runner contract/implementation `165` / `166` and settlement bridge `tools/run_t1_transition_slice_microsim_settlement_fix_v0_1.py`;
10. baseline recipe/static evidence `163-164`;
11. T1 skeleton/static authority `160-162` only when broader context is needed;
12. P6 closure `156` and active watches;
13. production/harness live heads;
14. older P3/P4/P5 evidence only for a concrete semantic question.

Do not rerun closed P6, full T1 skeleton audit or earlier baseline probes without a trigger.

---

# 2. Mandatory working method

At every meaningful step inspect:
```text
upstream authority
-> current local decision
-> downstream consequences
-> cross-stage / cross-system consistency
-> cheaper alternative explanation
-> minimum scope needed to resolve the actual uncertainty
```

Root-cause order:
```text
source/simulator fidelity
-> lifecycle/state
-> encounter composition / geometry / chronology
-> class/package semantics
-> shop/feedback only if actually coupled
-> exact scalar last
```

Campaign authoring order:
```text
Tier availability
-> monster vocabulary
-> encounter-family availability
-> class-opportunity envelope
-> Stage signature skeleton
-> bounded representative recipes
-> lifecycle-faithful representative execution
-> wider exact authoring only after representative evidence
```

Use progressive deepening / iterative convergence. Avoid both unnecessary repetition and scope inflation.

---

# 3. Current exact state

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
Initial campaign = 4 Tiers / USER APPROVED
Monster availability ladder = USER APPROVED
T1 ordinary roster = GRUNT/RUNNER/BRUTE / USER APPROVED
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
baseline representative recipes = STATIC PASS / EXACT-SOURCE EXECUTED
transition micro-sim runner = IMPLEMENTED / EXACT-SOURCE ADMISSION PASS
settlement ordering false-pass = FOUND / CORRECTED / SUPERSEDED
v0.2 pressure-shape candidate = DIAGNOSTIC ONLY / STATIC PASS / EXACT-SOURCE EXECUTED
Stage41 relief = RECONFIRMED
v0.2 Stage46-50 Lv31 absence = TOO SAFE
pressure duration lever = SUPPORTED
uniform late repetition = CLASS-SKEWED / NOT ADOPTED
CURRENT = STAGE49-50 CLASS-ROTATION PRESSURE-SHAPE DIAGNOSTIC
full exact T1 Stage1-50 recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# 4. Campaign authority that must not drift

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

Historical contradiction remains closed:
```text
obsolete GRUNT first mixed = Stage4-6
canonical GRUNT first mixed = Stage8-12
```
Skeleton uses Stage8. Do not solve by pulling RUNNER/BRUTE earlier.

Run lifecycle remains:
- Base HP deficit persists;
- combo persists;
- charge persists;
- Stage advances only at `STAGE_SETTLED`;
- enemy instances and Stage-local temporary state do not carry across the boundary;
- no midfield pop-in; right-edge spawn only.

---

# 5. T1 structural/static authority

`161/162`:
```text
structural FAIL = 0
PASS_WITH_WATCHES
pressure = BASELINE22 / FLOOD8 / RUSH16 / BULWARK16
complexity = C0 8 / C1 25 / C2 15 / C3 2 / C4 0
rolling 10-Stage class opportunity = 41/41 PASS
```

Baseline representative recipe `164`:
```text
Stages = 5, 18, 20-23, 39-45, 46-50
static PASS
errors = 0
warnings = 0
highest authored 4s density = 8
Stage40 max4s = 6
Stage41 max4s = 3
```

---

# 6. Runner implementation / fidelity correction

Canonical runner assets:
```text
tools/run_t1_transition_slice_microsim_v0_1.py
tools/t1_transition_microsim_core_v0_1.py
tools/t1_transition_microsim_skills_v0_1.py
tools/t1_transition_microsim_engine_v0_1.py
tools/run_t1_transition_slice_microsim_settlement_fix_v0_1.py
```

Important defect found by the first exact-source run:
- `stage_settled()` incorrectly waited for Stage-local wallShield/Aftershock timer expiry.
- This made Tank Lv16 ON Stage18 appear ~3 seconds longer than OFF despite unchanged removal chronology.

Correct classification:
```text
FALSE_PASS_SETTLEMENT_ORDERING
```

Corrected semantics:
```text
authored spawns complete
+ zero live Stage-owned enemy
+ delayed combat-event queue empty
=> STAGE_SETTLED
=> Stage-local passive temporary residue clears at boundary
```

Do not revert to the old ordering.

Exact-source admission after correction:
```text
exactRecipeIdentity = PASS
stageSettledOrTerminalFailure = PASS
noEnemyCarryAtSettledBoundary = PASS
noTransientLeakageAtSettledBoundary = PASS
persistentStateContinuity = PASS
deterministicReplay = PASS
pairedIsolation = PASS
explicitSkillStateTrace = PASS
```

Skill authority zoning:
```text
Lv6 = current frozen combat authority
Lv11/Lv16/Lv21 = legacy parity diagnostic inputs
Lv26 = user-approved structural semantics + provisional diagnostic coefficients
Lv31 = user-approved structural direction + P4D2 provisional diagnostic centers
N3 = frozen milestone semantics
```
These do not become production numerical authority through simulation.

---

# 7. Baseline exact dynamic result — doc167

Corrected baseline run:
```text
run 40074583842
job 120815112194
artifact 12552383686
head 61a4dc2fbef1bcf9bf6c48bee857bdbf2304d0d3
artifact SHA256 368d51ae76a45fd4b2fcbfb9e794246ace508e6a975b54a9f286a05e5fb36227
recipe SHA256 afd4c57e94ea797ab14954f67ecc576b202eeed4ca953162e0080892db1083a7
```

Main conclusions:
```text
Stage5 Lv6 collision = WATCH_NOT_FAIL
Stage18 Lv16 collision = MATERIAL_WATCH, especially Archer/Mage compression
Stage41 relief shape = SUPPORTED
Stage20-23 pressure = UNDERSHOOT
Stage39-45 pressure = UNDERSHOOT
Stage46-50 mastery pressure = CLEAR UNDERSHOOT
```

No class buff/nerf is authorized from these findings.

---

# 8. v0.2 pressure-shape candidate / exact result — doc168

Source:
`data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`

Exact SHA256:
`3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf`

Boundary:
- Stage5 unchanged;
- Stage18 unchanged;
- Stage41 unchanged;
- no monster/class/shop/EXP scalar changes;
- only representative pressure shape was deepened.

Static gate PASS:
```text
all representative max4s <= 8
Stage40 max4s 6
Stage41 max4s 3
```

Final comprehensive run:
```text
run 40075651830
job 120818295930
artifact 12553201879
head bd1959c73235255e9de8a103295d95aa260d69fd
artifact SHA256 a60523c6ed34d58e02aafe6fffffb8f997b2d4d28bf03d8b275c3847ae3da008
```

v0.2 dynamic conclusions:
- Stage20-23 gains only sparse pressure: 2/60 wall-positive rows / 246 total diagnostic damage;
- Stage39-45 remains wall-safe but Stage41 relief is clearly preserved;
- Stage46-50 Lv31 ON remains wall-safe;
- explicit Lv31 OFF/ON paired probe shows both sides 15/15 clear Stage46-50 with zero wall damage.

Therefore:
```text
V02_BASE_NOT_YET_MASTERY_GATE
```

---

# 9. Pressure-duration sensitivity

Naive repeated pulse spacing:
```text
6s / 8s / 10s = REJECTED BY authored4s DENSITY GUARD
```
No dynamic balance interpretation from rejected candidates.

Legal search:
```text
extra copies = 1 / 2 / 3
spacing = 11 / 12 / 14 / 16 seconds
all retained max4 <= 8
```

Representative sensitivity only:
```text
COPY2_SHIFT11000
OFF wall-positive 5/15
ON  wall-positive 4/15
OFF failures 1
ON  failures 0
OFF total wall damage 6184
ON  total wall damage 777
```

Meaning:
```text
PRESSURE_DURATION_IS_A_REAL_MASTERY_GATE_LEVER = SUPPORTED
SCALAR_INCREASE_REQUIRED = NOT SHOWN
```

But uniform repetition is **not adopted** because the pressure rotates poorly:
- Tank and Rogue take disproportionate Stage49-50 wall pressure;
- Archer/Mage remain too protected in many cases;
- this risks becoming generic throughput pressure rather than class-readable mastery pressure.

Do not promote any COPY/SHIFT candidate to authoring.

---

# 10. Exact next work

Next scope is intentionally narrow:
```text
Stage49-50 only
```

Build a bounded **distributed durable / split-axis pressure-shape candidate**.

Goals:
1. reduce uniform-repeat Tank/Rogue skew;
2. create spatial pressure that exposes limits of Archer strict-line and Mage local-density answers;
3. preserve Rogue durable-normal execution opportunity;
4. preserve Tank control/defense/objective-protection value;
5. preserve Knight generalist/frontline utility;
6. use only GRUNT/RUNNER/BRUTE;
7. right-edge spawn only;
8. authored 4s density <= 8;
9. alter composition/geometry/chronology before scalars.

Do not touch in this next unit:
```text
Stage5
Stage18
Stage41
monster HP/speed/wall damage
class coefficients
shop/EXP/P×P probabilities
```

Compare the candidate against:
- v0.2 base;
- duration-sensitivity envelope;
- paired Lv31 OFF/ON.

A useful candidate need not equalize classes. It should show broader pressure rotation without simply moving all damage from Tank/Rogue to another single class.

---

# 11. Active watches

```text
T1_RUNNER_LV6_PEDAGOGIC_COLLISION_WATCH
T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH
T1_RUNNER_HIGH_PRESSURE_LV16_TAIL_WATCH
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
T4_SUPPORTER_SIEGER_LEARNING_DENSITY_WATCH
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
```

Do not proliferate watches without a concrete new failure mode.

---

# 12. Approval boundary

Autonomous diagnostic work may:
- create/test Stage49-50 diagnostic shape candidates;
- add narrow instrumentation/validators;
- run exact-source deterministic comparisons;
- classify failures;
- repair diagnostic fidelity without changing gameplay semantics.

Explicit user approval remains required before adopting:
- full exact T1 Stage1-50 recipe set;
- class buff/nerf;
- Tank damage normalization;
- monster/shop/EXP/P×P numerical changes or freeze;
- new monster/boss gameplay adoption;
- production gameplay changes;
- material methodology/phase scope change.

---

# 13. Branch checkpoints

Planning/canonical:
- `timing-defense-workspace`
- always fetch live HEAD first.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- unauthorized to change.

Harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

P6-B2 temp:
- `timing-defense-workspace-temp-p6-b2-fresh-forward`
- last known `5093a151142090d58c0e1d26f52cdbee43653542`
- evidence only.

---

# 14. Session-close quality gate

Before ending a meaningful work group:
1. fetch live canonical HEAD;
2. verify production/harness unchanged unless explicitly authorized;
3. separate evidence / candidate / approved authority / numerical freeze;
4. sync status / next / handoff / active plan / relevant result docs;
5. record contradictions and minimal fixes;
6. leave no next-step dependency on chat memory;
7. stop before an adoption gate requiring user approval.
