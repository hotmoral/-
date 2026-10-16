# Mobi P1-C — Post-R10 Rigged Cat Motion Reference Final Result

Date: 2026-10-16
Status: **CLOSED / PASS AS MOTION-STRUCTURE EVIDENCE ONLY**
Public branch: `mobi/experiment-rigged-cat-motion-reference-20261016`
Accepted execution HEAD: `dd726f44aba9e51e8cbffc12cf88599481b2d77b`

## 1. Question

Can a real rigged cat source demonstrate the exact structural property needed for later pose mathematics:

> one fixed mesh topology whose same vertex identities are continuously deformed through different locomotion poses by a bone hierarchy and skin weights?

This audit does **not** ask whether the candidate cat morphology is suitable for Mobi.

## 2. Frozen source

Source:

- provider: OpenGameArt
- asset: `Cat Pilot (Rigged + Animated)` by Tomcat94
- file: `CatPilot.blend`
- provider page checked for CC0 / public-domain status and stated rig/animation availability
- bytes: `6,612,348`
- SHA-256: `c8506dada39953517b86ce28fa4c5d9c4867d375782f5c99e84392f6be1ea7d0`

The source is used as **motion/deformation reference only**.

Its stylized proportions, mesh, bone positions and authoring choices are not adopted as Mobi morphology or canonical physics.

## 3. Execution history

### Run 1 — harness failure, preserved

- run `38901937983`
- job `116976047015`
- result: FAILURE

Source acquisition and Blender installation succeeded, but Blender's default Python-script failure behavior did not propagate a nonzero exit code. The workflow reached a later missing-output comparison.

No scientific conclusion was drawn.

### Run 2 — dependency failure, preserved

- run `38902155033`
- job `116976765935`
- result: FAILURE

The hardened harness correctly exposed:

`ModuleNotFoundError: No module named 'numpy'`

This was an audit-environment dependency failure, not a rig/source failure.

### Run 3 — accepted

- run `38902595447` — **SUCCESS**
- job `116978225103`
- accepted HEAD `dd726f44aba9e51e8cbffc12cf88599481b2d77b`
- artifact `12046946948`
- artifact digest `sha256:cd32ef15724135792167ffcd2a27defe43cfd70c557a7ce93d1d0f5ab31f7a53`
- Blender `4.0.2`
- seed 1 / seed 777 evidence: byte-identical

The accepted script uses Blender's standard Python only; no external numeric package is required.

## 4. Exact accepted primary-mesh result

The final artifact JSON is authoritative over earlier console-level exploratory summaries.

Primary armature-bound cat mesh:

- object: `CatPilot`
- base vertices: **860**
- base polygons: **881**
- base/evaluated topology SHA-256: `55a5dd9dc41ddd1ac831a265dca08e5fb35cb55ca79bfbed70db089b1abd96b9`
- vertex groups: **42**
- groups with at least one weighted vertex: **38**
- armature object: `Armature`

Armature:

- bones: **46**

This final evidence supersedes any earlier transient console summary with different counts.

## 5. Motion-relevant hierarchy observed

The source contains a clear feline-like kinematic organization, including:

### Axial chain

`Root -> Hip -> Stomach -> Chest -> Neck -> Head`

### Tail chain

`Hip -> Tail1 -> Tail2 -> Tail3 -> Tail4 -> Tail5 -> Tail6`

### Forelimb chains

Left/right:

`Chest -> Shoulder -> Humerous -> Forearm -> Hand`

### Hindlimb chains

Left/right:

`Hip -> Thigh -> Shin -> Foot -> Toes`

with `Heel` branches and separate IK/control helpers.

The source also contains non-Mobi/decorative/control structures such as ears, goggles, scarf and pointer/IK bones.

Therefore the full 46-bone set is **not** a candidate Mobi skeleton count.

## 6. Skin-weight evidence

The primary mesh has actual nonzero weighted regions for the main body chains.

Examples:

- `Head`: 333 weighted vertices
- `Shoulder.L/R`: 131 / 132
- `Hip`: 96
- `Chest`: 75
- `Neck`: 72
- `Thigh.L/R`: 65 / 64
- `Shin.L/R`: 42 / 42
- `Humerous.L/R`: 31 / 32
- `Forearm.L/R`: 24 / 24
- `Hand.L/R`: 30 / 30
- `Foot.L/R`: 26 / 26
- `Tail1..6`: distributed weighted sets along the tail

Control/helper groups such as `Root`, `TailIK`, `LegPointer.L/R` have zero weighted vertices in the accepted artifact; `ArmPointer.L/R` carry only a negligible single-vertex weight.

This distinction is why control/helper bones must not be mechanically copied into a future semantic scaffold.

## 7. Fixed-topology locomotion result

### Run action

Source action frame range: `0..55`.

Sampled frames:

`0 / 14 / 28 / 41 / 55`

At every sampled frame:

- vertex count = **860**
- polygon count = **881**
- topology hash = exactly the same `55a5dd9d...96b9`

Direct same-vertex correspondence across sampled frames:

> **PASS**

The final frame returns exactly to the sampled starting mesh coordinates.

Non-rigid deformation remains substantial after removing centroid translation. The largest sampled run deformation occurs at frame 14:

- median normalized displacement: `0.03875`
- p90: `0.15415`
- p95: `0.19795`
- p99: `0.27246`
- max: `0.32488`
- RMS: `0.08208`

Normalization is by target bounding-box diagonal.

### Walk action

Source action frame range: `0..80`.

Sampled frames:

`0 / 20 / 40 / 60 / 80`

At every sampled frame:

- vertex count = **860**
- polygon count = **881**
- topology hash = unchanged

Direct same-vertex correspondence:

> **PASS**

The final frame again returns exactly to the sampled starting mesh coordinates.

Largest sampled walk deformation occurs at frame 20 after centroid translation removal:

- median normalized displacement: `0.01779`
- p90: `0.10368`
- p95: `0.14497`
- p99: `0.20215`
- max: `0.21210`
- RMS: `0.05624`

These are real pose-dependent surface deformations of the same indexed vertices, not separate pose meshes.

## 8. WalkBlink qualifier

The name-based audit also sampled `WalkBlink` because its name contains `walk`.

For the selected armature-bound primary mesh it produced zero evaluated vertex displacement across the sampled frames.

It is therefore not used as locomotion evidence.

The positive motion result rests on the nonzero `Walk` and `Run` actions.

## 9. Scientific conclusion

The audit demonstrates:

> **A cat-like articulated body can be represented as one fixed surface topology plus a hierarchical bone/control structure, skin weights and time-varying pose parameters, while preserving direct vertex identity through materially different locomotion poses.**

Final token:

> **`FIXED_TOPOLOGY_RIGGED_MOTION_REFERENCE_AVAILABLE`**

This directly supports the feasibility of the mathematical separation discussed with the Product Owner:

`morphology M + pose P(t) -> deformed surface V(t)`.

It does **not** prove that CatPilot's particular skeleton, proportions, weights or 860-vertex mesh should be used by Mobi.

## 10. Consequence for Mobi

The clean next research architecture is now evidence-supported:

1. retain `R10_QUALITY_HEADROOM_V3125_F6246` as Mobi's current successful visible-form/morphology regression reference;
2. treat rigged-source bone hierarchy / weighted deformation as motion-structure evidence only;
3. derive a Mobi-specific semantic scaffold from canonical Mobi roots, paws, contact semantics and the R10 feline surface;
4. regress that scaffold against the 3,125-vertex morphology before any animation claim;
5. only after neutral structure passes, test pose deformation against real feline-motion evidence.

## 11. Prohibited inference

Do not infer from this PASS that:

- 46 bones are required for Mobi;
- CatPilot's bone locations are anatomically optimal;
- CatPilot's stylized body is a valid Mobi morphology source;
- its weights may be copied unchanged onto the R10 mesh;
- Mobi walking is solved;
- arbitrary sitting/lying/jumping poses are solved;
- a final generative mathematical cat has been established.

## 12. Next private change-control question

> Can the R10 3,125-vertex feline morphology be equipped with a **bounded, Mobi-semantic, pose-ready structural scaffold** whose controls are derived from the successful surface and canonical semantic anchors, while using rigged-cat evidence only to constrain the kinds of articulated chains and deformation behavior that must be representable?
