# Twin Dock — START HERE

This file is the first entry point for any new GPT session, human contributor, or delegated implementation agent.

## Authority rule
Live GitHub on the current Twin Dock working/canonical branch is the authority. Past chat, memory, copied SHAs, and handoff text are only navigation aids. If they disagree with live repository state, live repository state wins.

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

Do not start Codex delegation, broad refactors, Android packaging, or expensive CI before this recovery pass is complete.

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

Do not silently change V8 feel constants during structural cleanup. Any change to input response, thrust, damping, maximum speed, angular behavior, ship-frame semantics, or docking thresholds requires an explicit controlled experiment.

See `BASELINE_V8.md` for exact constants and artifact hash.

## Product direction
Preserve these design principles:

- motion-state control, not direct-position control
- recovery from mistakes instead of immediate fail/reset
- full free rotation from first play; do not hide or stage-gate rotation
- precise docking should feel earned, not magnetic from a large distance
- visual docking geometry and physics collision/docking points must match
- deterministic/fixed background; no apparent world reset caused by random background regeneration
- UI should reveal the world rather than cover it
- final gameplay should increasingly communicate alignment through the docking scene itself rather than permanent debug checklists
- avoid fuel economy, progression, combat, or Android packaging until the 3–5 minute mission loop proves compelling

## Development pipeline
For each bounded slice:

1. Recover live state using the required read order.
2. Confirm the exact product question for the slice.
3. Check whether the slice touches frozen V8 behavior.
4. Prefer local deterministic tests for math/contracts.
5. Implement the smallest coherent batch.
6. Run deterministic regression checks.
7. For input/camera/game-feel changes, require device feel validation; synthetic tests are not enough.
8. Promote only after acceptance criteria pass.
9. Update `PROJECT_STATUS.md` and `SESSION_HANDOFF.md` together at group closure.
10. Record any new frozen/accepted decision in the appropriate canonical document.

## Tooling / usage-efficiency rule
Use the cheapest adequate lane:

- design, reasoning, constants, and narrow code review: current chat/local tools
- deterministic math/regression: local Node/browser tests
- Codex: only for implementation batches large enough to justify delegation, with frozen constants and acceptance tests supplied up front
- public GitHub Actions: only when repeatable build/test automation materially reduces manual cost
- Android packaging: only after the web mission loop, input stability, and replay intent are validated

Avoid repeated repository scans, repeated builds, repeated AI delegation, or broad verification of already-frozen areas unless relevant source changed or a concrete mismatch appears.

## Group-closure rule
A "large group" is a coherent milestone or implementation batch whose completion changes project state, architecture, accepted behavior, validation state, or next execution boundary.

At every large-group closure, synchronize the handoff package before starting the next group. `SESSION_HANDOFF.md` must be sufficient for a fresh GPT session to recover the project without relying on conversation memory.
