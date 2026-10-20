# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.24**
- Public URL: `https://timing-defense-v011.onrender.com/v024.html`
- Live source HEAD: `61ad74d833148d409dc65292f302bb9086c4e7c9`
- Render deploy: `dep-dbbg528m7kps73esejbg` / LIVE

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

# Presentation history

## v0.21
- Natural battlefield.
- Lower-left EXP float removed.
- `+EXP N` beside gauge.
- Judgment pops inside Timing Square.
- START cue.
- Debug stats/hint hidden.

## v0.22
- Nickname.
- Five-class horizontal carousel.
- Mechanic-specific skill icons.
- Button-based SOLO/TEAM/AI/Tier settings.
- Solo + selected AI starts immediately.
- FRIEND/LINK/RANDOM visible but not network-connected.

## v0.23
See `V023_LOBBY_POLISH_REPORT.md`.
- Character selection reorganized into left info / center hero / right skill detail.
- Every valid local timing EXP event arms `+EXP N`.
- TEAM reserves at least one human slot; TEAM AI FILL max +2.
- Result-board row spacing and nickname improved.
- Battle debug attack label hidden.

---

# v0.24 — current radar / readability polish
See `V024_RADAR_READABILITY_REPORT.md` and `CHARACTER_PROFILE_RADAR_V1.md`.

## Character profile radar
Six fixed axes:
`공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`.

Five visual levels; equal levels between classes are allowed.
Approved profiles:
- Knight `4 / 2 / 3 / 3 / 4 / 2`
- Rogue `2 / 5 / 5 / 1 / 1 / 1`
- Tank `2 / 1 / 1 / 5 / 1 / 3`
- Archer `3 / 2 / 4 / 1 / 5 / 2`
- Mage `4 / 2 / 2 / 1 / 1 / 5`

Radar animation uses center-out scan, staggered vertex growth, class-color fill/glow and short settling pulse.
The radar is an identity graphic, not a literal exposure of raw combat coefficients.

## Character-selection layout
- left = animated combat-profile radar,
- center = larger/taller hero,
- right = six skill cards in a `3 × 2` grid,
- arrows moved closer to the hero,
- short-landscape header/nickname/footer height reduced to give the hero more vertical space.

## TEAM lineup
- Bottom SUMMARY removed.
- Lineup gets more width.
- Five class choices wrap into two rows per AI unit.
- AI row height increased to prevent class clipping.
- TEAM AI FILL remains 0–2; SOLO AI remains 0–3.

## Rogue identity
Rogue HUD is now charcoal/black + silver instead of v0.23 red/silver:
- Timing Square,
- charge pips,
- charge/heavy text,
- EXP gauge and labels,
- `+EXP N` popup.

No Rogue balance value changed.

## Projectile visibility
Projectile travel times remain unchanged.
A visual-only contrast pass adds darker class-color silhouettes, brighter edges and stronger short trails so projectiles remain recognizable over the brighter natural background.

Do not numerically slow projectile travel unless device validation shows this visual pass is still insufficient; report/discuss before changing travel timing.

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
1. Device/browser validation of public v0.24.
2. Verify radar labels and five rings fit on short Android landscape.
3. Verify class-switch radar animation feels premium and never stacks stale frames.
4. Verify center hero no longer collides with the right 3×2 skill panel.
5. Verify all six skill descriptions remain readable.
6. Verify TEAM lineup shows all five class choices without clipping.
7. Verify Rogue HUD reads black/charcoal, not red.
8. Verify projectiles are recognizable as objects rather than only blur streaks.
9. If projectile visibility is still weak, discuss a small travel-time adjustment before applying it.
10. After this visual validation, implement the deferred FRIEND/LINK/RANDOM waiting-room UX as the next version.
11. Actual network transport remains a separate later boundary.
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
