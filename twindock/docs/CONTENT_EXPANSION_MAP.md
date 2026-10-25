# Twin Dock — Content Expansion Map

Purpose: preserve long-term content headroom without turning unvalidated ideas into roadmap commitments.

This document separates **frozen core**, **near-term validation axes**, **promotion gates**, and **later expansion families**. It is a planning authority for content direction, not a promise to implement every listed idea.

## 1. Core rule
Twin Dock should grow primarily by creating new physical/spatial docking problems from the already-proven control model before adding unrelated genre systems.

The preferred expansion question is:
> Can the same dual-RCS inertial control become meaningfully different through craft geometry, docking-anchor geometry, station geometry, relative motion, and clearance constraints?

Do not solve content scarcity first with combat, resource economy, RPG stats, or large meta systems.

## 2. Frozen core — not a content variable
The following are accepted gameplay truth and are not ordinary content knobs:
- two independent full-2D RCS controls
- common force -> translation; differential/lever-arm force -> rotation
- inertial translation and rotation
- free rotation from first play
- ship-frame camera
- recoverable collision/re-approach philosophy
- docking success requires simultaneous position, relative linear velocity, orientation, and angular-velocity match
- world-readable docking feedback should reflect the same truth as actual docking success
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

## 4. Immediate execution sequence

### Stage A — Android parity probe — PASS / CLOSED
Goal: verify the accepted P3 web game survives a thin Android wrapper without changing gameplay truth.

Validated:
- dual simultaneous touch / pointer behavior
- landscape behavior and safe-area handling
- audio
- haptics
- pause/resume/background lifecycle
- local asset packaging
- frame/interaction stability
- Mission 01 parity on a real Android phone

Physical-device acceptance occurred on **2026-10-26 KST**. The user ran the fixed parity matrix and reported all checked behavior normal. No Android-specific gameplay tuning or platform workaround was required after the successful wrapper build.

Exit condition:
- Mission 01 feels materially equivalent to the accepted web version — **PASS**.

Result:
- Android physical-device parity: **PASS / ACCEPTED**
- Android wrapper/platform contract: **FROZEN**
- Android parity lane: **CLOSED**
- game/content development returns to the shared web core

Do not reopen Stage A without a concrete platform/package/device/release trigger.

### Stage B — Docking Geometry v2 — CURRENT NEXT STAGE
Goal: remove the hidden assumption that the player's docking point is always a fixed forward probe.

Target model:
- player docking anchor: local X, local Y, local angle
- station docking anchor: local X, local Y, local angle
- world docking pose derived from local anchors + body transforms
- relative velocity evaluated at the actual docking anchor, including rotational tangential velocity
- orientation matching evaluated from anchor normals/frames, not body-center direction alone
- P2 feedback originates from the actual anchors

Non-goal:
- no broad collision rewrite yet.
- no control/physics tuning.
- no Android-specific gameplay fork.
- no new side/rear craft until the reference shuttle passes regression.

Exit condition:
- the current reference shuttle represented through Geometry v2 reproduces Mission 01 behavior with no meaningful feel/readability regression.

### Stage C — Three-craft geometry probe
Build only enough craft variation to determine whether docking-anchor geometry creates genuinely different play.

Minimum probe set:
1. **Reference Shuttle** — front-center anchor. Control case.
2. **Side-Service Craft** — side/mid-body anchor. Forces lateral/rotational positioning rather than nose-first alignment.
3. **Offset/Tail Craft** — rear or strongly asymmetric anchor. Tests mental transform and non-intuitive approach posture.

Questions:
- does each craft demand a distinct correction strategy?
- is the docking anchor readable without extra HUD clutter?
- does ship-frame camera remain intuitive when the active port is away from the nose?
- can the player recover naturally after a bad approach?

Exit condition:
- at least one non-front anchor produces clearly distinct but understandable gameplay on device.

### Stage D — Simplified hull clearance
Goal: make craft shape matter physically, not only cosmetically.

Start cheap:
- circles / capsules / oriented boxes / small compound primitives
- no arbitrary polygon solver unless demonstrated necessary

Questions:
- can a valid anchor pose still fail because another part of the craft clips the station?
- does this create interesting approach planning rather than frustrating hidden collisions?
- can clearance be communicated visually without adding another checklist?

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
- motion difficulty stays controlled enough that geometry, not raw speed, is the lesson

Mission 02 should answer:
> Does arbitrary docking-anchor geometry sustain a full mission with a learning curve?

### Stage G — Mission 03
Purpose: combine anchor geometry with physical clearance / more constrained station space.

Preferred identity:
- asymmetric/rear/mid-body craft
- simplified hull collision
- constrained approach geometry

Mission 03 should answer:
> Can Twin Dock become a spatial-physics docking game, not merely a sequence of faster moving targets?

### Stage H — Productization gate
Mission 03 is not the end of content. It is the first strong decision point.

At this gate, assess:
- are Mission 01/02/03 meaningfully different?
- is the content grammar producing new problems without changing core controls?
- is the difficulty curve teachable?
- is repetition appearing from motion alone, or does geometry keep the experience fresh?
- which idea-bank families have now earned promotion?

If YES:
- formalize mission/content data structures
- add selection/progression/records only as justified
- continue Mission 04+
- move toward Android productization/release work

If NO:
- do not hide the weakness under meta progression; revisit the content grammar first.

## 5. Content grammar
A future authored docking problem can be thought of as a composition of:

### Craft
- body shape
- docking anchor local position
- docking anchor local normal/orientation
- collision hull
- optionally handling differences only after geometry is proven insufficient

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

## 6. Difficulty policy
Avoid equating difficulty with simply making everything faster.

Preferred difficulty progression:
1. understand a geometry
2. execute it in open space
3. add moderate relative motion
4. reduce clearance
5. combine motion + clearance
6. introduce unusual anchor orientation/placement
7. combine previously learned skills

Raw speed/rotation increases are valid, but should be only one difficulty axis.

## 7. UI/readability implications
The current UI skeleton can remain, but future content must not assume a nose-mounted docking point.

Required direction:
- player docking anchor visibly identifiable on the craft itself
- target anchor visibly identifiable on the station
- position/orientation/spin/drift feedback derived from actual anchor frames
- no large persistent arrow/text explaining where the port is
- avoid moving critical information back into a permanent numeric checklist

If a new geometry cannot be understood without a large HUD explanation, first improve world readability before adding more UI.

## 8. Craft variety policy
Different craft should preferably create different docking problems, not merely different skins.

Good reason for a new craft:
- different anchor location
- different anchor orientation
- different hull clearance
- different proportions that affect approach planning

Weak reason:
- same gameplay geometry with only decorative art changes.

Cosmetic variants may exist later, but they should not be confused with core content variety.

## 9. Mission authoring / data-driven timing
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

## 10. Promotion ladder for ideas
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

## 11. Current promoted candidates
The following are currently promoted above the general idea bank:
- arbitrary player docking-anchor position
- arbitrary player docking-anchor orientation
- side/mid-body docking craft
- rear/asymmetric docking craft
- simplified hull clearance
- station recess/corridor geometry
- open-vs-constrained approach contrast
- Mission 02 centered on anchor geometry
- Mission 03 centered on geometry + clearance

These are still subject to bounded prototype gates; they are not yet accepted gameplay.

## 12. Explicit hold list
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

## 13. Current macro roadmap
`P3 accepted web baseline`
→ `Android parity probe PASS / wrapper contract FROZEN`
→ **`Docking Geometry v2`**
→ `reference-craft regression`
→ `3-craft geometry probe`
→ `simplified hull clearance`
→ `station geometry probe`
→ `Mission 02`
→ `Mission 03`
→ `content-expansion reassessment / productization gate`
→ `mission data generalization + justified progression/meta`
→ `Mission 04+ scale-out`
→ `Android productization / release candidate`

This sequence is directional, not calendar commitment. A failed gate may redirect later stages.
