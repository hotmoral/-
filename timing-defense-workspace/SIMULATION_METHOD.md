# Timing Defense — Headless Simulation Method

## Purpose
Use a renderer-free combat model to validate numerical balance much faster than manual play. The simulator is not a replacement for feel/UX testing.

## Mirrored prototype constants
- Monster HP, speed, wall damage, armor and knockback resistance.
- Stage 1–10 spawn counts and gaps.
- Timing damage tiers.
- EXP curve: `XP_next = 60 + 12 × (level - 1)`.
- Local knockback magnitudes by result tier.
- Current run-shop economy and upgrades where the test specifically includes shop modeling.
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

## Frozen semantic decisions

### Archer
Penetration is true straight-line geometry only.
- no homing
- no auto-retarget
- no automatic next-enemy chain after a hit
- only enemies intersecting the projectile's straight path may be penetrated

The headless geometric approximation uses a bounded lane/hitbox tolerance around the original arrow line. This approximates line-hitbox intersection and is not authority to turn penetration into chaining.

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

v3 total deliberate analysis volume: 27,500 runs.

Latest v3 interpretation:
- Knight / Archer / Mage show a useful mastery response.
- Rogue remains a solo-pressure specialist tradeoff and should be judged in team context.
- Tank solo result is intentionally non-normative.
- Cadence is a substantial skill dimension in a real-time defense game.
- No live values were changed from v3.

See `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`.

## v4 team-composition extension

v4 adds team-role validation.

### Primary matrix
- 2-player / 3-player / 4-player compositions.
- Average and Skilled human timing profiles.
- same seed sets reused across class mixes where applicable.
- current Stage 1–10 unscaled wave counts/gaps for the main saturation check.

### Important boundary
v4 intentionally excludes run-shop upgrades because true multiplayer economy ownership / shared-vs-individual purchase rules are not frozen. Therefore v4 absolute clear rates should not be compared one-to-one with v2/v3 shop-enabled solo campaign results.

v4 is used to study:
- composition ordering,
- marginal class contribution,
- Tank defensive value,
- Rogue durable-normal specialization,
- Archer/Mage geometry separation,
- Knight generalist value,
- duplicate-class stacking,
- whether current waves saturate at larger team sizes.

### Role diagnostics
Additional fixed-level Lv21 stress scenarios are allowed to expose class utility that current Stage 1–10 pressure may hide. These diagnostics are not live difficulty proposals.

Examples:
- hard mixed wall pressure,
- durable-normal waves,
- long straight-line packs,
- dense clusters.

### v4 volume
Total deliberate v4 analysis volume: **13,780 runs**.

### v4 interpretation
- Tank shows measurable team defensive value under meaningful pressure.
- Rogue shows disproportionate durable-normal execution value in team mixes.
- Archer wins long-line geometry while Mage wins dense-cluster geometry.
- Knight remains a strong stabilizing generalist.
- current Stage 1–10 waves saturate at 3–4 players and cannot serve as final co-op difficulty targets.
- double-Knight stacking is flagged for re-test after exact playable Knight penetration geometry exists.
- no live values were changed from v4.

See `BALANCE_SIM_REPORT_V4_TEAM.md`.

## Deterministic comparison principle
When comparing classes or team compositions, reuse the same random seeds so monster composition, timing samples and encounter randomness remain comparable. Change the class/team configuration, not the underlying random world.

## Metrics
- Stage clear / failure.
- Stage reached.
- Wall HP and wall hits.
- Total damage.
- High-HP normal TTK / kill share.
- Boss TTK / boss damage share.
- Multi-hit event count.
- Skill damage contribution.
- Shield generation / absorption.
- Level reached and level-after-stage profile.
- Attack count / run duration.
- Skill-unlock reach rate and stage.
- Shop-rank distribution when shop is part of the model.
- per-class team damage and target-type contribution.

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
Do not invent final co-op scaling yet.

First discuss and freeze the team-size pressure philosophy:
- more enemies,
- tougher enemies,
- mixed count + HP,
- or additional elite/special threats.

Then build v5 around that philosophy and compare 2/3/4-player compositions before any live difficulty patch.
