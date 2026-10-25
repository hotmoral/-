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
9. exact source/tests relevant to the next bounded slice

Read `twindock/docs/ANDROID_PACKAGING_PREFLIGHT.md` when Android history/contract is relevant.
Before proposing/promoting new content, also consult `twindock/docs/IDEA_BANK.md`.

Already ACCEPTED/CLOSED/FROZEN work must not be revalidated from scratch merely because a new session started. Revalidate only for a relevant source change, prospective dependency, platform/package trigger, release requirement, or concrete mismatch.

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
- docking requires position + relative linear velocity + orientation + relative angular velocity
- relative velocity includes target translation and rotating-port tangential velocity
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
- Android packaging preflight — PASS / CLOSED
- Android minimal wrapper/build — BUILD PASS
- Android physical-device parity — **PASS / ACCEPTED**
- Android wrapper/platform contract — **FROZEN**
- Android parity lane — **CLOSED**
- Docking Geometry v2 — **NEXT / not yet implemented**

## Current exact boundary
Do **not** reopen Android parity or start broad hull/collision work without a concrete trigger.

The next product question is:
**Can the hidden fixed-forward-probe assumption be replaced by local player/station docking anchors while the current reference shuttle reproduces Mission 01 with no meaningful feel/readability regression?**

Exact next slice:
`Docking Geometry v2 -> represent current reference shuttle through local anchor frames -> bounded reference-shuttle regression`

## Android accepted baseline
Canonical contract/history: `docs/ANDROID_PACKAGING_PREFLIGHT.md`.

Successful wrapper implementation/build:
- implementation head: `596ba9e4e89e4926cd10aad08908694572b0bf4b`
- workflow run: `40207650795`
- Capacitor: 8.5.3
- Node: 22+
- JDK: 21
- minSdk: 24
- targetSdk/compileSdk: 36
- AGP: 8.13.0
- Gradle: 8.14.3
- app ID: `com.hotmoral.twindock`
- version: `0.1.0` / versionCode 1

Debug APK reference:
- filename `app-debug.apk`
- SHA-256 `96e29d19f4c1c211ffcc8805e338549cc7ccd13c8f2255df14868afecb4cfcc2`

Wrapper implementation did **not** change gameplay `src/*`.

Physical-device parity was accepted on **2026-10-26 KST** after the user ran the fixed Android matrix on a real phone and reported all checked behavior normal. No Android-specific gameplay tuning or platform workaround was required after the successful build.

The accepted Android wrapper/platform contract is now FROZEN. Reopen only for a relevant source/platform/package change, device mismatch, release requirement, or explicit Android productization slice.

## Android wrapper guards
- thin Capacitor wrapper
- local/offline assets
- generated `www/` is output, not source authority
- preserve `renderer.js -> presentation.js -> main.js`
- phone-first `sensorLandscape`
- app category `game`
- SystemBars native inset handling + viewport-fit cover
- no explicit forced `EdgeToEdge.enable` / `WindowCompat.enableEdgeToEdge`
- keep current Web Audio / `navigator.vibrate()` baseline unless concrete evidence requires change
- no native physics/input/docking/camera rewrite

## P3 regression guard
`src/presentation.js` is required. It provides a continuous renderer-facing visual angle across physical `+π/-π` wrap and prevents the accepted fifth-dock distant-background regression without changing physical state.

Do not bypass it during Geometry v2 or move the fix into physics casually.

## Docking Geometry v2 — immediate scope
Goal: remove the assumption that the player docking point is always a fixed forward probe.

Target model:
- player docking anchor: local X, local Y, local angle
- station docking anchor: local X, local Y, local angle
- derive world docking pose from local anchors + body transforms
- evaluate relative velocity at the actual docking anchor, including rotational tangential velocity
- evaluate orientation from anchor normals/frames rather than body-center direction alone
- originate P2 feedback from actual anchor frames

Non-goals:
- no broad hull/collision rewrite yet
- no control tuning
- no Android-specific implementation fork
- no new side/rear craft until the reference shuttle passes regression

Exit condition:
**the current reference shuttle represented through Geometry v2 reproduces Mission 01 behavior with no meaningful feel/readability regression.**

## Content direction after Geometry v2
The current front-port shuttle is a reference craft, not the final universal geometry.

Path:
`Docking Geometry v2 -> reference-shuttle regression -> side/mid-body -> rear/asymmetric -> simplified hull clearance -> station geometry -> Mission 02 -> Mission 03 -> content/productization gate`.

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
8. require device evidence for tactile/visual/platform behavior
9. promote only after acceptance
10. synchronize canonical handoff at large-group closure

## Cost discipline
Prefer cheap review before expensive build/device work, but avoid repeated scans and closed-phase replay. Use Codex only for batches large enough to justify it and CI only when repeatability saves net work.

The Android build workflow intentionally does not trigger on documentation-only changes.

## Group-closure rule
At every large-group closure synchronize `PROJECT_STATUS.md` and `SESSION_HANDOFF.md`, then verify this file, README and any affected design docs agree on current truth, known risks and the exact next boundary.
