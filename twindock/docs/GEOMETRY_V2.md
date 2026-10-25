# Twin Dock — Docking Geometry v2

Status: **REFERENCE-ANCHOR FOUNDATION PASS / ACCEPTED**

Purpose: remove the hidden assumption that Twin Dock docking is permanently tied to a single fixed forward probe, while preserving the already accepted Mission 01 behavior as the control case.

Authority: this document defines the current Geometry v2 implementation boundary. It does not supersede the frozen V8/P0 control contract, accepted P1–P3 behavior, or the Android wrapper contract.

## 1. Product question answered by this slice
Can docking pose calculation be expressed through arbitrary local player/station anchors without changing the current reference shuttle's Mission 01 docking truth?

Answer: **yes**.

Evidence:
- implementation ref `0f60ab8f05b7c24dadb0a13a83f0951124754817`
- CI run `40240803157` SUCCESS
- 256 deterministic legacy-vs-anchor parity states PASS
- arbitrary non-front/asymmetric anchor closure test PASS
- accepted web regressions PASS
- Android staging/build PASS

## 2. Geometry data model
### Player craft
`state.ship.dockAnchor`

Current reference value:
```js
{ x: 40, y: 0, angle: 0 }
```

Meaning:
- `x`: anchor position in ship-local forward axis
- `y`: anchor position in ship-local lateral axis
- `angle`: anchor docking-frame orientation relative to ship body angle

### Station / target
`state.station.dockAnchor`

Current Mission 01 reference:
```js
{
  x: station.radius - PORT_CAPTURE_INSET,
  y: 0,
  angle: Math.PI,
  tracksRadius: true
}
```

`tracksRadius:true` is a Mission 01 compatibility behavior: the accepted circular station radius depends on viewport size, so its reference capture anchor continues to track the same radius/inset relationship as before.

Future arbitrary station anchors should use explicit local `x/y/angle` and disable radius tracking rather than forcing all content into the Mission 01 radial rule.

## 3. `src/geometry.js` ownership
`TD.Geometry` owns coordinate transforms only.

### `worldAnchor(...)`
Transforms a local anchor to world space and returns:
- world `x/y`
- world anchor `angle`
- rigid-body anchor `vx/vy`
- rotated local offset `rx/ry`

Rigid anchor velocity follows:
- `vx_anchor = vx_body - omega * ry`
- `vy_anchor = vy_body + omega * rx`

### `shipDockAnchor(state)`
Resolves the player anchor world frame.

### `stationDockAnchor(state)`
Resolves the station target anchor world frame, including Mission 01 radius tracking when enabled.

### `bodyPoseForWorldAnchor(...)`
Inverse transform used to solve a body's center position/body angle such that its local anchor lands at a desired world anchor pose.

Used by:
- initial dock-success snap
- continued dock-hold attachment

Geometry does **not** decide whether docking succeeds.

## 4. Docking truth after v2 foundation
`TD.Docking.metrics(state)` now derives:
- `probeX/probeY` from the player world anchor
- `captureX/captureY` from the station world anchor
- orientation error from player-anchor angle vs station-anchor angle
- station capture velocity from station-anchor rigid velocity

Legacy-compatible fields remain available so renderer/UI code does not need an unrelated broad rewrite.

`TD.Docking.checks()` and `canDock()` are unchanged in thresholds and logical structure.

## 5. Critical velocity-semantics decision
Geometry can compute rigid velocity at the player anchor. The docking success metric deliberately does **not** use it yet.

Current accepted relative-velocity calculation remains:
```text
ship linear velocity
minus
station capture-anchor rigid velocity
```

This preserves the V8/P1 contract where target rotation contributes tangential port velocity.

### Why player-anchor tangential velocity was not silently enabled
For a front anchor offset from the ship center, player angular velocity would add tangential velocity at that anchor. Switching to anchor-to-anchor rigid relative velocity would therefore change Mission 01's accepted `rel` metric even when all controls/thresholds are unchanged.

That would be a gameplay change disguised as a structural refactor.

Therefore:
- `Geometry.shipDockAnchor()` exposes the physically available rigid anchor velocity
- docking success continues using ship COM linear velocity for now
- before accepting side/rear craft, compare the legacy-compatible metric against full rigid anchor-to-anchor relative velocity as a separate bounded experiment
- do not bundle that decision with artwork, content layout or hull collision

## 6. Reference-shuttle parity proof
`tests/smoke.mjs` contains the old docking formulas directly and compares them against Geometry v2 across 256 deterministic states.

Compared fields include:
- ship probe world position
- station visual-port axis and world position
- station visual-port rigid velocity
- target angle
- capture position
- capture rigid velocity
- docking distance
- relative speed
- direction/orientation error
- spin error

Tolerance is numerical floating-point tolerance only.

This protects the reference shuttle from accidental semantic drift during future Geometry v2 work.

## 7. Arbitrary-anchor transform proof
The smoke test also constructs:
- an asymmetric station local anchor
- a non-front player local anchor with independent local orientation

It solves the player body pose using `bodyPoseForWorldAnchor`, matches the currently accepted velocity/spin truth, and verifies:
- zero anchor position error
- zero anchor orientation error
- zero accepted relative-speed error
- zero spin error
- `canDock === true`

This proves the new math is not limited to the front-center reference geometry.

It does **not** yet prove that non-front gameplay is readable or fun. That requires device content validation.

## 8. Presentation / feedback state
### Station visual port
`Docking.portState()` is now derived from the station capture anchor and target orientation, so station-side port presentation can follow arbitrary target anchors without a second physical truth.

### P2 orientation feedback
P2 relative orientation now compares `m.stationAnchor.angle` and `m.shipAnchor.angle`, matching docking truth.

Drift feedback still uses the same accepted relative velocity metric as docking success.

### Player craft visible port
The current renderer still draws the accepted reference front docking fixture in its existing location. This is valid for the reference control because the visible fixture and physical anchor coincide.

**Before side/rear craft device testing, the visible player docking fixture must be driven by `ship.dockAnchor`.**

Do not create a side physical anchor while leaving the visible active port at the nose.

## 9. Collision boundary
Broad hull collision is deliberately outside this Geometry v2 foundation.

Current bad-contact logic still uses docking proximity/relative-state behavior.

Do not introduce arbitrary polygon collision, detailed station mesh collision, or craft hull-clearance rules during the side-anchor readability probe.

Hull clearance is a later gated stage after non-front anchors prove distinct play.

## 10. Frozen contracts untouched
This slice did not change:
- FORCE_SCALE 58
- deadzone 0.10
- input exponent 2.05
- max speed 78
- max angular speed 0.90
- damping/torque model
- ship-frame camera
- docking distance 11
- docking relative speed 10
- docking direction threshold 0.095 rad
- docking spin threshold 0.10 rad/s
- Mission 01 stage profiles
- P2 threshold mapping
- P3 effects/transitions
- `presentation.js` angle-wrap protection
- Android wrapper/toolchain contract

## 11. CI evidence
Run: `40240803157`
Head: `0f60ab8f05b7c24dadb0a13a83f0951124754817`
Result: **SUCCESS**.

Passed:
- accepted web regressions
- Geometry v2 parity tests
- Android local asset staging
- pinned Capacitor shell generation
- Android contract checks before/after sync
- Gradle `assembleDebug`
- artifact upload

Artifact:
- name `twindock-android-debug`
- ID `12616678297`
- ZIP digest `sha256:f8b66fab07c25c9fb105b6592f13e6c82bbe6ee9967a71b92af2059f301397ee`

The Android wrapper itself was not changed; this build only proves shared-core packaging remains healthy.

## 12. Next bounded slice — Side/mid-body craft
Goal: determine whether local anchor geometry produces genuinely different play before generalizing content structures.

Smallest implementation:
1. make player docking fixture rendering follow `ship.dockAnchor`
2. preserve the reference craft as control/fallback
3. create one side/mid-body anchor prototype
4. keep handling constants identical
5. keep current Mission 01 station geometry initially
6. do not add hull collision yet
7. do not build a large craft schema

Device questions:
- is the active side port obvious from the craft itself?
- does docking require a different but learnable body posture/correction strategy?
- is ship-frame camera still intuitive?
- can the player recover after overshoot/bad orientation?
- do capture brackets/orientation/spin/drift cues still agree with what the player sees?
- does the new geometry create skill variety rather than arbitrary difficulty?

Promotion gate:
**at least one non-front anchor must produce clearly distinct but understandable gameplay on device.**

## 13. After side-anchor evidence
If PASS:
- add rear/asymmetric anchor probe
- then evaluate simplified hull clearance

If FAIL:
- diagnose port readability, camera interpretation and anchor placement before adding more craft or meta systems
- do not hide weak geometry behind speed increases, progression or extra HUD

## 14. Scope holds
Until non-front anchor gameplay is proven, hold:
- arbitrary polygon hull collision
- broad station geometry catalogue
- Mission 02 production
- mission schema generalization
- handling-stat differences between craft
- combat/economy/RPG/meta systems

Geometry variety must first prove it can extend the accepted core on its own.
