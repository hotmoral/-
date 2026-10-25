# Twin Dock — Session Handoff

This is the canonical new-session handoff. Update it with `PROJECT_STATUS.md` at every large-group closure.

## 1. Repository / accepted branches
- Repository: `hotmoral/-`
- P0 foundation branch: `twindock-foundation-v1`
- P1 accepted Mission 01 branch: `twindock-p1-mission01-v1`
- P2 accepted world-feedback branch: `twindock-p2-world-feedback-v1`
- P3-A accepted event-feedback branch: `twindock-p3-gamefeel-v1`
- P3-B accepted transition/final-polish branch: `twindock-p3b-transition-v1`
- P0 canonical closure reference: `185a974dbd818386019677409f875640df27442f`
- P1 closure-before-P2 reference: `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`
- P3-A accepted closure reference: `62fa4d75301071256dabdb20fdb4c0eb6f97d3d4`
- P3-B accepted closure HEAD: resolve from live `twindock-p3b-transition-v1`; copied SHAs are reference points only.
- Live remote is authoritative. Old chats, memories, copied SHAs and this handoff are navigation aids, not higher authority than live GitHub.

## 2. Required recovery order
Before proposing or implementing work, read in this exact order:
1. `twindock/docs/START_HERE.md`
2. `twindock/PROJECT_STATUS.md`
3. `twindock/docs/SESSION_HANDOFF.md`
4. `twindock/docs/BASELINE_V8.md`
5. `twindock/docs/FOUNDATION_MANIFEST.md`
6. `twindock/docs/OPERATING_RULES.md`
7. `twindock/docs/CONTENT_EXPANSION_MAP.md`
8. `twindock/README.md`
9. exact source/tests relevant to the next bounded slice

Before new mission/content ideation, also read `twindock/docs/IDEA_BANK.md`.

Do not delegate, refactor broadly, package Android, or run expensive CI before this recovery pass.

Already ACCEPTED / CLOSED / FROZEN phases must not be re-tested from scratch merely because a new GPT session started. Revalidate only when relevant source changed, a concrete mismatch appears, or the next slice prospectively depends on that contract.

## 3. Product identity / core feel
Twin Dock is a mobile-first inertial spacecraft docking game centered on embodied two-hand control.

Core control contract:
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

## 4. Design evolution / why current structure exists
The current control model was discovered through repeated tactile prototypes and device tests.

### Early control exploration
1. Direct-touch inertial object control proved the motion-state concept but the finger obscured the playfield.
2. Separated one-hand force pad preserved inertia but lacked embodied feel.
3. Heading/car-like steering constrained correction and felt unintuitive.
4. One 2D joystick improved freedom but braking/reversal/fine correction stayed sluggish.
5. Faster one-hand 2D improved response but still lacked two-hand cooperation.
6. Twin vertical-only thrusters removed useful lateral freedom and made play harder rather than clearer.
7. Two independent full-2D pads were the breakthrough: both hands cooperate for translation while their differential naturally creates rotation.

Design conclusion:
> Extra freedom is not inherently harder when each degree of freedom maps directly to an intuitive corrective action.

### Docking theme selection
Spacecraft docking naturally turns the control model into a skill task requiring simultaneous synchronization of:
- position
- relative linear velocity
- orientation
- angular velocity

The interaction is therefore about matching motion state, not merely reaching a target.

### Sensitivity / starting-state direction
Accepted direction developed toward:
- larger thumb travel
- nonlinear soft response near center
- lower thrust/torque than earliest prototypes
- broad fine-control region
- stationary start
- no automatic forward motion
- local touch point as joystick origin
- global pointer tracking for robust mobile touch

The V3-era sensitivity direction became the basis of frozen V8 feel.

### Visual / geometry contract
The player craft evolved into a compact docking/service shuttle with:
- clear forward probe/collar
- left/right control pods
- multiple visible RCS nozzles
- visible thruster firing tied to input

The station gained capture collar, tunnel, latches and guide lights.

Critical contract:
**visible docking probe/capture geometry must match internal docking geometry.**

Important later clarification:
- this contract freezes **agreement between visible and internal geometry**, not the current craft silhouette or front-center probe location
- the Mission 01 shuttle is now treated as a **reference craft**
- future craft may place docking anchors on the side, rear, middle, or asymmetric locations once Geometry v2 is validated

### Ship-frame camera breakthrough
The decisive presentation change was the ship-frame camera:
- player craft remains visually mostly fixed
- world/station move and rotate relative to the ship
- controls remain interpreted in body coordinates

This materially increased fun and embodiment. Motion-comfort risk is addressed with sparse stable references and calmer distant background motion, not by restricting rotation.

### V7/V8 stabilization
Later work fixed:
- deterministic/fixed background so resize/fullscreen/reset does not appear to regenerate the universe
- precision docking after an earlier failure report was recognized as mainly a docking-location misunderstanding rather than evidence for generous capture

V8 became the immutable fallback/control contract.

## 5. Frozen V8 contract
Do not silently change these during platform work or presentation cleanup:
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

## 6. Camera / motion comfort
Accepted camera is **ship-frame** and is part of the game feel, not a cosmetic preference.

Accepted mitigation:
- stable body-frame/HUD cues
- calmer distant background than nearby geometry
- sparse relative-motion references
- no random background regeneration on resize/reset/fullscreen

Important P3-A fix:
- physical `ship.angle` still wraps normally in `[-π,+π]`
- distant parallax must not directly treat the wrapped value as a fractional visual angle across the boundary
- `src/presentation.js` provides a renderer-facing continuous visual angle
- physical/camera truth is unchanged
- reset re-synchronizes visual angle to physical angle

Do not remove this adapter or move the fix into physics without a concrete reason and controlled test.

## 7. Docking contract
Successful docking requires all four simultaneously:
- docking-point position
- relative linear velocity
- orientation
- angular velocity

Docking-relative velocity includes target translation plus rotational port velocity.
Visible/internal geometry and feedback/actual thresholds must agree.
Avoid generous magnetic capture.

Future Geometry v2 must preserve these truths while generalizing docking anchors from the current front probe to arbitrary local positions/orientations.

## 8. Failure / recovery philosophy
Prefer:
`mistake -> unstable/bounce -> recovery -> re-approach`

over immediate FAIL/RESET.

Recovery is part of the tactile appeal.

## 9. Architecture contract
- Physics/world state: position, velocity, angle, angular velocity, target motion.
- Input: pointer identity, two-hand tracking, response curve, body-frame command vectors.
- Camera: world -> ship-frame presentation; never mutate physical truth.
- Docking: geometry, relative metrics, thresholds, success/recoverable collision.
- Renderer: world visuals only; derive visible docking geometry from docking definitions where possible.
- Feedback renderer: world-readable readiness cues only; no physics mutation.
- Presentation adapter: display continuity/readability only; may adapt wrapped physical values for presentation but must not mutate source physical state.
- Mission/state flow: target sequence, scoring/state; do not rewrite core physics.
- Effects/audio/haptics: presentation only; may observe input/events but must not mutate physics/docking truth.
- Transition layer: presentation only; no gameplay state beyond transient visual state.
- Future content geometry: craft/station docking anchors and collision geometry should become data/geometry-driven only after bounded prototypes expose the actual requirements.

## 10. Visual / UI direction
UI should expose the world rather than cover it.

Accepted direction:
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
- busy rotating scenery
- effects that increase motion sickness or mask physical information

Future geometry direction:
- active player port must be readable on the craft itself even when not nose-mounted
- station target port must remain physically readable
- P2 feedback should derive from the actual anchor frames rather than assuming craft center/nose
- do not solve unusual craft geometry with permanent large HUD arrows if world design can communicate it instead

## 11. P0 — modular foundation: ACCEPTED / CLOSED
- V8 modularized
- deterministic smoke PASS
- 12,000-frame V8 parity: zero divergence
- mobile feel parity: ACCEPTED
- V8 remains immutable fallback/control contract

## 12. P1 — Mission 01: ACCEPTED / CLOSED
Product question: does validated control remain compelling across a continuous multi-target mission?

Accepted answer: **yes**. Device feedback was explicitly positive/fun.

Accepted sequence:
1. `STATIC`
2. `TRANSLATE`
3. `ROTATE`
4. `COMBINED`
5. `FINAL`

Accepted behavior:
- deterministic five-target profiles
- target world state includes linear velocity
- relative velocity includes target translation + rotational port velocity
- ship state continues between dockings; no ship reset
- deterministic background persists
- recoverable collision/re-approach remains intact
- frozen V8/P0 control values and docking thresholds unchanged

Validation: JS syntax PASS, P0 smoke PASS, mission deterministic test PASS, mobile playtest ACCEPTED, fun/replay signal positive.

Do not invent a measured 3–5 minute duration; exact run duration was not separately instrumented.

Mission 01 is the **reference/basic mission**, not the intended total content volume.

## 13. P2 — world-readable docking feedback: ACCEPTED / CLOSED
Product question: can the player judge readiness primarily from world/docking hardware rather than a permanent developer checklist?

Accepted answer: **yes**; device feedback preferred it over the previous presentation.

Accepted normal-play UI:
- compact mission progress + status
- relative-speed numeric readout removed from normal play
- four-condition checklist removed from normal play
- diagnostics retained only via `?debug=1`

Accepted feedback:
- position: capture brackets
- orientation: ship-frame/port notches
- angular velocity: relative-spin trail
- relative linear velocity: drift arrow
- success: restrained green confirmation ring

The visual mapping uses `TD.Docking.checks()` / the same thresholds as actual docking success. Never create a separate hidden visual-threshold contract.

P2 intentionally changed only `index.html`, `styles.css`, `src/main.js`, and added `src/feedback.js`. Core/frozen modules remained unchanged.

## 14. P3-A — event/audio/haptic foundation: ACCEPTED / CLOSED
Accepted behavior:
- low-salience continuous RCS hiss tracks existing input magnitude
- bad contact has distinct mechanical/noise cue + short haptic
- soft capture has distinct cue + short haptic
- latch/hold completion has separate cue
- next target has delayed compact cue
- final Mission 01 completion has short audio/haptic cue
- `?audio=0` and `?haptics=0` allow independent comparison
- AudioContext arms/resumes from `pointerdown`, `touchstart`, `click`
- RCS sound silences on pause/reset/background
- gain automation is bounded rather than appended every animation frame

Implementation introduced `src/effects.js` and `src/presentation.js` while preserving frozen/core modules.

### P3-A issue history
**Audio initially perceived silent:** haptics worked, audio was not heard at the initial low device media volume. AudioContext activation was hardened and gains raised conservatively. Recheck: audio audible around normal mid-level media volume.

**Fifth-dock background flip:** caused by fractional parallax using wrapped physical angle directly. Fix: renderer-facing continuous visual angle in `src/presentation.js`; no physics/camera-semantic change. Angle-wrap boundary check PASS and device recheck confirmed no recurrence.

### P3-A device result
PASS / ACCEPTED:
- audio/haptics work and are low-fatigue
- contact vs capture is distinguishable
- capture/latch/next-target sequence satisfactory
- no touch/input regression
- no perceived control/physics/camera regression
- no background flip after fix

## 15. P3-B — stage transition / final completion: ACCEPTED / CLOSED
P3-B product question:
Can stage transitions and final completion be clearer/more satisfying while preserving P3-A, P2 readability, sparse UI and frozen gameplay truth?

Accepted answer after mobile device check: **yes**.

Accepted implementation:
- new `src/transitions.js` presentation-only controller
- new `transitions.css`
- successful dock briefly pulses compact Mission HUD
- next target uses ~0.98 s thin horizontal sweep + compact `TARGET n / 5` + stage label
- final completion uses ~1.9 s low-opacity edge frame + compact top completion cue
- Mission HUD stays subtly green after full completion until reset/restart
- transition layers are `pointer-events:none`
- reset/restart clears transition state
- `prefers-reduced-motion` respected
- no large central modal; playfield remains visible

P3-A accepted HEAD used as base: `62fa4d75301071256dabdb20fdb4c0eb6f97d3d4`.

P3-B changed exactly:
- `twindock/index.html`
- `twindock/package.json`
- `twindock/src/main.js`
- `twindock/src/transitions.js` (new)
- `twindock/transitions.css` (new)

Unchanged accepted/core files:
- `config.js`
- `input.js`
- `physics.js`
- `docking.js`
- `camera.js`
- `mission.js`
- `renderer.js`
- `feedback.js`
- `effects.js`
- `presentation.js`

Exact current `main.js` / `transitions.js` syntax checks: PASS.
Local clone/npm execution was unavailable because the local execution environment lacked outbound DNS; that was an environment limitation, not a code failure. Since deterministic/core-covered modules were unchanged, accepted P0/P1 suites were not rerun solely for the presentation slice.

### P3-B device result
PASS / ACCEPTED. User response to the candidate was positive (`오 괜찮네`) and no issue/regression was reported in transition clarity, final completion, scene obstruction, motion comfort, touch/input, P3-A audio/haptics, or background continuity.

**P3 as a whole is now ACCEPTED / CLOSED.**

Do not repeat full P0–P3 validation without a relevant source change, concrete mismatch, or prospective dependency.

## 16. Cloudflare mobile-validation exposure
For mobile validation, Twin Dock static assets were exposed under the existing Timing Defense Cloudflare Worker deployment at `/twindock/` without changing Timing Defense Worker/API behavior.

Rules:
- this is validation/exposure convenience only
- source authority remains live Twin Dock branch + canonical docs
- do not overwrite Timing Defense API/worker behavior
- do not allow this temporary arrangement to become permanent product coupling by accident
- if long-lived deployment is needed, prefer a dedicated Cloudflare project/domain

## 17. Canonical content-expansion direction
Two planning documents now govern long-term content growth:
- `docs/CONTENT_EXPANSION_MAP.md` — content grammar, near-term promotion order, prototype gates and macro sequence
- `docs/IDEA_BANK.md` — broad idea stockpile; deliberately not a roadmap

### Core content decision
Do **not** assume the player craft must remain the current shape or always dock from the nose.

The current Mission 01 shuttle/front probe is a reference craft. Future validated content may vary:
- craft silhouette/proportions
- craft docking-anchor local X/Y
- craft docking-anchor local orientation
- station geometry and target-anchor position/orientation
- station translation/rotation pattern
- available approach corridor
- simplified craft/station collision hulls

The intended content-expansion thesis is:
> Keep the proven dual-RCS inertial control and docking truth, but create new spatial/physical problems through geometry, motion and clearance.

### Promotion states
- `BANKED`: retained possibility; no commitment
- `CANDIDATE`: explicit bounded prototype selected
- `VALIDATED`: relevant device test demonstrates distinct useful play
- `ROADMAP`: validated and intentionally scheduled/produced

Do not convert the Idea Bank into an automatic feature list.

### Current promoted post-Android candidates
- Docking Geometry v2: arbitrary player/station local docking anchors
- reference-shuttle regression through the new anchor model
- side/mid-body docking craft
- rear/asymmetric docking craft
- simplified compound hull clearance
- recessed/slot/corridor station geometry
- Mission 02 centered on anchor geometry
- Mission 03 centered on geometry + clearance

Mission 03 is a **productization/content-expansion decision gate**, not the planned end of the game.

### Current macro content path
`minimal Android parity`
→ `freeze wrapper contract`
→ `Docking Geometry v2`
→ `reference-craft regression`
→ `three-craft geometry probe`
→ `simplified hull clearance`
→ `station geometry probe`
→ `Mission 02`
→ `Mission 03`
→ `content expansion reassessment / productization gate`
→ `Mission 04+ and only then justified scoring/unlock/meta/productization expansion`

### Near-term hold
Do not let these displace the geometry-content proof unless a new explicit gate justifies them:
- combat/weapons
- resource harvesting/economy
- crafting
- RPG stats
- large open world
- PvP
- complex narrative systems
- fuel economy as the primary loop
- large inventory/equipment systems

## 18. Exact next boundary — Android packaging lane
P3 is closed. Android packaging is now authorized as a **separate platform/build lane**.

Android product question:
**Can the accepted web game be packaged on Android with essentially identical input feel, rendering/readability, audio/haptics and Mission 01 behavior, without platform-specific regressions or a premature native rewrite?**

### First Android slice: preflight / wrapper contract
Do not immediately rewrite or generate broad native code. First:
1. recover live P3-B closure state
2. confirm exact accepted branch/HEAD
3. inventory web runtime assumptions:
   - multi-touch / pointer identity / pointer capture
   - landscape/orientation
   - fullscreen-equivalent behavior
   - Web Audio lifecycle
   - vibration/haptic availability
   - safe-area layout
   - local relative asset paths
   - pause/resume/background lifecycle
4. choose smallest wrapper approach, preferring Capacitor/WebView-style preservation unless a concrete native-only need appears
5. explicitly define app name, application ID, versioning, min SDK, target SDK and build lane
6. define offline/local asset packaging and network permissions
7. define Android back/pause/resume/orientation behavior
8. define device acceptance checks before generating APK

### Android frozen guards
- no native rewrite of physics/input/docking/camera merely for packaging
- no V8/P0 control tuning while solving wrapper issues
- no Mission 01 redesign
- no P2/P3 presentation redesign in the packaging batch
- do not freeze Mission 01 craft geometry as the universal future content model
- no fuel/combat/progression/3D migration
- platform fixes and gameplay changes remain separate

### Initial Android acceptance checks
- dual-touch controls retain pointer identity and accepted feel
- no touch loss at edges or after pause/resume
- landscape/safe-area layout matches web behavior
- ship-frame camera/parallax continuity matches accepted P3
- audio cues work after normal user interaction
- haptics remain short/meaningful
- all five Mission 01 dockings complete normally
- no final-stage background flip
- reset/lifecycle does not regenerate/randomize background
- install/launch/pause/resume/relaunch lifecycle stable on target device

The first Android goal is **faithful packaging of the accepted game**, not a native redesign.

On parity PASS:
- freeze the Android wrapper/platform contract
- return to the shared web/game core
- begin Docking Geometry v2

## 19. Development / validation pipeline
1. recover live state in required order
2. state one product question
3. classify frozen-feel impact
4. define acceptance checks before implementation
5. implement smallest coherent batch
6. run only deterministic/static regressions relevant to changed source
7. require device validation for input/camera/game-feel/readability/presentation/platform changes
8. promote only after acceptance
9. at every large-group closure synchronize `PROJECT_STATUS.md` + this handoff
10. verify `START_HERE.md`, README, refs, risks and exact next boundary are current

Tool economy:
- current chat/local tools for bounded design/implementation/static checks
- Codex only for substantial batches with explicit scope/non-goals/tests
- public GitHub Actions only when repeat automation saves net work
- avoid repeated scans/builds/revalidation of frozen areas without a concrete trigger

Content economy:
- consult the Idea Bank before inventing a new content family from scratch
- promote only a small bounded set of banked ideas at a time
- prefer geometry/motion/clearance variants before genre-system proliferation
- do not build a giant generic mission schema before Mission 02/03 expose real requirements

## 20. Known regression / scope risks
- mobile pointer capture/input loss
- sensitivity creep
- camera changes affecting feel
- visible/internal docking divergence
- feedback threshold vs actual success divergence
- random background regeneration
- fractional parallax using wrapped physical angle directly and reintroducing `+π/-π` jumps
- visual cues becoming busy/dizzying
- UI covering central scene
- generous auto-capture returning
- mission/UI/feedback/audio/presentation/transition layers mutating core physics constants
- excessive haptics
- audio masking relative-motion cues
- AudioContext remaining suspended if user-gesture arming is removed
- Android WebView lifecycle breaking audio/touch state
- Android back/pause/resume unexpectedly resetting mission or world state
- safe-area/orientation differences covering controls
- temporary shared Cloudflare exposure accidentally overwriting Timing Defense routes
- Android wrapper work accidentally freezing the reference front-probe craft into the permanent content model
- arbitrary anchor geometry being implemented visually without matching docking/velocity math
- hull collision becoming too detailed too early and consuming scope before geometry fun is proven
- Idea Bank entries being mistaken for committed roadmap features
- difficulty degenerating into raw speed increases rather than new spatial problems

## 21. Large-group closure discipline
At every closure:
- implementation/decision boundary explicit
- relevant checks passed
- device feel/readability/presentation/platform validated when required
- accepted/frozen decisions recorded
- `PROJECT_STATUS.md` + `SESSION_HANDOFF.md` synchronized
- `START_HERE.md` current milestone/read order checked
- README current phase checked
- `CONTENT_EXPANSION_MAP.md` updated when content direction/promotion changes
- `IDEA_BANK.md` may grow continuously, but BANKED items must not silently become roadmap commitments
- exact next boundary recorded
- risks/blockers current
- live refs refreshed where useful
- no stale canonical contradiction

A fresh GPT session must be able to recover the project from live GitHub and these documents without conversation memory.
