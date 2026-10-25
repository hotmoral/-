# Twin Dock Project Status

## Current phase
**Android physical-device parity: PASS / ACCEPTED — wrapper/platform contract FROZEN**

P0–P3 remain **ACCEPTED / CLOSED** and unchanged.
Android packaging preflight is **PASS / CLOSED**.
Android minimal wrapper/build is **BUILD PASS**.
Android physical-device parity is **PASS / ACCEPTED**.
The first Android wrapper/platform contract is now **FROZEN**.

Exact next boundary:
**return to the shared game core and begin Docking Geometry v2.**

The first Geometry v2 product question is:
**Can the hidden fixed-forward-probe assumption be replaced by local player/station docking anchors while the current reference shuttle reproduces Mission 01 with no meaningful feel/readability regression?**

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
- Android physical-device parity: **PASS / ACCEPTED**
- Android wrapper/platform contract: **FROZEN**
- Docking Geometry v2: **NEXT / not yet implemented**

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

Pinned `@capacitor/android` 8.5.3 source uses Java 21, so the canonical toolchain is:
- Capacitor core/CLI/Android: **8.5.3**
- Node.js: **22+**
- JDK: **21**
- minSdk: **24**
- targetSdk: **36**
- compileSdk: **36**
- AGP: **8.13.0**
- Gradle: **8.14.3**

The packaging guard script verifies Capacitor's Java-21 source/target level directly.

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

## Android physical-device acceptance
Physical-device parity was accepted on **2026-10-26 KST** after the user ran the fixed Android parity matrix on a real Android phone and reported that **all checked behavior operated normally with no observed mismatch**.

Accepted device evidence covers:
- install and cold launch
- landscape presentation
- dual-touch pointer identity
- simultaneous two-hand RCS feel
- edge-touch / release / reacquire behavior with no stuck input
- background/resume input clearing and state continuity
- safe-area/system-bar presentation
- fullscreen layout/state behavior
- ship-frame camera semantics
- continuous distant parallax through angle wrap
- no fifth-dock background flip recurrence
- Web Audio after normal interaction
- accepted short haptics
- all five Mission 01 dockings
- target translation + rotational-port-velocity docking behavior
- P2 feedback alignment with actual docking truth
- P3 effects/transitions remaining readable and non-blocking
- deterministic reset/world identity
- Android Back behavior without mission-state corruption
- warm background/foreground stability
- cold relaunch stability

No Android-specific gameplay tuning or platform workaround was required after the successful build. This is significant evidence that the minimal wrapper preserves the accepted web game rather than compensating for platform differences.

Result:
- physical-device parity: **PASS / ACCEPTED**
- wrapper/platform contract: **FROZEN**
- Android parity lane: **CLOSED**

Future wrapper changes require a concrete trigger such as a platform/package upgrade, relevant source change, device mismatch, release requirement or explicit Android productization work. Do not reopen this lane merely because a new session begins.

## Frozen Android wrapper/platform contract
- display name: `Twin Dock`
- app ID: `com.hotmoral.twindock`
- versionName `0.1.0`, versionCode `1` for this accepted parity baseline
- Capacitor 8.5.3
- Node 22+
- JDK 21
- minSdk 24
- targetSdk / compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- local/offline game assets
- generated `www/` is packaging output, not source authority
- `sensorLandscape`
- Android app category `game`
- SystemBars inset handling `native`
- viewport-fit hint `cover`
- no explicit forced `EdgeToEdge.enable` / `WindowCompat.enableEdgeToEdge` in `MainActivity`
- normal Back behavior does not invoke game reset
- warm background/foreground preserves mission/world while clearing active input and silencing RCS audio
- cold process recreation may restart Mission 01; persistence was not part of this milestone
- Web Audio and `navigator.vibrate()` remain the accepted first implementation
- `renderer.js -> presentation.js -> main.js` loading order remains required

FROZEN here means this is the accepted Android parity baseline, not that Android can never evolve. Reopen only for a justified future Android/release slice.

## Frozen guards after Android acceptance
Do not:
- rewrite physics/input/docking/camera natively merely because an Android shell exists
- tune V8/P0 controls without a new explicit gameplay experiment
- redesign Mission 01 while starting Geometry v2
- change P2 feedback truth mapping
- remove/bypass `src/presentation.js`
- redesign P3 transitions/effects without a new product question
- freeze the front-center reference craft as final geometry
- mix future Android productization changes with Docking Geometry v2

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

Current path:
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

### Docking Geometry v2 immediate boundary
Goal: remove the hidden assumption that the player's docking point is always a fixed forward probe.

Target model:
- player docking anchor: local X, local Y, local angle
- station docking anchor: local X, local Y, local angle
- world docking pose derived from local anchors + body transforms
- relative velocity evaluated at the actual docking anchor, including rotational tangential velocity
- orientation matching evaluated from anchor normals/frames
- P2 feedback originates from actual anchors

Non-goal:
- no broad hull/collision rewrite yet
- no new craft family before the reference shuttle passes regression

Geometry v2 exit condition:
**represent the current reference shuttle through the new anchor model and reproduce Mission 01 with no meaningful feel/readability regression.**

Idea states:
`BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`.

Mission 03 is a decision gate, not the end of content.

Near-term hold remains combat, resource economy, crafting, RPG stats, large open world, PvP, complex narrative, fuel economy as primary loop, and large inventory/equipment systems.

## Cloudflare validation exposure
Existing `/twindock/` Cloudflare exposure remains browser-validation convenience only.
The Android APK uses packaged local assets and does not depend on that route.
Do not modify Timing Defense Worker/API behavior for Twin Dock packaging.

## Development / validation policy
- bounded slice, one product question
- cheap multi-view consistency review before expensive work
- compare only contracts actually touched
- deterministic/static tests for math/contracts
- physical device for input/camera/game-feel/readability/platform behavior
- do not replay closed P0–P3 or the closed Android parity lane without a trigger
- Codex only for sufficiently large implementation batches
- CI only where repeatability saves net work
- platform changes separate from gameplay tuning

The Android build workflow trigger remains intentionally limited to runtime/package/test inputs, so documentation-only canonical synchronization does not rebuild the APK.

## Handoff rule
At each large-group closure update this file and `docs/SESSION_HANDOFF.md` together, then verify `START_HERE.md`, README and affected design docs have the same exact next boundary and no stale contradiction.
