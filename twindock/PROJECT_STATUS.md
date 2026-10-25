# Twin Dock Project Status

## Current phase
**Android minimal wrapper: BUILD PASS / PHYSICAL DEVICE PARITY PENDING**

P0–P3 remain **ACCEPTED / CLOSED** and unchanged.
Android packaging preflight is **PASS / CLOSED**.

Exact next boundary:
**install the generated debug APK on a physical Android phone and execute the fixed parity acceptance matrix.**

On device PASS:
**freeze Android wrapper/platform contract -> return to shared game core -> Docking Geometry v2.**

Current continuation branch: `twindock-p3b-transition-v1`.
Live remote remains authoritative; copied SHAs are reference points only.

## Current accepted / pending stack
- P0 modular foundation / V8 parity: **ACCEPTED / CLOSED**
- P1 Mission 01 five-stage continuous loop: **ACCEPTED / CLOSED**
- P2 world-readable docking feedback: **ACCEPTED / CLOSED**
- P3-A event/audio/haptic foundation: **ACCEPTED / CLOSED**
- P3-B stage-transition / final-completion polish: **ACCEPTED / CLOSED**
- P3 overall: **ACCEPTED / CLOSED**
- Android packaging preflight: **PASS / CLOSED**
- Android minimal wrapper/build: **BUILD PASS**
- Android physical-device parity: **PENDING**
- Android wrapper/platform contract: **not yet FROZEN**
- Docking Geometry v2: **not started**

V8 remains the immutable fallback/control contract.
Frozen input, thrust, speed, camera semantics, docking truth and precision thresholds remain unchanged.

## Android wrapper/build result

Canonical contract:
`docs/ANDROID_PACKAGING_PREFLIGHT.md`

Successful implementation/build reference:
- implementation head: `596ba9e4e89e4926cd10aad08908694572b0bf4b`
- GitHub Actions run: `40207650795`
- result: **SUCCESS**

Debug artifact:
- `twindock-android-debug`
- artifact ID `12604396208`
- `app-debug.apk`
- APK SHA-256 `96e29d19f4c1c211ffcc8805e338549cc7ccd13c8f2255df14868afecb4cfcc2`
- APK size `4141919` bytes

Build lane passed:
- Node 22
- JDK 21
- Android API 36 SDK
- pinned Capacitor 8.5.3 install
- accepted web regression tests
- deterministic local web staging
- generated Capacitor Android shell
- native/template contract checks before and after sync
- Gradle `assembleDebug`
- artifact upload

### Toolchain correction discovered by implementation
Initial preflight recorded JDK 17 from the AGP minimum requirement. Actual Capacitor compilation failed with `invalid source release: 21`.

Pinned `@capacitor/android` 8.5.3 source uses Java 21, so the canonical toolchain is now:
- Capacitor core/CLI/Android: **8.5.3**
- Node.js: **22+**
- JDK: **21**
- minSdk: **24**
- targetSdk: **36**
- compileSdk: **36**
- AGP: **8.13.0**
- Gradle: **8.14.3**

The packaging guard script now verifies Capacitor's Java-21 source/target level directly.

### Wrapper scope
Implementation changed only packaging/build files:
- `.github/workflows/twindock-android-parity.yml`
- `twindock/capacitor.config.json`
- `twindock/package.json`
- `twindock/scripts/patch-android.mjs`
- `twindock/scripts/stage-android-web.mjs`

No gameplay `src/*` file changed.
No control tuning, physics/docking/camera change, Mission 01 change, P2/P3 redesign or Geometry v2 work occurred.

APK inspection confirmed runtime packaging contains local game assets only and preserves the `renderer.js -> presentation.js -> main.js` loading chain. Docs/tests are not packaged as runtime assets.

## Android fixed platform contract for device probe
- display name: `Twin Dock`
- app ID: `com.hotmoral.twindock`
- versionName `0.1.0`, versionCode `1`
- local/offline game assets
- generated `www/` is packaging output, not source authority
- `sensorLandscape`
- Android app category `game`
- SystemBars inset handling `native`
- viewport-fit hint `cover`
- system bars visible by default during first probe
- no explicit forced `EdgeToEdge.enable` / `WindowCompat.enableEdgeToEdge` in `MainActivity`
- normal Back behavior initially; Back must not invoke game reset
- warm background/foreground should preserve mission/world while clearing active input and silencing RCS audio
- cold process recreation may restart Mission 01; persistence is not part of this milestone
- Web Audio and `navigator.vibrate()` preserved first; native adapters only after concrete mismatch

## Exact physical-device acceptance matrix
- install and cold launch stable
- landscape presentation correct
- dual-touch pointer identity preserved
- two-hand RCS feel materially equivalent to accepted web play
- no edge-touch loss or stuck input
- pause/background/resume clears old input and accepts new input
- no warm-resume mission/world reset
- safe area/system bars do not cover controls or critical HUD
- fullscreen behavior does not corrupt layout/state
- ship-frame camera unchanged
- distant parallax continuous through angle wrap
- fifth-dock background flip absent
- Web Audio audible after normal interaction
- short accepted haptics work, or concrete WebView limitation identified
- all five Mission 01 dockings complete normally
- target translation + rotational port velocity remain in docking-relative velocity
- P2 feedback remains aligned with docking truth
- P3 effects/transitions remain non-blocking/readable
- reset remains deterministic
- Back does not reset/corrupt mission state
- warm background/foreground and relaunch stable

Failures must be classified before fixing as wrapper/platform defect, WebView capability mismatch, packaging/build defect, pre-existing web defect, or frozen gameplay regression.

## Frozen guards for Android validation/fixes
Do not:
- rewrite physics/input/docking/camera natively merely for packaging
- tune V8/P0 controls to compensate for WebView behavior
- redesign Mission 01
- change P2 feedback truth mapping
- remove/bypass `src/presentation.js`
- redesign P3 transitions/effects
- freeze the front-center reference craft as final geometry
- mix platform fixes with Docking Geometry v2

## P0–P3 accepted reference

### P0
- deterministic smoke: PASS
- 12,000-frame V8-vs-modular parity: zero divergence
- mobile feel parity: ACCEPTED
- closure reference: `185a974dbd818386019677409f875640df27442f`

### P1 — Mission 01
Sequence:
1. STATIC
2. TRANSLATE
3. ROTATE
4. COMBINED
5. FINAL

Accepted behavior:
- continuous five-target mission
- persistent ship state between docks
- target translation and rotational port velocity included in relative velocity
- deterministic background
- recoverable collision/re-approach
- frozen V8 feel unchanged

Closure-before-P2 reference: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`.
Exact run duration was not separately instrumented.

### P2
Normal play uses world-readable docking feedback:
- position: capture brackets
- orientation: ship/port notches
- angular velocity: relative-spin trail
- relative linear velocity: drift arrow
- success: restrained green ring

Debug diagnostics remain under `?debug=1`.
Feedback uses the same truth/thresholds as actual docking success.

### P3-A
Accepted:
- restrained RCS hiss
- contact/capture/latch/next-target/mission-complete cues
- short haptics
- AudioContext user-gesture arming
- `?audio=0`, `?haptics=0`
- `src/presentation.js` continuous visual-angle adapter

Important fixed regression: fifth-dock distant-background flip from fractional parallax across physical `+π/-π` wrap.
P3-A closure reference: `62fa4d75301071256dabdb20fdb4c0eb6f97d3d4`.

### P3-B
Accepted:
- brief Mission HUD dock pulse
- ~0.98 s next-target sweep
- compact target/stage cue
- ~1.9 s final edge frame/completion cue
- completed HUD state until reset
- `pointer-events:none`
- reduced-motion support
- no central blocking modal

P3 overall CLOSED after device validation.

## Content expansion direction
Canonical planning:
- `docs/CONTENT_EXPANSION_MAP.md`
- `docs/IDEA_BANK.md`

The current Mission 01 front-port shuttle is reference content, not frozen universal geometry.

Post-Android parity path:
`Docking Geometry v2`
→ `reference-shuttle regression`
→ `side/mid-body craft`
→ `rear/asymmetric craft`
→ `simplified hull clearance`
→ `station geometry`
→ `Mission 02`
→ `Mission 03`
→ `content/productization gate`
→ `Mission 04+ / justified meta/productization`

Idea states:
`BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`.

Mission 03 is a decision gate, not the end of content.

Near-term hold remains combat, resource economy, crafting, RPG stats, large open world, PvP, complex narrative, fuel economy as primary loop, and large inventory/equipment systems.

## Cloudflare validation exposure
Existing `/twindock/` Cloudflare exposure remains browser-validation convenience only.
The Android APK uses packaged local assets and must not depend on that route.
Do not modify Timing Defense Worker/API behavior for Twin Dock packaging.

## Development / validation policy
- bounded slice, one product question
- cheap multi-view consistency review before expensive work
- compare only contracts actually touched
- deterministic/static tests for math/contracts
- physical device for input/camera/game-feel/readability/platform behavior
- do not replay closed P0–P3 without a trigger
- Codex only for sufficiently large implementation batches
- CI only where repeatability saves net work
- platform fixes separate from gameplay tuning

The Android build workflow trigger is intentionally limited to runtime/package/test inputs, so documentation-only canonical synchronization does not rebuild the APK.

## Handoff rule
At each large-group closure update this file and `docs/SESSION_HANDOFF.md` together, then verify `START_HERE.md`, README and affected design docs have the same exact next boundary and no stale contradiction.
