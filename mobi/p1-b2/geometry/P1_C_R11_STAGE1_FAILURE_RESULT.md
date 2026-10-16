# Mobi P1-C-R11 — Stage-1 Failure Result

Date: 2026-10-16
Status: **CLOSED / FAIL / FROZEN HYPOTHESIS FALSIFIED AT PAW-LOCAL SUPPORT GATE**
Decision token: **`R11_STAGE1_FAIL_FORE_L_PAW_LOCAL_SUPPORT`**

## 1. Scope

This record closes the first authorized R11 Stage-1 public evidence execution against the immutable Stage-0 hypothesis. No Stage-0 structural constant was changed after evidence. No finite Mobi pose, gait, animation, IK, planted-paw motion solve, production rig decision or Android runtime implementation was produced.

## 2. Frozen execution identity

- repository: `hotmoral/-`
- branch: `mobi/run-p1-c-r11-semantic-scaffold-20261016`
- execution HEAD: `4c695503b99974e929491b1e78b0cf2935b675c7`
- workflow: `.github/workflows/mobi-p1-c-r11-semantic-scaffold.yml`
- workflow blob: `0bd5e0444bb01625917a18eaa255d9e0fe27cfef`
- Stage-0 implementation SHA-256: `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`
- Stage-1 run: `38925709826`
- Stage-1 job: `117056590753`
- event: `workflow_dispatch`
- result: **FAILURE**

The dispatch was authorized with the already frozen token `RUN_R11_STAGE1_AFTER_STAGE0_FREEZE` and executed on the exact frozen R11 branch.

## 3. Execution-routing note

The initial one-shot relay attempt discovered a GitHub registration constraint: the R11 workflow existed only on the experiment branch and therefore the workflow-dispatch endpoint returned HTTP 404 because the workflow path was not registered on the repository default branch.

This was an execution-routing issue only, not Stage-1 evidence.

To resolve it without changing the frozen R11 branch or workflow bytes:

- the exact same workflow blob `0bd5e0444bb01625917a18eaa255d9e0fe27cfef` was registered on public default branch `main`;
- default-branch registration commit: `916c5843933c60184d57de645eba2ff458048a3c`;
- one-shot relay branch: `mobi/ops-r11-stage1-dispatch-20261016`;
- relay commit: `e2aa68f8fb07375bb4cc6c9e7bf3f9a9564a0308`;
- relay run: `38925467973`;
- attempt 1: FAIL / HTTP 404 before default-branch registration;
- attempt 2: SUCCESS / workflow_dispatch accepted.

The actual Stage-1 execution still checked out frozen R11 HEAD `4c695503...`; the registration/relay path did not modify any Stage-0 constant or experiment code.

## 4. Gates that passed before structural evidence

The following all passed:

1. exact branch + explicit authorization token;
2. Stage-0 freeze document presence/token;
3. all frozen blob identities in `P1_C_R11_STAGE0_IDENTITY.json`;
4. exact assembled implementation byte count and SHA-256;
5. Python `3.12.15`;
6. `numpy==2.5.4`;
7. `fast-simplification==0.2.0`;
8. `trimesh==4.11.1`;
9. `scikit-image==0.26.0`;
10. `scipy==1.17.0`;
11. inherited R10 reducer / Stage-D raster / Stage-B inspector blob identities;
12. all 8 Stage-0 synthetic contract tests;
13. frozen standing-cat source download and SHA-256;
14. deterministic V3125 reproduction under `PYTHONHASHSEED=1` and `777`;
15. exact reproduced topology `3125 V / 6246 F`.

## 5. Newly established V3125 mesh identity

Both identity-only reproductions produced the same frozen mesh-array identity:

> **`839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`**

This is now the observed deterministic mesh-array SHA-256 for the frozen R10 reproduction recipe under the R11 serialization contract.

No scaffold parameter was chosen or altered based on this hash.

## 6. Exact Stage-1 failure

The first full frozen Stage-1 execution reached:

`reproduce V3125`
→ `frame/sign hard gate`
→ `voxel / medial graph`
→ `semantic graph / controls`
→ `six-domain derivation`
→ `weights`
→ `weight audit`
→ `neutral rest LBS`
→ **Jacobian / non-vacuity audit**

and then stopped with:

```text
RuntimeError: paw terminal lacks local support FORE_L_PAW_CTRL
```

The failing check is the frozen requirement that a paw terminal control have nonzero differential support on at least one surface vertex within `4 * pitch` of that paw control bind.

The control was not rejected by the preceding generic `dead control` check. Therefore the observed failure is more specific than an entirely zero-weight control: `FORE_L_PAW_CTRL` had differential support somewhere, but none satisfied the frozen local-paw proximity criterion.

## 7. Mechanical interpretation

This run is a **real Stage-1 hypothesis failure**, not an environment or input-identity failure.

What is established:

- R10/V3125 reproduction is deterministic and stable;
- the source/frame/input identities are valid;
- the frozen implementation is the intended Stage-0 implementation;
- the scaffold proceeds far enough to construct domains, controls and weights;
- the left fore-paw terminal fails the required local-support non-vacuity gate.

What this run does **not** yet distinguish:

- whether the dominant cause is medial-path endpoint depth relative to the visible paw surface;
- domain assignment around the paw;
- top-4 weight competition among same-domain controls;
- or a combination of those frozen design choices.

Those causal subcases may be measured by a post-failure diagnostic, but the diagnostic may not retroactively turn this run into PASS.

## 8. Why no evidence artifact exists

The workflow was deliberately fail-fast. The failure occurred during the first full Stage-1 evidence generation command, before environment-manifest and `upload-artifact` steps. Therefore run `38925709826` has no uploaded artifact.

The authoritative evidence for this failure is the GitHub Actions run/job log plus the immutable execution HEAD and blob identities listed above.

This absence is not permission to rerun with altered constants merely to obtain an artifact.

## 9. Frozen-hypothesis consequence

Do **not** respond to this result by silently changing any of:

- paw support radius;
- voxel resolution or padding;
- skeletonization method;
- surface-anchor rule;
- graph snapping;
- control count or parentage;
- fore-paw endpoint placement rule;
- domain gating;
- weight kernel;
- top-4 rule;
- Jacobian threshold;
- frame/LR sign.

Any material change requires explicit post-R11 change control / a new bounded checkpoint.

An unchanged rerun is not expected to add information; the deterministic frozen inputs would exercise the same failing hypothesis.

## 10. Product / architecture interpretation

This failure does **not** reject V3125 as the neutral feline morphology authority. The accepted visible cat remains unchanged.

It rejects only the tested Stage-1 claim that the exact frozen RF-M scaffold/weight/non-vacuity construction is sufficient as-is.

Therefore:

- `R10_QUALITY_HEADROOM_V3125_F6246` remains neutral morphology authority;
- the exact 30-role R11 Stage-1 implementation does not pass feasibility;
- no finite pose deformation is authorized from this failed scaffold;
- no animation/gait work is authorized;
- P1-G/P1-H/downstream remain unauthorized.

## 11. Exact next boundary

> **Post-R11 failure diagnosis / change-control — ELIGIBLE.**

A bounded diagnostic may measure why `FORE_L_PAW_CTRL` missed its local-support gate using the frozen failed implementation and exact V3125 identity. It must be observational only and must not mutate the failed hypothesis.

After diagnosis, any revised scaffold/weight hypothesis requires explicit new change control before new evidence.
