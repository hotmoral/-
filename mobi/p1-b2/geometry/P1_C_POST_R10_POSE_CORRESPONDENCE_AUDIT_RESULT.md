# Mobi P1-C — Post-R10 Cat Pose Correspondence Audit Result

Date: 2026-10-16
Status: **CLOSED / INFORMATIVE FAIL / NO DIRECT VERTEX CORRESPONDENCE**
Public branch: `mobi/experiment-cat-pose-correspondence-20261016`
Accepted execution HEAD: `daab3c9c206aa5e75614e8b6c5e4b11d288f0141`

## 1. Question

Do the independently available Innerscene standing / walking / sitting domestic-cat GLBs share exact body topology and vertex ordering, such that actual per-vertex pose displacement can be read directly without registration or hand matching?

## 2. Execution identity

- workflow: `Mobi P1-C Post-R10 Pose Correspondence Audit`
- run: `38901164465` — SUCCESS
- job: `116973487909`
- artifact: `12047090136`
- artifact digest: `sha256:9fc8803b80d1df21a0fbdb1d60fc835a4ea99a897b1c296566dfbe312a596952`
- unit tests: 4/4 PASS
- seed 1 / 777 evidence: byte-identical

## 3. Frozen sources

### Standing

- Innerscene `Standing cat`
- SHA-256: `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- bytes: 4,903,420
- largest structural body primitive: 99,642 vertices / 199,280 triangles / 597,840 indices
- skin: 0
- animation: 0
- morph target sets: 0

### Walking

- Innerscene `Domestic cat walking`
- SHA-256: `22c8c6afc9c561947816b23a3987501adc6fe8c1f18007695ffd23af78d470e1`
- bytes: 891,024
- largest structural body primitive: 16,222 vertices / 27,444 triangles / 82,332 indices
- skin: 0
- animation: 0
- morph target sets: 0

### Sitting

- Innerscene `Domestic cat sitting`
- SHA-256: `88bf81d0805bf10b8ddb44c0b6c6b8ced14a43a519138467b78c2521ea9ed3b2`
- bytes: 848,348
- largest structural body primitive: 16,077 vertices / 28,000 triangles / 84,000 indices
- skin: 0
- animation: 0
- morph target sets: 0

All three provider pages were independently checked for `Public domain (CC0)` before the files were used.

## 4. Pair results

All three pairs fail direct correspondence:

- standing ↔ walking — vertex count differs, triangle count differs, index count differs;
- standing ↔ sitting — vertex count differs, triangle count differs, index count differs;
- walking ↔ sitting — vertex count differs, triangle count differs, index count differs.

No pair has an identical index sequence.

Audit conclusion:

> **`NO_DIRECT_POSE_VERTEX_CORRESPONDENCE_IN_TESTED_SOURCES`**

## 5. Meaning

The tested static poses may still be useful as independent feline-pose references, but they are not a direct deformation sequence.

Therefore it is invalid to claim:

> vertex `i` in standing moved to vertex `i` in sitting/walking.

No pose field, joint location, skin deformation or generative pose equation may be inferred from these raw vertex indices.

## 6. What is rejected

Do not:

- retopologize these files merely to manufacture a direct pair;
- nearest-neighbor-match vertices and call that ground-truth correspondence;
- hand-pin landmarks after looking at desired motion;
- fit separate per-pose curves and treat them as one continuous deformable model;
- replace the R10 3,125-vertex morphology baseline with either lower-detail static pose source.

## 7. Cheapest next evidence

The next useful source class is a single **rigged/animated cat mesh** where one mesh topology is driven through multiple poses/actions.

Such a source is useful only as a motion/deformation reference unless it independently passes Mobi morphology gates.

The immediate next audit should inspect:

- one mesh identity across actions/frames;
- armature/bone hierarchy;
- vertex groups / skin weights;
- action/frame ranges;
- evaluated mesh topology invariance;
- actual corresponding vertex displacement across selected walk/run frames.

## 8. Final token

> **`STATIC_POSE_SET_NOT_DIRECTLY_CORRESPONDING__RIGGED_SINGLE_TOPOLOGY_REFERENCE_REQUIRED`**
