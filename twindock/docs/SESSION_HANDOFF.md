# Twin Dock — Session Handoff

This is the canonical new-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Repository / branches
- Repository: `hotmoral/-`
- P0 foundation branch: `twindock-foundation-v1`
- P1 accepted Mission 01 branch: `twindock-p1-mission01-v1`
- Current P2 candidate branch: `twindock-p2-world-feedback-v1`
- P0 canonical closure commit: `185a974dbd818386019677409f875640df27442f`
- P1 accepted closure HEAD before P2: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`
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

## 4. Camera / motion comfort
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

## 5. Docking contract
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

## 6. P0 closure
P0 is complete and canonical.
- modular source promoted
- deterministic smoke PASS
- 12,000-frame V8 parity: zero divergence
- mobile feel parity: ACCEPTED
- V8 remains immutable fallback/control contract

## 7. Accepted relative-motion readability direction
Accepted low-salience scene cues:
- faint station reference ring
- sparse ticks
- three subtle navigation beacons
- short rotation-direction arc

These are readability aids only. Do not turn them into a busy moving background.

## 8. Architecture contract
- Physics/world state: position, velocity, angle, angular velocity, target motion.
- Input: pointer identity, two-hand tracking, response curve, body-frame command vectors.
- Camera: presentation only; never mutate physical truth.
- Docking: geometry, relative metrics, thresholds, success/recoverable collision.
- Renderer: world visuals only; derive visible docking geometry from docking definitions where possible.
- Feedback renderer: world-readable docking-readiness cues only; no physics mutation.
- Mission/state flow: target sequence, transitions, scoring/state; do not rewrite core physics.

## 9. Failure / recovery philosophy
Prefer `mistake -> unstable/bounce -> recovery -> re-approach` over immediate fail/reset. Recovery is part of the tactile appeal.

## 10. Visual direction
Player ship is a docking/service shuttle with clear forward probe/collar, left/right RCS pods, multiple attitude-control nozzles and legible RCS plumes. Station port uses capture collar, inner tunnel, guide lights and latch feedback. UI should expose rather than cover the world.

## 11. P1 Mission 01 — ACCEPTED / CLOSED
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
- docking-relative velocity includes target translation + rotational port velocity
- ship state continues between dockings; no ship reset
- deterministic background continues across the run
- recoverable collision/re-approach remains intact
- frozen V8/P0 control values and docking thresholds remain unchanged

Validation: JS syntax PASS, P0 smoke PASS, mission deterministic test PASS, mobile Mission 01 playtest ACCEPTED, fun/replay signal POSITIVE.

## 12. Current phase — P2 world-readable feedback candidate
P2 product question:
**Can the player judge docking readiness primarily from the world and docking hardware rather than a permanent debug-style four-condition checklist, while preserving clarity and the accepted game feel?**

Current branch: `twindock-p2-world-feedback-v1`.

### P2 implementation
Normal play now keeps only compact mission progress + status + target message. The old relative-speed number and four-condition checklist are removed from normal HUD but retained behind `?debug=1` for QA.

A new transparent `src/feedback.js` module draws docking feedback without altering the accepted world renderer or core gameplay modules.

Visual mappings:
- **position**: four capture brackets close around the docking point; exact threshold turns them green
- **orientation**: fixed ship-frame notches + rotating port notches converge/overlap; exact threshold turns them green
- **angular velocity**: relative-spin trail shrinks as spin mismatch approaches zero; exact threshold turns it green
- **relative velocity**: drift arrow shows direction + magnitude and shrinks as relative speed falls; exact threshold turns it green
- docked state: restrained green confirmation ring

The mapping uses the same `TD.Docking.checks()` thresholds as actual docking success, so there is no hidden looser/stricter visual contract.

### P2 regression boundary
Compared directly with accepted P1 closure HEAD `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`.

Changed files only:
- `twindock/index.html`
- `twindock/styles.css`
- `twindock/src/main.js`
- `twindock/src/feedback.js` (new)

Frozen/core files are unchanged, including `config.js`, `input.js`, `physics.js`, `docking.js`, `camera.js`, `mission.js`, and `renderer.js`.

Changed-JS syntax checks: PASS.

### Exact current gate
**Mobile device playtest of the P2 candidate.**

Evaluate:
- can the player dock without relying on the old checklist?
- after a few approaches, do position / drift / orientation / spin cues become legible?
- are the cues restrained enough not to increase dizziness or clutter?
- does the reduced HUD improve focus on the station?
- is any visual cue misleading or too abstract?
- does control feel remain identical to accepted P1?

If a cue is unclear, change the cue first. Do not retune frozen controls or docking thresholds during this gate.

## 13. Deferred / non-goals
Still deferred during P2:
- fuel economy / survival resources
- combat
- upgrades/meta progression
- 3D-engine migration
- control retuning without a concrete regression

Android packaging is now plausible because Mission 01 is fun, but platform/build complexity should follow a stable accepted P2 presentation layer.

## 14. Development / validation pipeline
1. recover live state in required order
2. state one product question
3. classify frozen-feel impact
4. define acceptance checks
5. implement smallest coherent batch
6. run deterministic/static regressions
7. require device validation for input/camera/game-feel/readability changes
8. promote only after acceptance
9. at large-group closure update `PROJECT_STATUS.md` and this handoff together

Tool economy:
- current chat/local tools for bounded design/implementation/static checks
- Codex only for substantial batches with explicit scope/non-goals/tests
- public GitHub Actions only when repeat automation saves net work
- avoid repeated scans/builds/revalidation of frozen areas without a concrete trigger

## 15. Known regression risks
- mobile pointer capture/input loss
- sensitivity creep
- camera changes affecting feel
- visible/internal docking divergence
- feedback threshold / actual success threshold divergence
- random background regeneration
- visual cues becoming busy/dizzying
- UI covering central scene
- generous auto-capture returning
- mission/UI/feedback layer mutating core physics constants
- removing too much textual feedback before visual cues are actually readable

## 16. Large-group closure discipline
At each large-group closure:
- implementation/decision boundary explicit
- relevant tests/checks passed
- device feel/readability validated when required
- accepted/frozen decisions recorded
- `PROJECT_STATUS.md` + `SESSION_HANDOFF.md` synchronized
- `START_HERE.md` read order checked
- next exact execution boundary recorded
- risks/blockers current
- live refs refreshed where useful
- no stale canonical contradiction

A fresh GPT session must be able to recover the project from the live repository and these documents without relying on conversation memory.
