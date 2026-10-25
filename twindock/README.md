# Twin Dock

Twin Dock is a mobile-first inertial spacecraft docking game built around dual independent full-2D RCS controls and a ship-frame camera.

## Start here
New sessions/contributors begin with `docs/START_HERE.md` and follow its recovery order. Live GitHub is authoritative over past chat, memory, copied SHAs or handoff text.

## Frozen fallback
V8 is the immutable fallback/control contract.

Frozen feel includes:
- ship-frame camera
- two independent full-2D thumb pads
- full free rotation from first play
- inertial translation and rotation
- simultaneous position / accepted relative velocity / orientation / angular-velocity docking truth
- deterministic background
- precision thresholds: distance 11, relative speed 10, direction 0.095 rad, spin 0.10 rad/s

## Accepted stack
- P0 modular/V8 parity — ACCEPTED / CLOSED
- P1 five-stage Mission 01 — ACCEPTED / CLOSED
- P2 world-readable docking feedback — ACCEPTED / CLOSED
- P3-A audio/haptics/contact-capture + angle-wrap protection — ACCEPTED / CLOSED
- P3-B stage/final polish — ACCEPTED / CLOSED
- Android packaging/device parity — PASS / ACCEPTED; wrapper/platform contract FROZEN
- Geometry v2 reference-anchor foundation — **PASS / ACCEPTED**
- Reference-shuttle deterministic regression — **PASS**

## Current exact phase
The hidden fixed-forward-probe calculation has been replaced by local player/station docking anchors while preserving the accepted reference Mission 01 behavior.

Foundation reference:
- implementation `0f60ab8f05b7c24dadb0a13a83f0951124754817`
- CI / Android run `40240803157` — SUCCESS
- artifact ID `12616678297`

Current Geometry v2 model:
- player anchor: local `x / y / angle`
- station anchor: local `x / y / angle`
- world docking pose derived by body transform
- inverse body pose solve used for successful dock snap/hold
- P2 orientation feedback uses the same anchor frames as docking truth

The current reference shuttle remains `x=40, y=0, angle=0`, so existing Mission 01 docking geometry is preserved.

## Important relative-velocity compatibility rule
Geometry can calculate rigid velocity at both local anchors, but the accepted Mission 01 success metric remains unchanged:
- player side uses ship linear velocity
- target side uses station velocity at the actual capture anchor, including station rotational tangential velocity

Do not silently switch to player-anchor tangential velocity during content work. That is a separate physics/gameplay experiment because it can change the accepted difficulty/feel.

Canonical detail: `docs/GEOMETRY_V2.md`.

## Current next step
**Side/mid-body craft geometry probe.**

Next bounded implementation:
- make visible player docking hardware follow `ship.dockAnchor`
- keep reference shuttle as control
- create one side/mid-body anchor only
- no control retuning
- no hull collision rewrite
- no Mission 02 yet

Then validate on device whether the side port creates distinct but understandable correction strategy while P2 feedback, camera and recovery remain readable.

## Android state
The Android wrapper is already accepted/frozen after physical-device parity PASS on 2026-10-26 KST.

Pinned wrapper:
- Capacitor 8.5.3
- JDK 21
- minSdk 24
- targetSdk / compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- local/offline assets

Shared-core source changes continue to be packaging-tested by CI, but Android platform work must not be reopened without a concrete trigger.

## Content expansion direction
Mission 01's current shuttle/front probe is a reference craft, not a permanent universal geometry.

Current path:
`Geometry v2 reference foundation PASS -> side/mid-body craft -> rear/asymmetric craft -> simplified hull clearance -> station geometry -> Mission 02 -> Mission 03 -> content/productization gate`.

Mission 03 is a decision gate, not the planned end of the game.

Planning docs:
- `docs/CONTENT_EXPANSION_MAP.md`
- `docs/GEOMETRY_V2.md`
- `docs/IDEA_BANK.md` — long-horizon stockpile, not roadmap

Idea states: `BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`.

## Operating policy
Work in bounded slices. Refactor and tuning are separate. Perform cheap relevant consistency review before expensive work, but do not repeat accepted phases without a trigger. Device validation is required for genuinely new tactile/visual/content behavior.

At large-group closure synchronize `PROJECT_STATUS.md` + `docs/SESSION_HANDOFF.md`, then verify `START_HERE.md`, this README and affected design docs remain consistent.
