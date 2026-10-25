# Foundation Manifest

## Immutable fallback contract
- accepted prototype: V8
- filename used at acceptance: `twin_dock_webapp_v8.html`
- size: 33069 bytes
- SHA-256: `fa569b3411acb59edcfde54b4bac6b59970f8aa0e1ef1fb7f7d339ab26a0ab89`
- exact feel constants are frozen in `BASELINE_V8.md`

## P0 modular foundation
The canonical modular implementation separates:
- config
- math/state
- input
- physics
- docking
- camera
- renderer
- UI
- main orchestration

Validation at P0 closure:
- deterministic smoke test: PASS
- deterministic V8-vs-modular comparison: 12,000 frames
- max observed divergence in position, velocity, angle, angular velocity, station angle, and docking metrics: 0
- mobile/device feel parity: ACCEPTED

## Post-parity accepted presentation experiment
A single-file candidate added subtle station-relative reference cues and was accepted on device:
- faint non-rotating reference ring around the station
- sparse radial ticks
- three low-salience navigation beacons
- short rotation-direction arc

This is a renderer-only accepted direction. Its modular merge is intentionally tracked as the first P1 presentation change so the P0 parity foundation stays a clean control point.

## Promotion status
P0 modular source is canonical for feature development. V8 remains the immutable fallback/control contract for regression comparison.
