# Mobi P1-C — 3D Cat Stage D Native 96px Direct Visual Review

Date: 2026-10-16
Status: **PASS / PROMISING / FRONT-VIEW CAUTION RETAINED**
Public branch: `mobi/experiment-3d-cat-projection-feasibility-20261016`

## 1. Review scope

This review evaluates only the frozen Stage C primary structural output:

- source: Innerscene `Standing cat`, exact SHA-256 frozen in Stage B;
- geometry: exact source node `Cat continuous body` only;
- 99,642 vertices / 199,280 triangles;
- orthographic projection;
- one common center, floor and scale;
- native 96×96;
- binary triangle-union silhouette at pixel centers;
- no antialiasing;
- no per-view fitting;
- no eye / pupil / glint / mouth / muzzle-pad / nose / inner-ear patch / whisker meshes;
- no texture, fur, lighting, shadow, normal-map, outline or hand-pixel correction.

Native 96px evidence owns the judgement. 8× nearest-neighbour images are diagnostic only.

## 2. Accepted execution

Workflow:

`Mobi P1-C 3D Cat Stage D Projection`

- run: `38894114430` — SUCCESS
- job: `116950377428` — SUCCESS
- execution HEAD: `075f99c318d156b265d63f9c3bfe9b98df6f1404`
- artifact: `12043770156`
- artifact digest: `sha256:cc6b851671e2a4c489c78155aeefb9dd2f3cd85f64b8e059c02350fcd04ab8b0`
- projection tests: PASS
- source SHA exact check: PASS
- PYTHONHASHSEED 1 / 777 evidence directories: byte-identical

Every rendered view remained one 8-connected occupied pixel component.

## 3. Frozen view metrics

| View | Yaw | Occupied px | Native bbox |
|---|---:|---:|---|
| EXACT_FRONT | 0° | 1,158 | `[34,8,61,90]` |
| NEAR_FRONT | 22.5° | 1,521 | `[29,8,69,90]` |
| STRONG_3Q | 45° | 1,926 | `[19,8,80,90]` |
| NEAR_PROFILE | 67.5° | 2,166 | `[9,8,87,90]` |
| EXACT_PROFILE | 90° | 2,043 | `[5,8,90,90]` |

The width change is real orthographic foreshortening. It was not normalized view-by-view.

## 4. Exact profile — STRONG PASS

Evidence:

`P1C_3D_CAT_EXACT_PROFILE_96.png`

Observed at native scale:

- immediate quadruped/cat readability;
- horizontally organized trunk rather than a plank-like procedural bar;
- recognizable shoulder/chest → abdomen → pelvis/haunch progression;
- hindlimb has a distinctly flexed feline/digitigrade contour rather than a straight support column;
- forelimb is straighter and emerges under the cranial thorax, producing useful fore/hind differentiation;
- head/neck transition remains compact and plausible;
- tail root leaves the posterior body continuously and rises in a coherent curve;
- the silhouette survives hard 1-bit rasterization without needing texture or shading.

Weaknesses retained:

- the source is a generic visualization mesh rather than production feline anatomy;
- the binary head is simplified and does not prove final facial proportion quality.

Disposition:

> **PROFILE CAT_ID / mass organization: STRONG PASS for feasibility.**

## 5. Near-profile 67.5° — STRONG PASS

Evidence:

`P1C_3D_CAT_NEAR_PROFILE_96.png`

Observed:

- profile identity does not collapse when depth becomes visible;
- torso thickness changes coherently;
- fore/hind supports remain differentiated rather than becoming four identical columns;
- chest and haunch volume remain visible as different parts of one body envelope;
- tail/body continuity remains plausible;
- head remains attached through a believable neck/chest transition.

Disposition:

> **NEAR_PROFILE CAT_ID / proximal emergence: STRONG PASS for feasibility.**

## 6. Strong 3Q 45° — PASS

Evidence:

`P1C_3D_CAT_STRONG_3Q_96.png`

Observed:

- still reads as the same cat rather than a separately authored view;
- foreshortening is coherent;
- hindlimbs retain flexion and do not collapse into the same geometry as forelimbs;
- four-limb overlap is plausible for a static standing cat;
- chest/trunk/haunch remain a continuous mass;
- head/body relation remains readable despite removal of all facial accessory meshes.

The 3Q result is materially more feline than the generic-quadruped failure pattern seen in the rejected R9 carrier. This is a causal difference in source morphology, not evidence that rasterization itself improved.

Disposition:

> **3Q CAT_ID / HEAD_BODY / limb emergence: PASS.**

## 7. Near-front 22.5° — PASS WITH CAUTION

Evidence:

`P1C_3D_CAT_NEAR_FRONT_96.png`

Observed:

- the body remains recognizably animal/cat-like under strong foreshortening;
- chest breadth remains materially greater than the neck/head base;
- the supporting limbs do not collapse into one central column;
- one side of the body and hindlimb still provides useful depth ordering in silhouette;
- the raised tail remains a strong anatomical cue.

Caution:

- silhouette-only head specificity is reduced as expected near front;
- pointed outer ears and raised tail contribute materially to CAT_ID.

Disposition:

> **NEAR_FRONT: PASS, but not a production-quality front-head proof.**

## 8. Exact front — MARGINAL / BOUNDED PASS

Evidence:

`P1C_3D_CAT_EXACT_FRONT_96.png`

This is the weakest view and is treated conservatively.

Positive:

- the source does not collapse to zero/narrow line width;
- shoulder/chest silhouette is visibly wider than the head/neck region;
- the two primary support legs remain separated;
- leg roots emerge from a broad lower chest rather than from one thin central trunk;
- the overall body therefore avoids the specific R9 failure pattern of a narrow vertical body column with long columnar legs;
- all facial decorative meshes are already absent, so this result is not being rescued by eyes, muzzle pads, nose, pupils, whiskers or inner-ear coloring.

Limitations:

- front silhouette contains less explicit abdomen/pelvis information because of self-occlusion;
- the upright tail projects close to the central/head region and is visually prominent;
- pointed outer ears remain an important CAT_ID cue;
- binary silhouette alone cannot express surface-depth organization inside the chest/head masses.

Disposition:

> **EXACT_FRONT HEAD_BODY: MARGINAL PASS for the narrow projection-viability question, with explicit caution.**

The predeclared hard stop was front collapse into a generic vertical/columnar quadruped organization. That specific collapse is not observed here.

## 9. Ear-dependence assessment

An additional destructive “ear removal” rerender is **not triggered inside this frozen Stage D identity**.

Reason:

- profile, near-profile and 3Q CAT_ID remain supported by trunk proportions, hind/fore limb differentiation, haunch/chest organization and tail-root/body continuity, not just the pointed ears;
- all non-body facial meshes are already removed;
- the outer ears are continuous anatomical geometry in the one closed body mesh, so deleting them after evidence would require a new geometry-edit rule and would violate the frozen no-edit projection identity.

The exact-front caution explicitly records that ears and tail remain material cues. If a future reduction model loses torso/limb cues and begins relying predominantly on ears, a separately contracted anti-ear diagnostic will be required before acceptance.

## 10. Pixel-readability review

PASS.

At native 96px:

- no catastrophic silhouette fragmentation;
- all five views are one occupied component;
- thin tail and lower limbs survive center-sample rasterization;
- limb bends remain readable in oblique/profile views;
- no antialiasing or dilation is required to keep the cat coherent.

The nearest-neighbour enlargements reveal expected single-pixel stair-stepping but no hidden repair.

## 11. Causal interpretation

Demonstrated:

1. an already-authored feline 3D body can survive direct 96×96 orthographic reduction;
2. strong profile/3Q CAT_ID survives after removing decorative facial geometry;
3. the same mesh supports all tested orientations with no view-specific shape data;
4. the front view remains structurally weak relative to profile/3Q but does not reproduce the R9 hard collapse;
5. deterministic 1-bit rasterization does not erase the source morphology.

Not demonstrated:

1. that this exact asset is production-quality Mobi morphology;
2. that all domestic-cat meshes will work;
3. that animation/rigging works;
4. that the source can be heavily reduced without CAT_ID loss;
5. that a low-dimensional generative equation system can reproduce it;
6. that four growth stages can be generated;
7. that 3D runtime rendering should be adopted.

## 12. Direct-review decision

> **PASS / `PUBLIC_3D_STATIC_CAT_MORPHOLOGY_SURVIVES_NATIVE_96PX_PROJECTION_WITH_FRONT_VIEW_CAUTION`**

This is the first positive evidence needed to justify asking the next question:

> Which parts of the full 99,642-vertex morphology actually carry the 96px feline signal, and how far can they be reduced before this evidence breaks?
