# Mobi P1-C — Public 3D Cat Mesh → 96x96 Projection Feasibility Contract

Date: 2026-10-16
Status: CONTRACT FROZEN / IMPLEMENTATION NOT YET STARTED
Public bounded branch: `mobi/experiment-3d-cat-projection-feasibility-20261016`
Canonical authority: private `hotmoral/Mobi` only

## 1. Primary question

> Can an already-authored, redistribution-safe public domestic-cat 3D mesh preserve convincing feline body identity across representative views when projected and rasterized directly to native 96x96 output, without 2D shape authoring or decorative rescue?

This is a cheaper discriminator before any attempt to compress a mesh into a deformable/generative mathematical cat model.

## 2. Frozen primary source

Primary source:

- provider: Innerscene
- asset: `Standing cat`
- page: https://www.innerscene.com/tools/library/3d-parts/standing-cat-cda42538
- download endpoint: https://www.innerscene.com/api/library/standing-cat-cda42538/download
- provider file name: `cat-original.glb`
- license: CC0 / public domain
- source-license review: `P1_C_3D_CAT_SOURCE_LICENSE_REVIEW.md`

The raw-file SHA-256 is not frozen until Stage B downloads the exact file. Once acquired, Stage B must record byte size and SHA-256 before any geometric processing.

## 3. Causal hypothesis

Previous R4–R9 attempts repeatedly tried to construct feline morphology from bounded procedural carriers. The new hypothesis is materially different:

> do not invent feline morphology first; use a pre-authored feline 3D body as source truth, then test whether projection + native raster reduction preserves the required cues.

If a credible 3D cat mesh still fails at native 96x96 without decorative rescue, then mesh compression, rigging and generative reduction are not justified yet.

## 4. Stage gates

### Stage A — source/license verification

Already complete in the companion source review.

Required result: explicit redistribution-safe source.

### Stage B — raw mesh acquisition and inspection

Must record at minimum:

- exact downloaded byte size;
- SHA-256;
- GLB/glTF version;
- scene count / default scene;
- node count;
- mesh count;
- primitive count;
- material count;
- POSITION accessor vertex counts;
- index accessor counts and implied triangle counts;
- coordinate bounds;
- number of connected mesh objects if recoverable without artistic processing;
- presence/absence of skins;
- presence/absence of animations;
- presence/absence of morph targets;
- presence/absence of texture/material dependencies;
- obvious malformed/non-finite data.

Stage B may not modify geometry.

### Stage C — projection setup freeze

Only after Stage B is structurally usable.

Freeze:

- body-up axis and forward axis inferred from source bounds/orientation;
- body centering rule;
- ground/floor alignment rule;
- camera target rule;
- camera elevation;
- orthographic scale rule;
- representative yaw set;
- silhouette-only material mode;
- rasterization rule;
- deterministic pixel coverage/depth rule.

No view-specific geometry edits.

### Stage D — native 96x96 evidence

Minimum representative views:

- exact profile;
- mild 3Q;
- strong 3Q;
- near-front;
- exact front.

Optional rear/3Q may be added only if it helps diagnose source orientation, not to rescue a failing front/profile result.

For each view preserve:

1. native 96x96 flat structural raster;
2. nearest-neighbour diagnostic enlargement;
3. source-space view metadata;
4. occupied-pixel / connected-component / bounding-box metrics;
5. deterministic rerender equality.

## 5. Primary perceptual acceptance dimensions

Mechanical metrics are secondary. Direct native-scale review owns the main decision.

Evaluate:

- `CAT_ID`: does the body read as a cat without texture/fur/face-detail rescue?
- `HEAD_BODY`: does head/neck/chest/trunk relation remain feline, especially front/3Q?
- forequarter/chest mass hierarchy;
- abdominal tuck;
- pelvis/haunch mass hierarchy;
- forelimb emergence from shoulder/chest;
- hindlimb emergence from pelvis/haunch;
- paw scale/placement readability;
- tail-root plausibility;
- front-view collapse or columnization;
- silhouette stability across yaw;
- 96x96 pixel readability.

## 6. Appearance firewall

The primary structural gate must not depend on:

- fur strands;
- coat texture or pattern;
- eye color;
- whiskers;
- facial markings;
- lighting drama;
- shadows;
- normal maps;
- specular cues;
- expression;
- post-process outlines;
- hand-pixel correction.

Ears may remain because they are actual geometry, but an ear-neutralized diagnostic is required if CAT_ID appears suspiciously ear-dependent.

## 7. Geometry/authoring firewall

Before the first direct review, forbidden:

- retopology;
- subdivision added for visual rescue;
- decimation for visual rescue;
- sculpting;
- vertex edits;
- silhouette correction;
- limb repositioning;
- head scaling;
- tail relocation;
- camera-per-view scale fitting beyond the frozen common framing rule;
- view-specific cropping;
- view-specific projection parameters;
- 2D paintover;
- per-view masks.

A global rigid transform, uniform scale and common ground alignment are allowed only to establish a consistent coordinate frame.

## 8. Projection order

Primary discriminator: **orthographic**.

Reason: orthographic projection isolates source morphology and yaw continuity without perspective-distance tuning as a rescue variable.

Weak perspective may be tested only after orthographic evidence is preserved, and only as a secondary diagnostic.

## 9. Relation to canonical Mobi semantics

This experiment does not transfer canonical physical ownership to the public mesh.

Private canonical truths such as BODY_ROOT, paw/contact semantics, support set, anatomical L/R, continuous orientation, MorphologyVectorV01 and six external visible domains remain unchanged.

This group asks only whether a 3D feline visible-form source is worth further change-control consideration.

## 10. Relation to Adult Walk Density

The closed Adult Walk Density result is not reopened.

- D24/F24, D36/F16 and D36/F24 remain the retained authored-pixel walk bracket.
- This 3D experiment does not choose among them.
- No walk cycle is rendered here.

The two representation paths are alternative feasibility evidence until private canonical change control selects or rejects a family.

## 11. Hard stops

Stop the group before rigging/compression if any of the following is true:

1. exact source/license cannot be frozen;
2. raw mesh cannot be acquired reproducibly;
3. mesh is malformed enough that basic projection requires artistic repair;
4. native 96x96 profile is materially non-feline;
5. native 96x96 3Q loses feline mass hierarchy;
6. exact front collapses into a generic vertical/columnar quadruped organization;
7. CAT_ID requires coat/face/fur/shading rescue;
8. common projection/framing cannot cover representative views without per-view fitting.

Mechanical success may not override a perceptual hard fail.

## 12. Success boundary

A Stage D PASS means only:

> an already-authored CC0 domestic-cat 3D morphology can survive representative 96x96 projection strongly enough to justify a *separate* next experiment on structural reduction / semantic parameterization.

It does **not** adopt:

- 3D runtime rendering;
- the Innerscene asset as Mobi production art;
- its topology as canonical topology;
- its pose as canonical pose;
- a rigging system;
- a generative model;
- all-direction rendering;
- all growth stages.

## 13. Next experiment after PASS only

If and only if Stage D passes, open a new bounded question:

> Which parts of the successful mesh actually carry native-scale feline identity, and can those be reduced from full vertices → silhouette-relevant structure → semantic landmarks/curves/sections → low-dimensional deformation parameters without losing the evidence?

That is where the proposed mathematical/generative-cat direction begins.
