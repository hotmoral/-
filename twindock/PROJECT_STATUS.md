# Twin Dock Project Status

## Current phase
**P1 — Mission 01 vertical slice / device-validation gate**

## Accepted foundation
- P0 modular foundation is canonical.
- V8 remains the immutable fallback/control contract.
- Frozen ship feel constants and precision docking thresholds are unchanged.

## P0 closure
- deterministic smoke test: PASS
- 12,000-frame V8-vs-modular parity: zero divergence
- mobile feel parity: ACCEPTED
- canonical foundation commit: `185a974dbd818386019677409f875640df27442f`

## P1 product question
Can the accepted control remain compelling for a continuous 3–5 minute mission instead of only a single docking attempt?

## Mission 01 candidate
Deterministic sequence:
1. `STATIC` — stationary target
2. `TRANSLATE` — translating target, no rotation
3. `ROTATE` — rotating target, no translation
4. `COMBINED` — translating + rotating target
5. `FINAL` — moving + rotating precision dock

Implemented:
- [x] mission/state-flow layer separated from core physics
- [x] deterministic five-target profiles
- [x] station linear velocity added to target world state
- [x] docking-relative velocity correctly includes target translation + rotation
- [x] continuous ship state between dockings; no ship reset between targets
- [x] same deterministic background remains across mission
- [x] accepted low-salience station reference ring/ticks/beacons/rotation arc merged as renderer-only behavior
- [x] recoverable collision/re-approach behavior preserved
- [x] core V8/P0 input/thrust/speed/docking constants unchanged
- [x] JavaScript syntax checks PASS
- [x] P0 smoke test PASS
- [x] Mission deterministic tests PASS

## Current gate
**Mobile device playtest of Mission 01 candidate.**

Evaluate:
- whether 5 docks feel like one continuous run rather than repeated resets
- whether target-motion progression is legible and meaningfully different
- whether stages 2–5 are fair rather than merely annoying
- whether accepted station-relative visual cues help without adding dizziness
- whether touch/input feel remains P0-equivalent
- rough run duration and desire to replay

Do not tune frozen controls before this playtest identifies a concrete problem.

## Deferred
No fuel, combat, meta progression, Android packaging, or 3D migration before this gate is evaluated.

## Handoff rule
At each large-group closure, update this file and `docs/SESSION_HANDOFF.md` together and verify `docs/START_HERE.md` remains correct.
