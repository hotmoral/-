# Mobi P1-C-R10 — Public Morphology Reduction Handoff

Date: 2026-10-16
Status: **GROUP CLOSED / PUBLIC EVIDENCE COMPLETE / PRIVATE IMPORT PENDING**
Public repo: `hotmoral/-`
Public branch: `mobi/run-p1-c-r10-morphology-reduction-20261016`

## 1. Recovery order

Resolve branch remote HEAD, then read:

1. `P1_C_R10_DIRECT_EVIDENCE_REVIEW.md`
2. `P1_C_R10_FINAL_RESULT.md`
3. this handoff

For the source/projection baseline, recover the prior `mobi/experiment-3d-cat-projection-feasibility-20261016` handoff only as needed.

## 2. Entry authority

Private canonical baseline before this public group:

- repo `hotmoral/Mobi`
- branch `p1-motion-morphology-foundation`
- HEAD `7b33ed8b632fd4cc9f307cb664f870f103846e0a`
- selected family `RF_L_REFERENCE_3D_SOURCE_DERIVED_MORPHOLOGY_REDUCTION`
- R10 eligible only after fresh contract/preflight.

Private contract/preflight working branch:

`p1-c-r10-morphology-reduction-contract-20261016`

Private GitHub Actions were not used.

## 3. Frozen source

- Innerscene `Standing cat`
- `cat-original.glb`
- CC0
- SHA-256 `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- structural node `Cat continuous body`
- 99,642 vertices / 199,280 triangles

## 4. Frozen reduction principle

R10 is topology-aware triangle-mesh reduction, not point-cloud deletion.

Simplifier:

- `fast-simplification==0.2.0`
- QEM collapse history
- intermediate tiers reconstructed from prefixes of one collapse history per lane

Broad vertex ladder:

99,642 → 50,000 → 25,000 → 12,500 → 6,250 → 3,125 → 1,560 → 780.

Primary lane:

- Lane A `agg=7.0`

Control lane:

- Lane B `agg=0.0`; could only reach 82,703 vertices and was therefore non-discriminating for the target range.

## 5. Broad run identity

- run `38897708802` — SUCCESS
- job `116962078574`
- HEAD `31a33045997aacfcd90a8120c8683fef32f4b75d`
- artifact `12045305614`
- digest `sha256:a52fead3dfca8028e17857b7ff038f8449ffd425b52cec295d3c109691cf5769`

Broad relevant result:

- 3,125 PASS
- 1,560 PASS
- 780 FAIL

25,000 candidate had one non-manifold edge and is rejected; lower final tiers were independently topology-audited and valid where reported PASS.

## 6. Predeclared refinement

Broad bracket 1,560 PASS / 780 FAIL produced:

- geometric mean ≈ 1,103.09
- nearest-64 target = **1,088**

No visual fitting chose this number.

## 7. Boundary/smoothness run identity

- run `38898663428` — SUCCESS
- job `116965212281`
- HEAD `4fa99a67bcfedbff40dc934d9eaba0546bdb60cb`
- artifact `12045116564`
- digest `sha256:99a1e41bfa63f014262d51ba5f6401a8c28bdc8e517005d01c27c70fd3a12d8f`

Compared:

- 3,125
- 1,560
- 1,088
- 780

1,088 failed near-profile IoU (`0.971351 < 0.975`).

## 8. Final public result

`MIN_PASS_TESTED`:

> **1,560 vertices / 3,116 triangles**

`FIRST_FAIL_TESTED`:

> **1,088 vertices**

`QUALITY_HEADROOM`:

> **3,125 vertices / 6,246 triangles**

Reason for selecting the denser working baseline:

- user rejects an overly angular cat;
- 3,125 keeps a full broad-ladder margin above the minimum pass;
- native 96×96 silhouette remains strongly reference-like;
- surface angularity rises materially as counts fall below this region.

Decision token:

> **`R10_REFERENCE_3D_MORPHOLOGY_REDUCTION_QUALITY_FLOOR_ESTABLISHED`**

Selected evidence baseline:

> **`R10_QUALITY_HEADROOM_V3125_F6246`**

## 9. What remains authoritative

Public mesh geometry is still derived visible-form evidence only.

Private canonical semantics remain authoritative and unchanged, including canonical contacts, continuous orientation and exactly six external visible domains.

## 10. Recommended next governance step

Import this public R10 evidence into the private R10 working branch, perform bounded private consistency review, sync STATUS/HANDOFF, scope-audit, lease-check, then non-force promote only if clean.

After R10 closure, do **not** immediately animate or rig.

Recommended next planning question:

> can the `V3125/F6246` quality-headroom surface be replaced by a much smaller semantic landmark / anatomical curve / section representation while preserving native 96×96 and smooth-form evidence?

That next question requires its own change control/contract before implementation.
