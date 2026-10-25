# Twin Dock

Twin Dock is a mobile-first inertial spacecraft docking game built around dual independent 2D RCS controls and a ship-frame camera.

## Start here
For any new GPT session, contributor, or delegated implementation agent, begin with:

`docs/START_HERE.md`

Then follow its required read order. Live GitHub is authoritative over past chat, memory, copied SHAs, or handoff text.

## Frozen fallback
The immutable fallback/control contract is **V8**.

Frozen feel:
- ship-frame camera
- two independent full-2D thumb pads
- full free rotation from first play
- inertial translation and rotation
- docking requires simultaneous position, relative velocity, orientation, and angular-velocity match
- deterministic/fixed background
- precision thresholds: distance 11, relative speed 10, direction 0.095 rad, spin 0.10 rad/s

## Accepted milestone stack
- P0 modular/V8 parity — ACCEPTED / CLOSED
- P1 five-stage Mission 01 — ACCEPTED / CLOSED
- P2 world-readable docking feedback — ACCEPTED / CLOSED
- P3-A restrained audio/haptics/contact-capture feedback — ACCEPTED / CLOSED
- P3-B stage transition / final completion polish — ACCEPTED / CLOSED
- Android packaging preflight — PASS / CLOSED

P3 mobile validation confirmed the final-stage distant-background angle-wrap fix, practical-volume audio, acceptable haptics, and no reported control/camera/touch regression.

## Current phase
**Next: minimal Capacitor Android wrapper implementation, then debug APK and physical Android parity validation.**

Canonical Android preflight contract:

`docs/ANDROID_PACKAGING_PREFLIGHT.md`

Fixed first-probe build baseline:
- Capacitor 8.5.3
- app ID `com.hotmoral.twindock`
- version `0.1.0` / versionCode `1`
- minSdk 24
- targetSdk / compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- JDK 17
- Node.js 22+

The wrapper must preserve the existing web game as local/offline assets. The initial implementation should use a deterministic generated `www/` package while keeping the existing root HTML/CSS/`src/` as canonical editable source.

Do not mix Android/platform work with changes to frozen V8 control, docking thresholds, Mission 01 profiles, P2 feedback mapping, P3 presentation behavior, or `src/presentation.js` angle-wrap protection.

Physical-device acceptance must prove dual-touch identity, edge behavior, lifecycle resume, safe-area/system-bar layout, audio, haptics, ship-frame camera continuity, all five Mission 01 dockings and no fifth-dock background regression.

## Content expansion direction
Mission 01's current shuttle/front probe is a **reference craft**, not a permanent universal geometry.

After Android parity is proven and the wrapper contract is frozen, the default return path is:

`Docking Geometry v2 -> reference-shuttle regression -> side/mid-body craft -> rear/asymmetric craft -> simplified hull clearance -> station geometry -> Mission 02 -> Mission 03 -> content/productization gate`.

The intended expansion strategy is to keep the accepted dual-RCS inertial control and docking truth while creating new physical problems through:
- craft silhouette/proportions
- arbitrary local docking-anchor position/orientation
- station/port geometry
- target motion
- approach clearance
- simplified hull collision

Mission 03 is a decision gate, not the planned end of the game. Mission 04+ and progression/productization work should follow only after the geometry-driven content grammar proves sustainable.

Canonical planning files:
- `docs/CONTENT_EXPANSION_MAP.md` — near-term content grammar, gates and promotion order
- `docs/IDEA_BANK.md` — long-horizon stockpile; not a roadmap

Idea states are `BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`. Documentation in the Idea Bank alone does not commit a feature.

## Operating policy
Work in bounded slices. Refactor and tuning are separate changes. Prefer cheap consistency review and relevant deterministic checks before expensive build/device work. Use Codex/CI only when they save net work. Device validation is required for input/camera/game-feel/readability/presentation/platform changes.

Do not revalidate closed P0–P3 work without a relevant source change, prospective dependency, platform/package trigger, or concrete mismatch.

At every large-group closure, synchronize `PROJECT_STATUS.md` and `docs/SESSION_HANDOFF.md`, then verify `docs/START_HERE.md`, this README and any affected design docs remain consistent.
