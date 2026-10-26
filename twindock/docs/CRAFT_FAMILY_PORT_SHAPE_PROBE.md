# Twin Dock — Craft Family + Port Shape Probe

Status: **IMPLEMENTED / BUILD PASS / PHYSICAL DEVICE EVALUATION IN PROGRESS**

This is an experimental Geometry v2 branch. It is not accepted gameplay yet.

## Authority boundary

Accepted continuation remains unchanged:
- branch `twindock-p3b-transition-v1`
- accepted Geometry v2 reference-anchor foundation HEAD `e40352fcc2fd56919f493728015d4edc02571009`

Parent experimental evidence:
- side/mid-body probe showed that moving the docking anchor changes spatial feel
- alternating-anchor device play showed a different feel, but the reference shuttle is small enough that anchor displacement is not dramatic and repeated use of the same silhouette becomes familiar quickly
- device feedback therefore suggests hull size/silhouette and port shape may need to vary together with anchor position to create stronger content contrast

Current experimental branch:
- `twindock-geometry-craft-shape-probe-v1`
- implementation commit `eb5d14e0e58486a130925335526d64063a398ad1`

Do not promote to accepted continuation until physical-device evidence closes the product question.

## Product question

Can craft hull size/silhouette + docking-anchor placement + directional port shape create materially different spatial problems while preserving accepted dual-RCS controls, ship-frame camera, docking thresholds and recovery philosophy?

## Five-stage comparison sequence

The original Mission 01 station motion values are preserved. Only the craft/anchor/port geometry assignment changes.

1. `SHUTTLE · 원형 전방`
   - reference shuttle visual size 84 × 46
   - circular front port
   - reference anchor x=`VISUAL_PROBE_X`, y=0, angle=0

2. `LONG CARGO · 직사각 측면`
   - visual hull 190 × 116
   - rectangular directional port
   - upper side anchor x=0, y=-61, angle=-90°

3. `SHUTTLE · 사다리꼴 전방`
   - same reference shuttle hull and same front anchor as stage 1
   - only port visual semantics change from circle to directional trapezoid
   - this is the cheapest within-run comparison for port-shape readability

4. `WIDE TUG · 사다리꼴 모서리`
   - visual hull 134 × 118
   - broad asymmetric tug silhouette
   - directional trapezoid port
   - strongly eccentric lower-right corner anchor x=58, y=50, angle=45°

5. `LONG CARGO · 직사각 전방`
   - same Long Cargo hull and same rectangular port semantics as stage 2
   - front anchor x=98, y=0, angle=0
   - stage 2 vs 5 provides a same-hull/same-port comparison with anchor location changed, but **not a controlled anchor-only comparison**, because the preserved Mission 01 target-motion profiles also differ between stages 2 and 5

## Port-shape semantics

The probe supports:
- `CIRCLE`
- `RECT`
- `TRAPEZOID`

Rectangle and trapezoid visuals include an asymmetric forward marker so the player can read orientation, not only the major axis.

The station capture fixture also receives a matching directional shape overlay for non-circular ports. This visual frame represents the same orientation truth already used by docking checks; it does **not** introduce a separate hidden threshold.

Port shape is therefore a readability/spatial-semantics experiment in this probe, not polygonal collision geometry yet.

## Hull rendering strategy

The accepted core renderer is not broadly rewritten.

`src/craft-probe.js` remains an experimental renderer adapter loaded between:

`renderer.js -> craft-probe.js -> presentation.js -> main.js`

Behavior:
- reference circular Shuttle passes through the accepted visual unchanged
- Shuttle trapezoid mode replaces only the nose fixture
- Long Cargo and Wide Tug draw deliberately larger alternative hull silhouettes over the accepted reference visual
- craft-specific RCS plume presentation is drawn by the probe adapter
- active player port and target port use matching shape/orientation cues

The P3-A continuous-angle presentation adapter remains in control of renderer-facing angle continuity.

## Frozen contracts untouched

This probe does not change:
- `FORCE_SCALE`
- input deadzone / exponent
- damping
- max linear speed
- max angular speed
- `ANGULAR_TORQUE_SCALE`
- physics integration
- docking thresholds
- docking checks
- ship-frame camera
- P2 threshold mapping
- P3 effects/transitions
- Android wrapper/platform contract

Large hulls use separate visual dimensions. `ship.length` and `ship.width` stay at the accepted physical reference values, specifically so this probe does not silently retune torque or control feel.

## Important physical-truth boundaries

### Broad hull clearance

The current game still lacks simplified hull-vs-station clearance collision. Large alternate hulls are therefore positioned with exposed external anchors so the intended docking pose does not require a recessed approach.

**Recessed / internal docking bays are deliberately deferred.** Adding a visually recessed bay before hull-clearance truth exists would create visible-geometry vs physical-truth mismatch.

### Player-anchor rigid velocity

The accepted Mission 01 relative-velocity contract remains:
- player side = ship COM linear velocity
- target side = station capture-anchor rigid velocity

Eccentric Cargo/Tug anchors make the deferred player-anchor rotational tangential-velocity question more important. This probe must not be interpreted as final acceptance of that velocity semantic.

## Automated evidence

GitHub Actions:
- run `40253672676`
- implementation head `eb5d14e0e58486a130925335526d64063a398ad1`
- result **SUCCESS**

Passed:
- existing accepted web regressions
- presentation-angle regression
- Geometry v2 mission tests
- non-front anchor contract tests
- alternating anchor-class tests
- new craft-family + port-shape contract tests
- probe JS syntax checks
- local Android staging
- renderer/probe/presentation ordering guard
- Capacitor Android shell generation
- Android contract checks before/after sync
- Gradle debug APK build
- artifact upload

Artifact:
- artifact name `twindock-android-debug`
- artifact ID `12621513454`
- artifact ZIP digest `sha256:f9b24db1e23ee928f65ae30995ca2c3cbbc0d81b2974314b37396f3b7dcf4997`
- APK filename `app-debug.apk`
- APK bytes `4,147,165`
- APK SHA-256 `31490585c118875912305df4a5cba94060342fdeb1a6ace79fe219bd86558b1a`

## Physical-device evidence

### 2026-10-26 — stage 5 difficulty observation

Device play feedback: **stage 5 felt substantially harder than the other stages**.

Relevant geometry / motion facts:
- stage 2 = `LONG CARGO · RECT · SIDE`, player anchor radius from COM = 61 (`x=0, y=-61`), target translation `(bodyVx=5, bodyVy=6)`, target `omega=0`
- stage 5 = `LONG CARGO · RECT · FRONT`, player anchor radius from COM = 98 (`x=98, y=0`), target translation `(bodyVx=5, bodyVy=6)`, target `omega=0.18`
- same hull and same port shape mean the stage-2-vs-stage-5 difference is **not explained by hull family or port shape alone**
- stage 5 anchor eccentricity is `98/61 ≈ 1.61×` stage 2, so the player docking point sweeps a materially larger arc for the same craft rotation
- stage 5 also adds rotating-target capture-anchor motion and relative angular-velocity matching pressure that stage 2 does not have

Interpretation:
- this is positive evidence that **anchor eccentricity can be a strong difficulty axis**
- it also confirms that the current five-stage probe is **confounded for causal attribution**: stage 5 combines larger player-anchor radius with the hardest preserved Mission 01 target-motion profile
- do **not** conclude yet that front placement is inherently harder than side placement
- do **not** retune controls or docking thresholds based on this observation

### 2026-10-26 — full device difficulty ordering

User-reported difficulty from hardest to easiest:

`5 > 4 > 2 > 3 > 1`

This ordering is now product evidence, not a theoretical ranking.

Interpretation boundaries:
- stage 5 = Long Cargo / rectangular / front / strongest preserved target rotation
- stage 4 = Wide Tug / trapezoid / corner / combined target motion
- stage 2 = Long Cargo / rectangular / side / translating target
- stage 3 = Shuttle / trapezoid / front / rotating target
- stage 1 = Shuttle / circle / front / static target
- therefore the ranking supports geometry as a meaningful difficulty axis, but it still mixes hull family, anchor geometry, port semantics and target motion

### Rotation-center invariant

Physical-device feedback explicitly rejects moving the craft rotation center / COM as a content trick.

For Geometry v2 content work:
- keep the accepted craft rotation-center semantics fixed
- do not move COM merely to manufacture difficulty
- treat difficulty as a function of the docking anchor **relative to the fixed rotation center**, together with hull geometry and target motion
- if true mass-distribution / inertia work is ever considered, it must be a separate physics workgroup rather than hidden inside content geometry

Next cheapest causal probe:
- use one Long Cargo hull
- use one rectangular port shape
- use identical station position/translation/rotation conditions for every trial
- vary only exposed player-anchor placement/eccentricity/direction
- include matched-radius comparisons so direction can be separated from distance
- keep the accepted rotation center fixed
- keep recessed/internal bays deferred until hull-clearance collision exists

## Physical-device questions

Play the five docks continuously and judge:
1. Does Long Cargo feel materially larger and require a different spatial plan than Shuttle?
2. Does Wide Tug + corner port produce a stronger correction problem than side-anchor-only Shuttle?
3. Stage 1 vs 3: does circle vs trapezoid materially change orientation readability/feel when hull and anchor are otherwise the same?
4. Stage 2 vs 5: does side vs front anchor remain clearly different when hull and port shape are held constant, while remembering that their target-motion profiles are not controlled?
5. Are rectangle/trapezoid direction markers readable without relying on explanatory HUD text?
6. Do large hulls visually remain clear of the station at successful docking poses?
7. Does any alternate hull create confusing RCS presentation or camera interpretation?
8. Can all five remain playable without control retuning or docking-threshold loosening?

## Promotion rule

Positive evidence should promote the following as candidate content axes:
- hull size
- hull silhouette / proportions
- anchor eccentricity / location / angle
- port visual shape / directional readability

Do not promote recessed bays, hull-clearance gameplay, player-anchor rotational velocity, craft-specific control tuning, or movable rotation-center semantics from this probe alone.
