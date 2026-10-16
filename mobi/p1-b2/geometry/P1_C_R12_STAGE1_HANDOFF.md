# Mobi P1-C R12 — Stage-1 Public Handoff

Date: 2026-10-17
Status: **CLOSED / FAIL / AWAITING PRIVATE IMPORT**

## 1. Exact current public result

R12 fresh remediated Stage-1 execution:

- execution HEAD: `4dbc13f67c0097e5bb84fd2b0ec27d71c280ac42`
- run: `38954480605`
- job: `117153764956`
- result: **FAILURE**
- artifact: `12070371133`
- artifact digest: `sha256:ffc8e9c99f2c7676169d021cf04846f79e1d5a59139816261283d510887461a0`
- exact failure token: **`R12_STAGE1_FAIL_INHERITED_TAIL_ROOT_ZERO_DIAGNOSTIC_TANGENT`**.

Primary result document:

`mobi/p1-b2/geometry/P1_C_R12_STAGE1_RESULT.md`

## 2. Do not confuse the two R12 Stage-1 attempts

Historical attempt #1:

- run `38953040299`
- HEAD `7d5a33648eeefe954bf1166923d9993e86a715c3`
- classification `R12_STAGE1_PRE_EVIDENCE_HARNESS_FAIL_DYNAMIC_IMPORT_REGISTRATION`
- no structural evidence entered.

Fresh remediated attempt #2:

- run `38954480605`
- HEAD `4dbc13f67c0097e5bb84fd2b0ec27d71c280ac42`
- real source/V3125 structural evidence entered;
- failed at inherited `TAIL_ROOT_CTRL` diagnostic-axis construction.

## 3. What R12 paw work demonstrated before the failure

The fresh run passed exact V3125 identity, unchanged synthetic tests and all pre-Jacobian R12 gates.

Its delta audit confirms exactly four changed roles and 26 unchanged non-paw roles.

Because the inherited Jacobian audit reached `TAIL_ROOT_CTRL`, every preceding fore/hind role—including all four revised paw controls—passed the frozen fail-fast derivative/domain/paw-locality conditions.

Therefore the original R11 paw-locality blocker was no longer the first failing condition under R12.

This is bounded positive evidence only; it is not full Stage-1 PASS.

## 4. Current blocker

`PELVIS_CTRL` and `TAIL_ROOT_CTRL` resolve to the same V3125-derived semantic graph location:

`[0.0, 0.2925511774265033, -0.08581501204510761]`

The frozen inherited hierarchy is:

`PELVIS_CTRL → TAIL_ROOT_CTRL`

The frozen diagnostic tangent for a parented role is:

`control.position - parent.position`

so the tail-root tangent is exactly zero and the audit raises:

`RuntimeError: zero diagnostic tangent TAIL_ROOT_CTRL`

R11 never exposed this because its fail-fast audit stopped earlier at `FORE_L_PAW_CTRL`.

## 5. Determinism / artifact integrity

- both structural seeds exit `1`;
- both failure logs are byte-identical;
- all five partial per-seed evidence files are byte-identical;
- artifact manifest has 16 entries;
- independent manifest verification: 16/16 PASS;
- independent ZIP SHA matches GitHub artifact digest.

## 6. Stop boundary

Do **not**:

- rerun R12;
- change tail hierarchy;
- substitute a different diagnostic axis;
- move `TAIL_ROOT_CTRL`;
- change any threshold/radius/domain/weight rule;
- start finite pose, IK, gait or animation.

The next legal step is:

> **private import / consistency review of the exact R12 Stage-1 failure**

After canonical closure, a separate post-R12 change-control must decide whether the coincident tail-root parent edge is a scaffold-geometry problem, a diagnostic-axis-definition problem, or requires another bounded observational diagnostic. No repair is selected by this handoff.
