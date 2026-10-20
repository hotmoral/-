# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.23**
- Public URL: `https://timing-defense-v011.onrender.com/v023.html`
- Live source HEAD: `6a7a4acafda9fe7dc405455c73adc3d7065f1285`
- Render deploy: `dep-dbbfierrjlhs73e3mfeg` / LIVE

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
- Simulation never self-authorizes a numerical rebalance.

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

## Passive A/B — not production-frozen
- `40 raw / 2.0 s`
- no EXP / charge / crit / skill / combo
- knockback suppressed
- ordinary non-boss HP +10%

## PERFECT combo A/B
- PERFECT-only unbounded streak.
- GOOD/NORMAL/MISS reset.
- Heavy X/Y count separately.
- No hidden high-combo timing penalty.
- Persistent bonus candidate: 5–9 +5%, 10–19 +8%, 20–29 +12%, 30+ +15% cap.
- Milestone raw-equivalent budgets: 60 / 90 / 150 / 210 cap.

---

# v0.21 presentation layer
See `V021_IMPLEMENTATION_REPORT.md`.
- Natural battlefield.
- Lower-left EXP float removed.
- `+EXP N` beside gauge.
- Judgment pops inside Timing Square.
- START cue.
- Debug stats/hint hidden.

# v0.22 lobby foundation
See `V022_LOBBY_IMPLEMENTATION_REPORT.md`.
- Nickname.
- Five-class horizontal carousel.
- Mechanic-specific skill icons.
- Button-based SOLO/TEAM/AI/Tier settings.
- Solo + selected AI starts immediately.
- FRIEND/LINK/RANDOM visible but not network-connected.

# v0.23 — current lobby/readability polish
See `V023_LOBBY_POLISH_REPORT.md`.

## Character selection hierarchy
Landscape three-zone layout:
- left = class identity / role / play-style,
- center = horizontally sliding hero only,
- right = all six skill icons + selected full skill detail.

Arrows + swipe remain navigation. Skill text is no longer dependent on truncated cards.

## Skill roadmap
All six levels remain simultaneously visible:
`6 / 11 / 16 / 21 / 26 / 31`.
Selecting an icon exposes full name + full description.
Mechanic-specific icon shape/color remains the rule.

## Rogue readability
Natural scenery made gray Rogue HUD weak. v0.23 adds a HUD-only brighter red/silver contrast accent to Rogue Timing Square edge and charge pips. No Rogue balance value changed.

## EXP feedback
Every valid local `awardXP(amount)` event now arms a dedicated `+EXP N` popup state beside the gauge, including gains between level-ups.

## TEAM AI rule
TEAM always reserves at least one slot for a human participant.
- SOLO may use +3 AI.
- TEAM may use at most +2 AI.
- TEAM uses `AI FILL` semantics.

This is a lobby rule only; actual remote networking is not implemented yet.

## Settings/readability
- AI class buttons use compact role glyph + KNI/ROG/TNK/ARC/MAG label.
- Setting/AI rows compressed to reduce landscape overflow.
- Battle `CLASS · ATTACK · RESULT · AXIS` debug line hidden.
- Result board redrawn with larger row spacing and local nickname.

---

# End-run metrics
KILLS / DMG / COIN / LV / MAX COMBO.
Rows follow actual character slot order. Per-column rank colors remain gold/silver/bronze/muted. No forced global MVP.

---

# Encounter framework retained
Pressure families: S Swarm / E Elite-Heavy / X Special-Mixed.
Tier identity uses varied 1/2/3-pattern distributions rather than all three every stage.

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
1. Device/browser validation of public v0.23.
2. Verify center hero + fixed left/right information hierarchy.
3. Verify all six skill icons and full descriptions fit/read well.
4. Verify Rogue Timing Square and charge pips remain visible over natural scenery.
5. Verify every local timing EXP gain displays `+EXP N`.
6. Verify TEAM cannot select +3 AI and leaves at least one human slot.
7. Verify result rows no longer visually collide.
8. Fix implementation/visual defects only.
9. Then implement **v0.24** FRIEND/LINK/RANDOM waiting-room UX.
10. Actual room/network/matchmaking transport remains a separate later boundary.
11. Continue full-run progression simulation before freezing passive/combo/HP coefficients.

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
