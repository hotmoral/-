# Timing Defense — Headless Simulation Method

## Purpose
Use a renderer-free combat model to validate numerical balance much faster than manual play. The simulator is not a replacement for feel/UX testing.

## Mirrored prototype constants
- Monster HP, speed, wall damage, armor and knockback resistance.
- Stage 1–10 spawn counts and gaps.
- Timing damage tiers.
- EXP curve: `XP_next = 60 + 12 × (level - 1)`.
- Local knockback magnitudes by result tier.
- Five class skill kits through Lv21.

## Timing profiles
- Novice: NORMAL 45%, GOOD 45%, PERFECT 10%.
- Average: NORMAL 25%, GOOD 55%, PERFECT 20%.
- Skilled: NORMAL 10%, GOOD 50%, PERFECT 40%.
- Expert: NORMAL 3%, GOOD 32%, PERFECT 65%.

Each profile also uses a characteristic normal/heavy attack-cycle duration so better timing skill is not represented only by judgment probability.

## Scenario tests
1. High-HP normal duel — validates Rogue specialist role.
2. Boss duel — checks boss damage ordering and Rogue dagger resistance.
3. Straight-line pack — validates Archer penetration role.
4. Dense cluster — validates Mage density-scaling role.
5. Wall pressure — validates Tank wall-preservation/control role.

## Sensitivity tests
### Rogue boss dagger scalar
Tested values:
`0.60 / 0.65 / 0.70 / 0.75 / 0.80 / 0.85 / 1.00`

Current preferred starting value: `0.70`.

### Boss knockback scalar
Tested values:
`0.25 / 0.30 / 0.35 / 0.40 / 0.45 / 0.50 / 0.55`

Current preferred starting value: `0.40`.

## Monte Carlo v1 volume
- Campaign: 6,000 runs.
- Role scenarios: 7,500 runs.
- Sensitivity sweeps: 3,360 runs.
- Total: 16,860 runs.

## Deterministic comparison principle
When comparing classes, reuse the same random seeds so monster composition, timing samples and encounter randomness remain comparable. Change the class, not the underlying random world.

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

## Current limitation
The first campaign model intentionally disables run-shop upgrades. Therefore its clear rates are a warning signal only and must not be used as final solo-difficulty targets.

## Required v2 extension
Add a deterministic shop policy that purchases run upgrades from the same coin economy as the playable prototype. Then validate full Stage 1–10 viability and level timing before expanding toward Stage 50.
