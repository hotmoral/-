# Twin Dock Project Status

## Current phase
**Android packaging preflight: PASS / CLOSED**

P0–P3 remain **ACCEPTED / CLOSED** and unchanged.

Exact next boundary: **minimal Capacitor Android wrapper implementation -> debug APK -> physical Android parity validation.**

Post-Android parity return boundary: **Docking Geometry v2** in the shared game core.

Current continuation branch: `twindock-p3b-transition-v1`.
Live remote remains authoritative; copied SHAs are reference points only.

Canonical Android preflight contract:
- `docs/ANDROID_PACKAGING_PREFLIGHT.md`
- preflight closure commit reference: `f482770af7e08cbdb6dcecda0f1d21aae9ed3897`

## Accepted milestone stack
- P0 modular foundation / V8 parity: **ACCEPTED / CLOSED**
- P1 Mission 01 five-stage continuous loop: **ACCEPTED / CLOSED**
- P2 world-readable docking feedback: **ACCEPTED / CLOSED**
- P3-A event/audio/haptic foundation: **ACCEPTED / CLOSED**
- P3-B stage-transition / final-completion polish: **ACCEPTED / CLOSED**
- P3 overall: **ACCEPTED / CLOSED**
- Android packaging preflight: **PASS / CLOSED**
- V8 remains the immutable fallback/control contract.

Frozen input, thrust, speed, camera semantics, collision/docking truth and precision thresholds remain unchanged through the Android preflight.

## Android preflight closure

### Product question
Can the accepted web implementation be packaged on Android with materially equivalent dual-touch feel, rendering/readability, audio/haptics, camera continuity and Mission 01 behavior without a native gameplay rewrite?

Preflight answer: **yes; no source-level blocker or contract contradiction was found.**

This does not constitute device parity. The next slice must implement the wrapper, create a debug APK and validate it on a physical Android device.

### Chosen wrapper/build baseline
- thin Capacitor/WebView-style wrapper
- Capacitor core/CLI/Android: **8.5.3 stable**
- Capacitor 9: not used while pre-release/alpha
- app display name: **Twin Dock**
- application ID: **com.hotmoral.twindock**
- versionName: **0.1.0**
- versionCode: **1**
- minSdk: **24**
- targetSdk: **36**
- compileSdk: **36**
- AGP: **8.13.0**
- Gradle wrapper: **8.14.3**
- JDK: **17**
- Node.js: **22+**
- Android Studio: **2025.2.1+**

The values above follow the stable Capacitor 8.5.3 Android template and current API-36 Google Play targeting requirement. Do not opportunistically upgrade this toolchain during the first parity slice without a concrete incompatibility.

### Packaging contract
- game remains static/local/offline inside the wrapper
- create a deterministic generated web directory such as `www/`
- current root HTML/CSS/`src/` remains canonical editable game source
- generated web assets are packaging output, not a second source authority
- preserve relative runtime paths
- preserve script order, especially `renderer.js -> presentation.js -> main.js`
- no CDN, remote game source, live-reload URL, analytics or API dependency in the parity APK
- stock Capacitor `INTERNET` permission may remain for the first probe, but Twin Dock itself must make no runtime network dependency

### Android display/lifecycle contract
- phone-first activity requests `sensorLandscape`
- app category should be `game`
- retain existing portrait blocker as safety fallback
- use Capacitor 8 SystemBars inset handling `native`
- initial viewport-fit hint `cover`
- keep system bars visible by default in the first probe; validate current Fullscreen API behavior before adding a platform-specific fullscreen fix
- warm background/foreground preserves mission/world state, clears old touches, silences RCS audio, avoids large physics time steps and does not regenerate the world
- cold process recreation may restart Mission 01; persistence is not part of this milestone
- normal Android Back may return to home in the first parity build but must not call game reset or corrupt state
- do not add deprecated `onBackPressed`-based design; target SDK 36 predictive-back behavior must remain valid

### Highest-risk device checks
1. simultaneous left/right pointer identity and capture
2. edge touch and `pointercancel` behavior
3. release/reacquire after background/foreground
4. safe-area/system-bar layout on API 36 edge-to-edge behavior
5. Web Audio resume after real user gesture
6. `navigator.vibrate()` behavior in WebView
7. Fullscreen API/system-bar behavior
8. presentation-angle continuity and fifth-dock background regression

### Frozen guards for Android implementation
Do not:
- rewrite physics/input/docking/camera natively merely for packaging
- tune V8/P0 controls to compensate for a WebView defect
- redesign Mission 01
- change P2 feedback truth mapping
- remove or bypass `src/presentation.js`
- redesign P3 transitions/effects in the wrapper batch
- freeze the current front-center craft geometry as the final content model
- mix platform fixes with Geometry v2 or other gameplay work

## Exact next bounded slice — minimal Android wrapper implementation

The implementation slice is authorized to:
1. add Capacitor 8.5.3 dependencies/config
2. add deterministic web-asset staging to `www/`
3. add the Android project from the stable Capacitor template
4. apply the fixed app ID/version/SDK/orientation/inset contract
5. make only platform-required source changes
6. run existing relevant JS regressions plus packaging/build checks
7. produce a debug APK
8. stop for physical-device parity validation

Do not begin Docking Geometry v2 until Android parity is demonstrated and the wrapper/platform contract is frozen.

## Android APK acceptance contract
The criteria are fixed before implementation:
- install and cold launch stable
- landscape layout correct
- dual-touch pointer identity preserved
- two-hand feel materially equivalent to accepted web play
- no edge touch loss or stuck input
- background/resume clears old input and accepts new input
- no warm-resume mission/world reset
- safe area/system bars do not cover controls or critical HUD
- fullscreen behavior does not corrupt layout/state
- ship-frame camera unchanged
- distant parallax continuity unchanged
- fifth-dock background flip does not recur
- Web Audio audible after normal interaction
- accepted short haptics function, or a concrete WebView limitation is identified
- all five Mission 01 dockings complete normally
- target translation + rotational port velocity still participate in docking-relative velocity
- P2 feedback remains aligned with docking truth
- P3 transition/effect layers remain non-blocking
- reset remains deterministic
- Android Back does not reset/corrupt mission state
- warm background/foreground and relaunch behavior stable

Failures must be classified as wrapper/platform defect, WebView capability mismatch, packaging/build defect, pre-existing web defect, or frozen gameplay regression before a fix is chosen.

## Content expansion planning — canonical direction
Long-horizon content planning remains governed by:
- `docs/CONTENT_EXPANSION_MAP.md` — near-term content grammar, promotion gates and macro sequence
- `docs/IDEA_BANK.md` — broad stockpile of future possibilities; not a roadmap

The current Mission 01 shuttle silhouette and front-center probe are **reference content**, not frozen universal geometry.

Idea promotion states:
- `BANKED`
- `CANDIDATE`
- `VALIDATED`
- `ROADMAP`

Post-Android parity macro direction remains:
`minimal Android parity`
→ `freeze wrapper contract`
→ `Docking Geometry v2`
→ `reference-shuttle regression`
→ `three-craft geometry probe`
→ `simplified hull clearance`
→ `station geometry probe`
→ `Mission 02`
→ `Mission 03`
→ `content-expansion/productization gate`
→ `Mission 04+ / justified meta and productization`

Mission 03 is a decision gate, not the planned end of the game.

Near-term hold list remains:
- combat/weapons
- resource harvesting/economy
- crafting
- RPG stat trees
- large open world
- PvP
- complex narrative systems
- fuel economy as a primary loop
- large inventory/equipment systems

## P0 closure
- deterministic smoke test: PASS
- 12,000-frame V8-vs-modular parity: zero divergence
- mobile feel parity: ACCEPTED
- canonical foundation commit: `185a974dbd818386019677409f875640df27442f`

## P1 accepted loop
Mission 01 sequence:
1. `STATIC`
2. `TRANSLATE`
3. `ROTATE`
4. `COMBINED`
5. `FINAL`

Accepted behavior:
- continuous five-target mission remained fun on device
- ship state continues between dockings
- target translation + rotational port velocity participate in relative-speed docking calculations
- deterministic background persists across the run
- recoverable collision/re-approach remains intact
- frozen V8 control feel remained unchanged

P1 accepted closure before P2: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`.
Exact run duration was not separately instrumented; do not invent a measured 3–5 minute duration.

## P2 accepted result
Accepted answer: the player can judge docking readiness primarily from the world/docking hardware rather than a permanent numeric checklist.

Normal-play feedback:
- position: capture brackets
- orientation: ship/port notches
- angular velocity: relative-spin trail
- relative linear velocity: drift arrow
- success: restrained green ring

Old diagnostics remain under `?debug=1`.
Feedback uses the same docking truth/thresholds as actual success.

## P3-A accepted result
Accepted implementation includes:
- restrained continuous RCS hiss
- bad-contact cue + short haptic
- soft-capture cue + short haptic
- latch / next-target / mission-complete cues
- AudioContext arming from `pointerdown`, `touchstart`, `click`
- `?audio=0`, `?haptics=0`
- `src/presentation.js` continuous renderer-facing visual-angle adapter

Important issue history:
- initial low device volume made audio seem silent; activation and gains were hardened conservatively and device recheck passed
- fifth-dock distant-background flip came from fractional parallax using wrapped physical angle; presentation-layer unwrap fixed it without changing physical/camera truth

P3-A accepted closure reference: `62fa4d75301071256dabdb20fdb4c0eb6f97d3d4`.

## P3-B accepted result
Accepted presentation:
- `src/transitions.js`
- `transitions.css`
- short Mission HUD dock pulse
- ~0.98 s target sweep + target/stage label
- ~1.9 s low-opacity final edge frame + completion cue
- subtle completed HUD state until reset
- transition layers `pointer-events:none`
- reduced-motion support
- no large central result modal

P3-B device result: PASS / ACCEPTED. No reported touch/input, camera, motion-comfort, P3-A audio/haptic or background-continuity regression.

## Deterministic background / presentation continuity
Current star generation is seeded and guarded by `starFieldReady`; resize calls do not regenerate a new field.

`src/presentation.js` wraps the renderer and substitutes only a continuous renderer-facing ship angle. Physical `ship.angle` remains wrapped and authoritative for gameplay.

Android packaging must preserve this script/order contract.

## Cloudflare validation exposure
Twin Dock static assets have been exposed under the existing Timing Defense Cloudflare Worker at `/twindock/` for device validation only.

Rules remain:
- this is validation convenience, not source authority
- do not change Timing Defense Worker/API behavior
- Android APK must not depend on this route at runtime
- prefer a dedicated deployment later if long-lived product hosting is needed

## Development / validation policy
- work in bounded slices
- one slice answers one product question
- compare every change only against the contracts it actually touches
- use deterministic/static checks for math/contracts
- require device validation for input/camera/game-feel/readability/presentation/platform behavior
- do not re-run closed P0–P3 validation without a relevant source change, prospective dependency or concrete mismatch
- use Codex only when a substantial implementation batch justifies it
- use public CI only when repeatable automation reduces net cost
- platform fixes and gameplay tuning remain separate

## Handoff rule
At every large-group closure:
- update this file and `docs/SESSION_HANDOFF.md` together
- verify `docs/START_HERE.md` and README reflect the exact current boundary
- update `CONTENT_EXPANSION_MAP.md` only when content direction/promotion changes
- keep `IDEA_BANK.md` banked unless explicit promotion occurs
- preserve accepted decisions, reasons, known risks, live refs and exact next execution boundary
