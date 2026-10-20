# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.22**
- Public URL: `https://timing-defense-v011.onrender.com/v022.html`
- Live source HEAD: `7a321d021cafbfc32749b4e8b9421b2bf908826a`
- Render deploy: `dep-dbbef5s9v7es73eupvlg` / LIVE

## Core playable scope
- Landscape timing-action side defense.
- Core rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Current combat run: Stage 1–10.
- Run-only EXP / level / coin / shop.
- Skills implemented through Lv21; Lv26/Lv31 planned.
- AI teammates internally gain timing results / EXP / levels / Lv6–21 skills without visible AI Timing Squares.

## Frozen role/progression decisions
- Knight = stable generalist / frontline / penetration.
- Rogue = fast multihit / durable-normal execution; same-target dagger hits uncapped.
- Tank = team-specialist / knockback / wall protection; fresh-run solo parity not required.
- Archer = true straight-line penetration; no off-line retarget/bending.
- Mage = density/AoE specialist.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to valid timing results/events.
- Passive attacks grant no EXP.
- Simulation never self-authorizes numerical rebalance.

Player mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

---

# Combat foundation retained through v0.22

## Turn-boundary target integrity
- Not-yet-visible enemies cannot be targeted or damaged.
- A **new** Timing Square turn begins only while a valid visible enemy exists.
- If none is visible at the next-turn boundary, the Timing Square pauses in target-wait.
- AI/passive attacks wait too; empty timing turns cannot farm EXP.
- Attack input cannot force-spawn an off-screen enemy.

Critical continuity rule:
- if a local timing turn already started while a target was visible, target disappearance does **not** cancel it,
- current X remains tappable,
- fourth attack X→Y may finish fully,
- that already-valid turn may still award its normal judgment/EXP,
- only the next turn waits.

Target-wait does not break PERFECT combo.

## Stage start
Current flow:
`STAGE N / READY → intro fades → combat activates + START! pop`.

Intro gates enemy progression, AI/passive attacks and Timing Square input/sweep.

## Passive attack A/B — not production-frozen
- `40 raw / 2.0 s`
- no EXP / charge / crit / skill proc / combo
- knockback suppressed
- non-boss HP compensation `+10%`

## PERFECT combo A/B — mechanics accepted, coefficients still experimental
- only PERFECT increments
- GOOD / NORMAL / MISS reset
- heavy X/Y count separately
- numeric streak unbounded
- no hidden timing-window shrink or sweep acceleration
- short tilted popup near Timing Square from `1 COMBO!`

Persistent bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone follow-up budgets:
- 5 = 60
- 10 = 90
- 20 = 150
- 30+ = 210 cap
- every +10 after 30 repeats 30-tier strength.

---

# v0.21 — combat presentation polish

Public historical page: `https://timing-defense-v011.onrender.com/v021.html`
Source HEAD: `5a1c7fbfb575e805ce65eb238157abd2136ba3fa`
Render: `dep-dbbec549v7es73euenkg` / previously LIVE

See `V021_IMPLEMENTATION_REPORT.md`.

Changes:
- lower-left `EXP +N` float removed,
- EXP gain consolidated beside vertical gauge as `+EXP N`,
- NORMAL/GOOD/PERFECT/heavy-result/CRITICAL/MISS moved **inside Timing Square** as fast pop feedback with different color/size/glow,
- natural geometric battlefield replaces black grid,
- centered `START!` cue added when READY ends,
- result board centered,
- test stats/hint hidden.

No combat coefficient changed.

---

# v0.22 — current pre-game lobby / entry flow

Files:
- `timing-defense-v011/v022-lobby.js`
- `timing-defense-v011/v022.html`

See `V022_LOBBY_IMPLEMENTATION_REPORT.md`.

## Entry flow
Current production-direction flow:
`nickname + character carousel → play settings → run / future waiting room → stage intro → combat`.

The in-battle class selector and bottom prototype TEAM/SPEED/RESET configuration box are hidden in v0.22.

## Nickname
- Required before continuing.
- Stored in local browser storage for reuse.

## Character carousel
- Five classes presented one at a time.
- Arrow navigation + horizontal swipe.
- Smooth slide transition.
- Large geometric class visual with class-specific clothing, silhouette, weapon and palette.
- Class role summary.
- Six-skill roadmap for Lv6/11/16/21/26/31.

## Skill-icon direction — now explicit
Icons must communicate the actual mechanic through **shape + color**, not merely reuse one generic symbol.
Examples in the current prototype:
- Knight: blade-wave arcs / penetration / double slash.
- Rogue: dual daggers / weak-point reticle / dagger fan / dagger rain.
- Tank: shields / shockwaves / ground crack / aftershock rings.
- Archer: piercing line / bow / triple arrows / giant arrow.
- Mage: blast orb / expanded circles / resonance / chain orbs / collapse rings.

## Play settings
For small fixed option sets, v0.22 favors **buttons / segmented controls** rather than dropdowns.

Current options:
- MODE: SOLO / TEAM
- AI COUNT: NONE / +1 / +2 / +3
- AI position: P2 / P3 / P4
- AI class per slot
- TEAM mode method: FRIEND / LINK / RANDOM
- TIER: Tier 1 only for now

Defaults:
- SOLO
- AI NONE
- highest available tier (currently Tier 1)

Solo + AI applies the chosen lineup and starts combat immediately.

## Network boundary
FRIEND / LINK / RANDOM are visible as the intended team modes, but **real networking is not implemented in v0.22**.
The UI does not pretend that a match succeeded.

Next planned slice is v0.23 waiting-room/invite/link/random UX, followed by actual network/backend wiring.

## End-run navigation
Because debug controls are removed from combat, v0.22 provides explicit:
- RETRY
- LOBBY

---

# End-run contribution board
Current metrics remain:
- KILLS
- DMG
- COIN
- LV
- MAX COMBO

Rows follow actual character order. Each metric has explicit ranking:
1st gold / 2nd silver / 3rd bronze / 4th muted.

---

# Encounter framework retained
Pressure families:
- S = Swarm
- E = Elite/Heavy
- X = Special/Mixed

Tiers use varied 1/2/3-pattern stage distributions; all three patterns are not forced into every stage.

Current Swarm candidate bursts:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

Current P95 four-second spawn-density reference:
- 2P ≈ 11
- 3P ≈ 15
- 4P ≈ 18

---

# Current next boundary
1. Device/browser validation of public v0.22.
2. Check nickname input + carousel swipe/arrow behavior on Android landscape.
3. Check geometric class visuals and six skill cards remain readable without vertical overflow.
4. Check every skill icon is recognizable enough to suggest its mechanic.
5. Check button-based SOLO/TEAM/AI settings are faster/easier than a dropdown-style setup.
6. Verify selected AI positions/classes actually map into combat.
7. Verify in-combat class selector and temporary bottom settings are absent.
8. Verify v0.21 battlefield/judgment/EXP/START changes remain intact under the lobby loader.
9. Implement v0.23 team waiting-room flows for FRIEND / LINK / RANDOM without falsely claiming real network connectivity.
10. After waiting UX is stable, begin actual multiplayer room/link/random network architecture.
11. Continue full-run progression simulation before production-freezing passive/combo/HP coefficients.

## Still not production-frozen / unresolved
- passive attack final damage/interval,
- ordinary/elite/boss HP compensation,
- combo persistent coefficients,
- milestone proc coefficients/final visuals,
- final result-board metric set,
- final E/X pressure values,
- final tier count/names/order,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients,
- real network protocol / room authority / reconnection / matchmaking backend.
