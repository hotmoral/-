# Mobi P1-C-R10 — Direct Evidence Review

Date: 2026-10-16
Status: **CLOSED / DIRECT REVIEW COMPLETE**
Public branch: `mobi/run-p1-c-r10-morphology-reduction-20261016`
Scope: reference-derived static morphology reduction only

## 1. Review question

> How far can the already-successful 99,642-vertex feline body be simplified before native 96×96 structure or smooth-form margin becomes materially inadequate?

The Product Owner explicitly rejected choosing a visibly angular low-poly cat merely because CAT_ID remains recognizable.

Therefore direct review separates:

- `MIN_PASS_TESTED` — lowest tested tier satisfying hard structural gates;
- `QUALITY_HEADROOM` — denser recommended working tier with visible/geometric margin.

## 2. Immutable reference

Source:

- Innerscene `Standing cat`
- `cat-original.glb`
- structural node `Cat continuous body`
- source SHA-256 `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- 99,642 vertices
- 199,280 triangles
- connected closed orientable body topology

Frozen projection identity is unchanged from the accepted 96×96 feasibility group.

## 3. Broad-ladder execution identity

Run:

- workflow run `38897708802` — SUCCESS
- job `116962078574` — SUCCESS
- execution HEAD `31a33045997aacfcd90a8120c8683fef32f4b75d`
- artifact `12045305614`
- artifact digest `sha256:a52fead3dfca8028e17857b7ff038f8449ffd425b52cec295d3c109691cf5769`
- `fast-simplification==0.2.0`
- NumPy `2.5.4`
- Python 3.12
- seed 1 / 777 outputs byte-identical

All environment/source/blob/unit-test gates passed before evidence.

## 4. Lane A — ordinary QEM (`agg=7.0`)

Broad result:

| Tier | Vertices | Triangles | Structural hard gate | Notes |
|---|---:|---:|---|---|
| L0 | 99,642 | 199,280 | PASS | immutable reference |
| L1 | 50,000 | 99,996 | PASS | visually/reference-near |
| L2 | 25,000 | 49,996 | FAIL | one transient non-manifold edge; candidate discarded |
| L3 | 12,500 | 24,996 | PASS | final topology independently valid |
| L4 | 6,250 | 12,496 | PASS | strong margin |
| L5 | 3,125 | 6,246 | PASS | strong native-scale fidelity |
| L6 | 1,560 | 3,116 | PASS | lowest broad hard-pass tier |
| L7 | 780 | 1,556 | FAIL | near-profile/profile silhouette gates fail |

The L2 topology anomaly is preserved as evidence. It does not make lower final candidates valid by assumption; L3-L7 topology was independently audited. L3-L7 return to one connected closed oriented manifold states. The simplification is offline source reduction, not a runtime collapse animation, so the invalid L2 candidate is simply excluded.

## 5. Lane B — quality-first QEM (`agg=0.0`)

Result:

- collapse count: 16,939
- minimum reachable vertex count: 82,703
- therefore the lane could not reach even the 50,000-vertex first discriminator.

Disposition:

> `TARGET_NOT_REACHED` / algorithm-setting reach limitation.

Do not reinterpret this as morphology failure and do not raise aggression after evidence inside Lane B.

## 6. Broad silhouette progression

Key Lane A static metrics against the full reference:

### 3,125 vertices

- all five views hard PASS
- minimum primary-view IoU: `0.98945`
- total differing pixels across five 96×96 views: `80`
- surface-area ratio: `1.011713`
- absolute-volume ratio: `0.995212`
- max excess adjacent-yaw XOR/union over reference: `0.003427`

Direct native review:

> body/head/limb/tail silhouette remains materially reference-like; no meaningful low-poly character is visible at the target output scale.

### 1,560 vertices

- all five views hard PASS
- minimum primary-view IoU: `0.978607`
- total differing pixels across five views: `153`
- surface-area ratio: `1.015976`
- absolute-volume ratio: `0.989426`
- max excess adjacent-yaw XOR/union: `0.005735`

Direct native review:

> still acceptable and recognizably feline, but this is visibly/quantitatively closer to the degradation boundary than 3,125.

### 780 vertices

- hard FAIL
- near-profile IoU: `0.971028`
- exact-profile IoU: `0.969495`
- total differing pixels: `237`
- max excess adjacent-yaw XOR/union: `0.009781`

Direct review:

> coarse reduction begins to alter the profile/near-profile envelope too much. This tier is below the useful quality floor.

## 7. Predeclared boundary refinement

The broad bracket was:

- PASS = 1,560
- FAIL = 780

Contract rule:

- geometric mean ≈ 1,103.09
- round to nearest 64
- frozen first refinement target = **1,088 vertices**

No target was chosen from visual fitting.

## 8. Boundary/smoothness execution identity

Run:

- workflow run `38898663428` — SUCCESS
- job `116965212281` — SUCCESS
- execution HEAD `4fa99a67bcfedbff40dc934d9eaba0546bdb60cb`
- artifact `12045116564`
- artifact digest `sha256:99a1e41bfa63f014262d51ba5f6401a8c28bdc8e517005d01c27c70fd3a12d8f`
- seed 1 / 777 byte-identical

Compared from one common `agg=7.0` collapse history:

- 3,125
- 1,560
- 1,088
- 780 vertices

## 9. 1,088-vertex refinement result

1,088 vertices:

- topology: PASS / connected closed oriented manifold
- exact front IoU: `0.981197`
- near front IoU: `0.983040`
- 45° 3Q IoU: `0.977355`
- near profile IoU: **`0.971351` — FAIL (< 0.975)**
- exact profile IoU: `0.979827`
- total differing pixels: `197`
- max same-view yaw IoU loss vs reference: `0.028649`

Therefore:

> **1,088 is a confirmed hard FAIL.**

The tested pass/fail bracket is now:

> **1,560 PASS ↔ 1,088 FAIL**

Further refinement is not required to choose a quality-headroom tier because the product question is not the mathematical absolute minimum.

## 10. Surface angularity diagnostic

Adjacent-triangle dihedral angle distributions were measured to expose geometric faceting hidden by flat silhouette output.

| Vertices | median | P95 | P99 | fraction >10° |
|---:|---:|---:|---:|---:|
| 99,642 ref | 1.42° | 8.64° | 15.96° | 3.25% |
| 3,125 | 9.45° | 47.92° | 74.75° | 47.76% |
| 1,560 | 12.96° | 60.07° | 87.21° | 57.68% |
| 1,088 | 15.56° | 69.47° | 98.58° | 64.95% |
| 780 | 18.54° | 78.15° | 103.02° | 70.05% |

Interpretation must be bounded:

- these values include real anatomical/high-curvature regions, so they are not a direct “visible polygon” score;
- nevertheless the monotonic rise shows the geometric smoothness reserve shrinking rapidly below the few-thousand-vertex range;
- 96×96 silhouette output hides much of this interior faceting, but later deformation or non-flat appearance could expose it.

This is exactly why the recommended tier must sit above the bare recognition floor.

## 11. Direct visual comparison

At native 96×96:

- 3,125 remains essentially reference-like across all five frozen views;
- 1,560 still passes but shows roughly double the aggregate changed pixels of 3,125 and has substantially larger local face-normal jumps;
- 1,088 crosses the silhouette hard boundary;
- 780 degrades further.

Nearest-neighbour enlargement was used only for diagnosis and did not replace native-scale judgment.

## 12. Direct selection

### `MIN_PASS_TESTED`

> **1,560 vertices / 3,116 triangles**

This is a useful lower-bound result, not the recommended working representation.

### `FIRST_FAIL_TESTED`

> **1,088 vertices**

### `QUALITY_HEADROOM`

> **3,125 vertices / 6,246 triangles**

Rationale:

1. only about 3.14% of the original vertex count remains;
2. five-view native silhouette fidelity remains very high;
3. yaw discontinuity remains close to reference;
4. body mass/limb/tail envelope remains perceptually stable;
5. it provides a full broad-ladder step of margin above the 1,560 minimum pass;
6. it materially reduces geometric angularity risk compared with 1,560/1,088;
7. choosing 1,560 solely because it passes would contradict the Product Owner's explicit “do not make the cat too angular” requirement.

## 13. Reduction significance

From 99,642 → 3,125 vertices:

- retained vertices ≈ 3.14%
- removed vertices ≈ 96.86%
- triangles 199,280 → 6,246
- retained triangles ≈ 3.13%

The successful small-output feline signal therefore does **not** require anything close to the original 100k-vertex density.

## 14. Result boundary

This review does not prove that 3,125 is the final mathematical Mobi representation.

It establishes a practical smooth geometry budget from which semantic abstraction can proceed.

The next logical question is no longer “how many raw mesh points can we delete?” but:

> **Can the ~3k-vertex quality-headroom shape be re-expressed by a much smaller semantic landmark / curve / section system while preserving the same regression evidence?**
