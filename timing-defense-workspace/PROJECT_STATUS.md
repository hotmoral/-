# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Public repo: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.20**
- Public URL: `https://timing-defense-v011.onrender.com/v020.html`
- Live source HEAD: `d5c0e5cb90e8e5aa99c7420beb96202563f07e46`
- Render deploy: `dep-dbbdpd49v7es73esaet0` / LIVE

## Playable scope
- Landscape mobile/browser timing-defense prototype.
- Rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Team controls: solo through +3 AI.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Current Stage 1–10 run with EXP / level / coin / shop.
- Skills implemented through Lv21; Lv26/Lv31 remain planned.

## Frozen role/progression decisions
- Knight = stable generalist/frontline/penetration.
- Rogue = fast multihit / high-HP normal execution; same-target dagger hits uncapped.
- Tank = team-specialist / knockback / wall protection; fresh-run solo parity not required.
- Archer = true straight-line penetration; no off-line retarget/bending.
- Mage = density/AoE specialist.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to timing results/events.
- Passive attacks grant no EXP.
- Simulation never self-authorizes a numerical balance patch.

Player mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is intended to be attainable; strong Average→Skilled improvement is desirable.

---

# Current playable build — v0.20

Files:
- `timing-defense-v011/v020-flow-ui.js`
- `timing-defense-v011/v020-results.js`
- `timing-defense-v011/v020.html`

See `V020_IMPLEMENTATION_REPORT.md`.

## Turn-boundary target gating
A new Timing Square turn only begins while at least one valid on-screen target exists.

If no target is visible at a turn boundary:
- Timing Square enters target-wait and sweep stops,
- passive attack waits,
- AI attacks wait,
- no empty-turn EXP/progression is generated.

Critical continuity rule:
- once a local timing turn has started with a visible target, it remains valid until that whole turn finishes,
- if AI/passive/team damage removes the final target during the moving needle, the current X may still be tapped,
- on the fourth attack the X→Y sequence may finish completely,
- normal timing judgment/EXP for that already-valid turn remains allowed,
- only the **next** turn waits if no target is visible.

Reason: cancelling an already-moving turn when a teammate kills the target can look like lag/input loss.

Target-wait does **not** reset PERFECT combo. Combo breaks only on an actual non-PERFECT judgment.

Stage clear/shop transition is deferred until an already-started local turn finishes or naturally times out.

## Visible-target integrity
Retained from v0.19:
- not-yet-visible enemies cannot be targeted or damaged,
- pierce/AoE spill cannot hit beyond the visible right edge,
- unseen kills cannot generate kill rewards.

Attack input no longer force-spawns invisible enemies; stage scheduling owns spawning.

## Stage-start gate
Every stage now begins with a centered `STAGE N / READY` intro (~1050 ms).

During intro:
- no stage spawning/movement,
- no AI/passive attack,
- no Timing Square sweep/input.

Combat starts only after the intro has disappeared; Timing Square then waits until the first enemy is actually visible.

## Timing/UX polish
- Test descriptor removed; top title is simply `TIMING DEFENSE`.
- Class selector moved upward.
- GOOD / PERFECT / CRITICAL / heavy-result text moved beside the EXP gauge and reduced in size.
- PERFECT combo pop remains the approved short tilted impact-style popup near Timing Square.

## Four-player spacing
Current v0.20 slot Y:
`.265 / .425 / .585 / .745`

Character scale remains `.41`.

## End-run result board
Rows stay in character order: YOU / CPU1 / CPU2 / CPU3.

Columns:
- KILLS
- DMG
- COIN
- LV
- MAX COMBO

v0.20 cleans alignment/spacing and removes heavy boxes around every metric while keeping explicit per-column ranks:
1st gold / 2nd silver / 3rd bronze / 4th muted.

---

# Current experimental combat values — unchanged

Passive A/B:
- `40 raw / 2.0 s`,
- no EXP / charge / crit / skill / combo,
- knockback suppressed,
- non-boss HP compensation `+10%`.

PERFECT combo:
- only PERFECT increments,
- GOOD / NORMAL / MISS reset,
- heavy X and Y count separately,
- streak numeric count is unbounded,
- no hidden timing-window shrink/sweep acceleration.

Persistent timing bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone follow-up budgets:
- 5 = 60
- 10 = 90
- 20 = 150
- 30+ = 210 cap
- every +10 after 30 repeats 30-tier power.

These values remain playable A/B values, not production-frozen.

---

# Encounter framework retained

Pressure families:
- S = Swarm
- E = Elite/Heavy
- X = Special/Mixed

Tier design uses varied 1/2/3-pattern stage distributions; all three are not forced into every stage.

Current candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

Current P95 four-second spawn-density reference:
- 2P ≈ 11
- 3P ≈ 15
- 4P ≈ 18

---

# Balance evidence retained

## v7 exact-formula rerun
Lv21 clear bounds:
- 3P Average/Skilled = 81.6 / 96.4%
- 4P = 52.8 / 73.6%

Rogue remains best durable-normal killer; Archer remains strongest on line geometry. No class rebalance authorized.

## v8 passive/combo analysis
Around 150 judgment opportunities:
- Skilled P40: 5 combo ~61%, 10 ~0.87%, 20 ~0
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%

User device feedback confirmed:
- combo count creates effective tension,
- passive fire creates useful battlefield-reading room,
- game feel improved.

No numerical retuning was authorized from this feedback.

---

# Current next boundary

1. Device/browser test public v0.20.
2. Verify no new timing turn starts without a visible enemy.
3. Verify a turn already in motion survives target disappearance and fourth-attack X→Y never cancels midway.
4. Verify no empty-turn EXP farming.
5. Verify target-wait preserves combo.
6. Verify Stage N intro ends before combat begins.
7. Verify judgment text no longer overlaps square/EXP/combo.
8. Verify wider party spacing on short landscape displays.
9. Verify result-board alignment/readability.
10. Fix implementation/visual defects only, then continue full-run progression simulation before freezing passive/combo/HP coefficients.

## Still not production-frozen
- final passive damage/interval,
- final ordinary/elite/boss HP compensation,
- final combo persistent bonuses,
- final milestone proc coefficients/visuals,
- final result-board metric set/presentation,
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- true human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync-bonus implementation,
- final tier number/names/order,
- Lv26/Lv31 coefficients.
