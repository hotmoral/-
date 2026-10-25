# Twin Dock

Twin Dock is a mobile-first inertial spacecraft docking game built around dual independent 2D RCS controls and a ship-frame camera.

## Start here
For any new GPT session, contributor, or delegated implementation agent, begin with:

`docs/START_HERE.md`

Then follow its required read order. Live GitHub is authoritative over past chat, memory, or copied SHAs.

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

## Canonical foundation
P0 modularization passed deterministic and mobile parity checks and is the canonical implementation foundation for feature work.

A subtle station-relative reference treatment has also been accepted for readability; its modular merge is tracked as the first P1 presentation change so the P0 parity point stays clean.

## Current phase
**P2 — World-readable docking feedback: ACCEPTED / CLOSED.**

The exact next boundary is **P3 — game-feel / presentation polish**: restrained audio, haptics, contact/capture feedback, and stage-transition polish while preserving the frozen V8 control/physics/camera/docking contract, accepted Mission 01, and P2 world-readable feedback mappings.

See `PROJECT_STATUS.md` for the exact current boundary.

## Operating policy
Work in bounded slices. Refactor and tuning are separate changes. Prefer local deterministic checks over expensive build/AI workflows. Use Codex/CI only when they save net work. P3 must remain presentation-only with respect to accepted gameplay truth; Android packaging follows as a separate lane after P3 device validation.

At every large-group closure, synchronize `PROJECT_STATUS.md` and `docs/SESSION_HANDOFF.md` before proceeding.
