# Timing Defense — Design Decisions

## Core combat
- Primary input is timing, not free movement.
- Timing result must create immediate visible combat consequence.
- One square, four-attack rhythm: `X → X → X → X+Y`.
- Fourth attack is charged/heavy and should feel substantially more energetic than attacks 1–3.
- P×P on the heavy attack produces CRITICAL.
- Tap-anywhere input remains the intended control model.

## Class roles
The classes must differ by the combat problem they solve, not only by DPS coefficients.

### Knight
Generalist / stable frontline damage / penetration / strong heavy attack.
Should be consistently good without owning every specialist benchmark.

### Rogue
Fast multihit / crit / high-HP normal-enemy execution.
Rogue is allowed to delete BRUTE-like high-HP normal enemies faster than other classes.
Do NOT cap repeated dagger hits on the same target; repeated impacts are core to Rogue feel.

Boss balancing rule instead:
- Boss dagger damage scalar initial value: `0.70`.
- All dagger visuals and hit events still occur.
- Resistance reduces final HP loss, not the number of hits.

### Tank
Knockback / wall protection / battlefield control.
Tank is explicitly a team-specialist class and is NOT required to have solo Stage-10 clear performance comparable to the damage-oriented classes at fresh-run power.
A future permanent-stat/meta-progression layer may eventually make solo completion practical without changing Tank's team identity.
Tank is not required to win DPS comparisons.
Bosses receive reduced knockback because of mass:
- Boss knockback scalar initial value: `0.40`.
- Bosses are not fully knockback-immune.

### Archer
Straight-line penetration / rear-target access / long-range pressure.
Archer penetration is geometric and strictly line-based:
- The arrow continues only on its current straight trajectory.
- Only enemies whose hitboxes intersect that trajectory may be penetrated.
- No auto-retarget, steering, homing, or "next enemy" chaining after a hit.
Archer should outperform Rogue when enemies are arranged in a line, while Rogue should outperform Archer against one very durable normal enemy.

### Mage
Area damage / dense-pack deletion / chained explosions.
Mage should scale with enemy density and should not become a top single-target boss killer.

## Balance principle
Do not normalize every class to identical DPS or identical solo clear rate. Balance by role value:
- Rogue: high-HP normal target TTK
- Archer: line-pack clear and strong boss pressure
- Mage: dense-cluster clear
- Tank: wall preservation / control / team utility
- Knight: general-purpose consistency

## Player-skill model and difficulty philosophy
The current simulation profile named `Skilled` means approximately:
- NORMAL 10%
- GOOD 50%
- PERFECT 40%

This corresponds to about 90% GOOD-or-better timing and approximately 16% P×P CRITICAL on heavy attacks before other considerations.
This is considered a plausible learned-player state rather than an extreme expert-only state. The design should leave visible room for players to improve from Average toward Skilled, and it is acceptable if the Stage-10 results become much better once that level of timing consistency is reached.
Do not automatically nerf classes merely because Skilled players perform strongly.

Latest v3 mastery-curve interpretation:
- The strong performance rise from Average toward Skilled is intentional and desirable as a player-mastery reward, not automatically a difficulty defect.
- Skilled play includes both better judgment accuracy and somewhat faster recognition/commitment to the timing window.
- A modest cadence improvement can materially improve defense survival because enemies advance continuously in real time.
- The user expects players to reach this Skilled state relatively quickly, so the game should preserve clear room to learn rather than flatten the mastery curve prematurely.

## Experience progression
Keep the current experience acquisition philosophy:
- EXP is awarded from timing attack results / attack events as currently designed.
- Do not compensate a strong class merely because it kills faster and therefore performs fewer attack events.
- The resulting difference in level-up pace is accepted as part of overall class/run balance unless later evidence shows a concrete progression failure.

## Boss resistance philosophy
Boss resistance is not a class shutdown mechanic. It exists only to prevent a specialist from becoming the universal best answer.

Current starting values:
- Rogue dagger damage vs boss: `70%`
- Tank knockback vs boss: `40%`

These remain tuning values and may move after automated and human validation, but no balance patch should be applied solely because a simulation exposes a performance gap. Report the gap, identify its cause, and discuss it before changing live balance.

## Balance-change governance
Simulation is diagnostic first.
- A large class-performance difference is not by itself authorization to patch.
- First determine whether the difference is intentional role specialization, a simulation-model artifact, or an actual balance defect.
- Report the result and discuss the design implication before changing gameplay values.
- Playable/live code must remain unchanged until the balance decision is explicitly agreed.

## UI hierarchy
- Charge stack stays above Timing Square.
- Learned skill icons stay below Timing Square.
- EXP gauge stays immediately right of Timing Square.
- Do not keep permanent skill-name text beside EXP because it overlaps EXP gain feedback.
- Timing Square must render above monsters.

## Class color language
- Knight: gold / bright steel
- Rogue: charcoal / silver / minimal red accent
- Tank: blue / dark steel
- Archer: green
- Mage: purple

The same palette propagates into character clothing, weapons, projectiles, Timing Square, EXP gauge, skill icon and impact VFX.
