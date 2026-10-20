# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Live source branch: `timing-defense-live-v011`
- Current public LIVE prototype: **v0.17**
- Public LIVE URL: `https://timing-defense-v011.onrender.com/v017.html`
- Current Render deploy: `dep-dbbc3emq1p3s73c29csg` / LIVE
- New v0.18 source HEAD: `8c4314831dd1b1ff6c8fd56d3bbc234ec2c87ed6`
- v0.18 loader: `timing-defense-v011/v018.html`

At the latest Render check, no v0.18 deploy had been created yet. Do not claim v0.18 public-live until Render reports `8c431483...` or later.

The workspace branch is canonical for design decisions, simulation interpretation and new-session recovery. The live branch remains separate.

---

# Frozen combat / progression decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / high-HP normal execution.
- Tank: team-specialist / knockback / wall protection / control; fresh-run solo parity not required.
- Archer: true straight-line geometry; trajectory locks at launch; no off-line retarget/bending.
- Mage: density specialist / AoE / chained explosions.
- Rogue same-target dagger hits are uncapped.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to timing attack results/events.
- Faster clear does not receive compensating EXP merely for fewer attacks.
- Passive basic attacks, if enabled, do not grant EXP.

Player mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is considered attainable; strong mastery improvement is intended.

Balance governance:
`measure/model → identify specialization/artifact/defect → report → discuss → explicit decision → numerical patch`

---

# Current public implementation — v0.17

Files:
- `timing-defense-v011/v017-ux-ai.js`
- `timing-defense-v011/v017.html`

## AI teammate growth parity
AI teammates internally maintain:
- EXP,
- level,
- skill milestones Lv6/11/16/21,
- timing judgments,
- class skill behavior.

No extra AI Timing Squares are rendered.

AI timing currently uses an internal N/G/P profile approximately 28/54/18, with the heavy fourth attack resolved from two internal judgments.

AI class behavior includes:
- Knight Lv6/11/16/21 damage/penetration/knock behavior,
- Rogue Lv6 second dagger, Lv11 native crit, Lv16 recovery shortening, Lv21 five-dagger barrage,
- Tank Lv6 knockback, Lv11 non-stacking Iron Wall, Lv16 shared refresh-only wall shield, Lv21 Ground Impact,
- Archer Lv6/11/16/21 straight-line penetration/triple-shot behavior,
- Mage Lv6/11/16/21 splash/resonance/Greater Orb behavior.

AI EXP comes from its own timing outcomes. It does not receive a visible Timing Square.

## Timing Square continuity
Between timing inputs/projectile/recovery phases:
- the Timing Square remains visible at reduced opacity (~42%),
- charge/location therefore stay continuously readable,
- this applies consistently to attacks 1–4 instead of making 1–3 disappear.

## Party spacing
Slot Y positions are widened slightly to approximately:
`.285 / .405 / .525 / .645`
while character scale remains unchanged.

Intent: improve full-body and weapon silhouette readability without making the party tiny.

---

# v0.18 source implementation — visible combo counter only

Files:
- `timing-defense-v011/v018-combo-ui.js`
- `timing-defense-v011/v018.html`

Implemented source behavior:
- counter appears starting at **1 COMBO**,
- only accepted PERFECT timing judgments increment,
- heavy X and Y each increment separately when PERFECT,
- GOOD / NORMAL / MISS reset to 0,
- number is rendered near the Timing Square rather than at monster impact,
- presentation escalates at 5 / 10 / 20 / 30,
- 30+ visual intensity is capped but numeric combo continues without limit.

This patch has **no combo damage rewards** and **no passive auto-attack** yet.

---

# New approved combat directions

## Passive/basic auto-attack
Purpose: allow brief battlefield observation without letting the game play itself.

Semantic rules:
- no EXP,
- no charge,
- no crit/proc-crit,
- no skill trigger,
- no combo contribution,
- minimal/zero knockback.

Do not offset passive damage 1:1 with enemy HP. Some real breathing room is intentional.

After v8 combat and forced-observation simulation, leading A/B candidate:
- `40 raw damage every 2.0 s`,
- ordinary-monster HP compensation around `+10%`,
- bosses/elites calibrated separately.

This is not frozen production balance and is not live-enabled yet.

## Consecutive PERFECT combo
Frozen semantics:
- only PERFECT increments,
- GOOD / NORMAL / MISS reset,
- attacks 1–3 = one possible increment each,
- heavy X + heavy Y = two possible increments,
- fully PERFECT 1→4 sequence = +5 combo,
- counter is **unbounded**: 20 / 30 / 40 / 50+,
- milestones never consume/reset combo,
- stage/shop downtime does not itself break combo unless later explicitly changed.

Psychological-pressure principle:
- the visible high streak and valuable reward should make the player nervous,
- **do not secretly shrink timing windows or speed up the sweep** at high combo.

Counter presentation:
- visible from 1 combo,
- stays near the Timing Square,
- 1–4 quiet,
- 5–9 mild emphasis,
- 10–19 larger pulse/glow,
- 20–29 stronger frame/impact feedback,
- 30+ presentation can plateau while number continues indefinitely.

Leading mechanical reward candidate after v8:
- 5–9 timing damage +5%,
- 10–19 +8%,
- 20–29 +12%,
- 30+ +15% cap,
- class-specific follow-up at 5 / 10 / 20 / 30 and every +10 after 30,
- 40 / 50 / 60 etc. repeat the 30-tier power rather than scaling forever.

Class language:
- Knight: extra blade/frontline break,
- Rogue: dagger burst,
- Tank: shockwave/protection,
- Archer: extra straight-line shot,
- Mage: secondary explosion.

---

# Simulation status

## v7 — exact v0.16 formula rerun
- Lv21 3P Average/Skilled clear = 81.6 / 96.4%.
- Lv21 4P = 52.8 / 73.6%.
- Rogue remains best durable-normal killer.
- Archer wins line geometry; Mage cluster separation remains close but not a patch trigger.
- No numerical class rebalance authorized.

Files:
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- `combat_exact_v016.py`

## v8 — passive attack / combo calibration
File:
- `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`

### High-combo rarity
Approx 150 judgment opportunities:
- Skilled P40: 5 combo ~61%, 10 ~0.87%, 20 ~0,
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%,
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%.

These are no-pressure independence-model upper bounds; real player tension may make high streaks rarer.

### Combo reward power
Balanced reward-only estimate over ~150 judgments:
- Average mean damage uplift ~0.01%,
- Skilled ~0.26%,
- Expert ~1.99%,
- Master-test P80 ~4.74%.

Therefore mechanical reward can be noticeable at milestones without making ordinary Skilled play explode numerically.

### Passive candidate
40 / 2.0 s = 20 passive raw DPS.
Approx share of no-skill timing DPS:
- Average 13.9%,
- Skilled 10.8%,
- Expert 8.8%.

Leading HP compensation after combat testing: **+10% ordinary HP** for the next A/B, not frozen.

### Continuous-play Lv6 exact-AI-bound check
3P:
- Average 67.9 → 72.4%,
- Skilled 79.2 → 80.9%.

4P:
- Average 54.2 → 56.4%,
- Skilled 58.8 → 62.2%.

### Battlefield-reading test
Forced local timing pause = 2 seconds every 12 seconds.

3P Average:
- current no pause 63.7,
- current + pause 61.3,
- candidate + same pause **65.7%**.

3P Skilled:
- 76.7 → 72.7 → **75.9%**.

4P Average:
- 56.8 → 54.4 → **57.2%**.

4P Skilled:
- 63.0 → 60.8 → **64.2%**.

Interpretation: passive fire recovers most of the gameplay penalty from briefly looking at the battlefield while preserving pressure. This is the strongest evidence for continuing the 40/2s + HP10% experiment.

### Passive-only sanity
Current concrete pressure samples with timing disabled:
- 3P individual-stage clear 0%,
- 4P 0%,
- 2P ~12.2%; surviving 2P clears average only ~357/2000 wall HP.

This is stage-local. Full-run wall carry/progression simulation is still required before final passive values can be frozen.

---

# Exact next work boundary

1. Re-check Render for v0.18 publication.
2. Device/browser check v0.18 counter placement:
   - visible from 1,
   - no overlap with charge / EXP / skill strip,
   - escalation readable at 5 / 10 / 20 / 30,
   - counter reset behavior correct.
3. Do **not** live-enable passive attack or combo reward coefficients solely from v8.
4. Next experimental block candidate:
   - passive 40 / 2.0 s,
   - ordinary HP +10%,
   - 5/8/12/15% combo damage cap,
   - class follow-ups at milestones.
5. Run full-run progression simulation with persistent wall HP and actual level growth before freezing the passive system.
6. Report/discuss before production coefficients are finalized.

## Still unresolved
- final passive attack damage/interval,
- final ordinary/elite/boss HP compensation,
- exact combo milestone proc coefficients and final visuals,
- final E HP/armor package,
- final X hardened values,
- final stage duration,
- human multiplayer cadence/network behavior,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync DUO/TRIPLE/FULL rules,
- final tier count/names/order,
- Lv26/Lv31 coefficients.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `DESIGN_DECISIONS.md`
4. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
5. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
6. `V016_IMPLEMENTATION_REPORT.md`
7. `SKILL_PLAN_LV6_31.md`
8. `TIER_PRESSURE_GRAMMAR_V1.md`
9. `PRESSURE_RECIPES_V1.md`
10. `SIMULATION_METHOD.md`
11. `NEXT_WORK.md`

Older reports remain available for numerical provenance and decision history.
