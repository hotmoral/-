# 166 — T1 Transition Slice Micro-Sim Adapter Implementation & Admission Preflight v0.1

Status: **RUNNER IMPLEMENTED / LOCAL SEMANTIC SMOKE PASS / EXACT CANONICAL-SOURCE EXECUTION NEXT / NO BALANCE INTERPRETATION**

## 1. Purpose

Implement the dedicated runner required by `165_T1_REPRESENTATIVE_TRANSITION_SLICE_MICROSIM_CONTRACT_V0_1.md` without changing production gameplay, production balance values, or the calibration harness.

The runner exists only to execute the bounded T1 representative transition recipes already materialized in `164`.

It does **not** authorize full Stage1-50 exact authoring or any production numerical freeze.

---

## 2. Implemented assets

Entry point:

- `tools/run_t1_transition_slice_microsim_v0_1.py`

Separated implementation layers:

- `tools/t1_transition_microsim_core_v0_1.py`
- `tools/t1_transition_microsim_skills_v0_1.py`
- `tools/t1_transition_microsim_engine_v0_1.py`

The split is deliberate. It keeps source/identity utilities, class-skill semantics, Stage lifecycle execution, and experiment orchestration separable for fidelity review.

---

## 3. Exact input policy

The entry runner reads:

- `legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml`

and reports:

- recipe source SHA256;
- per-Stage recipe-object SHA256;
- recipe id/version;
- explicit per-Stage skill state.

Recipes are not reconstructed in code and old P4/P5 late-stage encounter fixtures are not substituted for the current T1 recipes.

P4D2 assets are used only for the already-existing bounded diagnostic monster / Lv31 numerical anchors required by the current contract.

---

## 4. Reused authority by layer

### Lifecycle / deterministic state

Reused from approved P1/P3 authority:

- wall deficit persistence;
- combo persistence;
- charge persistence;
- deterministic player-model state persistence;
- `STAGE_SETTLED` boundary;
- no enemy carry;
- no Stage-local transient leakage.

### Lv6–21

Uses the recovered exact legacy parity semantics recorded by `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`.

This remains diagnostic parity use, not a new production re-freeze.

### Lv26

Uses the user-approved structural semantics in `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`.

Roadmap coefficients remain provisional diagnostic values where the Lv26 contract says they are provisional.

### Lv31

Uses the user-approved structural direction in `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md` and existing P4D2 provisional diagnostic centers.

Those centers remain non-production values.

### N3

Uses the frozen N3 milestone budget/geometry isolation semantics.

---

## 5. Implemented admission gates

Before any balance interpretation, the runner checks or emits evidence for:

```text
static recipe/group contract
exact source identity evidence
STAGE_SETTLED or terminal wall failure
no enemy carry at settled boundary
no Stage-local transient leakage
wall/combo/charge deterministic continuity
continuous judgment/proc RNG state
paired OFF/ON initial-state identity
paired OFF/ON tested-milestone-only difference
explicit class + active milestone trace
deterministic replay equality
```

Safety timeout behavior is fail-closed:

```text
if a Stage cannot settle within the diagnostic safety cap
-> raise RUNNER fidelity failure
-> never delete enemies
-> never advance Stage anyway
```

Thus the safety cap cannot masquerade as Stage completion.

---

## 6. Implemented execution groups

```text
A Stage5  : Lv6 OFF / ON, identical recipe and deterministic starting state
B Stage18 : Lv16 OFF / ON, identical recipe and deterministic starting state
C Stage20 -> 23 : sequential persistent-state run
D Stage39 -> 45 : sequential, Lv31 activation before Stage41 / 43 / 45
E Stage46 -> 50 : sequential, Lv31 active throughout
```

Classes:

```text
Knight / Rogue / Tank / Archer / Mage
```

Default deterministic seeds:

```text
101 / 211 / 307
```

---

## 7. Metrics emitted

At least:

```text
authoredSpawnCount
effectiveEntityCount
peakActive
max4sDensity
max6sDensity
frontlineBlockTime
targetReorderCount
backlineExposure
spawnToFirstContact
damage / kills / killsByType
removalThroughput
controlValue components
wallDamage
wallReserve
rootTimingActionCount
stageSettledTime
procCrits
entry / exit persistent state
skill state
action trace + digest
combat outcome
invariant evidence
```

Tank control/protection telemetry is kept separate:

- realized knockback distance;
- Aftershock movement distance prevented;
- Iron Wall damage prevented;
- wall-shield absorption.

No kill-parity score is introduced.

---

## 8. Local implementation preflight

The split implementation was syntax-compiled and executed locally against a semantic reconstruction of the current canonical fixtures.

Three-seed smoke:

```text
seeds = 101 / 211 / 307
static/group admission = PASS
deterministic replay = PASS
paired isolation = PASS
persistent continuity = PASS
no enemy carry = PASS
no transient leakage = PASS
safety-cap failure = 0
```

The local smoke also executed all five classes and Groups A-E.

### Critical evidence boundary

This local run is **engineering smoke only**.

The locally materialized recipe file was a semantic YAML reconstruction/redump, not the exact byte-for-byte canonical repository file. Therefore:

```text
LOCAL_SEMANTIC_SMOKE != EXACT_CANONICAL_DYNAMIC_EVIDENCE
```

No combat/balance conclusion is authorized from the local smoke.

In particular, a local observation that these candidate slices produced no wall contact in that smoke must **not** yet be interpreted as proof that the canonical recipes are too easy. The next exact-source execution must first pass admission using the live canonical recipe bytes and current committed runner.

---

## 9. Exact next action

Run the committed runner against the exact live canonical inputs and record the resulting recipe-source SHA256 and admission result.

Required order:

```text
1. exact canonical source execution
2. runner admission PASS
3. only then inspect Group A
4. Group B
5. Group C
6. Group D
7. Group E
8. classify any failure using fidelity -> lifecycle -> chronology/geometry -> class interaction -> scalar last
```

If exact-source execution fails a fidelity gate, fix the runner before interpreting combat results.

---

## 10. Explicitly not frozen / not changed

Still not authorized or frozen:

- full T1 Stage1-50 exact recipe set;
- production monster numbers;
- shop values;
- EXP formula/reach;
- P×P probability model;
- class buffs/nerfs;
- Tank damage normalization;
- boss adoption;
- production gameplay implementation.

Production and the standalone SKILLED_V2 calibration harness were not modified by this implementation package.

---

## 11. Decision state

```text
runnerImplementation = COMPLETE
localSemanticSmoke = PASS
exactCanonicalSourceDynamicExecution = PENDING
balanceInterpretation = NOT_STARTED
fullT1ExactRecipeFreeze = DEFERRED
productionGameplayChange = UNAUTHORIZED
```
