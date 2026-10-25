# Twin Dock — Session Handoff

This is the canonical new-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Repository / branches
- Repository: `hotmoral/-`
- P0 foundation branch: `twindock-foundation-v1`
- P1 Mission 01 branch: `twindock-p1-mission01-v1`
- P0 canonical closure commit: `185a974dbd818386019677409f875640df27442f`
- P1 implementation commit before acceptance closure: `1216c825fc77e172ebd0124b0c865ceb32b87028`
- Live remote is authoritative. Old chats, memories, and copied SHAs are navigation aids only.

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

## 12. P1 Mission 01 — ACCEPTED / CLOSED
Product question: **Does the validated control remain compelling when expanded into a continuous multi-target mission rather than a single docking attempt?**

Accepted answer: **yes**. Mobile device feedback after playing the five-stage candidate was explicitly positive (`좋아`, `재미있네`). This is sufficient to promote the Mission 01 loop concept. Exact run duration was not separately instrumented, so do not invent a measured 3–5 minute duration.

Accepted sequence:
1. `STATIC` — stationary target
2. `TRANSLATE` — translating target, no rotation
3. `ROTATE` — rotating target, no translation
4. `COMBINED` — translating + rotating target
5. `FINAL` — moving + rotating precision dock

Accepted P1 behavior:
- mission/state flow remains separate from core physics
- deterministic five-target profiles
- station world state includes linear velocity (`vx`, `vy`)
- docking-relative velocity includes target translation plus rotational port velocity
- ship state continues between targets; no ship reset after each dock
- deterministic background identity continues across the run
- accepted station reference cues remain renderer-only
- recoverable collision/re-approach remains intact
- frozen V8/P0 control constants and docking thresholds are unchanged

Validation completed:
- JavaScript syntax PASS
- P0 smoke regression PASS
- Mission deterministic test PASS
- mobile Mission 01 playtest ACCEPTED
- fun/replay signal POSITIVE

## 13. Exact next boundary — P2 world-readable feedback / UI reduction
P2 product question:
**Can the player judge docking readiness primarily from the world and docking hardware rather than a permanent debug-style four-condition checklist, while preserving clarity and the accepted game feel?**

Target P2 scope:
- preserve all frozen control, camera, physics, and docking constants
- preserve the accepted five-stage Mission 01 structure
- move position feedback into capture-ring / alignment geometry
- move relative-speed feedback into approach/guidance-light behavior
- move orientation feedback into visible alignment markers
- move angular-speed feedback into rotating/phase-matching visual cues
- reduce or hide the developer-style four-condition checklist during normal play
- keep mission progress compact and non-obstructive
- add restrained stage-complete and final-complete presentation
- preserve the sparse station reference ring/ticks/beacons/rotation arc
- maintain motion-comfort discipline; do not solve readability by filling the screen with moving scenery

P2 acceptance should be device-based because it affects readability and presentation, but deterministic regressions must still confirm frozen gameplay values are untouched.

## 14. Deferred / non-goals
Still deferred until P2 presentation direction is accepted:
- fuel economy
- survival resources
- combat
- upgrades/meta progression
- Android packaging
- 3D-engine migration

Android is now a plausible later step because the mission loop is fun, but platform complexity should follow a stable UI/presentation layer rather than precede it.

## 15. Development / validation pipeline
1. recover live state in required order
2. state one product question
3. classify frozen-feel impact
4. define acceptance checks
5. implement smallest coherent batch
6. run deterministic regressions
7. require device validation for input/camera/game-feel/readability changes
8. promote only after acceptance
9. at large-group closure update `PROJECT_STATUS.md` and this handoff together

Tool economy:
- current chat/local tools for bounded design, implementation, and deterministic checks
- Codex only for substantial batches with explicit scope/non-goals/tests
- public GitHub Actions only when repeat automation saves net work
- avoid repeated scans/builds/revalidation of frozen areas without a concrete trigger

## 16. Known regression risks
- mobile pointer capture/input loss
- sensitivity creep
- camera changes affecting feel
- visible/internal docking divergence
- UI threshold/success threshold divergence
- random background regeneration
- visual cues becoming busy/dizzying
- UI covering central scene
- generous auto-capture returning
- mission/UI layer mutating core physics constants
- removing too much debug feedback before world-space cues are actually readable

## 17. Large-group closure checklist
- [x] P1 exact boundary recorded
- [x] deterministic tests passed
- [x] device feel/playability validated
- [x] accepted/frozen decisions recorded
- [x] status + handoff synchronized
- [x] START_HERE read order remains valid
- [x] next execution boundary recorded
- [x] risks/blockers current
- [x] useful live refs refreshed where relevant
- [x] no known stale canonical contradiction

A fresh GPT session must be able to recover the project from the live repository and this handoff without relying on conversation memory.
