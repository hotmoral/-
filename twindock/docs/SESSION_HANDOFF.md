# Twin Dock — Session Handoff

This is the canonical new-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Authority / repository / current continuation
- Repository: `hotmoral/-`
- Current continuation branch: `twindock-p3b-transition-v1`
- Live remote is authoritative.
- Past chats, memories, copied SHAs and this handoff are navigation aids only when they agree with live GitHub.

Historical accepted refs:
- P0 foundation: `185a974dbd818386019677409f875640df27442f`
- P1 closure before P2: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`
- P3-A closure: `62fa4d75301071256dabdb20fdb4c0eb6f97d3d4`
- P3-B accepted branch: `twindock-p3b-transition-v1`
- Android packaging preflight closure document commit: `f482770af7e08cbdb6dcecda0f1d21aae9ed3897`

Copied SHAs are never higher authority than the current live branch.

## 2. Required recovery order
Before proposing or implementing work, read in this order:
1. `twindock/docs/START_HERE.md`
2. `twindock/PROJECT_STATUS.md`
3. `twindock/docs/SESSION_HANDOFF.md`
4. `twindock/docs/BASELINE_V8.md`
5. `twindock/docs/FOUNDATION_MANIFEST.md`
6. `twindock/docs/OPERATING_RULES.md`
7. `twindock/README.md`
8. `twindock/docs/CONTENT_EXPANSION_MAP.md`
9. `twindock/docs/IDEA_BANK.md` when content ideation/promotion is relevant
10. `twindock/docs/ANDROID_PACKAGING_PREFLIGHT.md` for the current Android lane
11. exact source/tests relevant to the next bounded slice

Do not delegate, refactor broadly, generate an APK, or rerun expensive validation before the recovery pass establishes the exact live boundary.

Already ACCEPTED / CLOSED / FROZEN work must not be re-tested from scratch merely because a new session started. Revalidation requires a relevant source change, concrete mismatch, prospective dependency, or platform/package change that directly affects the contract.

## 3. Current exact state
- P0: ACCEPTED / CLOSED
- P1: ACCEPTED / CLOSED
- P2: ACCEPTED / CLOSED
- P3-A: ACCEPTED / CLOSED
- P3-B: ACCEPTED / CLOSED
- P3 overall: ACCEPTED / CLOSED
- Android packaging preflight: PASS / CLOSED
- Android wrapper implementation: **not yet implemented**
- APK: **not yet generated**
- Android physical-device parity: **not yet validated**
- Docking Geometry v2: **not yet implemented**

Exact next boundary:
**minimal Capacitor Android wrapper implementation -> debug APK -> physical Android parity validation.**

After Android parity PASS:
**freeze wrapper contract -> return to shared game core -> Docking Geometry v2.**

## 4. Project identity / core experience
Twin Dock is a mobile-first inertial spacecraft precision-docking game centered on embodied two-hand control.

The player uses two independent full-2D RCS pads. Their common force creates translation; their differential/lever-arm effect creates rotation.

Input changes motion state rather than directly moving the ship.

Core experiential loop:
`mistake -> instability -> regain control -> recover -> re-approach -> precise docking`

Mistakes should usually remain recoverable rather than immediately forcing FAIL/RESET.

Rejected directions unless a new explicit product experiment is opened:
- one-hand primary control
- car/boat heading steering
- forward/back-only twin thrusters
- removing free rotation for tutorial simplicity
- unlocking rotation later
- large magnetic capture that substitutes for precision

## 5. How the control model was reached
Early tactile exploration established the current structure:
1. direct-touch inertial object control proved motion-state control but fingers obscured play
2. separated one-hand force control preserved inertia but lacked embodied feel
3. heading/car-like steering constrained correction
4. one 2D joystick improved freedom but braking/reversal remained weak
5. faster one-hand control improved responsiveness but still lacked two-hand cooperation
6. twin vertical-only thrust removed useful freedom and made control harder
7. two independent full-2D pads became the accepted breakthrough

Design conclusion:
**extra freedom is not inherently harder when every degree of freedom maps to an intuitive corrective action.**

The space-docking theme then made the control model a skill task requiring simultaneous position, relative velocity, orientation and angular-velocity synchronization.

## 6. Frozen V8 control contract
V8 is the immutable fallback/control baseline until explicitly superseded.

Do not silently change during platform, structure, UI or content work:
- FORCE_SCALE = 58
- deadzone = 0.10
- input exponent = 2.05
- max speed = 78
- max angular speed = 0.90
- station omega reference = 0.18
- docking distance = 11
- docking relative speed = 10
- docking direction/orientation error = 0.095 rad
- docking angular-speed error = 0.10 rad/s

Exact baseline artifact/hash live in `BASELINE_V8.md`.

Structural refactor and control tuning are separate changes. Any tuning requires an explicit controlled experiment and device validation.

## 7. Camera / motion-comfort contract
Accepted camera: **ship-frame**.

The player craft remains visually mostly fixed while nearby world/station geometry moves and rotates relative to it. This is part of the game feel, not a cosmetic choice.

Motion-comfort mitigation:
- stable body-frame/HUD cues
- calmer distant background
- sparse relative-motion references
- deterministic background identity

Do not solve motion comfort by removing rotation freedom.

### P3-A angle-wrap protection
Physical `ship.angle` remains wrapped in normal gameplay coordinates.

`src/presentation.js` wraps the renderer with a Proxy and supplies a continuous renderer-facing visual angle. This prevents distant fractional parallax from jumping at physical `+π/-π` wrap without changing physics or camera truth.

Script/order guard:
`renderer.js -> presentation.js -> main.js`

Do not remove this adapter, bypass it during packaging, or move the fix into physics casually.

## 8. Docking truth
Successful docking requires all four simultaneously:
1. docking-point position
2. relative linear velocity
3. orientation
4. relative angular velocity

Relative velocity includes:
- target translation
- target rotational tangential velocity at the docking port

Visible/internal docking geometry must agree.
P2 readiness feedback and actual success thresholds must agree.
Avoid generous magnetic capture.

## 9. Architecture responsibility contract
### Input
- pointer identity
- dual-touch tracking
- response curve
- body-frame command vectors

### Physics
- position / velocity
- angle / angular velocity
- inertial state
- collision response

### Docking
- geometry
- relative metrics
- four-condition truth
- success/recoverable collision criteria

### Camera
- world -> ship-frame transform
- never mutate physical truth

### Renderer
- world visuals
- visible docking hardware

### Feedback
- world-readable P2 readiness cues
- no physics mutation

### Mission
- target/stage sequence
- persistent ship state between dockings

### Effects
- audio/haptics presentation only

### Presentation adapter
- rendering continuity/readability only
- protects angle-wrap presentation without mutating physics

### Transitions
- stage/final presentation only
- no gameplay truth mutation

### Future geometry/content
- craft/station anchors and collision geometry should become data-driven only after bounded prototypes expose actual requirements

Keep these boundaries intact during Android work.

## 10. P0 — modular foundation / V8 parity
Status: **ACCEPTED / CLOSED**

Result:
- V8 modularized
- deterministic smoke PASS
- 12,000-frame V8-vs-modular comparison
- zero observed divergence in position, velocity, angle, angular velocity, station angle and docking metrics
- mobile feel parity accepted

V8 remains the immutable fallback/control point.

## 11. P1 — Mission 01
Status: **ACCEPTED / CLOSED**

Product question:
Does the accepted control remain compelling across a continuous multi-target mission?

Accepted answer: **yes**.

Mission 01 sequence:
1. STATIC
2. TRANSLATE
3. ROTATE
4. COMBINED
5. FINAL

Accepted behavior:
- five deterministic target profiles
- ship state persists between docks
- target translation participates in docking-relative velocity
- rotational port tangential velocity participates in docking-relative velocity
- deterministic background persists
- collisions remain recoverable
- V8 feel unchanged

Do not invent a measured 3–5 minute mission duration; exact duration was not separately instrumented.

Mission 01 is the reference/basic mission, not the intended total content volume.

## 12. P2 — world-readable docking feedback
Status: **ACCEPTED / CLOSED**

Accepted normal presentation:
- compact mission progress/status
- old permanent relative-speed number removed from normal play
- old four-condition debug checklist removed from normal play
- debug diagnostics retained under `?debug=1`

World feedback:
- position -> capture brackets
- orientation -> ship/port notches
- angular velocity -> relative-spin trail
- relative linear velocity -> drift arrow
- success -> restrained green ring

Feedback uses the same docking truth/thresholds as actual docking success.

## 13. P3-A — audio / haptic / event feedback
Status: **ACCEPTED / CLOSED**

Accepted behavior:
- restrained continuous RCS hiss
- bad-contact mechanical/noise cue + short haptic
- soft-capture cue + short haptic
- latch cue
- delayed next-target cue
- mission-complete cue
- `?audio=0`
- `?haptics=0`
- mobile AudioContext arm/resume on `pointerdown`, `touchstart`, `click`
- RCS sound silences on pause/reset/background

Issue history:
- audio initially appeared silent at low media volume; activation and gain were hardened conservatively and practical-volume device recheck passed
- fifth-dock distant-background flip was traced to fractional parallax using wrapped physical angle and fixed in the presentation layer

Device acceptance confirmed:
- audio/haptics satisfactory and low-fatigue
- contact vs capture distinct
- capture/latch/next-target sequence satisfactory
- no touch/control/camera regression reported
- no background flip recurrence

## 14. P3-B — transition / final polish
Status: **ACCEPTED / CLOSED**

Accepted implementation:
- `src/transitions.js`
- `transitions.css`
- brief dock pulse in Mission HUD
- ~0.98 s thin sweep for next target
- compact target/stage label
- ~1.9 s low-opacity final edge frame
- compact completion cue
- completed HUD state until reset
- `pointer-events:none`
- reduced-motion support
- no large central modal

Device result: PASS / ACCEPTED.

P3 overall is CLOSED. Do not re-open it without a real trigger.

## 15. Current UI direction
Preserve:
- open central playfield
- transparent lower-corner controls
- compact mission/status UI
- world-readable docking information
- sparse numeric instrumentation
- debug checklist hidden in normal play

Do not freeze the current craft silhouette/front port as the final content geometry.

## 16. Content expansion direction
Canonical documents:
- `docs/CONTENT_EXPANSION_MAP.md`
- `docs/IDEA_BANK.md`

The current shuttle/front-center port is reference content only.

Future intended content axes:
- craft silhouette/proportions
- craft docking-anchor local position
- craft docking-anchor local orientation
- station geometry
- station port geometry
- target translation/rotation
- initial relative pose
- approach corridor / clearance
- simplified craft/station hull collision
- mission composition
- later scoring/mastery if the physical content grammar proves sustainable

Idea lifecycle:
`BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`

`IDEA_BANK.md` is not a roadmap.

Post-Android path:
`Docking Geometry v2`
→ `reference-shuttle regression`
→ `side/mid-body craft`
→ `rear/asymmetric craft`
→ `simplified hull clearance`
→ `station geometry`
→ `Mission 02`
→ `Mission 03`
→ `content/productization gate`
→ `Mission 04+ / justified scoring, unlocks, records, selection`

Mission 03 is a decision gate, not the end of the game.

Near-term hold:
- combat/weapons
- resource economy
- crafting
- RPG stat trees
- large open world
- PvP
- complex narrative systems
- fuel economy as primary loop
- large inventory/equipment systems

## 17. Android packaging preflight — PASS / CLOSED
Canonical contract:
`docs/ANDROID_PACKAGING_PREFLIGHT.md`

Product question:
Can the accepted web game be packaged faithfully on Android without native gameplay rewrite or platform-driven gameplay tuning?

Preflight answer: **yes; no blocking source/contract contradiction found.**

This is not device parity. APK implementation/testing remains outstanding.

### Chosen stable toolchain
- Capacitor core/CLI/Android: 8.5.3
- Node.js: 22+
- Android Studio: 2025.2.1+
- app name: Twin Dock
- application ID: `com.hotmoral.twindock`
- versionName: 0.1.0
- versionCode: 1
- minSdk: 24
- targetSdk: 36
- compileSdk: 36
- AGP: 8.13.0
- Gradle: 8.14.3
- JDK: 17

Capacitor 9 is not selected while pre-release/alpha.

### Asset packaging contract
- use a deterministic generated web directory such as `www/`
- current root HTML/CSS/JS remains source authority
- generated package is not a second editable source tree
- copy only runtime assets
- preserve relative paths and script order
- no remote runtime dependency
- APK must not load Twin Dock from Cloudflare

The stock Capacitor INTERNET permission may remain during the first probe, but Twin Dock gameplay itself must remain offline. Permission removal is a separate least-privilege cleanup after parity if justified.

### Input contract / highest risk
Current web implementation:
- independent left/right `pointerId`
- pointer capture attempted on each pad
- window-scoped move/up/cancel
- `touch-action:none`
- background visibility clears input

Android device must prove:
- two simultaneous pointers remain distinct
- edges do not lose control
- pointer cancel/reacquire works
- background/resume cannot leave stuck thrust

Do not tune controls to hide a WebView defect.

### Orientation / display
First parity policy:
- `sensorLandscape`
- Android app category `game`
- retain portrait web blocker as fallback
- remain resilient to resize/configuration changes

### Safe area / system bars
Android 16 edge-to-edge must be treated explicitly.

Initial policy:
- SystemBars inset handling `native`
- initial viewport-fit hint `cover`
- system bars visible by default in the first probe
- current HTML Fullscreen API remains unchanged until device evidence shows a problem
- no controls/HUD may be obscured by cutout/navigation/system insets

### Lifecycle
Warm background/foreground:
- preserve mission/world state
- clear active touches
- silence RCS audio while hidden
- prevent huge physics time step
- preserve deterministic world/background

Cold process recreation may restart Mission 01. Persistent save/restore is not part of this milestone.

### Android Back
First parity build uses normal system behavior; do not add custom navigation preemptively.

Requirements:
- Back must not invoke game reset
- returning to a still-alive activity should preserve state
- target SDK 36 predictive-back behavior must not crash or corrupt the WebView

If accidental exits materially harm play, implement pause-first Back later as a bounded platform-only slice using modern back APIs.

### Audio / haptics
- keep Web Audio implementation first
- retain real user-gesture arming
- keep `navigator.vibrate()` first
- only introduce native haptics if device evidence shows a concrete WebView mismatch

### Deterministic background / presentation
- seeded star field must retain identity across resize/resume
- `starFieldReady` prevents regeneration
- presentation-angle Proxy must remain active
- fifth-dock background flip must not recur

## 18. Exact next bounded slice
**Minimal Android wrapper implementation.**

Authorized scope:
1. add Capacitor 8.5.3 dependencies/config
2. add deterministic staging into `www/`
3. generate/add Android platform
4. apply app ID/version/SDK/orientation/inset contract
5. make only platform-required source changes
6. run existing relevant JS regressions + build/static checks
7. produce debug APK
8. stop for physical-device parity validation

Not authorized in this slice:
- native gameplay rewrite
- control tuning
- Mission 01 redesign
- P2/P3 redesign
- Docking Geometry v2
- Mission 02
- scoring/unlock/meta work

## 19. Android APK acceptance contract
Before implementation, acceptance is fixed:
- install/cold launch stable
- landscape correct
- dual-touch identity stable
- left/right RCS feel materially equivalent
- no edge touch loss/stuck input
- background/resume clears old touches and accepts new ones
- no warm-resume mission reset
- safe area/system bars do not cover controls
- fullscreen behavior does not corrupt layout/state
- ship-frame camera correct
- parallax continuous across angle wrap
- fifth-dock background flip absent
- Web Audio works after normal interaction
- haptics work or limitation is identified concretely
- all five Mission 01 docks work
- target translation/rotational-port velocity logic survives
- P2 feedback still matches actual docking truth
- P3 transitions/effects remain readable/non-blocking
- reset deterministic
- Back does not reset/corrupt state
- warm resume/relaunch stable

Classify any failure before fixing:
- wrapper/platform defect
- WebView capability mismatch
- packaging/build defect
- pre-existing web defect
- frozen gameplay regression

Never compensate for platform defects by silently tuning frozen gameplay.

## 20. Android 16 / future platform notes
- Google Play API-36 target requirement is already active for new apps/updates at this checkpoint.
- Android 16 uses enforced edge-to-edge behavior.
- Android 16 predictive Back means deprecated `onBackPressed` assumptions are unsafe.
- API-36 large-screen orientation restrictions can be ignored generally; games are an exception at API 36 when categorized as games.
- Future API-37 productization will require more general adaptive behavior, so do not assume landscape lock is a permanent universal solution.

These are platform constraints, not reasons to change core gameplay.

## 21. Cloudflare role
Twin Dock was exposed under the existing Timing Defense Cloudflare Worker `/twindock/` route for mobile browser validation.

This is temporary validation convenience only.

Rules:
- GitHub live branch/docs remain source authority
- APK runtime must use packaged local assets
- do not alter Timing Defense Worker/API behavior
- do not let shared validation routing become permanent product coupling

## 22. Development / validation operating policy
Every slice:
1. recover live state
2. state one product question
3. classify frozen-contract impact
4. check previous-stage consistency from multiple relevant viewpoints
5. define acceptance criteria first
6. implement smallest coherent change
7. run only regressions relevant to changed source/contracts
8. require device validation for tactile/platform/presentation behavior
9. promote only after acceptance
10. synchronize canonical handoff at large-group closure

Multi-view consistency review should consider:
- frozen baseline
- architecture responsibility
- state/lifecycle semantics
- visual/physics agreement
- prior regression history
- platform behavior
- future content extensibility
- cost/benefit of each validation

Avoid:
- whole-repository rescans every session
- full replay of accepted phases without triggers
- over-broad scope
- Codex for tiny work
- CI for cheap one-off smoke checks
- mixing refactor with tuning

## 23. Tool / cost policy
Use the cheapest adequate lane:
- reasoning/design/narrow review: current chat/tools
- deterministic math/contracts: local Node/browser tests
- Codex: only sufficiently large implementation batches
- GitHub Actions: only if repeat automation saves net work
- device: only when behavior is tactile, visual, platform-specific or lifecycle-specific

The project intentionally spends cheap review effort early to catch contract contradictions before expensive build/device work.

## 24. Known regression / scope risks
- dual-touch identity loss
- pointer capture/edge-touch loss
- sensitivity creep
- Android WebView pointer cancellation differences
- camera semantic drift
- visible/internal docking divergence
- feedback threshold vs success divergence
- deterministic background accidentally regenerating
- `+π/-π` fractional-parallax discontinuity recurrence
- `presentation.js` bypass caused by asset/script-order changes
- excessive visual motion
- center-scene obstruction
- generous auto-capture creep
- excessive haptics
- audio masking relative-motion cues
- suspended AudioContext
- Android lifecycle resetting mission/world
- stuck controls after background/resume
- safe-area/system-bar overlap
- fullscreen behavior corrupting resize/state
- predictive Back mishandled with deprecated APIs
- platform fix mixed with gameplay tuning
- current front-port shuttle accidentally frozen as universal geometry
- arbitrary anchor visuals diverging from actual docking math later
- hull collision scope expanding too early
- Idea Bank mistaken for roadmap
- shared Cloudflare route affecting Timing Defense

## 25. Large-group closure discipline
At every large-group closure:
- implementation/decision boundary explicit
- relevant checks passed
- device validation recorded when required
- accepted/frozen decisions recorded
- `PROJECT_STATUS.md` + `SESSION_HANDOFF.md` synchronized
- `START_HERE.md` current milestone/read order checked
- README current phase checked
- relevant design/expansion docs checked for contradiction
- exact next boundary recorded
- known risks/blockers refreshed
- live refs refreshed where useful
- no stale canonical contradiction

A fresh GPT session must be able to recover the entire project structure, why it exists, what is frozen, what has been accepted, current architecture, validation philosophy, content direction, platform contract and exact next execution boundary without relying on conversation memory.
