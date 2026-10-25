# Twin Dock — START HERE

This file is the first entry point for any new GPT session, human contributor, or delegated implementation agent.

## Authority rule
Live GitHub on the current Twin Dock continuation branch is the authority. Past chat, memory, copied SHAs, and handoff text are navigation aids only. If they disagree with live repository state, live repository state wins.

## Required read order
Read these in order before proposing or implementing work:

1. `twindock/docs/START_HERE.md`
2. `twindock/PROJECT_STATUS.md`
3. `twindock/docs/SESSION_HANDOFF.md`
4. `twindock/docs/BASELINE_V8.md`
5. `twindock/docs/FOUNDATION_MANIFEST.md`
6. `twindock/docs/OPERATING_RULES.md`
7. `twindock/README.md`
8. `twindock/docs/CONTENT_EXPANSION_MAP.md`
9. `twindock/docs/ANDROID_PACKAGING_PREFLIGHT.md` for the current Android lane
10. exact source/tests relevant to the next bounded slice

Before proposing new missions, craft families, station geometry, scoring/progression, or other content, also consult:
- `twindock/docs/IDEA_BANK.md`

`IDEA_BANK.md` is deliberately not a roadmap. Promotion rules live in `CONTENT_EXPANSION_MAP.md`.

Do not start broad refactors, gameplay tuning, Docking Geometry v2, Mission 02, or expensive CI before the recovery pass is complete.

## Project identity
Twin Dock is a mobile-first inertial spacecraft docking game whose core experience is embodied two-hand control rather than conventional virtual-stick steering.

The player uses two independent 2D thumb pads. Their combined forces create translation; their difference/lever-arm effect creates rotation. The ship uses inertial motion, full free rotation is available from the beginning, and successful docking requires synchronization of:
- position
- relative linear velocity
- orientation
- angular velocity

The accepted presentation is ship-frame: the player spacecraft remains visually fixed while nearby world geometry moves/rotates relative to it. This camera is part of the game feel, not a cosmetic option.

## Frozen baseline
V8 is the immutable fallback/control baseline unless a later accepted baseline explicitly supersedes it.

Do not silently change V8 feel constants during structural, platform, UI or content work. Any change to input response, thrust, damping, maximum speed, angular behavior, ship-frame semantics, or docking thresholds requires an explicit controlled experiment.

See `BASELINE_V8.md` for exact constants and artifact hash.

## Accepted milestone stack
- P0 modular foundation / V8 parity — ACCEPTED / CLOSED
- P1 continuous five-target Mission 01 — ACCEPTED / CLOSED
- P2 world-readable docking feedback — ACCEPTED / CLOSED
- P3-A audio/haptic/event feedback + angle-wrap protection — ACCEPTED / CLOSED
- P3-B transition/final-completion polish — ACCEPTED / CLOSED
- P3 overall — ACCEPTED / CLOSED
- Android packaging preflight — PASS / CLOSED

## Current exact boundary
The next product question is no longer preflight.

**Can the preflight-fixed Capacitor Android wrapper be implemented and produce a debug APK without changing accepted gameplay truth?**

Current authorized slice:
`minimal Capacitor Android wrapper implementation -> debug APK -> physical Android parity validation`

Do not begin `Docking Geometry v2` until Android parity passes and the wrapper/platform contract is frozen.

## Android packaging contract
Canonical details: `docs/ANDROID_PACKAGING_PREFLIGHT.md`.

Fixed first-probe baseline:
- Capacitor 8.5.3
- display name `Twin Dock`
- application ID `com.hotmoral.twindock`
- versionName `0.1.0`
- versionCode `1`
- minSdk 24
- targetSdk 36
- compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- JDK 17
- Node.js 22+
- Android Studio 2025.2.1+

Packaging direction:
- local/offline assets
- deterministic generated `www/` staging directory
- canonical editable game source remains current root HTML/CSS/`src/`
- generated assets are not a second source authority
- no remote game URL/CDN/live-reload dependency
- preserve script order, especially `renderer.js -> presentation.js -> main.js`

Android display/lifecycle direction:
- phone-first `sensorLandscape`
- app category `game`
- retain portrait fallback
- SystemBars inset handling `native`
- viewport-fit hint `cover`
- system bars visible by default for first probe
- warm background/foreground preserves mission/world, clears input and silences RCS audio
- cold process recreation may restart Mission 01 at this milestone
- Back must not trigger game reset; custom Back interception is deferred unless device evidence requires it

## Android implementation frozen guards
Do not:
- rewrite physics/input/docking/camera natively merely for packaging
- tune V8/P0 controls to hide WebView defects
- redesign Mission 01
- change P2 feedback thresholds independently of docking truth
- remove/bypass `src/presentation.js`
- redesign P3 effects/transitions in the wrapper batch
- freeze the current front-port craft as the universal future geometry
- mix Android fixes with Geometry v2

## Android device acceptance contract
After the debug APK exists, physical-device validation must include:
- install/cold launch
- landscape and safe-area behavior
- dual simultaneous pointer identity
- edge touch / pointer cancel / reacquire
- no stuck thrust
- warm background/foreground state preservation
- fullscreen/system-bar behavior
- ship-frame camera parity
- continuous parallax across physical angle wrap
- no fifth-dock background flip
- Web Audio after real user interaction
- haptics
- all five Mission 01 docks
- target translation and rotational-port velocity docking truth
- P2 feedback truth alignment
- P3 transition/effect readability
- deterministic reset/background
- Android Back not resetting/corrupting state

Any failure must be classified before fixing as wrapper/platform, WebView capability, packaging/build, pre-existing web, or frozen gameplay regression.

## Product direction
Preserve:
- motion-state control, not direct-position control
- recovery from mistakes instead of immediate reset
- full free rotation from first play
- precise earned docking, not generous magnetic capture
- visible/internal docking geometry agreement
- deterministic background identity
- sparse/open UI
- world-readable docking readiness

## Content-expansion direction
The current Mission 01 shuttle/front-center probe is a reference implementation, not a universal final craft layout.

Post-Android path:
`Docking Geometry v2 -> reference-shuttle regression -> side/mid-body craft -> rear/asymmetric craft -> simplified hull clearance -> station geometry -> Mission 02 -> Mission 03 -> productization/content gate`.

Content ideas follow:
`BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`.

Do not promote Idea Bank entries automatically.

## Accepted P3 notes that must survive Android packaging
- RCS/mechanical audio and short event haptics are accepted.
- AudioContext must be armed from real user gestures.
- `src/presentation.js` protects distant parallax from `+π/-π` physical angle-wrap discontinuity.
- P3-B uses short non-blocking stage/final transitions.
- no touch/control/physics/camera feel regression was reported after final P3 device validation.

## Development pipeline
For each bounded slice:
1. recover live state
2. state one product question
3. identify frozen contracts touched
4. inspect prior-stage consistency from relevant viewpoints
5. define acceptance before implementation
6. implement smallest coherent batch
7. run only relevant deterministic/static regressions
8. require device validation for tactile/visual/platform behavior
9. promote only after acceptance
10. synchronize canonical handoff at large-group closure

## Tool / cost rule
Use the cheapest adequate lane:
- reasoning/design/narrow implementation/review: current chat/tools
- deterministic math/regression: local Node/browser tests
- Codex: only for implementation batches large enough to justify delegation
- GitHub Actions: only when repeatable automation reduces total work
- Android/device validation: only where platform/tactile evidence is actually required

Avoid repeated repository scans, accepted-phase revalidation, broad builds, and AI delegation without a concrete trigger.

## Group-closure rule
At every large-group closure, synchronize `PROJECT_STATUS.md` and `SESSION_HANDOFF.md`, then verify this file, README and any affected design docs do not contradict the new state.

A fresh session must be able to recover project identity, design rationale, frozen/accepted decisions, architecture, validation philosophy, content direction, platform contract, known risks and the exact next execution boundary without conversation memory.
