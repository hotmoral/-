# Mobi P1-C-R11 — Public Handoff

Date: 2026-10-16
Status: **R11 STAGE-1 CLOSED / FAIL**
Decision token: **`R11_STAGE1_FAIL_FORE_L_PAW_LOCAL_SUPPORT`**

## Current public identity

- branch: `mobi/run-p1-c-r11-semantic-scaffold-20261016`
- frozen Stage-1 execution HEAD: `4c695503b99974e929491b1e78b0cf2935b675c7`
- first Stage-1 run: `38925709826`
- job: `117056590753`
- result: **FAILURE**
- uploaded evidence artifact: **none; fail-fast occurred before upload**
- deterministic V3125 mesh-array SHA-256: `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`
- failure-result commit: `5a3fbd94528ac26586ad50c728a9a5f1d625e900`

## What passed

Stage-0 blob identities, frozen implementation SHA, exact dependencies, inherited R10 identities, 8 synthetic tests, source SHA, frame/sign assumptions already frozen in Stage 0, and two-seed V3125 identity reproduction all passed.

## Exact failure

The first full Stage-1 execution stopped in the Jacobian/non-vacuity audit with:

```text
RuntimeError: paw terminal lacks local support FORE_L_PAW_CTRL
```

The preceding generic dead-control check did not fail, so the left fore-paw terminal had differential support somewhere but no support vertex satisfied the frozen `<= 4*pitch` paw-local criterion.

## Interpretation

This is an R11 scaffold/weight/non-vacuity hypothesis failure, not a failure of the accepted V3125 neutral cat, source acquisition, environment, deterministic reduction, or coordinate-sign gate.

Do not retune the frozen Stage-0 constants in place. Do not rerun merely after changing thresholds. Any revised structural hypothesis requires explicit change control.

## Execution routing note

GitHub workflow dispatch required the workflow path to exist on the public default branch. The exact frozen workflow blob was therefore registered byte-identically on `main` at commit `916c5843933c60184d57de645eba2ff458048a3c` without modifying the frozen R11 experiment branch before execution.

One-shot relay:

- branch `mobi/ops-r11-stage1-dispatch-20261016`
- commit `e2aa68f8fb07375bb4cc6c9e7bf3f9a9564a0308`
- run `38925467973`
- attempt 1: HTTP 404 before default-branch registration
- attempt 2: SUCCESS

This routing work is operational only and does not alter the Stage-1 result.

## Exact next boundary

> **Post-R11 failure diagnosis / change-control — ELIGIBLE / NOT STARTED.**

Recommended diagnostic question:

> Why does `FORE_L_PAW_CTRL` have nonzero support yet no support within the frozen `4*pitch` local-paw radius?

A diagnostic may measure medial endpoint depth, nearest visible-surface distance, local domain assignment and top-4 influence competition. It must not mutate R11 or reinterpret this failed run as PASS.

No finite pose, animation, gait, IK, runtime skinning selection, P1-G/P1-H or downstream work is authorized at this boundary.
