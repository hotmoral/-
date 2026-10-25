# Twin Dock — Session Handoff

This is the canonical new-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Repository / branch
- Repository: `hotmoral/-`
- P0 foundation branch: `twindock-foundation-v1`
- Live remote is authoritative. Old chat text, memories, and copied SHAs are navigation aids only.
- P1 branch: `twindock-p1-mission01-v1`
- P0 canonical closure commit: `185a974dbd818386019677409f875640df27442f`

## 2. Required recovery order
1. `twindock/docs/START_HERE.md`
2. `twindock/PROJECT_STATUS.md`
3. `twindock/docs/SESSION_HANDOFF.md`
4. `twindock/docs/BASELINE_V8.md`
5. `twindock/docs/FOUNDATION_MANIFEST.md`
6. `twindock/docs/OPERATING_RULES.md`
7. `twindock/README.md`
8. exact source/tests relevant to the next bounded slice

Do not delegate, refactor broadly, package Android, or rerun expensive verification before this recovery pass.

## 3. Product identity
Twin Dock is a mobile-first inertial spacecraft docking game centered on embodied two-hand control.

### Core control
- two independent full-2D thumb pads
- both hands apply thrust-like forces
- common force produces translation
- differential/lever-arm force produces torque
- input changes motion state, not direct position
- inertia is preserved
- full free rotation is available from first play

Rejected control directions:
- one-hand primary control
- car/boat heading-only steering
- forward/back-only twin thrusters
- removing free rotation for tutorial simplicity

## 4. Camera / embodiment
Accepted camera is **ship-frame**:
- player craft remains visually fixed
- controls are interpreted in ship/body coordinates
- nearby station/world geometry moves and rotates relative to the ship
- this substantially increased immersion and replay desire

Do not revert to a freely moving on-screen player ship without a deliberate controlled experiment.

### Motion-comfort direction
Ship-frame rotation can feel intense. Accepted mitigation is visual, not by removing freedom:
- smooth rotational response
- stable body-frame/HUD cues
- calmer distant background than nearby geometry
- sparse relative-motion references rather than busy scenery

## 5. Docking contract
Successful docking requires simultaneous match of docking-point position, relative linear velocity, orientation, and angular velocity. Visible and internal docking geometry must agree. UI feedback and actual success thresholds must agree. Avoid generous magnetic capture.

## 6. Frozen V8 feel constants
- force scale 58
- deadzone 0.10
- input exponent 2.05
- max speed 78
- max angular speed 0.90
- station omega reference 0.18
- docking distance 11
- docking relative speed 10
- docking direction error 0.095 rad
- docking angular-speed error 0.10 rad/s

Exact artifact hash is in `BASELINE_V8.md`.

## 7. P0 closure state
P0 is complete. Modular source is canonical; deterministic smoke PASS; 12,000-frame V8 parity had zero divergence; mobile feel parity was accepted. V8 remains the fallback/control contract.

## 8. Accepted relative-motion readability direction
A low-salience visual treatment is accepted: faint station reference ring, sparse ticks, three subtle navigation beacons, and a short rotation-direction arc. It is a readability aid only and must not change physics/camera/docking or become a busy motion-sickness-heavy background.

## 9. Architecture contract
- Physics/world state: position, velocity, angle, angular velocity, target motion.
- Input: pointer identity, two-hand tracking, response curve, body-frame command vectors.
- Camera: presentation only; never mutate physical truth.
- Docking: geometry, relative metrics, thresholds, success/recoverable collision.
- Renderer: visual only; derive visible docking geometry from docking definitions where possible.
- Mission/state flow: target sequence, transitions, scoring/state; do not rewrite core physics.

## 10. Failure / recovery philosophy
Prefer `mistake -> unstable/bounce -> recovery -> re-approach` over immediate reset. Recovery is part of the tactile appeal.

## 11. Visual direction
Player ship is a docking/service shuttle with clear forward probe/collar, left/right RCS pods, multiple attitude-control nozzles and legible RCS plumes. Station port uses capture collar, inner tunnel, guide lights and latch feedback. UI should expose rather than cover the world.

## 12. Current phase: P1 Mission 01
Product question: **Does the validated control remain compelling for a continuous 3–5 minute mission?**

Sequence: STATIC -> TRANSLATE -> ROTATE -> COMBINED -> FINAL.

### P1 implementation status
A coherent Mission 01 candidate is implemented and awaits device validation.

Implemented:
- mission/state flow is separate
- deterministic five-target profiles
- station world state includes linear velocity (`vx`, `vy`)
- docking-relative velocity includes target translation plus rotational port velocity
- ship state continues between targets; no ship reset after each dock
- deterministic background identity continues across the run
- accepted station reference cues are merged as renderer-only behavior
- recoverable collision/re-approach remains intact
- frozen V8/P0 control constants and docking thresholds are unchanged

Validation completed:
- JavaScript syntax PASS
- P0 smoke regression PASS
- Mission deterministic test PASS

### Exact next gate
Mobile device playtest of Mission 01. Do not tune frozen controls unless the device run exposes a concrete mismatch. Evaluate run continuity, stage differentiation/fairness, visual-cue comfort, input parity, approximate 3–5 minute duration, and replay desire.

## 13. Deferred / non-goals
No fuel economy, survival resources, combat, upgrades/meta progression, Android packaging, or 3D migration before P1 evaluation. Android becomes justified only after the mission loop, stable input, UI direction and replay intent are validated.

## 14. Development / validation pipeline
1. recover live state in required order
2. state one product question
3. classify frozen-feel impact
4. define acceptance checks
5. implement smallest coherent batch
6. run deterministic regressions
7. require device validation for input/camera/game-feel changes
8. promote only after acceptance
9. at large-group closure update `PROJECT_STATUS.md` and this handoff together

Tool economy: use current chat/local tools for bounded work and deterministic checks; Codex only for substantial batches with explicit scope/non-goals/tests; public Actions only when automation saves net work; do not repeatedly revalidate frozen work without a concrete trigger.

## 15. Known regression risks
- mobile pointer capture/input loss
- sensitivity creep
- camera changes affecting feel
- visible/internal docking divergence
- UI threshold/success threshold divergence
- random background regeneration
- visual cues becoming busy/dizzying
- UI covering central scene
- generous auto-capture returning
- mission layer mutating core physics constants

## 16. Large-group closure checklist
- [ ] exact boundary recorded
- [ ] deterministic tests passed
- [ ] device feel validated when required
- [ ] accepted/frozen decisions recorded
- [ ] status + handoff synchronized
- [ ] START_HERE read order still correct
- [ ] next execution boundary recorded
- [ ] risks/blockers current
- [ ] useful live refs refreshed
- [ ] no stale canonical contradictions
