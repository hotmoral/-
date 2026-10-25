# Twin Dock — Session Handoff

This is the canonical new-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Repository / branches
- Repository: `hotmoral/-`
- P0 foundation branch: `twindock-foundation-v1`
- P1 accepted Mission 01 branch: `twindock-p1-mission01-v1`
- P2 accepted world-feedback branch: `twindock-p2-world-feedback-v1`
- Current P3 working branch: `twindock-p3-gamefeel-v1`
- P0 canonical closure commit: `185a974dbd818386019677409f875640df27442f`
- P1 accepted closure HEAD before P2: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`
- P2 accepted closure HEAD: resolve from live P2 branch when needed; copied SHAs are reference points only.
- P3-A accepted closure HEAD: resolve from live `twindock-p3-gamefeel-v1` before new work; live remote is authoritative.
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

Already ACCEPTED / CLOSED / FROZEN phases must not be re-tested from scratch merely because a new GPT session started. Revalidate only when relevant source actually changed, a concrete mismatch appears, or the next slice prospectively depends on that contract.

## 3. Product identity / core feel
Twin Dock is a mobile-first inertial spacecraft docking game centered on embodied two-hand control.

Core control:
- two independent full-2D thumb pads
- common force produces translation
- differential/lever-arm force produces torque
- input changes motion state, not direct position
- inertia is preserved
- full free rotation is available from first play

Core experiential loop:
`mistake -> instability -> regain control -> recover -> precise docking`

Rejected directions:
- one-hand primary control
- car/boat heading-only steering
- forward/back-only twin thrusters
- removing free rotation for tutorial simplicity
- generous magnetic capture that substitutes for precision matching

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
- **P0**: preserve V8, modularize source, prove deterministic parity, establish governance/handoff rules — ACCEPTED / CLOSED.
- **P1**: test whether one fun docking action can become a continuous five-target mission — ACCEPTED / CLOSED; fun on device.
- **P2**: replace developer-style docking checklist dependence with world-readable feedback — ACCEPTED / CLOSED; preferred over prior presentation.
- **P3-A**: add presentation-only RCS/mechanical audio, meaningful haptics, capture/contact event feedback, and protect distant-background presentation across physical angle wrapping — ACCEPTED / CLOSED after device validation.
- **P3-B next**: stage-transition / final-completion polish while preserving P3-A and all prior accepted gameplay truth.
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

Important P3-A presentation fix:
- physical `ship.angle` continues to wrap normally in `[-π, +π]`
- distant parallax must not directly treat that wrapped value as a fractional visual angle across the wrap boundary
- `src/presentation.js` now provides a renderer-facing continuous visual angle while leaving physical/camera truth unchanged
- reset must re-synchronize visual angle to the physical angle

Do not remove this adapter or replace it with a physics-angle change unless there is a concrete reason and controlled test.

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
- Camera: world -> ship-frame presentation; never mutate physical truth.
- Docking: geometry, relative metrics, thresholds, success/recoverable collision.
- Renderer: world visuals only; derive visible docking geometry from docking definitions where possible.
- Feedback renderer: world-readable docking-readiness cues only; no physics mutation.
- Presentation adapter: visual continuity/readability only; may adapt wrapped physical state for display but must not mutate source physical state.
- Mission/state flow: target sequence, transitions, scoring/state; do not rewrite core physics.
- Effects/audio/haptics: presentation only; may observe input/event state but must not mutate physics/docking truth.

## 10. Failure / recovery philosophy
Prefer `mistake -> unstable/bounce -> recovery -> re-approach` over immediate fail/reset. Recovery is part of the tactile appeal.

## 11. Visual / UI direction
Player ship is a docking/service shuttle with clear forward probe/collar, left/right RCS pods, multiple attitude-control nozzles and legible RCS plumes. Station port uses capture collar, inner tunnel, guide lights and latch feedback.

UI direction:
- compact mission progress
- compact status
- small stage/target messaging
- transparent lower-corner thumb controls
- world-readable docking feedback
- central playfield stays open

Avoid:
- permanent developer checklist in normal play
- large central overlays
- dense numeric instrument panels
- visually busy rotating background layers
- effects that increase motion sickness or mask physical information

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

## 14. P3-A event-feedback foundation — ACCEPTED / CLOSED
P3 product question:
**Can restrained audio, haptics, contact/capture feedback, and stage transitions make docking substantially more satisfying without obscuring physical information, increasing fatigue, or changing the accepted control/docking behavior?**

P3-A handled the event/effects foundation portion only.

Accepted P3-A behavior:
- continuous low-salience RCS hiss tracks existing left/right input magnitude
- bad contact has a distinct mechanical/noise cue and short haptic
- successful soft capture has a distinct cue and short haptic
- latch/hold completion has a separate cue
- next-target advance has a compact delayed cue
- final Mission 01 completion has a short completion cue + haptic
- audio/haptics are independently disableable (`?audio=0`, `?haptics=0`) for comparison
- audio context arms/resumes from real mobile user gestures (`pointerdown`, `touchstart`, `click`)
- RCS sound silences on pause/reset/backgrounding
- audio gain changes are bounded instead of appending automation every animation frame

Implementation boundary from accepted P2 base:
- `twindock/index.html`
- `twindock/package.json`
- `twindock/src/main.js`
- `twindock/src/effects.js` (new)
- `twindock/src/presentation.js` (new)

Core/frozen modules remained unchanged:
- `config.js`
- `input.js`
- `physics.js`
- `docking.js`
- `camera.js`
- `mission.js`
- `renderer.js`
- `feedback.js`

### P3-A mobile issue / resolution history
**Audio initially reported inaudible:** haptics worked but sound was not heard at the initial device-volume setting. AudioContext activation was hardened and gains were raised conservatively. Recheck confirmed sound is audible with the phone at roughly normal mid-level volume. Do not infer that the audio system is broken merely because a device is at very low media volume.

**Fifth-dock background flip:** user observed the background suddenly appearing to flip around the fifth docking. Root cause was presentation-only: physical `ship.angle` wraps across `+π/-π`, while distant parallax multiplied that wrapped value by fractional rotation factors, causing a discontinuity. Fix was a renderer-facing continuous-angle adapter in `src/presentation.js`; physical state and camera semantics were not changed. A dedicated angle-wrap boundary check passed, reset behavior was protected, and the device recheck confirmed the flip no longer occurs.

### P3-A device acceptance result
**PASS / ACCEPTED.** User confirmed after the fixes:
- audio works at normal mid-level device volume
- haptics work and are not excessive
- contact vs capture feedback is distinguishable
- capture/latch/next-target sequence is satisfactory
- audio does not materially obstruct docking judgment
- no touch/input regression
- no perceived camera/physics/control-feel regression
- fifth-dock background flip no longer occurs
- no remaining issue was reported in the full five-dock run

P3-A is CLOSED. Do not repeat this full validation unless relevant P3-A source changes or a concrete mismatch appears.

## 15. Exact next boundary — P3-B stage-transition / final-completion polish
P3-B product question:
**Can stage transitions and the final mission-complete moment be made clearer and more satisfying while preserving accepted P3-A audio/haptics, P2 world-readable feedback, sparse UI, and all frozen gameplay truth?**

Target P3-B scope:
- improve next-target transition presentation
- improve final mission-complete presentation
- refine contact/capture visuals only where a concrete readability/satisfaction need is identified
- preserve P3-A event audio/haptics unless a concrete regression appears
- keep transitions short, restrained, non-blocking, and low-fatigue
- require mobile device validation before P3-B acceptance

P3-B non-goals:
- no input/control tuning
- no thrust/torque/speed/damping tuning
- no docking-threshold changes
- no camera-semantic change
- no Mission 01 profile redesign
- no fuel economy / survival resources
- no combat
- no upgrades/meta progression
- no 3D-engine migration
- no Android packaging in the same implementation batch

Do not broaden P3-B into a general UI redesign. It is a narrow presentation-polish slice.

## 16. Cloudflare mobile-validation exposure
The repository already has Cloudflare Workers Builds / GitHub integration for the Timing Defense Cloudflare branch. Twin Dock mobile candidates can be exposed without modifying Timing Defense Worker/API behavior by copying only the candidate static assets under the existing asset root as `/twindock/`.

Current test URL path convention:
- `/twindock/index.html`

Important:
- this is a **validation/exposure lane**, not Twin Dock's source authority
- authoritative Twin Dock source remains the live `twindock-p3-gamefeel-v1` branch and canonical docs
- do not overwrite Timing Defense worker/API routes or repurpose its product behavior for Twin Dock
- if future exposure becomes long-lived, prefer a dedicated Cloudflare project instead of coupling products indefinitely

## 17. Android direction
Android packaging is justified as a near-term platform step because:
- core dual-RCS control is accepted
- Mission 01 continuous play is fun
- P2 world-readable UI direction is accepted
- P3-A audio/haptic event foundation is accepted

However, finish and device-validate P3-B first. Then Android should be a separate platform/build lane, initially preserving the proven web implementation (PWA/Capacitor-style wrapper) unless a concrete native-only requirement appears.

## 18. Development / validation pipeline
1. recover live state in required order
2. state one product question
3. classify frozen-feel impact
4. define acceptance checks before implementation
5. implement smallest coherent batch
6. run deterministic/static regressions relevant to changed source
7. require device validation for input/camera/game-feel/readability/presentation changes
8. promote only after acceptance
9. at large-group closure update `PROJECT_STATUS.md` and this handoff together
10. verify `START_HERE.md`, README, refs, risks, and exact next boundary are current

Tool economy:
- current chat/local tools for bounded design/implementation/static checks
- Codex only for substantial batches with explicit scope/non-goals/tests
- public GitHub Actions only when repeat automation saves net work
- avoid repeated scans/builds/revalidation of frozen areas without a concrete trigger

## 19. Known regression risks
- mobile pointer capture/input loss
- sensitivity creep
- camera changes affecting feel
- visible/internal docking divergence
- feedback threshold / actual success threshold divergence
- random background regeneration
- fractional parallax using wrapped physical angle directly and reintroducing `+π/-π` background jumps
- visual cues becoming busy/dizzying
- UI covering central scene
- generous auto-capture returning
- mission/UI/feedback/audio/presentation layers mutating core physics constants
- excessive haptics causing fatigue
- audio masking relative-motion cues or becoming arcade-like
- mobile AudioContext remaining suspended on some browsers if user-gesture arming is removed
- temporary Cloudflare validation exposure accidentally becoming product coupling or overwriting Timing Defense routes

## 20. Large-group closure discipline
At each large-group closure:
- implementation/decision boundary explicit
- relevant tests/checks passed
- device feel/readability/presentation validated when required
- accepted/frozen decisions recorded
- `PROJECT_STATUS.md` + `SESSION_HANDOFF.md` synchronized
- `START_HERE.md` read order/current milestone checked
- README current phase checked
- next exact execution boundary recorded
- risks/blockers current
- live refs refreshed where useful
- no stale canonical contradiction

A fresh GPT session must be able to recover the project from the live repository and these documents without relying on conversation memory.
