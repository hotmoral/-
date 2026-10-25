# Timing Defense — T1 Wider Exact Authoring Wave A Plan & Static Preflight V0.1

Date: 2026-10-25 KST  
Status: **STATIC PREFLIGHT PASS / BOUNDED PLAN ONLY / NO NEW SPAWN RECIPE MATERIALIZATION / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`
- `162_T1_STAGE1_50_SIGNATURE_SKELETON_STATIC_AUDIT_V0_1.md`
- `174_T1_STAGE49_50_STRUCTURAL_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`
- `data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`
- `data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml`

Plan:
`data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`

## 1. Why this is bounded

The next step does not fill all missing T1 Stages. It selects only transition/bridge anchors where exact spawn authoring is most likely to expose a contradiction early and cheaply.

New target stages:

```text
1, 4, 8,
15, 19,
24, 25, 29, 30, 31,
33, 37, 38
```

Total new targets: `13`.

Context-only anchors:

```text
5, 18, 20, 39, 40, 41, 49, 50
```

These context stages are not modified in Wave A.

## 2. Four authoring slices

### A1 — onboarding to first mix
```text
target = 1,4,8
context = 5
```
Purpose: initial baseline, first authored wave boundary, first G+R mix around the preserved RUNNER teach.

### A2 — BRUTE teach to first reorder
```text
target = 15,19
context = 18,20
```
Purpose: connect BRUTE teach and preserved first mixed Stage18 into the first B+R target-order contrast and Star Gate A.

### A3 — Lv21 buffer to Checkpoint B / soft-wall entry
```text
target = 24,25,29,30,31
```
Purpose: preserve the Lv21 reward buffer, then test first bounded F08 synthesis, Checkpoint B, and the initial soft-wall durable-pressure entry.

### A4 — pre-gate pressure bridge
```text
target = 33,37,38
context = 39,40
```
Purpose: connect Mage density pressure and bounded split-axis tempo into the already-authored Stage39 peak and Stage40 gate.

## 3. Exact-source preflight history

Initial run:
```text
run 40189197117
head 931ec15c0852eda17322b3d140f11456d7da6d6f
result = FAIL
```

The workflow initially skipped failure artifact upload. That observability defect was corrected without changing plan semantics.

Second run:
```text
run 40189239070
head df68367b30947402f4f9f7da464eb0f3e5d16ff8
artifact 12596704425
artifact sha256 6865641acf8c7ae59832b83871838349b41acf290c43f972f16746e7ba235f04
result = FAIL
```

The recovered artifact showed exactly one error:

```text
adopted Stage49-50 candidate does not contain both Stage49 and Stage50
```

All other structural/semantic guards were already PASS.

Root cause was a validator schema assumption:
- representative recipes use `recipes`;
- the adopted Stage49–50 candidate correctly uses `stageOverrides`.

The validator was corrected to accept both containers. No plan or candidate content changed.

Final exact-source run:
```text
run      40189296422
artifact 12597413342
head     a2817325b87fe4796d7f3c10c860835e30513df0
artifact sha256 d7a18825573c798484995d4ce107ff5d161365c1ad4e4bb5f134bee861d28643
status   PASS
errors   []
warnings []
```

## 4. Exact source identities

```text
plan sha256
= da383188a61f0488769b87e5767286ece7840d15262ebb07ed8c449173a6b806

skeleton sha256
= 4bc8af12324cee744f1bcb55e3261f41012e741c97fbcdbd8f5dadd6a297bf4c

representative v0.2 sha256
= 3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf

adopted Stage49-50 candidate sha256
= c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3
```

## 5. Static guards passed

All target stage signatures exactly match the canonical skeleton.

Semantic guards all passed:

```text
Stage8  = first G+R mixed bridge
Stage15 = BRUTE teach
Stage19 = first B+R target-order contrast
Stage25 = Lv21 buffer / C0
Stage29 = first bounded F08 synthesis
Stage30 = Checkpoint B
Stage31 = soft-wall entry / C1
Stage33 = Mage density surface
Stage37 = bounded F08 tempo
Stage38 = durable bridge into Stage39
```

Also passed:
- no target overlaps an already-authored representative recipe;
- all required context anchors exist;
- adopted Stage49/50 override identity is intact;
- production change authorization = false;
- full T1 exact recipe freeze authorization = false;
- monster/class/shop/EXP/P×P scalar changes remain unauthorized.

## 6. What this PASS means

It authorizes the **plan shape**, not the actual new Stage recipes.

```text
PASS = these 13 stages are a consistent next bounded authoring wave
PASS != exact spawn recipe approved
PASS != dynamic execution approved
PASS != numerical freeze
PASS != production change
PASS != full Stage1-50 recipe freeze
```

## 7. Next decision boundary

Next candidate action:

```text
MATERIALIZE_WAVE_A_EXACT_SPAWN_RECIPE_CANDIDATES
```

If approved, materialization should occur slice-by-slice in this order:

```text
A1 -> static recipe gate
A2 -> static recipe gate
A3 -> static recipe gate
A4 -> static recipe gate
```

Do not author all 13 and only validate at the end. Each slice should fail cheaply before the next slice is expanded.

No dynamic execution should begin until the corresponding materialized slice passes its static recipe gate.