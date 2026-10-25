# Twin Dock — START HERE

This file is the first entry point for any new GPT session, human contributor or delegated implementation agent.

## Authority rule
Live GitHub on the current Twin Dock continuation branch is the authority. Past chat, memory, copied SHAs and handoff text are navigation aids only. If they disagree with live repository state, live repository state wins.

## Required read order
1. `twindock/docs/START_HERE.md`
2. `twindock/PROJECT_STATUS.md`
3. `twindock/docs/SESSION_HANDOFF.md`
4. `twindock/docs/BASELINE_V8.md`
5. `twindock/docs/FOUNDATION_MANIFEST.md`
6. `twindock/docs/OPERATING_RULES.md`
7. `twindock/README.md`
8. `twindock/docs/CONTENT_EXPANSION_MAP.md`
9. `twindock/docs/GEOMETRY_V2.md` for current geometry work
10. `twindock/docs/ANDROID_PACKAGING_PREFLIGHT.md` only when Android history/contract is relevant
11. exact source/tests relevant to the next bounded slice

Before proposing/promoting new content, also consult `twindock/docs/IDEA_BANK.md`.

Already ACCEPTED/CLOSED/FROZEN work must not be revalidated merely because a new session started. Revalidate only for a relevant source change, prospective dependency, platform/package trigger, release requirement or concrete mismatch.

## Project identity / frozen core
Twin Dock is a mobile-first inertial precision-docking game centered on embodied two-hand control.

Frozen direction:
- two independent full-2D RCS pads
- common force -> translation
- differential/lever-arm force -> rotation
- inertial translation and rotation
- full free rotation from first play
- stationary start / body-frame control
- ship-frame camera
- recovery/re-approach after mistakes
- docking requires position + accepted relative linear velocity + orientation + relative angular velocity
- station capture velocity includes target translation and rotating-port tangential velocity
- deterministic background identity
- precise earned docking rather than generous magnetic capture

V8 remains the immutable fallback/control baseline. See `BASELINE_V8.md` for exact values/hash.

## Accepted stack
- P0 modular foundation / V8 parity — ACCEPTED / CLOSED
- P1 five-target Mission 01 — ACCEPTED / CLOSED
- P2 world-readable docking feedback — ACCEPTED / CLOSED
- P3-A audio/haptics/event feedback + angle-wrap protection — ACCEPTED / CLOSED
- P3-B transition/final polish — ACCEPTED / CLOSED
- P3 overall — ACCEPTED / CLOSED
- Android packaging/device parity — PASS / ACCEPTED; wrapper contract FROZEN
- Geometry v2 reference-anchor foundation — **PASS / ACCEPTED**
- Reference-shuttle deterministic regression — **PASS**

## Current exact boundary
Do not reopen Android packaging or start hull collision/Mission 02 yet.

The next product question is:
**Does a side/mid-body player docking anchor create distinct but understandable play while preserving the accepted controls, ship-frame camera, docking thresholds and recovery loop?**

Exact next slice:
`anchor-driven player-port visual -> one side/mid-body craft probe -> focused regression -> physical-device readability/gameplay check`

The current reference shuttle remains the control/fallback.

## Geometry v2 accepted foundation
Canonical detail: `docs/GEOMETRY_V2.md`.

Foundation implementation:
- ref `0f60ab8f05b7c24dadb0a13a83f0951124754817`
- CI run `40240803157` — SUCCESS
- new `src/geometry.js`
- player and station anchors represented as local `x / y / angle`
- docking position/orientation derives from world anchor frames
- dock snap/hold uses inverse anchor pose solving
- P2 orientation feedback reads anchor frames
- Mission 01 reference geometry remains numerically equivalent

Validation:
- 256 deterministic states compared against exact legacy formulas
- arbitrary non-front/asymmetric anchor transform closes correctly
- accepted web regressions PASS
- Android staging/build contract PASS
- debug APK build PASS

### Important velocity decision
Do **not** silently change docking relative velocity to use player-anchor rigid/tangential velocity.

Current accepted truth remains:
- ship linear velocity on player side
- actual station capture-anchor velocity on target side, including station rotational tangential velocity

`Geometry.shipDockAnchor()` exposes rigid anchor velocity for future analysis, but that value is not yet promoted into docking success.

Any change here is a separate gameplay/physics experiment because it can change Mission 01 difficulty.

## Geometry v2 next-slice guards
For the side/mid-body probe:
- renderer/player docking fixture must visually follow `ship.dockAnchor`
- preserve exact reference craft as control
- one new anchor prototype only
- no broad craft schema
- no new handling constants
- no hull-clearance collision yet
- no station catalogue
- no Mission 02 yet
- no large explanatory HUD
- P2 cues and visible/physical anchor must agree

Require device evidence before promoting the non-front craft.

## P3 regression guard
`src/presentation.js` is required. It provides a continuous renderer-facing visual angle across physical `+π/-π` wrap and prevents the accepted fifth-dock distant-background regression without changing physical state.

Required loading chain remains:
`renderer.js -> presentation.js -> main.js`.

## Android state
Android wrapper/platform contract is already FROZEN after physical-device parity PASS on 2026-10-26 KST.

Pinned accepted wrapper:
- Capacitor 8.5.3
- Node 22+
- JDK 21
- minSdk 24
- targetSdk/compileSdk 36
- AGP 8.13.0
- Gradle 8.14.3
- app ID `com.hotmoral.twindock`
- local/offline assets

Shared-core content changes may continue to produce APK CI artifacts, but do not reinterpret that as reopening Android platform parity.

## Content direction
Current path:
`Geometry v2 reference foundation PASS`
→ `side/mid-body craft`
→ `rear/asymmetric craft`
→ `simplified hull clearance`
→ `station geometry`
→ `Mission 02`
→ `Mission 03`
→ `content/productization gate`

Ideas follow `BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`.
`IDEA_BANK.md` is not a roadmap.

## Development pipeline
For each bounded slice:
1. recover live state
2. state one product question
3. identify touched frozen contracts
4. perform cheap multi-view consistency review
5. define acceptance first
6. implement smallest coherent change
7. run only relevant deterministic/static checks
8. require device evidence for genuinely new tactile/visual behavior
9. promote only after acceptance
10. synchronize canonical handoff at large-group closure

## Cost discipline
Prefer cheap review before expensive build/device work. Avoid repeated scans, accepted-phase replay, redundant CI and premature schema generalization.

For multi-file source changes, batch blobs/tree/commit and move the branch ref once; do not create avoidable intermediate commits that each trigger Android CI.

## Group-closure rule
At every large-group closure synchronize `PROJECT_STATUS.md` and `SESSION_HANDOFF.md`, then verify this file, README and affected design docs agree on current truth, known risks and exact next boundary.
