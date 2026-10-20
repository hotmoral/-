# Timing Defense — v0.16 Multi-Skill Implementation Report

Date: 2026-10-20 KST
Status: **SOURCE IMPLEMENTED / PUBLIC DEPLOY AUTO-TRIGGER NOT YET OBSERVED AT REPORT TIME**

## Live-source branch
- Repository: `hotmoral/-`
- Branch: `timing-defense-live-v011`
- v0.16 source HEAD: `caa7e249f4b52aa3b6215ff2677b0c4973f3eb17`
- Loader: `timing-defense-v011/v016.html`
- Patch files:
  - `timing-defense-v011/v016-core.js`
  - `timing-defense-v011/v016-ui.js`
  - `timing-defense-v011/v016-render.js`

v0.15 is preserved unchanged as the rollback/stable version.

## Implemented scope

### Common
- Automatic skill milestones: Lv6 / Lv11 / Lv16 / Lv21, while the six-slot HUD also reserves Lv26 / Lv31 positions.
- The old single learned-skill icon is replaced in v0.16 by a compact six-slot horizontal strip below the Timing Square.
- Newly reached skill slots pulse temporarily; permanent skill-name text remains absent.
- Existing Timing Square / EXP / charge hierarchy is preserved.

### Knight
- Lv6: +12% blade-wave damage; existing enhanced-wave presentation retained.
- Lv11: normal blade wave can hit one additional nearby-forward enemy at 85%; heavy can hit two additional enemies.
- Lv16: attacks whose actual timing inputs contain PERFECT gain +18% damage and +20% knockback.
- Lv21: heavy damage +20%, larger signature wave VFX, up to three additional penetrations.

### Rogue
- Lv6: second dagger = 55% of main hit.
- Lv11: +6 percentage points native proc-crit chance.
- Lv16: an attack containing PERFECT shortens the next recovery from 390 ms to 312 ms (20%).
- Lv21: heavy becomes five daggers total: main 100% + four 45% follow-ups.
- Same-target dagger hits remain uncapped.
- Bosses take 70% dagger damage.

### Tank
- Lv6: knockback ×1.30; enhanced shockwave presentation retained.
- Lv11: wall incoming damage -10% while the local player is Tank; non-stacking by construction in the current local-player model.
- Lv16: an attack containing PERFECT refreshes an 80-point wall shield for 3 s; value/duration refresh, no stacking.
- Lv21: heavy becomes Ground Impact with broad nearby multi-target coverage and ×2.0 Tank heavy knockback.
- Boss knockback is globally scaled to 40% of normal.
- Temporary wall-shield HUD/VFX added.

### Archer
- Lv6: up to two additional penetration targets.
- Penetration now uses actual straight-line geometry: projection along the fired line plus a monster-size hit corridor; no homing, retarget chain or next-enemy-by-X shortcut.
- Pre-Lv16 secondary penetrations retain the known live 52% damage coefficient.
- Lv11: projectile travel time reduced by 25% equivalent speed increase; base damage +10%.
- Lv16: attacks containing PERFECT ignore armor and preserve 100% damage through penetration.
- Lv21: heavy becomes three arrows: 100% + 65% + 65%, with separated parallel trajectories.

### Mage
- Lv6: splash = 50% around the impact target.
- Lv11: splash radius +35%, splash damage 60%.
- Lv16: attacks containing PERFECT schedule a second 55% outer-ring Resonance after ~180 ms; original center target is explicitly excluded.
- Lv21: heavy damage +20%, explosion radius ×1.6, slightly slower/larger Greater Arcane Orb presentation.

## Implementation method
v0.16 is layered on top of v0.15 rather than rewriting the stable base:

`index/v0.13 runtime → v0.14 UI/combat/character → v0.15 palette → v0.16 core/UI → v0.14 render → v0.16 render overlay`

This preserves rollback and limits regression surface.

## Validation completed
- `node --check` PASS for `v016-core.js`.
- `node --check` PASS for `v016-ui.js`.
- `node --check` PASS for `v016-render.js`.
- Loader dependency check PASS.
- GitHub live branch confirmed at source HEAD `caa7e249...`.

## Deployment status boundary
Render service reports `autoDeploy=yes` on branch `timing-defense-live-v011`.

At report time the latest Render deployment list still showed v0.15 commit `4ce695f...`; no new automatic deployment had appeared yet. Because auto-deploy is enabled, no duplicate manual deployment was triggered.

Therefore do **not** claim v0.16 public URL is live until Render shows a deployment containing `caa7e249...` or a later v0.16 commit.

## Important validation caveat
Source/syntax validation is not visual/device validation. After public deployment appears, verify:
- page loads without console/runtime errors,
- six skill slots fit below Timing Square on target landscape sizes,
- each class can naturally unlock and execute Lv11/Lv16/Lv21 behavior,
- Archer straight-line penetration does not bend toward off-line enemies,
- Tank shield absorbs wall damage and expires correctly,
- Rogue barrage preserves repeated impacts,
- Mage Resonance excludes the original center target,
- Lv21 heavy VFX remains readable under monster overlap.

## Next boundary after public smoke test
1. fix implementation defects only; do not rebalance merely from first impressions,
2. extract exact v0.16 formulas into the headless simulator,
3. rerun `PRESSURE_RECIPES_V1` with exact implementation behavior,
4. report role/mastery/co-op differences before numerical balance changes,
5. human-play suspicious pressure windows only.
