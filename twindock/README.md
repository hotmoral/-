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

P3 mobile validation also confirmed the final-stage distant-background angle-wrap fix, normal audio at practical device volume, acceptable haptics, and no reported control/camera/touch regression.

## Current phase
**P3 is ACCEPTED / CLOSED. Next: minimal Android packaging/parity lane.**

The Android lane should initially preserve the proven web implementation rather than rewrite gameplay natively. Begin with wrapper/build preflight: multi-touch/pointer capture, landscape/orientation, Web Audio, vibration, lifecycle, safe-area layout, local asset packaging, application ID/version/SDK choices, and device acceptance criteria.

Preferred direction is a thin Capacitor/WebView-style wrapper unless a concrete native-only requirement appears.

Do not mix Android/platform fixes with changes to frozen V8 control, docking thresholds, Mission 01 profiles, P2 feedback mapping, or P3 presentation behavior.

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
- `docs/IDEA_BANK.md` — long-horizon stockpile; **not** a roadmap

Idea states are `BANKED -> CANDIDATE -> VALIDATED -> ROADMAP`. Documentation in the Idea Bank alone does not commit a feature.

See `PROJECT_STATUS.md` for the exact next boundary and `docs/SESSION_HANDOFF.md` for the full project history/architecture/validation record.

## Operating policy
Work in bounded slices. Refactor and tuning are separate changes. Prefer local deterministic checks over expensive build/AI workflows. Use Codex/CI only when they save net work. Device validation is required for input/camera/game-feel/readability/presentation/platform changes.

Prefer geometry/motion/clearance content expansion before adding unrelated combat/economy/RPG/open-world systems.

At every large-group closure, synchronize `PROJECT_STATUS.md` and `docs/SESSION_HANDOFF.md`, then verify `docs/START_HERE.md`, `docs/CONTENT_EXPANSION_MAP.md` when relevant, and this README remain current.
