# Twin Dock Project Status

## Current phase
**P0 — Project foundation / V8 preservation**

## Accepted baseline
- Prototype: V8
- Camera: ship-frame
- Control: dual independent 2D RCS pads
- Rotation: fully available from first play
- Docking: precision four-condition synchronization
- Background: deterministic/fixed

## P0 deliverables
- [x] Freeze V8 product contract
- [x] Record exact V8 artifact hash
- [x] Define bounded operating rules
- [x] Establish canonical new-session recovery order (`docs/START_HERE.md`)
- [x] Establish canonical comprehensive session handoff (`docs/SESSION_HANDOFF.md`)
- [x] Require handoff/status synchronization at every large-group closure
- [x] Build a local modularization candidate
- [x] Add deterministic smoke tests to the local candidate
- [ ] Mobile parity check: modular candidate vs V8
- [ ] Promote modular candidate to canonical source after parity

## Documentation authority / recovery
A new session must recover live state through `docs/START_HERE.md` before implementation or delegation. Live GitHub is authoritative over past chat, memory, or copied SHAs.

At every large-group closure, synchronize at minimum:
- `PROJECT_STATUS.md`
- `docs/SESSION_HANDOFF.md`

Also verify that `docs/START_HERE.md` still contains the correct read order and that accepted/frozen decisions are reflected in their canonical documents.

## Next gate
**P1 — Mission 01 vertical slice**

Goal: test whether the core control remains compelling for 3–5 minutes, not merely for one docking attempt.

Proposed sequence:
1. static target
2. translating target
3. rotating target
4. translating + rotating target
5. final precision dock

No fuel economy, progression, combat, or Android packaging before this gate is evaluated.
