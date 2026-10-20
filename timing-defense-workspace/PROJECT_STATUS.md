# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.25**
- Public URL: `https://timing-defense-v011.onrender.com/v025.html`
- Live source HEAD: `fce42eb1261ff43277c27d844617b96a546d6d1a`
- Render deploy: `dep-dbbga8c9v7es73f567b0` / LIVE

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

---

# v0.25 — current character-select vertical/layout polish
See `V025_LAYOUT_POLISH_REPORT.md`.

Android screen recording showed that the v0.24 top brand/nickname area still consumed too much real-device vertical space. v0.25 fixes the layout rather than merely scaling the hero.

## Vertical reclaim
- Lobby top header reduced again.
- Nickname row compressed and moved upward.
- Footer reduced.
- Recovered height is assigned directly to the character-selection panel.
- Center hero maximum height increased again.

## Left combat profile restored
The radar remains, but the sparse v0.24 left panel now again contains richer class identity:
- COMBAT PROFILE label,
- Korean class name,
- large English class name,
- class tag,
- animated radar,
- role summary,
- fuller one-sentence play-style description.

Radar axis labels are significantly larger. The animation still uses center-out scan, staggered vertex growth, class-color fill/glow, landing nodes and a final ripple.

## Right skill area
- Keeps six cards as `3 × 2`.
- Uses the newly available height for slightly larger icons/text/spacing rather than returning to a single-row strip.

## Non-goals
- No combat coefficient changed.
- Projectile travel timing unchanged.
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
1. Device/browser validation of public v0.25 on the same Android landscape setup.
2. Verify top whitespace is materially reduced.
3. Verify selection panel is visibly taller, not merely scaled internally.
4. Verify radar labels are readable without squinting.
5. Verify restored class description has enough presence without crowding the radar.
6. Verify center hero and 3×2 skill panel do not overlap.
7. Recheck TEAM lineup class buttons for clipping.
8. Recheck Rogue black/silver HUD and projectile visibility during combat.
9. Fix visual defects only from that validation.
10. Then implement deferred FRIEND/LINK/RANDOM waiting-room UX.
11. Actual room/network transport remains a separate later boundary.
12. Continue full-run progression simulation before freezing passive/combo/HP coefficients.

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
