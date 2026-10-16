# Mobi P1-C — 3D Cat Stage C Projection Setup Freeze

Date: 2026-10-16
Status: **FROZEN / PRE-EVIDENCE**
Public branch: `mobi/experiment-3d-cat-projection-feasibility-20261016`

## 1. Purpose

Freeze every projection/framing/raster degree of freedom before native 96x96 visual evidence is generated.

No view may receive individual fitting.

## 2. Frozen structural geometry

Primary structural raster includes exactly one source node:

> `Cat continuous body`

Source identity:

- file SHA-256: `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- node index: 0
- mesh index: 0
- vertices: 99,642
- triangles: 199,280
- connected closed orientable manifold by Stage B topology evidence

Excluded globally from the primary gate:

- Eye ×2
- Eye glint ×2
- Inner ear patches ×2
- Mouth
- Muzzle pads ×2
- Nose
- Vertical pupils ×2
- Whiskers ×6

This exclusion is an appearance firewall, not view-specific editing. Outer ear geometry that belongs to `Cat continuous body` remains present.

## 3. Frozen source-axis interpretation

The source uses glTF coordinates and the raw geometry provides an independent semantic check:

- `+Y` = up;
- `+Z` = anatomical front;
- `X` = bilateral left/right axis.

Evidence for `+Z` front:

- eye, muzzle, nose, pupil and whisker meshes all occupy the positive-Z face region;
- nose reaches approximately `z=+0.389 m`;
- the continuous body's rear extent reaches approximately `z=-0.404 m`;
- paired facial parts are mirrored across positive/negative X.

No camera orientation is inferred from a rendered image after the fact.

## 4. Frozen structural reference frame

Continuous-body world AABB:

- min = `[-0.1237740517, 0.0055554211, -0.4041111767]`
- max = `[+0.1237795800, 0.7522867620, +0.3667509556]`

Frozen horizontal rotation/framing center from AABB midpoint:

- `cx = +0.0000027641654014587402 m`
- `cz = -0.018680110573768616 m`

Frozen floor:

- `y_ground = 0.0055554211139678955 m`

Frozen body height:

- `0.7467313408851624 m`

For yaw-independent horizontal fit, use the structural XZ bounding-circle diameter about `(cx, cz)`:

- radius = `0.3860869346743748 m`
- diameter = `0.7721738693487497 m`

This is deliberately slightly more conservative than exact-profile AABB width and guarantees one common scale across the full frozen yaw interval.

## 5. Frozen yaw convention

Let yaw `α` run from front to profile around +Y.

Camera forward vector, toward the target:

`f(α) = (sin α, 0, -cos α)`

Screen-right vector:

`r(α) = (cos α, 0, sin α)`

Screen-up:

`u = (0, 1, 0)`

Consequences:

- `α=0°`: camera is on +Z side, exact front;
- `α=90°`: camera is on -X side, exact profile;
- in exact profile, anatomical +Z/front points to screen-right.

Frozen representative views:

1. `0°` — EXACT_FRONT
2. `22.5°` — NEAR_FRONT
3. `45°` — STRONG_3Q
4. `67.5°` — SHALLOW_3Q / NEAR_PROFILE
5. `90°` — EXACT_PROFILE

No view-specific yaw adjustment is allowed after evidence.

## 6. Frozen orthographic framing

Canvas:

- `96 × 96` native pixels

Nominal minimum outer margin:

- `5 px`

Usable span:

- `86 px`

One common pixels-per-meter scale is derived before rendering:

`scale = min(86 / xzBoundingCircleDiameter, 86 / bodyHeight)`

Frozen numerical value:

> `scale = 111.37388017614773 px/m`

Horizontal mapping in continuous pixel-edge coordinates:

`screenX = 48 + scale * dot((p - centerXZ), r(α))`

Vertical mapping, top-left image convention:

`screenY = 91 - scale * (p.y - y_ground)`

Thus:

- the ground plane is fixed at continuous image Y = 91 for every view;
- horizontal center is fixed at X = 48;
- no per-view recentering occurs;
- no per-view scale/crop occurs.

The structural height occupies approximately `83.1664 px`; the yaw-independent XZ support bound occupies exactly `86 px`.

## 7. Frozen primary raster rule

Primary evidence is a **binary structural silhouette**.

For every projected source triangle:

- project its three vertices using the frozen orthographic mapping;
- evaluate native pixel centers `(x+0.5, y+0.5)`;
- a pixel is occupied if its center is inside or on at least one projected structural triangle;
- union coverage only; no lighting or material shading;
- shared-edge numerical comparisons use one fixed epsilon in implementation;
- no antialiasing;
- no subpixel hand correction;
- no morphological dilation/erosion;
- no outline stroke;
- no hole filling after rasterization.

Because this is silhouette occupancy, depth ordering cannot change whether a pixel is occupied. A z-buffer is therefore unnecessary for the primary binary gate and is intentionally excluded as irrelevant complexity.

## 8. Frozen output set

For each of the five views generate:

1. native `96×96` binary PNG;
2. exact nearest-neighbour `8×` diagnostic enlargement (`768×768`);
3. JSON metrics:
   - occupied pixel count;
   - occupied bounding box;
   - connected component count under 8-neighbour pixel connectivity;
   - centroid;
   - source yaw;
   - common scale and reference-frame values.

Also generate one horizontal five-view native-scale strip and one nearest-neighbour enlarged strip.

## 9. Determinism

Evidence must be rendered at least twice under different `PYTHONHASHSEED` values and be byte-identical.

PNG output must be deterministic: fixed encoder implementation/settings and no timestamps or nondeterministic metadata.

## 10. Primary review ownership

Direct native-scale perceptual review remains decisive for:

- CAT_ID;
- HEAD_BODY;
- chest / abdomen / pelvis hierarchy;
- fore/hind limb emergence;
- front-view collapse;
- silhouette stability;
- 96px readability.

Mechanical metrics may diagnose but may not override a perceptual fail.

## 11. No rescue after freeze

After this document is committed, do not change in response to visual evidence:

- selected source node;
- axes;
- center;
- floor;
- scale;
- margin;
- representative yaw angles;
- per-view framing;
- pixel coverage rule.

If these rules themselves prove invalid for a non-aesthetic technical reason, preserve the first evidence and open an explicit correction delta rather than silently rerendering.

## 12. Next boundary

Stage D is now eligible:

> render the frozen continuous-body source under this exact projection/raster contract, then conduct native-scale direct review.

No rigging, animation, generative reduction or private canonical adoption is authorized by this freeze.
