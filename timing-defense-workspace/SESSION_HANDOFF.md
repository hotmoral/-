# Timing Defense — Session Handoff

Updated: 2026-10-24 KST

## 0. Recovery rule — mandatory
Always fetch live remote first. Never reconstruct current state from chat, memory or copied SHA. Live GitHub canonical state wins.

Do not make the user re-explain project state, dependency order or reasoning method.

## 1. Mandatory read/check order
1. live `timing-defense-workspace` HEAD;
2. `PROJECT_STATUS.md`;
3. `NEXT_WORK.md`;
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_44.yaml`;
5. `legacy-game-structure/156_P6_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`;
6. `legacy-game-structure/158_INITIAL_FOUR_TIER_CAMPAIGN_AND_MONSTER_AVAILABILITY_APPROVED_CONTRACT_V0_1.md`;
7. `legacy-game-structure/160_FOUR_TIER_AUTHORING_CONSTRAINT_APPROVED_WITH_T1_BASELINE_CORRECTION_V0_1.md`;
8. `legacy-game-structure/161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`;
9. `legacy-game-structure/163_T1_REPRESENTATIVE_TRANSITION_SLICE_PREFLIGHT_V0_1.md`;
10. `legacy-game-structure/164_T1_REPRESENTATIVE_TRANSITION_SLICE_RECIPE_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`;
11. `legacy-game-structure/165_T1_REPRESENTATIVE_TRANSITION_SLICE_MICROSIM_CONTRACT_V0_1.md`;
12. `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`;
13. current production/harness heads;
14. only then older implementation evidence needed by the adapter.

Methodology detail is in `138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md` and `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`; reopen them only when needed.

Do not reread or rerun everything by default. Reopen closed work only for source change, new contradictory evidence, runtime/source mismatch, exact-byte need, or a watch becoming material.

---

# 2. Mandatory cognition / review method

At every meaningful step inspect:
```text
upstream authority
-> current local decision
-> downstream consequences
-> cross-stage / cross-system consistency
-> cheaper alternative explanation
-> scope needed to resolve actual uncertainty
```

Root-cause order:
```text
source/simulator fidelity
-> lifecycle/state
-> encounter composition / geometry / chronology
-> class/package semantics
-> shop/feedback
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
-> wider exact recipe authoring only after evidence
```

Operating philosophy:
```text
progressive deepening / iterative convergence
not pure waterfall
not tune-everything-at-once
```

The user explicitly requires careful multi-perspective consistency checking because it is cheaper than late rework, while also forbidding unnecessary repetition and scope inflation.

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
Lower-layer Tier/authoring constraints = USER APPROVED WITH MINIMAL T1 BASELINE CORRECTION
T1 Stage1-50 signature skeleton = STATIC CANDIDATE PASS_WITH_WATCHES
Representative transition slice preflight = COMPLETE
Representative transition recipes = MATERIALIZED / STATIC PASS
Micro-sim execution contract = COMPLETE
Dedicated transition-slice runner = NOT STARTED
CURRENT = T1 TRANSITION SLICE MICROSIM RUNNER IMPLEMENTATION
full exact T1 50-Stage recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# 4. Four-Tier campaign authority

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

Five-Tier split is inactive fallback only if concrete later evidence shows T4 SUPPORTER/SIEGER learning/readability/role-expression cannot be preserved.

---

# 5. Important T1 correction — do not lose

Historical candidate contradiction:
```text
GRUNT first mixed 4-6
RUNNER first mixed 8-12
```
With the approved T1 roster, no other monster exists for a legal GRUNT mix before RUNNER is mixed.

Canonical correction in doc160:
```text
GRUNT first mixed = 8-12
```
Skeleton uses Stage8.

Do not solve by introducing/mixing RUNNER early or pulling BRUTE forward.

Stage1-4 E01 repetition is an explicit onboarding exception because only GRUNT is taught/readable; formation/cadence signatures rotate. Normal archetype repetition guard applies after RUNNER teach.

---

# 6. T1 signature skeleton static result

Source `161`, audit `162`.

```text
verdict = PASS_WITH_WATCHES
structural FAIL = 0
pressure presence = BASELINE22 / FLOOD8 / RUSH16 / BULWARK16
complexity = C0 8 / C1 25 / C2 15 / C3 2 / C4 0
rolling 10-Stage class opportunity = 41/41 PASS
```

This is structural starvation/readability evidence, not equal class clear-rate evidence.

Stage20/40 reward boundaries do not coincide with mandatory complexity spikes.
Stage41-45 is a controlled Lv31 acquisition runway with no new ordinary mechanic.
Stage46-49 is post-Lv31 mastery; Stage50 is learned-vocabulary synthesis.

---

# 7. Representative recipe materialization — new exact handoff point

Data:
`legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`

Static analyzer:
`tools/analyze_t1_transition_slice_recipes_v0_1.py`

Static report:
`164_T1_REPRESENTATIVE_TRANSITION_SLICE_RECIPE_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`

Materialized Stages:
```text
5
18
20 21 22 23
39 40 41 42 43 44 45
46 47 48 49 50
```

Static result:
```text
RESULT=PASS errors=0 warnings=0
max authored 4-second density = 8
inherited NORMAL upper bound = 8
no recipe enters 9-10 WATCH
Stage40 max4s = 6
Stage41 max4s = 3
```

The Stage40->41 drop proves the relief intent is represented in authored spawn density. It does not prove dynamic ease for every class.

No SPLITTER exists in T1, so effective entity count equals authored count for this static density check.

---

# 8. Micro-sim runner fidelity conclusion

Contract:
`165_T1_REPRESENTATIVE_TRANSITION_SLICE_MICROSIM_CONTRACT_V0_1.md`

Old `simulate_class_aware_layer_a.py` is not admissible as-is for sequential Stage20-23 / 39-45 / 46-50 because it resets isolated recipe state and does not provide the required Lv16/Lv31 execution surface.

Later P5/P6 runners are valid references for lifecycle, `STAGE_SETTLED`, class packages and deterministic tracing, but their historical encounter fixtures cannot substitute for the new T1 YAML.

Therefore the next correct implementation is a small dedicated adapter that consumes the exact new T1 recipe YAML and reuses approved lifecycle/class/skill semantics.

Admission gates before balance interpretation:
```text
exact recipe identity
STAGE_SETTLED
no arbitrary timer deletion
no enemy carry
no transient leakage
wall deficit persists
combo persists
charge persists
deterministic paired substreams
explicit skill-state trace
paired OFF/ON differs only by tested skill
```

Any failure is a runner/lifecycle fidelity failure first, not a balance failure.

---

# 9. Required execution groups after adapter admission

```text
A Stage5 RUNNER teach × Lv6 OFF/ON
B Stage18 BRUTE first mixed × Lv16 OFF/ON
C Stage20->23 sequential
D Stage39->45 sequential with Lv31 activation before 41 / 43 / 45
E Stage46->50 sequential with Lv31 active
```

Required metrics include:
```text
authoredSpawnCount
effectiveEntityCount
peakActive
max4sDensity
max6sDensity
frontlineBlockTime
targetReorderCount
backlineExposure when relevant
spawnToFirstContact
removalThroughput
controlValue
wallDamage / wallReserve
rootTimingActionCount
stageSettledTime
failureClassification
per-class directional opportunity / weakness
```

For Tank, assess objective protection from control/defense separately from kills.

---

# 10. T1 active watches

```text
T1_RUNNER_LV6_PEDAGOGIC_COLLISION_WATCH
T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH
T1_RUNNER_HIGH_PRESSURE_LV16_TAIL_WATCH
```

Carried system watches:
```text
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
T4_SUPPORTER_SIEGER_LEARNING_DENSITY_WATCH
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
```

Do not proliferate watches without concrete evidence.

---

# 11. Binding P6 / interpretation rules

- encounter family can materially rotate class advantage;
- one late class ranking is not universal balance evidence;
- Tank is control/defense/objective-protection specialist and kill parity is not required;
- shop ATK can reduce same-stage timing/EXP opportunity but increase total opportunity by preventing failure;
- pure per-root-action provisional EXP still creates class progression divergence pressure;
- fresh-forward exact magnitude is not production authority;
- final EXP semantics remain OPEN and route to P10R;
- no flat shop->EXP multiplier;
- `SURVIVAL != CLEAR`.

Failure classification order:
```text
runner/source fidelity
-> lifecycle/state
-> encounter geometry / chronology
-> class/skill interaction
-> shop/EXP if actually coupled
-> scalar sensitivity last
```

---

# 12. Approval / authority boundary

Autonomous diagnostic work may:
- implement the dedicated adapter under doc165;
- add instrumentation/validators;
- run bounded fidelity/causal checks;
- classify failures;
- correct diagnostic assumptions without changing gameplay semantics.

Explicit user approval is still required before adopting:
- full exact T1 50-Stage recipe set;
- class buff/nerf;
- monster numerical freeze;
- shop numerical freeze;
- EXP rule change;
- P×P/judgment probability change;
- Tank damage normalization;
- new monster or boss gameplay adoption;
- production gameplay changes;
- material methodology/phase scope changes.

---

# 13. Branch checkpoints

Planning/canonical:
- `timing-defense-workspace`
- always fetch live HEAD.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- unauthorized to change.

Harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

P6-B2 fresh-forward temp:
- `timing-defense-workspace-temp-p6-b2-fresh-forward`
- last known final head `5093a151142090d58c0e1d26f52cdbee43653542`
- evidence only; do not promote automatically.

---

# 14. Session-close quality gate
Before ending a work group:
1. fetch live canonical HEAD;
2. verify production/harness unchanged unless explicitly authorized;
3. separate evidence, candidate, approved authority and numerical freeze status;
4. sync `PROJECT_STATUS.md`, `NEXT_WORK.md`, `SESSION_HANDOFF.md`, active dependency YAML and relevant result/preflight docs;
5. record any concrete contradiction and its minimal resolution;
6. do not leave the next session dependent on chat explanation;
7. stop before a user-approval gate that would change gameplay/content authority.
