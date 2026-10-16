# Mobi — Post-R9 Authored Pixel Animation Public Analysis Handoff

Status: **ANALYSIS GROUP CLOSED / PUBLIC NON-CANONICAL**  
Date: **2026-10-16**

## Recovery order

1. Public repo: `hotmoral/-`
2. Branch: `mobi/analysis-authored-pixel-animation-space-20261016`
3. Read `P1_C_POST_R9_AUTHORED_PIXEL_ANIMATION_DESIGN_SPACE.md`
4. Read `P1_C_POST_R9_ASSET_BUDGET_AND_PRUNING_ANALYSIS.md`
5. Read `P1_C_POST_R9_AUTHORED_PIXEL_ANIMATION_PROVISIONAL_SELECTION.md`
6. Read prior R9 public handoff only when reconstructing why the authored alternative was considered.

## Entry baseline

Created from closed R9 public branch HEAD:

`cbee1eea991f2e2666b4821a97360e8888f3a455`

## What was analyzed

- four growth-stage architecture;
- broad behavior candidate pool (~150 action/micro candidates before pruning);
- action-specific direction-density tiers D1/D4/D8/D12/D16/D24/D36/D48/D72;
- action-specific frame-density tiers F3 through F64+;
- loop / one-shot / transition / paired-role / overlay-micro clip types;
- user-cat and cat-cat interaction implications;
- mirror/choreography/behavioral reuse;
- package/runtime texture implications;
- lean / balanced / premium asset envelopes;
- explicit pruning rules.

## Working growth architecture

- G1 young kitten
- G2 juvenile kitten
- G3 adolescent / young cat
- G4 adult

Exact age windows and native sizes are NOT frozen.

Candidate size ladder for later testing only: roughly 64/72/84/96 px.

## Quantitative planning results

FFE = full-frame equivalent.

- Lean: 10,392 FFE across four stages.
- Balanced symmetric: 32,704 FFE.
- Balanced stage-sparse example: 30,216 FFE.
- Premium stress envelope: 129,664 FFE.

Theoretical maximum valid body-base mirror reuse:

- Balanced stage-sparse runtime FFE 30,216 → about 18,402 unique authored FFE.

This mirror count is an upper reuse assumption; asymmetrical art/roles can reduce savings.

## Current strongest pruning hypothesis

Do not freeze one global density.

- primary locomotion: compare D16/D24/D36, keeping D12 lower baseline;
- posture/social: D8/D12 first;
- rest/groom: D4/D8 first;
- micro overlays: D1/local where visually valid;
- normal walk: compare F16/F24/F32 with F12 baseline;
- quick actions: F8–F16;
- posture transitions: F12–F24;
- long grooming/expression: F24–F48+ only when duration requires it.

## Provisional family result

`FOUR_STAGE_SPARSE_AUTHORED_PIXEL_ANIMATION_LIBRARY_SELECTED_FOR_FEASIBILITY_ANALYSIS ONLY`

This is NOT canonical adoption.

## Important conflict for private canonical review

A finite directional sprite bank conflicts with the historical requirement of mathematically continuous orientation if interpreted literally.

Before canonical adoption, private change control must decide whether **perceptual continuity at native scale** is an acceptable product requirement instead.

Do not silently weaken the old rule from this public branch.

## Next recommended bounded experiment

One representative high-quality walk cycle only:

- D12 / D16 / D24 / D36 direction density;
- F12 / F16 / F24 / F32 frame density;
- native pixel scale;
- same gait/anatomical reference;
- measure feline gait identity, heading stepping, silhouette popping, paw contact, loop seam and authoring cost.

Then test one posture transition and one low-direction rest/groom clip.

Do NOT begin four-stage mass asset production before those thresholds are known.

## Governance

Private `hotmoral/Mobi` remains canonical.

This branch is a public analysis artifact only. Any adoption must be imported through fresh private P1-C change control/consistency review when canonical access is used again.