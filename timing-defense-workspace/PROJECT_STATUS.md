# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Public repo: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.19**
- Public URL: `https://timing-defense-v011.onrender.com/v019.html`
- Live source HEAD: `0e51e172dc1ea11a78e67eb62c557d9ac4c373bc`
- Render deploy: `dep-dbbd6duq1p3s73c659cg` / LIVE

## Current playable scope
- Landscape mobile/browser timing-defense prototype.
- Fixed local player near left wall; monsters approach from right.
- Rhythm: `X → X → X → X+Y`.
- Judgments: NORMAL / GOOD / PERFECT plus HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Team controls: solo through +3 AI.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Current playable Stage 1–10 prototype.
- Run-only EXP / level / coin / shop upgrades.
- Playable class skills through Lv21.

## Growth structure
Automatic skill milestones:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Implemented now:
`Lv6 / Lv11 / Lv16 / Lv21`

Lv21 is intentionally the first major fourth-attack transformation milestone. Lv26/Lv31 remain planned only.

## Frozen class / progression decisions
- Archer = true straight-line geometry; launch path locks and cannot bend/retarget off-line.
- Tank = team-specialist; fresh-run solo parity is not required.
- Rogue repeated dagger hits on the same target are uncapped.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to timing attack events/results.
- Faster clear does not receive compensating EXP merely for fewer attacks.
- Passive basic attacks do not grant EXP.
- Simulation never self-authorizes a production balance patch.

## Player mastery reference
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is considered attainable; strong Average→Skilled improvement is intended.

---

# v0.18 combat experiment retained in v0.19

## Passive basic attack — still experimental
- Local passive attack = `40 raw / 2.0 s`.
- No EXP / charge / crit / proc-crit / skill trigger / combo contribution.
- Knockback suppressed.
- Non-boss spawned monsters receive `+10% HP`.
- Bosses do not automatically receive the same +10%.

## PERFECT combo mechanics — still experimental
- Only PERFECT increments.
- GOOD / NORMAL / MISS reset.
- Heavy X and Y count independently.
- Counter is unbounded.
- No hidden timing-window shrink or sweep acceleration.

Persistent timing-attack bonus:
- 5–9: +5%
- 10–19: +8%
- 20–29: +12%
- 30+: +15% cap

Milestone follow-ups:
- 5 / 10 / 20 / 30 / every +10 after 30.
- Raw-equivalent budgets = 60 / 90 / 150 / 210 cap.

These values are playable A/B values, not production-frozen coefficients.

---

# v0.19 — current UX / integrity build

Files:
- `timing-defense-v011/v019-combo-pop.js`
- `timing-defense-v011/v019-ux-results.js`
- `timing-defense-v011/v019.html`

See `V019_IMPLEMENTATION_REPORT.md`.

## Visible-target integrity
Legacy behavior could target monsters immediately after spawn even while they were still beyond the right viewport edge.

v0.19:
- an enemy is targetable only after its aim point enters the viewport,
- not-yet-visible enemies are ignored by nearest-target selection,
- damage/AoE/pierce spill to not-yet-visible enemies is rejected,
- therefore unseen kills do not award kill coin.

Timing input may still produce an empty forward attack if no visible target exists; it simply cannot damage an unseen monster.

## Wider four-player spacing
v0.19 slot-Y candidate:
`.255 / .405 / .555 / .705`

Character scale remains `.41`.
Intent: improve full-body/weapon readability; temporary prototype bottom controls should not constrain production character spacing.

## Combo presentation
The v0.18 persistent rectangular combo HUD is replaced in v0.19.

New behavior:
- `1 COMBO!` appears from the first PERFECT,
- text appears near the Timing Square only at the PERFECT moment,
- slight tilt + punch/scale + fade-out,
- no persistent box between attacks,
- visual strength escalates at 5 / 10 / 20 / 30+,
- 30+ presentation may plateau while the numeric streak remains unbounded.

## End-run team result board
On Stage 10 clear or game over, rows follow character slot order:
1. YOU
2. CPU 1
3. CPU 2
4. CPU 3

First summary fields:
- KILLS
- DMG
- COIN (kill-reward coin contribution)
- LV
- MAX COMBO

Every field receives an explicit rank. Rank style:
- 1st gold
- 2nd silver
- 3rd bronze
- 4th muted blue-gray

The board tracks per-slot damage, kills, kill-coin value and max combo; AI streak data comes from its internal timing judgments.

---

# Simulation / design history

## v1–v4
Established class-role separation, Stage 1–10/run-shop behavior, mastery curve, and team-role validation.

Accepted outcomes:
- Tank defensive/team utility is intentional.
- Rogue owns durable-normal execution.
- Archer line geometry differs from Mage density geometry.
- Knight is the stabilizing generalist.

## v5 — Tier Pressure Grammar
Future 50-stage tiers use S/E/X pressure families with 1/2/3-pattern stage distributions rather than forcing all patterns into every stage.

Representative five-tier distribution:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

## v6 — concrete pressure recipes
Candidate Swarm burst sizes:
- line 2P/3P/4P = `8 / 11 / 14`,
- cluster = `7 / 10 / 13`,
- scatter = `9 / 12 / 16`.

X remains primary co-op scaling language; E is treated as an effective durability budget rather than one absurd HP bar.

## v7 — exact v0.16 formula rerun
Lv21 clear bounds:
- 3P Average/Skilled = 81.6 / 96.4%,
- 4P = 52.8 / 73.6%.

Rogue retains best durable-normal TTK. Archer remains strongest on line geometry. No numerical class rebalance authorized.

## v8 — passive + unbounded PERFECT combo
See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

Combo rarity around 150 judgments:
- Skilled P40: 5 ~61%, 10 ~0.87%, 20 ~0.
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%.
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%.

Mean combo reward uplift:
- Average ~0.01%
- Skilled ~0.26%
- Expert ~1.99%
- Master-test P80 ~4.74%

Forced local timing pause = 2 seconds every 12 seconds:
- 3P Average: `63.7 → 61.3 → 65.7%`
- 3P Skilled: `76.7 → 72.7 → 75.9%`
- 4P Average: `56.8 → 54.4 → 57.2%`
- 4P Skilled: `63.0 → 60.8 → 64.2%`

Sequence = current no-pause → current with pause → passive40/2s + HP10% with same pause.

User device feedback after v0.18:
- game feel clearly improved,
- combo number creates effective tension,
- passive attack gives real battlefield-reading breathing room,
- persistent combo box presentation needed refinement.

This feedback motivated v0.19 UX work but did not authorize numerical retuning.

---

# Current next boundary

1. Device/browser playtest public v0.19.
2. Verify no unseen enemy can be damaged/rewarded.
3. Verify widened four-character spacing improves silhouette readability.
4. Verify transient combo pop is readable but not visually sticky/obstructive.
5. Verify result-board density/ranking on the user's landscape Android browser.
6. Confirm whether KILLS / DMG / COIN / LV / MAX COMBO are the correct first five team-summary metrics.
7. Fix implementation/visual defects only.
8. Continue full-run progression simulation before production-freezing passive/HP/combo coefficients.

## Still not production-frozen
- final passive damage/interval,
- final ordinary/elite/boss HP compensation,
- final combo persistent bonuses,
- final milestone proc coefficients/visuals,
- final end-result metric set/presentation,
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- true human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync-bonus implementation,
- final number/names/order of tiers,
- Lv26/Lv31 exact coefficients.
