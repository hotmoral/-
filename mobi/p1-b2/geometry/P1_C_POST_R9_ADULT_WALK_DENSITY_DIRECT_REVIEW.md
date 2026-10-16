# Mobi P1-C — Adult Walk Density Direct Review

Status: **CLOSED / DIRECT REVIEW COMPLETE**  
Date: **2026-10-16**

## 1. Review scope

This review evaluates only density economics for one controlled G4 adult normal-walk cycle on a 96x96 canvas.

It does **not** evaluate final Mobi cat art quality and does not freeze production direction/frame counts.

The same deterministic continuous gait reference was quantized into:

- directions: 12 / 16 / 24 / 36
- temporal frames per cycle: 12 / 16 / 24 / 32

The controlled reference uses the frozen engineering gait timing in the experiment contract:

- lateral-sequence order RH -> RF -> LH -> LF
- cycle 1.08 s
- stance 0.80 s
- swing 0.28 s

## 2. Main execution evidence

Accepted main density execution:

- workflow: `Mobi P1-C Adult Walk Density Experiment`
- run: `38882221698` — SUCCESS
- job: `116911423823` — SUCCESS
- execution HEAD: `1644e7d3771b34bcc3c97b9983da22251b42afaa`
- artifact: `12038796332`
- artifact digest: `sha256:cf84244dea3f6b1e8cb9df85aa6005aadf4fcdd19983a5fd9fc4c8c6dc065896`
- tests: 9/9 PASS
- seed 1 / seed 777 evidence: byte-identical

## 3. Original direction-grid limitation found during review

The first experiment sampled direction error on a 5-degree yaw grid.

That grid was sufficient for relative trend discovery but did not land on the exact theoretical half-step for every candidate:

- D12 half-step: 15 deg — sampled
- D16 half-step: 11.25 deg — not sampled exactly
- D24 half-step: 7.5 deg — not sampled exactly
- D36 half-step: 5 deg — sampled

Therefore the original `maxAngularErrorDeg` values for D16 and D24 were under-sampled and were **not** used as final worst-case values.

No main-run evidence was overwritten. A separate bounded diagnostic was added.

## 4. Exact half-step diagnostic

- workflow: `Mobi P1-C Adult Walk Direction Half-Step Diagnostic`
- run: `38884849284` — SUCCESS
- job: `116919989366` — SUCCESS
- execution HEAD: `4eecec90c94fd023771eceb712524295c8db30c5`
- artifact: `12038602730`
- artifact digest: `sha256:7dc407fc0fdc0e96e0e857e3a34d6f1788a69aefb257e15b626208b1c336c385`

Exact half-step results:

| Directions | Step | Exact max angle error | Mean half-step mask disagreement | P95 half-step disagreement | Max half-step disagreement |
|---:|---:|---:|---:|---:|---:|
| 12 | 30.0 deg | 15.0 deg | 0.338225 | 0.569671 | 0.600360 |
| 16 | 22.5 deg | 11.25 deg | 0.278861 | 0.463176 | 0.498507 |
| 24 | 15.0 deg | 7.5 deg | 0.201103 | 0.338964 | 0.388889 |
| 36 | 10.0 deg | 5.0 deg | 0.143311 | 0.253339 | 0.283811 |

The correction strengthens rather than reverses the original trend: direction density remains a material quality variable through D36 in this controlled synthetic test.

## 5. Direct direction-strip review

Review target was density only, not feline art quality.

### D12

- obvious orientation stepping
- profile -> 3Q -> front changes are coarse
- too sparse for the high-quality locomotion hypothesis

Decision: **PRUNE for normal adult locomotion quality target**.

### D16

- materially better than D12
- still visibly discrete in directional progression
- plausible low-density / budget floor candidate only

Decision: **retain only as minimum/budget comparison**.

### D24

- first candidate where directional progression becomes substantially finer
- 15-degree stored step / 7.5-degree worst quantization
- strong balanced candidate

Decision: **RETAIN**.

### D36

- further visible refinement over D24, especially around oblique/front transitions
- exact half-step diagnostic confirms substantial reduction in midpoint mask disagreement
- costs 50% more stored directions than D24

Decision: **RETAIN as high-quality comparison**.

This experiment does not prove D36 is worth its production cost. That must be decided using actual authored pixel-art frames, where artist-controlled silhouettes may behave differently from the synthetic reference.

## 6. Direct temporal-cycle review

### F12

- large pose jumps
- temporal quantization visibly coarse
- support-state mismatch rate: 0.15625

Decision: **PRUNE for normal adult walk quality target**.

### F16

- clear improvement over F12
- still visibly discrete
- support-state mismatch rate: 0.125

Decision: **minimum/budget candidate only**.

### F24

- substantially smoother than F16
- max phase quantization: 22.5 ms
- support-state mismatch rate falls to 0.0625
- loop seam remains comparable to ordinary adjacent-frame motion

Decision: **strong balanced candidate / first temporal plateau candidate**.

### F32

- adds intermediate poses over F24
- lower mean/P95 synthetic disagreement
- but support-state mismatch remains 0.0625, unchanged from F24
- direct visual incremental gain is much smaller than F16 -> F24

Decision: **retain only as premium comparison, not default recommendation**.

## 7. Equal-authoring-budget comparison

The controlled data show that, after a reasonable temporal density, adding directional samples provides more benefit than spending the same authored-frame budget on more temporal samples.

Examples:

- D16 x F24 = 384 FFE: mean combined disagreement 0.151795
- D24 x F16 = 384 FFE: mean combined disagreement 0.126935

and:

- D24 x F24 = 576 FFE: mean combined disagreement 0.122357
- D36 x F16 = 576 FFE: mean combined disagreement 0.087614

This is **not** a production winner declaration. F16 may still look temporally too coarse in final hand-authored animation even when its aggregate mask error is lower at high direction density.

## 8. Bounded perceptual bracket

For the next **actual authored-pixel walk validation**, retain:

### Primary balanced candidate

`D24 x F24 = 576 full-frame equivalents per adult normal-walk clip family`

Rationale:

- first strong plateau on both axes
- 7.5-degree exact worst direction quantization
- 22.5 ms temporal half-step
- support mismatch already at the F24/F32 floor observed here

### Equal-budget orientation-heavy challenger

`D36 x F16 = 576 FFE`

Rationale:

- markedly better directional approximation at equal FFE
- deliberately tests whether 16 temporal frames are visibly too coarse once actual pixel art is authored

### Premium ceiling comparison

`D36 x F24 = 864 FFE`

Rationale:

- combines the stronger retained direction tier with the stronger balanced temporal tier
- use only to determine whether visible improvement justifies +50% FFE over D24xF24

Do not carry D12 or F12 into the next authored-art validation.

D16 and F32 remain diagnostic boundary values, not primary production candidates.

## 9. Important semantic caveat

The synthetic `supportMismatchRate` measures nearest-frame phase classification mismatch against a continuous reference.

A real authored animation can and should attach exact frame metadata for:

- paw contact/release
- load bearing
- BODY_ROOT
- paw anchors
- interaction anchors

Therefore the bitmap must not become the owner of contact physics. The metric measures temporal sampling pressure, not permission to mutate canonical contact truth.

## 10. Direct-review conclusion

> **ADULT_NORMAL_WALK_DENSITY_BRACKET_NARROWED_TO_D24F24_VS_D36F16_WITH_D36F24_PREMIUM_CEILING**

This conclusion applies only to one G4 adult normal-walk feasibility experiment.

It does not freeze:

- one direction count for all behavior classes;
- one frame count for all behavior classes;
- exact growth-stage canvas sizes;
- the final production animation representation;
- discrete orientation as a replacement for the private canonical continuous-orientation rule.
