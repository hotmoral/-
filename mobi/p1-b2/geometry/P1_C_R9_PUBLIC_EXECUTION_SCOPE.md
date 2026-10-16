# Mobi P1-C-R9 — Public Stage 1 Execution Scope

Status: FROZEN BEFORE R9 IMPLEMENTATION EVIDENCE
Date: 2026-10-16
Public execution branch: `mobi/run-p1-c-r9-intrinsic-curve-pixel-raster-20261016`
Public baseline: `5b322062dcddf8a6a3cd07e6bc03a0e909497950`

## Purpose

This public branch is an execution/evidence lane only. It does not replace the private Mobi canonical governance state.

R9 tests one bounded family selected by the canonical post-R8 change control:

`RF_K_BOUNDED_INTRINSIC_DEFORMABLE_CURVE_CARRIER_WITH_PIXEL_RASTERIZATION`

## Stage 1 question

Can one projection-independent body-local curve carrier, constrained by canonical semantic/contact state and using deterministic 80x80 pixel rasterization, preserve a recognizably feline neutral body across continuous profile -> three-quarter -> exact-front orientation without authored view bases or frame-specific corrections?

## Frozen Stage 1 limits

- semantic curve groups <= 16
- body-local cubic control nodes <= 64
- cubic curve segments <= 48
- one carrier/signature for all tested yaw values
- one M0 neutral carrier before evidence
- native output: 80 x 80 pixels
- no PROFILE/3Q/FRONT authored shape banks
- no angle-specific geometry tables
- no frame-specific corrective silhouettes
- no raster-space structural corrections
- no motion-shape law in Stage 1
- no morphology expansion in Stage 1
- exactly six external domains: CORE / FORE_L / FORE_R / HIND_L / HIND_R / TAIL

## Canonical ownership preserved

The renderer may consume canonical state, but it may not move or redefine:

- BODY_ROOT
- FOREQUARTER_REF
- PELVIS_REF
- HEAD_ROOT
- TAIL_ROOT
- four paw endpoints
- support/contact state
- planted-paw truth
- continuous orientation
- anatomical L/R

Pixel output is derived presentation state only.

## Required evidence

At minimum:

- M0 80px profile
- M0 80px 3Q
- M0 80px exact front
- ear-neutralized 3Q
- ear-neutralized exact front
- domain/proximal diagnostic
- continuous orientation strip from 0 to 90 degrees
- deterministic rerender equality
- semantic immutability / paw endpoint binding checks

## Hard falsifiers

Stop before motion/morph expansion if any of the following occurs:

- exact-front HEAD_BODY remains materially non-feline
- ear-neutralized CAT_ID materially collapses
- curve carrier requires authored view-specific geometry
- pixel quantization causes severe orientation popping/flicker
- paw/contact truth must move to improve appearance
- a seventh external visible domain is required
- raster-space hand correction is required
- the carrier exceeds the frozen capacity ceiling

No coefficient/view tuning loop is permitted after accepted Stage 1 perceptual evidence.
