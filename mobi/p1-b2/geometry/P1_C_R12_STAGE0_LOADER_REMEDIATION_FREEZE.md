# Mobi P1-C-R12 — Stage-0 Loader Remediation Freeze

Date: 2026-10-17
Status: **FROZEN / PRE-EVIDENCE REMEDIATION PASS / STRUCTURAL EVIDENCE NOT ENTERED**

Remediation token:

> **`R12_STAGE0_LOADER_REMEDIATION_FROZEN_PRE_EVIDENCE_PASS`**

## 1. Why this remediation exists

The first R12 Stage-1 public run was:

- run `38953040299`
- job `117148935288`
- execution HEAD `7d5a33648eeefe954bf1166923d9993e86a715c3`
- conclusion `FAILURE`.

The run passed checkout, Stage-0 identity, exact assembled R11 bytes, frozen runtime and inherited R10/R11 identity. All 8 inherited R11 synthetic tests passed.

The R12 synthetic suite then failed during `setUpClass` before any real-source or V3125 evidence step. The exact failure came from `load_r11()` executing a dynamically created Python module before registering it in `sys.modules`, causing Python 3.12 dataclass processing to fail.

Classification:

> **`R12_STAGE1_PRE_EVIDENCE_HARNESS_FAIL_DYNAMIC_IMPORT_REGISTRATION`**

This is not an R12 structural-hypothesis failure.

## 2. Evidence boundary of the failed run

Run `38953040299` did **not** execute:

- source acquisition;
- V3125 reproduction/identity gate;
- real V3125 surface-terminal alias derivation;
- domain / own-weight paw gates;
- Jacobian paw-local support;
- seed 1 structural evidence;
- seed 777 structural evidence;
- deterministic structural comparison.

The small always-uploaded artifact only records environment/manifest material and does not constitute R12 structural evidence.

Artifact:

- ID `12069228184`
- name `mobi-p1-c-r12-surface-terminal-bind-38953040299`
- digest `sha256:a53efee6a46a8fdd84a9a599035dcfeed520a064d377c257ac98cd9f222d2095`.

## 3. Canonically authorized code delta

Private change control authorized exactly two inserted lines of semantic effect:

1. `import sys`
2. `sys.modules[spec.name] = mod` immediately before `spec.loader.exec_module(mod)`.

Public compare from initial frozen Stage-0 HEAD `7d5a33648eeefe954bf1166923d9993e86a715c3` to remediation implementation commit `3b1297a4c52dabd791ceb2d960709165a5c487f0` is exactly:

- one modified file;
- `+2 / -0` lines;
- no other file change.

No numerical, geometry, domain, weighting, radius, hierarchy, acceptance or test semantics changed.

## 4. Remediated adapter identity

Path:

`mobi/p1-b2/geometry/p1_c_r12_surface_terminal_bind_alias_v1.py`

Remediated frozen identity:

- byte count: `16883`
- SHA-256: `fc4096162607dbf59859749562ec5ab9ea7d0e09551aa7cd3cd1ad05e9f5594c`
- Git blob SHA-1: `837f4abe7ff474a527893b099be8087a104f7aaa`
- version remains `P1_C_R12_SURFACE_TERMINAL_BIND_ALIAS_V1`.

The initial pre-remediation adapter identity remains historical and must not be reused for a new Stage-1 dispatch.

## 5. Pre-evidence verification

A separate verification-only branch was used so the remediation execution branch remained free of verification workflow files.

Verification run:

- branch `mobi/verify-r12-stage0-loader-remediation-20261017`
- HEAD `84c1e1a43e69971fa87542e7ef54279de4e73428`
- run `38953786641`
- result **SUCCESS**.

The verification did not acquire the cat source and did not generate V3125 structural evidence.

It verified:

- Python `3.12.15`;
- frozen dependency family unchanged;
- assembled R11 SHA-256 `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`;
- inherited R11 synthetic tests: `8 / 8 PASS`;
- unchanged R12 synthetic tests: `4 / 4 PASS`;
- remediated adapter byte/hash/blob identity above.

## 6. Unchanged frozen R12 semantics

The following remain exactly as before remediation:

- V3125 expected SHA `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`;
- 30 roles and hierarchy;
- only four paw active binds may differ from R11;
- 26 non-paw control positions unchanged;
- medial semantic paths unchanged;
- six visible domains unchanged;
- paw quadrant definitions unchanged;
- sole rule `y <= quadrantYMin + 0.035*h` unchanged;
- alias selection `(squaredDistanceToSoleMean, globalVertexIndex)` unchanged;
- inverse-distance weights unchanged;
- `sigma = 2*pitch` unchanged;
- top-4 unchanged;
- normalized weighting unchanged;
- paw-local radius exactly `4*pitch` unchanged;
- Jacobian epsilon/threshold unchanged;
- canonical/contact semantics unchanged;
- `+X_R10 = anatomical left` unchanged;
- source hash and dependency versions unchanged;
- R12 synthetic test file unchanged;
- Stage-1 workflow logic unchanged.

## 7. Freeze relationship

`P1_C_R12_STAGE0_IMPLEMENTATION_FREEZE.md` remains the historical original Stage-0 contract/freeze record.

This remediation freeze **supersedes only the executable adapter identity** recorded in that original document. It does not supersede or weaken any R12 numerical, semantic, scope, non-goal, acceptance or determinism rule.

The companion `P1_C_R12_STAGE0_IDENTITY.json` is updated to the remediated adapter identity and references this remediation record.

## 8. Disposition

Remediation is:

> **CLOSED / FROZEN / PRE-EVIDENCE PASS**

A fresh R12 Stage-1 workflow dispatch may become eligible only after private consistency import and canonical STATUS/HANDOFF synchronization.

Do not use GitHub's rerun mechanism on failed run `38953040299`, because that would execute the historical pre-remediation HEAD. A fresh dispatch must target the remediated execution-branch HEAD after canonical review.
