# Mobi P1-C — Adult Walk Density Final Result

Status: **CLOSED / BOUNDED DENSITY BRACKET ESTABLISHED**  
Date: **2026-10-16**

## Final question

For one nominal G4 adult normal-walk loop at 96x96, how dense should a directional authored-pixel animation family plausibly be before cost starts outrunning visible benefit?

## Evidence accepted

Main density run:

- run `38882221698` — SUCCESS
- artifact `12038796332`
- 9/9 tests PASS
- deterministic seed replay PASS

Exact direction half-step correction:

- run `38884849284` — SUCCESS
- artifact `12038602730`
- D12 / D16 / D24 / D36 exact midpoint errors confirmed as 15 / 11.25 / 7.5 / 5 degrees

## Final bounded result

### Pruned for this locomotion-quality target

- D12: too coarse directionally
- F12: too coarse temporally

### Minimum / budget-boundary comparators

- D16
- F16

These remain useful as lower-bound references but are not the preferred quality target for the next authored-art test.

### Retained primary candidates

1. **D24 x F24 = 576 FFE** — balanced baseline
2. **D36 x F16 = 576 FFE** — equal-budget orientation-heavy challenger
3. **D36 x F24 = 864 FFE** — premium ceiling comparator

### Diagnostic upper temporal comparator

- F32 remains available only if real authored playback shows a material smoothness gain over F24.
- The controlled test did not show a support-state improvement from F24 to F32.

## Why no single winner is frozen

The experiment deliberately used one synthetic continuous reference so that direction and frame density could be compared without art-quality confounds.

That makes the density trend useful, but it also means the experiment cannot answer whether hand-authored pixel silhouettes at native size make D36 worth the extra production cost or whether F16 is visibly sufficient at D36.

Therefore the next experiment must author only a **small real pixel-art validation subset**, not the whole library.

## Next validation target

Author one adult normal-walk cycle family sufficient to compare:

- D24/F24 balanced baseline
- D36/F16 equal-budget challenger
- D36/F24 premium ceiling

The validation should use the same cat design, gait, scale and art standard. It should compare native-size playback, not just enlarged sheets.

Do not author all 24 or 36 directions at full quality if a smaller strategically chosen angular subset can discriminate the candidates first. Prefer representative sectors around:

- profile
- shallow 3Q
- strong 3Q
- near-front
- front

and exact between-direction boundaries where stepping is most visible.

## Transition-system consequence

The user-specified transition insight is retained:

> transition assets are not a Cartesian product of every behavior and direction.

Future animation logic must use a plausibility/reachability graph. Examples:

- `WALK_LOOP -> WALK_STOP -> IDLE -> SIT_DOWN -> SIT`
- `RUN -> DECELERATE -> STAND/IDLE -> SETTLE -> LIE_DOWN -> SLEEP`

Direct impossible or visually contradictory edges should not exist merely because two states exist in the library.

Direction-changing transitions should similarly route through plausible orientation/locomotion states instead of arbitrary pose teleportation.

## Growth-stage consequence

Nothing here changes the provisional four-stage growth architecture.

The density result is only for G4 adult normal walking. Other stages and behaviors may require different:

- direction density
- temporal frame density
- loop length
- pose exaggeration
- transition topology

A sparse per-behavior/per-stage portfolio remains the governing feasibility hypothesis.

## Canonical compatibility boundary

Public evidence does not modify private canonical semantics.

If a directional authored-sprite family is later selected for production, private P1-C change control must explicitly resolve the difference between:

- historically frozen mathematical continuous orientation, and
- visually discrete authored direction banks that approximate orientation.

Frame metadata must retain contact/anchor truth rather than transferring physics ownership to the bitmap.

## Final decision token

> **CLOSED / `ADULT_WALK_AUTHORED_PIXEL_DENSITY_BRACKET_ESTABLISHED`**

Next work boundary:

> **REAL_AUTHORED_PIXEL_WALK_DISCRIMINATOR — ELIGIBLE / NOT STARTED**
