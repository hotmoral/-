# Twin Dock — Idea Bank

Status rule: **Everything in this file is BANKED unless explicitly promoted elsewhere.**

This is not a roadmap. The purpose is to preserve content headroom, prevent idea loss, and make future content planning cheaper. An idea only becomes a candidate/roadmap item through `CONTENT_EXPANSION_MAP.md` promotion gates.

## How to use this bank
- Prefer ideas that deepen the proven docking/RCS core.
- Before inventing a new system, check whether craft geometry, station geometry, motion, or clearance can already create the desired challenge.
- Promote only a small number of ideas at a time.
- Record why an idea produces a distinct physical problem, not just a different visual theme.
- When a promoted prototype fails, return the idea to the bank with the failure reason rather than deleting the learning.

---

## A. Craft geometry / player vehicle ideas

### A01 — Side-service craft
Docking port sits around the middle of one side. Requires the player to present the craft sideways instead of nose-first.

### A02 — Rear-dock tug
Docking port faces backward. Encourages reversing, braking while visually moving away from the target, and stronger mental transformation.

### A03 — Offset-nose courier
Port remains front-facing but is displaced left/right from centerline. Makes small rotational errors create larger positional errors at the port.

### A04 — Long cargo barge with mid-body port
Very long fore/aft clearance around a central port. A correct port pose can still be physically unsafe because the bow/stern sweeps into nearby structure.

### A05 — Wide maintenance skiff
Wide lateral body, front port. Rotation near walls becomes the primary clearance problem.

### A06 — L-shaped service craft
Docking port on one arm of an asymmetric body. Strongly separates center-of-view from docking-point intuition.

### A07 — T-shaped utility craft
Port at the end of the crossbar rather than nose. Requires a nonstandard final posture.

### A08 — Twin-boom craft
Central body with two long side booms; port on one boom. Makes rotational clearance visually obvious.

### A09 — Ring craft
Port positioned on the rim rather than geometric center. Large lever arm exaggerates port motion during rotation.

### A10 — Compact high-clearance pod
Tiny body with side port. Useful as a control case showing that geometry can become easier even when motion is harder.

### A11 — Forked cargo handler
Two front arms around an inner docking port. Requires threading the target into the fork.

### A12 — Underbody port craft
Port lies below the visual centerline. Tests whether players can read vertical offset in ship-frame view without HUD overload.

### A13 — Diagonal port craft
Port normal is not aligned to a principal body axis. Final dock orientation looks intentionally “crooked” relative to the screen-fixed craft.

### A14 — Multi-port craft
Craft has two or more valid ports with different local positions/orientations. Mission specifies which is active.

### A15 — Select-a-port service craft
Player may choose among multiple ports for the same target, trading approach simplicity against clearance/time.

### A16 — Deployable docking arm
Port anchor extends outward before final approach. Potentially changes leverage/clearance mid-mission; high complexity, keep banked until static anchors are proven.

### A17 — Articulated tug
A secondary module pivots around the main craft. Docking anchor lives on the articulated element. Distant/high-risk idea.

### A18 — Towed payload
Player controls tug but must dock the far end of an attached payload. Strong extension of current control model if tether/rigid-body handling is later justified.

---

## B. Station / target geometry ideas

### B01 — Open external port
No surrounding obstacles. Baseline geometry-control environment.

### B02 — Flat-wall side port
Port mounted flush to a wall. Approach angle matters because overshoot causes immediate structure contact.

### B03 — Recessed alcove
Port is set back into a shallow cavity. Requires translation alignment before final insertion.

### B04 — Deep tunnel port
Long narrow approach corridor. Tests sustained alignment rather than last-second correction.

### B05 — Slot port
Two parallel structures create a narrow lateral window. Wide craft becomes significantly harder than compact craft.

### B06 — Corner port
Port sits near an inside corner. One side of the craft has much less clearance than the other.

### B07 — Ring-center port
Craft must pass partly through a large rotating ring before capture.

### B08 — Rotating-arm port
Target port is on the end of a rotating arm, creating visible tangential velocity.

### B09 — Counter-rotating inner port
Outer structure and inner docking collar rotate at different rates. Strong relative-motion reading challenge.

### B10 — Sliding rail port
Port travels back and forth along a station rail.

### B11 — Orbiting service pod
Docking target orbits a larger fixed structure. Combines target translation with nearby obstacle geometry.

### B12 — Paired wall gap
Port lies between two bulky modules with asymmetric clearance.

### B13 — Radial hub
Several ports point outward from a common rotating hub. Mission selects one target sector.

### B14 — Interior bay
Player enters through a large opening, then docks inside a calmer enclosed volume.

### B15 — Exterior-to-interior sequence
First align with bay entrance, then perform final dock inside. Natural two-stage spatial objective.

### B16 — Moving blast-door corridor
Safe approach window opens/closes slowly. Should remain readable and deterministic if ever promoted.

### B17 — Telescoping port
Station port extends/retracts on a predictable cycle.

### B18 — Offset capture collar
Visual station body center differs substantially from actual port location, testing world-reading rather than center chasing.

---

## C. Relative-motion pattern ideas

### C01 — Static target
Baseline.

### C02 — Constant translation
Target drifts linearly.

### C03 — Constant rotation
Existing core family.

### C04 — Translation + rotation
Existing combined family.

### C05 — Slow acceleration arc
Target velocity changes smoothly rather than remaining constant.

### C06 — Rotation-rate ramp
Target gradually spins faster/slower, demanding predictive matching.

### C07 — Rotation reversal
Target slows, stops, then reverses on a deterministic schedule.

### C08 — Elliptical path
Target follows a simple predictable ellipse.

### C09 — Circular orbit around parent
Target has clear tangential velocity around another structure.

### C10 — Pendulum-like sweep
Target port swings back and forth through a bounded angular range.

### C11 — Figure-eight service path
More complex but still learnable deterministic translation pattern.

### C12 — Intermittent stabilization window
Target alternates between moving and a brief low-motion window. Player can choose to wait or synchronize dynamically.

### C13 — Synchronized twin motion
Station translation and rotation are phase-coupled so the port traces a recognizable repeating curve.

### C14 — Slow precession
Target orientation changes around a second axis conceptually represented in 2D as a changing local port angle. Use only if readable in current visual language.

---

## D. Clearance / spatial-layout ideas

### D01 — Open-space docking
Baseline.

### D02 — One-wall proximity
Only one side is dangerous, encouraging deliberate offset.

### D03 — Two-wall corridor
Requires maintaining a centerline while rotating carefully.

### D04 — Narrow final throat
Open approach becomes tight only near the port.

### D05 — Wide-entry / narrow-exit bay
Easy insertion but difficult correction/escape if badly aligned.

### D06 — Rotational clearance puzzle
Position is easy, but long craft cannot rotate freely near the target.

### D07 — Translation clearance puzzle
Orientation is simple, but lateral movement is constrained.

### D08 — Obstacle behind craft
Approaching too slowly/far can cause the rear of a long craft to contact something during correction.

### D09 — Offset obstacle pair
Creates an S-shaped safe approach corridor without scripting a path.

### D10 — Moving obstacle gate
Obstacle movement is slow and deterministic; player chooses approach timing.

### D11 — Safe holding pocket
A calm open area before the final narrow approach gives a natural staging point.

### D12 — No-turn zone by geometry
Not an artificial rule: there is physically insufficient room to rotate after a certain point, so orientation must be prepared early.

### D13 — Exit-clearance mission
Docking succeeds, but mission later requires undocking/retreat without collision. Possible future extension.

### D14 — Large-craft tiny-clearance bay
Emphasizes precise angular planning over target speed.

---

## E. Docking-objective variations

### E01 — Standard single dock
Baseline.

### E02 — Sequential ports on one station
Complete several ports around the same structure without resetting craft state.

### E03 — Opposite-side sequence
Dock one side, release, then reach the opposite side; tests repositioning around structure.

### E04 — Precision-only challenge
Time is secondary; grade based on residual relative speed/orientation/spin at capture.

### E05 — Time trial
Same physical course, fastest safe completion.

### E06 — No-contact challenge
Any bad collision invalidates top grade but does not necessarily end the run.

### E07 — Recovery challenge
Start intentionally in a poor motion state and judge how efficiently the player stabilizes and docks.

### E08 — Limited-correction challenge
Not fuel economy; instead score rewards fewer large control reversals/oscillations. Use cautiously to avoid changing core feel.

### E09 — Dock-under-motion challenge
Target never provides a calm window; true synchronization required.

### E10 — Hold-and-release
Maintain a safe dock briefly, then undock cleanly on command.

### E11 — Two-anchor alignment
Future advanced objective requiring two separated connection points to align at once. High geometry value, higher implementation complexity.

### E12 — Ordered multi-anchor coupling
Capture first hinge/guide point, then rotate around it to seat a second connection. Potentially strong “mechanical docking” extension.

---

## F. Scenario / role fantasies

### F01 — Station resupply shuttle
Classic service run; clear beginner fantasy.

### F02 — Satellite repair craft
Approach a disabled rotating satellite with an awkward side port.

### F03 — Cargo module delivery
Move a long cargo body into a station bay.

### F04 — Orbital tug repositioning
Dock rear/side to a module before towing or reorienting it. Towing itself can remain future scope.

### F05 — Emergency crew transfer
Fast but controlled dock to a slowly tumbling vehicle.

### F06 — Construction module placement
Dock a structural segment at a very specific orientation.

### F07 — Solar-array service
Large fragile-looking obstacles create strong visual clearance cues.

### F08 — Rotating habitat ring maintenance
Port mounted on rotating circumference.

### F09 — Debris-field service bay
Static debris provides spatial constraints; avoid turning this into combat.

### F10 — Deep-space relay repair
Minimal station, unusual target motion, strong precision focus.

### F11 — Shuttle-to-shuttle rendezvous
Both craft-shaped rather than station-shaped; one acts as target.

### F12 — Rescue pod capture
Small target with irregular drift, but deterministic/readable rather than random chaos.

### F13 — Dockyard transfer
Navigate between multiple nearby large hulls before final capture.

### F14 — Spin-stabilization rescue
Target begins with substantial angular velocity; mission fantasy explains the harder matching task.

---

## G. Mission-structure ideas

### G01 — Skill missions
Each mission teaches one geometry/motion concept.

### G02 — Mixed certification
Several previously learned problems in random-free authored order.

### G03 — Challenge missions
One difficult dock rather than five standard docks.

### G04 — Endurance chain
Many docks with persistent ship state and score accumulation.

### G05 — Daily authored challenge
Later live-content possibility using deterministic mission definitions.

### G06 — Craft certification tracks
Separate short mission sets teach specific craft geometries.

### G07 — Station certification tracks
Same craft, different environmental geometry.

### G08 — Precision league
Rank by smoothness/accuracy rather than only speed.

### G09 — Time-trial league
Fixed deterministic courses for comparable records.

### G10 — Recovery drills
Start from predefined unstable states.

### G11 — Composite exam
Final mission combines side-port craft, rotating station, and constrained geometry.

### G12 — Branching mission set
Player chooses between an easier open-space route and a harder constrained route for higher score. Later possibility.

---

## H. Scoring / mastery ideas

### H01 — Residual-speed score
Lower relative speed at capture improves grade.

### H02 — Orientation precision score
Reward how close to exact alignment the craft is at capture.

### H03 — Spin precision score
Reward angular-velocity match.

### H04 — Contact penalty
Bad contacts reduce grade without ending the mission.

### H05 — Recovery efficiency
Measure time/control effort from bad contact to stable re-approach.

### H06 — Smoothness metric
Penalize repeated large oscillatory corrections only if it correlates with better player understanding.

### H07 — Composite dock quality
Weighted physical quality score from existing docking metrics.

### H08 — Mission rank
S/A/B/C or 1–3 stars based on authored thresholds.

### H09 — Personal best replay target
Show previous best score/time, not ghost motion unless later justified.

### H10 — Consistency award
Reward several high-quality docks in a row.

---

## I. Progression / unlock ideas

### I01 — Craft unlocks as new geometry
Unlocking a craft should preferably unlock a new docking problem, not just a skin.

### I02 — Mission unlocks by demonstrated skill
Open next geometry family after completing prerequisite mission.

### I03 — Optional mastery medals
Do not block basic progression; reward precision players.

### I04 — Craft certification badges
Complete a short test set for each vehicle geometry.

### I05 — Station-sector progression
Different sectors correspond to environmental geometry families rather than arbitrary level numbers.

### I06 — Challenge unlocks from rank
High mission grades reveal advanced variants.

### I07 — Cosmetic-only variants
Safe later addition, clearly separated from gameplay geometry.

### I08 — Training / expert variants
Same mission geometry with more demanding movement or clearance.

### I09 — Player record book
Track best time, quality score, contact count by mission/craft.

### I10 — Completion map
Visualize which geometry families the player has mastered.

---

## J. Presentation / readability ideas

### J01 — Port hardware families
Different visual collars/nozzles/guide rails while preserving a consistent active-anchor language.

### J02 — Craft-local active-port light
Small localized glow/marker at the actual player docking anchor.

### J03 — Station approach-lane lighting
Physical lights embedded in the station geometry rather than HUD arrows.

### J04 — Clearance warning through world lights
Nearby structure subtly warms/red-shifts when hull clearance is tight. Only if it can be derived cleanly and not become noisy.

### J05 — Contact-scrape visual
Short sparks/abrasion cue on bad hull contact, restrained and non-arcade.

### J06 — Mechanical latch sequence variants
Different port families can have different restrained latch animations/audio identities.

### J07 — Interior bay lighting transition
As craft enters a recess/bay, local lighting communicates depth and enclosure.

### J08 — Motion reference hardware
Sparse station markings/ticks that make rotation/translation easier to read in constrained spaces.

### J09 — Craft silhouette readability rules
Every craft should clearly reveal forward/body axes and active port location without text.

### J10 — Port-normal visualization in-world
Very small mechanical/lighting cue indicating the port's mating direction, especially for diagonal/side anchors.

---

## K. Advanced mechanical ideas — later only

### K01 — Dock then tow
After capture, target becomes attached and changes movement dynamics.

### K02 — Rigid payload transfer
Dock to a payload, carry it, then dock payload to another station.

### K03 — Two-body coupled rotation
Attached payload changes rotational response. High risk because it touches accepted control feel.

### K04 — Failed thruster scenario
One RCS axis or side partially degraded. Strong challenge idea but changes control symmetry; requires explicit experiment.

### K05 — External disturbance impulse
A predictable mechanical jolt/vent event disturbs the craft during approach. Avoid random unfairness.

### K06 — Magnetic capture arm
A mechanical arm may engage only after normal docking truth is met. Presentation/sequence extension, not generous auto-capture.

### K07 — Hinged docking
First contact creates a pivot, then player must rotate into full latch.

### K08 — Soft tether capture
First connection constrains distance but not orientation. Potential advanced mechanic.

### K09 — Docking with rotating payload attached
Combines craft geometry and coupled-body clearance; distant idea.

### K10 — Multi-craft handoff
One docking connects to a module, another target receives it. Large future system.

---

## L. Environment / theme ideas that preserve core gameplay

### L01 — Low-orbit Earth backdrop
Visual theme only; keep motion references readable and deterministic.

### L02 — Moon-orbit dockyard
Different distant visual identity, no gravity mechanic required initially.

### L03 — Deep-space construction site
Large sparse structures emphasize geometry.

### L04 — Asteroid service station
Irregular surrounding silhouette creates natural clearance problems.

### L05 — Solar research array
Long thin structures create strong collision/clearance visuals.

### L06 — Rotating habitat
Natural reason for ring/arm motion.

### L07 — Shipyard interior
Large enclosed bay for later constrained missions.

### L08 — Damaged station sector
Bent/offset geometry changes approach without requiring combat/destruction systems.

### L09 — Cargo terminal
Repeated standardized bays with different craft sizes.

### L10 — Relay constellation
Small target craft and sparse visual references.

---

## M. Deliberate hold / genre-drift ideas
These may be interesting someday, but they are intentionally **not** near-term directions because they can overwhelm the docking identity.

### M01 — Combat / weapons
Could create a different game loop; hold until docking content grammar is exhausted/proven.

### M02 — Fuel economy
May discourage experimentation/recovery and change tactile behavior. Only consider with strong evidence.

### M03 — Resource harvesting
Genre expansion, not required to prove docking depth.

### M04 — Crafting
Meta-heavy; hold.

### M05 — RPG stats
Could undermine skill-based control if stats alter physics. Hold.

### M06 — PvP
High networking/balance cost and may conflict with precision-learning focus.

### M07 — Large open world
Massive scope expansion; no current justification.

### M08 — Complex branching story
Can be layered later after gameplay content proves sustainable.

### M09 — Inventory/equipment
Avoid until there is an actual gameplay need.

### M10 — Procedural randomness as primary content source
Twin Dock benefits from learnable, authored/deterministic motion. Procedural generation may later assist authoring, but should not replace readable design.

---

## N. Idea-combination seeds
These are examples of how multiple proven axes could later create higher-order content without inventing a new core mechanic.

### N01
Side-service craft + recessed wall port + slow station rotation.

### N02
Long cargo barge + narrow bay + static target.

### N03
Rear-dock tug + open-space orbiting target.

### N04
Offset-nose courier + rotating-arm port + generous clearance.

### N05
Wide skiff + corridor + no target rotation.

### N06
Diagonal-port craft + flat-wall port + slow translation.

### N07
Twin-boom craft + slot port + static station.

### N08
Compact pod + fast rotating target + open space.

### N09
Long barge + corner port + low motion.

### N10
Side-service craft + interior bay + station translation only.

### N11
Asymmetric craft + holding pocket + narrow final throat.

### N12
Reference shuttle + rotating ring interior + moderate tangential motion.

### N13
Rear-dock tug + moving rail port + open clearance.

### N14
Forked cargo handler + target module that must enter between the forks.

### N15
Multi-port craft + mission that requires two different ports on successive targets.

---

## O. Current likely promotion order
This section is advisory only; `CONTENT_EXPANSION_MAP.md` is authoritative for actual near-term promotion.

1. arbitrary docking anchor model
2. side/mid-body craft
3. rear/asymmetric craft
4. simple compound hull collision
5. recessed/slot station geometry
6. Mission 02
7. Mission 03
8. scoring/rank using existing docking metrics
9. craft unlocks tied to geometry
10. challenge/time/precision variants

The bank should grow continuously, but implementation should remain narrow and evidence-driven.