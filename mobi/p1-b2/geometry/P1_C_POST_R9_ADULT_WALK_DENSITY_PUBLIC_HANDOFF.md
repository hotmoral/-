# Mobi P1-C — Adult Walk Density Public Handoff

Status: **CLOSED / PUBLIC ANALYSIS + EXECUTION COMPLETE**  
Date: **2026-10-16**

## Recovery order

1. Public repo: `hotmoral/-`
2. Branch: `mobi/experiment-adult-walk-density-20261016`
3. Read `P1_C_POST_R9_ADULT_WALK_DENSITY_EXPERIMENT_CONTRACT.md`
4. Read `P1_C_POST_R9_ADULT_WALK_DENSITY_DIRECT_REVIEW.md`
5. Read `P1_C_POST_R9_ADULT_WALK_DENSITY_FINAL_RESULT.md`
6. Read `P1_C_POST_R9_ADULT_WALK_DENSITY_CONSISTENCY_REVIEW.md`
7. Inspect code/workflows only when execution identity is required.

## Entry baseline

This experiment branch was created from authored-pixel analysis HEAD:

`b7a6ace7df9166129a195c794826252599e1103e`

## Main experiment

Accepted run:

- run: `38882221698` — SUCCESS
- job: `116911423823` — SUCCESS
- execution HEAD: `1644e7d3771b34bcc3c97b9983da22251b42afaa`
- artifact: `12038796332`
- digest: `sha256:cf84244dea3f6b1e8cb9df85aa6005aadf4fcdd19983a5fd9fc4c8c6dc065896`
- tests: 9/9 PASS
- deterministic seed replay: PASS

Frozen main implementation blobs:

- `p1_c_adult_walk_density_experiment_v1.py` — `3d96036e9c2aca29acafef20e5c72db090c3ec44`
- `test_p1_c_adult_walk_density_experiment_v1.py` — `80e80d9f64435bffcab9edd5d62839ba6dfea32e`
- `run_p1_c_adult_walk_density_experiment_v1.py` — `28f5a9649d0e37e0e8928536c2c31d8da57fc19b`

## Exact direction correction

The main experiment’s 5-degree angular sample grid missed exact D16 and D24 midpoint worst cases.

A separate bounded diagnostic was added rather than mutating accepted main evidence.

- run: `38884849284` — SUCCESS
- job: `116919989366` — SUCCESS
- execution HEAD: `4eecec90c94fd023771eceb712524295c8db30c5`
- artifact: `12038602730`
- digest: `sha256:7dc407fc0fdc0e96e0e857e3a34d6f1788a69aefb257e15b626208b1c336c385`
- diagnostic blob: `60e2b2ecf52bf80dff65df28ea7ecdb84bad6e4d`

Exact maximum directional quantization:

- D12 = 15 deg
- D16 = 11.25 deg
- D24 = 7.5 deg
- D36 = 5 deg

## Retained density bracket

For one G4 adult normal-walk **next real authored-pixel discriminator**:

1. `D24 x F24 = 576 FFE` — balanced baseline
2. `D36 x F16 = 576 FFE` — equal-budget orientation-heavy challenger
3. `D36 x F24 = 864 FFE` — premium ceiling

Pruned from the next high-quality locomotion comparison:

- D12
- F12

Boundary comparators only:

- D16
- F16
- F32

## Key learning

Within the frozen synthetic reference, after reasonable temporal density is reached, **direction density is the larger error source**.

At equal FFE:

- D24/F16 beats D16/F24 mechanically.
- D36/F16 beats D24/F24 mechanically.

But this does **not** prove D36/F16 is the production winner; actual authored pixel playback must determine whether F16 is perceptually too coarse and whether D36’s extra directions justify their authoring cost.

## Transition rule

Retain user decision:

> transitions are sparse, plausibility-gated graph edges, not all-to-all combinations.

Examples:

- valid chain: `WALK -> WALK_STOP -> IDLE -> SIT_DOWN -> SIT`
- invalid direct edge: `RUN -> SLEEP`
- arbitrary left-walk -> opposite-oriented lie teleport: invalid

## Four-stage growth rule

Retain provisional four-stage growth architecture.

This experiment applies only to G4 adult normal walking and must not be copied mechanically to every stage or behavior.

## Semantic ownership rule

Authored bitmap frames may carry contact/anchor metadata but may not become the owner of canonical physical truth.

Private Mobi semantics remain authoritative.

## Private canonical boundary

This branch is public analysis/execution evidence only.

When private `hotmoral/Mobi` is accessible again, import this result through explicit P1-C change control/consistency review.

In particular, selecting directional sprite banks for production would require an explicit decision about the historically frozen continuous-orientation requirement.

## Next work boundary

> **REAL_AUTHORED_PIXEL_WALK_DISCRIMINATOR — ELIGIBLE / NOT STARTED**

Do not begin full four-stage asset production from this handoff.
