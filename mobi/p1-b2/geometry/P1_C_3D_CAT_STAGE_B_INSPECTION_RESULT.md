# Mobi P1-C — 3D Cat Stage B Raw Mesh Inspection Result

Date: 2026-10-16
Status: **CLOSED / PASS / STRUCTURALLY_INSPECTABLE_STATIC_CAT_MESH**
Public branch: `mobi/experiment-3d-cat-projection-feasibility-20261016`
Private canonical authority: unchanged

## 1. Frozen source identity

Primary source:

- provider: Innerscene
- asset: `Standing cat`
- provider file: `cat-original.glb`
- license: CC0 / public domain
- downloaded bytes: `4,903,420`
- SHA-256: `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- GLB version: 2
- declared asset version: 2.0
- generator: `Khronos glTF Blender I/O v5.2.40`

The topology diagnostic reacquired the provider file independently and required the same SHA-256 before analysis. Source drift therefore did not occur between the two accepted runs.

## 2. Main Stage B execution

Workflow:

`Mobi P1-C 3D Cat Stage B Inspection`

- run: `38893007226` — SUCCESS
- job: `116946790029` — SUCCESS
- execution HEAD: `ec1105ce6cf6512f531ef409433452b6af4ced5d`
- artifact: `12041969360`
- artifact digest: `sha256:2dbb79061d20561cfdeb1e8070e82c8bbf296bac3a3a6a7455281b2092fb30ac`
- bounded inspector tests: 2/2 PASS
- PYTHONHASHSEED 1 / 777 inspection output: byte-identical
- source page + library terms archived in evidence
- CC0 text checks: PASS

Frozen inspector blobs:

- `p1_c_3d_cat_stage_b_inspector_v1.py`: `9b7899bc1c39d02291813a826df01d3697192846`
- `test_p1_c_3d_cat_stage_b_inspector_v1.py`: `f7125437320b6bbf6c2d70cdbe8dd306002577ec`

## 3. Container / scene structure

- scene count: 1
- node count: 19
- mesh count: 19
- mesh nodes in default scene: 19
- primitive count: 19
- material count: 8
- accessor count: 65
- buffer view count: 65
- buffer count: 1
- texture count: 0
- image count: 0
- skin count: 0
- animation count: 0
- morph-target sets: 0
- camera count: 0
- required glTF extensions: none
- non-finite POSITION scalars: 0

The model is therefore a static geometry source. There is no hidden rig, animation or morph system to conflate with the morphology test.

## 4. World bounds

Full source world bounds:

- min: `[-0.1551885903, 0.0055554211, -0.4041111767]`
- max: `[ 0.1551885903, 0.7522867620,  0.3905487061]`
- extents: `[0.3103771806, 0.7467313409, 0.7946598828]` m

These agree with the provider's approximately `310.4 × 794.7 × 746.7 mm` dimensions after accounting for source-axis ordering.

## 5. Structural body separation

The decisive structural mesh is explicitly named:

> `Cat continuous body`

It is node 0 / mesh 0 and consists of one triangle primitive:

- vertices: `99,642`
- triangles: `199,280`
- index references: `597,840`
- connected components by index graph: `1`
- attributes: POSITION + NORMAL
- material index: 0

Its world bounds are:

- min: `[-0.1237740517, 0.0055554211, -0.4041111767]`
- max: `[ 0.1237795800, 0.7522867620,  0.3667509556]`
- extents: `[0.2475536317, 0.7467313409, 0.7708621323]` m

The remaining 18 meshes are separately named facial/decorative components:

- Eye ×2
- Eye glint ×2
- Inner ear ×2
- Mouth
- Muzzle pad ×2
- Nose
- Vertical pupil ×2
- Whisker ×6

Therefore the Stage C appearance firewall can be implemented by one global source-space rule:

> **include only the exact node `Cat continuous body` for the primary structural raster.**

No per-view masking, paint-over, silhouette correction or hand selection is required.

This also removes the full-source x-extent inflation caused by whiskers.

## 6. Topology diagnostic

Because the primary body is large and high-resolution, a second bounded diagnostic was added instead of mutating the accepted Stage B run.

Workflow:

`Mobi P1-C 3D Cat Stage B Topology Diagnostic`

- run: `38893431641` — SUCCESS
- job: `116948154143` — SUCCESS
- execution HEAD: `37629e1c1da6de95122f7450bf096f38fd0ac791`
- artifact: `12043245096`
- artifact digest: `sha256:91d671433218a8affd2f754915207b9612628d56682cb266dd12b52be94d93d1`
- topology unit tests: PASS
- source SHA-256 exact recheck: PASS

Primary body topology:

- V = `99,642`
- E = `298,920`
- F = `199,280`
- every unique edge multiplicity = exactly 2
- boundary edges = `0`
- non-manifold edges = `0`
- orientation-mismatch edges = `0`
- degenerate index triangles = `0`
- duplicate triangles = `0`
- Euler characteristic `χ = V - E + F = 2`
- genus under connected/closed/orientable interpretation = `0`

Disposition:

> **The primary structural body is a clean single connected closed orientable 2-manifold by index topology.**

This is unusually favorable for deterministic projection/silhouette work and later geometric reduction studies.

## 7. Stage B interpretation

Demonstrated:

1. a redistribution-safe exact source exists;
2. the raw file can be reacquired reproducibly by hash;
3. the source contains a single, clean, high-resolution continuous cat body mesh;
4. facial/decorative geometry is separately addressable;
5. no rig/animation/morph or texture dependency is required for the morphology discriminator;
6. no malformed/non-finite geometry was found;
7. the primary body topology does not require repair before projection.

Not demonstrated:

1. feline identity at 96x96;
2. exact profile/3Q/front perceptual quality;
3. suitability of this topology for runtime use;
4. suitability for deformation;
5. suitability for low-dimensional generative reduction;
6. canonical adoption.

## 8. Stage B decision

> **PASS / `REDISTRIBUTION_SAFE_CONTINUOUS_STATIC_CAT_MESH_STRUCTURALLY_VALID_FOR_PROJECTION_DISCRIMINATOR`**

The reason to proceed is narrow: the cheap source-quality prerequisites have passed without artistic repair.

## 9. Next boundary

Proceed to **Stage C — projection setup freeze** only.

Stage C must freeze, before visual evidence:

- source-axis interpretation;
- structural-node inclusion rule;
- yaw convention and exact representative angles;
- common camera/framing target;
- common orthographic scale/margin;
- raster coverage rule;
- deterministic output metadata.

Do not yet infer that Stage D will pass.
