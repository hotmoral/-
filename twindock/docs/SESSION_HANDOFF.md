# Twin Dock — Session Handoff

This is the canonical fresh-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Authority / repository / continuation
- repository: `hotmoral/-`
- continuation branch: `twindock-p3b-transition-v1`
- live remote is authoritative
- past chats, memory, copied SHAs and this handoff are navigation aids only when they agree with live GitHub

Historical accepted refs:
- P0 closure: `185a974dbd818386019677409f875640df27442f`
- P1 closure before P2: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`
- P3-A closure: `62fa4d75301071256dabdb20fdb4c0eb6f97d3d4`
- Android successful wrapper implementation/build head: `596ba9e4e89e4926cd10aad08908694572b0bf4b`

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
9. `twindock/docs/ANDROID_PACKAGING_PREFLIGHT.md` for Android work
10. `twindock/docs/IDEA_BANK.md` when content ideation/promotion is relevant
11. exact source/tests relevant to the next bounded slice

Do not broadly refactor, retune controls, begin Geometry v2, delegate, or rerun expensive validation before recovery establishes the exact live boundary.

Closed/frozen work is not re-tested simply because a session restarted. Revalidation requires a relevant source change, prospective dependency, platform/package trigger, or concrete mismatch.

## 3. Exact current state
- P0: ACCEPTED / CLOSED
- P1: ACCEPTED / CLOSED
- P2: ACCEPTED / CLOSED
- P3-A: ACCEPTED / CLOSED
- P3-B: ACCEPTED / CLOSED
- P3 overall: ACCEPTED / CLOSED
- Android packaging preflight: PASS / CLOSED
- Android minimal wrapper/build: **BUILD PASS**
- debug APK: **generated**
- Android physical-device parity: **PENDING**
- Android wrapper/platform contract: **not yet FROZEN**
- Docking Geometry v2: **not started**

Exact next boundary:
**install the debug APK on a physical Android phone -> execute the fixed parity matrix -> classify/fix only concrete Android mismatches -> freeze wrapper on PASS.**

After PASS:
**return to shared game core -> Docking Geometry v2.**

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

Prefer recovery to immediate FAIL/RESET.

Rejected unless reopened as explicit experiment:
- one-hand primary control
- car/boat heading steering
- forward/back-only twin thrusters
- tutorial removal/stage-gating of free rotation
- generous magnetic capture replacing precision

## 5. Why the current control model exists
The current structure emerged from tactile device prototypes:
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
V8 is the immutable fallback/control baseline until explicitly superseded.

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

Structural/platform work must not silently alter these. Tuning is a separate controlled experiment requiring device evidence.

## 7. Camera / motion comfort
Accepted camera: **ship-frame**.

The player craft remains visually mostly fixed while nearby world/station geometry moves and rotates relative to it. This is a core feel contract.

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
Successful docking requires all four simultaneously:
1. docking-point position
2. relative linear velocity
3. orientation
4. relative angular velocity

Relative velocity includes:
- target translation
- target rotation-induced tangential velocity at the port

Visible/internal geometry must agree.
P2 readiness feedback and actual success thresholds must agree.
Avoid generous magnetic capture.

## 9. Architecture boundaries
### Input
pointer identity, dual-touch tracking, response curve, body-frame commands.

### Physics
position, velocity, angle, angular velocity, inertia, collision response.

### Docking
geometry, relative metrics, four-condition truth, capture/recoverable collision criteria.

### Camera
world -> ship-frame presentation; no physical mutation.

### Renderer
world visuals and visible docking hardware.

### Feedback
world-readable P2 readiness cues only; no physics mutation.

### Mission
stage/target sequence and persistent ship state between docks.

### Effects
presentation audio/haptics only.

### Presentation adapter
visual continuity/readability only; wrapped physical values may be adapted for display, never source-state mutation.

### Transitions
stage/final presentation only.

### Future geometry
craft/station docking anchors and collision geometry become data-driven only after bounded prototypes expose real requirements.

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

Question: does the validated control remain compelling across a continuous multi-target mission?
Accepted answer: yes.

Sequence:
1. STATIC
2. TRANSLATE
3. ROTATE
4. COMBINED
5. FINAL

Accepted behavior:
- deterministic five-target profiles
- ship state persists between docks
- target translation included in relative velocity
- rotational port tangential velocity included in relative velocity
- deterministic background persists
- recoverable collision/re-approach
- frozen V8 feel unchanged

Exact mission duration was not separately instrumented; do not invent one.
Mission 01 is a reference/basic mission, not total intended content.

## 12. P2 — world-readable feedback
Status: ACCEPTED / CLOSED.

Normal UI removed the permanent numeric/checklist diagnostics; QA diagnostics remain under `?debug=1`.

Accepted scene feedback:
- position -> capture brackets
- orientation -> ship/port notches
- angular velocity -> relative-spin trail
- relative linear velocity -> drift arrow
- success -> restrained green confirmation ring

Feedback uses the same docking checks/thresholds as actual success.

## 13. P3-A — event/audio/haptic foundation
Status: ACCEPTED / CLOSED.

Accepted:
- restrained continuous RCS hiss
- bad-contact cue + short haptic
- soft-capture cue + short haptic
- latch cue
- delayed next-target cue
- mission-complete cue
- `?audio=0`, `?haptics=0`
- AudioContext arm/resume from `pointerdown`, `touchstart`, `click`
- RCS silence on pause/reset/background
- `src/presentation.js` angle-wrap protection

Issue history:
- initial low media volume made audio seem silent; activation/gain hardened conservatively and recheck passed
- fifth-dock distant-background flip came from fractional parallax using wrapped angle; fixed presentation-only and device recheck passed

No accepted control/physics/camera regression was reported.

## 14. P3-B — transition/final polish
Status: ACCEPTED / CLOSED.

Accepted:
- `src/transitions.js` + `transitions.css`
- short dock HUD pulse
- ~0.98 s next-target sweep + compact cue
- ~1.9 s low-opacity final frame + completion cue
- subtle completed HUD state until reset
- transition layers `pointer-events:none`
- reduced-motion support
- no large central modal

Device result PASS. P3 overall CLOSED.

## 15. Content direction
Canonical:
- `docs/CONTENT_EXPANSION_MAP.md`
- `docs/IDEA_BANK.md`

The current front-center shuttle/probe is reference content, not a universal final geometry.

Primary future axes:
- craft silhouette/proportions
- player docking-anchor local position/orientation
- station geometry/anchor
- target translation/rotation
- initial relative pose/motion
- approach corridor/clearance
- simplified hull collision
- mission composition
- later scoring/mastery if physical content grammar proves sustainable

Idea lifecycle:
`BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`.

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
→ `Mission 04+ / justified meta`

Mission 03 is a decision gate, not an end point.

Hold near-term: combat, economy/harvesting, crafting, RPG stats, large open world, PvP, complex narrative, fuel economy as primary loop, large inventory/equipment systems.

## 16. Android packaging preflight
Status: PASS / CLOSED.
Canonical detail: `docs/ANDROID_PACKAGING_PREFLIGHT.md`.

Chosen wrapper:
- thin Capacitor 8 wrapper
- local/offline web assets
- no native gameplay rewrite

Current canonical toolchain:
- Capacitor 8.5.3
- Node 22+
- JDK **21**
- minSdk 24
- targetSdk 36
- compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- app ID `com.hotmoral.twindock`
- versionName 0.1.0 / versionCode 1

Important correction:
The initial preflight used JDK 17 by looking at AGP minimum requirements. Actual pinned Capacitor compilation failed with `invalid source release: 21`; Capacitor 8.5.3 source was then directly checked and confirmed Java 21. The build/guard contract was corrected to JDK 21.

## 17. Android wrapper implementation — BUILD PASS
Implementation intentionally remained outside gameplay source.

Added/changed only:
- `.github/workflows/twindock-android-parity.yml`
- `twindock/capacitor.config.json`
- `twindock/package.json`
- `twindock/scripts/stage-android-web.mjs`
- `twindock/scripts/patch-android.mjs`

No `twindock/src/*` change.

### Staging/build architecture
- root HTML/CSS/`src/` remain canonical editable source
- deterministic script creates `www/`
- staging rejects remote entrypoint assets
- staging verifies `renderer -> presentation -> main`
- CI generates the native Android project from pinned Capacitor 8.5.3
- patch script asserts SDK/AGP/Gradle/app ID/version/orientation/category/Java-21 contract
- patch script rejects explicit forced edge-to-edge calls in MainActivity
- `cap sync` then re-verifies contract
- Gradle builds debug APK

The native project is not yet maintained as a second large checked-in source tree; reproducible generation minimizes drift during parity validation.

### Build history / classification discipline
Run 1: setup action requested obsolete Android SDK `tools`; infrastructure failure before app work. Replaced with direct runner sdkmanager.

Run 2: Gradle invoked from wrong working directory; CI path defect. Corrected to `android/` project root.

Run 3: first real toolchain mismatch: Capacitor Android Java source level 21 vs JDK 17. Corrected canonical/tooling to JDK 21 and added a direct guard.

Run 4: **PASS**.
- run ID `40207650795`
- head `596ba9e4e89e4926cd10aad08908694572b0bf4b`
- web regressions PASS
- staging PASS
- Capacitor project generation PASS
- contract checks PASS before/after sync
- Gradle assembleDebug PASS
- artifact upload PASS

### Artifact
- artifact name `twindock-android-debug`
- ID `12604396208`
- ZIP SHA-256 `10436d55b5057092a830fada531e084f9ddb0e9dd086725002e1987d442ac670`
- APK `app-debug.apk`
- bytes `4141919`
- APK SHA-256 `96e29d19f4c1c211ffcc8805e338549cc7ccd13c8f2255df14868afecb4cfcc2`

APK archive inspection confirmed local game runtime assets, no project docs/tests, and preserved presentation script order.

The GitHub artifact is temporary. Reproducible source/build contract is canonical.

## 18. Android platform contract under test
- phone-first `sensorLandscape`
- app category `game`
- existing web portrait blocker retained
- SystemBars inset handling `native`
- viewport-fit hint `cover`
- system bars visible by default for first probe
- no explicit `EdgeToEdge.enable` / `WindowCompat.enableEdgeToEdge` in first wrapper
- existing HTML Fullscreen API unchanged until device evidence
- warm background/foreground preserves mission/world, clears touches, silences RCS audio
- cold process recreation may restart Mission 01
- normal Back initially; must not reset/corrupt game state
- Web Audio + `navigator.vibrate()` preserved first
- native adapters only after concrete mismatch

## 19. Exact next slice — physical Android parity
The wrapper is **not frozen yet**.

Install `app-debug.apk` on a real Android phone and verify:
- install/cold launch
- landscape/safe-area/system bars
- simultaneous pointer identity
- edge touch / pointer cancel / reacquire
- accepted dual-RCS feel
- no stuck thrust
- pause/background/resume state preservation
- fullscreen behavior
- ship-frame camera
- continuous angle-wrap parallax and no fifth-dock flip
- Web Audio
- haptics
- all five Mission 01 docks
- target translation + rotational port velocity truth
- P2 feedback vs actual docking truth
- P3 transition/effect readability
- deterministic reset/world identity
- Android Back
- warm resume / cold relaunch stability

Classify each failure before fixing:
- wrapper/platform defect
- WebView capability mismatch
- packaging/build defect
- pre-existing web defect
- frozen gameplay regression

Do not tune frozen gameplay to hide platform defects.

On PASS:
- freeze Android wrapper/platform contract
- synchronize canonical docs
- return to shared game core
- begin Docking Geometry v2

## 20. Cloudflare role
Twin Dock browser validation was exposed under the existing Timing Defense Worker `/twindock/` route.

This is temporary validation convenience only.
- source authority remains GitHub
- APK uses packaged local assets
- do not modify Timing Defense Worker/API behavior for Android packaging
- do not let shared exposure become permanent coupling

## 21. Operating / consistency discipline
Every slice:
1. recover live state
2. state one product question
3. identify frozen contracts touched
4. review consistency from relevant views: baseline, architecture, lifecycle/state, visual/physics agreement, regression history, platform, future extensibility, validation cost
5. define acceptance before implementation
6. implement smallest coherent change
7. run only relevant deterministic/static regressions
8. require device evidence for tactile/visual/platform behavior
9. promote only after acceptance
10. synchronize canonical handoff at large-group closure

Avoid whole-repository rescans, full replay of accepted phases, over-broad scope, small-task Codex use, and CI that does not save net work.

The Android workflow trigger is narrowed to runtime/package/test files, so documentation-only commits do not rebuild the APK.

## 22. Known regression / scope risks
- dual-touch identity loss
- pointer capture / edge-touch loss
- WebView pointer cancellation differences
- sensitivity creep from attempting to compensate for platform behavior
- camera semantic drift
- visible/internal docking divergence
- feedback threshold divergence
- deterministic background regeneration
- `+π/-π` fractional-parallax discontinuity recurrence
- `presentation.js` bypass/script-order change
- visual motion clutter / center obstruction
- generous auto-capture creep
- excessive haptics / audio masking
- suspended AudioContext
- Android lifecycle mission/world reset
- stuck input after background/resume
- safe-area/system-bar overlap
- forced edge-to-edge mismatch on older supported Android
- fullscreen resize/state corruption
- predictive Back misuse
- platform fix mixed with gameplay tuning
- current reference craft accidentally frozen as universal geometry
- later arbitrary-anchor visuals diverging from docking math
- premature hull-collision scope growth
- Idea Bank mistaken for roadmap
- shared Cloudflare route affecting Timing Defense

## 23. Large-group closure discipline
At closure:
- record exact implementation/decision boundary
- record relevant tests/device evidence
- distinguish BUILD PASS from DEVICE ACCEPTED
- synchronize `PROJECT_STATUS.md` + this handoff
- verify `START_HERE.md`, README and affected design docs
- record exact next boundary and current risks
- refresh live refs where useful
- ensure no stale canonical contradiction

A fresh session must be able to recover the entire project structure, rationale, frozen contracts, accepted history, architecture, validation philosophy, content direction, Android build contract, known risks and exact next step without conversation memory.
