# Timing Defense — v0.22 Pre-game Lobby Implementation Report

Date: 2026-10-20 KST
Status: **LIVE — pre-game UX implemented; real network matchmaking NOT implemented yet**

## Public build
- URL: `https://timing-defense-v011.onrender.com/v022.html`
- Live source HEAD: `7a321d021cafbfc32749b4e8b9421b2bf908826a`
- Render deploy: `dep-dbbef5s9v7es73eupvlg` / LIVE

Files:
- `timing-defense-v011/v022-lobby.js`
- `timing-defense-v011/v022.html`

## Purpose
Move class/team configuration out of the combat battlefield and establish a production-like entry flow:

`nickname + character selection → play settings → run / future waiting room → stage intro → combat`

The old in-combat class selector and bottom prototype setting controls are hidden in v0.22.

---

# 1. Nickname + class carousel

The first lobby page provides:
- nickname input,
- nickname persistence in local browser storage,
- five-class horizontal carousel,
- arrow navigation,
- swipe navigation,
- smooth slide transition,
- one large class presentation at a time.

Classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

## Geometric class art
The lobby uses deliberately designed geometric character art rather than generic rectangles.
Class identity is carried by clothing silhouette, weapon and palette:
- Knight: armor + sword,
- Rogue: hood/dark outfit + dual daggers,
- Tank: heavier silhouette + shield,
- Archer: hood/green outfit + bow/arrow,
- Mage: robe/hat + staff/orb.

This remains prototype vector/geometric art, not final production illustration.

---

# 2. Skill roadmap and icon language

Each class shows six milestones:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.

Every skill card includes:
- skill name,
- unlock level,
- concise mechanic description,
- unique canvas-drawn icon.

## Frozen icon direction
Skill icons must communicate mechanics through **shape as well as color** rather than using one generic glyph family.

Examples implemented:
- Knight: blade-wave arcs, penetration path, large slash, double slash.
- Rogue: two daggers, weak-point reticle, dagger fan, chain throw path, dagger rain.
- Tank: shield, expanding shockwave, guard star, ground crack, aftershock rings.
- Archer: piercing line arrow, bow, armor penetration, three arrows for Triple Shot, giant arrow.
- Mage: burst orb, expanded circles, resonance pair, large orb, chained orbs, collapse rings.

Different skills within one class also vary in symbol composition and accent treatment.

---

# 3. Play settings — button/segmented interaction

The play-setting page intentionally favors direct buttons over dropdowns for the small fixed option sets.

Current controls:
- MODE: SOLO / TEAM
- TEAM MATCH: FRIEND / LINK / RANDOM
- AI COUNT: NONE / +1 / +2 / +3
- TIER: Tier 1 only in the current prototype
- AI lineup: position and class per AI

Defaults:
- SOLO
- AI NONE
- highest available tier (currently Tier 1)

## AI configuration
For each enabled AI teammate:
- choose P2 / P3 / P4 position,
- choose one of the five classes,
- duplicate positions are resolved by swapping positions,
- selected configuration is applied to actual AI slots/classes when a solo+AI run starts.

Solo + AI therefore starts the actual existing combat immediately with the selected lineup.

---

# 4. Team/network boundary

The TEAM UI exposes the intended future modes:
- FRIEND
- LINK
- RANDOM

**These are not real multiplayer connections in v0.22.**

Current behavior deliberately does not fake successful matchmaking. TEAM continuation briefly indicates that network waiting belongs to the next build.

Planned next boundary:
- v0.23 waiting-room/room-flow UX,
- then actual room/link/random matchmaking backend/network synchronization.

---

# 5. End-run navigation

Because prototype class/team controls are removed from combat, v0.22 adds explicit post-run actions:
- RETRY
- LOBBY

LOBBY returns to pre-game character/settings flow.

---

# 6. Combat retained

v0.22 inherits v0.21/v0.20 combat behavior unchanged, including:
- target-boundary gating,
- active-turn continuity when final target disappears,
- stage `READY → START!`,
- natural background,
- inside-square judgment pops,
- passive attack A/B,
- unbounded PERFECT combo,
- Lv6–21 class skills,
- AI internal EXP/level/skill progression.

No numerical balance value was changed by the lobby implementation.

## Validation boundary
- lobby JS passed syntax checking before push,
- Render LIVE confirms the published build,
- final mobile composition/gesture/readability still requires user device playtest.
