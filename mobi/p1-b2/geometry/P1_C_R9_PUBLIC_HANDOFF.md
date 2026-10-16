# Mobi P1-C-R9 — Public Execution Handoff

Status: **CLOSED / REJECT / PUBLIC EXECUTION COMPLETE**  
Date: **2026-10-16**

## Recovery order

1. Public repo: `hotmoral/-`
2. Branch: `mobi/run-p1-c-r9-intrinsic-curve-pixel-raster-20261016`
3. Read `P1_C_R9_PUBLIC_EXECUTION_SCOPE.md`
4. Read `P1_C_R9_PUBLIC_STAGE1_DIRECT_VISUAL_REVIEW.md`
5. Read `P1_C_R9_PUBLIC_STAGE1_CLOSURE.md`
6. Inspect frozen implementation/test/runner only when exact execution identity is required.

## Public baseline

R9 branch was created from R8 public execution HEAD:

`5b322062dcddf8a6a3cd07e6bc03a0e909497950`

## Accepted evidence execution

- accepted execution HEAD: `e3d3020b99a8aa92280bc42ad9cae48d92fc9346`
- workflow: `Mobi P1-C-R9 Curve Pixel Stage 1`
- run: `38872708322` — SUCCESS
- job: `116880341665` — SUCCESS
- artifact: `12034101138`
- artifact digest: `sha256:2dc9a02091232acb8136d2cd63d80900571d290586e940cc30c47a0a4e4b7d87`

## Frozen implementation identity

- `p1_c_r9_intrinsic_curve_pixel_v1.py` blob `3cc6e2b9b1f5001c93b6b4530c2bdd03a7bad883`
- `test_p1_c_r9_intrinsic_curve_pixel_v1.py` blob `617e4aa131eb1b845cb014794011a937c10018c7`
- `run_p1_c_r9_curve_pixel_stage1.py` blob `5fbe3da3b876653fd471b2f17dd2fa5ed46c6f93`
- carrier signature `1159a34a650543374666a161bd2890bcfaa31a96ee53b2a59e69e31f2bf2bf6e`

Capacity:

- 15 curve groups
- 60 body-local control nodes
- 15 cubic segments
- 80x80 native raster
- 33 samples/curve
- exactly six visible domains
- one carrier across all yaw

## Mechanical evidence

- tests 9/9 PASS
- all four neutral paw pins 0.0 dp at profile/3Q/front
- deterministic rerender PASS
- seed 1/777 byte-identical
- max area jump 0.17028670721112077
- max centroid step 2.720578114348863 px
- max adjacent XOR/union 0.35077881619937695
- max components 3
- min occupied pixels 955
- mechanicalPass true

## Perceptual decision

Direct native-scale review:

- profile: generic/plank torso; weak feline mass hierarchy
- 3Q: generic quadruped; weak proximal emergence
- exact front: HEAD_BODY hard fail
- ear-neutralized 3Q/front: CAT_ID hard fail
- orientation continuity/pixel stability: mechanically promising

Final narrow result:

> `TESTED_RF_K_NEUTRAL_CURVE_PIXEL_CARRIER_NOT_DEMONSTRATED`

## Retained learning

Keep:

> deterministic native pixel rasterization is compatible with one continuous body-local carrier and exact canonical paw binding.

Keep:

> pixelization does not by itself solve feline-specific form authoring; a generic source carrier remains generic after rasterization.

Do not infer:

- pixel art as a whole failed;
- all curve carriers failed;
- native pixel-part puppets failed;
- motion-driven shape deformation failed.

## Closed actions

Do not on this branch:

- tune the frozen carrier after evidence;
- add view-specific shapes;
- add angle-specific sprite banks;
- run motion-shape Stage 2;
- expand to 64/96px or M1/M2;
- use final art to rescue CAT_ID.

## Governance boundary

This public branch is execution evidence only.

Private `hotmoral/Mobi` remains canonical. When private canonical access is used again, import this result through a fresh P1-C consistency/change-control review rather than treating the public branch as canonical automatically.
