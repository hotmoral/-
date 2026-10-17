# P1-C FPD1 Canonical-Weight Replay Implementation Freeze

Status: **FROZEN / PRE-EVIDENCE PASS**

Freeze token:

`P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_IMPLEMENTATION_FREEZE`

Selection:

`P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_SELECTED`

Contract:

`P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_CONTRACT_FROZEN`

Pose remains:

`FPD1_FOREQUARTER_PIVOT_NECK_HEAD_YAW_LEFT_8DEG`

## 1. Scope and purpose

This implementation exists only to remove cross-run recomputation of already-frozen float64 weight bytes as an uncontrolled numerical variable while preserving the previously frozen FPD1 pose and evaluator semantics exactly.

It does **not** change the weight design, topology, controls, domains, hierarchy, pose axis, pivot, angle, transformed role set, contact model or production runtime-skinning decision.

It does **not** claim that the +8 degree deformed cat looks natural. Actual finite-pose evidence has still not executed under this freeze.

## 2. Frozen public identity

Public branch:

`mobi/run-p1-c-fpd1-canonical-weight-replay-20261017`

Frozen implementation base:

`263dd07a07a67f31947e9be24b63fb1c3b62e671`

Executable QA HEAD:

`3abd89f8d91b3249ef2ffade432ac6b7eb676c4c`

Frozen replay executable files:

- adapter
  - `mobi/p1-b2/geometry/p1_c_fpd1_canonical_weight_replay_v1.py`
  - blob `d91b434172ee30cd233b5647ba52295a89e1a925`
  - SHA-256 `76c7fad97ad7820b59b4935b4206fb67e74c866a12d0097bd7b11e70bbddeb41`
- tests
  - `mobi/p1-b2/geometry/test_p1_c_fpd1_canonical_weight_replay_v1.py`
  - blob `f211f6e2d6aa6573df79d9ab4925f1d34ebe402c`
  - SHA-256 `6d04dcd1b09a52e565f5f2c58e15be28501ba3a07bdb672897a181cf10b2b356`
- pre-evidence QA workflow
  - `.github/workflows/mobi-p1-c-fpd1-canonical-weight-replay-pre-evidence-qa.yml`
  - blob `b1c056d64c8b8c825308c79e35f412b93bf9d95e`
  - SHA-256 `ca619ee745c4bb68a2709e36a84ee8c6913fd5cfdcf94810d6e16f0045b672a4`

Frozen original FPD1 evaluator remains untouched:

- blob `b76d4034cc23555c382d2508aaaa31e7578797ec`
- SHA-256 `157ca0408f27e67330d10e49dff8b91446c0d674d4c106ec548bfbe001b8f097`

Exact machine-readable identity is recorded in `P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_IDENTITY.json`.

No replay executable file may be modified after this freeze without new change-control.

## 3. Canonical weight-byte authority

Source successful pre-evidence run:

- run `38999151364`
- artifact `12088123879`
- artifact digest `sha256:a395cf71206d3459c9ed052c37ff51ad1c0be097bc66fb5ebb02f7e208b97c84`
- member `neutral_stage1_regression/weights.bin`

Required exact byte identity:

- length `112,532 bytes`
- prefix `MOBI_R11_WEIGHTS_V1\0`
- header `3125 vertices / 30 roles`
- serialized SHA-256 `171653287d416ce2fdb30db3e51356b241f0507614de8316ec0ed4ec0588b12c`
- raw top-4 indices SHA-256 `1907a206446b8da3497cb1e6adba4f59120f3af41bd5b003fabe513db64f871b`
- raw float64 weight SHA-256 `aa3569c6d2c3350bf21493d8c4fc8acc8d15db366cdcf51c8c81c7cdafa57411`

The adapter parses these exact bytes. It does not accept the fresh cross-run `0bcdb051...` serialization as a replacement authority.

## 4. Adapter behavior

Before any future pose evaluation the adapter:

1. verifies exact frozen FPD1 evaluator file identity;
2. reconstructs the exact Standing Cat / V3125 / R12 / DAR1 structural state;
3. verifies V3125 mesh identity;
4. parses the canonical `weights.bin` only after length/prefix/header/all SHA gates pass;
5. requires fresh reconstructed top-4 indices to be bit-for-bit identical to canonical indices;
6. substitutes only the already-frozen canonical float64 weight bytes for subsequent evaluation;
7. reruns inherited weight audit on canonical bytes;
8. reruns selected-role support isolation;
9. requires all four frozen paw anchors to have selected-role total exactly zero;
10. reruns neutral rest identity with the canonical bytes;
11. preserves the original frozen FPD1 finite weighted evaluator for any later actual pose execution.

The measured fresh-vs-canonical float drift remains diagnostic output; it is not used as an acceptance tolerance.

## 5. Frozen pose semantics remain unchanged

- frame R10;
- pivot exact `FOREQUARTER_CTRL` bind coordinate;
- axis exact `[0.0, 1.0, 0.0]`;
- angle exact `+8.0°` / `0.13962634015954636 rad`;
- transformed roles exactly `NECK_BASE_CTRL`, `HEAD_CTRL`;
- all other 28 role transforms identity;
- BODY_ROOT translation zero;
- no IK or contact compensation;
- direct review views exactly 9;
- dense diagnostic yaws exactly 73.

## 6. Pre-evidence QA result

Run:

- run `39003049219`
- job `117309812491`
- attempt `1`
- event `push`
- executable HEAD `3abd89f8d91b3249ef2ffade432ac6b7eb676c4c`
- conclusion **SUCCESS**

Test results:

- R11 `8/8 PASS`
- R12 `4/4 PASS`
- DAR1 `8/8 PASS`
- FPD1 `9/9 PASS`
- canonical replay `7/7 PASS`

Canonical artifact acquisition inside the QA reverified:

- source artifact ZIP SHA exact `a395cf71206d3459c9ed052c37ff51ad1c0be097bc66fb5ebb02f7e208b97c84`
- extracted canonical `weights.bin` exact SHA `171653287d416ce2fdb30db3e51356b241f0507614de8316ec0ed4ec0588b12c`
- Standing Cat source SHA exact `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`

Replay audit under seeds `1` and `777` was byte-identical.

Replay audit JSON SHA-256:

`830dab53baa7ab4507ceb359660372f8c19f4e05bc262c8887d1a18d69981f39`

## 7. QA artifact independent verification

Artifact:

- ID `12089912679`
- size `9,089,511 bytes`
- GitHub digest `sha256:dbafb146d4abd71992a39eea6aca75cd0e96911b7be7f76fd58d7d990852703f`
- independently downloaded ZIP SHA-256 exact match
- `REPLAY_QA_SHA256SUMS.txt` independent rehash **43 / 43 PASS**

The artifact includes the exact canonical weight bytes and the prior canonical artifact contents for provenance, plus the two replay audit JSON files.

## 8. Pre-evidence results

Canonical replay pre-evidence reconstruction verifies:

- V3125 `3125 V / 6246 F` and mesh SHA unchanged;
- canonical weight bytes exact;
- fresh top-4 indices exact canonical match;
- canonical weight audit finite/nonnegative;
- `domainBleedCount=0`;
- `unweightedVertexCount=0`;
- max weight-sum error `2.220446049250313e-16`;
- selected-role support union exactly `626`;
- domain support exactly CORE `612`, FORE_L `10`, FORE_R `4`, HIND_L `0`, HIND_R `0`, TAIL `0`;
- selected support mask SHA `00d146898426ea970cbe9e7f17e553cb274021e549dc61c8e9910ce71c553bb5`;
- paw surface-bind indices `1338 / 146 / 2277 / 826` all selected-role weight exactly `0.0`;
- canonical neutral rest max normalized `3.0561548317486276e-16`;
- canonical neutral rest RMS normalized `5.27737336708397e-17`.

The fresh recomputation drift remains visible in diagnostics:

- fresh serialized SHA `0bcdb0514d672eeaf03920c37af4ff717892f26ab4631a8b3dce5b33528374c8`;
- 2,294 differing float slots;
- 1,065 vertices with any float-bit difference;
- max absolute difference `2.7755575615628914e-16`;
- max relative difference `9.743092789540392e-16`;
- max ULP `6`.

This drift is not accepted as a new authority; exact canonical replay is used instead.

## 9. Explicit evidence boundary

The replay QA records:

- `actualFinitePoseEvidenceExecuted=false`
- `deformedV3125Produced=false`
- `rasterEvidenceExecuted=false`
- `perceptualReviewExecuted=false`

Independent artifact inspection found no deformed vertex output, geometry-health output, visual-evidence output or deformed-view PNG.

Therefore this freeze establishes only:

> **the exact canonical weight bytes can be replayed deterministically into the frozen FPD1 scaffold without changing topology, support semantics, contact isolation or pose definition.**

It does not establish finite-pose naturalness.

## 10. Authorization boundary

This freeze does **not** itself authorize an actual finite-pose evidence execution.

`finitePoseEvidenceRunAuthorizedByThisFreeze = false`

Next legal step is private import/review of this exact replay implementation identity. Only after that import may a separate intentional evidence group invoke the frozen canonical-replay pose path.

Still prohibited without later change-control:

- accepting fresh recomputed weights as authority;
- tolerance-based identity weakening;
- angle/axis/pivot/transformed-role retuning;
- geometry/control/domain/weight redesign;
- IK/contact compensation or root shift;
- gait/animation;
- production runtime skinning selection;
- R13/tail-root relocation;
- P1-G/P1-H or downstream Android motion work.
