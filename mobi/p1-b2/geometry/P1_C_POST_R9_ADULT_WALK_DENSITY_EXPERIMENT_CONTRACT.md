# Mobi P1-C — Adult Walk Direction/Frame Density Experiment Contract

Status: **ACTIVE / EXPERIMENT CONTRACT FROZEN**  
Date: **2026-10-16**

## 1. Purpose

This experiment isolates one question:

> For one adult-cat normal-walk loop rendered as small pixel animation, what direction count and temporal frame count are sufficient before additional authored assets produce diminishing perceptual return?

This is not a final-art acceptance test and not a proof that a procedural carrier is the production representation.

## 2. Fixed subject

- growth stage: G4 adult candidate
- nominal native canvas: 96x96 px
- behavior: normal level-ground walk only
- gait family: four-beat lateral-sequence walk
- reference footfall order: RH -> RF -> LH -> LF
- reference nominal cycle duration: 1.08 s
- reference stance duration: 0.80 s
- reference swing duration: 0.28 s
- stance fraction used by the controlled model: 0.80 / 1.08
- final-art texture, fur, coat pattern and expression: excluded

The gait timing is a controlled engineering reference derived from adult-cat locomotion literature, not a claim that every real cat uses exactly one timing at every speed.

## 3. Independent variables

Direction-count candidates:

- 12 directions (30 deg spacing)
- 16 directions (22.5 deg spacing)
- 24 directions (15 deg spacing)
- 36 directions (10 deg spacing)

Frame-count candidates per walk cycle:

- 12 frames
- 16 frames
- 24 frames
- 32 frames

The full 4x4 grid is evaluated mechanically. Perceptual review may prune before any production asset authoring.

## 4. Controlled reference

A single deterministic continuous gait reference is sampled at high angular and temporal resolution.

Every candidate library is obtained only by quantizing that same reference in:

- yaw/orientation,
- gait phase.

No candidate receives hand tuning, view-specific repair, frame-specific repair or different body proportions.

This ensures the experiment measures density rather than differences in drawing quality.

## 5. Metrics

For each candidate configuration:

### Direction quantization
- mean and P95 binary-mask disagreement against continuous-yaw reference
- worst angular quantization error
- adjacent-direction visual-step statistics

### Temporal quantization
- mean and P95 binary-mask disagreement against continuous-phase reference
- maximum phase-time quantization in milliseconds
- support-state mismatch rate
- loop seam step relative to ordinary adjacent-frame step

### Combined density
- mean and P95 disagreement under simultaneous yaw + phase quantization
- asset-frame count = directions x frames

### Stability
- deterministic rerender equality
- finite coordinates
- nonempty raster

## 6. Perceptual review

Mechanical scores do not select the winner alone.

Review at native and nearest-neighbor enlarged scale for:

- recognisable four-beat walk rhythm
- shoulder/haunch alternation readability
- planted-paw sliding impression
- loop seam visibility
- orientation stepping
- front/3Q/profile readability
- diminishing visual return from added directions
- diminishing visual return from added frames

## 7. Transition scope

Only minimal walk-state topology is represented conceptually:

`IDLE -> WALK_START -> WALK_LOOP -> WALK_STOP -> IDLE`

No transition assets are authored in this density experiment.

A later transition graph must contain only semantically/plausibly reachable edges. A full Cartesian transition matrix is explicitly forbidden. Examples of direct edges that should not exist include `RUN -> SLEEP` and arbitrary cross-direction pose jumps such as leftward walking directly into a right-oriented lying pose.

## 8. Non-goals

Do not in this experiment:

- build all four growth stages;
- build running, sitting, grooming, jumping, sleeping or social behavior;
- decide final direction count for all behavior classes;
- decide final frame count for all behavior classes;
- create production coat/color variants;
- create a full transition library;
- treat synthetic reference art as production pixel art.

## 9. Decision rule

Prefer the smallest candidate on the perceptual plateau.

A higher-density candidate is justified only when the added authored-frame cost produces a material visible improvement at native scale or fixes a concrete semantic/contact failure.

The expected output is a bounded recommendation such as:

- direction-count plateau candidate(s),
- frame-count plateau candidate(s),
- combinations requiring direct authored-pixel validation,
- combinations pruned as clearly under-dense or over-dense.

No production-wide number is frozen by this experiment alone.
