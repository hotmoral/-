# Twin Dock — Side / Mid-body Craft Probe

Status: **IMPLEMENTED / BUILD PASS / POSITIVE PHYSICAL-DEVICE OBSERVATION / NOT YET PROMOTED**

This is an experimental Geometry v2 candidate, not yet accepted gameplay.

## Authority boundary
Accepted continuation remains:
- branch `twindock-p3b-transition-v1`
- Geometry v2 reference-anchor foundation PASS / ACCEPTED
- accepted canonical checkpoint before this experiment: `e40352fcc2fd56919f493728015d4edc02571009`

Experimental branch:
- `twindock-geometry-side-probe-v1`
- implementation commit: `828461d2178ce2e988241ac80f8dfabd43c6fc9b`

Do not promote this branch back to accepted continuation until the remaining velocity-semantics question is closed.

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

## Physical-device observation — 2026-10-26 KST
The user tested the side-port APK on the physical Android device used for the prior platform parity acceptance.

Observed result:
- changing the docking-point location clearly changed the player's spatial sense / spatial interpretation of the approach
- the user specifically identified alternating docking locations as a likely natural way to raise difficulty
- no new Android/platform regression was reported in that observation

Interpretation:
- the core Geometry v2 product hypothesis received positive physical-device evidence
- non-front anchor position is therefore a credible mission-difficulty/content axis
- this evidence motivates the separate `twindock-geometry-alternating-probe-v1` mission-composition experiment

This is not yet a full promotion of side geometry because player-anchor rotational tangential velocity remains intentionally unresolved.

## User-facing probe control
The side-probe APK contains both modes.

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

Therefore the positive device observation must not be interpreted as final acceptance of velocity semantics. Before promoting non-front craft broadly, separately evaluate whether player-anchor rotational tangential velocity should enter docking success truth.

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

## Next boundary
The direct A/B product question is positive enough to justify a mission-composition probe.

Next experiment:
- branch `twindock-geometry-alternating-probe-v1`
- alternate front / upper-side / front / lower-side / front anchors while keeping accepted Mission 01 motion constants unchanged
- evaluate whether anchor alternation itself creates a readable difficulty curve
