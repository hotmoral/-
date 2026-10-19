# Timing Defense — Next Work Boundary

## Immediate next implementation slice
Implement the validated first growth block in the playable prototype:
- Lv6 / Lv11 / Lv16 / Lv21 skills for all five classes.
- Rogue boss dagger damage scalar = 0.70.
- Boss knockback scalar = 0.40.
- Mage Lv16 Resonance = outer-ring second explosion that does not re-hit the original center target.
- Tank Lv11 wall damage reduction = 10%.
- Tank Lv16 wall shield = 80 for 3 s, refresh-only and non-stacking.

## HUD change required with multi-skill growth
The current single learned-skill icon below Timing Square must evolve into a compact horizontal skill strip. It should light one slot at each unlock level. Do not place skill-name text permanently beside the EXP gauge.

## Validation after implementation
1. Re-run role scenarios using the exact implemented formulas.
2. Add deterministic run-shop purchasing policy to the headless simulator.
3. Re-run Stage 1–10 campaign across novice / average / skilled / expert timing profiles.
4. Measure clear rate, wall HP, level timing, shop economy, stage TTK and role separation.
5. Human-play only the suspicious stages/levels identified by simulation.

## Only after this closes
Proceed to Lv26 / Lv31 skills and signature P×P CRITICAL finishers.

## Things not yet numerically frozen
- Exact Lv26 and Lv31 coefficients.
- Final shop policy and upgrade purchase heuristic for automated campaign tests.
- Final Stage 1–10 difficulty and economy.
- Final boss resistance values after playable implementation verification.

## Human-play focus
Simulation does not replace checks for:
- impact feel / hitstop
- VFX readability
- Timing Square readability
- projectile visibility
- skill icon density
- whether the fourth attack feels meaningfully stronger
- subjective class fun
