# Twin Dock — Session Handoff

This is the canonical new-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Repository / branches
- Repository: `hotmoral/-`
- P0 foundation branch: `twindock-foundation-v1`
- P1 accepted Mission 01 branch: `twindock-p1-mission01-v1`
- P2 accepted world-feedback branch: `twindock-p2-world-feedback-v1`
- P0 canonical closure commit: `185a974dbd818386019677409f875640df27442f`
- P1 accepted closure HEAD before P2: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`
- P2 accepted closure HEAD: resolve from live branch before new work; copied SHAs are reference points only.
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

## 3. Product identity / core feel
Twin Dock is a mobile-first inertial spacecraft docking game centered on embodied two-hand control.

Core control:
- two independent full-2D thumb pads
- common force produces translation
- differential/lever-arm force produces torque
- input changes motion state, not direct position
- inertia is preserved
- full free rotation is available from first play

Rejected directions:
- one-hand primary control
- car/boat heading-only steering
- forward/back-only twin thrusters
- removing free rotation for tutorial simplicity

## 4. How the design evolved / why the current structure exists
This project did not begin with the current docking structure. The control model was discovered through repeated tactile prototypes and device tests. Preserve the causal history below because it explains which parts are accidental implementation details versus actual product decisions.

### Early control exploration
1. **Direct-touch inertial object control** proved the basic idea that input should change motion state rather than directly place an object, but the finger obscured the playfield.
2. **Separated one-hand force pad** preserved inertial control but did not produce enough physical/embodied feel.
3. **Heading-based / car-like steering** felt constrained and made correction unintuitive.
4. **One 2D joystick** was better, but braking/reversal and fine correction remained sluggish.
5. **Faster one-hand 2D control** improved responsiveness but still lacked the intended body-level cooperation.
6. **Twin vertical-only thrusters** made the game harder rather than clearer because useful lateral freedom had been removed.
7. **Two independent full-2D pads** was the breakthrough. Both hands can cooperate to translate while their differential naturally creates rotation. User response was strongly positive and this became the control foundation.

Design conclusion from this sequence:
> Extra freedom is not inherently harder when each extra degree of freedom maps directly to an intuitive corrective action.

### Docking theme selection
Spacecraft docking was chosen because it naturally turns the control model into a readable skill task. A good dock requires synchronization of:
- position
- relative linear velocity
- orientation
- angular velocity

This made the core interaction about matching motion state, not merely reaching a target.

### Sensitivity and starting-state iteration
Early docking tuning was too sensitive. The accepted direction became:
- larger thumb travel
- nonlinear soft response near center
- lower thrust/torque than the first versions
- broad fine-control region
- ship starts fully stationary
- no automatic forward motion
- touch point becomes local joystick origin
- global pointer tracking for robust mobile touch

The V3-era sensitivity direction became the basis of the frozen V8 control feel.

### Visual / geometry correction
The player craft evolved from a simplified engine-like marker into a compact docking/service shuttle with:
- clear forward probe/collar
- left/right control pods
- multiple visible RCS nozzles
- visual thruster firing tied to input

The station gained a capture collar, tunnel, latches and guide lights. A critical contract was established: the visible docking probe/capture point must match the internal docking geometry exactly.

### Ship-frame camera breakthrough
The most important presentation change was moving from a world camera to a **ship-frame camera**:
- player craft remains visually fixed
- world/station move and rotate relative to the ship
- controls remain interpreted in body coordinates

This significantly increased fun and embodiment. It also introduced motion-comfort risk, so the accepted mitigation became sparse stable references and calmer distant background motion rather than restricting rotation.

### V7/V8 stabilization
Later iteration fixed two important presentation/precision issues:
- deterministic/fixed background so resize/fullscreen/reset does not appear to regenerate the universe
- precision docking restored/tightened after it became clear an earlier failure report was mainly a docking-location misunderstanding rather than evidence that capture should be more generous

V8 therefore became the immutable fallback/control contract.

### Formal project phases
- **P0**: preserve V8, modularize source, prove deterministic parity, establish governance/handoff rules.
- **P1**: test whether one fun docking action can become a continuous five-target mission; accepted as fun on device.
- **P2**: replace developer-style docking checklist dependence with world-readable feedback; accepted as better than P1 presentation.
- **P3 next**: add restrained audio/haptics/capture-transition polish without altering accepted physics or readability.
- **Android after P3**: package the stable proven web game as a separate platform/build lane.

## 5. Camera / motion comfort
Accepted camera is **ship-frame**:
- player craft remains visually fixed
- controls are interpreted in ship/body coordinates
- nearby station/world geometry moves and rotates relative to the ship
- this substantially increased immersion and replay desire

Motion-comfort mitigation is visual, not by removing freedom:
- stable body-frame/HUD cues
- calmer distant background than nearby geometry
- sparse relative-motion references rather than busy scenery
- no random background regeneration on resize/reset/fullscreen

## 6. Docking contract
Successful docking requires simultaneous match of:
- docking-point position
- relative linear velocity
- orientation
- angular velocity

Visible and internal docking geometry must agree. UI/world feedback and actual success thresholds must agree. Avoid generous magnetic capture.

Frozen V8 values:
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

Exact V8 artifact hash is in `BASELINE_V8.md`.

## 7. P0 closure
P0 is complete and canonical.
- modular source promoted
- deterministic smoke PASS
- 12,000-frame V8 parity: zero divergence
- mobile feel parity: ACCEPTED
- V8 remains immutable fallback/control contract

## 8. Accepted relative-motion readability direction
Accepted low-salience scene cues:
- faint station reference ring
- sparse ticks
- three subtle navigation beacons
- short rotation-direction arc

These are readability aids only. Do not turn them into a busy moving background.

## 9. Architecture contract
- Physics/world state: position, velocity, angle, angular velocity, target motion.
- Input: pointer identity, two-hand tracking, response curve, body-frame command vectors.
- Camera: presentation only; never mutate physical truth.
- Docking: geometry, relative metrics, thresholds, success/recoverable collision.
- Renderer: world visuals only; derive visible docking geometry from docking definitions where possible.
- Feedback renderer: world-readable docking-readiness cues only; no physics mutation.
- Mission/state flow: target sequence, transitions, scoring/state; do not rewrite core physics.
- Audio/haptics in future work must remain a presentation layer and must not mutate physics/docking truth.

## 10. Failure / recovery philosophy
Prefer `mistake -> unstable/bounce -> recovery -> re-approach` over immediate fail/reset. Recovery is part of the tactile appeal.

## 11. Visual direction
Player ship is a docking/service shuttle with clear forward probe/collar, left/right RCS pods, multiple attitude-control nozzles and legible RCS plumes. Station port uses capture collar, inner tunnel, guide lights and latch feedback. UI should expose rather than cover the world.

## 12. P1 Mission 01 — ACCEPTED / CLOSED
Product question: does the validated control remain compelling when expanded into a continuous multi-target mission rather than a single docking attempt?

Accepted answer: **yes**. User device feedback was explicitly positive and fun. Exact run duration was not separately instrumented, so do not invent a measured 3–5 minute duration.

Accepted sequence:
1. `STATIC`
2. `TRANSLATE`
3. `ROTATE`
4. `COMBINED`
5. `FINAL`

Accepted P1 behavior:
- deterministic five-target profiles
- target world state includes linear velocity
- docking-relative velocity includes target translation plus rotational port velocity
- ship state continues between dockings; no ship reset
- deterministic background continues across the run
- recoverable collision/re-approach remains intact
- frozen V8/P0 control values and docking thresholds remain unchanged

Validation: JS syntax PASS, P0 smoke PASS, mission deterministic test PASS, mobile Mission 01 playtest ACCEPTED, fun/replay signal POSITIVE.

## 13. P2 world-readable feedback — ACCEPTED / CLOSED
P2 product question:
**Can the player judge docking readiness primarily from the world and docking hardware rather than a permanent debug-style four-condition checklist, while preserving clarity and the accepted game feel?**

Accepted answer: **yes**. User device feedback after the P2 candidate was that it was better than the previous version.

Accepted normal-play UI:
- compact mission progress + compact status
- old relative-speed numeric readout removed from normal play
- old four-condition checklist removed from normal play
- old diagnostics available only with `?debug=1` for QA

Accepted world-readable feedback:
- **position**: four capture brackets converge around the docking point and turn green at the exact position threshold
- **orientation**: ship-frame and rotating port notches converge/overlap and turn green at the exact direction threshold
- **angular velocity**: relative-spin trail shrinks as mismatch approaches zero and turns green at the exact spin threshold
- **relative velocity**: drift arrow shows relative-motion direction/magnitude and turns green at the exact relative-speed threshold
- docked state gets a restrained green confirmation ring

The feedback mapping uses `TD.Docking.checks()` / the same thresholds as actual docking success. Do not create a separate hidden visual threshold contract.

P2 implementation intentionally touched only:
- `twindock/index.html`
- `twindock/styles.css`
- `twindock/src/main.js`
- `twindock/src/feedback.js`

Core/frozen modules remained unchanged: `config.js`, `input.js`, `physics.js`, `docking.js`, `camera.js`, `mission.js`, `renderer.js`.

Validation:
- changed-JS syntax PASS
- P1-vs-P2 scope compare confirmed no frozen/core source changes
- mobile device readability/presentation check ACCEPTED

## 14. Exact next boundary — P3 game-feel / presentation polish
P3 product question:
**Can restrained audio, haptics, contact/capture feedback, and stage transitions make docking substantially more satisfying without obscuring physical information, increasing fatigue, or changing the accepted control/docking behavior?**

Target P3 scope:
- preserve all frozen control/physics/camera/docking values
- preserve the accepted five-stage Mission 01
- preserve P2 world-readable feedback mappings
- add restrained spacecraft-internal / RCS / mechanical audio cues rather than loud arcade effects
- improve bad-contact / bounce / recovery feedback
- improve soft-capture, latch and next-target transition feedback
- use short low-fatigue haptic patterns only for meaningful events
- improve final mission-complete presentation without covering the scene
- keep audio/haptics separable and easy to disable or compare

P3 non-goals:
- no fuel economy / survival resources
- no combat
- no upgrades/meta progression
- no 3D-engine migration
- no frozen-control or docking-threshold tuning without a concrete regression
- no Android packaging inside the same implementation batch

## 15. Android direction
Android packaging is now justified as a near-term platform step because:
- the core control is accepted
- Mission 01 continuous play is fun
- P2 world-readable UI direction is accepted

However, finish and device-validate P3 first. Then Android can be introduced as a separate platform/build lane, preferably preserving the proven web implementation initially (PWA/Capacitor-style wrapper unless a native-only requirement appears).

## 16. Development / validation pipeline
1. recover live state in required order
2. state one product question
3. classify frozen-feel impact
4. define acceptance checks
5. implement smallest coherent batch
6. run deterministic/static regressions
7. require device validation for input/camera/game-feel/readability/presentation changes
8. promote only after acceptance
9. at large-group closure update `PROJECT_STATUS.md` and this handoff together

Tool economy:
- current chat/local tools for bounded design/implementation/static checks
- Codex only for substantial batches with explicit scope/non-goals/tests
- public GitHub Actions only when repeat automation saves net work
- avoid repeated scans/builds/revalidation of frozen areas without a concrete trigger

## 17. Known regression risks
- mobile pointer capture/input loss
- sensitivity creep
- camera changes affecting feel
- visible/internal docking divergence
- feedback threshold / actual success threshold divergence
- random background regeneration
- visual cues becoming busy/dizzying
- UI covering central scene
- generous auto-capture returning
- mission/UI/feedback/audio layer mutating core physics constants
- excessive haptics causing fatigue
- audio masking relative-motion cues or becoming arcade-like

## 18. Large-group closure discipline
At each large-group closure:
- implementation/decision boundary explicit
- relevant tests/checks passed
- device feel/readability/presentation validated when required
- accepted/frozen decisions recorded
- `PROJECT_STATUS.md` + `SESSION_HANDOFF.md` synchronized
- `START_HERE.md` read order checked
- next exact execution boundary recorded
- risks/blockers current
- live refs refreshed where useful
- no stale canonical contradiction

A fresh GPT session must be able to recover the project from the live repository and these documents without relying on conversation memory.
