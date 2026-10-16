# Mobi P1-C-R11 — Stage-0 Implementation Freeze

Date: 2026-10-16
Status: **FROZEN / PRE-EVIDENCE / NO ACTIONS RUN**
Freeze token: **`R11_STAGE0_IMPLEMENTATION_FREEZE`**
Public repository: `hotmoral/-`
Public branch: `mobi/run-p1-c-r11-semantic-scaffold-20261016`
R10 public base HEAD: `a2138902b1070bc2d9ecb54c7e5d08efecbda1d2`
R11 Stage-0 implementation commit: `176bbb42b06e49c216ecd2f6de9d16e12feaa709`

## 1. Scope

This record freezes the executable hypothesis for R11 Stage 1 **before any R11 public Actions evidence run**. It does not report scaffold success, does not authorize finite pose deformation, and does not authorize animation/gait production.

The neutral visible-form owner remains `R10_QUALITY_HEADROOM_V3125_F6246`. The internal scaffold is invisible control metadata and may not alter the accepted neutral surface or canonical semantic/contact state.

## 2. Immutable implementation identity

The assembled R11 implementation bytes are frozen as:

- assembled file: `mobi/p1-b2/geometry/p1_c_r11_semantic_scaffold_v1.py`
- byte count: `37,871`
- SHA-256: `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`

To avoid transport/reassembly drift, the public branch stores those exact bytes as seven ordered UTF-8/ASCII fragments under `mobi/p1-b2/geometry/r11_stage0_parts/`. `assemble_p1_c_r11_semantic_scaffold_v1.sh` concatenates them in lexical order, then hard-checks both byte count and SHA-256 before any Python execution.

Committed implementation blobs:

- workflow `.github/workflows/mobi-p1-c-r11-semantic-scaffold.yml` — `0bd5e0444bb01625917a18eaa255d9e0fe27cfef`
- assembler `assemble_p1_c_r11_semantic_scaffold_v1.sh` — `7a5c4bda8131fcbfc1ef301c70c64d423bf5c04f`
- synthetic tests `test_p1_c_r11_semantic_scaffold_v1.py` — `868a9cf58a32fdf725fe79c0d34d2cc77cb3c7aa`
- part000 — `8e4c430cf405c0b1c05dcad591a7c73e6bb143db`
- part001 — `86d3651e1b115c9bbfcedddbe0b42b0ac95f91c1`
- part002 — `b514eaca8a1af556509d719411ccf679c6eacabb`
- part003 — `8e9c9798de55bde7099971e6a868c98b65f377cf`
- part004 — `a09ae537bdec38534adc63882854f4fac3ae9e50`
- part005 — `db9dd42cb562ce23049cb32ca6cda6728e159b10`
- part006 — `10449747ebebb1a96298427d8e570675d3c4e2a9`

The companion `P1_C_R11_STAGE0_IDENTITY.json` is the machine-readable blob gate consumed by the workflow.

## 3. Exact R10/V3125 reproduction identity

Frozen source and inherited implementation:

- Innerscene `Standing cat`, `cat-original.glb`
- source SHA-256: `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- structural node: `Cat continuous body`
- source topology: `99,642 V / 199,280 F`
- inherited R10 reducer blob: `f281aad3e3a6c740c38c0a3f015718996dc45157`
- inherited Stage-D raster blob: `5c8820fb7270e7727ececb1bb37d3a24331b24ab`
- inherited Stage-B GLB inspector blob: `9b7899bc1c39d02291813a826df01d3697192846`
- `agg = 7.0`
- lowest simplification target used to create collapse stream: `1556` faces
- replay collapse-prefix length: `96,517`
- required replay result: exactly `3,125 V / 6,246 F`

V3125 mesh-array serialization is frozen exactly as the private contract requires:

1. ASCII `MOBI_R11_MESH_V1\0`;
2. little-endian unsigned-64 `(vertex_count, face_count)`;
3. C-contiguous little-endian float64 vertices `(3125,3)`;
4. C-contiguous little-endian int32 faces `(6246,3)`;
5. SHA-256 over the concatenation.

The accepted R10 artifact did not preserve reduced arrays as an authoritative file. Therefore Stage 0 freezes the exact reproduction implementation and hash serialization, and the workflow performs a **V3125 identity-only prelude under `PYTHONHASHSEED=1` and `777` before any scaffold extraction**. Both identities must be byte-identical and exactly `3125/6246`; the resulting `meshArraySha256` is the execution input identity. If the two seeds disagree or the topology differs, execution stops before voxelization. No scaffold parameter depends on the resulting hash value.

This identity prelude is not allowed to tune, inspect, or alter any Stage-1 structural constant.

## 4. Frozen environment

- runner family: GitHub hosted `ubuntu-latest`
- Python: exactly `3.12.15`
- `numpy==2.5.4`
- `fast-simplification==0.2.0`
- `trimesh==4.11.1`
- `scikit-image==0.26.0`
- `scipy==1.17.0`

Versions are checked at runtime and drift is a hard stop.

## 5. Frame/sign hard gate

V3125 arrays stay in `R10_SOURCE_FRAME`:

- `+Y_R10` = up
- `+Z_R10` = anatomical front
- `X_R10` = bilateral axis

Canonical `B3_SEMANTIC_FRAME` remains:

- `+X_B3` = forward
- `+Y_B3` = up
- `+Z_B3` = anatomical left

Frozen mapping candidate:

```text
x_B3 = z_R10
y_B3 = y_R10
z_B3 = x_R10
```

Mechanical sign procedure is frozen to the inherited Stage-D projection convention. At yaw `0°`, screen-right is `+X_R10` while the camera is on `+Z_R10` facing the animal; for a front-facing animal, viewer-right is anatomical-left. The implementation independently probes the frozen projection function and requires `+X_R10` to move screen-right at yaw `0°` and `+Z_R10` to move screen-right at yaw `90°`.

If this audit does not establish `+X_R10 = anatomical left`, execution **STOPs with change control**. No silent sign flip or post-result L/R relabel is permitted.

## 6. Surface-anchor derivation

All bind coordinates are re-derived from V3125; no legacy numeric coordinates are imported.

Frozen surface-anchor rules:

- body bounds use exact V3125 AABB;
- head candidate region: `y >= ymin + 0.55*bodyHeight` and `z >= zmin + 0.65*bodyLength`; anchor = arithmetic mean of candidates;
- tail-tip candidate region: `z <= zmin + 0.05*bodyLength`; anchor = arithmetic mean;
- body midplanes: AABB center `xmid`, `zmid`;
- fore/hind split: `z >= zmid` / `z < zmid`;
- left/right split: `x >= xmid` / `x < xmid`, using the frame hard-gate result that `+X_R10` is anatomical-left;
- in each paw quadrant, find minimum `y`; paw candidate set is within `0.035*bodyHeight` above that minimum; anchor = arithmetic mean.

Surface anchors are snapped to the nearest medial-graph node by squared Euclidean distance with lexicographic graph-node tie-break.

Allowed provenance classes remain only `CANONICAL_ID_VISUAL_BIND` and `SOURCE_DERIVED_INTERNAL`. Visual binds never write back into canonical physics/contact state.

## 7. Voxelization / medial graph

Frozen volumetric constants:

- isotropic pitch = `bodyHeight / 192`
- voxelizer: `trimesh.Trimesh(process=False, validate=False).voxelized(...)`
- voxel method: `subdivide`
- closed-body fill: `holes`
- zero padding: `4` voxels on every side
- thinning: `skimage.morphology.skeletonize(method='lee')`
- graph connectivity: full deterministic `26`-neighbour connectivity
- edge length: `pitch * sqrt(di^2 + dj^2 + dk^2)`
- graph nodes and neighbours always lexicographically sorted before tie-sensitive operations.

No manual branch creation or repair is permitted.

## 8. Branch pruning / semantic paths

Protected nodes are snapped `HEAD`, four paw anchors, and `TAIL_TIP`.

Terminal pruning is iterative and frozen:

- only degree-1 terminal chains are candidates;
- prune if chain length `< 0.035 * bodyHeight`;
- never prune a chain containing a protected node;
- remove terminal nodes up to, but not including, the first surviving junction;
- repeat until no eligible chain remains.

Shortest paths use deterministic Dijkstra with lexicographic predecessor tie-break at `1e-15` distance tolerance.

Semantic junction selection:

- `FOREQUARTER`: common node of head→left-fore-paw and head→right-fore-paw paths minimizing summed graph distance to both fore paws; lexicographic tie-break;
- `PELVIS`: analogous common node for both hind paws;
- `TAIL_ROOT`: first common node, by graph distance from tail tip, between tail→head and pelvis→head paths.

Required frozen paths are then shortest deterministic paths:

- `PELVIS → FOREQUARTER`
- `FOREQUARTER → HEAD`
- `FOREQUARTER → FORE_L_PAW`
- `FOREQUARTER → FORE_R_PAW`
- `PELVIS → HIND_L_PAW`
- `PELVIS → HIND_R_PAW`
- `TAIL_ROOT → TAIL_TIP`

Failure to resolve any path deterministically is a hypothesis fail; do not repair manually.

## 9. Exact 30 controls and placement

The contract's exact 30-role hierarchy is encoded unchanged. The count, names and parentage may not change after evidence.

Path processing is frozen:

- arc-length resample: `129` samples;
- smoothing: `2` passes of binomial kernel `[1,4,6,4,1]/16`, preserving endpoints;
- curvature score: angle between two-sample chords;
- accepted curvature extremum: `>= 0.12 rad`;
- selected extrema separated by at least `0.12` path-fraction;
- endpoint guard: `[0.08, 0.92]` path-fraction;
- extrema selection order: descending curvature, then sample index;
- selected controls are finally ordered by path fraction.

If insufficient separated extrema exist, the **entire role set for that path request** uses predeclared arc-length fallback quantiles:

- LUMBAR: `0.50`
- NECK_BASE: `0.55`
- each FORE chain: `0.12 / 0.32 / 0.58 / 0.82`
- each HIND chain: `0.18 / 0.50 / 0.80`
- TAIL internal controls: `0.20 / 0.40 / 0.60 / 0.80`

`BODY_ROOT_CTRL` is fixed at `0.50` of the pelvis→forequarter path. Paw and tail-tip controls use path endpoints. `PELVIS_CTRL`, `FOREQUARTER_CTRL`, `HEAD_CTRL`, and `TAIL_ROOT_CTRL` use their deterministic semantic graph nodes.

## 10. Six-domain derivation

External visible domains remain exactly:

`CORE / FORE_L / FORE_R / HIND_L / HIND_R / TAIL`.

Domain carrier polylines are the frozen semantic paths. For every V3125 vertex, closest polyline distance and arc fraction are computed segment-wise with earlier arc-fraction tie-break.

Frozen gates:

- midline CORE band: `0.5 * pitch` around AABB center X; fore/hind L/R child candidates are disabled inside this band;
- outside the band, only same-side fore and hind child candidates are considered;
- TAIL is always a child candidate;
- a child wins only if `childDistance + 0.5*pitch < coreDistance`;
- otherwise domain = CORE;
- child root-interface eligibility requires child arc fraction `<= 0.22` and `(coreDistance - childDistance) <= 3.0*pitch`.

No seventh domain exists.

## 11. Weight field

Allowed roles are strictly same-domain roles. At a child root interface only, CORE roles are additionally eligible.

For each eligible role:

```text
rawWeight = 1 / (distance^2 + sigma^2)
sigma = 2.0 * pitch
```

Frozen truncation/tie rule:

1. sort by descending raw weight;
2. exact ties by frozen role ordinal;
3. retain at most `4` influences;
4. float64 renormalize to sum 1.

Hard audit:

- finite;
- nonnegative;
- per-vertex sum error `<= 1e-12`;
- max four influences;
- zero unweighted vertices;
- no role outside the domain/interface whitelist.

Weight serialization is frozen:

1. ASCII `MOBI_R11_WEIGHTS_V1\0`;
2. little-endian `u64 vertex_count` + `u32 control_count`;
3. C-order `(N,4)` uint8 role indices, `255` for empty;
4. C-order `(N,4)` little-endian float64 weights.

## 12. Diagnostic deformation / Jacobian

Rest evaluator is deterministic float64 LBS identity only; it is not a production skinning decision.

Neutral limits remain:

- max normalized rest displacement `<= 1e-9`;
- RMS normalized rest displacement `<= 1e-10`.

Jacobian probe:

- rotation epsilon: `1e-6 rad`;
- tangent = role minus parent bind (global root uses first child direction if needed);
- choose Cartesian basis least aligned with tangent; ties follow NumPy basis order X/Y/Z;
- diagnostic axis = normalized tangent × chosen basis;
- normalized derivative support threshold: `> 1e-10`.

Every non-global control must have nonzero support. Non-CORE controls may support only their matching external child domain. Paw terminals must have some support within `4*pitch` of their paw bind. Tail controls must have strictly increasing weighted support arc centroids from root to tip and every adjacent tail-control support set must overlap.

A failure is a Stage-1 falsifier, not a reason to retune weights or controls.

## 13. Raster identity

Raster implementation is inherited byte-for-byte from Stage D blob `5c8820fb7270e7727ececb1bb37d3a24331b24ab`.

Frozen neutral regression:

- primary yaws: `0 / 22.5 / 45 / 67.5 / 90°`;
- full yaw sweep: `0..90°` inclusive every `2.5°`, exactly 37 samples;
- binary 96×96 masks;
- rest result must be byte-identical to reproduced V3125 baseline at every yaw;
- exact front (`0°`) remains a separately named/reportable result;
- no per-view correction, recentering or weight field.

Primary baseline/rest/XOR PNGs use the inherited deterministic Stage-D PNG writer.

## 14. Evidence serialization and determinism

Stable JSON uses UTF-8, `sort_keys=True`, indent 2 and final newline. Evidence outputs include medial graph, semantic paths, scaffold roles/positions/provenance, domains/interfaces, binary weights, weight audit, Jacobian report, all-yaw raster identity, five primary PNG triplets, summary and SHA-256 manifest.

Full Stage-1 execution, if separately authorized later, runs under `PYTHONHASHSEED=1` and `777`; the two evidence trees must be byte-identical (`diff -qr` empty).

## 15. Anti-copy / anti-fitting firewall

Executable R11 work does not acquire or parse CatPilot, walking static meshes or sitting static meshes. It imports none of their morphology, coordinates, hierarchy, weights or timing.

After this freeze, forbidden without explicit new change control:

- changing voxel resolution/fill/thinning;
- changing anchor regions or sign conventions;
- changing graph connectivity/pruning/ties;
- changing semantic junction/path rules;
- changing active control count, names or parentage;
- changing smoothing/curvature/fallback quantiles;
- changing domain gates;
- changing weight kernel, truncation or normalization;
- moving controls because a diagnostic looks poor;
- manual graph or weight repair;
- view/action-specific geometry, rig or weights;
- any neutral V3125 geometry edit.

## 16. Public workflow trigger boundary

The R11 workflow has **only** `workflow_dispatch`. There is no `push`, `pull_request`, `schedule` or other automatic trigger.

Even manual dispatch is gated by both:

- exact branch `mobi/run-p1-c-r11-semantic-scaffold-20261016`;
- exact input token `RUN_R11_STAGE1_AFTER_STAGE0_FREEZE`.

The workflow also requires this freeze token/file and the machine-readable identity file before any executable step can proceed.

At the time this freeze record is authored, R11 Actions run count on the branch is **zero**. The freeze commit itself must not trigger a run.

## 17. Stage-0 synthetic verification already performed

Before public freeze, local result-blind tests passed for:

- exact 30-role count/domain split/hierarchy acyclicity;
- mesh-array hash determinism and order sensitivity;
- deterministic shortest-path tie handling;
- protected-anchor pruning;
- predeclared curvature fallback;
- six-domain weight gating without cross-side bleed;
- deterministic weight serialization;
- neutral LBS identity.

These synthetic tests do not contain V3125 scaffold evidence and do not imply R11 Stage-1 PASS.

## 18. Stop boundary

This freeze makes the implementation immutable for the first R11 evidence attempt. It does **not** itself authorize that attempt.

After this commit, verify:

1. public branch HEAD and blob identities;
2. workflow trigger scope is dispatch-only;
3. no Actions run was created by implementation/freeze commits;
4. private canonical STATUS/HANDOFF record this Stage-0 closure.

Then STOP. A Stage-1 public evidence run requires a separate explicit execution decision.
