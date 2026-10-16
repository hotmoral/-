# Mobi P1-C — Public 3D Cat Mesh → 96x96 Projection Feasibility Final Result

Date: 2026-10-16
Status: **CLOSED / PASS / PROMISING STATIC MORPHOLOGY SOURCE**
Public branch: `mobi/experiment-3d-cat-projection-feasibility-20261016`
Private canonical state: unchanged / not automatically imported

## 1. Question answered

> Can an already-authored, redistribution-safe public domestic-cat 3D mesh preserve convincing feline body identity across representative views when projected and rasterized directly to native 96x96 output, without 2D shape authoring or decorative rescue?

For the frozen Innerscene `Standing cat` structural body:

> **YES, sufficiently for a next-stage reduction/generative-model feasibility study.**

This is not production adoption.

## 2. Source / license result

Primary source:

- provider: Innerscene
- asset: `Standing cat`
- provider file: `cat-original.glb`
- license: CC0 / public domain
- exact bytes: `4,903,420`
- SHA-256: `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`

Stage A conclusion:

> redistribution-safe source found.

## 3. Raw structure result

Primary structural node:

`Cat continuous body`

- vertices: 99,642
- triangles: 199,280
- one index-graph connected component
- closed orientable manifold by edge topology
- boundary edges: 0
- non-manifold edges: 0
- orientation mismatch edges: 0
- degenerate index triangles: 0
- duplicate triangles: 0
- Euler characteristic: 2
- no skins
- no animations
- no morph targets
- no textures/images

Facial/decorative geometry is separately addressable and was excluded from the primary structural gate.

Stage B conclusion:

> structurally clean static feline body source; no repair required before projection.

## 4. Frozen projection result

One projection identity was frozen before evidence:

- structural node only;
- +Y up / +Z anatomical front / X bilateral;
- orthographic;
- common center/floor/scale;
- no per-view fitting;
- 96×96;
- binary pixel-center triangle-union raster;
- no antialiasing;
- no dilation/erosion;
- no outline;
- no texture/lighting/shading;
- views: 0° / 22.5° / 45° / 67.5° / 90°.

Stage D accepted execution:

- run `38894114430` — SUCCESS
- job `116950377428` — SUCCESS
- execution HEAD `075f99c318d156b265d63f9c3bfe9b98df6f1404`
- artifact `12043770156`
- digest `sha256:cc6b851671e2a4c489c78155aeefb9dd2f3cd85f64b8e059c02350fcd04ab8b0`
- seed 1 / 777 evidence: byte-identical

## 5. Perceptual result

### Exact profile

**STRONG PASS** for feasibility.

Cat identity survives from trunk proportions, fore/hind differentiation, haunch/chest organization, head/neck relation and tail-root/body continuity.

### Near-profile

**STRONG PASS**.

Source morphology remains coherent as depth becomes visible.

### 45° 3Q

**PASS**.

No generic-quadruped collapse; limb emergence and body mass remain plausible.

### Near-front

**PASS WITH CAUTION**.

Foreshortening is strong but chest breadth and support organization remain readable.

### Exact front

**MARGINAL / BOUNDED PASS**.

This is the weak view. Ears and raised tail contribute materially, and silhouette-only projection hides internal surface depth. However the specific hard-stop failure — narrow central body column plus generic long support columns — does not occur. Chest breadth remains materially wider than head/neck and the primary support legs remain separated.

## 6. Why this is materially different from R9

R9 demonstrated that continuous curve ownership + deterministic pixel rasterization is mechanically feasible but its frozen low-order neutral carrier remained structurally generic.

The current experiment changes the causal source of morphology:

- R9: low-order procedural body carrier authored by the project;
- current: externally pre-authored feline 3D morphology, then direct projection.

The positive result therefore supports the new hypothesis:

> **The missing ingredient was not rasterization bandwidth alone; sufficiently feline source morphology can survive the small-output reduction.**

Do not infer that high vertex count itself is necessary. That is the next question.

## 7. What passed

The following narrow proposition is now supported:

> **A high-quality-enough continuous 3D feline source can preserve useful CAT_ID at native 96px across profile → 3Q → front without authored 2D view banks or decorative facial rescue.**

That is enough to justify studying mathematical reduction.

## 8. What did not pass / is not tested

Not established:

- production source selection;
- final adult Mobi design;
- exact-front production quality;
- animation;
- rigging;
- contact semantics mapping;
- runtime 3D architecture;
- Android performance;
- growth stages;
- morphology variants;
- low-poly sufficiency;
- generative parameterization;
- compression level;
- semantic landmark set;
- authored-pixel representation rejection;
- private canonical change.

## 9. Consequence for the mathematical-model idea

The original question was whether known 3D coordinates could become the starting point for a mathematical whole-cat representation.

This experiment removes the first major uncertainty:

> the full coordinate-defined mesh contains feline information that remains visible after the intended small-output projection.

Therefore it is now rational to ask whether the 99,642-vertex source can be reduced while preserving the same native-scale evidence.

The next ladder should be evidence-preserving, not theory-first:

`full mesh`
→ `silhouette-relevant geometry / topology`
→ `semantic landmarks + anatomical sections/curves`
→ `deformable low-dimensional controls`
→ only then `generative morphology parameters`.

At every reduction step, the frozen 96px views act as a perceptual regression target.

## 10. Final decision token

> **CLOSED / `PUBLIC_3D_CAT_96PX_PROJECTION_VIABILITY_DEMONSTRATED`**

with retained qualifier:

> **`EXACT_FRONT_REMAINS_THE_WEAKEST_VIEW_AND_MUST_NOT_BE_HIDDEN_BY_LATER_REDUCTION`**

## 11. Next bounded question

Eligible, not started:

> **P1-C 3D Morphology Reduction / Generative Parameterization Feasibility**

Primary question:

> How much of the successful full mesh can be removed/re-expressed as semantic geometry before native 96px CAT_ID / HEAD_BODY / mass hierarchy materially degrades?

Do not start with a compact formula and fit it until it looks right. Start from the successful source and remove degrees of freedom under frozen perceptual regression gates.
