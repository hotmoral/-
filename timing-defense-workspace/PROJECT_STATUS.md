# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Public repo: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.18**
- Public URL: `https://timing-defense-v011.onrender.com/v018.html`
- Live source HEAD: `bacc0b86e356e003bdf697187ff6ea313130fc73`
- Render deploy: `dep-dbbcntjbc2fs73anb9rg` / LIVE

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

# v0.17 foundation retained in v0.18

### AI teammate growth parity
AI teammates internally maintain:
- independent EXP,
- independent level,
- Lv6/11/16/21 automatic skill unlocks,
- internally simulated timing judgments,
- class skill mechanics.

No additional AI Timing Squares are rendered.

### Timing Square continuity
- After an input the Timing Square remains visible at reduced opacity (~42%) through projectile/recovery.
- Charge/location therefore remain continuously anchored.

### Party spacing
- Four-player vertical slot positions are widened to approximately `.285 / .405 / .525 / .645`.
- Character scale is preserved.

---

# v0.18 — current playable A/B experiment

Files:
- `timing-defense-v011/v018-combo-ui.js`
- `timing-defense-v011/v018-auto-combo.js`
- `timing-defense-v011/v018.html`

See `V018_IMPLEMENTATION_REPORT.md`.

## PERFECT combo counter
- Visible from **1 COMBO** near the Timing Square.
- Only PERFECT increments.
- GOOD / NORMAL / MISS reset to zero.
- Heavy X and heavy Y count separately.
- Counter is unbounded.
- Visual tiers: 1–4 / 5–9 / 10–19 / 20–29 / 30+.
- Visual intensity may cap at 30+, numeric count never caps.
- No hidden PERFECT-window shrink or sweep acceleration at high combo.

## Combo power — experimental, not production-frozen
Persistent timing-attack bonus while streak survives:
- 5–9: +5%
- 10–19: +8%
- 20–29: +12%
- 30+: +15% cap

Milestone follow-up triggers at:
- 5,
- 10,
- 20,
- 30,
- every +10 after 30.

First playable raw-equivalent milestone budgets:
- 5: 60
- 10: 90
- 20: 150
- 30+: 210 cap

Class expression:
- Knight: blade/frontline follow-up.
- Rogue: multi-dagger burst.
- Tank: local shockwave follow-up.
- Archer: straight-line follow-up.
- Mage: compact secondary explosion.

Milestones do not consume/reset combo.

## Passive basic attack — experimental
- Local passive attack = `40 raw damage / 2.0 s`.
- No EXP.
- No charge.
- No crit/proc crit.
- No skill trigger.
- No combo contribution.
- Knockback suppressed.

## Enemy compensation — experimental
- Non-boss spawned monsters: `+10% HP`.
- Bosses do not automatically receive the same +10% in this A/B build.
- This is intentionally not 1:1 compensation for passive DPS; some real attention/breathing-room benefit is the design goal.

---

# Simulation / design history

## v1–v4
Established role separation, Stage 1–10/run-shop behavior, mastery curve, and team-role validation.

Key accepted outcomes:
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

X remains the main co-op scaling language; E is treated as effective durability budget rather than one absurd HP bar.

## v7 — exact v0.16 formula rerun
Lv21 clear bounds:
- 3P Average/Skilled = 81.6 / 96.4%,
- 4P = 52.8 / 73.6%.

Rogue retains best durable-normal TTK. Archer remains strongest on line geometry. No numerical class rebalance authorized.

## v8 — passive basic attack + unbounded PERFECT combo
See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

### Combo rarity around 150 judgments
- Skilled P40: 5 ~61%, 10 ~0.87%, 20 ~0.
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%.
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%.

This supports 30/40 as rare high-tension events rather than routine rotation.

### Combo reward power estimate
Mean damage uplift over ~150 judgments:
- Average ~0.01%,
- Skilled ~0.26%,
- Expert ~1.99%,
- Master-test P80 ~4.74%.

### Passive candidate evidence
40/2.0s contributes about:
- 13.9% of Average baseline timing DPS,
- 10.8% of Skilled,
- 8.8% of Expert.

Forced local timing pause = 2 seconds every 12 seconds:
- 3P Average: `63.7 → 61.3 → 65.7%`
- 3P Skilled: `76.7 → 72.7 → 75.9%`
- 4P Average: `56.8 → 54.4 → 57.2%`
- 4P Skilled: `63.0 → 60.8 → 64.2%`

Sequence = current no-pause → current with pause → passive40/2s + HP10% with same pause.

Interpretation: passive fire recovers most of the attention cost of briefly reading the battlefield without replacing timing play.

Passive-only stage sanity:
- 3P = 0% clear,
- 4P = 0%,
- 2P ~12.2% with very low wall HP (~357/2000 average among clears).

---

# Current next boundary

1. Device/browser playtest public v0.18.
2. Verify combo HUD does not overlap charge/EXP/skill strip.
3. Verify 1 COMBO appears immediately and X/Y counting/reset semantics are exact.
4. Verify passive projectile is visibly weaker and gives no EXP/charge/combo.
5. Verify 5/10/20 milestone follow-ups are readable and class-distinct.
6. Run full-run progression simulation with wall HP carried stage-to-stage before production-freezing passive/HP values.
7. Report/discuss before changing experimental coefficients.

## Still not production-frozen
- final passive damage/interval,
- final ordinary/elite/boss HP compensation,
- final combo persistent bonuses,
- final milestone proc coefficients/visuals,
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- true human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync-bonus implementation,
- final number/names/order of tiers,
- Lv26/Lv31 exact coefficients.
