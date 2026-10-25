# Twin Dock Project Status

## Current phase
**Docking Geometry v2 reference-anchor foundation: PASS / ACCEPTED**

P0–P3 remain **ACCEPTED / CLOSED** and unchanged.
Android packaging/device parity remains **PASS / ACCEPTED** and the wrapper/platform contract remains **FROZEN**.

The first Geometry v2 slice has replaced the hidden fixed-forward-probe calculation in docking math with local docking anchors while preserving the accepted Mission 01 reference behavior.

Exact next boundary:
**side/mid-body craft geometry probe.**

Next product question:
**Does a non-front player docking anchor create a clearly different but understandable correction strategy without changing the accepted dual-RCS controls, ship-frame camera, docking thresholds, or recovery philosophy?**

Current continuation branch: `twindock-p3b-transition-v1`.
Live remote remains authoritative; copied SHAs are reference points only.

## Current accepted / pending stack
- P0 modular foundation / V8 parity: **ACCEPTED / CLOSED**
- P1 Mission 01 five-stage continuous loop: **ACCEPTED / CLOSED**
- P2 world-readable docking feedback: **ACCEPTED / CLOSED**
- P3-A event/audio/haptic foundation + angle-wrap protection: **ACCEPTED / CLOSED**
- P3-B stage-transition / final-completion polish: **ACCEPTED / CLOSED**
- P3 overall: **ACCEPTED / CLOSED**
- Android packaging preflight: **PASS / CLOSED**
- Android minimal wrapper/build: **BUILD PASS**
- Android physical-device parity: **PASS / ACCEPTED**
- Android wrapper/platform contract: **FROZEN**
- Geometry v2 reference-anchor foundation: **PASS / ACCEPTED**
- Reference-shuttle deterministic regression: **PASS**
- Side/mid-body craft probe: **NEXT / not yet implemented**
- Rear/asymmetric craft probe: **not started**
- Simplified hull clearance: **not started**

V8 remains the immutable fallback/control contract.
Frozen input, thrust, speed, camera semantics, docking truth and precision thresholds remain unchanged.

## Geometry v2 accepted foundation
Canonical detail:
`docs/GEOMETRY_V2.md`

Implementation reference:
- foundation commit: `0f60ab8f05b7c24dadb0a13a83f0951124754817`
- CI / Android build run: `40240803157`
- result: **SUCCESS**

Implemented:
- new `src/geometry.js` local-anchor transform layer
- player dock anchor stored as local `x / y / angle`
- station dock anchor stored as local `x / y / angle`
- Mission 01 reference ship remains `x=40, y=0, angle=0`
- Mission 01 station capture anchor remains the same radius/inset geometry as before
- docking position and orientation metrics now derive from anchor world transforms
- station target-anchor rigid velocity remains the source for accepted relative-velocity truth
- successful-dock snap and dock-hold attachment use inverse anchor transforms rather than `VISUAL_PROBE_X` body-center arithmetic
- P2 orientation feedback reads the same anchor frames used by docking truth
- station port presentation continues to derive from the same docking result

### Deliberately unchanged
Geometry v2 foundation did **not** change:
- V8/P0 control response
- thrust / torque / damping / speed limits
- ship-frame camera
- docking thresholds
- Mission 01 target profiles
- P2 truth thresholds
- P3 effects/transitions
- Android wrapper contract
- broad collision/hull model

### Relative-velocity compatibility decision
`TD.Geometry.shipDockAnchor()` can compute rigid velocity at the player anchor, including rotational tangential velocity.

However, `TD.Docking.metrics()` deliberately continues the accepted Mission 01 velocity contract:
- player side: existing ship linear velocity
- target side: station velocity at the actual capture anchor, including station rotational tangential velocity

Reason: silently switching Mission 01 to player-anchor rigid velocity would alter an already frozen success metric and could change difficulty even for the reference front probe.

This is **not forgotten technical debt**. Before accepting a non-front craft, player-anchor rigid velocity must be evaluated as an explicit bounded product/physics experiment against the accepted reference contract. Do not change it incidentally during renderer/content work.

## Geometry v2 validation evidence
`tests/smoke.mjs` now includes:
- 256 deterministic reference states comparing the new anchor implementation against the exact legacy docking formulas
- position, capture point, capture velocity, distance, relative speed, orientation and spin comparisons
- station visual-port state comparisons
- a non-front / asymmetric arbitrary-anchor transform case that closes at zero position/orientation error and satisfies the unchanged docking checks when velocity/spin are matched

CI run `40240803157` passed:
- accepted web regressions
- Geometry v2 reference parity tests
- local Android staging
- Capacitor shell generation
- Android contract verification before and after sync
- Gradle debug APK build
- artifact upload

New debug artifact from that run:
- artifact ID `12616678297`
- artifact name `twindock-android-debug`
- ZIP digest `sha256:f8b66fab07c25c9fb105b6592f13e6c82bbe6ee9967a71b92af2059f301397ee`

No new Android device parity replay is required for this reference-only mathematical refactor unless a concrete tactile/visual/platform mismatch appears. The Android wrapper itself did not change.

## Geometry v2 architecture boundary
### Geometry
Owns local anchor → world anchor transforms and inverse body-pose solving.
It does not own mission progression, input, physics integration, rendering style, or success thresholds.

### Docking
Consumes world anchor frames and owns metrics/checks/canDock.
It must remain the single truth used by P2 feedback.

### Physics
Owns body state/integration and uses Geometry only to maintain the body pose during dock hold.

### Mission
Owns which reference geometry is active. Mission 01 still installs its original station anchor geometry.

### Renderer / Feedback
Presentation reads docking/anchor truth; it must not invent a second physical anchor.
The current reference ship visual remains aligned with the front anchor. Anchor-driven player-port artwork becomes necessary before a side/rear craft can be device-tested.

## Exact next slice — Side/mid-body craft probe
Bounded goal:
- make the player docking fixture visually follow `ship.dockAnchor`
- create one side/mid-body anchor prototype only
- keep the current reference craft as control/fallback
- do not redesign the whole craft system or mission schema
- do not add hull-clearance collision yet
- do not alter controls or thresholds

Evaluate on device:
- can the player immediately identify the side port?
- does the required body posture/correction strategy feel meaningfully different from nose-first docking?
- does ship-frame camera remain understandable?
- can a bad approach be recovered naturally?
- does P2 orientation/position feedback still agree with the visible port?

Promotion condition:
**at least one non-front anchor produces distinct but understandable play without requiring large explanatory HUD or control retuning.**

## Frozen V8 / docking guards
Frozen values remain:
- FORCE_SCALE 58
- deadzone 0.10
- exponent 2.05
- max speed 78
- max angular speed 0.90
- station omega reference 0.18
- docking distance 11
- docking relative speed 10
- docking orientation error 0.095 rad
- docking angular-speed error 0.10 rad/s

Successful docking still requires all four simultaneously:
1. docking-point position
2. accepted relative linear velocity truth
3. anchor orientation
4. relative angular velocity

Avoid generous magnetic capture.

## Android accepted contract
The Android lane remains frozen at the accepted first wrapper:
- Capacitor 8.5.3
- Node 22+
- JDK 21
- minSdk 24
- targetSdk / compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- app ID `com.hotmoral.twindock`
- local/offline packaged assets
- `sensorLandscape`
- SystemBars native inset handling
- no native gameplay rewrite

Original physical-device parity passed on 2026-10-26 KST with no observed mismatch.
Do not reopen Android wrapper work merely because shared game-core content changes.

## P0–P3 accepted reference
### P0
- V8 modularized
- deterministic smoke PASS
- 12,000-frame V8 vs modular zero observed divergence
- mobile feel parity accepted
- closure ref `185a974dbd818386019677409f875640df27442f`

### P1
Mission 01 sequence:
1. STATIC
2. TRANSLATE
3. ROTATE
4. COMBINED
5. FINAL

Accepted: continuous state, deterministic background, target translation and rotating-port tangential velocity, recoverable collision/re-approach, frozen V8 feel.
Closure-before-P2 ref `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`.

### P2
World-readable feedback:
- position → capture brackets
- orientation → port/ship notches
- angular velocity → relative-spin trail
- relative linear velocity → drift arrow
- success → restrained green confirmation

Debug diagnostics remain under `?debug=1`.

### P3-A
Accepted audio/haptics/event layer and `src/presentation.js` continuous renderer-angle adapter.
Important fixed regression: distant background flip across physical `+π/-π` wrap.
Closure ref `62fa4d75301071256dabdb20fdb4c0eb6f97d3d4`.

### P3-B
Accepted non-blocking target transition and mission-complete polish; P3 overall CLOSED.

## Content direction
Canonical planning:
- `docs/CONTENT_EXPANSION_MAP.md`
- `docs/IDEA_BANK.md`

Current path:
`Geometry v2 reference foundation PASS`
→ `side/mid-body craft probe`
→ `rear/asymmetric craft probe`
→ `simplified hull clearance`
→ `station geometry`
→ `Mission 02`
→ `Mission 03`
→ `content/productization gate`
→ `Mission 04+ / justified meta`

Current reference shuttle remains a control craft, not universal final geometry.

## Development / validation policy
- bounded slice, one product question
- cheap multi-view consistency review before expensive work
- compare only contracts actually touched
- deterministic/static tests for geometry/math/contracts
- physical device for genuinely new tactile/visual/readability behavior
- do not replay closed P0–P3 or Android parity without a trigger
- platform fixes separate from gameplay tuning
- do not generalize mission/craft schemas before side/rear prototypes expose real needs

## Handoff rule
At each large-group closure update this file and `docs/SESSION_HANDOFF.md` together, then verify `START_HERE.md`, README and affected design docs agree on current truth and exact next boundary.
