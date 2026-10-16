# Mobi P1-C-R10 — Reference 3D Morphology Reduction Feasibility Final Result

Date: 2026-10-16
Status: **CLOSED / PASS / QUALITY FLOOR ESTABLISHED**
Public branch: `mobi/run-p1-c-r10-morphology-reduction-20261016`
Private canonical import: not yet done by this document

## 1. Question answered

> How far can the known-successful 99,642-vertex feline body be reduced before structural fidelity or smooth-form quality becomes inadequate at Mobi's native 96×96 target?

Answer:

> **The tested body can be reduced by roughly 97% while retaining a strong practical quality margin.**

## 2. Key result

- full reference: **99,642 vertices / 199,280 triangles**
- `QUALITY_HEADROOM`: **3,125 vertices / 6,246 triangles**
- `MIN_PASS_TESTED`: **1,560 vertices / 3,116 triangles**
- `FIRST_FAIL_TESTED`: **1,088 vertices**
- 780 vertices: further hard FAIL

The project must not select 1,560 merely because it passes.

The recommended working reduction baseline is:

> **3,125 vertices / 6,246 triangles**

because the Product Owner explicitly requires avoiding a visibly angular cat.

## 3. Why 3,125 rather than 1,560

3,125 vertices:

- all five frozen 96×96 views PASS;
- minimum primary-view IoU ≈ `0.98945`;
- only 80 differing native pixels across all five views;
- yaw behavior remains close to the reference;
- silhouette remains materially reference-like;
- retains one full broad-ladder step of geometric margin above the lowest tested pass.

1,560 vertices:

- still hard PASS;
- minimum IoU ≈ `0.97861`;
- 153 differing pixels across the five views;
- stronger face-normal/dihedral changes;
- therefore retained as lower-bound evidence rather than preferred quality baseline.

1,088 vertices:

- near-profile IoU `0.971351` < `0.975` hard floor;
- confirmed FAIL.

## 4. Important angularity finding

The raw 96×96 silhouette hides much of interior mesh faceting.

Measured adjacent-face angularity rises substantially as geometry is reduced:

- reference P95 dihedral ≈ 8.64°;
- 3,125 P95 ≈ 47.92°;
- 1,560 P95 ≈ 60.07°;
- 1,088 P95 ≈ 69.47°;
- 780 P95 ≈ 78.15°.

These values include genuine anatomical curvature and are not a direct visible-facet score, but the trend proves that geometric smoothness reserve becomes materially smaller below the few-thousand-vertex range.

This supports keeping `QUALITY_HEADROOM` above the bare pass boundary.

## 5. Broad-ladder execution

- run `38897708802` — SUCCESS
- job `116962078574` — SUCCESS
- execution HEAD `31a33045997aacfcd90a8120c8683fef32f4b75d`
- artifact `12045305614`
- digest `sha256:a52fead3dfca8028e17857b7ff038f8449ffd425b52cec295d3c109691cf5769`

## 6. Boundary/smoothness execution

- run `38898663428` — SUCCESS
- job `116965212281` — SUCCESS
- execution HEAD `4fa99a67bcfedbff40dc934d9eaba0546bdb60cb`
- artifact `12045116564`
- digest `sha256:99a1e41bfa63f014262d51ba5f6401a8c28bdc8e517005d01c27c70fd3a12d8f`

Both runs used the exact source hash and deterministic seed comparison.

## 7. Preserved anomalies / caveats

### 25,000-vertex transient topology failure

The Lane-A 25k candidate contained one non-manifold edge and is rejected as a candidate. Lower final candidate tiers were independently topology-audited and returned valid connected closed oriented manifolds.

This anomaly is preserved; it is not hidden or averaged away.

### `agg=0` lane

Quality-first QEM could only reach 82,703 vertices and therefore did not discriminate the useful range. This is an algorithm-setting reach limitation, not product evidence against reduction.

### 3D source-space fidelity

R10 established topology, area/volume, triangle-shape and dihedral diagnostics plus native raster/yaw evidence. It did not yet establish final deformation quality, animation quality, semantic landmark sufficiency or source-to-canonical contact mapping.

## 8. What this proves

Supported proposition:

> **The 96×96 feline signal demonstrated by the full source does not require the original ~100k vertex density; a ~3.1k-vertex connected surface retains a strong practical quality margin.**

This is the first concrete bridge from raw coordinate storage toward a compact mathematical morphology representation.

## 9. What it does not prove

Not established:

- 3,125 vertices are the final production topology;
- runtime 3D is selected;
- rigging/skinning works;
- the source mesh owns canonical physics;
- four growth stages are solved;
- final Mobi art is selected;
- semantic landmarks/curves are sufficient;
- final generative equations exist.

## 10. Next recommended question

Before animation or runtime work, perform a new bounded change-control/contract for:

> **semantic structural abstraction of the 3,125-vertex quality-headroom reference.**

Candidate next ladder:

`3,125-vertex quality reference`
→ `semantic landmarks`
→ `anatomical section/curve network`
→ `surface reconstruction from those controls`
→ `native 96×96 regression`
→ only after success, deformable/generative parameters.

Do not start by inventing another tiny forward-fit cat model.

## 11. Final decision token

> **CLOSED / `R10_REFERENCE_3D_MORPHOLOGY_REDUCTION_QUALITY_FLOOR_ESTABLISHED`**

with selected working evidence baseline:

> **`R10_QUALITY_HEADROOM_V3125_F6246`**

and lower-bound evidence:

> **`R10_MIN_PASS_TESTED_V1560` / `R10_FIRST_FAIL_TESTED_V1088`**
