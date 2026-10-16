# P1-C Post-R12 Tail-Root Degeneracy Observational Diagnostic — Result

Status: **CLOSED / STRUCTURAL DIAGNOSTIC PASS / CLASSIFICATION FROZEN**

Primary classification:

`COINCIDENT_BRANCH_ROOT_WITH_NONVACUOUS_TAIL_SUPPORT`

This result is intentionally narrow. It does **not** make R12 PASS, does not prove production-valid tail geometry, and does not prove natural finite-angle tail motion.

## 1. Product anchor

The governing Mobi objective remains unchanged:

> The body itself must read naturally as a cat from proportions, mass relationships, joints, silhouette and continuous orientation, before fur, texture, shading, facial detail, style or animation polish are added.

This diagnostic exists only to remove one structural uncertainty in the deformation scaffold. Mechanical evidence may inform the foundation but may never replace the product criterion.

## 2. Frozen public execution identity

Repository:

`hotmoral/-`

Frozen implementation branch:

`mobi/run-p1-c-post-r12-tail-root-diagnostic-20261017`

Frozen implementation/handoff HEAD:

`725d49dd4ebe25a70e97fe5f3101405d91012899`

Frozen evidence workflow Git blob:

`7c32f77fc04dcb8436bb704bdfc524b26357e85f`

Frozen evidence workflow SHA-256:

`e418f958cd83a740a6b51339e576ae6799754637ac99fc93283a4355764ebb0c`

Public-main registration:

- previous main: `d9c009185b7df8556598ae640be28da46e05b1ca`
- exact byte-identical registration commit: `afc81ce6ebe912404de80a2060393174e1ff37a4`
- registered blob remains `7c32f77fc04dcb8436bb704bdfc524b26357e85f`

One-shot relay:

- branch `mobi/ops-post-r12-tail-root-diagnostic-dispatch-20261017`
- relay commit `77e56e9e2425b9f0a3609ca36bd5dbf02d6ec965`
- relay run `38978421988`
- relay job `117233307339`
- conclusion `SUCCESS`
- dispatch response `HTTP 204`
- no retry performed.

Structural diagnostic run:

- run `38978429045`
- job `117233333508`
- event `workflow_dispatch`
- head `725d49dd4ebe25a70e97fe5f3101405d91012899`
- conclusion `SUCCESS`

Artifact:

- artifact ID `12080027358`
- name `mobi-p1-c-post-r12-tail-root-diagnostic-38978429045`
- size `2,965,501` bytes
- GitHub digest / independently downloaded ZIP SHA-256:
  `26353b064ad8042cb3a505818253c933cdd56d0a58831a90e915cc0a9b593df2`

## 3. Determinism and evidence integrity

Evidence manifest verification independently reproduced all listed hashes.

Key hashes:

- source GLB SHA-256:
  `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- diagnostic JSON SHA-256:
  `758f30665e24a98342ee5029bb0eb2fbcc9e233d3ecb3b3cdecd7341e06f0a27`
- seed 1 diagnostic JSON SHA-256:
  `758f30665e24a98342ee5029bb0eb2fbcc9e233d3ecb3b3cdecd7341e06f0a27`
- seed 777 diagnostic JSON SHA-256:
  `758f30665e24a98342ee5029bb0eb2fbcc9e233d3ecb3b3cdecd7341e06f0a27`
- deterministic diff SHA-256:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The two diagnostic JSON files are byte-identical.

Runtime:

- Python `3.12.15`
- NumPy `2.5.4`
- fast-simplification `0.2.0`
- trimesh `4.11.1`
- scikit-image `0.26.0`
- scipy `1.17.0`

Frozen identities reproduced:

- V3125 topology `3125 V / 6246 F`
- V3125 mesh-array SHA-256 `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`
- R11 assembled SHA-256 `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`
- R12 adapter SHA-256 `fc4096162607dbf59859749562ec5ab9ea7d0e09551aa7cd3cd1ad05e9f5594c`
- R12 adapter blob `837f4abe7ff474a527893b099be8087a104f7aaa`
- role count `30`
- mutation-free before/after diagnostic: `true`
- global weight-domain bleed count: `0`
- unweighted vertices: `0`
- maximum weight-sum absolute error: `2.220446049250313e-16`.

## 4. Hierarchy-edge audit

All `29` parent-child hierarchy edges were audited.

Known singular edge:

`PELVIS_CTRL -> TAIL_ROOT_CTRL`

Both coordinates are exactly:

`[0.0, 0.2925511774265033, -0.08581501204510761]`

Therefore:

- exact tuple equal: `true`
- edge length: `0.0`
- `<= 1e-15` diagnostic-degenerate: `true`.

Critically:

- additional diagnostic-degenerate edge count: `0`
- additional exact-coincident edge count: `0`.

Thus the observed zero-length hierarchy degeneracy is localized to the already known pelvis/tail-root edge rather than a broader collapsed hierarchy.

## 5. Medial-graph topology

`PELVIS_CTRL` and `TAIL_ROOT_CTRL` are:

- the same exact medial-graph node `[36, 78, 86]`;
- the same exact world coordinate;
- graph degree `3`;
- connected to the same three incident medial-graph neighbors.

The equality arises from two different frozen selection rules:

- pelvis: `pair_merge_node(HIND_L,HIND_R,closest_sum_to_hind_endpoints)`
- tail root: `first_merge_from_tail(tail_to_head,pelvis_to_head,minimum_tail_graph_distance)`.

This confirms the coincidence is an inherited consequence of the deterministic medial-graph derivation, not evidence of mutation during this diagnostic.

## 6. Tail path and control spacing

Frozen tail path:

- graph nodes: `106`
- arc length R10: `0.5226317484871421`
- arc length / pitch: `133.9846979299309`
- arc length / body height: `0.6978369683850567`.

The first path node after the coincident root is already distinct:

- path index `1`
- grid node `[37, 78, 85]`
- distance `0.005516397904063737`
- distance / pitch `1.414213562373101`.

There are no exact coordinate coincidences among the six tail controls themselves.

Consecutive control distances R10:

- root -> tail1: `0.08455559618696346`
- tail1 -> tail2: `0.06969087225163592`
- tail2 -> tail3: `0.13854934857558587`
- tail3 -> tail4: `0.09923280478199381`
- tail4 -> tip: `0.06640728124917872`.

## 7. Frozen weight support

`TAIL_ROOT_CTRL` has real final frozen support despite sharing its coordinate with `PELVIS_CTRL`:

- positive-weight support vertices: `294`
- maximum normalized weight: `0.29054180329975654`
- mean positive weight: `0.12620073223922798`
- support-weight sum: `37.103015278333025`
- support domain: exactly `TAIL`
- support-domain confinement: PASS.

`PELVIS_CTRL` and `TAIL_ROOT_CTRL` do **not** collapse into the same support set:

- intersection: `19`
- pelvis-only: `395`
- tail-root-only: `275`
- union: `689`
- Jaccard overlap: `0.027576197387518143`
- exact support-set equality: `false`.

This is important: coincident bind coordinates do not make the two roles semantically identical under the frozen domain/interface weighting system.

## 8. Tail weighted-arc structure

Weighted-arc centroids are strictly ordered root-to-tip:

- root `0.23053000480675057`
- tail1 `0.2640831887346988`
- tail2 `0.34596693342001`
- tail3 `0.5910414139857748`
- tail4 `0.8514063630879488`
- tip `0.9750175767472181`.

`strictRootToTipCentroidOrdering = true`.

Every adjacent tail support pair overlaps positively:

- root/tail1: `289`
- tail1/tail2: `348`
- tail2/tail3: `600`
- tail3/tail4: `325`
- tail4/tip: `259`.

`allAdjacentPositiveSupportOverlap = true`.

## 9. Downstream tail Jacobian audit

Using the unchanged frozen parent-axis rule, every downstream tail control whose parent vector is nonzero passes its dead-control/domain gate:

- `TAIL_1_CTRL` support `355`, max normalized derivative `0.051434917832426506`
- `TAIL_2_CTRL` support `607`, max normalized derivative `0.05170498117781759`
- `TAIL_3_CTRL` support `600`, max normalized derivative `0.04486091067897948`
- `TAIL_4_CTRL` support `325`, max normalized derivative `0.06890220284760554`
- `TAIL_TIP_CTRL` support `259`, max normalized derivative `0.10543134216999141`.

All are domain-confined to `TAIL`.

`allDownstreamTailControlsPassFrozenDeadAndDomainGate = true`.

## 10. Predeclared counterfactual probes

Exactly the two frozen probes were used. No third axis was introduced.

### `TAIL_ROOT_TO_TAIL_1`

- defined: `true`
- tangent norm: `0.08455559618696346`
- support count: `294`
- max normalized derivative: `0.03654724997875539`
- support domain confined: `true`
- nonzero allowed-domain differential support: `true`.

### `TAIL_PATH_FORWARD`

- defined: `true`
- tangent norm: `0.005516397904063737`
- support count: `294`
- max normalized derivative: `0.04661009910374392`
- support domain confined: `true`
- nonzero allowed-domain differential support: `true`.

Both probes therefore demonstrate that the tail-root control is not vacuous when evaluated along either predeclared nonzero tail-derived tangent.

## 11. Frozen classification

Classification precedence was evaluated exactly as contracted:

1. `BROADER_ZERO_LENGTH_HIERARCHY_DEGENERACY`
2. `COINCIDENT_BRANCH_ROOT_WITH_TAIL_SUPPORT_DEFECT`
3. `COINCIDENT_BRANCH_ROOT_WITH_NONVACUOUS_TAIL_SUPPORT`
4. `MIXED_OR_UNRESOLVED`

Observed primary result:

> **`COINCIDENT_BRANCH_ROOT_WITH_NONVACUOUS_TAIL_SUPPORT`**

Reasons:

- pelvis and tail root are the same exact medial-graph node and coordinate;
- no additional hierarchy-edge degeneracy exists;
- tail-root frozen final support is positive and domain-confined;
- tail weighted-arc centroids are strictly ordered;
- every adjacent tail support overlaps;
- `TAIL_1..TAIL_TIP` pass unchanged parent-axis differential/domain gates;
- both predeclared root probes show nonzero allowed-domain differential support.

## 12. Interpretation ceiling

The strongest permitted conclusion is:

> **The neutral frozen Stage-1 scaffold contains a structurally non-vacuous coincident tail-root. The previously exposed R12 blocker is now localized strongly enough to justify considering a separate diagnostic-axis change-control.**

Not proven:

- R12 PASS;
- anatomically correct tail-root placement;
- natural finite-angle deformation;
- natural gait or tail animation;
- planted-contact behavior;
- IK;
- runtime skinning quality;
- final Mobi body quality.

No coordinate, hierarchy, weight, domain, threshold or production motion change is authorized by this result alone.

## 13. Next boundary

Next legal private step:

> import this result into canonical governance and perform explicit change-control before choosing any structural repair or diagnostic-axis revision.

Until that import/change-control closes:

- do not move `TAIL_ROOT_CTRL`;
- do not change hierarchy;
- do not change weights/domains;
- do not invent a third tangent;
- do not begin finite-pose, IK, gait or animation work.
