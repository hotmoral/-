# Timing Defense — v0.16 Multi-Skill Implementation Report

Updated: 2026-10-20 KST  
Status: **IMPLEMENTED + DEPLOYED LIVE**

## Public deployment
- Public URL: `https://timing-defense-v011.onrender.com/v016.html`
- Live source branch: `timing-defense-live-v011`
- Final v0.16 source HEAD at this report boundary: `b8b823742bd5fb16026090045cd347feb0f9275e`
- Render deploy: `dep-dbbb6pom7kps73ebd0eg`
- Render status: `live`
- Finished: `2026-10-20T00:19:08Z`

v0.15 remains preserved as the previous rollback/stable page.

## Files
- `timing-defense-v011/v016.html`
- `timing-defense-v011/v016-core.js`
- `timing-defense-v011/v016-ui.js`
- `timing-defense-v011/v016-render.js`

## Implemented growth scope
Automatic skill milestones now function at:
`Lv6 / Lv11 / Lv16 / Lv21`

The HUD reserves all six long-term positions:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.

A compact six-slot strip sits below Timing Square. Newly unlocked slots pulse temporarily; permanent skill-name text is still omitted.

## Class implementation through Lv21

### Knight
- Lv6: +12% blade-wave damage.
- Lv11: normal +1 penetration at 85%; heavy +2 penetration targets.
- Lv16: attacks containing PERFECT gain +18% damage and +20% knockback.
- Lv21: heavy +20%, large blade-wave presentation, up to 3 extra penetrations.

### Rogue
- Lv6: second dagger = 55%.
- Lv11: +6 percentage points native proc-crit chance.
- Lv16: PERFECT-containing attack changes recovery from 390 ms to 312 ms.
- Lv21: five daggers total = main 100% + four 45% follow-ups.
- repeated hits on one target remain uncapped.
- boss dagger damage scalar = 0.70.

### Tank
- Lv6: knockback ×1.30 with enhanced shockwave presentation.
- Lv11: wall incoming damage -10% for local Tank; non-stacking in current model.
- Lv16: PERFECT refreshes 80 wall shield / 3 s / no stacking.
- Lv21: Ground Impact broad multi-target heavy, Tank heavy knockback ×2.0.
- boss knockback scalar = 0.40.

### Archer
- Lv6: up to 2 additional penetrations.
- pre-Lv16 penetration damage uses the current 52% secondary coefficient.
- Lv11: projectile speed +25%, base damage +10%.
- Lv16: PERFECT-containing arrow ignores armor and preserves 100% penetration damage.
- Lv21: triple shot = 100% + 65% + 65%.

### Mage
- Lv6: 50% splash.
- Lv11: radius +35%, splash 60%.
- Lv16: PERFECT schedules ~180 ms delayed 55% outer-ring Resonance; original center target excluded.
- Lv21: heavy +20%, blast radius ×1.6, larger/slightly slower Greater Arcane Orb.

## Important Archer semantic defect found and fixed

Initial v0.16 made *penetration selection* straight-line geometric, but inherited the generic projectile fallback:

`dead original target -> nearestMonster() retarget`

This could make Lv21 side arrows bend toward an off-line target, which violated the frozen Archer identity.

Fixed in commit:
`b8b823742bd5fb16026090045cd347feb0f9275e`

Final rule:
- Archer trajectory locks at launch.
- Archer projectiles do not retarget or bend after launch.
- if the intended target disappears, only a live hitbox intersecting the locked path can become the primary impact.
- all subsequent penetration remains on that same geometric line.

This was an implementation-fidelity fix, **not a numerical balance patch**.

## Validation completed
- `node --check` PASS for v0.16 JS files before deployment.
- final Archer-lock `v016-core.js` syntax PASS.
- loader dependency check PASS.
- Render final deployment PASS / LIVE at exact fix commit.
- exact-formula headless re-run completed after implementation; see `BALANCE_SIM_REPORT_V7_V016_EXACT.md`.

## Validation caveat
Render LIVE proves the built static source is published; it does not by itself prove visual/device behavior. Direct browser-render inspection was not available in the current tool lane.

Human/device checks still required for:
- six-slot strip fit/readability,
- Lv21 VFX overlap,
- visually straight Archer paths with off-line enemies nearby,
- Tank shield expiry/absorption feel,
- Mage Resonance center exclusion readability,
- repeated Rogue dagger impact feel.

## Balance governance
No numerical class coefficient was changed in response to v7 performance differences.

Required sequence remains:
`measure -> explain -> report -> discuss -> explicit decision -> numerical patch`.
