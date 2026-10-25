# Twin Dock — Session Handoff

This is the canonical fresh-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Authority / repository / continuation
- repository: `hotmoral/-`
- continuation branch: `twindock-p3b-transition-v1`
- live remote is authoritative
- past chats, memory, copied SHAs and this handoff are navigation aids only when they agree with live GitHub

Authority order:
`live remote > canonical documents > handoff > copied SHA/chat/memory`

Historical accepted refs:
- P0 closure: `185a974dbd818386019677409f875640df27442f`
- P1 closure before P2: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`
- P3-A closure: `62fa4d75301071256dabdb20fdb4c0eb6f97d3d4`
- Android successful wrapper implementation/build: `596ba9e4e89e4926cd10aad08908694572b0bf4b`
- Android parity closure documentation reference before Geometry v2: `f564650140043414d5aa405110f8703394b49b0e`
- Geometry v2 reference-anchor foundation implementation: `0f60ab8f05b7c24dadb0a13a83f0951124754817`

Copied SHAs are never higher authority than the current live branch.

## 2. Recovery order
Read before work:
1. `twindock/docs/START_HERE.md`
2. `twindock/PROJECT_STATUS.md`
3. `twindock/docs/SESSION_HANDOFF.md`
4. `twindock/docs/BASELINE_V8.md`
5. `twindock/docs/FOUNDATION_MANIFEST.md`
6. `twindock/docs/OPERATING_RULES.md`
7. `twindock/README.md`
8. `twindock/docs/CONTENT_EXPANSION_MAP.md`
9. `twindock/docs/GEOMETRY_V2.md` for current geometry work
10. `twindock/docs/ANDROID_PACKAGING_PREFLIGHT.md` only when Android history/contract is relevant
11. `twindock/docs/IDEA_BANK.md` for content ideation/promotion
12. exact source/tests relevant to the next bounded slice

Do not broadly refactor, retune controls, reopen Android parity, or replay accepted P0–P3 work before recovery establishes the exact live boundary.

Revalidation requires a relevant source change, prospective dependency, platform/package trigger, release requirement, or concrete mismatch.

## 3. Exact current state
- P0: ACCEPTED / CLOSED
- P1: ACCEPTED / CLOSED
- P2: ACCEPTED / CLOSED
- P3-A: ACCEPTED / CLOSED
- P3-B: ACCEPTED / CLOSED
- P3 overall: ACCEPTED / CLOSED
- Android packaging preflight: PASS / CLOSED
- Android minimal wrapper/build: BUILD PASS
- Android physical-device parity: PASS / ACCEPTED
- Android wrapper/platform contract: FROZEN
- Geometry v2 reference-anchor foundation: **PASS / ACCEPTED**
- reference-shuttle deterministic regression: **PASS**
- side/mid-body craft probe: **NEXT / not yet implemented**
- rear/asymmetric craft probe: not started
- simplified hull clearance: not started

Exact next boundary:
**build one side/mid-body player-anchor probe while keeping the reference shuttle as the control.**

Immediate product question:
**Does a non-front docking anchor create clearly distinct but understandable play while preserving the accepted controls, camera, thresholds and recovery loop?**

## 4. Project identity / experiential loop
Twin Dock is a mobile-first inertial spacecraft precision-docking game centered on embodied two-hand control.

Core control:
- two independent full-2D thumb/RCS pads
- common force produces translation
- differential/lever-arm force produces torque
- input changes motion state, not direct position
- inertia is preserved
- full free rotation from first play
- stationary start
- body-frame control

Experiential loop:
`mistake -> instability -> regain control -> recover -> re-approach -> precise docking`

Prefer recovery over immediate FAIL/RESET.

Rejected unless reopened as explicit experiment:
- one-hand primary control
- car/boat heading steering
- forward/back-only twin thrusters
- removing/stage-gating free rotation for tutorial
- generous magnetic capture replacing precision

## 5. Why the current control model exists
The accepted twin full-2D control emerged from tactile prototypes:
1. direct-touch inertial control proved motion-state control but fingers obscured the scene
2. separated one-hand force control preserved inertia but lacked embodied feel
3. heading/car steering restricted correction
4. one 2D joystick improved freedom but braking/reversal/fine correction stayed weak
5. faster one-hand 2D improved response but lacked two-hand cooperation
6. twin vertical-only thrust removed useful freedom and became harder, not clearer
7. two independent full-2D pads became the accepted breakthrough

Design conclusion:
**extra freedom is not inherently harder when every degree of freedom maps to an intuitive corrective action.**

Space docking turns that control into a skill task requiring simultaneous motion-state synchronization.

## 6. Frozen V8 contract
V8 remains the immutable fallback/control baseline until explicitly superseded.

Frozen values:
- FORCE_SCALE 58
- deadzone 0.10
- exponent 2.05
- max speed 78
- max angular speed 0.90
- station omega reference 0.18
- docking distance 11
- docking relative speed 10
- docking orientation/direction error 0.095 rad
- docking angular-speed error 0.10 rad/s

Exact artifact/hash are in `BASELINE_V8.md`.

Structural/content/platform work must not silently alter these. Tuning is a separate controlled experiment requiring device evidence.

## 7. Camera / motion comfort
Accepted camera: **ship-frame**.

The player craft remains visually mostly fixed while world/station geometry moves and rotates relative to it. This is gameplay feel, not a cosmetic option.

Motion-comfort mitigation:
- stable body-frame/HUD cues
- calmer distant background
- sparse relative-motion references
- deterministic background identity

Do not solve motion comfort by removing rotation freedom.

### P3-A presentation angle protection
Physical `ship.angle` remains wrapped for gameplay.
`src/presentation.js` supplies a continuous renderer-facing visual angle through a renderer wrapper/Proxy.

This prevents fractional distant parallax from jumping across physical `+π/-π` without changing physical/camera truth.

Required loading chain:
`renderer.js -> presentation.js -> main.js`.

Do not remove/bypass this adapter or move the fix into physics casually.

## 8. Docking truth
Successful docking still requires all four simultaneously:
1. docking-point position
2. accepted relative linear velocity truth
3. docking-anchor orientation
4. relative angular velocity

P2 readiness feedback and actual success use the same checks/thresholds.
Visible and physical docking geometry must agree.
Avoid generous magnetic capture.

### Current accepted velocity semantics
The frozen Mission 01 contract is preserved:
- player contribution uses ship linear velocity
- station contribution uses velocity at the target capture anchor
- station capture velocity includes rotational tangential velocity from station rotation

Geometry v2 computes rigid velocity at both anchors, but **player-anchor tangential velocity is not yet part of success truth**.

Why: adding it silently would change the already accepted reference docking metric. Before non-front craft acceptance, evaluate this as an explicit bounded experiment rather than an incidental refactor.

## 9. Architecture boundaries
### Input
Pointer identity, dual-touch tracking, response curve, body-frame commands.

### Physics
Position, velocity, body angle, angular velocity, inertia, collision response.

### Geometry
Local docking anchors and transforms only:
- local anchor `x / y / angle`
- local → world anchor pose/rigid velocity
- inverse solve from desired world anchor pose to body center/angle

Geometry does not own mission logic or docking thresholds.

### Docking
Consumes anchor world frames; owns position/velocity/orientation/spin metrics, checks and canDock truth.

### Camera
World → ship-frame presentation; never mutates physical truth.

### Renderer
World visuals and visible docking hardware. Must derive future non-front port presentation from the same anchor data rather than inventing a second location.

### Feedback
P2 world-readable readiness cues only; no physics mutation. Orientation now reads the same anchor frames as docking truth.

### Mission
Stage/target sequence and persistent ship state between docks. Mission 01 still installs its original station geometry.

### Effects
Presentation audio/haptics only.

### Presentation adapter
Visual continuity only; wrapped physical values may be adapted for rendering, never source-state mutation.

### Transitions
Stage/final presentation only.

### Future content
Do not build a broad generic craft/mission schema before side/rear prototypes expose real requirements.

## 10. P0 — modular foundation
Status: ACCEPTED / CLOSED.

Evidence:
- V8 modularized
- deterministic smoke PASS
- 12,000-frame V8-vs-modular comparison
- zero observed divergence in position, velocity, angle, angular velocity, station angle and docking metrics
- mobile feel parity accepted

V8 remains fallback/control.

## 11. P1 — Mission 01
Status: ACCEPTED / CLOSED.

Sequence:
1. STATIC
2. TRANSLATE
3. ROTATE
4. COMBINED
5. FINAL

Accepted behavior:
- continuous five-target mission
- persistent ship state between docks
- station translation included in relative velocity
- rotating-port tangential velocity included
- deterministic background
- recoverable collision/re-approach
- frozen V8 feel unchanged

Exact mission duration was not separately instrumented; do not invent one.
Mission 01 is reference/basic content, not the total intended game.

## 12. P2 — world-readable feedback
Status: ACCEPTED / CLOSED.

Normal UI uses world-readable cues; QA diagnostics remain under `?debug=1`.

Accepted cues:
- position -> capture brackets
- orientation -> ship/port notches
- angular velocity -> relative-spin trail
- relative linear velocity -> drift arrow
- success -> restrained green ring

Feedback shares docking truth/thresholds.

## 13. P3-A — audio/haptic/event foundation
Status: ACCEPTED / CLOSED.

Accepted:
- restrained continuous RCS hiss
- bad-contact / soft-capture / latch / next-target / completion cues
- short haptics
- `?audio=0`, `?haptics=0`
- user-gesture AudioContext arming
- background/pause RCS silence
- `src/presentation.js` angle-wrap protection

Historical issue: fifth-dock distant background flip came from fractional parallax using wrapped physical angle. It was fixed presentation-only and device recheck passed.

## 14. P3-B — transition/final polish
Status: ACCEPTED / CLOSED.

Accepted:
- short dock HUD pulse
- ~0.98 s next-target sweep + compact cue
- ~1.9 s final edge frame/completion cue
- completed HUD state until reset
- `pointer-events:none`
- reduced-motion support
- no blocking central modal

P3 overall CLOSED.

## 15. Android packaging / device parity
Status: ACCEPTED / FROZEN wrapper contract.
Canonical detail: `docs/ANDROID_PACKAGING_PREFLIGHT.md`.

Toolchain:
- Capacitor 8.5.3
- Node 22+
- JDK 21
- minSdk 24
- targetSdk / compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- app ID `com.hotmoral.twindock`

Wrapper:
- thin Capacitor Android shell
- local/offline assets
- no native physics/input/docking/camera rewrite
- phone-first `sensorLandscape`
- SystemBars native inset handling
- existing Web Audio / `navigator.vibrate()` path

Physical Android device parity passed on 2026-10-26 KST with all fixed checks reported normal.
Do not reopen wrapper/platform tuning without a concrete platform trigger.

## 16. Geometry v2 reference-anchor foundation
Status: **PASS / ACCEPTED**.
Canonical detail: `docs/GEOMETRY_V2.md`.

Implementation:
- `src/geometry.js`
- `state.ship.dockAnchor = {x,y,angle}`
- `state.station.dockAnchor = {x,y,angle,...}`
- `Docking.metrics()` derives player/target position and orientation from world anchors
- station reference anchor tracks current Mission 01 radius/inset
- dock-success snap and dock-hold use inverse anchor pose solving
- P2 orientation uses anchor frames

Reference ship remains:
- local anchor x = 40
- local anchor y = 0
- local anchor angle = 0

Reference station remains mathematically equivalent to the previous radial port/capture inset.

### Regression evidence
Foundation ref: `0f60ab8f05b7c24dadb0a13a83f0951124754817`.

`tests/smoke.mjs`:
- 256 deterministic states compare new metrics to exact previous formulas
- compares probe/capture points, station port state, capture velocity, distance, relative speed, direction and spin
- arbitrary non-front/asymmetric anchor transform also closes at zero pose error under matched accepted velocity/spin

CI run `40240803157`: SUCCESS.
Passed web regressions, staging, Capacitor generation, Android contract checks, Gradle build and artifact upload.

Artifact:
- ID `12616678297`
- ZIP digest `sha256:f8b66fab07c25c9fb105b6592f13e6c82bbe6ee9967a71b92af2059f301397ee`

No control/threshold/camera/Mission/P3/Android-wrapper changes were made.

### Validation-cost note
The first standalone `geometry.js` file addition was accidentally committed separately and triggered one extra successful CI run before the atomic integration commit. It did not enter runtime because `index.html` had not yet loaded it. Do not repeat this pattern; batch future source edits before moving the branch ref.

## 17. Exact next slice — side/mid-body craft probe
Do not start hull collision or Mission 02 yet.

Smallest coherent next implementation:
- player docking fixture rendering must follow `ship.dockAnchor`
- preserve exact reference rendering as control
- add one side/mid-body anchor prototype
- avoid broad craft-data schema
- keep all handling constants identical
- keep current station/Mission 01 geometry initially so anchor placement is the main changed skill

Device questions:
- is the active side port immediately readable?
- does it demand a distinct correction/posture strategy?
- does ship-frame camera remain intuitive with a non-nose port?
- is recovery after a bad approach natural?
- do P2 cues match visible/physical anchor truth?

If side-anchor play is not distinct/readable, do not scale to many craft skins. Diagnose geometry/readability first.

Before accepting the side craft, separately decide whether player-anchor rotational tangential velocity should join docking-relative velocity. Do not sneak that change into the visual prototype.

## 18. Content direction
Canonical:
- `docs/CONTENT_EXPANSION_MAP.md`
- `docs/IDEA_BANK.md`

Current sequence:
`reference Geometry v2 foundation PASS`
→ `side/mid-body craft`
→ `rear/asymmetric craft`
→ `simplified hull clearance`
→ `station geometry`
→ `Mission 02`
→ `Mission 03`
→ `content/productization gate`
→ `Mission 04+ / justified meta`

Mission 03 is a decision gate, not the end of content.

Hold near-term:
- combat/weapons
- economy/resource harvesting
- crafting
- RPG stats
- large open world
- PvP
- complex narrative systems
- fuel economy as primary loop
- large inventory/equipment systems

## 19. Cloudflare role
Existing `/twindock/` exposure is browser-validation convenience only.
Source authority remains GitHub. Android uses packaged local assets. Do not modify Timing Defense Worker/API behavior for Twin Dock content work.

## 20. Operating / consistency discipline
Every slice:
1. recover live state
2. state one product question
3. identify frozen contracts touched
4. review baseline, architecture, lifecycle, visual/physical truth, regression history, platform coupling, future extensibility and validation cost
5. define acceptance first
6. implement the smallest coherent change
7. run only relevant deterministic/static regressions
8. require device evidence for genuinely new tactile/visual behavior
9. promote only after acceptance
10. synchronize canonical handoff at large-group closure

Avoid whole-repository rescans, accepted-phase replay, broad scope, small-task Codex use, redundant CI and platform/gameplay mixing.

## 21. Known risks
- player visual port diverging from `ship.dockAnchor` during side/rear prototypes
- accidental switch to player-anchor tangential velocity changing frozen Mission 01 difficulty
- anchor orientation feedback diverging from docking truth
- current reference craft accidentally treated as universal geometry
- broad hull collision entering before anchor gameplay is validated
- camera semantic drift
- `presentation.js` bypass / angle-wrap regression
- generous auto-capture creep
- mission schema over-generalized before prototypes reveal needs
- Android wrapper unnecessarily reopened for shared-core changes
- Idea Bank mistaken for roadmap

## 22. Large-group closure discipline
At closure:
- record exact implementation/decision boundary
- record relevant tests/device evidence
- distinguish deterministic/reference PASS from device/content acceptance
- synchronize `PROJECT_STATUS.md` + this handoff
- verify `START_HERE.md`, README and affected design docs
- record exact next boundary and known risks
- refresh live refs
- ensure no stale canonical contradiction

A fresh session must recover project identity, accepted history, rationale, frozen contracts, architecture, Android state, current Geometry v2 decisions, unresolved velocity semantics and the exact next product question without relying on conversation memory.
