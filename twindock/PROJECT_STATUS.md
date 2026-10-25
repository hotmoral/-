# Twin Dock Project Status

## Current phase
**P1 — Mission 01 vertical slice**

## Accepted foundation
- V8 remains the immutable fallback/control baseline.
- P0 modular source passed deterministic smoke tests and mobile feel parity against V8.
- Canonical P0 source preserves the accepted ship-frame camera, dual independent 2D controls, free rotation, inertial motion, and precision four-condition docking.

## P0 closure
- [x] Freeze V8 product contract and exact artifact hash.
- [x] Establish canonical recovery/handoff/operating documents.
- [x] Build modular separation for config/math/state/input/physics/docking/camera/renderer/UI/main.
- [x] Deterministic smoke test PASS.
- [x] 12,000-frame deterministic V8-vs-modular comparison: zero state/metric divergence.
- [x] Mobile feel parity accepted by user.
- [x] Promote modular source to canonical foundation.
- [x] Synchronize P0 handoff package.

## Accepted presentation decision after parity
The user accepted a low-salience station-relative reference treatment because empty space made station rotation direction/rate hard to read:
- faint station reference ring
- sparse radial ticks
- three subtle navigation beacons
- short rotation-direction arc

This decision is accepted, but the modular-source merge belongs to the first P1 presentation slice; it must not alter P0 physics or camera semantics.

## P1 product question
Can the accepted control remain compelling for a continuous 3–5 minute mission instead of only a single docking attempt?

## P1 Mission 01 sequence
1. static docking target
2. translating target
3. rotating target
4. translating + rotating target
5. final precision dock

## P1 first implementation boundary
- add mission/state-flow ownership without rewriting core physics
- define five deterministic target profiles
- transition between targets without apparent universe regeneration
- merge the accepted station-relative reference cues as renderer-only behavior
- preserve recoverable collision/re-approach behavior
- keep UI lightweight and central docking view unobstructed
- no fuel, combat, progression, Android packaging, or broad graphics rewrite

## Validation
- existing P0 smoke regression must remain PASS
- add deterministic mission transition/profile tests
- device playtest after a coherent Mission 01 candidate exists

## Handoff rule
At each large-group closure, update this file and `docs/SESSION_HANDOFF.md` together, then verify `docs/START_HERE.md` still gives the correct recovery order.
