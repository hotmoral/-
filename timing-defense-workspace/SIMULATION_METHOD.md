# Timing Defense — Headless Simulation Method

## Purpose
Use a renderer-free combat model to validate numerical balance much faster than manual play. The simulator is not a replacement for feel/UX testing.

## Mirrored prototype constants
- Monster HP, speed, wall damage, armor and knockback resistance.
- Stage 1–10 spawn counts and gaps.
- Timing damage tiers.
- EXP curve: `XP_next = 60 + 12 × (level - 1)`.
- Local knockback magnitudes by result tier.
- Current run-shop economy and upgrades.
- Five class skill kits through Lv21 for pre-implementation validation.

## Timing profiles
Baseline named profiles:
- Novice: NORMAL 45%, GOOD 45%, PERFECT 10%.
- Average: NORMAL 25%, GOOD 55%, PERFECT 20%.
- Skilled: NORMAL 10%, GOOD 50%, PERFECT 40%.
- Expert: NORMAL 3%, GOOD 32%, PERFECT 65%.

Each profile also uses a characteristic normal/heavy attack-cycle duration so player skill is not represented only by judgment probability.

Current Average cadence:
- normal cycle 1.14 s
- heavy cycle 1.68 s

Current Skilled cadence:
- normal cycle 1.04 s
- heavy cycle 1.54 s

## Frozen semantic decisions used after v2

### Archer
Penetration is true straight-line geometry only.
- no homing
- no auto-retarget
- no automatic next-enemy chain after a hit
- only enemies intersecting the projectile's straight path may be penetrated

The current headless geometric approximation uses a bounded Y-lane tolerance around the original arrow line. This is an approximation of hitbox-line intersection, not authority to turn penetration into chaining.

### Tank
Tank is team-specialized. Fresh-run solo Stage-10 parity is not required. A poor solo clear result is diagnostic information, not automatic evidence that Tank needs a buff.

### Rogue / bosses
- no same-target dagger hit cap
- boss dagger damage scalar starting value: 0.70
- boss knockback scalar starting value: 0.40

### EXP
EXP remains attached to timing attack results/events. Faster-clearing classes are allowed to level differently because they can perform fewer attack events.

## v1 role scenarios
1. High-HP normal duel — validates Rogue specialist role.
2. Boss duel — checks boss damage ordering and Rogue dagger resistance.
3. Straight-line pack — validates Archer penetration role.
4. Dense cluster — validates Mage density-scaling role.
5. Wall pressure — validates Tank wall-preservation/control role.

## v2 campaign extension
v2 added:
- Stage 1–10 full campaign
- kill coin rewards
- stage-clear rewards
- deterministic run-shop policies
- ATK / CRIT / CRIT DMG / WALL HP / DEF / KNOCKBACK effects
- Lv6 / Lv11 / Lv16 / Lv21 candidate skills

Shop policies used for robustness:
- balanced
- offense
- class-role-aware

v2 total deliberate analysis volume: 39,600 runs.

Important v2 outcome: permissive Archer next-target chaining was identified as a model artifact and rejected. Subsequent campaign interpretation uses straight-line geometry.

## v3 mastery-curve extension
v3 studies the transition from Average → Skilled rather than treating those as only two isolated points.

Nine evenly spaced interpolation points are used between:
- Average = N25 / G55 / P20, normal 1.14 s, heavy 1.68 s
- Skilled = N10 / G50 / P40, normal 1.04 s, heavy 1.54 s

Two variants are compared:
1. full mastery progression: accuracy + cadence both improve
2. accuracy-only diagnostic: judgment probabilities improve while cadence stays at Average

This separates "better timing precision" from "recognizes the window and commits faster".

v3 total deliberate analysis volume: 27,500 runs.

Latest interpretation:
- Knight / Archer / Mage show a useful mastery response.
- Rogue remains a solo-pressure specialist tradeoff and should be judged in team context next.
- Tank solo result is intentionally non-normative.
- Cadence is a substantial skill dimension in a real-time defense game.
- No live values were changed from v3.

See `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`.

## Deterministic comparison principle
When comparing classes or team compositions, reuse the same random seeds so monster composition, timing samples and encounter randomness remain comparable. Change the class/team configuration, not the underlying random world.

## Metrics
- Stage clear / failure.
- Stage reached.
- Wall HP and wall hits.
- Total damage.
- High-HP normal TTK.
- Boss TTK.
- Multi-hit event count.
- Skill damage contribution.
- Shield absorption.
- Level reached and level-after-stage profile.
- Attack count / run duration.
- Skill-unlock reach rate and stage.
- Shop-rank distribution.

## Balance-change rule
Simulation does not authorize a patch.

Required order:
1. identify a measured difference
2. determine whether it comes from role specialization, model abstraction/artifact, or an actual balance defect
3. report the result
4. discuss with the user
5. make an explicit design decision
6. only then change live gameplay values

## Next required extension
Add team-composition / co-op role simulation.

Required scope:
- 2-player / 3-player / 4-player compositions
- identical seeded waves across composition comparisons
- explicit teammate timing/AI assumptions
- Tank wall/control contribution
- Rogue high-HP-target contribution
- Archer line geometry vs Mage density geometry
- Knight generalist contribution
- duplicated-class composition checks

This extension is report-only until its results are discussed.
