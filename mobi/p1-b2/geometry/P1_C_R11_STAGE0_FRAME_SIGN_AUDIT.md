# Mobi P1-C-R11 — Stage-0 Frame / Anatomical-LR Sign Audit

Date: 2026-10-16
Status: **CLOSED / PASS / PRE-EVIDENCE**
Decision token: **`R11_STAGE0_FRAME_SIGN_PASS_PLUS_X_R10_IS_ANATOMICAL_LEFT`**

## 1. Purpose

Close the frozen R11 Stage-0 requirement that the bilateral sign be verified from the actual accepted source geometry plus the frozen view convention before any semantic scaffold extraction.

This is a coordinate/sign audit only. It is **not** Stage-1 scaffold evidence and does not generate a medial graph, controls, weights, Jacobian result, neutral raster result or finite pose.

## 2. Frozen inputs

Accepted R10 source artifact:

- source: Innerscene `Standing cat`, `cat-original.glb`
- bytes: `4,903,420`
- SHA-256: `6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5`
- structural node: `Cat continuous body`
- source structural vertices: `99,642`

Frozen projection identity referenced:

- Stage-D projection blob: `5c8820fb7270e7727ececb1bb37d3a24331b24ab`
- yaw convention: `0°` exact front, camera on the source `+Z` side looking toward the target
- screen-right vector: `r(alpha) = (cos alpha, 0, sin alpha)`

Audit executable:

- path: `mobi/p1-b2/geometry/p1_c_r11_stage0_frame_sign_audit_v1.py`
- bytes: `5,159`
- SHA-256: `2cb5a5c26dac3b724b08eda2d8e7c124c1b83db9080e938393f2dfe99b945eaa`
- Git blob: `a49c4b6b9efc2ea6809624a09c474721980a10a8`

Result JSON:

- path: `mobi/p1-b2/geometry/P1_C_R11_STAGE0_FRAME_SIGN_AUDIT_RESULT.json`
- bytes: `1,810`
- SHA-256: `6c547cb42d76870afe7828afb31e29ee560ee78a17fabc0bcfeb39914d5c996d`
- Git blob: `63b9a3e829816e777e0bfdfabd47314a5e828b94`

The audit executable uses only Python standard-library GLB/JSON parsing and frozen projection equations; its result does not depend on the Stage-1 voxel/skeleton dependency stack.

## 3. Actual source-geometry verification

The preserved R10 source artifact was read directly and its SHA-256/byte count matched the frozen identity.

The structural body AABB reproduced exactly within source float precision:

```text
min = [-0.12377405166625977, 0.0055554211139678955, -0.40411117672920227]
max = [ 0.12377957999706268, 0.7522867619991302,  0.36675095558166504]
```

Facial semantic parts occupy the positive-Z face region:

- Eye: `z = +0.3529999852`
- Eye.001: `z = +0.3529999852`
- Muzzle pad: `z = +0.3580000103`
- Muzzle pad.001: `z = +0.3580000103`
- Nose: `z = +0.3819999993`
- Vertical pupil: `z = +0.3630000055`
- Vertical pupil.001: `z = +0.3630000055`

The paired eye, muzzle-pad and pupil nodes are mirrored across source X:

```text
Eye               x = -0.0410000011
Eye.001           x = +0.0410000011
Muzzle pad        x = -0.0230000000
Muzzle pad.001    x = +0.0230000000
Vertical pupil    x = -0.0410000011
Vertical pupil.001 x = +0.0410000011
```

Therefore the actual source geometry independently confirms:

- `+Y_R10` = up;
- `+Z_R10` = anatomical front/face side;
- `X_R10` = bilateral axis.

## 4. Frozen-view sign verification

At frozen yaw `0°`:

```text
screen-right = (+1, 0, 0) = +X_R10
camera-forward-toward-target = (0, 0, -1)
```

The camera is therefore on the animal's `+Z_R10` front side while the source geometry shows the animal's face is also on `+Z_R10`. The animal faces the viewer.

For a subject facing the viewer, viewer screen-right is the subject's anatomical left. Because frozen yaw-0 screen-right is exactly `+X_R10`, the bilateral sign is:

> **`+X_R10 = anatomical left`**

As a cross-check, at frozen yaw `90°`:

```text
screen-right ≈ (0, 0, +1) = +Z_R10
```

which matches the previously frozen exact-profile rule that the animal's anatomical front points to screen-right.

## 5. Mapping decision

The candidate mapping is therefore mechanically accepted without sign repair:

```text
x_B3 = z_R10
y_B3 = y_R10
z_B3 = x_R10
```

Decision:

> **PASS / `R11_STAGE0_FRAME_SIGN_PASS_PLUS_X_R10_IS_ANATOMICAL_LEFT`**

No silent L/R flip is required or permitted.

## 6. Delta-consistency audit

This audit changes **no** frozen Stage-1 structural constant.

It only resolves the predeclared sign gate using already accepted source geometry and the already frozen view convention. Therefore:

- V3125 remains stored/hashed in `R10_SOURCE_FRAME`;
- the B3 mapping remains a semantic query/reporting map;
- the exact 30-role hypothesis is unchanged;
- six external domains are unchanged;
- no bind coordinate is authored manually;
- no CatPilot/static-pose/prototype numeric coordinate is imported;
- no Stage-1 output was viewed or used for sign selection.

## 7. Execution boundary

The Stage-0 frame/sign requirement is now explicitly closed.

R11 Stage-1 public evidence remains **NOT RUN**. A future separately authorized Stage-1 run should re-assert the same sign mapping as a runtime hard gate before voxelization, but it may not choose another sign based on evidence.
