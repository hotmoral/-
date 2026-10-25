# Twin Dock — Android Packaging / Parity Contract

Status: **PREFLIGHT PASS / WRAPPER BUILD PASS / PHYSICAL DEVICE PARITY PENDING**

Purpose: define and preserve the smallest Android packaging contract that carries the accepted P3 web game into an Android APK without changing gameplay truth.

Authority rule: live GitHub on the current continuation branch remains authoritative. This document records the Android packaging decision and build evidence; it does not supersede `BASELINE_V8.md`, accepted P0–P3 contracts, or later physical-device evidence.

## 1. Product question

Can the accepted Twin Dock web implementation be packaged on Android with materially equivalent dual-touch feel, ship-frame rendering, Mission 01 behavior, audio/haptics and presentation continuity without a native gameplay rewrite?

Current answer:
- **preflight: yes**
- **wrapper/build: yes**
- **physical-device parity: not yet proven**

No source-level contradiction was found that requires changing physics, input mapping, docking truth, camera semantics, Mission 01, P2 feedback, P3 effects, or P3 transitions for packaging.

## 2. Frozen guards

Android packaging must not silently change:
- V8 control constants or response curve
- dual independent full-2D RCS semantics
- inertial translation/rotation
- full free rotation from first play
- ship-frame camera semantics
- four-condition docking truth or thresholds
- Mission 01 target profiles/state continuity
- P2 world-readable feedback mapping
- P3 audio/haptic event intent
- P3-B transition/final-completion presentation intent
- deterministic background behavior
- `src/presentation.js` continuous visual-angle protection around physical `+π/-π` wrap

Platform fixes and gameplay tuning remain separate changes.

## 3. Wrapper strategy

Use a **thin Capacitor 8 Android wrapper** around the current static HTML/CSS/JS implementation.

Pinned first-parity baseline:
- Capacitor core/CLI/Android: **8.5.3**
- Node.js: **22+**
- Android Studio: **2025.2.1+**
- JDK: **21**

Capacitor 9 is not used while it remains a pre-release line at this checkpoint.

Do not introduce React, Ionic UI, a JS framework migration, a native physics layer, or a native rendering rewrite merely for packaging.

### JDK correction history
The initial preflight incorrectly recorded JDK 17 after considering the Android Gradle Plugin minimum only.

The first real Capacitor compilation exposed the mismatch with:
`invalid source release: 21`.

Direct inspection of the pinned `@capacitor/android` 8.5.3 Gradle source confirmed `JavaVersion.VERSION_21` for source and target compatibility. The contract is therefore **JDK 21**, and the packaging guard script now verifies that requirement directly.

This is a canonical correction, not a gameplay change.

## 4. Android build contract

Initial parity package contract:
- display name: **Twin Dock**
- application ID: **com.hotmoral.twindock**
- versionName: **0.1.0**
- versionCode: **1**
- minSdk: **24**
- targetSdk: **36**
- compileSdk: **36**
- Android Gradle Plugin: **8.13.0**
- Gradle wrapper: **8.14.3**
- JDK: **21**

Rationale:
- current Google Play targeting requires API 36 for the relevant new-app/update lane at this checkpoint
- Capacitor 8.x is the stable line aligned with API 36
- the Capacitor 8.5.3 Android template uses minSdk 24, compileSdk 36, targetSdk 36, AGP 8.13.0 and Gradle 8.14.3
- pinned Capacitor Android source compiles at Java 21

Do not opportunistically upgrade Capacitor/AGP/Gradle/JDK during the parity probe without a concrete incompatibility and a bounded review.

## 5. Web asset packaging contract

Twin Dock remains a local/offline web game inside the wrapper.

Capacitor uses a generated `www/` staging directory.

Rules:
- canonical editable game source remains `twindock/index.html`, root CSS and `src/`
- `www/` is deterministic packaging output, not a second source authority
- copy only runtime-required files
- preserve relative asset/script paths
- preserve script order, especially `renderer.js -> presentation.js -> main.js`
- do not package docs/tests/repository metadata as runtime assets
- no CDN or remote runtime dependency

The staging script fails if the entrypoint contains remote HTTP(S) runtime references and checks the presentation script order.

APK inspection after the successful build confirmed:
- local `assets/public/index.html`
- local root CSS files
- local `assets/public/src/*`
- no docs/tests/canonical project files in runtime assets
- `renderer.js -> presentation.js -> main.js` order preserved

## 6. Network policy

Twin Dock gameplay has **zero network runtime dependency** in the parity APK.

The stock Capacitor Android template declares `android.permission.INTERNET`. Keep that stock permission for the first parity probe rather than modifying the native template before device validation, but do not add remote URLs, live-reload server URLs, analytics, CDN assets or API calls.

After parity is proven, INTERNET permission removal may be evaluated as a separate least-privilege cleanup if it can be demonstrated not to disturb the wrapper/local-server path.

Cloudflare `/twindock/` exposure is not used as the APK runtime source.

## 7. Input / pointer contract

Current web assumptions to preserve:
- each pad owns a separate `pointerId`
- `setPointerCapture()` is attempted on pointer down
- pointer move/up/cancel are observed at window scope
- scrolling/gesture interference is suppressed with `touch-action:none` / preventDefault
- background visibility clears both control states

Highest-risk physical-device area:
- simultaneous two-finger identity
- pointer capture at/near screen edges
- `pointercancel` behavior
- release/reacquire after app background/foreground
- no stuck thrust after interruption

Do not tune deadzone, exponent, force or torque to compensate for a WebView input defect.

## 8. Orientation / display contract

Phone-first parity policy:
- native activity requests **sensorLandscape** so either landscape direction is usable
- Android application category is **game**
- retain the existing web portrait blocker as a fallback
- keep web resize/orientation handling because native orientation policy is not a replacement for responsive layout

Do not treat this first phone policy as a permanent large-screen product contract.

## 9. Safe area / edge-to-edge / system bars

Current Twin Dock uses `viewport-fit=cover` and CSS `env(safe-area-inset-*)` around HUD/controls.

Capacitor config:
- SystemBars inset handling: **native**
- initial viewport-fit hint: **cover**
- system bars visible by default for the first parity build

Important guard:
- do **not** explicitly call `EdgeToEdge.enable(...)` or `WindowCompat.enableEdgeToEdge(...)` in the first wrapper
- Android 15+/16 platform edge-to-edge behavior should be handled by the platform/Capacitor path
- avoid forcing the same edge-to-edge path onto older supported Android versions before device evidence

The patch script rejects explicit forced-edge-to-edge calls in `MainActivity`.

The existing HTML Fullscreen API remains unchanged until physical-device evidence shows a concrete issue. If it fails, fix fullscreen/system-bar behavior as a bounded Android-only slice rather than mixing it with gameplay changes.

## 10. Lifecycle contract

### Warm background / foreground
Must:
- preserve mission index, score, ship state, station state and deterministic world identity
- clear active input so no thrust remains latched
- silence continuous RCS audio while hidden
- avoid a large physics time-step on return
- resume without random world/background regeneration

The current web implementation already clears input on visibility change, silences RCS audio on visibility/page hide, and clamps simulation `dt`; preserve this first and validate in WebView before adding native lifecycle code.

### Cold relaunch / process death
A true cold launch or Android process recreation may restart Mission 01 from its normal initial state for this milestone. Persistent mission save/restore is not part of parity validation.

## 11. Android Back contract

Do not add a custom back-navigation framework for the first parity build.

Contract:
- normal Android Back may return to home
- Back must not call Twin Dock reset logic
- returning to a still-alive activity from Recents should preserve current mission/world state
- predictive-back behavior on targetSdk 36 must not crash or corrupt WebView state

If accidental exits materially harm play, implement pause-first Back handling later as a separate Android-only slice using current predictive-back-compatible APIs.

## 12. Audio / haptic contract

Audio:
- preserve current Web Audio implementation
- preserve real-user-gesture arming/resume (`pointerdown`, `touchstart`, `click`)
- no native audio rewrite in the first APK
- backgrounding must silence continuous RCS audio

Haptics:
- preserve `navigator.vibrate()` first
- verify real WebView/device behavior
- only introduce a native/Capacitor haptic adapter after a concrete mismatch
- any adapter must preserve accepted short event timing/meaning

## 13. Deterministic world / presentation guards

Current renderer star creation is seeded and guarded by `starFieldReady`; resize does not regenerate a new field.

`src/presentation.js` wraps the renderer with a continuous renderer-facing ship angle while leaving physical `ship.angle` wrapped.

Android packaging must preserve:
- deterministic star-field identity across resize/fullscreen/background resume
- `presentation.js` loading and wrapper order
- no physics mutation as a substitute for visual-angle continuity
- no fifth-dock/background flip regression

## 14. Implemented wrapper/build lane

Implemented on the continuation branch without modifying gameplay `src/*`:
- pinned Capacitor 8.5.3 dependencies/config
- deterministic `www/` staging script
- generated Android shell in CI from the pinned stable template
- template contract verification/patch script
- application ID/version/orientation/category guards
- explicit Java-21 guard
- relevant web regression run before Android build
- debug APK build + artifact upload workflow

The Android project is generated during CI rather than being maintained as a second large checked-in source tree at this stage. This keeps the wrapper reproducible and minimizes native drift while the contract is still under parity validation.

## 15. Build-validation history

Build failures were classified before fixes:

1. **Run 1 — CI infrastructure failure**
   - obsolete Android SDK `tools` request inside a setup action
   - app/Capacitor code had not run
   - fix: use runner `sdkmanager` directly

2. **Run 2 — CI working-directory error**
   - generated Gradle project existed, but Gradle was invoked from `twindock/` instead of `twindock/android/`
   - fix: run wrapper from Android project root

3. **Run 3 — real toolchain-contract mismatch**
   - `:capacitor-android:compileDebugJavaWithJavac`
   - `invalid source release: 21`
   - root cause: preflight recorded JDK 17 from AGP minimum while pinned Capacitor 8.5.3 compiles at Java 21
   - fix: JDK 21 + direct Java-21 contract assertion

4. **Run 4 — PASS**
   - workflow run: `40207650795`
   - wrapper implementation head: `596ba9e4e89e4926cd10aad08908694572b0bf4b`
   - web regressions: PASS
   - staging: PASS
   - Capacitor shell generation: PASS
   - native contract verification before/after sync: PASS
   - Gradle `assembleDebug`: PASS
   - artifact upload: PASS

No gameplay source change was needed to obtain the successful APK.

## 16. Successful debug artifact

GitHub Actions artifact:
- name: `twindock-android-debug`
- artifact ID: `12604396208`
- run: `40207650795`
- artifact ZIP SHA-256: `10436d55b5057092a830fada531e084f9ddb0e9dd086725002e1987d442ac670`
- APK filename: `app-debug.apk`
- APK bytes: `4141919`
- APK SHA-256: `96e29d19f4c1c211ffcc8805e338549cc7ccd13c8f2255df14868afecb4cfcc2`

The workflow artifact is temporary and must not be treated as long-term source authority. Source + reproducible build contract remain canonical.

## 17. Build-scope consistency review

Compared with the canonical state immediately after preflight documentation, wrapper implementation changed only:
- `.github/workflows/twindock-android-parity.yml`
- `twindock/capacitor.config.json`
- `twindock/package.json`
- `twindock/scripts/patch-android.mjs`
- `twindock/scripts/stage-android-web.mjs`

No `twindock/src/*`, gameplay CSS/HTML, physics, input, docking, camera, renderer, mission, feedback, effects, presentation or transition source was modified by wrapper implementation.

The workflow trigger was narrowed to runtime/package/test inputs so canonical documentation-only commits do not waste APK builds.

## 18. Physical-device acceptance contract

The exact next boundary is physical Android parity validation.

Check on a real Android phone:
- install and cold launch succeed
- landscape presentation is correct in both landscape directions where supported
- dual-touch pointer identity is stable
- simultaneous left/right RCS feel is materially equivalent to accepted web play
- no edge-touch loss or stuck input
- pause/background/resume clears old touches and accepts new touches
- no mission/world reset on normal warm resume
- safe-area/system-bar layout does not cover controls or critical HUD
- HTML/native fullscreen behavior does not corrupt layout/state
- ship-frame camera semantics remain correct
- distant parallax stays continuous through `+π/-π`
- fifth-dock background flip does not recur
- Web Audio becomes audible after normal interaction
- accepted short haptics work, or a concrete WebView limitation is identified
- all five Mission 01 dockings complete normally
- target translation and rotational-port-velocity docking behavior remains intact
- P2 feedback remains aligned with actual docking truth
- P3 transitions/effects remain non-blocking and readable
- reset remains deterministic
- Back does not reset/corrupt mission state
- warm background/foreground is stable
- cold relaunch is stable

Any failure must be classified before fixing as:
- wrapper/platform defect
- WebView capability mismatch
- packaging/build defect
- pre-existing web defect
- frozen gameplay regression

Do not compensate for a platform defect by tuning frozen gameplay.

## 19. Exit / next state

Android packaging preflight: **PASS / CLOSED**.
Android minimal wrapper build: **BUILD PASS**.
Physical Android parity: **PENDING**.
Android wrapper contract: **not yet FROZEN** until device acceptance passes.

Exact next boundary:
**install `app-debug.apk` on a physical Android phone -> run the fixed parity acceptance matrix -> classify/fix only concrete platform mismatches -> freeze wrapper on PASS.**

After Android parity PASS and wrapper freeze, return to the shared game core for `Docking Geometry v2`.
