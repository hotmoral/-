# Mobi P1-C-R11 Post-Failure Diagnostic Result

Date: 2026-10-16
Status: **PASS / CAUSE LOCALIZED / OBSERVATIONAL ONLY**
Decision token: **`R11_DIAGNOSTIC_ALL_PAW_BIND_SURFACE_SEPARATION`**

## Execution identity

- branch: `mobi/run-p1-c-r11-post-failure-diagnostic-20261016`
- execution HEAD: `9d6d8de674c7d164975b0bf0286f8e573cbebe6e`
- run: `38929129248`
- conclusion: **SUCCESS**
- artifact: `12058232236`
- artifact digest: `sha256:d7d1fb4abffd8f4ce05d35feedc8c2c20cbd1715f6d8e167acad1bff7c4556a3`
- diagnostic JSON SHA-256: `9c11d312f9fe32ff458488bf0e6b3f8a304102dbc159d4e2819aaaf827b8f9be`
- seed1 JSON SHA-256: same
- seed777 JSON SHA-256: same
- deterministic diff: empty / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Frozen identity reproduced

- V3125: `3125 V / 6246 F`
- mesh-array SHA-256: `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`
- body height: `0.7489310142118484`
- pitch: `0.0039006823656867104`
- frozen paw-local radius `4*pitch`: `0.015602729462746842`
- original `FORE_L_PAW_CTRL` failure reproduced observationally.

## Four-paw result

All four paw terminals classify identically:

> **`BIND_SURFACE_SEPARATION`**

Cross-side classification:

> **`ALL_PAW_SYSTEMATIC`**

| Paw | nearest surface distance | radius ratio | weighted support | differential support | local support |
|---|---:|---:|---:|---:|---:|
| FORE_L | `0.024423494346825194` | `1.5653347323×` | 95 | 95 | 0 |
| FORE_R | `0.024106946238096297` | `1.5450467366×` | 109 | 109 | 0 |
| HIND_L | `0.021845035958720952` | `1.4000778525×` | 459 | 459 | 0 |
| HIND_R | `0.021287591707225592` | `1.3643504977×` | 380 | 380 | 0 |

For every paw:

- nearest visible V3125 vertex is already outside the frozen `4*pitch` radius;
- therefore the count of V3125 vertices inside that radius is exactly zero;
- consequently local domain eligibility and top-4 competition cannot be the primary cause of the Stage-1 paw-local failure;
- each paw control nevertheless has nonzero weighted and differential support farther away.

## FORE_L exact causal measurements

- bind: `[0.07411296494804749, 0.031205458925493684, 0.19893480065002228]`
- derived sole-anchor mean: `[0.07466864945100886, 0.01625805635038497, 0.19819211480872972]`
- snapped medial endpoint = bind
- sole-anchor mean → snapped endpoint distance: `0.01497615475574603`
- nearest V3125 surface distance from bind: `0.024423494346825194`
- nearest `FORE_L`-domain surface distance: same
- weighted support: `95`
- differential support: `95`
- weighted/differential support within frozen radius: `0`
- nearest supported vertex paw weight: `0.6918368626739805`
- nearest supported vertex normalized derivative: `0.0222548838762092`

The nearest weighted support vertex is itself the nearest visible surface vertex, so no hidden closer eligible surface exists that was merely evicted by top-4.

## Interpretation

The Stage-1 exception was the first role-order failure, not a unique left-side defect. If the audit had continued rather than fail-fast, all four paw terminals would fail the same local-radius requirement.

The frozen construction places paw terminal controls on medial-path endpoints. Under the tested V3125/voxel/skeleton geometry, those endpoints are systematically farther than `4*pitch` from the visible mesh surface.

Therefore the failure is upstream of domain/top-4 competition:

`surface-derived paw region`
→ `medial graph snapping / terminal bind`
→ **bind remains too deep relative to the frozen surface-locality radius**
→ local vertex set is empty
→ paw-local Jacobian gate fails.

This diagnostic does not decide whether the eventual correction should change the visual bind derivation, separate semantic contact points from deformation controls, alter the scaffold representation, or abandon this RF-M construction. Those are change-control choices.

## R11 status remains unchanged

> **R11 Stage 1 remains CLOSED / FAIL / `R11_STAGE1_FAIL_FORE_L_PAW_LOCAL_SUPPORT`.**

Diagnostic PASS means only that the failure mechanism was localized deterministically.

No finite pose, gait, IK, runtime skinning or animation work is authorized.
