# Twin Dock

Twin Dock is a mobile-first inertial spacecraft docking game built around dual independent 2D RCS controls and a ship-frame camera.

## Start here
For any new GPT session, contributor, or delegated implementation agent, begin with:

`docs/START_HERE.md`

Then follow its required read order. Live GitHub is authoritative over past chat, memory, or copied SHAs.

## Promoted baseline
The accepted prototype baseline is **V8**.

Frozen feel/contract:
- ship-frame camera: the player ship stays fixed while the world moves around it
- two independent 2D thumb pads
- full free rotation from first play
- inertial translation and rotation
- docking requires simultaneous position, relative velocity, orientation, and angular-velocity match
- deterministic/fixed star background
- precision thresholds: distance 11, relative speed 10, direction 0.095 rad, spin 0.10 rad/s

## Development policy
V8 is the immutable fallback. Refactors must prove parity before changing tuning. Work proceeds in bounded slices, with local deterministic checks preferred over expensive build/AI workflows.

At every large-group closure, synchronize `PROJECT_STATUS.md` and `docs/SESSION_HANDOFF.md` before proceeding to the next group.

Current status: see `PROJECT_STATUS.md`.
