# Mobi P1-C-R12 — Stage-0 Closure

Date: 2026-10-17
Status: **CLOSED / FROZEN / PRE-EVIDENCE PASS**

Closure token:

> **`R12_STAGE0_CLOSED_FROZEN_PRE_EVIDENCE_PASS`**

## 1. Checkpoint question

Did R12 Stage 0 implement and freeze the selected dual-anchor surface-terminal bind revision without executing evidence, retuning the failed R11 test, or modifying inherited morphology/scaffold machinery outside the explicitly authorized four-paw bind boundary?

Decision:

> **YES — bounded Stage-0 implementation/freeze is complete.**

This is not an R12 Stage-1 PASS and is not evidence that the new aliases solve the paw-local support problem.

## 2. Frozen public branch

- repository: `hotmoral/-`
- branch: `mobi/run-p1-c-r12-surface-terminal-bind-20261017`
- base HEAD: `4ce94fa9c07f0f86b0380c58cdacaf59481732c2`
- identity commit HEAD before this closure document: `b4dc6cf445aa3095be8e0694ce712190d296816e`
- R11 frozen execution HEAD inherited: `4c695503b99974e929491b1e78b0cf2935b675c7`

## 3. Scope audit

Compare `4ce94fa9c07f0f86b0380c58cdacaf59481732c2..b4dc6cf445aa3095be8e0694ce712190d296816e`:

- ahead: `6`
- behind: `0`
- changed inherited files: `0`
- added R12 files: exactly `5`

Added files:

1. `.github/workflows/mobi-p1-c-r12-surface-terminal-bind.yml`
2. `mobi/p1-b2/geometry/P1_C_R12_STAGE0_IDENTITY.json`
3. `mobi/p1-b2/geometry/P1_C_R12_STAGE0_IMPLEMENTATION_FREEZE.md`
4. `mobi/p1-b2/geometry/p1_c_r12_surface_terminal_bind_alias_v1.py`
5. `mobi/p1-b2/geometry/test_p1_c_r12_surface_terminal_bind_alias_v1.py`

No R10/R11 source, assembler, part, synthetic test, failure result or handoff file was modified.

## 4. Exact new implementation identity

R12 adapter:

- bytes: `16839`
- SHA-256: `06d8529cf28b3dc1cffa1cecb3da4524083167614cf3a4b3da36d46844557025`
- Git blob: `f63d7ee780e5fb2f4716b83532e16d3d2ee525a3`

R12 synthetic tests:

- bytes: `5049`
- SHA-256: `64b85b6c8331783fc313e68064af724ffbf5966bcdfeb9e2dddb20e5f8d60140`
- Git blob: `7257217740e2ff7dedffc3b54f33b85d42a920db`

R12 workflow Git blob:

`8918c48e6330b493c15e9fb41c6b5b741ee5f698`

Stage-0 freeze document Git blob:

`d436bde0b2fa550ed5d5ac1639403a8d8c40aa95`

Stage-0 identity JSON Git blob:

`72a4d5d2484b326fb113edd9c03d9fdb284b99e5`

## 5. Inherited R11 byte lock

The R12 adapter imports only the exact assembled R11 implementation:

- bytes: `37871`
- SHA-256: `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`

Assembler Git blob:

`7a5c4bda8131fcbfc1ef301c70c64d423bf5c04f`

All seven R11 implementation-part blobs remain equal to the R11 Stage-0 freeze identities.

The R10 reducer, Stage-D raster and Stage-B inspector blobs also remain unchanged.

## 6. Bounded semantic delta

R12 does not create new visible domains, new canonical contact truth, or extra active controls.

Exactly 30 existing roles remain.

The implementation is allowed to change only the active coordinates of:

- `FORE_L_PAW_CTRL`
- `FORE_R_PAW_CTRL`
- `HIND_L_PAW_CTRL`
- `HIND_R_PAW_CTRL`

The other 26 active control positions must remain R11-identical.

Parent/domain/provenance metadata for all 30 controls must remain unchanged.

The four R11 medial semantic-path endpoints remain retained as separate recorded internal topology references.

## 7. Frozen alias rule

Each new active paw bind is an exact existing V3125 vertex selected deterministically from the already frozen sole candidate region:

`quadrant -> ymin -> y <= ymin + 0.035*h -> float64 mean -> argmin(squared distance, global vertex index)`.

No threshold enlargement, interpolation, free projection, optimization, manual fitting or external rig coordinate was added.

## 8. Failed-test preservation

The original locality radius remains:

> **`4*pitch` unchanged.**

Also unchanged:

- six-domain construction;
- interface rule;
- inverse-distance weighting;
- `sigma=2*pitch`;
- top-4 truncation;
- Jacobian threshold;
- 30-role hierarchy;
- neutral V3125;
- raster path.

Therefore Stage 1 can still expose a secondary domain/top-4/weighting failure rather than hiding it.

## 9. New non-vacuity gates

The frozen adapter requires each paw alias to be:

- an exact V3125 vertex;
- in its expected anatomical domain;
- assigned positive final normalized weight from its own paw role at that alias vertex.

Then the unchanged inherited Jacobian audit must demonstrate local differential support inside unchanged `4*pitch`.

## 10. Trigger audit

The R12 workflow uses `workflow_dispatch` only.

The job additionally requires:

- exact branch `mobi/run-p1-c-r12-surface-terminal-bind-20261017`;
- exact token `RUN_R12_STAGE1_AFTER_STAGE0_FREEZE`.

After all implementation/workflow/freeze/identity commits through `b4dc6cf445aa3095be8e0694ce712190d296816e`, branch workflow-run query returned:

- `total_count = 0`
- `workflow_runs = []`.

Thus Stage 0 did not accidentally execute Stage 1.

## 11. Pre-freeze correction record

During static workflow review, one malformed quote in the dependency-version dictionary was detected before identity freeze.

It was corrected by commit:

`6955239841219384e55fcd8c0fb6092cf859a62a`.

The workflow blob pinned by the identity JSON is the corrected post-review blob `8918c48e6330b493c15e9fb41c6b5b741ee5f698`.

No evidence had run before or during that correction.

## 12. Stage-0 result

Stage 0 establishes only that a bounded, reproducible R12 candidate and execution lane have been defined and byte-frozen consistently with the private R12 contract.

It does **not** establish:

- that the four aliases have the expected real V3125 domains;
- that each paw survives top-4 at its alias vertex;
- that local differential support now exists;
- that neutral/raster determinism passes under the revised weights;
- that finite deformation is natural;
- that any gait or animation is feasible.

Those are later evidence questions.

## 13. Exact next boundary

> **R12 Stage 0 — CLOSED / FROZEN / PRE-EVIDENCE PASS.**

> **R12 Stage 1 — NOT STARTED.**

The public workflow is structurally available but must not be dispatched until the private canonical import/consistency review is complete and a separate execution decision authorizes Stage 1.
