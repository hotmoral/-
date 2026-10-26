# Twin Dock — Anchor Eccentricity Controlled Probe

Status: **IMPLEMENTED / BUILD VALIDATION PENDING**

This is an experimental Geometry v2 branch. It is not accepted gameplay.

## Parent evidence

Parent branch: `twindock-geometry-craft-shape-probe-v1`

Physical-device difficulty ordering from the combined craft/port probe:

`5 > 4 > 2 > 3 > 1`

The user explicitly rejected moving the craft rotation center / COM as a difficulty mechanism. That is a fixed invariant for this probe.

## Product question

With craft hull, port shape, controls, rotation center, docking thresholds and target motion all fixed, how much difficulty difference comes from docking-anchor eccentricity and direction alone?

## Controlled variables

Every stage uses:
- craft: `LONG CARGO`
- port shape: `RECT`
- accepted rotation-center / COM semantics unchanged
- accepted `ship.length` / `ship.width` physical values unchanged
- same station placement factors: `ahead=0.49`, `lateral=-0.10`
- same target body translation: `(4, -5)`
- same target angular velocity: `-0.14`
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

The comparison can therefore separate some direction effects from distance effects while keeping the craft rotation center fixed.

## Residual experimental limitation

The five trials are still played sequentially in one mission. Player learning and inherited ship motion across docks can influence subjective ordering. The target motion profile itself is now controlled, so this is substantially cleaner than the parent five-stage probe, but it is not a laboratory-isolated single-trial reset design.

If device evidence remains ambiguous, the next probe should use an explicit trial selector that resets to identical initial state for each anchor.

## Physical-truth boundaries

Still deferred:
- moving COM / rotation center
- true mass distribution / inertia changes
- player-anchor rotational tangential velocity in docking relative-speed truth
- recessed/internal bays before hull-clearance collision exists
- polygonal port collision

## Device question

Play all five and report difficulty ordering again.

Most useful comparisons:
- 1 vs 3: same radius 61, opposite side direction
- 2 vs 4: same radius 98, front vs rear
- 2 vs 5 vs 4: same radius ~98, different direction/placement
- r61 group vs r98 group: whether larger eccentricity consistently increases difficulty

Do not tune controls or docking thresholds from this probe. The goal is causal attribution, not balance.
