# Twin Dock — Side / Mid-body Craft Probe

Status: **IMPLEMENTED / BUILD PASS / PHYSICAL DEVICE EVALUATION PENDING**

This is an experimental Geometry v2 candidate, not yet accepted gameplay.

## Authority boundary
Accepted continuation remains:
- branch `twindock-p3b-transition-v1`
- Geometry v2 reference-anchor foundation PASS / ACCEPTED
- accepted canonical checkpoint before this experiment: `e40352fcc2fd56919f493728015d4edc02571009`

Experimental branch:
- `twindock-geometry-side-probe-v1`
- implementation commit: `828461d2178ce2e988241ac80f8dfabd43c6fc9b`

Do not promote this branch back to accepted continuation until physical-device evidence closes the product question.

## Product question
Does a non-front player docking anchor create a clearly different but understandable correction strategy without changing accepted dual-RCS controls, ship-frame camera, docking thresholds, or recovery philosophy?

## Probe geometry
Reference mode remains the default and is unchanged.

Side probe:
- id: `SIDE`
- player local docking anchor x: `2`
- player local docking anchor y: `-31`
- player local docking anchor angle: `-π/2` (-90°)

Station target orientation is initialized from the active player anchor frame so the target does not manufacture an unrelated initial orientation penalty. Reference mode remains mathematically identical because its anchor angle is zero.

## User-facing probe control
The same APK contains both modes.

Button:
- `기체 · 기준` = accepted reference shuttle
- tap once -> `기체 · 측면`
- changing craft resets Mission 01 so comparison starts from a clean state

This selector is probe UI, not a committed final craft-selection UX.

## Visible geometry strategy
The accepted `renderer.js` was not broadly rewritten.

New `src/craft-probe.js` wraps the renderer only for the experimental SIDE mode:
- REFERENCE mode passes the original renderer through unchanged
- SIDE mode visually seals/dims the old nose fixture
- SIDE mode draws active docking hardware at `ship.dockAnchor`
- the active side fixture is visually highlighted
- the adapter loads between `renderer.js` and `presentation.js`

Required presentation chain remains:
`renderer.js -> craft-probe.js -> presentation.js -> main.js`

The P3-A continuous-angle adapter remains in control of renderer-facing angle continuity.

## Frozen contracts untouched
This probe does not change:
- FORCE_SCALE / deadzone / exponent
- torque / damping / speed caps
- physics integration
- docking thresholds
- docking checks
- ship-frame camera
- P2 threshold mapping
- P3 effects/transitions
- Android wrapper/platform contract
- broad hull collision

The accepted reference craft remains available in the same build for A/B comparison.

## Relative-velocity boundary
The probe still uses accepted Mission 01 relative-velocity truth:
- player side = ship COM linear velocity
- target side = actual station capture-anchor rigid velocity

`tests/side-probe.mjs` deliberately proves that, on a rotating side-anchor case, full player-anchor rigid velocity differs materially from the currently accepted metric.

Therefore device evaluation must not be interpreted as final acceptance of velocity semantics. Before promoting non-front craft, separately evaluate whether player-anchor rotational tangential velocity should enter docking success truth.

## Automated evidence
GitHub Actions run:
- run `40241656683`
- implementation head `828461d2178ce2e988241ac80f8dfabd43c6fc9b`
- result **SUCCESS**

Passed:
- accepted reference web regressions
- Geometry v2 legacy/reference parity tests
- Mission 01 tests
- side-anchor probe contract tests
- craft-probe syntax validation
- local Android staging
- renderer -> craft-probe -> presentation ordering guard
- Capacitor shell generation
- Android contract checks before/after sync
- Gradle debug APK build
- APK artifact upload

Artifact:
- artifact name `twindock-android-debug`
- artifact ID `12616809662`
- artifact ZIP digest `sha256:11d432b5897f2557dbb1d6b351a5ac7588bb5a211ff32ae9a008378778595242`
- APK filename `app-debug.apk`
- APK bytes `4144460`
- APK SHA-256 `4f081fb8267779eb6edafb7206fed25dd645e61e8b0eb89c50b5f2a85b118101`

## Physical-device acceptance questions
Compare REFERENCE and SIDE in the same APK.

SIDE candidate passes only if device play shows:
1. active side port is immediately identifiable without relying on explanatory HUD
2. docking posture/correction strategy feels materially different from nose-first reference docking
3. difference is understandable rather than arbitrary confusion
4. ship-frame camera remains intuitive
5. P2 position/orientation/spin/drift cues agree with the visible side port
6. bad approaches remain recoverable through normal RCS correction
7. no control retuning or docking-threshold loosening is needed
8. no input, background, presentation-angle, audio, haptic, transition, or Android-wrapper regression appears

Prefer completing the five-target Mission 01 in SIDE mode if the first targets are readable enough to continue.

## Failure classification
Before fixing any observed problem classify it as one of:
- side-port visual/readability defect
- anchor/mission-placement defect
- P2 visual/physical mismatch
- candidate velocity-semantics issue
- pre-existing reference defect
- Android/platform regression
- content-design failure (geometry is not meaningfully distinct or understandable)

Do not compensate by changing frozen controls or widening docking thresholds.

## Decision after device evidence
If PASS:
- decide the player-anchor tangential-velocity question in a separate bounded experiment
- then promote side/mid-body geometry and proceed toward rear/asymmetric probe

If FAIL:
- keep accepted reference foundation intact
- fix only the classified side-probe issue or reject/reposition this anchor
- do not proceed to hull clearance, Mission 02, or broad craft schema
