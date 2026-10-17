# P1-C FPD2 Tail-Branch Implementation Freeze

Status: **FROZEN / PRE-EVIDENCE PASS**

Freeze token:

`P1_C_FPD2_TAIL_BRANCH_IMPLEMENTATION_FREEZE`

Selection:

`P1_C_POST_FPD1_TAIL_BRANCH_YAW_SELECTED`

Contract:

`P1_C_FPD2_TAIL_BRANCH_YAW_CONTRACT_FROZEN`

Preflight:

`P1_C_FPD2_TAIL_BRANCH_YAW_PREFLIGHT_PASS`

Pose:

`FPD2_TAIL_ROOT_PIVOT_FULL_TAIL_YAW_RIGHT_8DEG`

## 1. Scope

This freeze closes only the bounded FPD2 implementation stage.

It establishes that the exact canonical frozen V3125 scaffold and exact canonical frozen top-4 weight bytes can be reconstructed into an FPD2 evaluator whose only new finite transform is the already-contracted whole-tail +8 degree yaw.

It does **not** establish that the deformed tail looks natural. Actual FPD2 finite-pose evidence has not executed under this freeze.

No production FK/runtime skinning choice is made.

## 2. Exact public implementation identity

Public branch:

`mobi/run-p1-c-fpd2-tail-branch-implementation-20261018`

Frozen implementation base:

`f30f5a6fac315026bd870927de569cf6592375b0`

Exact executable QA HEAD:

`8a534066e2fdf4f705911e20bd24049fc7cb63d5`

Exact executable files:

### Evaluator

- path: `mobi/p1-b2/geometry/p1_c_fpd2_tail_branch_yaw_v1.py`
- blob: `5192bf66da974339eb5c080508fad327442133c5`
- SHA-256: `035fce7081507bd8d0e6f1f089d4fcbb13fdb54988d479f2528bc4076a9c1cc7`

### Tests

- path: `mobi/p1-b2/geometry/test_p1_c_fpd2_tail_branch_yaw_v1.py`
- blob: `26aa780f819c829c0b742488fa7645fd7d7b4570`
- SHA-256: `0e1f2d6ac0a944eb0f46dbe81a161819a3600f00bd9cb6188bcd53e791836fc6`

### Pre-evidence QA workflow

- path: `.github/workflows/mobi-p1-c-fpd2-tail-branch-pre-evidence-qa.yml`
- blob: `39f4a93fdc1305f5bb6dccc354a83a789d6ea426`
- SHA-256: `cdb5239b7979b110f7909a6239231d249256c1f46defe48b0001f0e86ad64e46`

Machine-readable identity:

`P1_C_FPD2_TAIL_BRANCH_IMPLEMENTATION_IDENTITY.json`

No executable byte above may change after this freeze without new change-control.

## 3. Inherited frozen authority remains untouched

The implementation layers on the exact frozen canonical-replay state.

Inherited bytes verified during QA:

- canonical replay adapter blob `d91b434172ee30cd233b5647ba52295a89e1a925`
- canonical replay adapter SHA-256 `76c7fad97ad7820b59b4935b4206fb67e74c866a12d0097bd7b11e70bbddeb41`
- original FPD1 evaluator blob `b76d4034cc23555c382d2508aaaa31e7578797ec`
- original FPD1 evaluator SHA-256 `157ca0408f27e67330d10e49dff8b91446c0d674d4c106ec548bfbe001b8f097`
- assembled R11 SHA-256 `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`

The implementation does not mutate R10/R11/R12/DAR1/FPD1 or canonical-replay files.

## 4. Canonical weight authority

FPD2 uses the exact frozen canonical `weights.bin` authority from successful run `38999151364`, artifact `12088123879`.

Required identity:

- bytes `112,532`
- serialized SHA-256 `171653287d416ce2fdb30db3e51356b241f0507614de8316ec0ed4ec0588b12c`
- top-4 indices SHA-256 `1907a206446b8da3497cb1e6adba4f59120f3af41bd5b003fabe513db64f871b`
- float64 weights SHA-256 `aa3569c6d2c3350bf21493d8c4fc8acc8d15db366cdcf51c8c81c7cdafa57411`

Fresh recomputed float64 weights are diagnostic only and cannot replace this authority.

## 5. Frozen FPD2 pose semantics

Exact pose:

- frame: R10
- pivot: exact `TAIL_ROOT_CTRL` bind point `[0.0, 0.2925511774265033, -0.08581501204510761]`
- axis: exact `[0.0, 1.0, 0.0]`
- angle: exact `+8.0°` / `0.13962634015954636 rad`
- right-handed
- anatomical meaning: whole tail yaw toward anatomical right
- selected roles exactly:
  1. `TAIL_ROOT_CTRL`
  2. `TAIL_1_CTRL`
  3. `TAIL_2_CTRL`
  4. `TAIL_3_CTRL`
  5. `TAIL_4_CTRL`
  6. `TAIL_TIP_CTRL`
- all other 24 roles identity
- BODY_ROOT translation zero
- no IK
- no root compensation
- no geometry or bind-control rewrite
- no smoothing, corrective shape, optimization, retargeting or post-fit

The evaluator groups the six equal tail-role transforms algebraically and preserves exact bind bytes for vertices whose selected-tail total weight is exactly zero.

## 6. Support-isolation regression identity

Under exact canonical weight bytes:

- selected-tail positive support union: `619`
- TAIL domain count: `619`
- selected support == TAIL domain: exact set equality
- support-mask SHA-256: `72565b6b1a7db89aaa11c37097463ccbde45dd1540c524313dcdc9074e9b530e`
- CORE support: `0`
- FORE_L support: `0`
- FORE_R support: `0`
- HIND_L support: `0`
- HIND_R support: `0`
- TAIL support: `619`

Root interface:

- mixed selected-tail / non-tail identity vertices: exactly `19`
- selected-tail total minimum: `0.2606796033855258`
- selected-tail total maximum: `0.7507989280093238`
- remaining full-tail vertices: `600`
- those 600 have selected-tail total `1.0` within inherited frozen normalization tolerance

Paw anchors:

- FORE_L index `1338`: selected-tail total `0.0`
- FORE_R index `146`: selected-tail total `0.0`
- HIND_L index `2277`: selected-tail total `0.0`
- HIND_R index `826`: selected-tail total `0.0`

No IK or compensation is permitted if a later evidence run violates these identities.

## 7. Reference transform regression identity

Under the exact +8 degree rigid branch transform:

- TAIL_ROOT displacement `0.0`
- TAIL_1 displacement `0.011728595742647828`
- TAIL_2 displacement `0.01886362579442028`
- TAIL_3 displacement `0.03488653203299144`
- TAIL_4 displacement `0.04089078599591688`
- TAIL_TIP displacement `0.041991318968251645`

Frozen pitch:

`0.0039006823656867104`

TAIL_TIP reference displacement is therefore `10.765121338163386 * pitch`.

This confirms a visibly finite discriminator without tuning the tail angle after seeing a result.

## 8. Pre-evidence QA

Run:

- run `39076540003`
- job `117524749951`
- attempt `1`
- event `push`
- executable HEAD `8a534066e2fdf4f705911e20bd24049fc7cb63d5`
- conclusion **SUCCESS**

Test results:

- R11 `8/8 PASS`
- R12 `4/4 PASS`
- DAR1 `8/8 PASS`
- FPD1 `9/9 PASS`
- canonical replay `7/7 PASS`
- FPD2 `9/9 PASS`

Exact runtime:

- Python `3.12.15`
- NumPy `2.5.4`
- fast-simplification `0.2.0`
- trimesh `4.11.1`
- scikit-image `0.26.0`
- scipy `1.17.0`

## 9. QA artifact independent verification

Artifact:

- ID `12116907842`
- name `mobi-p1-c-fpd2-tail-branch-pre-evidence-39076540003`
- size `9,090,430 bytes`
- GitHub digest `sha256:ed02950ca395ef6592411a1fafa162921fad3b0f17f0dc0054c5523a885d38e0`
- independent ZIP SHA-256 exact match
- `FPD2_QA_SHA256SUMS.txt` independent rehash: **43 / 43 PASS**

Seed determinism:

- seed 1 / 777 pre-evidence JSON byte-identical
- pre-evidence JSON SHA-256 `49ec9be0ae1abf0db5aae53a0b646e0853cd560baa43b9c05e6d6f73538a431d`

The canonical source artifact ZIP embedded in QA also reverified the preexisting artifact digest `a395cf71206d3459c9ed052c37ff51ad1c0be097bc66fb5ebb02f7e208b97c84` and exact canonical weight bytes.

## 10. Explicit evidence boundary

The pre-evidence report records:

- `actualFinitePoseEvidenceExecuted=false`
- `deformedV3125Produced=false`
- `rasterEvidenceExecuted=false`
- `perceptualReviewExecuted=false`

Independent artifact inspection found no new:

- deformed V3125 vertex payload
- FPD2 geometry-health result
- FPD2 visual-evidence result
- FPD2 deformed-view PNG

Therefore this freeze establishes only:

> **the FPD2 evaluator is causally isolated, deterministic, canonical-weight replayable, and contract-exact before any actual tail deformation evidence is interpreted.**

It does not establish tail-root naturalness.

## 11. Authorization boundary

This implementation freeze does **not** authorize an actual FPD2 pose execution by itself.

Next legal step is:

> **private import/review of this exact public implementation identity and QA result.**

Only after private canonical import may a separate intentional evidence group execute the exact frozen FPD2 evaluator.

Still prohibited here:

- actual FPD2 evidence execution
- angle/axis/pivot/selected-role retuning
- weight editing or fresh-weight authority substitution
- tail-root relocation / R13
- IK or planted-paw solving
- support release/acquisition
- gait / animation
- production runtime-skinning selection
- downstream P1-G/P1-H Android motion integration
