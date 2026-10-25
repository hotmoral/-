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
**P3 — Game-feel / presentation polish: P3-A ACCEPTED / CLOSED; P3-B is next.**

P0, P1, P2, and P3-A are accepted. P3-A adds a presentation-only effects layer for restrained RCS/mechanical audio and meaningful event haptics while preserving the frozen V8 control/physics/camera/docking contract, accepted Mission 01, and P2 world-readable feedback mappings.

P3-A mobile validation confirmed audio is audible at normal mid-level device volume, haptics are acceptable across the five-dock run, contact/capture cues are distinct and non-fatiguing, and no touch/control/camera feel regression was perceived. A final-dock distant-background flip was traced to wrapped physical angle being multiplied by parallax factors and was fixed with a presentation-only continuous-angle adapter; the device recheck confirmed the flip no longer occurs.

The exact next slice is P3-B: stage-transition and final mission-completion polish, still presentation-only.

See `PROJECT_STATUS.md` for the exact current boundary.

## Operating policy
Work in bounded slices. Refactor and tuning are separate changes. Prefer local deterministic checks over expensive build/AI workflows. Use Codex/CI only when they save net work. P3 must remain presentation-only with respect to accepted gameplay truth; Android packaging follows as a separate lane after P3 device validation.

At every large-group closure, synchronize `PROJECT_STATUS.md` and `docs/SESSION_HANDOFF.md` before proceeding.
