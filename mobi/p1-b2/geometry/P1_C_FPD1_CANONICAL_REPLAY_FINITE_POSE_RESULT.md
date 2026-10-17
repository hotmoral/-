# P1-C FPD1 Canonical-Replay Finite-Pose Result

Status: **CLOSED / PASS / BOUNDED FINITE-POSE PRODUCT-PERCEPTUAL PASS**

Result token:

`P1_C_FPD1_CANONICAL_REPLAY_FINITE_POSE_PASS_PERCEPTUAL`

Governing pose:

`FPD1_FOREQUARTER_PIVOT_NECK_HEAD_YAW_LEFT_8DEG`

Governing replay contract:

`P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_CONTRACT_FROZEN`

## 1. Interpretation ceiling

This result proves only the first frozen bounded finite deformation:

- exact R10 frame;
- exact FOREQUARTER pivot;
- exact +Y axis;
- exact +8 degree right-handed neck/head turn toward anatomical left;
- transformed influence roles exactly `NECK_BASE_CTRL` and `HEAD_CTRL`;
- exact canonical frozen top-4 indices and float64 weights;
- no IK/contact compensation/root shift;
- the required 9 deformed-only direct views and 73-yaw diagnostic sweep.

It does **not** prove full articulated range, inverse kinematics, planted-paw solving, release/acquisition, gait, animation, production runtime skinning, or downstream Android motion integration.

The product criterion remains:

> **The unstyled Mobi body must read naturally as a cat from proportions, mass relationships, joints, silhouette and continuous orientation.**

## 2. Exact execution identity

Public execution branch:

`mobi/run-p1-c-fpd1-canonical-replay-evidence-20261017`

Replay implementation/freeze parent:

`f30f5a6fac315026bd870927de569cf6592375b0`

Exact execution HEAD:

`d072190520f2f2e17ce8f57580d60551dcf89cf8`

Execution-branch scope against frozen replay parent:

- `1` commit ahead;
- `0` behind;
- exactly one added file:
  `.github/workflows/mobi-p1-c-fpd1-canonical-replay-finite-pose-evidence.yml`;
- frozen adapter/evaluator/tests modified: `0`.

Evidence workflow identity:

- Git blob `b4d99c64b5142c4a820d7a20b56140e07c3be5b0`;
- SHA-256 `6d299d5d3a44f32ca8f7fb2ba111cae6b65c736292639df0d167a1b727d1b5d5`.

The workflow statically verified that the actual canonical-replay pose invocation appeared exactly once.

## 3. Run and artifact identity

Run:

- run `39003554353`;
- job `117311287573`;
- attempt `1`;
- event `push`;
- conclusion **SUCCESS**.

Runtime:

- Ubuntu 24.04 hosted runner;
- Azure region `centralus`;
- Python `3.12.15`;
- NumPy `2.5.4`;
- fast-simplification `0.2.0`;
- trimesh `4.11.1`;
- scikit-image `0.26.0`;
- scipy `1.17.0`.

Artifact:

- ID `12090545062`;
- size `216,510 bytes`;
- GitHub digest `sha256:827b22dae1ec86fc1b4ad276ca6e092378743dd1b5de16ce9c2323788dcfbcde`;
- independently downloaded ZIP SHA-256 matched exactly;
- `EVIDENCE_SHA256SUMS.txt` independent rehash: **33 / 33 PASS**.

## 4. Frozen authority gates passed before deformation

The run reverified:

- replay adapter blob `d91b434172ee30cd233b5647ba52295a89e1a925`;
- replay adapter SHA-256 `76c7fad97ad7820b59b4935b4206fb67e74c866a12d0097bd7b11e70bbddeb41`;
- original FPD1 evaluator blob `b76d4034cc23555c382d2508aaaa31e7578797ec`;
- original FPD1 evaluator SHA-256 `157ca0408f27e67330d10e49dff8b91446c0d674d4c106ec548bfbe001b8f097`;
- assembled R11 SHA-256 `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`;
- Standing Cat source SHA-256 `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`;
- V3125 mesh-array SHA-256 `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`;
- canonical weight serialization SHA-256 `171653287d416ce2fdb30db3e51356b241f0507614de8316ec0ed4ec0588b12c`;
- canonical top-4 indices SHA-256 `1907a206446b8da3497cb1e6adba4f59120f3af41bd5b003fabe513db64f871b`.

Frozen regression suites passed before pose execution:

- R11 `8 / 8 PASS`;
- R12 `4 / 4 PASS`;
- DAR1 `8 / 8 PASS`;
- FPD1 `9 / 9 PASS`;
- canonical replay `7 / 7 PASS`.

Immediate pre-pose replay gate also passed.

## 5. Actual finite deformation result

The run produced the first actual frozen FPD1 deformation:

- `actualFinitePoseEvidenceExecuted=true`;
- `deformedV3125Produced=true`;
- `rasterEvidenceExecuted=true`;
- V3125 remains `3125 V / 6246 F`;
- bind vertex SHA-256 `ce82444863e4c64ecf158d3514fb65f3d373dc5604f3ed5e1d09e86201c57632`;
- deformed vertex SHA-256 `74eef316116cdfaac83204835ab9100828d606e53d58b9b1facca672ef7c141a`;
- face-index SHA-256 `951c2636698fb4b54a988e28d4e7182f6ab65ffe2ebd5312a585b1c162ce5282`.

The deformed result is therefore nontrivial and separately identifiable from neutral bind state.

## 6. Contact/support isolation under actual deformation

Selected neck/head positive-weight support remains exactly `626` vertices:

- CORE `612`;
- FORE_L `10`;
- FORE_R `4`;
- HIND_L `0`;
- HIND_R `0`;
- TAIL `0`.

All `2,499` vertices outside selected support have maximum displacement exactly `0.0`.

Frozen paw surface-bind vertices:

- FORE_L `1338`;
- FORE_R `146`;
- HIND_L `2277`;
- HIND_R `826`.

All four paw anchors remained exact numeric identity with displacement `0.0`.

No IK, root shift or contact correction was used to obtain this result.

## 7. Direct deformed-only perceptual review

The visual review was deliberately performed on the deformed-only evidence **before** consulting geometry-health scalar diagnostics.

Mandatory direct views reviewed:

1. `-90°`
2. `-67.5°`
3. `-45°`
4. `-22.5°`
5. `0°` exact front
6. `+22.5°`
7. `+45°`
8. `+67.5°`
9. `+90°`

Material frozen failure classes were checked directly.

Observed result:

- no apparent head detachment;
- no neck pinch/collapse/hourglass severe enough to fail the body read;
- no hard hinge seam visible in silhouette;
- no material forequarter/neck/head mass discontinuity;
- no non-anatomical shoulder or forelimb-root drag;
- no obvious fold/plate boundary in the mandatory silhouettes;
- no wrong-turn-direction indication under the frozen frame/sign contract;
- no loss of natural feline silhouette;
- exact front remains recognizably feline rather than exposing a disqualifying failure;
- mirrored three-quarter/profile views preserve a continuous head-neck-body read.

Perceptual verdict:

**PASS**

The unstyled deformed body remains legible as a natural cat for this exact bounded +8 degree discriminator.

## 8. Geometry-health diagnostics after visual review

The scalar diagnostics do not reveal a hidden structural failure that would overturn the visual verdict.

Vertex/face validity:

- finite vertices `3125 / 3125`;
- neutral exact-zero-area faces `0`;
- deformed exact-zero-area faces `0`;
- non-finite-area faces `0`.

Overall displacement:

- max `0.03283533761605176`;
- mean `0.0032038486978543824`;
- median `0.0`;
- p95 `0.02419604485019568`;
- p99 `0.031035873480673992`;
- RMS `0.00833199690109734`.

Selected support displacement:

- count `626`;
- max `0.03283533761605176`;
- mean `0.015993653643442404`;
- median `0.01601345023688954`;
- p95 `0.031035830046422803`;
- p99 `0.032550537204643744`;
- RMS `0.01861602459186468`.

Maximum displacement outside selected support is exactly `0.0`.

Face-normal dot:

- minimum `0.19270622123302705`;
- p01 `0.9883735232745277`;
- p05 `0.9920324390446206`;
- median `1.0`;
- mean `0.9985097910431172`.

No face-normal sign reversal is indicated.

Triangle-area ratio:

- minimum `0.26330846248118545`;
- maximum `2.8860751628135137`;
- p01 `0.907707979601906`;
- p05 `0.9842691179299271`;
- median `1.0`;
- p95 `1.0082666991962277`;
- p99 `1.0638320090553812`.

The extreme local area ratios do not produce zero-area faces, inverted-normal evidence, or a material visible failure in the required direct views.

## 9. Note on the earlier cross-run weight drift

Historical pre-pose failures remain valid and are not erased.

Earlier independent hosted execution reproduced fresh weight bytes with SHA `0bcdb051...`, while the canonical frozen bytes are `171653...`. A dedicated diagnostic isolated that as machine-scale cross-run float64 byte variation with identical indices/support topology.

In this successful actual run, the immediate fresh reconstruction happened to reproduce the canonical weight bytes exactly (`171653...`, zero float-bit drift on that runner). This does **not** invalidate the earlier diagnosis or make fresh recomputation the authority.

The actual pose still used the explicitly acquired and verified canonical `weights.bin` bytes as required by the frozen replay contract.

## 10. Final bounded result

Result token:

`P1_C_FPD1_CANONICAL_REPLAY_FINITE_POSE_PASS_PERCEPTUAL`

Bounded conclusion:

> **The exact frozen +8 degree neck/head finite-pose discriminator, evaluated on V3125 with the exact canonical frozen top-4 indices and float64 weights, preserves paw/contact isolation, produces structurally valid finite geometry, and retains a natural feline body read across all nine mandatory deformed-only views.**

This is the first accepted finite deformation of the current Mobi motion-morphology scaffold.

It is not a general motion-system acceptance.

## 11. Still not authorized by this result

This PASS does not authorize automatic progression into:

- larger or arbitrary articulation ranges;
- inverse kinematics;
- planted-paw solve;
- paw release/acquisition scheduling;
- root-shift compensation;
- gait-cycle generation;
- animation timing/polish;
- production runtime-skinning selection;
- R13/tail-root relocation;
- P1-G/P1-H;
- downstream Android motion integration.

The next motion-morphology step requires a separate explicit change-control and must preserve this result rather than reinterpret it.
