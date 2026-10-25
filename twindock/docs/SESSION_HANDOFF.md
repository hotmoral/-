# Twin Dock — Session Handoff

This document is the canonical new-session handoff. Update it at every large-group closure together with `PROJECT_STATUS.md`.

## 1. Repository / branch
- Repository: `hotmoral/-`
- Twin Dock branch at foundation stage: `twindock-foundation-v1`
- Live remote state is authoritative; copied SHAs in old chats are only reference points.

## 2. First-read order for a new session
1. `twindock/docs/START_HERE.md`
2. `twindock/PROJECT_STATUS.md`
3. `twindock/docs/SESSION_HANDOFF.md`
4. `twindock/docs/BASELINE_V8.md`
5. `twindock/docs/FOUNDATION_MANIFEST.md`
6. `twindock/docs/OPERATING_RULES.md`
7. `twindock/README.md`
8. source/tests relevant to the next exact slice

Do not start implementation or delegation until the live branch and these documents have been reconciled.

## 3. Game concept / design direction
Twin Dock is a mobile-first spacecraft docking game centered on embodied inertial control.

### Core control
- two independent 2D thumb pads
- both hands apply thrust-like force
- combined force produces translation
- differential/lever-arm force produces torque and rotation
- inertia is preserved; input changes motion state rather than directly placing the ship
- full free rotation is available from the first moment of play

### Camera / embodiment
Accepted camera is **ship-frame**:
- the player ship remains visually fixed
- nearby world/target geometry moves and rotates relative to the ship
- controls are interpreted in ship/body coordinates
- this presentation substantially improved immersion and replay desire and is part of the core feel

### Docking skill
Docking is not mere collision with a target. Success requires simultaneous match of:
- docking-point position
- relative linear velocity
- facing/orientation
- angular velocity

The visible docking probe/capture ring must coincide with the internal docking coordinates. Avoid hidden stricter success conditions than the UI/visual feedback communicates.

### Difficulty philosophy
Difficulty should come from synchronization and precision, not simply increasing speed.
Possible axes:
- translating target
- rotating target
- translating + rotating target
- tighter position tolerance
- tighter relative-speed tolerance
- tighter orientation/angular-speed tolerance
- constrained approach geometry / surrounding structure

Do not remove free rotation to make early play easier; this was judged more confusing and less coherent.

### Failure / recovery philosophy
Prefer:
`mistake -> unstable state / bounce -> recovery -> re-approach`

over:
`mistake -> instant fail/reset`.

Recovery is part of the tactile appeal.

## 4. Accepted V8 baseline
V8 is the immutable fallback until explicitly superseded.

Frozen feel constants are recorded in `BASELINE_V8.md`:
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

The exact V8 artifact hash is also recorded there.

Important accepted V8 behavior:
- ship-frame camera
- two independent 2D controls
- full rotation from start
- deterministic/fixed background
- precision docking rather than generous magnetic capture
- improved docking-work-shuttle/RCS visual concept

## 5. UX findings from prototype development
The following were learned empirically and should not be casually regressed:

### Better
- two independent full-2D controls were clearly preferred over one-hand control
- preserving lateral correction made the inertial system easier, not harder
- ship-frame camera was reported as more fun than world-frame ship movement
- lower sensitivity / wider fine-control region improved docking control
- starting fully stationary reduced panic and improved learnability
- UI should leave the central docking scene unobstructed

### Worse / rejected
- car/boat heading-only steering
- forward/back-only dual thrusters
- direct touch on the playfield that hides the scene
- removing free rotation for tutorial ease
- large central control buttons/HUD covering the docking scene
- overly generous auto-capture that lets approximate alignment dock
- random background regeneration / apparent scene changes

### Motion-sickness consideration
Ship-frame world rotation can create stronger embodiment and also visual discomfort for some users.
Accepted mitigation direction:
- retain full free rotation
- smooth rotational response rather than restricting freedom
- provide stable body-frame/HUD reference cues
- use layered visual motion so distant background is calmer than nearby station geometry
Do not solve discomfort by disabling rotation.

## 6. Visual / spacecraft direction
The player craft should read as a docking/service shuttle, not a fighter or a single front/back-engine icon.

Visual intent:
- short, wide service craft
- clear forward docking probe/collar
- left/right RCS pods
- multiple visible attitude-control nozzles
- left/right identification accents
- RCS plume location should correspond to actual input/force direction
- docking station uses capture collar, inner tunnel/port, guide lights, and latch/capture feedback

The purpose is not merely decorative realism: visual thruster activation should help explain the two-hand physics.

## 7. Current architecture state
Foundation phase P0 exists to preserve V8 before feature expansion.

A local modularization candidate has already been created with conceptual separation for:
- config
- math/state
- input
- physics
- docking
- camera
- renderer
- UI
- main orchestration

Deterministic smoke tests passed, but the modular candidate is **not canonical yet** because mobile/device feel parity against V8 must be confirmed first.

See `FOUNDATION_MANIFEST.md` and `PROJECT_STATUS.md` for current validation state.

## 8. Target architecture rule
When the candidate is promoted, maintain hard separation between:

### Physics/world state
Owns position, velocity, angle, angular velocity, target motion.

### Input
Owns pointer identity, two-hand tracking, deadzone/response curve, ship-frame command vectors.

### Camera
Transforms world state into ship-frame presentation. It must not mutate physical truth.

### Docking
Owns docking geometry, relative-motion metrics, thresholds, success/collision behavior.

### Renderer
Visual only. Visual docking points must be derived from the same geometry used by docking logic where possible.

### Mission/state flow
Owns target sequence, transitions, scoring, and mission progression without rewriting core physics.

This separation exists specifically to prevent UI/graphics/mission work from silently changing the tactile baseline.

## 9. Development / validation pipeline
For each bounded work slice:

1. recover live repository state
2. read canonical docs in required order
3. identify one product question
4. classify whether frozen feel is touched
5. define acceptance checks before implementation
6. implement smallest coherent batch
7. run deterministic regression tests
8. if input/camera/feel changed, run mobile device comparison
9. promote only when accepted
10. update project status + this handoff at group closure

### Verification economy
Do not repeatedly revalidate already-frozen material merely because a new chat started.
Revalidation is justified when:
- relevant source changed
- a new relevant commit exists
- a deterministic contract must be re-proven for the current slice
- device behavior shows a concrete mismatch
- a frozen contract explicitly requires a pre-promotion check

## 10. Tool / build strategy
Prefer the least expensive adequate tool path.

### Current chat / local tools
Use for:
- design decisions
- bounded implementation
- static inspection
- local deterministic checks
- quick web prototype iteration

### Codex
Use only for substantial implementation batches where delegation saves net work. Before delegation provide:
- frozen baseline constants
- exact files/scope
- non-goals
- acceptance tests
- expected output boundary

Avoid repeated Codex prompts for tiny edits.

### Public GitHub Actions
Use only once a repeatable test/build workflow materially reduces repeated manual verification. Do not create CI merely for ceremony.

### Android
Do not package yet. Android becomes justified after:
- 3–5 minute Mission 01 loop exists
- mobile input is stable
- core UI direction is accepted
- replay intent remains positive after multi-target play

Initial Android route can remain web-based/PWA/Capacitor unless a concrete native requirement appears.

## 11. Current product boundary / next gate
Current phase: **P0 — foundation and V8 preservation**.

Immediate gate:
- mobile parity check of modular P0 candidate against V8
- if feel is equivalent, promote modular source as canonical implementation foundation

Then begin **P1 — Mission 01 vertical slice**.

Proposed Mission 01 sequence:
1. static docking target
2. translating target
3. rotating target
4. translating + rotating target
5. final precision dock

Purpose of P1:
Determine whether the validated control is compelling for a continuous 3–5 minute play session, not merely for a single docking maneuver.

## 12. Deferred systems / non-goals for now
Do not add before P1 validates the core loop:
- fuel economy
- oxygen/battery survival systems
- upgrade progression
- combat
- large meta-progression
- Android packaging
- 3D-engine migration solely for visual ambition

These can be reconsidered after the core mission loop proves itself.

## 13. Known regression risks
Watch these specifically:
- pointer capture/input loss on mobile
- ChatGPT/container gesture interference versus standalone browser behavior
- sensitivity creeping upward during refactor
- visual docking point and internal docking point diverging
- checklist thresholds differing from actual success thresholds
- background star/random state regenerating after resize/fullscreen/reset
- camera comfort changes accidentally altering core control
- UI expansion covering the docking scene
- auto-capture becoming too generous
- refactor silently changing constants

## 14. Large-group closure checklist
Before declaring a large group complete:
- [ ] implementation/decision boundary is explicit
- [ ] relevant deterministic tests passed
- [ ] device feel validated if required
- [ ] accepted/frozen decisions recorded
- [ ] `PROJECT_STATUS.md` updated
- [ ] `SESSION_HANDOFF.md` updated
- [ ] `START_HERE.md` read order still correct
- [ ] next exact execution boundary recorded
- [ ] known risks/blockers recorded
- [ ] branch/commit references refreshed from live GitHub where useful
- [ ] no stale statement in handoff contradicts live canonical docs

A new GPT session should be able to recover the project by reading repository documents alone, without relying on conversation memory.
