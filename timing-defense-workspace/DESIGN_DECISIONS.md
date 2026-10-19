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
Tank is not required to win DPS comparisons.
Bosses receive reduced knockback because of mass:
- Boss knockback scalar initial value: `0.40`.
- Bosses are not fully knockback-immune.

### Archer
Straight-line penetration / rear-target access / long-range pressure.
Archer should outperform Rogue when enemies are arranged in a line, while Rogue should outperform Archer against one very durable normal enemy.

### Mage
Area damage / dense-pack deletion / chained explosions.
Mage should scale with enemy density and should not become a top single-target boss killer.

## Balance principle
Do not normalize every class to identical DPS. Balance by role value:
- Rogue: high-HP normal target TTK
- Archer: line-pack clear and strong boss pressure
- Mage: dense-cluster clear
- Tank: wall preservation / control
- Knight: general-purpose consistency

## Boss resistance philosophy
Boss resistance is not a class shutdown mechanic. It exists only to prevent a specialist from becoming the universal best answer.

Current starting values:
- Rogue dagger damage vs boss: `70%`
- Tank knockback vs boss: `40%`

These remain tuning values and may move after automated and human validation.

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
