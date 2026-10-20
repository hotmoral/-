# Timing Defense v0.26 — HUD / Layout Patch Report

Updated: 2026-10-20 KST

## Public state
- Version: **v0.26**
- URL: `https://timing-defense-v011.onrender.com/v026.html`
- Live source HEAD: `8aee137de2f775cda3537b6cc0b9404f6692a55b`
- Render deploy: `dep-dbbgvjjbc2fs73b657s0` / LIVE

Files:
- `timing-defense-v011/v026-hud-layout.js`
- `timing-defense-v011/v026.html`

---

# Scope
This patch responds to Android landscape screenshots/video from v0.25.
It is a presentation/input-reliability patch only.

**Explicit non-goal:** combo behavior is unchanged. The user identified the legacy combat title as the collision problem, not the combo popup itself. v0.26 does not change combo size, position, animation, milestones, counters, coefficients, or streak logic.

No numerical combat-balance values changed.

---

# Character-select changes

## Skill cards
The six-card `3 × 2` layout remains.
Each card now uses the vertical area more efficiently:
- row 1: skill icon + skill name,
- acquisition level shown directly below the skill name as `습득 LV N`,
- row 2: description spans the full card width, including the area under the icon,
- overall text sizing increased where device height permits.

This removes the previously unused blank column below each icon.

## Left combat profile
- radar moved upward,
- radar vertical reservation reduced enough to guarantee room below,
- role summary and full one-sentence class description remain visible,
- radar animation/data remain unchanged from approved v0.24/v0.25 contract.

## Hero class name
The large class name is moved from beneath the hero to above the character head.

## Carousel arrows
Input stability patch:
- fixed left/right coordinates,
- larger hit target,
- active press no longer overrides the vertical centering transform,
- pointer/touch events on arrows stop propagation before the carousel swipe handler can steal the gesture.

Swipe navigation remains available outside the arrow buttons.

---

# Combat HUD changes

## Legacy prototype title removed
`#topbar` is hidden during the base game UI. This removes the combat-screen `TIMING DEFENSE` title that collided visually with large combo popups.

Again: **combo display itself was not modified.**

## BASE HP
A formal horizontal BASE HP HUD is added at the map top-center:
- base icon,
- `BASE HP`,
- current / max numeric HP,
- long horizontal gauge,
- gauge color shifts green → amber → red as HP decreases.

The obsolete small wall HP text/gauge on the left base is suppressed/covered.

## Run status
Top-right HUD is formalized in the requested order:
1. stage icon + `STAGE N`,
2. level icon + `LV N`,
3. kill icon + `KILLS N`.

Legacy bottom canvas strings for team/stage/kills and coin/wall/enemies are suppressed to avoid redundant HUD duplication.

The new top HUD is hidden while the lobby/result screen is active and shown for stage intro/combat.

---

# Home-base visual pass
The left-side base is upgraded from a plain dark slab into a more readable fortified structure:
- armored top cap,
- crenellated silhouette,
- reinforced side columns,
- four recessed character bays,
- individual character ledges/platforms,
- small center crest.

Characters are still drawn afterward, so they remain visually seated on top of the base structure.

---

# Combat skill strip
The six slots below the Timing Square no longer use generic v0.16 glyphs.
They now draw from the same `data-skill="class:index"` canvases authored for the character-select skill roadmap.

Rules:
- learned slots show the original class-specific skill artwork,
- locked slots show the same artwork dimmed/grayscaled,
- unlock pulse/border behavior remains available,
- six-slot ordering stays Lv6 / 11 / 16 / 21 / 26 / 31.

This establishes one visual identity per skill across lobby and combat.

---

# Device validation required
Validate on the same Android landscape setup:
1. skill card names/`습득 LV`/full-width descriptions fit cleanly,
2. radar sits higher and both role + description remain visible,
3. hero class name is clearly above the head,
4. repeated fast arrow taps always register and arrow position does not jump,
5. swipe still works away from arrows,
6. combo presentation is unchanged,
7. combat title is gone,
8. BASE HP is immediately readable at top-center,
9. STAGE → LV → KILLS chips are readable at top-right,
10. improved base structure reads as a defensive fortification,
11. six combat skill icons match the character-select skill artwork,
12. no top HUD overlaps stage intro or combat-critical visuals.

## Explicit regression guard
If later feedback concerns combo/title overlap, do not change combo unless the user explicitly authorizes it. The v0.26 decision is that the title was the defect.