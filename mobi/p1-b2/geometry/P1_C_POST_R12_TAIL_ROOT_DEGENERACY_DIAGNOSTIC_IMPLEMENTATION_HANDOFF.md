# Mobi P1-C — Post-R12 Tail-Root Diagnostic Implementation Handoff

Date: **2026-10-17**  
Status: **IMPLEMENTATION FROZEN / PRE-EVIDENCE PASS / AWAITING PRIVATE IMPORT**

## Exact identities

Public repository: `hotmoral/-`

Branch:

`mobi/run-p1-c-post-r12-tail-root-diagnostic-20261017`

R12 base:

`4dbc13f67c0097e5bb84fd2b0ec27d71c280ac42`

Final executable pre-freeze HEAD:

`e6b94f3d318ded465af437c8c90210e12e8167c4`

Identity commit:

`d5c585f6c5fdd3611702c0f01f4deab14921e54b`

Implementation-freeze commit:

`91ea9fe23b179589461ba78ccdd76d8006e8c530`

Freeze token:

`POST_R12_TAIL_ROOT_DEGENERACY_DIAGNOSTIC_IMPLEMENTATION_FREEZE`

## Final QA authority

Run `38976599230`, job `117227429393`, HEAD `e6b94f3d...` — **SUCCESS**.

- R11 tests: `8/8 PASS`
- R12 tests: `4/4 PASS`
- post-R12 diagnostic tests: `8/8 PASS`
- dispatch-only evidence workflow guard: PASS
- pre-evidence no-source-acquisition guard: PASS
- structural source acquired: **NO**
- structural evidence entered: **NO**

Historical QA #1 `38976274333` failed only because the pre-evidence source guard matched its own literal grep pattern. It did not acquire source data or enter structural evidence. QA #2 and final QA #3 passed after bounded guard remediation.

## Frozen new executable identities

| File | Git blob | SHA-256 | Bytes |
|---|---|---|---:|
| `p1_c_post_r12_tail_root_degeneracy_diagnostic_v1.py` | `d5f006bab21fb1c022fb4a67011b5be9b7a0306e` | `5cb8297d6f47fe16a5cf80f5bb6d18bbe6a891ffa44b5d9ccba8e992424c4367` | 32200 |
| `test_p1_c_post_r12_tail_root_degeneracy_diagnostic_v1.py` | `79afe96c4d31e32010c22f55916177ab185d7b8a` | `41cca69cac39990f740ddff18ec46bc82408be86be691640c231194a0463b07f` | 8406 |
| pre-evidence QA workflow | `b1fe94d43989bc7d0f2340362241eeb31ab8fa16` | `704e636c5977c731bd510c46b1e24dd1e9b8d629f08e2c97a0f45cbb6fcf2f18` | 7229 |
| future evidence workflow | `7c32f77fc04dcb8436bb704bdfc524b26357e85f` | `e418f958cd83a740a6b51339e576ae6799754637ac99fc93283a4355764ebb0c` | 9506 |

## Frozen inherited authority

- R11 assembled SHA-256: `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`
- R12 adapter SHA-256: `fc4096162607dbf59859749562ec5ab9ea7d0e09551aa7cd3cd1ad05e9f5594c`
- R12 adapter blob: `837f4abe7ff474a527893b099be8087a104f7aaa`
- source SHA-256: `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- V3125 SHA-256: `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`

## Frozen diagnostic question

No repair is selected. The diagnostic only distinguishes whether the inherited pelvis/tail-root coincidence is:

1. localized branch-root diagnostic-axis singularity with non-vacuous tail support;
2. broader tail support/control defect;
3. broader zero-length hierarchy degeneracy;
4. unresolved.

Exactly two root counterfactual probes exist:

- `TAIL_ROOT_TO_TAIL_1`
- `TAIL_PATH_FORWARD`

Classification precedence remains frozen before evidence.

## Evidence state

`diagnosticEvidenceRunAuthorized = false`

No structural diagnostic run exists yet.

The future evidence workflow is `workflow_dispatch` only and requires:

`RUN_POST_R12_TAIL_ROOT_DIAGNOSTIC_AFTER_PRIVATE_IMPORT`

Do not dispatch it before private canonical import/consistency closure. If GitHub workflow registration requires a default-branch copy, perform only a byte-identical registration step after private authorization; do not alter the frozen diagnostic implementation/workflow.

## Next boundary

1. private canonical import and consistency review;
2. STATUS/HANDOFF sync and canonical promotion;
3. then, in a separate intentional group, public workflow registration/dispatch;
4. evidence/result review;
5. only then choose any tail-root repair hypothesis.

Finite pose, IK, gait and animation remain unauthorized.
