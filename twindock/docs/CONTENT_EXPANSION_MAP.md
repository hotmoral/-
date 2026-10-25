# Twin Dock — Content Expansion Map

Purpose: preserve long-term content headroom without turning unvalidated ideas into roadmap commitments.

This document separates **frozen core**, **validated foundations**, **near-term validation axes**, **promotion gates**, and **later expansion families**. It is a planning authority for content direction, not a promise to implement every listed idea.

## 1. Core rule
Twin Dock should grow primarily by creating new physical/spatial docking problems from the already-proven control model before adding unrelated genre systems.

Preferred expansion question:
> Can the same dual-RCS inertial control become meaningfully different through craft geometry, docking-anchor geometry, station geometry, relative motion and clearance constraints?

Do not solve content scarcity first with combat, resource economy, RPG stats or large meta systems.

## 2. Frozen core — not a content variable
The following are accepted gameplay truth and are not ordinary content knobs:
- two independent full-2D RCS controls
- common force -> translation; differential/lever-arm force -> rotation
- inertial translation and rotation
- free rotation from first play
- ship-frame camera
- recoverable collision/re-approach philosophy
- docking success requires simultaneous position, accepted relative linear velocity, orientation and angular-velocity match
- world-readable docking feedback reflects the same truth as docking success
- deterministic background / no apparent world regeneration

Changing these requires a new explicit product experiment, not normal content authoring.

## 3. Content variables — intended to remain extensible
These should not be frozen to the Mission 01 implementation:
- craft silhouette and proportions
- player-craft docking-anchor local position
- player-craft docking-anchor local orientation
- station silhouette and local docking geometry
- station-port local position/orientation
- station translation and rotation patterns
- initial relative pose and motion
- available approach corridor / clearance
- simplified craft collision hull
- simplified station collision hull
- mission ordering and composition
- scoring/challenge rules after the physical content model is proven

The current front-center shuttle docking probe is a **reference craft**, not the final universal docking layout.

## 4. Validated platform/foundation state
### Stage A — Android parity probe
Status: **PASS / ACCEPTED / CLOSED**.

The accepted P3 web game was carried into a thin Capacitor Android wrapper and validated on a physical Android phone with no reported mismatch in the fixed parity matrix.

Result:
- Android wrapper/platform contract FROZEN
- shared game/content development returned to the common web core
- no Android-specific gameplay tuning was required

### Stage B1 — Docking Geometry v2 reference-anchor foundation
Status: **PASS / ACCEPTED**.

Implemented:
- player docking anchor as local `x / y / angle`
- station docking anchor as local `x / y / angle`
- world anchor pose derived from body transform
- inverse body pose solving for dock snap/hold
- docking position/orientation and P2 orientation feedback use the same anchor frames
- current reference shuttle/station reproduce Mission 01 docking behavior

Validation:
- 256 deterministic states compare Geometry v2 against the exact legacy reference formulas
- arbitrary non-front/asymmetric anchor transform closes correctly
- accepted web regressions and Android packaging/build path pass

Canonical detail: `docs/GEOMETRY_V2.md`.

### Important relative-velocity boundary
The accepted Mission 01 velocity truth is deliberately preserved during the Geometry v2 structural refactor:
- player side uses ship linear velocity
- target side uses velocity at the actual station capture anchor, including station rotational tangential velocity

Geometry v2 can calculate rigid velocity at the player anchor too. However, promoting player-anchor rotational tangential velocity into docking success would change an already accepted metric, including for the front reference probe.

Therefore full rigid anchor-to-anchor relative velocity is a **CANDIDATE physics experiment**, not an automatic consequence of Geometry v2. It must be evaluated separately before non-front craft acceptance and must not be introduced incidentally during visual/content work.

## 5. Immediate execution sequence
### Stage B2 — Side/mid-body craft geometry probe — NEXT
Goal: determine whether a non-front player anchor creates genuinely distinct but understandable play.

Smallest coherent probe:
- make visible player docking hardware follow `ship.dockAnchor`
- preserve Reference Shuttle as control/fallback
- build one Side-Service Craft or equivalent side/mid-body anchor
- keep handling constants unchanged
- keep current station geometry initially
- do not add hull-clearance collision yet

Questions:
- is the active side port readable without large HUD explanation?
- does it demand a distinct correction/body-posture strategy?
- does ship-frame camera remain intuitive when the active port is away from the nose?
- can the player recover naturally after a bad approach?
- do position/orientation/spin/drift cues agree with visible and physical anchor truth?

Before promotion, separately compare the accepted velocity metric with full rigid anchor-to-anchor velocity. Any change to success truth needs its own evidence.

Exit condition:
- at least one non-front anchor produces clearly distinct but understandable gameplay on device
- no control retuning or threshold loosening is required to make the concept work

### Stage C — Rear/asymmetric craft probe
After the side/mid-body probe passes, test a rear or strongly asymmetric player anchor.

Purpose:
- stress mental body-to-anchor transformation
- test non-intuitive approach posture
- verify world-readable feedback remains sufficient

Do not build many craft variants yet.

Exit condition:
- a second non-front geometry creates another understandable correction pattern rather than merely more confusion.

### Stage D — Simplified hull clearance
Goal: make craft shape matter physically, not only cosmetically.

Start cheap:
- circles / capsules / oriented boxes / small compound primitives
- no arbitrary polygon solver unless demonstrated necessary

Questions:
- can a valid anchor pose still fail because another part of the craft clips the station?
- does this create interesting approach planning rather than frustrating hidden collisions?
- can clearance be communicated visually without another checklist?

Exit condition:
- hull clearance creates meaningful spatial planning and remains readable.

### Stage E — Station geometry probe
Introduce a small set of station-side spatial problems.

Recommended probe families:
- open external port
- wall/side port
- recessed port
- narrow corridor / slot
- rotating arm or ring-mounted port

Do not create a large station catalogue yet.

Exit condition:
- station geometry creates distinct approach planning beyond simply increasing target speed.

### Stage F — Mission 02
Purpose: prove that a new craft/anchor arrangement can carry a complete mission rather than a one-off prototype.

Preferred identity:
- side or mid-body docking as the main new skill
- motion difficulty controlled enough that geometry, not raw speed, is the lesson

Mission 02 should answer:
> Does arbitrary docking-anchor geometry sustain a full mission with a learning curve?

### Stage G — Mission 03
Purpose: combine anchor geometry with physical clearance / constrained station space.

Preferred identity:
- asymmetric/rear/mid-body craft
- simplified hull collision
- constrained approach geometry

Mission 03 should answer:
> Can Twin Dock become a spatial-physics docking game, not merely a sequence of faster moving targets?

### Stage H — Productization gate
Mission 03 is not the end of content. It is the first strong decision point.

Assess:
- are Mission 01/02/03 meaningfully different?
- is the content grammar producing new problems without changing core controls?
- is the difficulty curve teachable?
- is repetition appearing from motion alone, or does geometry keep the experience fresh?
- which idea-bank families have earned promotion?

If YES:
- formalize mission/content data structures
- add selection/progression/records only as justified
- continue Mission 04+
- move toward Android productization/release work

If NO:
- do not hide the weakness under meta progression; revisit the content grammar first.

## 6. Content grammar
A future authored docking problem can be treated as a composition of:

### Craft
- body shape
- docking anchor local position
- docking anchor local normal/orientation
- collision hull
- optionally handling differences only after geometry proves insufficient

### Station
- body/obstacle geometry
- target anchor local position/orientation
- allowed approach volume

### Motion
- station linear motion
- station angular motion
- trajectory/pattern
- initial relative pose
- initial relative velocity

### Space
- open area
- wall proximity
- tunnel/recess
- moving obstruction
- clearance margin

### Objective
- single precise dock
- sequence
- time challenge
- precision challenge
- recovery challenge
- later specialized scenario

A new mission should preferably change one or two primary dimensions at a time before combining many dimensions.

## 7. Difficulty policy
Avoid equating difficulty with simply making everything faster.

Preferred difficulty progression:
1. understand a geometry
2. execute it in open space
3. add moderate relative motion
4. reduce clearance
5. combine motion + clearance
6. introduce unusual anchor orientation/placement
7. combine previously learned skills

Raw speed/rotation increases are valid but only one difficulty axis.

## 8. UI/readability implications
The current UI skeleton can remain, but future content must not assume a nose-mounted docking point.

Required direction:
- player docking anchor visibly identifiable on the craft itself
- target anchor visibly identifiable on the station
- position/orientation/spin/drift feedback derived from actual anchor frames and the accepted docking velocity truth
- no large persistent arrow/text explaining where the port is
- avoid moving critical information back into a permanent numeric checklist

If a new geometry cannot be understood without a large HUD explanation, improve world readability before adding more UI.

## 9. Craft variety policy
Different craft should preferably create different docking problems, not merely different skins.

Good reason for a new craft:
- different anchor location
- different anchor orientation
- different hull clearance
- different proportions that affect approach planning

Weak reason:
- same gameplay geometry with only decorative art changes

Cosmetic variants may exist later, but they should not be confused with core content variety.

## 10. Mission authoring / data-driven timing
Do not build a giant generic mission schema before Mission 02/03 expose real requirements.

After at least two non-reference geometry families work on device, consider a data-driven description covering:
- craft type
- craft anchor
- station type
- station anchor
- station movement profile
- start pose/motion
- clearance geometry
- success thresholds only if a later explicit design decision permits mission-specific thresholds
- scoring modifiers

Default assumption: frozen global docking truth remains shared unless deliberately changed.

## 11. Promotion ladder for ideas
Every idea belongs to one of four states:

### BANKED
Interesting, no implementation commitment.

### CANDIDATE
Worth a bounded prototype because it appears to reinforce Twin Dock's core.

### VALIDATED
Device test showed meaningful distinct play/readability.

### ROADMAP
Validated and selected for production/content scheduling.

Never treat BANKED ideas as promised features.

## 12. Current promoted candidates
Currently promoted above the general idea bank:
- side/mid-body docking craft — **NEXT CANDIDATE**
- rear/asymmetric docking craft — CANDIDATE after side probe
- full rigid player-anchor relative-velocity semantics — CANDIDATE physics experiment before non-front acceptance
- simplified hull clearance
- station recess/corridor geometry
- open-vs-constrained approach contrast
- Mission 02 centered on anchor geometry
- Mission 03 centered on geometry + clearance

Already validated foundation:
- arbitrary local player docking-anchor position/orientation transform
- arbitrary local station docking-anchor position/orientation transform
- reference shuttle parity through Geometry v2

## 13. Explicit hold list
Keep these out of the near-term critical path until the physical content grammar is proven:
- combat/weapons
- resource harvesting/economy
- crafting
- RPG stat trees
- large open world
- PvP
- complex narrative systems
- fuel economy as a primary loop
- large inventory/equipment systems

They may remain in the idea bank as distant possibilities, but should not consume implementation budget now.

## 14. Current macro roadmap
`P3 accepted web baseline`
→ `Android parity PASS / wrapper FROZEN`
→ `Geometry v2 reference-anchor foundation PASS`
→ **`side/mid-body craft probe`**
→ `rear/asymmetric craft probe`
→ `simplified hull clearance`
→ `station geometry probe`
→ `Mission 02`
→ `Mission 03`
→ `content-expansion reassessment / productization gate`
→ `mission data generalization + justified progression/meta`
→ `Mission 04+ scale-out`
→ `Android productization / release candidate`

This sequence is directional, not a calendar commitment. A failed gate may redirect later stages.
