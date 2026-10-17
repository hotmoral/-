# P1-C DAR1 Diagnostic-Axis Revision Implementation Freeze

Status: **CLOSED / FROZEN / PRE-EVIDENCE PASS**

Freeze token:

`P1_C_DAR1_IMPLEMENTATION_FREEZE`

Selected variant:

`DAR1_HIERARCHY_CONTINUATION_ON_EXACT_PARENT_DEGENERACY`

## 1. Scope of this freeze

This freeze closes only the DAR1 implementation and pre-evidence QA group.

It does **not** claim revised R12/DAR1 Stage-1 structural PASS, finite-pose quality, anatomical tail-root correctness, natural tail motion, gait, IK, runtime skinning quality, or final Mobi product quality.

No revised Stage-1 structural evidence was executed in this group.

## 2. Frozen public lineage

Repository:

`hotmoral/-`

Branch:

`mobi/run-p1-c-dar1-diagnostic-axis-revision-20261017`

Exact inherited R12 base:

`4dbc13f67c0097e5bb84fd2b0ec27d71c280ac42`

Exact executable/pre-evidence QA HEAD:

`84e13cca51c5bceedccd8c74877248c2215c5b3d`

R12-base-to-QA delta is exactly three added files and zero inherited-file modifications:

1. `mobi/p1-b2/geometry/p1_c_dar1_diagnostic_axis_revision_v1.py`
2. `mobi/p1-b2/geometry/test_p1_c_dar1_diagnostic_axis_revision_v1.py`
3. `.github/workflows/mobi-p1-c-dar1-pre-evidence-qa.yml`

The later identity/freeze documents are non-executable records and are excluded from the QA push trigger.

## 3. Frozen executable identities

DAR1 adapter:

- Git blob SHA-1 `d13d191499b6d734845051ba428323fdcf37dabd`
- SHA-256 `2ed9eac016c32a29a855eb26e0006c6e299a9b25d4a843b6cb4f398e6c356450`

DAR1 synthetic tests:

- Git blob SHA-1 `ff49605ea62ac1c346cb9469c038d73da665976c`
- SHA-256 `4e1d129082c8eb54776c3b87a0530f016961c060ef9b69dfe84e280ccd9a231b`

DAR1 pre-evidence QA workflow:

- Git blob SHA-1 `23924ca07dd36ef512c9cf895966bfadcc3feccc`
- SHA-256 `1c35ece2bc276bda8ec1f65bebb78814f32afc753c2a05ccd8bece4ea9274cc3`

Frozen inherited identities remain:

- R12 adapter blob `837f4abe7ff474a527893b099be8087a104f7aaa`
- R12 adapter SHA-256 `fc4096162607dbf59859749562ec5ab9ea7d0e09551aa7cd3cd1ad05e9f5594c`
- assembled R11 SHA-256 `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`
- V3125 mesh-array SHA-256 `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`
- source GLB SHA-256 `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`.

## 4. Exact bounded implementation rule

For every nondegenerate role, DAR1 delegates to the inherited R11 `diagnostic_axis()` exactly.

Only when the frozen hierarchy audit proves all of the following may DAR1 define the `TAIL_ROOT_CTRL` diagnostic tangent from its direct child:

- hierarchy edge count exactly `29`;
- number of edges with length `<=1e-15` exactly `1`;
- that sole edge exactly `PELVIS_CTRL -> TAIL_ROOT_CTRL`;
- fallback role exactly `TAIL_ROOT_CTRL`;
- direct-child set exactly `[TAIL_1_CTRL]`;
- `TAIL_ROOT_CTRL -> TAIL_1_CTRL` vector nonzero.

Frozen continuation tangent:

`[0.0, 0.0090661229202611, -0.08406815248194494]`

Norm:

`0.08455559618696346`

Frozen diagnostic axis:

`[0.0, -0.9942352283349678, -0.10722085029374898]`

No recursive descendant search, no second fallback, no raw `TAIL_PATH_FORWARD` rescue, no world-axis fallback and no choose-the-passing-axis behavior is permitted.

The diagnostic axis remains a structural probe axis only. It is not promoted into production joint-axis truth.

## 5. Pre-evidence QA result

Public QA:

- run `38984440992`
- job `117252505893`
- event `push`
- executable HEAD `84e13cca51c5bceedccd8c74877248c2215c5b3d`
- conclusion **SUCCESS**.

All steps passed, including:

- inherited executable identity gates;
- exact R11 assembly;
- frozen Python/runtime identity;
- inherited R11 synthetic tests;
- inherited R12 synthetic tests;
- DAR1 synthetic tests;
- exact frozen source acquisition;
- seed 1/777 V3125 pre-evidence structural-isolation audit;
- identity/manifest packaging.

Artifact:

- ID `12082611409`
- name `mobi-p1-c-dar1-pre-evidence-qa-38984440992`
- size `2,917,712` bytes
- GitHub digest `sha256:19a2f7a945406be8bf93302fa5c3aa5a80331fe4fc7079e1626400ed996bb933`
- independently downloaded ZIP SHA-256 exactly matched the GitHub digest.

The artifact manifest was independently recomputed from extracted bytes and every listed file matched.

## 6. Determinism and isolation

Seed 1 stage0 audit SHA-256:

`281094895daf60dbe47a99d3cc7464241e2781c61bc3158a052ca4f26c5af6f4`

Seed 777 stage0 audit SHA-256:

`281094895daf60dbe47a99d3cc7464241e2781c61bc3158a052ca4f26c5af6f4`

Deterministic diff:

- bytes `0`
- SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Observed isolation:

- V3125 exact identity PASS;
- control count `30`;
- R12 changed paw-bind count remains exactly `4`;
- non-paw role count unchanged `26`;
- parent/domain/provenance unchanged;
- control snapshot before/after axis audit byte-identical;
- weights before/after axis audit byte-identical;
- domain bleed `0`;
- unweighted vertices `0`;
- changed diagnostic-axis role set exactly `[TAIL_ROOT_CTRL]`;
- all non-tail-root axes exact inherited;
- frozen tangent identity PASS;
- frozen axis identity PASS;
- neutral rest max normalized error `3.0561548317486276e-16`;
- neutral rest RMS normalized error `5.27737336708397e-17`.

## 7. Evidence ceiling

This QA intentionally records:

- `structuralStage1EvidenceExecuted = false`
- `jacobianDerivativeExecuted = false`
- `rasterEvidenceExecuted = false`.

Therefore this freeze proves only that DAR1 is implemented consistently and causally isolated enough to become eligible for a later, separately authorized revised structural Stage-1 run.

It does not rewrite the historical R12 Stage-1 FAIL as PASS.

## 8. Frozen prohibitions

After this freeze, do not mutate the DAR1 adapter, tests or QA workflow in place to improve later evidence.

Do not:

- change geometry or control positions;
- move `TAIL_ROOT_CTRL` or `PELVIS_CTRL`;
- change hierarchy;
- change domains or weights;
- change top-4 rules;
- change `1e-15` degeneracy threshold;
- change Jacobian epsilon/derivative threshold;
- introduce another diagnostic fallback;
- run finite pose, IK, gait or animation as part of this freeze;
- interpret a later mechanical PASS as product-quality proof.

Any executable repair after this point requires explicit new change-control and a new frozen identity.

## 9. Next boundary

After private import and canonical consistency closure, the next possible group is a **separate execution decision for revised DAR1 structural Stage-1 evidence**.

That future run must execute the exact frozen adapter identities above. A FAIL must be preserved and canonicalized before repair. A PASS would authorize only a separately contracted finite-pose discriminator; it would not establish gait, animation or final body quality.
