# Timing Defense — Next Work Boundary

Updated: 2026-10-24 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_44.yaml`;
5. read `160_FOUR_TIER_AUTHORING_CONSTRAINT_APPROVED_WITH_T1_BASELINE_CORRECTION_V0_1.md`;
6. read `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`;
7. read `163_T1_REPRESENTATIVE_TRANSITION_SLICE_PREFLIGHT_V0_1.md`;
8. read `164_T1_REPRESENTATIVE_TRANSITION_SLICE_RECIPE_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`;
9. read `165_T1_REPRESENTATIVE_TRANSITION_SLICE_MICROSIM_CONTRACT_V0_1.md`;
10. inspect exact recipe data `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`;
11. preserve P6 closure `156` and active watches;
12. verify production/harness heads;
13. open older implementation evidence only when needed for the adapter.

Do not rerun closed P6, Model A Layer-A0, or the full static T1 audit without a concrete trigger.

---

# Current phase

```text
P6 = USER_APPROVED STRUCTURAL CLOSED WITH WATCHES
Initial campaign = 4 Tier / USER APPROVED
Monster availability ladder = USER APPROVED
T1 roster = G/R/B / USER APPROVED
Lower-layer authoring constraints = USER APPROVED WITH T1 BASELINE CORRECTION
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
Representative slice preflight = COMPLETE
Representative recipe materialization = STATIC PASS
Micro-sim contract = COMPLETE
CURRENT = IMPLEMENT DEDICATED T1 TRANSITION SLICE MICROSIM ADAPTER
full 50-Stage exact recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Static evidence already established

Recipe source:
`legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`

Result:
```text
PASS errors=0 warnings=0
max authored 4s density = 8
Stage40 max4s = 6
Stage41 max4s = 3
```

Do not reinterpret this static PASS as dynamic clearability or balance proof.

---

# Next bounded implementation

Implement a dedicated adapter/runner for exactly these groups:

```text
A. Stage5 RUNNER teach × Lv6 OFF/ON
B. Stage18 BRUTE first mixed × Lv16 OFF/ON
C. Stage20->23 sequential Star Gate A + first high-pressure ramp
D. Stage39->45 sequential 2★ gate + Lv31 activation before Stage41/43/45
E. Stage46->50 sequential post-Lv31 mastery/final with Lv31 active
```

The adapter must read the exact current recipe YAML. Do not reconstruct recipes in code and do not substitute old late-stage fixtures.

---

# Runner admission gates

Before interpreting any balance result, prove:

```text
exact recipe identity
STAGE_SETTLED boundary
no timer deletion
no enemy carry
no transient leakage
wall deficit persists
combo persists
charge persists
deterministic RNG/player-model substreams
explicit per-Stage skill-state trace
paired OFF/ON differs only in tested skill state
```

If a gate fails, classify the result as runner/lifecycle fidelity failure and stop balance interpretation.

---

# Implementation reuse rule

Do not use `simulate_class_aware_layer_a.py` as-is for sequential slices; it resets state and lacks the required Lv16/Lv31 surface.

Later P5/P6 runners are reference implementations for:
- persistent lifecycle semantics;
- `STAGE_SETTLED`;
- class packages;
- deterministic traces;
- wall/objective attribution.

They may be adapted, but historical encounter fixtures must not leak into the T1 recipe set.

Reuse existing approved class/skill semantics; do not independently recreate them with changed behavior.

---

# Required output metrics

At minimum:
```text
authoredSpawnCount
effectiveEntityCount
peakActive
max4sDensity
max6sDensity
frontlineBlockTime
targetReorderCount
backlineExposure where relevant
spawnToFirstContact
removalThroughput
controlValue
wallDamage
wallReserve
rootTimingActionCount
stageSettledTime
failureClassification
per-class directional opportunity/weakness observations
```

For Tank, separately attribute objective-protection value from control/defense. Do not use kill parity as the success criterion.

---

# Result interpretation order

```text
runner/source fidelity
-> lifecycle/state
-> composition / geometry / chronology
-> skill/class-package interaction
-> shop/EXP only if actually coupled
-> exact scalar last
```

Do not collapse results to one fairness score.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
NO FULL-50 EXACT RECIPE AUTHORING BEFORE REPRESENTATIVE SLICE EVIDENCE
NO CLASS BUFF/NERF FROM ONE SLICE
SURVIVAL != CLEAR
TANK KILL PARITY NOT REQUIRED
NO FLAT SHOP->EXP MULTIPLIER
FINAL EXP ROUTING = P10R
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```

The adapter itself is diagnostic instrumentation and may be implemented autonomously under doc165. Any resulting gameplay/content authority change still requires the appropriate user decision gate.
