# Mobi P1-C R12 — Stage-1 Public Evidence Result

Date: 2026-10-17
Status: **CLOSED / FAIL / STRUCTURAL EVIDENCE ENTERED**

Result token:

> **`R12_STAGE1_FAIL_INHERITED_TAIL_ROOT_ZERO_DIAGNOSTIC_TANGENT`**

## 1. Scope

This document records the fresh remediated R12 Stage-1 execution only.

It does not rewrite the historical first R12 attempt, which remains classified separately as:

> `R12_STAGE1_PRE_EVIDENCE_HARNESS_FAIL_DYNAMIC_IMPORT_REGISTRATION`

The fresh run used the canonically reviewed loader-remediated Stage-0 identity and entered the real V3125 structural-evidence region.

## 2. Exact execution identity

Repository:

`hotmoral/-`

Workflow:

`Mobi P1-C R12 Surface-Terminal Bind Stage-1 Evidence`

Execution branch:

`mobi/run-p1-c-r12-surface-terminal-bind-20261017`

Exact execution HEAD:

`4dbc13f67c0097e5bb84fd2b0ec27d71c280ac42`

Workflow blob:

`8918c48e6330b493c15e9fb41c6b5b741ee5f698`

Run:

- run `38954480605`
- job `117153764956`
- event `workflow_dispatch`
- conclusion **FAILURE**.

Artifact:

- ID `12070371133`
- name `mobi-p1-c-r12-surface-terminal-bind-38954480605`
- bytes `2946719`
- digest `sha256:ffc8e9c99f2c7676169d021cf04846f79e1d5a59139816261283d510887461a0`.

Independent artifact recheck after download confirmed the ZIP SHA-256 above.

## 3. Gates passed before structural failure

The fresh run passed:

1. exact execution-branch and authorization-token gate;
2. remediated Stage-0 blob identity gate;
3. exact assembled frozen R11 SHA-256:
   `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`;
4. Python `3.12.15` and frozen dependency versions;
5. inherited R10/R11 blob gates;
6. inherited R11 synthetic tests `8 / 8`;
7. unchanged R12 synthetic tests `4 / 4`;
8. exact standing-cat source acquisition and SHA-256;
9. exact V3125 reproduction under `PYTHONHASHSEED=1` and `777`;
10. V3125 mesh-array SHA-256:
    `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`.

Therefore this execution is valid structural evidence rather than a pre-evidence harness failure.

## 4. Seed execution result

Both frozen structural executions returned the same nonzero exit code:

```json
{
  "seed1ExitCode": 1,
  "seed777ExitCode": 1
}
```

Both logs terminate with the same exception:

```text
RuntimeError: zero diagnostic tangent TAIL_ROOT_CTRL
```

The seed-1 and seed-777 failure logs are byte-identical.

All partial evidence files generated before failure are also byte-identical between the two seeds:

- `medial_graph.json`
- `semantic_paths.json`
- `r11_medial_paw_endpoints.json`
- `r12_surface_terminal_aliases.json`
- `r12_delta_audit.json`.

The artifact manifest contains 16 entries; independent post-download verification found `0` manifest mismatches.

## 5. R12 causal-delta audit passed

Before the failure, both seeds produced the same R12 delta audit:

- role count: `30`;
- changed role count: `4`;
- unchanged non-paw role count: `26`;
- parent/domain/provenance unchanged: `true`.

Exactly these roles changed active bind coordinate:

- `FORE_L_PAW_CTRL`
- `FORE_R_PAW_CTRL`
- `HIND_L_PAW_CTRL`
- `HIND_R_PAW_CTRL`.

No tail control coordinate was changed by R12.

## 6. Exact four-paw surface aliases produced

The deterministic V3125 surface aliases were:

| Role | V3125 vertex | Surface-bind R10 position | Medial→surface distance |
|---|---:|---|---:|
| `FORE_L_PAW_CTRL` | `1338` | `[0.06441181153059006, 0.007175602484494448, 0.19632242619991302]` | `0.026045553909864582` |
| `FORE_R_PAW_CTRL` | `146` | `[-0.06608831137418747, 0.00617956044152379, 0.20751623809337616]` | `0.026694571133613273` |
| `HIND_L_PAW_CTRL` | `2277` | `[0.08790043741464615, 0.0050377328880131245, -0.17178253829479218]` | `0.022365006001253098` |
| `HIND_R_PAW_CTRL` | `826` | `[-0.08211533725261688, 0.005899150390177965, -0.1699567586183548]` | `0.02277643690275294` |

Candidate counts were respectively `28 / 35 / 27 / 28`.

The alias derivation remained exactly:

> `FROZEN_SOLE_CANDIDATE_ARGMIN_DISTANCE_THEN_GLOBAL_VERTEX_INDEX`

## 7. What passed for the paw revision before tail failure

The R12 execution order is significant.

Before `jacobian_audit()` is called, the implementation completes:

- six-domain derivation;
- weight construction;
- global weight audit;
- `alias_semantic_weight_gate()` for all four paws;
- neutral rest identity check.

The run reached `jacobian_audit()`, so all of those gates completed without exception.

Inside the inherited frozen R11 `jacobian_audit()`, roles are visited in frozen `ROLE_ORDER[1:]`. All fore/hind roles, including all four paw controls, occur before `TAIL_ROOT_CTRL`.

The frozen audit would fail immediately if any paw had:

- no differential support;
- domain bleed;
- no support within frozen `4*pitch` of its R12 surface bind.

Instead execution reached `TAIL_ROOT_CTRL`.

Therefore the fresh R12 run establishes, under the frozen ordering and fail-fast semantics, that **all four revised paw controls passed their inherited differential-support/domain/paw-locality gates before the tail-root failure was encountered**.

This is an important bounded positive result for the intended R12 paw change, but it is not a full R12 Stage-1 PASS.

## 8. Exact failure mechanism

Frozen R11 hierarchy defines:

```text
TAIL_ROOT_CTRL parent = PELVIS_CTRL
```

Frozen `diagnostic_axis(role, controls_by_role)` defines a parented control's tangent as:

```text
tangent = control.position - parent.position
```

and fails if:

```text
norm(tangent) <= 1e-15
```

The fresh structural evidence shows:

- `PELVIS_FOREQUARTER` semantic path starts at
  `[0.0, 0.2925511774265033, -0.08581501204510761]`;
- `TAIL` semantic path also starts at
  `[0.0, 0.2925511774265033, -0.08581501204510761]`.

Under frozen R11 `make_controls()` those starts define:

- `PELVIS_CTRL` at the pelvis semantic graph node;
- `TAIL_ROOT_CTRL` at the tail-root semantic graph node.

For this exact V3125 reproduction the two nodes are coincident, so:

```text
TAIL_ROOT_CTRL.position - PELVIS_CTRL.position = [0, 0, 0]
```

and the inherited diagnostic-axis construction has no direction.

Exact failure:

> **`zero diagnostic tangent TAIL_ROOT_CTRL`**

## 9. Causal interpretation

This failure is **not caused by the four R12 paw surface-bind substitutions**:

- R12 changed exactly four paw coordinates;
- all 26 non-paw control coordinates are unchanged;
- `TAIL_ROOT_CTRL` is unchanged;
- `PELVIS_CTRL` is unchanged;
- their parent relationship is inherited from R11;
- the frozen R11 Stage-1 run failed earlier at `FORE_L_PAW_CTRL`, so its fail-fast Jacobian loop never reached `TAIL_ROOT_CTRL`.

The R12 paw revision removed the earlier paw-locality blocker far enough for execution to expose a second, previously masked inherited condition.

The demonstrated problem is specifically:

> **an inherited coincident `PELVIS_CTRL → TAIL_ROOT_CTRL` parent edge makes the current frozen diagnostic-axis rule undefined.**

This result alone does **not** establish that the tail-root control has no weight support or that fixed-topology tail deformation is infeasible. The audit fails while constructing the diagnostic axis, before it can test `TAIL_ROOT_CTRL` derivative support.

Accordingly, the failure is classified as:

> **`R12_STAGE1_FAIL_INHERITED_TAIL_ROOT_ZERO_DIAGNOSTIC_TANGENT`**

rather than a paw-locality failure or a demonstrated dead-tail-control failure.

## 10. What remains unresolved

Because Stage 1 stops at `TAIL_ROOT_CTRL`, this run does not complete:

- `TAIL_ROOT_CTRL` derivative-support measurement;
- remaining tail-control Jacobian audit;
- tail weighted-arc ordering/overlap audit;
- primary neutral raster evidence;
- all-37-yaw neutral raster identity;
- final weight/scaffold/jacobian summary emission.

Therefore full R12 scaffold feasibility remains unproven.

## 11. No-retuning rule

Do not change any frozen numerical threshold in response to this failure.

In particular, do not change:

- `4*pitch`;
- Jacobian epsilon;
- derivative threshold;
- top-4;
- `sigma=2*pitch`;
- domain/interface rules;
- V3125;
- the paw alias derivation.

Do not mutate the existing failed R12 hypothesis in place.

## 12. Disposition

Fresh R12 Stage 1 is:

> **CLOSED / FAIL**

with exact result token:

> **`R12_STAGE1_FAIL_INHERITED_TAIL_ROOT_ZERO_DIAGNOSTIC_TANGENT`**

The intended paw-locality revision produced bounded positive evidence, but the overall checkpoint is not PASS because a previously masked inherited tail-root diagnostic degeneracy prevents completion.

The next legal activity is private consistency import and then a separate post-R12 change-control/diagnostic-design decision. No immediate code repair or rerun is authorized by this result document.
