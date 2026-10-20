# Timing Defense — v0.24 Radar / Readability Report

Updated: 2026-10-20 KST

## Public build
- Page: `https://timing-defense-v011.onrender.com/v024.html`
- Live source HEAD: `61ad74d833148d409dc65292f302bb9086c4e7c9`
- Render deploy: `dep-dbbg528m7kps73esejbg` / LIVE

## Scope
v0.24 is a UI/readability patch. It does **not** change combat-balance coefficients and does not change projectile travel-life values.

## Character-selection layout
The three-zone landscape layout is retained but rebalanced:
- left = animated combat-profile radar,
- center = larger/taller hero presentation,
- right = six skill cards in a `3 × 2` grid.

The center hero gets more vertical space by reducing header/nickname/footer height on short landscape displays. Navigation arrows move closer to the hero.

## Radar chart
Approved six axes:
`공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`.

Five visual levels are rendered as five concentric hexagonal rings. Numeric 1–5 values are not printed in the player UI.

Approved values:
- Knight `4 / 2 / 3 / 3 / 4 / 2`
- Rogue `2 / 5 / 5 / 1 / 1 / 1`
- Tank `2 / 1 / 1 / 5 / 1 / 3`
- Archer `3 / 2 / 4 / 1 / 5 / 2`
- Mage `4 / 2 / 2 / 1 / 1 / 5`

Animation:
- center-out scan,
- staggered six-vertex growth,
- class-color polygon fill + glow,
- vertex landing pulses,
- short settling pulse,
- total animation roughly one second.

See `CHARACTER_PROFILE_RADAR_V1.md` for the canonical profile contract.

## Skill roadmap
The previous icon-strip + selected-detail layout is replaced by six direct skill cards in a `3 × 2` grid.
Each card includes icon, name, unlock level, and description. This removes the single-row crowding and frees more visual space for the hero.

## TEAM lineup
- Bottom SUMMARY block is removed.
- TEAM LINEUP gets more horizontal width.
- Each AI class selector uses a 3-column grid, naturally wrapping five class choices into two rows.
- AI rows gain vertical height rather than clipping class labels.
- TEAM still reserves at least one human slot; AI FILL max remains +2.

## Rogue HUD identity
Rogue combat HUD changes from the v0.23 red/silver accent to a charcoal/black + silver identity:
- Timing Square outline,
- 1–3 charge pips,
- charge/heavy label,
- EXP gauge,
- level/EXP labels,
- `+EXP N` popup.

This is presentation-only; Rogue combat coefficients are unchanged.

## Projectile visibility
Natural scenery made several projectiles visually too faint/fast.
v0.24 keeps existing travel timing but adds a second readability pass over projectile visuals:
- deeper class-color silhouettes,
- brighter contrast edge/core,
- stronger short trails,
- stronger local-player alpha,
- class-specific high-contrast rendering.

Class direction:
- Knight: deep amber outline + bright gold inner blade.
- Rogue: charcoal blade + silver edge/trail.
- Tank: dark navy shockwave + cyan inner edge.
- Archer: forest-green shaft/trail + pale edge.
- Mage: deep purple orb/trail + pale violet ring.

Do not slow projectiles numerically unless device validation shows visibility remains insufficient after this contrast/trail pass.

## Validation focus
1. Radar labels must not clip on short Android landscape.
2. Radar animation should replay cleanly on every class switch and not stack old animation frames.
3. Center hero must no longer visually collide with the right skill panel.
4. All six skill descriptions must remain readable in 3×2.
5. TEAM lineup class controls must show all five choices without clipping.
6. Rogue HUD must read as black/charcoal, not red.
7. Projectiles should be recognizable as objects rather than only brief blur streaks.
8. If projectile visibility still fails, discuss whether a small travel-time change is warranted before applying it.
