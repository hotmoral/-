# Mobi P1-C — Public 3D Cat Projection Feasibility Handoff

Date: 2026-10-16
Status: **GROUP CLOSED / PUBLIC FEASIBILITY PASS / PRIVATE IMPORT NOT DONE**
Public repo: `hotmoral/-`
Public branch: `mobi/experiment-3d-cat-projection-feasibility-20261016`
Pre-handoff documentation HEAD: `480484a88f454b5056e64ccdb131030997b3e260`

## 1. Recovery rule

A new session must first resolve the branch remote HEAD, then read in this order:

1. `P1_C_3D_CAT_SOURCE_LICENSE_REVIEW.md`
2. `P1_C_3D_CAT_96PX_PROJECTION_FEASIBILITY_CONTRACT.md`
3. `P1_C_3D_CAT_STAGE_B_INSPECTION_RESULT.md`
4. `P1_C_3D_CAT_STAGE_B_CONSISTENCY_REVIEW.md`
5. `P1_C_3D_CAT_STAGE_C_PROJECTION_SETUP_FREEZE.md`
6. `P1_C_3D_CAT_STAGE_D_DIRECT_VISUAL_REVIEW.md`
7. `P1_C_3D_CAT_96PX_PROJECTION_FINAL_RESULT.md`
8. `P1_C_3D_CAT_96PX_PROJECTION_CONSISTENCY_REVIEW.md`
9. this handoff.

Read the prior post-R9 authored-pixel / Adult Walk Density handoffs only when reconstructing alternative representation history.

## 2. Entry baseline

This branch was created from:

`5fb9352b9f67c638c461b6c3d1bad99583aa5966`

which was the Adult Walk Density branch plus the 3D-exploration delta handoff.

Private canonical remained:

- repo: `hotmoral/Mobi`
- branch: `p1-motion-morphology-foundation`
- last recovered HEAD before this public group: `028f9a2c015d7f5a0c535a04d51a159c716c32f0`

No private canonical import has occurred in this group.

## 3. Primary source

Selected feasibility source:

- Innerscene `Standing cat`
- file: `cat-original.glb`
- CC0 / public domain
- bytes: 4,903,420
- SHA-256: `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`

Backups identified but not needed for this group:

- Innerscene `Domestic cat walking`
- Innerscene `Domestic cat sitting`

Low-poly Quaternius remains only a possible style/detail control.

## 4. Stage B structural finding

The source contains 19 meshes, but the structural feline body is cleanly isolated as:

`Cat continuous body`

- 99,642 vertices
- 199,280 triangles
- 1 connected component
- closed orientable index topology
- V/E/F = 99,642 / 298,920 / 199,280
- boundary edges 0
- non-manifold edges 0
- orientation mismatch edges 0
- degenerate index triangles 0
- duplicate triangles 0
- Euler characteristic 2

The other 18 meshes are eyes/glints/inner-ear patches/mouth/muzzle/nose/pupils/whiskers and were excluded from the structural gate.

No skin, animation, morph target or texture dependency exists.

## 5. Stage B evidence identity

Main inspection:

- run `38893007226` — SUCCESS
- job `116946790029`
- execution HEAD `ec1105ce6cf6512f531ef409433452b6af4ced5d`
- artifact `12041969360`
- digest `sha256:2dbb79061d20561cfdeb1e8070e82c8bbf296bac3a3a6a7455281b2092fb30ac`

Topology diagnostic:

- run `38893431641` — SUCCESS
- job `116948154143`
- execution HEAD `37629e1c1da6de95122f7450bf096f38fd0ac791`
- artifact `12043245096`
- digest `sha256:91d671433218a8affd2f754915207b9612628d56682cb266dd12b52be94d93d1`

The topology run independently reacquired the exact same source hash.

## 6. Frozen Stage C projection identity

Primary geometry:

`Cat continuous body` only.

Frozen axes:

- +Y up
- +Z anatomical front
- X bilateral

Frozen representative yaw:

- 0° exact front
- 22.5° near front
- 45° strong 3Q
- 67.5° near profile
- 90° exact profile

Frozen output:

- orthographic
- one common center/floor/scale
- 96×96
- scale `111.37388017614773 px/m`
- binary pixel-center triangle-union silhouette
- no antialiasing / dilation / outline / per-view fitting / accessory rescue.

## 7. Stage D evidence identity

Projection run:

- run `38894114430` — SUCCESS
- job `116950377428`
- execution HEAD `075f99c318d156b265d63f9c3bfe9b98df6f1404`
- artifact `12043770156`
- digest `sha256:cc6b851671e2a4c489c78155aeefb9dd2f3cd85f64b8e059c02350fcd04ab8b0`
- seed 1 / 777 evidence byte-identical

Key evidence files:

- `P1C_3D_CAT_EXACT_FRONT_96.png`
- `P1C_3D_CAT_NEAR_FRONT_96.png`
- `P1C_3D_CAT_STRONG_3Q_96.png`
- `P1C_3D_CAT_NEAR_PROFILE_96.png`
- `P1C_3D_CAT_EXACT_PROFILE_96.png`
- corresponding `*_8X.png`
- `P1C_3D_CAT_VIEW_STRIP_96.png`
- `P1C_3D_CAT_VIEW_STRIP_96_8X.png`
- `summary.json`

## 8. Direct perceptual result

- exact profile: STRONG PASS for feasibility
- near profile: STRONG PASS
- 45° 3Q: PASS
- near front: PASS WITH CAUTION
- exact front: MARGINAL / BOUNDED PASS

Exact front remains the weak view because silhouette-only output loses interior depth and the raised tail/outer ears contribute materially. However it does not reproduce R9's narrow central column / generic long-leg collapse.

The body remains readable without eye/pupil/muzzle/nose/mouth/whisker/inner-ear-detail geometry.

## 9. Final decision

> **CLOSED / `PUBLIC_3D_CAT_96PX_PROJECTION_VIABILITY_DEMONSTRATED`**

Retained qualifier:

> **`EXACT_FRONT_REMAINS_THE_WEAKEST_VIEW_AND_MUST_NOT_BE_HIDDEN_BY_LATER_REDUCTION`**

This means only that mathematical reduction is worth studying.

It does not select this asset or 3D runtime for production.

## 10. Core new learning

The causal picture is now clearer:

- R9 showed stable continuous-to-pixel projection cannot rescue a generic source carrier.
- This group shows sufficiently feline pre-authored source morphology can survive hard 96px silhouette reduction.

Therefore the next productive mathematical question is no longer “can we invent a cat from a few curves?”

It is:

> **which geometric degrees of freedom in a known-successful cat source actually carry the native-scale feline signal, and how far can they be reduced without losing it?**

## 11. Recommended next governance step

Before starting a large reduction/generative implementation, resolve the accumulated public/private delta explicitly.

Private canonical currently predates:

1. public R9 Stage 1 closure;
2. authored-pixel feasibility analysis;
3. Adult Walk Density closure;
4. this successful 3D projection feasibility group.

Recommended next bounded governance group:

> **Private P1-C Post-R9/Public-Evidence Change-Control Import + Representation Decision Update**

That review should preserve both viable alternatives:

- sparse authored-pixel library remains experimentally open;
- 3D-source → projection → mathematical reduction is now experimentally promising.

Do not silently declare one production winner yet.

## 12. Next technical group after governance

Eligible but not started:

`P1-C 3D Morphology Reduction / Generative Parameterization Feasibility`

Recommended first question:

> Starting from the exact successful full mesh, how aggressively can geometry be reduced/re-expressed while retaining the frozen 96px regression views, especially exact-front HEAD_BODY?

The reduction ladder should proceed from source evidence downward, not from a low-order formula upward.

## 13. Hard non-goals still in force

Do not yet:

- rig/walk the source;
- build 24/36 directions;
- build four growth stages;
- adopt this source as final Mobi art;
- implement Android 3D runtime;
- infer canonical paw/contact data from source vertices;
- jump directly to a generative neural/parametric model;
- tune a reduced model indefinitely after evidence;
- reopen R2–R9 procedural-carrier tuning.
