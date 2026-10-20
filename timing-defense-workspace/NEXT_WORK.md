# Timing Defense — Next Work Boundary

## Current boundary after public v0.17, v0.18 combo-counter source, and v8 simulation

Do **not** freeze passive-attack, combo-reward or enemy-HP values from first impressions.

Required governance:
`implement experiment → simulate/observe → classify intended breathing-room vs role effect vs balance defect → report → discuss → explicit decision → freeze numerical values`

## Current public state
- Public LIVE version: **v0.17**
- URL: `https://timing-defense-v011.onrender.com/v017.html`
- Render deploy: `dep-dbbc3emq1p3s73c29csg` / LIVE

v0.17 includes:
- Timing Square remains visible at reduced opacity between attacks,
- four-player vertical spacing widened slightly,
- AI teammates gain internal EXP/levels and use Lv6/11/16/21 skills,
- AI receives no visible Timing Square.

## v0.18 source state
Source HEAD:
`8c4314831dd1b1ff6c8fd56d3bbc234ec2c87ed6`

Files:
- `timing-defense-v011/v018-combo-ui.js`
- `timing-defense-v011/v018.html`

Implemented source only:
- PERFECT combo visible from **1 COMBO**,
- heavy X/Y count separately,
- GOOD/NORMAL/MISS reset,
- counter stays near Timing Square,
- visual tiers at 5 / 10 / 20 / 30,
- numeric count unbounded above 30.

At the latest check Render had not created a deploy for v0.18. Do not call it public-live until Render reports the new HEAD or later.

No passive attack or numerical combo reward is live-enabled yet.

---

# v8 simulation state — completed

See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

## Leading passive A/B candidate
- `40 raw damage / 2.0 s`,
- no EXP,
- no charge,
- no crit,
- no skill proc,
- no combo contribution,
- minimal/zero knockback,
- ordinary-monster HP compensation **+10% candidate**.

The earlier +8% paper estimate was superseded by combat/observation testing. +10% is now the leading A/B candidate, still not frozen.

### Continuous Lv6 pressure check
3P Average/Skilled:
- current 67.9 / 79.2%,
- candidate 72.4 / 80.9%.

4P:
- current 54.2 / 58.8%,
- candidate 56.4 / 62.2%.

### Battlefield-reading check
Forced timing pause = 2 seconds every 12 seconds.

3P Average: `63.7 → 61.3 → 65.7%`
3P Skilled: `76.7 → 72.7 → 75.9%`
4P Average: `56.8 → 54.4 → 57.2%`
4P Skilled: `63.0 → 60.8 → 64.2%`

Sequence means:
`current no-pause → current with pause → candidate with same pause`.

Conclusion: candidate passive fire recovers most of the penalty from briefly reading the battlefield without collapsing pressure.

### Passive-only sanity
With timing disabled:
- 3P individual-stage clear 0%,
- 4P 0%,
- 2P ~12.2%, with surviving clears averaging only ~357/2000 wall HP.

A full-run wall-carry simulation is still required before final passive values can be frozen.

---

# Combo reward result

## Frozen semantics
- only consecutive PERFECT judgments count,
- GOOD/NORMAL/MISS reset,
- normal attacks = +1 opportunity,
- heavy X and Y = +1 each,
- fully PERFECT 1→4 sequence = +5,
- counter is unbounded,
- milestones never consume/reset the counter,
- no hidden timing-window/sweep-speed penalty at high combo,
- visual counter begins at 1 near the Timing Square.

## High-combo rarity
Approx 150 judgment opportunities:
- Skilled P40: 5 ~61%, 10 ~0.87%, 20 ~0,
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%,
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%.

## Leading mechanical candidate
Persistent timing damage:
- 5–9 +5%,
- 10–19 +8%,
- 20–29 +12%,
- 30+ +15% cap.

Class-specific milestone follow-up:
- 5 small,
- 10 medium,
- 20 strong,
- 30 maximum,
- every +10 after 30 repeats the 30-tier mechanical strength.

Reward-only mean total-damage uplift over ~150 judgments:
- Average ~0.01%,
- Skilled ~0.26%,
- Expert ~1.99%,
- Master-test P80 ~4.74%.

Therefore reward strength can remain visible/meaningful without ordinary Skilled play numerically exploding.

---

# Immediate next execution slice

1. Re-check Render for v0.18 deployment.
2. Device/readability check v0.18 counter:
   - 1 COMBO visible immediately,
   - no overlap with charge/EXP/skill strip,
   - 5/10/20/30 visual escalation legible,
   - reset behavior correct.
3. Build the first **passive + combo-reward A/B block** only after the v0.18 counter UI is visually acceptable.
4. Candidate A/B numbers:
   - passive 40 / 2.0 s,
   - ordinary HP +10%,
   - combo 5/8/12/15% cap,
   - class milestone follow-ups.
5. Run a full-run progression model with:
   - wall HP carried between stages,
   - actual player/AI level growth,
   - passive-only / Average / Skilled / Expert comparisons.
6. Report/discuss before production values are frozen.

---

# Accepted encounter state remains unchanged
Pressure grammar:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Current candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

Current P95 4-second spawn-density reference:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

Do not retune pressure recipes merely because the passive/combo experiment exists.

## Still not frozen
- final passive attack damage/interval,
- final ordinary/elite/boss HP compensation,
- exact combo milestone proc coefficients/final visuals,
- final E HP/armor package,
- final X hardened multipliers,
- exact stage duration,
- final tier number/names/order,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- human multiplayer cadence/network behavior,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients.
