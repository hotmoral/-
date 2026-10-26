# Twin Dock — Anchor Eccentricity Controlled Probe

Status: **BUILD PASS / PHYSICAL DEVICE EVALUATED / CAUSAL RESULT CONFOUNDED**

This is an experimental Geometry v2 branch. It is not accepted gameplay.

## Parent evidence

Parent branch: `twindock-geometry-craft-shape-probe-v1`

Physical-device difficulty ordering from the combined craft/port probe:

`5 > 4 > 2 > 3 > 1`

The user explicitly rejected moving the craft rotation center / COM as a difficulty mechanism. That remains a fixed invariant.

## Intended product question

With craft hull, port shape, controls, rotation center, docking thresholds and target motion fixed, how much difficulty difference comes from docking-anchor eccentricity and direction alone?

## Intended controlled variables

Every stage uses:
- craft: `LONG CARGO`
- port shape: `RECT`
- accepted rotation-center / COM semantics unchanged
- accepted `ship.length` / `ship.width` physical values unchanged
- same station placement factors: `ahead=0.49`, `lateral=-0.10`
- same station-COM body translation: `(4, -5)`
- same station angular velocity: `-0.14`
- same docking thresholds
- same dual-RCS controls
- same ship-frame camera

No craft-specific mass, torque, damping or speed tuning is introduced.

## Five anchor trials

1. `상단 측면 · r61`
   - `(x=0, y=-61)`
   - angle `-90°`

2. `전방 · r98`
   - `(x=98, y=0)`
   - angle `0°`

3. `하단 측면 · r61`
   - `(x=0, y=61)`
   - angle `+90°`

4. `후방 · r98`
   - `(x=-98, y=0)`
   - angle `180°`

5. `우하단 모서리 · r98`
   - `y=36`
   - `x=sqrt(98²-36²) ≈ 91.15`
   - radial distance exactly ~98
   - port angle `45°`

This provides two matched-radius groups:
- `r61`: upper side vs lower side
- `r98`: front vs rear vs corner

## Rotation-center regression guard

Automated tests verify that applying each anchor setup does not change:
- ship center `x/y`
- ship body angle
- accepted physical `ship.length`
- accepted physical `ship.width`

The probe therefore does not manufacture difficulty by moving COM or changing the accepted torque lever.

## Automated evidence

GitHub Actions:
- run `40260448984`
- implementation head `1ff61e879295c15c106a13222a3865b9fecc5918`
- result **SUCCESS**

Passed:
- accepted presentation-angle regression
- accepted Geometry v2 smoke/reference regression
- controlled Mission profile tests
- controlled non-front anchor contract tests
- retained craft-family/port-shape regression
- new anchor-eccentricity controlled tests
- JS syntax checks
- local Android staging
- Capacitor Android shell generation
- Android contract checks before/after sync
- Gradle debug APK build
- artifact upload

Artifact:
- artifact ID `12624068522`
- extracted APK bytes `4,147,309`
- extracted APK SHA-256 `0dd3b3dc57a4490c2206ef1609be0f160d59b88ce2128369ad77569b74537693`

## 2026-10-26 physical-device result

User-reported difficulty, hardest to easiest:

`2 > 4 > 1 > 3 > 5`

The user also reported that the station appeared to change movement/rotation speed in a regular pattern and specifically asked whether control sensitivity or station motion had changed.

### Control sensitivity did not change

The accepted control constants and physics code are unchanged:
- `FORCE_SCALE=58`
- deadzone `0.10`
- exponent `2.05`
- max speed `78`
- max angular speed `0.90`
- accepted damping/torque integration unchanged

### The causal-control assumption was nevertheless incomplete

Although all five profiles use identical **station-COM** body translation `(4,-5)` and identical `omega=-0.14`, the actual gameplay-relative target motion is not identical.

Two mechanisms create a systematic difference:

1. **Inherited ship motion across sequential docks**
   - on successful docking, the ship is assigned the station capture anchor velocity (`ship.vx/vy = captureVx/captureVy`) and station angular velocity
   - the next stage does not reset ship linear/angular motion to an identical baseline
   - therefore each trial inherits motion produced by the previous anchor orientation

2. **Station capture-anchor tangential velocity depends on target orientation**
   - station COM velocity is fixed, but the capture anchor also has `omega × r` tangential velocity
   - changing the player anchor angle changes the station orientation required for geometric alignment
   - this rotates the station capture-anchor tangential-velocity vector
   - therefore identical station-COM translation/omega does **not** imply identical capture-anchor world velocity

The same issue also means identical station-center placement factors do not guarantee identical target capture-anchor start position across anchor orientations.

Consequently, `2 > 4 > 1 > 3 > 5` is valid device evidence about this build, but **must not be promoted as a causal anchor-direction/eccentricity ranking**.

## Required corrected probe

The next probe must control the quantities that docking actually sees, not only station COM settings.

For every anchor trial:
- same Long Cargo hull
- same rectangular player/target port semantics
- fixed accepted craft rotation center / COM
- identical ship initial `x/y`
- identical ship initial `vx/vy = 0`
- identical ship initial angle and angular velocity
- identical target **capture-anchor world position** relative to the ship
- identical target **capture-anchor world linear velocity**
- identical target angular velocity
- derive station center pose and station COM velocity from that capture-anchor truth
- reset each trial independently rather than carrying previous dock motion forward

Then vary only the player docking anchor local `(x,y,angle)`.

## Physical-truth boundaries

Still deferred:
- moving COM / rotation center
- true mass distribution / inertia changes
- player-anchor rotational tangential velocity in docking relative-speed truth
- recessed/internal bays before hull-clearance collision exists
- polygonal port collision

## Disposition

This v1 probe remains useful because it exposed a lifecycle/relative-motion confound that a static parameter comparison would miss.

Do not tune controls or docking thresholds from its subjective difficulty order.
