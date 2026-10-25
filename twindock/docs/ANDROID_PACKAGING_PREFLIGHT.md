# Twin Dock — Android Packaging Preflight

Status: **PASS / CLOSED**

Purpose: define the smallest Android packaging contract that preserves the accepted P3 web game before any APK implementation begins.

Authority rule: live GitHub on the current continuation branch remains authoritative. This document records the preflight decision; it does not supersede `BASELINE_V8.md`, accepted P0–P3 contracts, or later device evidence.

## 1. Product question

Can the accepted Twin Dock web implementation be packaged on Android with materially equivalent dual-touch feel, ship-frame rendering, Mission 01 behavior, audio/haptics and presentation continuity without a native gameplay rewrite?

Preflight answer: **yes, implementation is viable with a thin Capacitor/WebView shell.**

No source-level contradiction was found that requires changing physics, input mapping, docking truth, camera semantics, Mission 01, P2 feedback, P3 effects, or P3 transitions before packaging.

This is a preflight conclusion only. Android tactile/platform parity still requires a real APK and physical-device validation.

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

## 3. Chosen wrapper strategy

Use a **thin Capacitor 8 Android wrapper** around the current static HTML/CSS/JS implementation.

Chosen stable baseline at preflight closure:
- Capacitor core/CLI/Android: **8.5.3**
- Capacitor 9 is not used because it is still pre-release/alpha at this checkpoint.
- Android Studio: **2025.2.1 or newer**
- Node.js: **22+**
- JDK: **17**

Do not introduce React, Ionic UI, a JS framework migration, a native physics layer, or a native rendering rewrite merely for packaging.

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
- JDK: **17**

Rationale:
- Google Play requires Android 16 / API 36 targeting for new apps and updates from 2026-08-31.
- Capacitor 8.x is the stable Capacitor line tied to target SDK 36.
- The Capacitor 8.5.3 Android template uses minSdk 24, compileSdk 36, targetSdk 36, AGP 8.13.0 and Gradle 8.14.3.
- AGP 8.13 requires JDK 17 and supports API 36.x.

Do not opportunistically upgrade AGP/Gradle/Capacitor during the first parity implementation unless the generated stable template or build environment produces a concrete incompatibility.

## 5. Web asset packaging contract

Twin Dock remains a local/offline web game inside the wrapper.

Capacitor requires a separate built-web directory. The implementation slice should therefore create a deterministic generated web package such as `www/` from the current canonical root assets rather than point Capacitor at the repository root.

Rules:
- canonical editable game source remains the existing `twindock/index.html`, CSS and `src/` files
- generated `www/` is packaging output, not a second source authority
- copy only runtime-required files
- preserve relative asset/script paths
- preserve script order, especially `renderer.js -> presentation.js -> main.js`
- do not package docs/tests/repository metadata as runtime assets
- no CDN or remote runtime dependency may be introduced

Current entrypoint uses relative local CSS/JS paths and has a valid `<head>`, which fits Capacitor's web asset model.

## 6. Network policy

Twin Dock gameplay must have **zero network runtime dependency** in the parity APK.

The stock Capacitor Android template declares `android.permission.INTERNET`. For the first parity implementation, keep the stock permission rather than modify the native template before device validation, but do not add remote URLs, live-reload server URLs, analytics, CDN assets or API calls.

After parity is proven, removal of the INTERNET permission may be evaluated as a separate least-privilege cleanup if it can be demonstrated not to disturb the wrapper/local-server path.

Cloudflare `/twindock/` exposure is not used as the APK runtime source.

## 7. Input / pointer contract

Current web input assumptions to preserve unchanged initially:
- each pad owns a separate `pointerId`
- `setPointerCapture()` is attempted on pointer down
- pointer move/up/cancel are observed at window scope
- touch scrolling/gesture interference is suppressed with `touch-action:none` / preventDefault
- background visibility clears both control states

Highest-risk Android acceptance area:
- simultaneous two-finger identity
- pointer capture at/near screen edges
- pointercancel behavior
- release/reacquire after app background/foreground
- no stuck thrust after interruption

Do not tune deadzone, exponent, force or torque to compensate for a WebView input defect.

## 8. Orientation / display contract

Phone-first parity policy:
- native activity requests **sensorLandscape** so either landscape direction is usable
- set Android app category to **game**
- retain the existing web portrait blocker as a safety fallback rather than deleting it

Android 16 can ignore orientation restrictions on large screens in general, although games are an exception at API 36. The web layout must therefore remain resilient to resize/configuration changes even while the first device acceptance target is a phone in landscape.

Do not treat native orientation locking as a reason to remove web resize/orientation handling.

## 9. Safe area / system bars / fullscreen policy

Android 16 enforces edge-to-edge behavior. Current Twin Dock already uses `viewport-fit=cover` and CSS `env(safe-area-inset-*)` around HUD/controls.

For Capacitor 8:
- configure SystemBars inset handling explicitly as **native**
- set initial viewport-fit hint to **cover**
- keep system bars **visible by default** for the first parity build
- do not preemptively redesign the existing `전체` button or P3 layout

Reason: this is the lowest-risk first probe. The existing Fullscreen API behavior is a device acceptance item. If Android WebView fullscreen does not provide an acceptable result, fix system-bar/fullscreen behavior in a bounded platform-only follow-up rather than mixing it with gameplay changes.

Safe-area acceptance is mandatory: no RCS pad, center controls, HUD or transition cue may be obscured by cutouts, gesture/navigation areas or system bars.

## 10. Lifecycle contract

### Background / foreground
Warm background/foreground must:
- preserve mission index, score, ship state, station state and deterministic world identity
- clear active input so no thrust remains latched
- silence continuous RCS audio while hidden
- avoid a large physics time-step on return
- resume without random world/background regeneration

The current web implementation already clears input on `visibilitychange`, silences RCS audio on visibility/page hide, and clamps simulation `dt`; preserve this behavior first and validate it in WebView before adding native lifecycle code.

### Cold relaunch
A true cold launch/process recreation may start Mission 01 from its normal initial state. Persistent mission save/restore is not part of the parity probe.

### Process death while backgrounded
If Android kills the process, returning to a fresh Mission 01 state is acceptable for this milestone. Persistence belongs to later productization unless promoted separately.

## 11. Android Back contract

For the first parity build, do not add a custom back-navigation framework.

Contract:
- Android Back may use normal system back-to-home behavior
- Back must **not** invoke Twin Dock reset logic
- returning to the still-alive activity from Recents should preserve current mission/world state
- predictive-back behavior on targetSdk 36 must not cause a crash or corrupted WebView state

If physical-device testing shows that accidental Back exits materially harm play, implement pause-first Back handling as a separate Android-only slice using current predictive-back-compatible APIs. Do not use deprecated `onBackPressed` assumptions as the design basis.

## 12. Audio / haptic contract

Audio:
- preserve the current Web Audio implementation first
- preserve real-user-gesture arming/resume (`pointerdown`, `touchstart`, `click`)
- no native audio rewrite in the first APK
- backgrounding must silence continuous RCS audio

Haptics:
- preserve `navigator.vibrate()` first
- verify actual WebView/device behavior
- only if it fails or is materially inconsistent may a Capacitor/native haptic adapter be introduced
- any adapter must preserve the accepted short event timing/meaning rather than retune gameplay feedback

## 13. Deterministic world / presentation guards

Current renderer star creation is seeded and guarded by `starFieldReady`, so resize calls do not regenerate a new random field.

Current P3-A presentation continuity is implemented by wrapping the renderer with `src/presentation.js`, exposing a continuous renderer-facing ship angle while leaving physical `ship.angle` wrapped.

Android packaging must preserve:
- deterministic star field identity across resize/fullscreen/background resume
- `presentation.js` script loading and wrapper order
- no direct replacement of the visual-angle adapter with a physics mutation
- no fifth-dock/background flip regression

## 14. Implementation slice authorized by this preflight

The next bounded slice is **minimal Android wrapper implementation**, not gameplay work.

Smallest coherent implementation should:
1. add Capacitor 8.5.3 dependencies/config
2. add deterministic web-asset staging into `www/`
3. generate/add the Android platform using the stable Capacitor template
4. apply the build/app/orientation/inset contract above
5. make only platform-required source changes
6. run existing JS regression tests plus build/static checks relevant to packaging
7. produce a debug APK
8. stop before gameplay tuning or Geometry v2

Codex delegation is not required merely to scaffold this bounded wrapper unless local implementation constraints make it net-cheaper.

## 15. APK acceptance contract — fixed before implementation

Physical-device acceptance must check:
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
- accepted short haptics work or a concrete WebView limitation is identified
- all five Mission 01 dockings complete normally
- target translation and rotational-port-velocity docking behavior remains intact
- P2 feedback remains aligned with actual docking truth
- P3 transitions/effects remain non-blocking and readable
- reset remains deterministic
- Back does not reset/corrupt mission state
- warm background/foreground is stable
- cold relaunch is stable

Any failure must be classified before fixing it as one of:
- wrapper/platform defect
- WebView capability mismatch
- packaging/build defect
- pre-existing web defect
- frozen gameplay regression

Do not compensate for a platform defect by tuning frozen gameplay.

## 16. Preflight consistency review

Reviewed against accepted P0–P3 architecture and future content direction.

No blocking contradiction found.

Important non-blocking tensions recorded:
1. Android 16 edge-to-edge/safe-area behavior differs from ordinary browser fullscreen; validate rather than assume equivalence.
2. Android 16 predictive Back means deprecated Back interception patterns must not be introduced casually.
3. Landscape restriction is reliable for the phone-first probe, but future large-screen/API 37 productization must remain adaptive.
4. `navigator.vibrate()` is not guaranteed across every web engine/device; native haptics remain a fallback, not a preemptive rewrite.
5. Capacitor requires a separate web asset directory; generated packaging assets must not become a competing source authority.
6. Stock Capacitor INTERNET permission is retained for the first probe even though Twin Dock itself must remain offline; least-privilege cleanup is intentionally deferred until parity is proven.

## 17. Exit state

Android packaging preflight: **PASS / CLOSED**.

Exact next boundary:
**minimal Capacitor Android wrapper implementation -> debug APK -> physical Android parity validation.**

After Android parity PASS and wrapper contract freeze, return to the shared game core for `Docking Geometry v2`.
