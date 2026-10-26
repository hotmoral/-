# Twin Dock — Alternating Dock Anchor Mission Probe

Status: **IMPLEMENTED / BUILD PASS / PHYSICAL DEVICE EVALUATION PENDING**

This is an experimental Geometry v2 mission-composition probe. It is not accepted gameplay yet.

## Authority boundary
Accepted continuation remains unchanged:
- branch `twindock-p3b-transition-v1`
- accepted checkpoint `e40352fcc2fd56919f493728015d4edc02571009`
- Geometry v2 reference-anchor foundation PASS / ACCEPTED

The prior side-port experiment remains separate:
- branch `twindock-geometry-side-probe-v1`
- implementation `828461d2178ce2e988241ac80f8dfabd43c6fc9b`
- user physical-device observation on 2026-10-26 KST: moving the player docking point materially changed spatial perception; alternating positions was expected to raise difficulty

Current experiment:
- branch `twindock-geometry-alternating-probe-v1`
- implementation commit `f4685b5c406a3bbc2a04c402e70bf54e20a239bd`

Do not promote this branch to accepted continuation until device play closes the product question.

## Product question
Can changing only the player-local docking anchor between stages create a useful difficulty curve and require different spatial correction strategies without retuning controls, thresholds, camera, or mission motion constants?

## Mission sequence
The five existing Mission 01 motion profiles remain in the same order and keep the same movement constants.

Only the player docking-anchor geometry changes:
1. STATIC — `REFERENCE` — front anchor `(40, 0, 0°)`
2. TRANSLATE — `SIDE_TOP` — upper mid-body anchor `(2, -31, -90°)`
3. ROTATE — `REFERENCE` — front anchor `(40, 0, 0°)`
4. COMBINED — `SIDE_BOTTOM` — lower mid-body anchor `(2, 31, +90°)`
5. FINAL — `REFERENCE` — front anchor `(40, 0, 0°)`

The sequence deliberately alternates front-vs-side anchor class at every stage boundary. It does not add rear/asymmetric geometry yet; that remains a later bounded probe.

## Architecture
New `src/craft-geometry.js` owns player docking-anchor definitions and applies them to the ship.

Mission profiles choose only `craftId`. `mission.js` applies the selected craft anchor before placing/orienting the target station.

This separates:
- craft-local geometry ownership
- mission composition / sequence ownership
- renderer-only probe visualization

`src/craft-probe.js` remains a presentation adapter:
- reference stages use the accepted front fixture unchanged
- side stages visually seal the old nose fixture
- active docking hardware is drawn at the current `ship.dockAnchor`
- no explanatory SIDE label is drawn; the probe is intended to test whether visible geometry itself is understandable

Required script order:
`geometry.js -> craft-geometry.js -> state.js -> mission.js`

Presentation order remains:
`renderer.js -> craft-probe.js -> presentation.js -> main.js`

## Frozen contracts untouched
This experiment does not change:
- FORCE_SCALE / deadzone / exponent
- torque / damping / speed caps
- physics integration
- docking thresholds
- accepted Mission 01 target motion constants
- ship-frame camera
- P2 threshold mapping
- P3 audio / haptics / transitions
- Android wrapper/platform contract
- broad hull collision model

Relative-velocity truth also remains the accepted Mission 01 definition:
- player side = ship COM linear velocity
- target side = actual station capture-anchor rigid velocity

Player-anchor rotational tangential velocity remains a separate unresolved product/physics question and is not silently introduced here.

## Automated evidence
GitHub Actions:
- run `40250411803`
- implementation head `f4685b5c406a3bbc2a04c402e70bf54e20a239bd`
- result **SUCCESS**

Passed:
- accepted web regressions
- Geometry v2 reference parity tests
- Mission 01 tests
- prior side-anchor contract tests
- new alternating-anchor sequence tests
- script syntax and ordering guards
- local Android staging
- Capacitor shell generation
- Android contract checks before/after sync
- Gradle debug APK build
- APK artifact upload

Artifact:
- name `twindock-android-debug`
- artifact ID `12620351221`
- artifact ZIP digest `sha256:1a62c2e5e3d967bb1da3d88520923678f3a87526916d45d624b59a30b30a4ca0`
- APK filename `app-debug.apk`
- APK bytes `4144501`
- APK SHA-256 `ddcd2712c4190c1680a6b54c7d6f79bff9d7300c830c9ab9e42003e33a62c985`

## Physical-device acceptance questions
Play all five docks as one continuous mission. The candidate is useful if device play shows:
1. each anchor change is visually discoverable without needing a dedicated explanatory HUD
2. front -> side -> front -> opposite-side transitions materially change posture planning
3. difficulty rises from spatial interpretation rather than control degradation or threshold tightening
4. returning to the front anchor requires a meaningful mental reframe rather than feeling random
5. upper and lower side anchors feel related but not identical
6. P2 position/orientation/spin/drift cues stay aligned with the visible active port
7. approaches remain recoverable with normal dual-RCS corrections
8. no control retuning or docking-threshold loosening is needed
9. no input, camera, presentation-angle, background, audio, haptic, transition, or Android-wrapper regression appears

## Next boundary
Do not add rear/asymmetric geometry or change velocity semantics before this device probe is evaluated.

On positive device evidence:
- record whether alternating anchors are a validated mission-difficulty axis
- decide whether to promote side/mid-body geometry to accepted Geometry v2 content
- then run a separate player-anchor rotational-velocity truth experiment before rear/asymmetric craft
