# Mobi P1-C — Post-R9 3D Mesh Exploration Delta Handoff

Date: 2026-10-16
Status: SESSION-BOUNDARY DELTA ONLY — NO 3D IMPLEMENTATION STARTED
Public execution host: hotmoral/-
Current branch: mobi/experiment-adult-walk-density-20261016

## 1. Closed group immediately before this delta

The bounded Adult Walk Density experiment is CLOSED.

Canonical public result for that group:
- branch: `mobi/experiment-adult-walk-density-20261016`
- prior handoff HEAD: `4636418ff734e658618315b0eb6eccf62f55ae49`
- main density workflow: SUCCESS
- exact direction half-step diagnostic: SUCCESS
- result: `CLOSED / ADULT_WALK_AUTHORED_PIXEL_DENSITY_BRACKET_ESTABLISHED`
- next experimental bracket retained for real authored-quality comparison: D24/F24, D36/F16, D36/F24
- D12 and F12 pruned; F32 not adopted as default because marginal temporal gain was smaller than directional gain

No later discussion changes or reopens this closed density result.

## 2. New direction discussed after the closed group

A new representation possibility was explored conceptually only:

> use an existing public 3D cat mesh as body truth, then project/rasterize it to 2D/native pixel output instead of procedurally inventing feline morphology from scratch.

Potential pipeline discussed:

`public cat 3D mesh -> inspect vertices/topology -> optional skeleton/rig -> pose/orientation -> orthographic or perspective 3D-to-2D projection -> 96x96 native raster/pixel output`

This is materially different from R4-R9 attempts because the feline 3D morphology could come from an already-authored cat mesh rather than being reconstructed from low-order procedural geometry.

## 3. Public 3D-source exploration

Publicly available source categories were identified conceptually:
- CC0/redistribution-safe static domestic-cat GLB meshes are the strongest first feasibility candidates.
- Rigged/animated public cats may be useful as motion/rig references, but individual licenses must be checked before any canonical/public reuse.
- SMAL is a relevant research example of a parametric/skinned animal model, but its research/noncommercial licensing means it must NOT be treated as the default production asset for Mobi without a separate license decision.
- anatomy/scan datasets may be useful as morphology evidence, not automatically as runtime assets.

No external 3D asset has yet been committed, mirrored, modified, or adopted by Mobi.

## 4. Relationship to the uploaded 8,810-function trace

The user supplied two local reference files during discussion:
- `cat_function_trace_8810_segments.json`
- `cat_function_trace_8810_equations.txt`

Observed semantics from those files:
- reference canvas: 1448x1086
- 44 contour groups
- 8,810 parametric linear segment functions
- 17,620 scalar coordinate functions counting x/y separately
- each segment is `x(t)=x0+dx*t`, `y(t)=y0+dy*t`, `0<=t<=1`
- binary silhouette validation against the source reports IoU 1.0 / different pixels 0

Interpretation frozen for handoff:

This trace is **mathematical transcription of one finished 2D shape**, not yet a compact generative cat model. Most of the 8,810 functions encode contour fidelity rather than feline semantic degrees of freedom.

Three conceptual representation levels were distinguished:

A. `Mathematical trace`
- finished image -> many line equations
- exact reproduction of a particular 2D shape

B. `Deformable mathematical drawing`
- semantic curves/control structures derived from a reference shape
- curves move according to pose/time/orientation rules

C. `Generative cat model`
- compact parameters such as growth, morphology, action phase, pose/orientation drive an entire 3D/2D cat representation

The 8,810-function trace is Level A. It may provide reference evidence or raw material for Level B, but it does not by itself prove Level C.

## 5. 3D coordinates and mathematical generation

Discussion conclusion:

If a public 3D cat mesh exposes vertices/faces, then the body is already mathematically defined as:

`V = {(x_i,y_i,z_i)}`
`F = {(i,j,k), ...}`

That is sufficient to reconstruct, rotate, pose if rigged, project to 2D, and rasterize the cat.

However, storing all raw vertices is best described as a coordinate-defined 3D model, not yet a highly compressed generative equation system.

A later reduction path could be:

`full mesh -> silhouette-relevant structure / landmarks / sections / skeleton -> deformable controls -> low-dimensional parameters`

Potential eventual model form:

`v_i = v_i(growth, morphology, pose, action_phase, orientation)`

or a lower-dimensional semantic representation that reconstructs the required mesh/silhouette.

## 6. Key insight / hypothesis for next group

The next bounded feasibility group should NOT begin by designing another feline procedural body.

Instead test the cheaper hypothesis first:

> Does an already-authored, redistribution-safe public 3D domestic-cat mesh preserve convincing feline identity when rendered from representative orientations and reduced to native 96x96 output?

If this fails, there is little reason to invest in mesh compression/generative equations.

If this passes, only then analyze whether the full mesh can be reduced into a smaller mathematical/deformable representation without losing feline identity.

## 7. Recommended next bounded group

Suggested official group name:

`P1-C Public 3D Cat Mesh -> 96x96 Projection Feasibility`

Recommended scope:
1. identify 1-3 redistribution-safe public domestic-cat meshes with explicit license evidence;
2. freeze exact source identity/hash/license metadata;
3. inspect mesh dimensions, vertex/face counts, coordinate conventions, topology, pose, rig availability;
4. no retopology or artistic correction in the first discriminator;
5. render representative orientations, at minimum profile / weak 3Q / strong 3Q / front, preferably orthographic first;
6. reduce/rasterize to exact 96x96 native output with deterministic settings;
7. direct perceptual review for CAT_ID / HEAD_BODY / forequarter / haunch / limb emergence / view consistency;
8. measure silhouette/component/pixel stability as secondary evidence;
9. stop before walk animation, rig authoring, growth stages, texture/coat variants, or production integration.

Primary gate:
- Can the source mesh produce a convincing adult-cat body at native 96x96 across representative views **without decorative rescue**?

Secondary gate, only after primary PASS:
- Is the mesh structured enough to justify a later compression/deformable-math experiment?

## 8. Non-goals for next group

Do NOT yet:
- adopt a 3D runtime architecture;
- import a license-unclear mesh;
- build walk cycles;
- solve rigging comprehensively;
- solve all 24/36 directions;
- solve all four growth stages;
- compress vertices into equations before native-scale visual viability is demonstrated;
- claim the private Mobi canonical branch has adopted the 3D approach.

## 9. Canonical/private warning

The private `hotmoral/Mobi` repository remains canonical.

This public document is a session-boundary delta handoff only. It does NOT mean the private canonical representation contract has been changed. Any 3D approach that survives public feasibility must later go through private change-control / consistency review before adoption.

## 10. Recovery instruction for a new GPT session

On a new session:
1. recover private canonical Mobi state first from its canonical GitHub docs/HEAD;
2. then recover the public adult-walk-density branch and read the existing density result/consistency/handoff docs;
3. read this delta handoff;
4. do not restart R2-R9 tuning;
5. do not assume 3D has been adopted;
6. begin only the bounded public 3D-mesh-to-96x96 feasibility discriminator described above.
