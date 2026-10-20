# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.26**
- Public URL: `https://timing-defense-v011.onrender.com/v026.html`
- Live source HEAD: `8aee137de2f775cda3537b6cc0b9404f6692a55b`
- Render deploy: `dep-dbbgvjjbc2fs73b657s0` / LIVE

## Core playable scope
- Landscape timing-action side defense.
- Rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Current run: Stage 1–10 with EXP / level / coin / shop.
- Implemented class skills: Lv6 / 11 / 16 / 21. Lv26/Lv31 planned.
- AI teammates internally gain timing results / EXP / levels / skills without visible AI Timing Squares.

## Frozen role/progression decisions
- Knight = stable generalist / frontline / penetration.
- Rogue = fast multihit / durable-normal execution; same-target dagger hits uncapped.
- Tank = team-specialist / knockback / wall protection; fresh-run solo parity not required.
- Archer = strict straight-line penetration; no bending/retarget.
- Mage = density/AoE specialist.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Simulation never self-authorizes numerical rebalance.

Mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

---

# Combat foundation retained

## Target/turn integrity
- Off-screen enemies cannot be targeted/damaged/rewarded.
- New timing turn starts only with a visible target.
- If no target exists at the next-turn boundary, Timing Square waits.
- AI/passive attacks wait too; empty-turn EXP farming is blocked.
- An already-started valid timing turn survives target disappearance.
- Heavy X→Y may finish fully even if the final target disappears mid-turn.
- Target-wait does not break PERFECT combo.

## Stage start
`STAGE N / READY → fade → START! + combat`

## Experimental values — not production-frozen
Passive:
- `40 raw / 2.0 s`
- no EXP / charge / crit / skill / combo
- knockback suppressed
- ordinary non-boss HP +10%

PERFECT combo:
- PERFECT-only unbounded streak
- GOOD/NORMAL/MISS reset
- Heavy X/Y count separately
- no hidden high-combo timing penalty
- persistent candidate 5/8/12/15%
- milestone raw-equivalent budgets 60 / 90 / 150 / 210 cap

**v0.26 regression guard:** combo display/size/position/animation was deliberately not changed. The user identified the combat title as the overlap defect.

---

# Presentation history

## v0.21
- Natural battlefield.
- Lower-left EXP float removed.
- `+EXP N` beside gauge.
- Judgment pops inside Timing Square.
- START cue.
- Debug stats/hint hidden.

## v0.22
- Nickname + five-class carousel.
- Mechanic-specific skill icons.
- Button-based SOLO/TEAM/AI/Tier settings.
- Solo + selected AI starts immediately.
- FRIEND/LINK/RANDOM visible but not network-connected.

## v0.23
- Character selection reorganized as left info / center hero / right skill detail.
- Every valid local timing EXP event arms `+EXP N`.
- TEAM reserves at least one human slot; TEAM AI FILL max +2.
- Result-board row spacing/nickname improved.
- Battle attack debug line hidden.

## v0.24
See `V024_RADAR_READABILITY_REPORT.md` and `CHARACTER_PROFILE_RADAR_V1.md`.
- Added animated five-level six-axis class radar.
- Radar axes frozen: `공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`.
- Approved profiles:
  - Knight `4/2/3/3/4/2`
  - Rogue `2/5/5/1/1/1`
  - Tank `2/1/1/5/1/3`
  - Archer `3/2/4/1/5/2`
  - Mage `4/2/2/1/1/5`
- Right skill layout changed to `3 × 2` direct cards.
- TEAM lineup SUMMARY removed; class choices wrap to two rows.
- Rogue HUD changed to charcoal/black + silver.
- Projectile visibility increased with darker silhouettes/brighter edges/trails; travel timing unchanged.

## v0.25
See `V025_LAYOUT_POLISH_REPORT.md`.
- Reclaimed more vertical lobby space.
- Enlarged radar labels.
- Restored richer class identity/role/detail copy.
- Increased center hero presence.

---

# v0.26 — current HUD / layout patch
See `V026_HUD_LAYOUT_REPORT.md`.

## Character select
- `3 × 2` skill cards retained.
- Skill card header = icon + skill name, with `습득 LV N` directly below the name.
- Description now spans the full card width below, including the area under the icon.
- Radar moved upward and given a bounded height so role + full description remain visible.
- Hero class name moved from below the character to above the head.
- Carousel arrow hit targets enlarged and fixed; active-state jump removed; pointer/touch propagation no longer conflicts with swipe.

## Combat HUD
- Legacy combat `TIMING DEFENSE` prototype title removed.
- New top-center BASE HP HUD:
  - base icon,
  - `BASE HP`,
  - current/max HP,
  - long horizontal gauge.
- New top-right status HUD in fixed order:
  1. STAGE,
  2. LV,
  3. KILLS,
  each preceded by an icon.
- Legacy bottom canvas status strings are suppressed to avoid duplication.

## Home base
Left-side home base now has a fortified visual pass:
- armored cap,
- crenellations,
- reinforced side columns,
- four character bays,
- character ledges,
- small central crest.

## Combat skill strip
The six slots below the Timing Square now reuse the same class-specific skill canvases as the character-select roadmap.
- learned = full artwork,
- locked = same artwork dimmed/grayscaled,
- ordering stays Lv6 / 11 / 16 / 21 / 26 / 31.

## Explicit non-goals
- No combo visual or logic change.
- No combat coefficient change.
- No projectile travel-time change.
- Actual multiplayer networking still not implemented.

---

# Team / network truth boundary
TEAM always reserves at least one human slot:
- SOLO AI: 0–3
- TEAM AI FILL: 0–2

FRIEND / LINK / RANDOM are still only front-end intent states. Do not claim remote connectivity until two independent clients share authoritative state.

---

# End-run metrics
KILLS / DMG / COIN / LV / MAX COMBO.
Rows follow actual character slot order. Per-column rank colors remain gold/silver/bronze/muted. No forced global MVP.

---

# Encounter framework retained
Pressure families: S Swarm / E Elite-Heavy / X Special-Mixed.
Current Swarm candidate bursts:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

P95 four-second spawn-density reference:
- 2P ≈ 11
- 3P ≈ 15
- 4P ≈ 18

---

# Current next boundary
1. Device/browser validation of public v0.26 on the same Android landscape setup.
2. Verify skill cards use the full lower width and `습득 LV` sits below every skill name.
3. Verify radar is higher and the class role/detail text is no longer clipped.
4. Verify class name is above the hero head.
5. Rapidly tap arrows and confirm no positional jump or missed taps; recheck swipe outside arrows.
6. Confirm combo presentation is unchanged.
7. Confirm combat title is gone.
8. Confirm top-center BASE HP is immediately readable.
9. Confirm top-right icon + STAGE → LV → KILLS HUD is readable.
10. Confirm improved base structure and lobby-derived combat skill icons look coherent in motion.
11. Fix visual/implementation defects only from this validation.
12. Then implement deferred FRIEND/LINK/RANDOM waiting-room UX.
13. Actual room/network transport remains a separate later boundary.
14. Continue full-run progression simulation before freezing passive/combo/HP coefficients.

## Still unresolved / not production-frozen
- passive final damage/interval,
- ordinary/elite/boss HP compensation,
- combo persistent/milestone coefficients,
- final result-board metrics,
- final E/X values and tier count,
- multiplayer economy/shop ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL sync implementation,
- Lv26/Lv31 coefficients,
- room authority / invite-link contract / random queue / reconnect-state reconciliation.