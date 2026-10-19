# Timing Defense — Next Work Boundary

## Current boundary after v3

Do **not** immediately change live numerical balance and do not treat a simulation gap as authorization to patch.

Required governance:

`simulate → identify intentional specialization vs model artifact vs actual defect → report → discuss → explicit decision → patch`

The latest v3 mastery-curve result was accepted as plausible enough to continue without a balance change.

## Immediate next validation slice

Run a **team-composition / co-op role simulation** using the currently frozen class identities and Stage 1–10 rules.

Required matrix:
- 2-player compositions
- 3-player compositions
- 4-player compositions
- repeated deterministic seeds so different class mixes face equivalent waves
- at minimum Average and Skilled local-player profiles

Primary questions:
1. Does Tank materially improve team survival/wall preservation without making a team effectively immortal?
2. Does Rogue's high-HP-normal deletion create real team value even though Rogue solo clear is low?
3. Do Archer + Mage overlap too much in crowd-clear value, or remain distinct through line-vs-density geometry?
4. Does Knight retain useful generalist value in mixed teams?
5. Do duplicated classes create obvious dominant compositions?
6. How much value comes from total extra DPS versus actual class-specific utility?

## Team-simulation modeling rules to document explicitly

- Archer penetration remains straight-line geometric only.
- Tank remains team-specialized; do not normalize it to solo DPS.
- Rogue same-target dagger hit cap remains absent.
- Boss dagger scalar remains 0.70 for the current test.
- Boss knockback scalar remains 0.40 for the current test.
- EXP philosophy remains unchanged.
- Local-player timing mastery should stay the principal skill variable.
- AI/teammate timing profiles and attack cadence must be stated explicitly so team results are not mistaken for real-network multiplayer balance.

## After team simulation

Report first. Do not patch.

If the team-role results are coherent, the next implementation candidate is still the first multi-skill block:
- Lv6 / Lv11 / Lv16 / Lv21 skills for all five classes.
- multi-skill HUD strip below Timing Square.
- exact straight-line Archer collision.
- boss resistance rules above.

After implementation, re-run the simulator using the exact implemented formulas and human-play only the suspicious stages/skills identified numerically.

## Later boundary

Only after the Lv6–21 block and its role validation close should the project proceed to:
- Lv26 skills
- Lv31 signature P×P CRITICAL finishers
- larger stage range
- permanent/meta-stat layer

## Human-play focus remains
Simulation does not replace checks for:
- impact feel / hitstop
- VFX readability
- Timing Square readability
- projectile visibility
- skill icon density
- whether the fourth attack feels meaningfully stronger
- subjective class fun
