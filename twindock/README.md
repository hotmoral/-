# Twin Dock

Twin Dock is a mobile-first inertial spacecraft docking game built around dual independent 2D RCS controls and a ship-frame camera.

## Start here
New sessions/contributors begin with `docs/START_HERE.md` and follow its recovery order. Live GitHub is authoritative over past chat, memory, copied SHAs or handoff text.

## Frozen fallback
V8 is the immutable fallback/control contract.

Frozen feel includes:
- ship-frame camera
- two independent full-2D thumb pads
- full free rotation from first play
- inertial translation and rotation
- simultaneous position / relative velocity / orientation / angular-velocity docking truth
- deterministic background
- precision thresholds: distance 11, relative speed 10, direction 0.095 rad, spin 0.10 rad/s

## Accepted / current stack
- P0 modular/V8 parity — ACCEPTED / CLOSED
- P1 five-stage Mission 01 — ACCEPTED / CLOSED
- P2 world-readable docking feedback — ACCEPTED / CLOSED
- P3-A audio/haptics/contact-capture + angle-wrap protection — ACCEPTED / CLOSED
- P3-B stage/final polish — ACCEPTED / CLOSED
- Android packaging preflight — PASS / CLOSED
- Android minimal wrapper/build — **BUILD PASS**
- Android physical-device parity — **PENDING**

## Current exact phase
A reproducible Capacitor debug APK has been built successfully. The next step is **physical Android parity validation**, not Geometry v2 yet.

Successful build reference:
- wrapper head `596ba9e4e89e4926cd10aad08908694572b0bf4b`
- Actions run `40207650795`
- artifact `twindock-android-debug`
- APK `app-debug.apk`
- APK SHA-256 `96e29d19f4c1c211ffcc8805e338549cc7ccd13c8f2255df14868afecb4cfcc2`

Pinned first-parity baseline:
- Capacitor 8.5.3
- app ID `com.hotmoral.twindock`
- version `0.1.0` / versionCode 1
- minSdk 24
- targetSdk / compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- JDK **21**
- Node.js 22+

The earlier JDK 17 preflight assumption was corrected after real Capacitor compilation proved Java 21 is required.

Wrapper implementation changed packaging/build files only; gameplay `src/*` remained untouched.

Canonical Android details: `docs/ANDROID_PACKAGING_PREFLIGHT.md`.

## Android parity policy
The APK uses local/offline assets. Generated `www/` is packaging output, not source authority.

Device validation must cover dual touch/pointer capture, edge touch, pause/resume, landscape/safe-area/system bars, fullscreen, Web Audio, haptics, Back, ship-frame camera, angle-wrap continuity, all five Mission 01 docks and deterministic world identity.

Do not compensate for platform defects by tuning V8 controls or changing docking truth.

The wrapper is not FROZEN until physical-device parity passes.

## Content expansion direction
Mission 01's current shuttle/front probe is a reference craft, not a permanent universal geometry.

After Android parity PASS and wrapper freeze:
`Docking Geometry v2 -> reference-shuttle regression -> side/mid-body craft -> rear/asymmetric craft -> simplified hull clearance -> station geometry -> Mission 02 -> Mission 03 -> content/productization gate`.

The intended expansion keeps the accepted dual-RCS inertial control/docking truth and creates new problems through craft geometry, arbitrary local docking anchors, station geometry, target motion, approach clearance and simplified hull collision.

Mission 03 is a decision gate, not the planned end of the game.

Planning docs:
- `docs/CONTENT_EXPANSION_MAP.md`
- `docs/IDEA_BANK.md` — long-horizon stockpile, not a roadmap

Idea states: `BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`.

## Operating policy
Work in bounded slices. Refactor and tuning are separate. Perform cheap relevant consistency review before expensive work, but do not repeat accepted phases without a trigger. Device validation is required for tactile/visual/platform behavior.

At every large-group closure synchronize `PROJECT_STATUS.md` + `docs/SESSION_HANDOFF.md`, then verify `START_HERE.md`, this README and affected design docs remain consistent.
