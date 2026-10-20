# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Public repo: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning/balance/handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.17**
- Public LIVE URL: `https://timing-defense-v011.onrender.com/v017.html`
- Current Render deploy: `dep-dbbc3emq1p3s73c29csg` / LIVE
- New v0.18 source loader exists on live branch, but at the latest check Render had not created a new deploy for it yet.
- v0.18 source HEAD: `8c4314831dd1b1ff6c8fd56d3bbc234ec2c87ed6`

## Current playable scope
- Landscape mobile/browser timing-defense prototype.
- Fixed player near left wall; monsters approach from right.
- Rhythm: `X → X → X → X+Y`.
- Judgments: NORMAL / GOOD / PERFECT plus HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Team controls: solo through +3 AI.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Current playable Stage 1–10 prototype.
- Run-only EXP / level / coin / shop upgrades.
- Playable skill implementation reaches Lv21.

## Growth structure
Automatic skill unlocks:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Implemented now:
`Lv6 / Lv11 / Lv16 / Lv21`

Lv21 is intentionally the first major fourth-attack transformation milestone. Lv26/Lv31 remain planned only.

## Frozen class / progression decisions
- Archer = true straight-line geometry; launch trajectory is fixed and cannot retarget off-line.
- Tank = team-specialist; fresh-run solo parity is not required.
- Rogue repeated dagger hits on the same target are uncapped.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to timing attack events/results.
- Faster clear does not receive compensating EXP merely because it generates fewer attacks.
- Passive basic attacks, if enabled, do not grant EXP.
- Simulation never self-authorizes a live numerical balance patch.

## Player mastery reference
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is considered attainable; strong Average→Skilled improvement is intended.

---

# Current public changes — v0.17

v0.17 intentionally avoids auto-attack/combo numerical balance changes and applies only approved system/UX changes.

### AI teammate growth parity
AI teammates internally carry:
- independent EXP,
- independent level,
- automatic Lv6/11/16/21 unlocks,
- internally simulated timing judgments,
- class skill behavior including Rogue barrage, Tank protection, Archer line mechanics and Mage burst/resonance.

No additional AI Timing Squares are rendered.

### Timing Square continuity
- After a timing input the square no longer disappears during projectile/recovery.
- It remains visible at reduced opacity (~42%) until the next active timing pass.
- Charge/location information therefore remains continuously anchored.

### Party spacing
- Four-character vertical spacing is widened slightly from v0.16.
- Character scale is preserved so the intent is more full-body/weapon readability rather than simply shrinking everyone.

Source files:
- `timing-defense-v011/v017-ux-ai.js`
- `timing-defense-v011/v017.html`

---

# v0.18 source state — combo counter only

Source files:
- `timing-defense-v011/v018-combo-ui.js`
- `timing-defense-v011/v018.html`

Implemented source behavior:
- PERFECT combo counter appears from **1 COMBO**,
- only accepted PERFECT timing judgments increment it,
- heavy X and heavy Y each count independently,
- GOOD / NORMAL / MISS reset to zero,
- counter is positioned near the Timing Square,
- visual emphasis steps at 5 / 10 / 20 / 30,
- visual intensity caps at 30+, numeric counter does not cap.

No passive basic attack, enemy-HP compensation, or numerical combo reward is included in v0.18 source yet.

At latest check, Render still showed v0.17 as the public LIVE deploy. Do not claim v0.18 public-live until a Render deploy contains `8c431483...` or later.

---

# Simulation / design history

## v1 — role separation
Established the intended class-role split.

## v2 — Stage 1–10 + run shop
Resolved Archer straight-line semantics, Tank team specialization and EXP/attack-count coupling.

## v3 — mastery curve
Confirmed meaningful Average→Skilled improvement.

## v4 — team composition
Confirmed Tank defensive utility, Rogue durable-normal niche, Archer-line/Mage-density split and Knight generalist value.

## v5 — Tier Pressure Grammar
Future 50-stage tier grammar:
- `S` Swarm,
- `E` Elite/Heavy,
- `X` Special/Mixed.

Representative five-tier distribution:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

## v6 — concrete pressure recipes
Candidate Swarm burst sizes:
- line 2P/3P/4P = `8 / 11 / 14`,
- cluster = `7 / 10 / 13`,
- scatter = `9 / 12 / 16`.

X remains the main co-op scaling language; E is an effective durability budget.

## v7 — exact v0.16 formula re-run
Key Lv21 clear bounds:
- 3P Average/Skilled = 81.6 / 96.4%,
- 4P = 52.8 / 73.6%.

Rogue retains best durable-normal TTK. Archer remains strongest on line geometry. No numerical class rebalance authorized.

Files:
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- `combat_exact_v016.py`

## v8 — latest: passive basic attack + unbounded PERFECT combo
Approved semantic direction:
- passive basic attack exists to buy attention bandwidth, not replace timing play,
- consecutive PERFECT combo is unbounded,
- combo is visible from 1 near the Timing Square,
- visual strength may cap at 30+ while the number keeps increasing,
- no hidden timing-window/sweep-speed punishment at high combo.

### Combo rarity
Around 150 judgment opportunities:
- Skilled P40: 5 combo ~61%, 10 ~0.87%, 20 essentially 0,
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%,
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%.

This supports 30/40 being rare, high-tension events rather than routine rotations.

### Leading combo-power candidate
Persistent timing damage while streak survives:
- 5–9 +5%,
- 10–19 +8%,
- 20–29 +12%,
- 30+ +15% cap.

Class-specific milestone follow-ups at 5 / 10 / 20 / 30 and every +10 thereafter, with mechanical strength capped at the 30 tier.

Reward-only Monte Carlo mean damage uplift over ~150 judgments:
- Average ~0.01%,
- Skilled ~0.26%,
- Expert ~1.99%,
- Master-test P80 ~4.74%.

### Leading passive-attack A/B candidate after combat simulation
- `40 raw damage / 2.0 s`,
- no EXP / crit / charge / skill / combo,
- ordinary-monster HP compensation around `+10%` as a **test candidate**, not frozen production value.

No-skill passive share:
- ~13.9% of Average timing DPS,
- ~10.8% of Skilled,
- ~8.8% of Expert.

### Continuous-play Lv6 pressure check
3P Average/Skilled:
- baseline 67.9 / 79.2%,
- passive40/2s + HP10% + balanced combo 72.4 / 80.9%.

4P:
- baseline 54.2 / 58.8%,
- candidate 56.4 / 62.2%.

### Battlefield-reading pause check
Forced local pause: 2 seconds every 12 seconds.

3P Average:
- no pause/current 63.7%,
- pause/current 61.3%,
- pause + candidate 65.7%.

3P Skilled:
- 76.7 → 72.7 → 75.9%.

4P Average:
- 56.8 → 54.4 → 57.2%.

4P Skilled:
- 63.0 → 60.8 → 64.2%.

Interpretation: the passive attack recovers most of the penalty from deliberately looking at the battlefield without collapsing overall pressure. This is the strongest reason to continue with the 40/2s + HP10% A/B candidate.

Passive-only sanity check under current pressure samples:
- 3P = 0% individual-stage clear,
- 4P = 0%,
- 2P ~12.2%, mostly because the wall barely survives; cleared 2P samples averaged only ~357/2000 wall HP.

See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

---

# Current next boundary

1. Confirm whether Render publishes v0.18 source.
2. Device/browser check v0.18 combo-counter placement and visual escalation.
3. Keep combo reward and passive auto-attack numbers out of live balance until the A/B block is explicitly implemented.
4. Next playable A/B candidate:
   - passive 40 / 2.0 s,
   - ordinary HP +10%,
   - combo 5/8/12/15% persistent cap + class milestone follow-ups.
5. Run full-run progression simulation with wall HP carried between stages before freezing passive value; the current passive-only check is stage-local.
6. Report/discuss before final monster-HP or reward coefficients are frozen.

## Still not frozen
- final passive attack interval/damage,
- final HP compensation and elite/boss handling,
- exact combo milestone visual/proc coefficients,
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- true human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync-bonus implementation,
- final number/names/order of tiers,
- Lv26/Lv31 exact coefficients.
