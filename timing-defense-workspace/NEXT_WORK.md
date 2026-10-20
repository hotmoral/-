# Timing Defense — Next Work Boundary

## Current boundary after v0.16 source implementation

Do **not** change numerical balance merely because the new skills feel strong or weak on first inspection.

Required governance:
`implement → smoke-test → extract exact formulas → simulate → identify specialization/artifact/defect → report → discuss → explicit decision → numerical patch`

## v0.16 source state
Implemented on `timing-defense-live-v011` at:
`caa7e249f4b52aa3b6215ff2677b0c4973f3eb17`

Files:
- `timing-defense-v011/v016-core.js`
- `timing-defense-v011/v016-ui.js`
- `timing-defense-v011/v016-render.js`
- `timing-defense-v011/v016.html`

Implemented mechanics:
- Lv6 / Lv11 / Lv16 / Lv21 for all five classes,
- six-slot HUD reserving Lv6/11/16/21/26/31,
- exact straight-line Archer penetration geometry,
- boss dagger scalar 0.70,
- boss knockback scalar 0.40,
- Mage Lv16 center-excluding Resonance,
- Tank Lv11 wall reduction 10%,
- Tank Lv16 80/3s refresh-only shield,
- class-specific Lv21 heavy transformations.

Node syntax checks and loader dependency checks passed.

## Deployment boundary
Render service is configured with `autoDeploy=yes` on the live branch.

At the latest check, Render had **not yet exposed a new deploy after v0.16 source commits**; v0.15 remained the newest observed public deployment.

Therefore:
- do not claim v0.16 public-live yet,
- do not trigger duplicate deployment while auto-deploy remains enabled,
- first re-check Render deployment state.

## Immediate next execution slice

### 1. Public deployment confirmation
Confirm a Render deployment containing `caa7e249...` or a later v0.16 commit.

### 2. Smoke test only
Check:
- page/runtime load,
- six-slot HUD fit,
- each class's Lv11/Lv16/Lv21 execution,
- Archer line collision,
- Tank shield lifecycle,
- Rogue five-dagger heavy,
- Mage Resonance center exclusion,
- Lv21 heavy visual readability.

Fix implementation defects if found. Do not tune class coefficients at this stage.

### 3. Exact-formula simulation refresh
After smoke closure:
- mirror exact v0.16 formulas into the headless simulator,
- rerun `PRESSURE_RECIPES_V1`,
- 2P/3P/4P,
- Average and Skilled,
- same seeds / same stage grammar,
- measure clear rate, wall HP, target-type contribution, mastery response, role rotation and short-window pressure.

### 4. Report before rebalance
Any large discrepancy must be classified as:
- intended role specialization,
- implementation/model artifact,
- or actual balance defect.

Only then discuss a numerical change.

## Accepted encounter state remains unchanged
Pressure grammar:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Rules:
- X is the main co-op scaling language,
- S/E are timed spikes,
- 1/2/3-pattern stages are all valid,
- all three families are not required every stage,
- higher tier does not automatically mean more pattern types,
- geometry/timing/internal ratios are gameplay data.

Current candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

Current candidate P95 4-second spawn density:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

Do not tune these again until the exact v0.16 simulation rerun exists.

## Still not frozen
- literal final E HP/armor package,
- final X hardened multipliers,
- exact stage duration,
- final tier number/names/order,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- true human multiplayer cadence/network behavior,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients.

## Later boundary
Only after v0.16 smoke + exact-formula re-simulation close:
- decide whether co-op pressure needs numeric adjustment,
- then proceed to Lv26/Lv31 signature skills,
- larger stage/tier production authoring,
- permanent/meta-stat layer.
