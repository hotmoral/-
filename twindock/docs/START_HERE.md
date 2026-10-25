# Twin Dock — START HERE

This file is the first entry point for any new GPT session, human contributor, or delegated implementation agent.

## Authority rule
Live GitHub on the current Twin Dock working/canonical branch is the authority. Past chat, memory, copied SHAs, and handoff text are navigation aids only. If they disagree with live repository state, live repository state wins.

## Required read order
Read these in order before proposing or implementing work:

1. `twindock/docs/START_HERE.md`
2. `twindock/PROJECT_STATUS.md`
3. `twindock/docs/SESSION_HANDOFF.md`
4. `twindock/docs/BASELINE_V8.md`
5. `twindock/docs/FOUNDATION_MANIFEST.md`
6. `twindock/docs/OPERATING_RULES.md`
7. `twindock/README.md`
8. relevant source/tests for the exact next slice

Do not start Codex delegation, broad refactors, Android implementation, or expensive CI before this recovery pass is complete.

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

Do not silently change V8 feel constants during structural or platform work. Any change to input response, thrust, damping, maximum speed, angular behavior, ship-frame semantics, or docking thresholds requires an explicit controlled experiment.

See `BASELINE_V8.md` for exact constants and artifact hash.

## Accepted milestone stack
- **P0**: modular foundation / V8 parity — ACCEPTED / CLOSED
- **P1**: continuous five-target Mission 01 — ACCEPTED / CLOSED; fun/replay signal positive
- **P2**: world-readable docking feedback / reduced debug HUD — ACCEPTED / CLOSED
- **P3-A**: event/audio/haptic foundation + presentation angle-wrap protection — ACCEPTED / CLOSED
- **P3-B**: stage-transition / final-completion polish — ACCEPTED / CLOSED
- **P3 overall**: ACCEPTED / CLOSED after mobile device validation
- **Next**: Android packaging lane, beginning with wrapper/build preflight rather than a native rewrite

## Product direction
Preserve these design principles:
- motion-state control, not direct-position control
- recovery from mistakes instead of immediate fail/reset
- full free rotation from first play; do not hide or stage-gate rotation
- precise docking should feel earned, not magnetic from a large distance
- visual docking geometry and physics collision/docking points must match
- deterministic/fixed background; no apparent world reset caused by random regeneration
- UI should reveal the world rather than cover it
- communicate docking readiness primarily through scene/docking hardware
- keep old numeric/checklist diagnostics for QA rather than normal play
- sparse relative-motion references over busy scenery
- no fuel economy, combat, upgrades/meta progression, or 3D migration without a later explicit product gate

## Accepted P3 notes that must survive platform work
- RCS/mechanical audio and short event haptics are accepted.
- AudioContext must be armed from real user gestures on mobile browsers/WebViews.
- `src/presentation.js` protects distant parallax from `+π/-π` physical angle-wrap discontinuity; do not move this fix into physics casually.
- P3-B uses short non-blocking stage/final transitions; no large central result modal.
- No touch/control/physics/camera feel regression was reported after final P3 device validation.

## Current execution direction — Android packaging preflight
The next product question is:

**Can the accepted web implementation be packaged on Android with essentially identical dual-touch feel, rendering/readability, audio/haptics, camera continuity and Mission 01 behavior, without forcing a native rewrite or introducing platform regressions?**

First Android slice is preflight only:
- confirm live P3-B closure branch/HEAD
- inventory pointer/multi-touch, orientation, fullscreen-equivalent, Web Audio, vibration, safe-area and lifecycle assumptions
- choose the smallest wrapper approach, preferring Capacitor/WebView-style preservation unless a concrete native-only need appears
- define app ID/name/version/min SDK/target SDK/build lane
- define local/offline asset packaging and network permissions
- define back/pause/resume/orientation behavior
- define device acceptance checks before APK generation

Do not rewrite physics/input/docking/camera in native code merely for packaging, and do not mix platform fixes with gameplay tuning.

## Development pipeline
For each bounded slice:
1. Recover live state using the required read order.
2. Confirm the exact product question.
3. Check whether the slice touches frozen V8 behavior.
4. Define acceptance checks before implementation.
5. Prefer local deterministic/static tests for math/contracts and narrow changes.
6. Implement the smallest coherent batch.
7. Run only regressions relevant to changed source.
8. For input/camera/game-feel/readability/presentation/platform changes, require device validation.
9. Promote only after acceptance criteria pass.
10. Update `PROJECT_STATUS.md` and `SESSION_HANDOFF.md` together at group closure.

## Tooling / usage-efficiency rule
Use the cheapest adequate lane:
- design/reasoning/narrow implementation/code review: current chat/local tools
- deterministic math/regression: local Node/browser tests
- Codex: only for implementation batches large enough to justify delegation, with frozen constants and acceptance checks supplied up front
- public GitHub Actions: only when repeatable build/test automation materially reduces manual cost
- Android packaging/build: preserve proven web implementation first; add native complexity only for a concrete requirement

Avoid repeated repository scans, builds, AI delegation, or broad verification of already-frozen areas unless relevant source changed or a concrete mismatch appears.

## Group-closure rule
A large group is a coherent milestone or implementation batch whose completion changes project state, architecture, accepted behavior, validation state, or next execution boundary.

At every large-group closure, synchronize the handoff package before starting the next group. `SESSION_HANDOFF.md` must be sufficient for a fresh GPT session to recover the project without relying on conversation memory.
