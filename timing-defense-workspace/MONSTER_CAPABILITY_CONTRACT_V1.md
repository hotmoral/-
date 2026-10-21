# Timing Defense — Monster Capability Contract V1

Date: 2026-10-22 KST
Status: **STRUCTURE FROZEN V1 / PRODUCTION NUMBERS NOT FROZEN**

## 0. Purpose

Define the non-boss monster vocabulary before final 50-stage authoring and numerical calibration.

This contract deliberately separates:
1. **capability / behavior structure**, which is frozen here, from
2. **production balance values**, which remain provisional until the 50-stage tier/pressure/progression model is calibrated.

The old Stage 1–10 encounter recipes are no longer the target campaign design. Existing Stage 1–3 Cloudflare content remains a regression fixture for the validated multiplayer/combat kernel, not a promise that the final campaign will preserve those recipes.

The intended core roster is **9 non-boss archetypes**:
- GRUNT
- RUNNER
- BRUTE
- SHIELD
- FLYER
- CHARGER
- SPLITTER
- SUPPORTER
- SIEGER

Bosses are a separate layer and may compose or modify these capabilities later. A boss is not counted as a tenth ordinary archetype.

---

# 1. Global design constraints

## 1.1 Every archetype must create a different player decision
Do not add a monster whose only identity is "same thing but +HP" or "same thing but +speed".

Primary pressure axes:
- baseline/reference,
- sustained tempo,
- raw durability,
- armor mitigation,
- vertical/spatial geometry,
- burst tempo / interrupt window,
- population transformation,
- formation support,
- ranged/objective pressure.

## 1.2 No hard class lockouts
Every class must be able to kill every ordinary monster.

Class identity may produce soft advantages, but ordinary monsters must not require one specific class to progress.

Examples:
- Tank may be especially good at interrupting/control pressure.
- Mage may be especially good when SPLITTER children cluster.
- Archer may gain value when SUPPORTER is screened behind aligned enemies.
- Rogue may retain value against durable normals.

These are opportunities, not mandatory counters.

## 1.3 Respect the core input model
Timing Defense is a timing game, not a free-target action game.

The monster set must not assume the player can freely click a backline target. Current target acquisition remains system-driven/authoritative.

Therefore SUPPORTER cannot be designed around "manually select and assassinate the healer in the back" as a required solution.

## 1.4 Server authority
All gameplay-relevant monster state must be server authoritative.

The client may interpolate/present, but must not decide:
- state transitions,
- special-ability timing,
- child spawning,
- aura membership/effect,
- ranged wall attack timing,
- damage/armor,
- knockback consequences,
- death/reward/contribution.

## 1.5 Telegraph before exceptional pressure
Any behavior that changes normal movement/attack grammar must have a readable pre-action state.

Required examples:
- CHARGER windup before dash,
- SIEGER windup before wall strike,
- SPLITTER death transition before/with children appearing.

Exact durations are not frozen here.

## 1.6 No uncontrolled recursive spawning/buff stacking
- SPLITTER children never split again.
- SUPPORTER aura does not stack multiplicatively/additively with another SUPPORTER aura of the same type.
- No ordinary archetype recursively generates another full-strength copy of itself.

This protects event volume, readability and deterministic simulation.

---

# 2. Capability matrix

| Archetype | Primary decision | Core capability | Main pressure axis | Explicit non-role |
|---|---|---|---|---|
| GRUNT | establish baseline | ordinary advance/contact | reference | no special mechanic |
| RUNNER | react sooner | sustained high movement | tempo | not a burst/dash unit |
| BRUTE | spend more control/damage | high HP + strong knock resistance | raw durability | no armor identity |
| SHIELD | overcome mitigated damage | flat armor reduction + moderate durability | mitigation | not just BRUTE with more HP |
| FLYER | read vertical geometry | authoritative Y movement/oscillation | spatial geometry | no armor/durability identity |
| CHARGER | interrupt/read a danger window | telegraph → burst dash | burst tempo | not continuously fast like RUNNER |
| SPLITTER | manage post-kill population | parent death → two non-splitting children | population transformation | not a generic swarm spawner |
| SUPPORTER | break/contain a moving formation | non-stacking nearby movement-speed aura | formation support | no healing / armor aura in V1 |
| SIEGER | stop repeated wall pressure | stop at standoff range → telegraphed wall attacks | objective pressure | does not need wall contact to attack |

---

# 3. Existing archetypes — structural contract

## 3.1 GRUNT — baseline/reference
State grammar:
`ADVANCE -> WALL CONTACT -> REMOVE`

Identity:
- default reference for HP, movement, knockback and wall-pressure comparisons.
- no armor, no stateful special action, no spawn-on-death behavior.

Purpose:
- keep mixed encounters readable,
- provide a neutral unit against which other archetypes are perceived.

Do not later give GRUNT hidden special behavior just to keep it relevant. Relevance should come from count, geometry, timing and combinations.

## 3.2 RUNNER — sustained tempo
State grammar:
`FAST ADVANCE -> WALL CONTACT -> REMOVE`

Identity:
- persistent speed pressure from spawn to wall.
- threat is reduced reaction time, not a discrete charge event.

Separation from CHARGER:
- RUNNER is **always fast**.
- CHARGER is **normally manageable, then temporarily much more dangerous after a telegraph**.

## 3.3 BRUTE — raw durability / control resistance
State grammar:
`SLOW ADVANCE -> WALL CONTACT -> REMOVE`

Identity:
- high raw HP,
- low movement speed,
- strong knockback resistance,
- no armor-based damage reduction as its defining mechanic.

Separation from SHIELD:
- BRUTE asks "can the team spend enough damage/control on one heavy body?"
- SHIELD asks "can the team handle reduced effective damage?"

## 3.4 SHIELD — mitigation
State grammar:
`ADVANCE -> WALL CONTACT -> REMOVE`

Identity:
- ordinary incoming damage is reduced by an armor multiplier.
- armor applies consistently through authoritative damage resolution.
- V1 does **not** require facing-angle simulation or directional shield arcs.

Legacy coefficient exists and may be used as a provisional/reference value, but the final 50-stage production calibration remains governed separately.

Interaction requirements:
- ordinary hit,
- AI hit,
- passive hit,
- Lv6 secondary,
- N3,
- future higher-level skill damage
must all pass through one explicit armor policy unless a skill is later approved to ignore armor.

## 3.5 FLYER — vertical/spatial geometry
State grammar:
`ADVANCE WITH AUTHORITATIVE Y MOTION -> WALL CONTACT -> REMOVE`

Identity:
- changes vertical position while advancing.
- pressure comes from geometry and target/line/AoE relationships, not from immunity.

Constraints:
- remains attackable by every class.
- no generic "ground attacks cannot hit" rule in V1.
- Y position and motion must be server-authoritative enough that Archer/Mage geometry cannot disagree between clients.

---

# 4. New archetypes — structural contract

## 4.1 CHARGER — telegraphed burst threat
Primary state machine:
`ADVANCE -> WINDUP -> CHARGE -> (WALL CONTACT | RECOVER/ADVANCE)`

Behavior:
1. advances at an ordinary/non-Runner pace,
2. when an authoritative trigger condition is reached, enters WINDUP,
3. WINDUP is visibly telegraphed,
4. if not interrupted, enters CHARGE with a large temporary movement increase,
5. after charge resolution, either contacts the wall or returns to a normal/recovery state if displaced/otherwise prevented.

Interrupt rule:
- authoritative knockback during WINDUP cancels the pending charge in V1.
- passive/no-knock effects do not count as an interrupt merely because they deal damage.
- exact interrupt threshold/cooldown may be introduced later if simulations show "any nonzero knockback" is too permissive.

Separation guardrail:
- never tune normal CHARGER movement so high that it becomes a second RUNNER.

Server-authoritative state:
- phase,
- windup start/end,
- charge start/end,
- charge movement multiplier,
- interrupt result,
- wall contact.

## 4.2 SPLITTER — population transformation
Primary state machine:
`PARENT ADVANCE -> PARENT DEATH -> SPLIT EVENT -> CHILD A + CHILD B -> normal child resolution`

Behavior:
- parent behaves as one ordinary target until killed.
- parent death spawns exactly **two** child entities in V1.
- children are subforms of SPLITTER, not a tenth/tenth+first roster archetype.
- children never split again.

Spawn semantics:
- child positions originate from the authoritative parent death position with deterministic bounded offsets.
- child creation is one server event/state transition, not a client cosmetic guess.

Economy/score guardrail:
- final reward and KILLS semantics are **not numerically frozen yet**.
- however, the authoring/balance model must account for the parent plus children as one authored threat package; SPLITTER must not become an unintended infinite/oversized coin or score farm.

Interaction requirements:
- if a parent dies from an AoE/secondary/N3 event, children still spawn deterministically.
- the attack that killed the parent does not retroactively hit children unless a future skill contract explicitly supports persistent-area effects.

Separation guardrail:
- SPLITTER is about a **death-triggered count change**, not sustained summoning.

## 4.3 SUPPORTER — formation-speed support
Primary state machine:
`ADVANCE -> AURA ACTIVE WHILE ALIVE -> WALL CONTACT/DEATH -> AURA REMOVED`

V1 aura:
- affects nearby eligible allied monsters' **movement speed only**.
- does not heal.
- does not grant armor.
- does not grant damage.
- does not grant knockback resistance.
- does not buff itself.
- multiple SUPPORTER auras of this same V1 type do **not stack** on one target.

Why speed-only:
- avoids duplicating SHIELD's armor identity,
- avoids duplicating BRUTE's control-resistance identity,
- produces visible formation pressure,
- works without requiring free/manual target selection.

Authoritative motion rule:
When a monster enters/leaves the aura or the SUPPORTER dies:
- materialize the affected monster at the transition timestamp,
- update the movement modifier,
- continue from that exact authoritative position.

This prevents server/client disagreement caused by changing speed on an old reference timestamp.

Targeting/readability guardrail:
SUPPORTER may be screened by other enemies, but encounters must not require manual backline selection. Its effect must remain survivable through normal target order, line penetration, AoE, knockback and encounter composition.

## 4.4 SIEGER — ranged wall/objective pressure
Primary state machine:
`ADVANCE -> ENTER SIEGE RANGE -> STOP -> WINDUP -> WALL ATTACK -> REPEAT / REPOSITION`

Behavior:
- advances toward the base like an ordinary monster,
- stops at an authoritative standoff distance before physical wall contact,
- visibly winds up,
- damages the wall from range,
- repeats on an attack cadence while alive and still in valid siege range.

Knockback interaction:
- knockback can push SIEGER out of valid siege range.
- if pushed out, it must leave attack/windup state and advance/reposition before it can attack again.

This gives control classes value without making them mandatory.

Server-authoritative state:
- siege-range membership,
- stopped/moving state,
- windup timing,
- wall-attack timing,
- wall damage event,
- interruption/reposition.

Separation guardrail:
- SIEGER is not just a BRUTE with higher wall damage.
- its identity is **repeated wall pressure before contact**.

---

# 5. Interaction policy with current combat systems

## 5.1 Armor
Only archetypes explicitly carrying armor use an armor multiplier.

In the current roster that identity belongs to SHIELD by default.
BRUTE durability should remain primarily HP + knock resistance unless a future elite recipe explicitly applies a temporary hardened package.

## 5.2 Knockback
All ordinary archetypes remain knockback-capable unless a later explicit boss/special contract says otherwise.

Knockback can additionally affect state machines:
- CHARGER: cancel WINDUP under the approved interrupt rule.
- SIEGER: force exit/reposition if displaced outside siege range.

## 5.3 Lv6 / N3 / future skills
Monster capabilities must be implemented below or within the common authoritative damage/geometry layer so that class skills do not need one-off hacks per stage.

Required compatibility tests for every new archetype/capability:
- normal human hit,
- passive,
- AI,
- Lv6 class secondary where geometrically applicable,
- N3,
- kill/reward/contribution,
- event delivery/reconnect.

## 5.4 Targeting
No new ordinary archetype introduces manual target selection in V1.

If future design requires explicit target switching, that is a separate core-combat decision and must not be smuggled in as a monster feature.

---

# 6. Capability overlap audit

## GRUNT vs RUNNER
Distinct: baseline vs persistent speed.

## RUNNER vs CHARGER
Distinct: continuously fast vs telegraphed temporary burst.

## BRUTE vs SHIELD
Distinct: raw HP/control resistance vs damage mitigation.

## FLYER vs CHARGER
Distinct: spatial/Y geometry vs temporal burst movement.

## SPLITTER vs Swarm recipes
Distinct: one authored entity transforms on death; Swarm is encounter-level spawn composition.

## SUPPORTER vs SHIELD/BRUTE
Distinct under V1 speed-only aura. Do not add armor/knock-resist aura without a new decision.

## SIEGER vs high wall-damage monster
Distinct: repeated ranged wall attack before contact vs one contact event.

Conclusion: the nine-archetype set covers nine useful pressure functions without requiring a tenth ordinary type at this stage.

---

# 7. Numerical status

## Frozen now
- roster membership: 9 ordinary archetypes,
- each primary role,
- each state-machine shape,
- CHARGER has telegraph + interruptible charge,
- SPLITTER creates exactly 2 non-recursive children,
- SUPPORTER V1 aura is movement-speed-only and non-stacking,
- SIEGER attacks the wall repeatedly from a standoff state,
- no hard class lockouts,
- server authority requirements.

## Not frozen now
- HP,
- base speed,
- armor coefficient for final campaign calibration,
- knock resistance,
- wall damage,
- reward,
- CHARGER trigger distance/windup/charge multiplier/cooldown,
- SPLITTER parent/child HP/speed/reward allocation,
- SUPPORTER aura radius/speed multiplier,
- SIEGER standoff range/windup/cadence/wall damage,
- tier introduction points,
- final stage compositions.

Existing legacy values may be used only as **reference/provisional test anchors**, not automatically promoted into final 50-stage production balance.

---

# 8. Next implementation boundary

Do **not** resume legacy Stage 4 -> Stage 10 reconstruction.

Next sequence:
1. build a monster-capability sandbox/harness independent of final stage numbering,
2. give the nine archetypes provisional test values clearly marked NOT BALANCE FROZEN,
3. implement/validate capabilities in small bounded slices,
4. retain v0.39 Stage 1–3 as regression fixtures,
5. implement remaining player-skill authority required for later calibration,
6. build the 50-stage tier/S-E-X authoring model,
7. run large deterministic simulation/calibration,
8. discuss and explicitly freeze production numbers,
9. perform targeted real-device readability tests only where automation cannot judge presentation.

Recommended capability implementation order:
- SHIELD / common armor layer,
- FLYER / authoritative Y geometry,
- CHARGER state machine,
- SPLITTER child-spawn kernel,
- SUPPORTER dynamic movement aura,
- SIEGER repeated wall-attack kernel.

This order moves from low architectural novelty to high novelty and minimizes debugging ambiguity.
