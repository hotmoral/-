# Timing Defense — Session Handoff

Updated: 2026-10-24 KST

## 0. Recovery rule — mandatory
Always fetch live remote first. Never reconstruct current state from chat, memory or copied SHA. Live GitHub canonical state wins.

Do not make the user re-explain project state, dependency order or reasoning method.

## 1. Mandatory recovery order
1. live `timing-defense-workspace` HEAD;
2. `PROJECT_STATUS.md`;
3. `NEXT_WORK.md`;
4. active `legacy-game-structure/data/system_dependency_calibration_order_v0_45.yaml`;
5. `legacy-game-structure/166_T1_TRANSITION_SLICE_MICROSIM_ADAPTER_IMPLEMENTATION_AND_ADMISSION_PREFLIGHT_V0_1.md`;
6. `legacy-game-structure/165_T1_REPRESENTATIVE_TRANSITION_SLICE_MICROSIM_CONTRACT_V0_1.md`;
7. exact recipe data `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`;
8. runner `tools/run_t1_transition_slice_microsim_v0_1.py` and support modules only as needed;
9. `164` static recipe report and `163` slice preflight;
10. `161/162` T1 skeleton/static audit when broader context is needed;
11. `160` lower-layer approved constraints/correction;
12. P6 closure `156` and active watches;
13. production/harness live heads;
14. older P3/P4/P5 implementation evidence only when a specific runner-semantic question requires it.

Methodology detail remains in `138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md` and `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`. Do not reread them by default.

Reopen closed work only for source change, contradictory evidence, runtime/source mismatch, exact-byte need, or a watch becoming material.

---

# 2. Mandatory working method

At every meaningful step inspect:
```text
upstream authority
-> current local decision
-> downstream consequences
-> cross-stage / cross-system consistency
-> cheaper alternative explanation
-> minimum scope needed to resolve the real uncertainty
```

Root-cause order:
```text
source/simulator fidelity
-> lifecycle/state
-> encounter composition / geometry / chronology
-> class/package semantics
-> shop/feedback only if coupled
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

Use progressive deepening / iterative convergence. Avoid both waterfall rigidity and tune-everything-at-once behavior.

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
T1 lower-layer constraints = USER APPROVED WITH BASELINE CORRECTION
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
Representative transition recipes = MATERIALIZED / STATIC PASS
Micro-sim contract = COMPLETE
Dedicated transition runner = IMPLEMENTED
Local semantic smoke = PASS / ENGINEERING ONLY
Exact canonical-source execution = PENDING
CURRENT = EXACT CANONICAL-SOURCE T1 TRANSITION MICROSIM EXECUTION
full exact T1 50-Stage recipe freeze = DEFERRED
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

Important resolved contradiction:
```text
obsolete: GRUNT first mixed Stage4-6
canonical: GRUNT first mixed Stage8-12
```
Reason: with the approved T1 roster there is no legal second monster before RUNNER's own mixed window. Skeleton chooses Stage8. Do not pull RUNNER or BRUTE earlier to satisfy the obsolete window.

Stage1-4 E01 repetition remains a bounded onboarding exception; exact formation/cadence signatures still rotate.

---

# 5. T1 structural/static state

`161/162` result:
```text
structural FAIL = 0
PASS_WITH_WATCHES
pressure = BASELINE22 / FLOOD8 / RUSH16 / BULWARK16
complexity = C0 8 / C1 25 / C2 15 / C3 2 / C4 0
rolling 10-Stage class opportunity = 41/41 PASS
```

Representative recipe materialization (`164`):
```text
Stages = 5, 18, 20-23, 39-45, 46-50
static RESULT = PASS
errors = 0
warnings = 0
highest authored 4s density = 8
Stage40 max4s = 6
Stage41 max4s = 3
```

The Stage40->41 density drop confirms authored Lv31 relief direction statically. It does not prove dynamic ease or balance.

---

# 6. Dedicated micro-sim runner — implemented

Canonical assets:
```text
tools/run_t1_transition_slice_microsim_v0_1.py
tools/t1_transition_microsim_core_v0_1.py
tools/t1_transition_microsim_skills_v0_1.py
tools/t1_transition_microsim_engine_v0_1.py
```

The runner directly consumes the current recipe YAML and emits source/per-recipe SHA256 evidence. Recipes are not embedded/reconstructed in code.

Implementation layers are split intentionally:
- core = deterministic RNG, source/static gates, target helpers, damage/N3/event primitives;
- skills = class-specific Lv6-31 diagnostic semantics;
- engine = root timing action, Stage lifecycle, movement, wall/control attribution, `STAGE_SETTLED`;
- entry runner = paired/sequential experiment matrix, replay checks, admission/result output.

### Admission invariants
Before balance interpretation require:
```text
exact source identity evidence
STAGE_SETTLED or terminal wall failure
no timer deletion
no enemy carry at settled boundary
no Stage-local transient leakage
wall deficit continuity
combo continuity
charge continuity
judgment/proc RNG continuity
deterministic replay
paired OFF/ON isolation
explicit per-Stage skill state
```

Safety cap behavior:
```text
unsettled at cap -> RunnerFidelityError
never delete enemies
never advance Stage anyway
```

### Skill authority zoning
```text
Lv6 = current frozen combat authority
Lv11/Lv16/Lv21 = recovered legacy parity inputs for diagnostics
Lv26 = user-approved structural contract; coefficients remain provisional diagnostic values
Lv31 = user-approved structural direction; P4D2 centers remain provisional diagnostic values
N3 = frozen milestone semantics
```

Do not interpret the runner as a production re-freeze of Lv11-31.

---

# 7. Local implementation smoke — evidence boundary

The committed split architecture was syntax-compiled and locally executed against semantic reconstructions of the current fixtures with seeds:
```text
101 / 211 / 307
```

Engineering result:
```text
static/group admission = PASS
deterministic replay = PASS
paired isolation = PASS
persistent continuity = PASS
no enemy carry = PASS
no transient leakage = PASS
safety-cap failure = 0
```

However the locally materialized recipe YAML was a semantic redump, not the exact canonical source bytes.
Therefore:
```text
LOCAL_SEMANTIC_SMOKE != EXACT_CANONICAL_DYNAMIC_EVIDENCE
```

A local observation of zero wall contact in that smoke is **not** yet balance evidence and must not be used to modify recipes or class/monster scalars.

---

# 8. Exact next work — no user clarification needed

Run the committed runner against an exact current canonical checkout/source:

```text
python tools/run_t1_transition_slice_microsim_v0_1.py \
  --recipes legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml \
  --p3-fixture legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json \
  --p4d2-base legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json \
  --p4d2-temporal legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json \
  --seeds 101,211,307 \
  --json-out <evidence-path>
```

Record live canonical HEAD, recipe source SHA256 emitted by runner, runner identity, admission result and evidence digest.

If admission FAILS: stop and repair fidelity only.

If admission PASSES: inspect exactly in this order:
```text
A Stage5 Lv6 OFF/ON
B Stage18 Lv16 OFF/ON
C Stage20->23 sequential
D Stage39->45 sequential with Lv31 before 41/43/45
E Stage46->50 sequential with Lv31 active
```

Do not skip directly to Stage46-50 because later results depend on proving runner/lifecycle behavior first.

---

# 9. Required dynamic measurements

Keep dimensions separate:
```text
authored/effective entity count
peak active
4s/6s density
frontline block time
target reorder
backline exposure
spawn-to-first-contact
removal throughput
control value components
wall damage/reserve
root timing actions
stage settled time
combat outcome
failure classification
per-class opportunity/weakness observations
```

Tank control/protection telemetry includes knockback distance, Aftershock movement prevented, Iron Wall damage prevented and shield absorption. Do not use Tank kill parity as a success criterion.

---

# 10. Active watches

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

# 11. Binding P6 / interpretation rules

- encounter family can materially rotate class advantage;
- one late class ranking is not universal balance evidence;
- Tank is control/defense/objective-protection specialist; kill parity is not required;
- `SURVIVAL != CLEAR`;
- shop ATK -> EXP feedback is bidirectional/outcome-conditioned;
- no flat shop->EXP multiplier;
- pure per-root-action provisional EXP still has class progression divergence pressure;
- fresh-forward exact magnitude is not production authority;
- final EXP semantics remain OPEN and route to P10R.

---

# 12. Authority / approval boundary

Autonomous diagnostic work may:
- execute the exact-source runner;
- record deterministic evidence;
- classify failures;
- add narrow instrumentation/validators;
- repair runner fidelity without changing gameplay semantics.

Explicit user approval is still required before adopting:
- full exact T1 Stage1-50 recipe set;
- class buff/nerf;
- Tank damage normalization;
- monster/shop numerical freeze;
- EXP rule change;
- P×P/judgment probability change;
- new monster/boss gameplay adoption;
- production gameplay changes;
- material methodology/phase scope change.

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
Before ending a meaningful work group:
1. fetch live canonical HEAD;
2. verify production/harness unchanged unless explicitly authorized;
3. separate engineering smoke, dynamic evidence, candidate design, approved authority and numerical freeze;
4. sync `PROJECT_STATUS.md`, `NEXT_WORK.md`, `SESSION_HANDOFF.md`, active dependency YAML and result/preflight docs;
5. record concrete contradictions/minimal fixes;
6. do not leave next session dependent on chat;
7. stop before a gameplay/content adoption gate requiring user approval.
