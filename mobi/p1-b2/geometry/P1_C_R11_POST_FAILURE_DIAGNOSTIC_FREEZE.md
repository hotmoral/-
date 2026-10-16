# Mobi P1-C-R11 Post-Failure Diagnostic Freeze

Date: 2026-10-16
Status: **FROZEN / PRE-EVIDENCE / OBSERVATIONAL ONLY**
Token: **`R11_POST_FAILURE_DIAGNOSTIC_IMPLEMENTATION_FREEZE`**

## Frozen base

- public parent state: `4ce94fa9c07f0f86b0380c58cdacaf59481732c2`
- frozen failed R11 execution HEAD retained in history: `4c695503b99974e929491b1e78b0cf2935b675c7`
- frozen R11 assembled SHA-256: `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`
- deterministic V3125 SHA-256: `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`

## Diagnostic-only additions

- diagnostic script: `mobi/p1-b2/geometry/p1_c_r11_post_failure_diagnostic_v1.py`
- diagnostic script git blob: `d26fd0027782d7633ba1c8c19be75e41dccb6e0f`
- workflow: `.github/workflows/mobi-p1-c-r11-post-failure-diagnostic.yml`
- workflow git blob: `61143ed0f07dbe9ba9cdd7cb7923812067e707ee`

The first script candidate was corrected before evidence only to register the dynamically loaded frozen R11 module in `sys.modules`, which is required for safe execution of dataclass definitions. No R11 measurement formula, constant, threshold, domain rule, control rule or weight rule changed.

## Execution authorization token

`RUN_R11_POST_FAILURE_DIAGNOSTIC_AFTER_FREEZE`

The workflow is `workflow_dispatch` only and additionally requires the exact diagnostic branch.

## Frozen diagnostic scope

The script may only:

1. reproduce exact V3125 using frozen R11 code;
2. reproduce frame, voxel skeleton, semantic paths, 30 controls, domains and weights;
3. inspect all four paw controls without calling the fail-fast R11 Stage-1 audit as the primary reporting path;
4. calculate the predeclared bind/local/domain/top-4/differential-support measurements;
5. classify the failure using only the predeclared diagnostic labels;
6. run twice under seeds 1 and 777 and require byte-identical JSON.

## Prohibition

No frozen R11 implementation part may be changed on this branch after this freeze in response to evidence. No diagnostic threshold may be added after evidence. Any execution failure is retained first and reviewed before any code change.
