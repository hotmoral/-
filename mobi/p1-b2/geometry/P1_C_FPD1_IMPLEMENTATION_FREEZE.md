# P1-C FPD1 Implementation Freeze

Status: **FROZEN / PRE-EVIDENCE PASS**

Freeze token:

`P1_C_FPD1_IMPLEMENTATION_FREEZE`

Governing decision:

`P1_C_SMALL_FINITE_POSE_NECK_YAW_SELECTED`

Governing contract:

`P1_C_SMALL_FINITE_POSE_NECK_YAW_CONTRACT_FROZEN`

Governing preflight:

`P1_C_SMALL_FINITE_POSE_NECK_YAW_PREFLIGHT_PASS`

Selected pose:

`FPD1_FOREQUARTER_PIVOT_NECK_HEAD_YAW_LEFT_8DEG`

## 1. Product interpretation ceiling

The implementation exists only to test the first bounded finite deformation without changing the governing Mobi objective:

> **The unstyled body must still read naturally as a cat from proportions, mass relationships, joints, silhouette and continuous orientation.**

This freeze does **not** claim that the +8° pose is natural. No actual deformed V3125, deformed raster evidence, or perceptual feline-readability review was produced by the pre-evidence QA. Mechanical implementation PASS cannot establish product PASS.

## 2. Frozen executable identity

Public branch:

`mobi/run-p1-c-fpd1-implementation-20261017`

Neutral authority base:

`35d4a914ed4656d8a975922ae3eeac34e3ab0c52`

Executable QA HEAD:

`ef82d2b67ef574154f1b397a0d688155118e9070`

Frozen executable files:

- implementation
  - `mobi/p1-b2/geometry/p1_c_fpd1_finite_pose_discriminator_v1.py`
  - blob `b76d4034cc23555c382d2508aaaa31e7578797ec`
  - SHA-256 `157ca0408f27e67330d10e49dff8b91446c0d674d4c106ec548bfbe001b8f097`
- synthetic tests
  - `mobi/p1-b2/geometry/test_p1_c_fpd1_finite_pose_discriminator_v1.py`
  - blob `06d65f0aeddc2c854b8d8dce6e265eb729f6dbb9`
  - SHA-256 `c6131b75e7a38abd7580c671b8a6c4fe8db0ca85ae86e86ad0e7e0f44ea5825c`
- pre-evidence QA workflow
  - `.github/workflows/mobi-p1-c-fpd1-pre-evidence-qa.yml`
  - blob `65b77b06e3b2da7ea351453d5b83ffa7921a19e3`
  - SHA-256 `2265eb1ade8e6607cf34139f7d735e5ecd231821cf3450e3003d9b1e6beacd3e`

Identity authority is also recorded in `P1_C_FPD1_IMPLEMENTATION_IDENTITY.json`.

No executable file may be modified after this freeze without a new implementation change-control.

## 3. Exact implementation semantics

The bounded evaluator freezes exactly:

- frame `R10`;
- pivot `FOREQUARTER_CTRL`;
- axis `[0, +1, 0]`;
- angle `+8°` = `0.13962634015954636 rad`;
- anatomical interpretation: neck/head turn toward anatomical left;
- transformed influence roles exactly `NECK_BASE_CTRL` and `HEAD_CTRL`;
- the other 28 role transforms are identity;
- all frozen bind control positions, hierarchy, domains, top-4 role indices and float64 weights remain unchanged;
- BODY_ROOT translation remains zero;
- no IK/contact compensation exists;
- no production runtime-skinning decision is made.

The two selected roles share the same rigid transform. The evaluator groups their selected weights algebraically. Vertices whose selected-role weight is exactly zero are copied exactly from bind state. That identity branch is the explicit mathematical consequence of zero selected influence; it is not a post-deformation correction.

## 4. Pre-evidence QA result

One public QA run was produced from the executable HEAD:

- run `38999151364`
- job `117298180934`
- attempt `1`
- event `push`
- conclusion **SUCCESS**

Artifact:

- ID `12088123879`
- size `3,047,732 bytes`
- GitHub digest `sha256:a395cf71206d3459c9ed052c37ff51ad1c0be097bc66fb5ebb02f7e208b97c84`
- independently downloaded ZIP SHA-256 matched exactly
- `QA_SHA256SUMS.txt` independent rehash: **36 / 36 PASS**

Synthetic regressions:

- R11 `8 / 8 PASS`
- R12 `4 / 4 PASS`
- DAR1 `8 / 8 PASS`
- FPD1 `9 / 9 PASS`

Frozen DAR1 neutral Stage-1 regression also completed successfully before the FPD1 pre-evidence isolation audit.

## 5. Real-scaffold pre-evidence isolation

The implementation reconstructed the exact Standing Cat / V3125 / R12 / DAR1 state under seeds `1` and `777` without executing the finite pose.

Both pre-evidence JSON outputs were byte-identical:

`eda0f5d0680351e3453dc2b06469efbee92dff2815aab45cbb9b7e0f79e9a3ce`

Deterministic diff:

- bytes `0`
- SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

Verified identities include:

- Standing Cat SHA-256 `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`;
- V3125 `3125 V / 6246 F`;
- V3125 mesh-array SHA-256 `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`;
- frozen weight SHA-256 `171653287d416ce2fdb30db3e51356b241f0507614de8316ec0ed4ec0588b12c`;
- DAR1 axis-isolation role remains exactly `TAIL_ROOT_CTRL`;
- neutral rest error remains at machine-precision scale.

## 6. Selected-support isolation

Positive support union of `NECK_BASE_CTRL` and `HEAD_CTRL`:

- total `626` vertices;
- CORE `612`;
- FORE_L `10`;
- FORE_R `4`;
- HIND_L `0`;
- HIND_R `0`;
- TAIL `0`.

Support-mask SHA-256:

`00d146898426ea970cbe9e7f17e553cb274021e549dc61c8e9910ce71c553bb5`

Each frozen paw surface-bind vertex has selected-role weight exactly `0.0`:

- FORE_L index `1338`;
- FORE_R index `146`;
- HIND_L index `2277`;
- HIND_R index `826`.

Therefore future FPD1 evidence must preserve all four paw anchors exactly. If an actual FPD1 run moves one, the run fails; no IK or contact compensation is permitted inside FPD1.

## 7. Explicit evidence boundary

The QA artifact independently confirms all of the following remained false:

- `actualFinitePoseEvidenceExecuted=false`
- `deformedV3125Produced=false`
- `rasterEvidenceExecuted=false`
- `perceptualReviewExecuted=false`

No `deformed_vertices`, `geometry_health`, `visual_evidence`, or deformed-view PNG output exists in the QA artifact. PNG files present in the artifact belong only to the inherited neutral DAR1 regression.

The implementation contains a future `--evaluate-pose` path, but the pre-evidence workflow explicitly prohibits invoking it.

## 8. What is frozen vs. what is still unknown

Frozen/validated pre-evidence:

- pose parameters;
- finite weighted evaluator semantics;
- exact inherited identities;
- support isolation;
- paw-anchor zero selected influence;
- 9-view direct-review contract;
- 73-yaw diagnostic sweep contract;
- deterministic neutral reconstruction;
- executable identity.

Still unknown:

- whether the actual +8° V3125 deformation remains naturally feline;
- whether the neck/forequarter transition pinches, hinges, folds, or visually detaches;
- whether exact-front or any other view exposes an unacceptable silhouette defect;
- whether numeric deformation-health metrics show a structural warning;
- the direct human product verdict.

## 9. Authorization boundary

This freeze does **not** authorize the actual finite-pose evidence run.

`finitePoseEvidenceRunAuthorizedByThisFreeze = false`

The next legal step is private import/review of this exact implementation identity. Only after that private import and a separate intentional user authorization may an execution group invoke the frozen `--evaluate-pose` path.

Still prohibited:

- angle/pivot/axis retuning;
- weight/domain/control/hierarchy edits;
- IK or contact compensation;
- gait/animation;
- runtime skinning selection;
- R13 geometry or tail-root relocation;
- product acceptance from numeric evidence alone.
