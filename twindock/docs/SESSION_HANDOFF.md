# Twin Dock — Session Handoff

This is the canonical new-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Repository / branch
- Repository: `hotmoral/-`
- P0 foundation branch: `twindock-foundation-v1`
- Live remote is authoritative. Old chat text, memories, and copied SHAs are navigation aids only.
- P1 should branch from the live P0 closure commit.

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
Successful docking requires simultaneous match of:
- docking-point position
- relative linear velocity
- orientation
- angular velocity

Visible docking probe/capture geometry and internal coordinates must agree.
UI/visual success feedback must not use looser thresholds than actual success.
Docking should feel earned; avoid large magnetic capture zones.

## 6. Frozen V8 feel constants
V8 remains the immutable fallback until explicitly superseded:
- force scale 58
- deadzone 0.10
- input exponent 2.05
- max speed 78
- max angular speed 0.90
- station omega 0.18
- docking distance 11
- docking relative speed 10
- docking direction error 0.095 rad
- docking angular-speed error 0.10 rad/s

Exact artifact hash is in `BASELINE_V8.md`.

## 7. P0 closure state
P0 is complete.

Accepted facts:
- modular source separated config/math/state/input/physics/docking/camera/renderer/UI/main
- deterministic smoke test PASS
- 12,000-frame deterministic comparison against V8 produced zero divergence in state and docking metrics
- mobile device feel parity against V8 was accepted by the user
- modular source is the canonical implementation foundation
- V8 remains the fallback/control contract

## 8. Accepted relative-motion readability direction
The user reported that empty space made station rotation direction/rate difficult to judge.
A low-salience visual candidate was accepted:
- faint reference ring outside the station
- sparse ticks
- three subtle navigation beacons
- short rotation-direction arc

This is intentionally a visual/readability aid only. It must not change world physics, camera semantics, docking thresholds, or create a busy/motion-sickness-heavy background.
Its modular-source merge is the first P1 presentation task.

## 9. Architecture contract
Keep responsibilities separate:

### Physics/world state
Position, velocity, angle, angular velocity, target motion.

### Input
Pointer identity, two-hand tracking, response curve, body-frame command vectors.

### Camera
World-to-ship-frame presentation only. It must not mutate physical truth.

### Docking
Docking geometry, relative metrics, thresholds, success and recoverable collision behavior.

### Renderer
Visual-only presentation. Prefer deriving visible docking geometry from the same definitions used by docking logic.

### Mission/state flow
Target sequence, stage transition, mission scoring/state. It must not rewrite core physics.

## 10. Failure / recovery philosophy
Prefer:
`mistake -> unstable/bounce state -> recovery -> re-approach`
over:
`mistake -> immediate fail/reset`.

Recovery is part of the tactile appeal.

## 11. Visual direction
Player ship should read as a docking/service shuttle, not a fighter:
- short wide craft
- clear forward docking probe/collar
- left/right RCS pods
- multiple attitude-control nozzles
- left/right accents
- RCS plume positions should make input/force legible

Station docking port should visibly include capture collar, inner tunnel/port, guide lights, and latch/capture feedback.
UI should expose the world rather than cover it. Long term, alignment should increasingly be communicated by the docking scene instead of permanent debug checklists.

## 12. Current phase: P1 Mission 01
Product question:
**Does the validated control remain compelling for a continuous 3–5 minute mission?**

Planned deterministic sequence:
1. static target
2. translating target
3. rotating target
4. translating + rotating target
5. final precision dock

Difficulty should come from synchronization dimensions, not merely faster targets.

### P1 first implementation boundary
- add mission/state flow as a new layer
- define deterministic five-target profiles
- merge accepted station-relative reference cues as renderer-only behavior
- preserve all P0/V8 feel constants
- maintain continuous scene/background identity between docks
- keep recoverable collision behavior
- keep central view unobstructed

## 13. Deferred / non-goals until P1 evaluation
Do not add yet:
- fuel economy
- oxygen/battery survival
- combat
- upgrades/meta progression
- Android packaging
- 3D-engine migration solely for graphics

Android becomes justified only after a 3–5 minute mission loop, stable touch input, accepted UI direction, and continued replay intent.

## 14. Development / validation pipeline
For each bounded slice:
1. recover live state in required order
2. state one product question
3. classify whether frozen feel is touched
4. define acceptance checks first
5. implement smallest coherent batch
6. run deterministic regressions
7. require device feel validation for input/camera/game-feel changes
8. promote only after acceptance
9. at large-group closure update `PROJECT_STATUS.md` + this handoff together

### Tool economy
- current chat/local tools: design, bounded implementation, static review, deterministic tests
- Codex: substantial implementation batches only; provide scope/non-goals/frozen constants/tests up front
- public GitHub Actions: only when repeatable build/test automation saves net manual work
- do not repeatedly rescan/rebuild/revalidate frozen work without a concrete trigger

## 15. Known regression risks
- mobile pointer capture/input loss
- sensitivity creep during refactor
- camera changes silently changing feel
- visible/internal docking-point divergence
- UI checks and actual docking thresholds diverging
- random background regeneration on reset/resize/fullscreen
- relative-motion aids becoming visually busy and increasing discomfort
- UI covering the central docking scene
- generous auto-capture returning accidentally
- mission layer mutating core physics constants

## 16. Large-group closure checklist
- [ ] exact implementation/decision boundary recorded
- [ ] deterministic tests passed
- [ ] device feel validated when required
- [ ] accepted/frozen decisions recorded
- [ ] `PROJECT_STATUS.md` updated
- [ ] `SESSION_HANDOFF.md` updated
- [ ] `START_HERE.md` recovery order still correct
- [ ] next exact execution boundary recorded
- [ ] known risks/blockers current
- [ ] useful live branch/commit refs refreshed
- [ ] no stale statement contradicts live canonical state
