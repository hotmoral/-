# Timing Defense — v0.23 Lobby / Readability Polish Report

Date: 2026-10-20 KST
Status: **PUBLIC LIVE**

## Public build
- URL: `https://timing-defense-v011.onrender.com/v023.html`
- Live branch: `timing-defense-live-v011`
- Live HEAD: `6a7a4acafda9fe7dc405455c73adc3d7065f1285`
- Render deploy: `dep-dbbfierrjlhs73e3mfeg` / LIVE

## Scope
v0.23 is a UI/readability/entry-flow polish slice. It does **not** change passive, combo, monster HP, class damage, shop or EXP coefficients.

## Character selection re-layout
The v0.22 card that placed character left and six skill cards right was replaced with a landscape-oriented three-zone hierarchy:
- left = class identity / Korean name / role / play-style summary,
- center = the only horizontally sliding character hero,
- right = six skill icons + one selected skill detail panel.

Arrow buttons and horizontal swipe remain the class navigation methods.

The fixed information wings update whenever the centered character changes. Skill details no longer rely on truncated two-line cards.

## Skill roadmap
All six milestones remain visible together:
`Lv6 / 11 / 16 / 21 / 26 / 31`.

Each icon is selectable and reveals the full skill name, level and non-truncated description.
The v0.22 mechanic-specific icon drawings are reused rather than replaced with generic symbols.

## Character prototype art
Small second-pass geometric detail accents were added to the five hero canvases to improve limb/gear/silhouette separation while keeping the current vector prototype art direction.

## Rogue contrast fix
The natural battlefield made Rogue's gray/silver Timing Square and charge pips too weak.
v0.23 adds a combat-HUD-only brighter red/silver accent for Rogue:
- square edge receives a red contrast accent,
- active charge pips become bright red,
- inactive pips get a brighter neutral fill.

This does not change Rogue projectile/damage coefficients or the charcoal/silver/red class identity.

## EXP feedback fix
A separate v0.23 EXP-pop state is armed on **every valid local `awardXP(amount)` event**.
The existing gauge still displays level/progress, but `+EXP N` is now independently redrawn beside the gauge for every valid gain, including gains between level-ups.

Lower-left EXP float remains suppressed.

## TEAM slot rule
TEAM mode must reserve at least one slot for another human participant.
Therefore:
- `+3 AI` remains available in SOLO,
- `+3 AI` is hidden/disabled in TEAM,
- switching to TEAM while +3 AI was selected automatically falls back to +2 AI,
- TEAM label uses `AI FILL` semantics.

This is a lobby rule, not real multiplayer networking. FRIEND/LINK/RANDOM are still front-end choices only.

## AI setup readability
AI class controls now use compact class glyph + short label instead of only `K/R/T/A/M` initials:
- KNI
- ROG
- TNK
- ARC
- MAG

Settings rows/spacing were compressed so SOLO +3 AI and TEAM options fit better on short landscape screens without the previous obvious summary clipping.

## Result board
v0.23 redraws the end-run team table as the final canvas layer with:
- centered larger board,
- more deliberate row spacing,
- smaller class subtitle under the player name,
- stable metric columns,
- rank medal alignment preserved,
- local nickname used instead of hard-coded `YOU` when available.

Metrics remain:
KILLS / DMG / COIN / LV / MAX COMBO.

## Debug cleanup
The battle top-line `CLASS · ATTACK N · RESULT · AXIS` development label is hidden in v0.23.

## Validation
- `v023-polish.js`: Node syntax PASS.
- `v023-results.js`: Node syntax PASS.
- loader dependency check PASS.
- Render deploy reached LIVE.

No claim is made that the final mobile visual layout has been fully human-verified; device screenshots remain the next QA evidence.

## Next boundary
1. Device-test v0.23 landscape layout.
2. Verify center hero + fixed left/right information hierarchy.
3. Verify all six skill icons and full descriptions are readable.
4. Verify Rogue Timing Square/charge visibility on the natural background.
5. Verify every local timing EXP event produces `+EXP N`.
6. Verify TEAM never allows +3 AI and always reserves a human slot.
7. Verify result rows no longer visually collide.
8. Fix visual/implementation defects only.
9. Then implement v0.24 FRIEND/LINK/RANDOM waiting-room UX.
10. Real network transport/room authority remains a later, separate boundary.
