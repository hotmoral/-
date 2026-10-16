# Mobi — Authored Pixel Animation Provisional Selection after R9

Status: **PUBLIC ANALYSIS / PROVISIONAL / NON-CANONICAL**  
Date: **2026-10-16**

## 1. Question

Can a directionally authored, growth-specific pixel animation library be a more practical Mobi visible-form strategy than requiring one procedural carrier to generate every feline pose/view?

## 2. Current answer

**YES — STRONG CANDIDATE FOR BOUNDED FEASIBILITY, NOT YET A PRODUCT DECISION.**

R9 showed that continuous procedural curve→pixel rendering can preserve mechanics but still fail feline form authoring. An authored animation family changes the causal problem: feline silhouette, mass rhythm and gait can be explicitly designed per action rather than expected to emerge from one generic carrier.

## 3. Retained architecture

The promising architecture is not “thousands of unrelated sprites.”

It is:

`behavior state / environment`  
`→ intent/action selection`  
`→ growth-stage clip family`  
`→ directional variant`  
`→ transition / loop / one-shot playback`  
`→ frame event + contact metadata`  
`→ pixel rendering`

Canonical physical semantics can remain outside the art bank.

## 4. Four growth stages retained

Working growth architecture:

- G1 young kitten
- G2 juvenile kitten
- G3 adolescent / young cat
- G4 adult

Exact ages, durations and pixel dimensions are intentionally not frozen.

Growth may be influenced by Mobi progression, user routine and relationship development; it need not be a simple wall-clock age model.

## 5. Key pruning decision

Do **not** use one global direction count, frame count or action count.

Use a sparse matrix.

### Direction density

- locomotion: main test frontier D16 / D24 / D36;
- posture/transitions/social: D8 / D12, with D16 only where visible value exists;
- rest/groom: D4 / D8 first;
- micro overlays: D1/local where valid.

### Frame density

- normal walk: test F16 / F24 / F32, F12 baseline;
- fast actions: F8–F16;
- posture transition: F12–F24;
- long grooming/expression: F24–F48+ only where duration warrants it.

### Behavior breadth

Prioritize in layers:

1. identity/core locomotion and posture;
2. life simulation;
3. user/cat relationship expression;
4. rare/luxury behavior.

## 6. Capacity envelopes

Planning envelopes from the quantitative analysis:

- Lean: ~10,392 FFE across four stages;
- Balanced symmetric: ~32,704 FFE;
- Balanced stage-sparse example: ~30,216 FFE;
- Premium stress ceiling: ~129,664 FFE.

Theoretical maximum body-base mirror reuse reduces the balanced stage-sparse example to ~18,402 unique authored FFE. This is an upper reuse assumption, not a guaranteed production count.

## 7. Why four stages do not imply four complete duplicates

Every action receives one of:

- unique motion;
- timing variant;
- stage-specific art with shared choreography;
- shared micro behavior;
- unavailable for that stage.

This avoids blind four-way duplication while preserving meaningful growth differences.

## 8. Interaction complexity control

User/cat relationship variables decide **which action occurs**, not unique animation for every numeric relationship state.

Cat-cat behavior uses synchronized role clips (`ROLE_A`, `ROLE_B`) with contact/event markers rather than unique assets for every pair combination.

## 9. Compatibility review with existing Mobi truths

### Preserved

- physical/contact state can remain authoritative;
- paw plant/release can be encoded as frame events;
- exactly six visible-domain semantics need not change;
- behavior selection remains separate from art;
- Android overlay premise is unaffected;
- R9 result remains valid; no R9 tuning is resumed.

### Requires explicit future change-control if adopted canonically

The current private project historically treats continuous orientation as binding. A finite direction bank is perceptually discrete even if D24/D36 appears continuous at native scale.

Therefore canonical adoption would require a product-level decision on whether:

> perceptual directional continuity at native pixel scale is sufficient,

instead of mathematical continuous shape ownership.

This is the major governance conflict to resolve before canonical adoption.

## 10. Major risks

1. direction/action/growth multiplication can still explode if density is uniform;
2. transition coverage may be more expensive than loop coverage;
3. pair interaction alignment is difficult across growth-size differences;
4. asymmetrical coat/accessory design can reduce mirror savings;
5. loading all atlases simultaneously would create excessive decoded texture memory;
6. authored quality may become inconsistent across a large library;
7. stage changes can look abrupt unless growth transition design exists.

## 11. Next bounded feasibility recommendation

Before authoring a large library, answer one empirical question:

> What direction density and frame density are actually visible at Mobi native scale?

Use one high-quality representative walk cycle and compare a bounded matrix:

- D12, D16, D24, D36;
- F12, F16, F24, F32.

Do not needlessly author every Cartesian combination from scratch. A high-fidelity master motion can be systematically sampled/downsampled for controlled perceptual comparison if that does not bias pixel-art quality.

Evaluate:

- feline gait identity;
- heading stepping;
- silhouette popping;
- paw contact;
- shoulder/haunch rhythm;
- loop seam;
- native-scale readability;
- authoring effort.

Then repeat threshold testing on:

- one posture transition;
- one low-direction rest/groom action.

Only after these thresholds are known should a four-stage production portfolio be budgeted.

## 12. Provisional result

> **FOUR_STAGE_SPARSE_AUTHORED_PIXEL_ANIMATION_LIBRARY_SELECTED_FOR_FEASIBILITY_ANALYSIS ONLY**

This is not a canonical representation selection and does not authorize mass asset production.