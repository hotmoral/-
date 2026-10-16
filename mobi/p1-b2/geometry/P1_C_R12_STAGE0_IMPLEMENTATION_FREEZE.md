# Mobi P1-C-R12 — Stage-0 Implementation Freeze

Date: 2026-10-17
Status: **FROZEN / PRE-EVIDENCE / STAGE-1 NOT AUTHORIZED**

Freeze token:

> **`R12_STAGE0_IMPLEMENTATION_FREEZE`**

## 1. Scope

This Stage-0 freeze implements only the private-canonical R12 contract:

- decision: `R12_RF_M_SURFACE_TERMINAL_BIND_ALIAS_SELECTED_FOR_FEASIBILITY`
- contract: `R12_SURFACE_TERMINAL_BIND_ALIAS_FEASIBILITY_CONTRACT_FROZEN`
- preflight: `R12_SURFACE_TERMINAL_BIND_ALIAS_PREFLIGHT_CONSISTENT_WITH_CONSTRAINT`

It does not execute R12 Stage 1 and does not reinterpret the failed R11 checkpoint.

R11 remains historical **FAIL / `R11_STAGE1_FAIL_FORE_L_PAW_LOCAL_SUPPORT`**.

## 2. Public execution branch

- repository: `hotmoral/-`
- branch: `mobi/run-p1-c-r12-surface-terminal-bind-20261017`
- branch base: `4ce94fa9c07f0f86b0380c58cdacaf59481732c2`
- frozen R11 Stage-1 execution identity inherited from: `4c695503b99974e929491b1e78b0cf2935b675c7`
- implementation/workflow pre-freeze HEAD: `6955239841219384e55fcd8c0fb6092cf859a62a`

The two commits between R11 frozen execution HEAD and the R12 branch base add R11 result/handoff documentation only. No inherited R11 source, assembler, test or workflow byte changed in that delta.

## 3. R12 executable architecture

R12 does **not** fork or rewrite the 37,871-byte R11 implementation.

Instead:

1. the existing R11 assembler reconstructs the exact frozen R11 module;
2. its exact SHA-256 is verified before R12 imports it;
3. R12 calls the inherited R11 code for V3125 reproduction, frame/sign, voxelization, skeleton graph, pruning, semantic paths, 30-role construction, six-domain derivation, weight construction, weight audit, neutral LBS, Jacobian audit and rasterization;
4. an R12 adapter replaces only the active bind coordinate of the four existing paw roles;
5. explicit delta gates reject any change outside those four coordinates or any change to parent/domain/provenance.

This adapter architecture is intentionally chosen to minimize accidental divergence from the failed-but-diagnostic R11 hypothesis.

## 4. Exact R12 adapter identity

Path:

`mobi/p1-b2/geometry/p1_c_r12_surface_terminal_bind_alias_v1.py`

Frozen identity:

- byte count: `16839`
- SHA-256: `06d8529cf28b3dc1cffa1cecb3da4524083167614cf3a4b3da36d46844557025`
- Git blob SHA-1: `f63d7ee780e5fb2f4716b83532e16d3d2ee525a3`
- version: `P1_C_R12_SURFACE_TERMINAL_BIND_ALIAS_V1`

The adapter refuses to load R11 unless the assembled R11 SHA-256 is exactly:

`af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`.

It also hard-checks:

- R11 version `P1_C_R11_SEMANTIC_SCAFFOLD_V1`;
- R11 freeze token `R11_STAGE0_IMPLEMENTATION_FREEZE`;
- role count `30`;
- domain order `CORE / FORE_L / FORE_R / HIND_L / HIND_R / TAIL`;
- paw support radius `4.0*pitch`;
- maximum influences `4`.

## 5. Frozen surface-terminal alias derivation

Frame/sign remains:

> **`+X_R10 = anatomical left`**

For exact V3125 body center `(xmid, zmid)` and body height `h`, the four quadrants remain:

- FORE_L: `x >= xmid` and `z >= zmid`
- FORE_R: `x < xmid` and `z >= zmid`
- HIND_L: `x >= xmid` and `z < zmid`
- HIND_R: `x < xmid` and `z < zmid`

For each quadrant:

1. obtain global V3125 vertex indices in the quadrant;
2. compute `quadrantYMin`;
3. retain exact existing vertices with `y <= quadrantYMin + 0.035*h`;
4. compute the float64 arithmetic mean of those sole candidates;
5. rank candidates by `(squaredDistanceToSoleMean, globalVertexIndex)`;
6. select the minimum;
7. use that exact existing V3125 vertex as the active paw deformation bind.

No interpolation, surface projection, optimization, manual choice, rendered-fit correction or external rig coordinate is permitted.

## 6. Exact allowed causal delta

Only these active bind coordinates may differ from R11:

- `FORE_L_PAW_CTRL`
- `FORE_R_PAW_CTRL`
- `HIND_L_PAW_CTRL`
- `HIND_R_PAW_CTRL`

The R11 medial semantic-path endpoints remain computed and recorded separately.

The implementation hard-fails unless:

- changed role count is exactly `4`;
- changed roles are exactly the four paw roles above;
- the other `26` active role positions are byte/numeric-identical at the Python float tuple level to R11 construction;
- all 30 role names and order remain unchanged;
- all parent/domain/provenance metadata remain unchanged;
- each historical R11 paw bind still equals its inherited medial semantic-path endpoint.

## 7. Explicitly inherited unchanged machinery

The following are not modified by R12:

- exact V3125 authority and topology;
- mesh-array SHA-256 expectation `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`;
- source SHA-256 `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`;
- frame/sign;
- voxel pitch and fill method;
- medial skeleton and graph construction;
- branch pruning;
- semantic path extraction;
- the 26 non-paw control coordinates;
- 30-role hierarchy;
- six-domain derivation;
- root-interface rule;
- inverse-distance weight kernel;
- `sigma = 2*pitch`;
- top-4 truncation;
- normalized weight rules;
- Jacobian epsilon and support threshold;
- **paw locality radius remains exactly `4*pitch`**;
- tail order/overlap checks;
- neutral rest identity convention;
- 96x96 inherited raster path;
- five primary views and full `0..90` by `2.5` degree sweep;
- seed 1 / 777 determinism requirement.

R12 deliberately does not repair domain or top-4 behavior in advance. A secondary failure there must remain observable.

## 8. Added R12 hard gates

Before the inherited paw-local Jacobian gate can PASS, each paw alias must prove:

1. selected index is in V3125 range;
2. stored position is exactly the selected V3125 vertex position;
3. domain at the alias vertex equals the expected anatomical domain;
4. the same paw role survives final top-4 truncation at its own alias vertex;
5. the same paw role has strictly positive normalized weight at its own alias vertex.

The inherited `jacobian_audit` then checks nonzero support, domain confinement, and local differential support using the unchanged `4*pitch` radius around the new active bind.

A later PASS therefore cannot be created by merely moving the audit center without real local weighted influence.

## 9. Synthetic contract tests

Path:

`mobi/p1-b2/geometry/test_p1_c_r12_surface_terminal_bind_alias_v1.py`

Frozen identity:

- byte count: `5049`
- SHA-256: `64b85b6c8331783fc313e68064af724ffbf5966bcdfeb9e2dddb20e5f8d60140`
- Git blob SHA-1: `7257217740e2ff7dedffc3b54f33b85d42a920db`

Tests cover:

- frozen quadrant and `0.035*h` sole-candidate rule;
- exact squared-distance tie breaking by global vertex index;
- exactly-four-paw replacement / 26-role preservation;
- expected domain and own-positive-weight alias gate.

The inherited R11 synthetic test suite remains part of future pre-evidence execution as well.

## 10. Future public Stage-1 workflow lock

Workflow:

`.github/workflows/mobi-p1-c-r12-surface-terminal-bind.yml`

Frozen Git blob SHA-1:

`8918c48e6330b493c15e9fb41c6b5b741ee5f698`

The workflow has **only** `workflow_dispatch` as a trigger.

The evidence job additionally requires both:

- exact branch `mobi/run-p1-c-r12-surface-terminal-bind-20261017`;
- exact authorization token `RUN_R12_STAGE1_AFTER_STAGE0_FREEZE`.

Stage-0 commits alone therefore cannot start evidence.

The workflow preserves failure evidence with `if: always()` artifact upload. Both seeds are attempted before a structural failure is surfaced, so the first failure evidence is not intentionally discarded.

## 11. Exact inherited R11 bytes

Assembler:

- path `mobi/p1-b2/geometry/assemble_p1_c_r11_semantic_scaffold_v1.sh`
- Git blob `7a5c4bda8131fcbfc1ef301c70c64d423bf5c04f`

Assembled R11 implementation:

- byte count `37871`
- SHA-256 `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`

Seven frozen parts:

- `part000.txt` — `8e4c430cf405c0b1c05dcad591a7c73e6bb143db`
- `part001.txt` — `86d3651e1b115c9bbfcedddbe0b42b0ac95f91c1`
- `part002.txt` — `b514eaca8a1af556509d719411ccf679c6eacabb`
- `part003.txt` — `8e9c9798de55bde7099971e6a868c98b65f377cf`
- `part004.txt` — `a09ae537bdec38534adc63882854f4fac3ae9e50`
- `part005.txt` — `db9dd42cb562ce23049cb32ca6cda6728e159b10`
- `part006.txt` — `10449747ebebb1a96298427d8e570675d3c4e2a9`

Inherited source-code blobs:

- R10 reducer `f281aad3e3a6c740c38c0a3f015718996dc45157`
- Stage-D raster `5c8820fb7270e7727ececb1bb37d3a24331b24ab`
- Stage-B inspector `9b7899bc1c39d02291813a826df01d3697192846`
- R11 synthetic tests `868a9cf58a32fdf725fe79c0d34d2cc77cb3c7aa`

## 12. Frozen runtime

Future evidence runtime remains:

- runner: `ubuntu-latest`
- Python: `3.12.15`
- `numpy==2.5.4`
- `fast-simplification==0.2.0`
- `trimesh==4.11.1`
- `scikit-image==0.26.0`
- `scipy==1.17.0`

No substitute local dependency version may create canonical evidence.

## 13. Future Stage-1 outputs

A later separately authorized Stage 1 will attempt to preserve at least:

- exact V3125 identity JSON;
- inherited medial graph and semantic paths;
- retained R11 medial paw endpoints;
- R12 surface-terminal aliases and selected global vertex indices;
- exact four-role delta audit;
- scaffold;
- six-domain field;
- weights and weight audit;
- alias semantic/weight hard-gate report;
- Jacobian support report;
- neutral rest/raster identity;
- two-seed execution status and deterministic comparison on PASS;
- complete evidence SHA manifest.

A PASS would establish only bounded dual-anchor scaffold feasibility. It would not prove natural finite pose or natural motion.

## 14. Prohibited changes after this freeze

Do not change after seeing Stage-1 evidence:

- alias candidate formula;
- tie-breaking;
- the four-vs-26 delta boundary;
- `4*pitch`;
- domain rules;
- weight kernel;
- top-4;
- control count/hierarchy;
- non-paw coordinates;
- frame/sign;
- V3125;
- runtime versions.

A material change requires explicit new private change control/checkpoint.

## 15. Stage-0 disposition

At this document's creation:

- implementation bytes are defined;
- workflow trigger is locked;
- synthetic tests are defined;
- exact inherited R11 bytes are pinned;
- **no R12 Stage-1 evidence run is authorized by Stage 0 itself**.

The companion identity JSON must pin the final Git blob set before Stage 0 can be privately imported and closed.
