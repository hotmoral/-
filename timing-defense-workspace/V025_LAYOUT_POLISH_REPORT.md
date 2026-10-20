# Timing Defense v0.25 — Character Select Vertical/Layout Polish

Updated: 2026-10-20 KST

## Public build
- URL: `https://timing-defense-v011.onrender.com/v025.html`
- Live source HEAD: `fce42eb1261ff43277c27d844617b96a546d6d1a`
- Render deploy: `dep-dbbga8c9v7es73f567b0` / LIVE

## Trigger
Android screen recording showed that v0.24 technically reduced header heights, but on the real browser/device the brand + nickname region still consumed too much vertical space. The character-selection panel therefore did not feel materially taller, while the left radar labels and class copy were too small/sparse.

## v0.25 changes
### Vertical reclaim
- Lobby top header reduced again.
- Nickname row compressed and moved upward.
- Footer reduced.
- Recovered height is assigned to the carousel/profile area.
- Center hero max visual height increased.

### Left combat profile
The left panel now restores the richer class identity hierarchy:
- COMBAT PROFILE label,
- Korean class name,
- large English class name,
- class tag,
- animated 5-level / 6-axis radar,
- concise role line,
- fuller one-sentence play-style description.

Radar axes remain frozen:
`공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`.

Profiles remain unchanged:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

### Radar readability/animation
- Axis labels increased substantially.
- Five-ring web retained.
- Center-out scan retained.
- Six vertices grow with staggered timing.
- Class-color fill/glow retained.
- Node landing pulses and final ripple retained.
- Stale animation is cancelled when class changes.

### Right skill area
The v0.24 `3 × 2` six-card layout remains.
The extra vertical height is used to slightly increase card/icon/text breathing room rather than returning to a one-line strip.

## Non-goals
- No combat damage/crit/HP/passive/combo changes.
- No projectile travel-time change.
- No networking implementation.

## Device validation target
Verify on the same Android landscape/browser:
1. selection panel clearly occupies more vertical area,
2. top whitespace is materially reduced,
3. radar labels are readable without squinting,
4. class description feels informative again,
5. hero remains centered and does not collide with the skill panel,
6. 3×2 skill cards remain readable.
