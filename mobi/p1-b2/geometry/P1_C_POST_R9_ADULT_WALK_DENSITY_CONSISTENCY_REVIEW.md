# Mobi P1-C — Adult Walk Density Consistency Review

Status: **PASS / CONSISTENT WITH CONSTRAINT**  
Date: **2026-10-16**

## 1. Review scope

This is a delta review for the adult-walk density experiment only.

It checks the experiment against directly affected Mobi constraints and the post-R9 authored-pixel feasibility direction. It is not a whole-project re-audit.

## 2. Semantic/contact ownership

PASS.

The experiment does not transfer BODY_ROOT, paw contact, support phase, load-bearing or anchor truth to bitmap pixels.

The synthetic `supportMismatchRate` is an analysis metric for temporal quantization pressure only. Future authored frames must carry explicit contact/anchor metadata derived from canonical semantics.

## 3. Orientation compatibility

PASS WITH EXPLICIT PRIVATE CHANGE-CONTROL REQUIREMENT.

The experiment samples discrete authored directions and therefore tests an approximation to continuous orientation. It does not claim that the private canonical continuous-orientation rule has already been changed.

If this representation is later adopted, private P1-C must explicitly decide that product/semantic boundary.

## 4. Growth-stage consistency

PASS.

The experiment uses G4 adult only to isolate density. It does not collapse or redefine the provisional four-stage growth model.

No direction/frame count is generalized automatically to G1/G2/G3.

## 5. Behavior-library consistency

PASS.

The result strengthens the sparse-library hypothesis rather than a Cartesian asset matrix:

- locomotion may justify high directional density;
- less direction-sensitive behaviors may use fewer directions;
- frame density is behavior-specific;
- micro-actions may use partial/overlay assets when perceptually safe.

## 6. Transition-graph consistency

PASS.

The user-specified rule is incorporated:

> only plausible/reachable behavior transitions require transition assets.

No all-to-all transition matrix is implied.

Semantically impossible direct edges such as `RUN -> SLEEP` remain excluded. Orientation-contradictory teleports are similarly excluded.

## 7. R9 consistency

PASS.

R9 rejected one tested generated curve-pixel carrier because it was not sufficiently feline. This experiment does not reopen or tune that carrier.

The synthetic cat used here is only a common controlled signal for density comparison. It is explicitly not accepted as Mobi’s production body representation.

Therefore:

- R9 visual failure remains true;
- pixel art globally remains un-rejected;
- authored directional pixel animation is a distinct feasibility family.

## 8. Anti-fitting / evidence discipline

PASS.

All 16 direction/frame combinations were sampled from one frozen continuous gait reference.

No candidate received:

- hand-tuned proportions,
- view-specific correction,
- frame-specific correction,
- separate gait timing,
- separate rendering quality.

The original 5-degree direction grid was found to under-sample D16/D24 exact worst-case midpoint angles. Rather than rewriting the main evidence, a separate exact-halfstep diagnostic was run and preserved.

This correction improved measurement validity without fitting the representation to a desired result.

## 9. Evidence-economy review

PASS WITH ENGINEERING NOTE.

The experiment answered the density question without authoring thousands of production frames.

The main test suite was computationally more expensive than necessary because synthetic renders were recomputed repeatedly. Future diagnostics should cache shared render states or keep heavy matrix calculation out of unit tests.

This is an execution-efficiency lesson, not a product-quality failure.

## 10. Capacity / downstream lock-in

PASS.

No production-wide D/F constants were frozen.

The next retained candidate set is deliberately small:

- D24/F24
- D36/F16
- D36/F24

A real authored-pixel discriminator can further prune these before any four-stage behavior library expansion.

## 11. External visible domains

PASS / NOT MUTATED.

The density experiment is an animation sampling study and introduces no seventh external visible domain.

## 12. Product-quality hierarchy

PASS.

Mechanical disagreement scores do not override direct visual review. Conversely, direct visual review was restricted to density stepping/smoothness and did not falsely accept the synthetic cat as final feline art.

Final product-quality acceptance still requires actual authored pixel-art evidence.

## 13. Final consistency result

> **PASS / CONSISTENT_WITH_CONSTRAINT / ADULT_WALK_DENSITY_BRACKET_VALID_FOR_NEXT_AUTHORED_ART_DISCRIMINATOR**

No private canonical decision is changed by this public execution group.
