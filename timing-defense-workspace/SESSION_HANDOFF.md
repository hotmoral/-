# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Live source branch: `timing-defense-live-v011`
- Current public prototype: **v0.17**
- Public URL: `https://timing-defense-v011.onrender.com/v017.html`
- Current live source HEAD: `8f46b2460f0d16b6103e0f10bec0b5206aa93ae6`
- Current Render deploy: `dep-dbbc3emq1p3s73c29csg` / LIVE

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

Player mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is considered attainable; strong mastery improvement is intended.

Balance governance:
`measure/model → identify specialization/artifact/defect → report → discuss → explicit decision → numerical patch`

---

# Current playable implementation — v0.17

v0.17 layers on top of the stable v0.16 Lv6–21 block.

Files:
- `timing-defense-v011/v017-ux-ai.js`
- `timing-defense-v011/v017.html`

## AI teammate growth parity
AI teammates now internally maintain:
- EXP,
- level,
- skill milestones Lv6/11/16/21,
- timing judgments,
- class skill behavior.

No extra AI Timing Squares are rendered.

AI timing currently uses an internal N/G/P profile approximately 28/54/18, with the heavy fourth attack resolved from two internal judgments rather than a separate arbitrary heavy-tier roll.

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

## Previous v0.16 foundation remains
- Lv6/11/16/21 for all five classes,
- six-slot skill strip,
- exact locked-line Archer collision,
- Tank shield,
- Mage center-excluding Resonance,
- class-specific Lv21 heavy transforms.

v0.16 remains available as rollback/reference:
`https://timing-defense-v011.onrender.com/v016.html`

---

# New approved combat directions after v0.17

## Passive/basic auto-attack
Purpose: allow brief battlefield observation without letting the game play itself.

Leading first experiment from v8:
- 40 raw damage every ~2.0 s,
- no EXP,
- no charge,
- no crit/proc-crit,
- no skill trigger,
- no combo contribution,
- minimal/zero knockback.

Do not offset the passive damage 1:1 with enemy HP.
Current leading ordinary-monster compensation candidate ≈ +8%, because it retains small real breathing room.

This is **not yet live-enabled or frozen**.

## Consecutive PERFECT combo
Frozen semantics:
- only PERFECT increments,
- GOOD/NORMAL/MISS reset,
- attacks 1–3 = one possible increment each,
- heavy X + heavy Y = two possible increments,
- fully PERFECT 1→4 sequence = +5 combo,
- counter is **unbounded**: 20/30/40/50+,
- milestones do not consume/reset combo,
- stage/shop downtime does not itself break combo.

Psychological-pressure principle:
- the visible high streak and valuable reward should make the player nervous,
- **do not secretly shrink timing windows or speed up the sweep** at high combo.

Visual candidate:
- 1–4 small HUD,
- 5+ struck-monster combo number,
- 10/20 stronger presentation,
- 30+ maximum visual tier may plateau while numeric counter continues indefinitely.

Mechanical reward coefficients remain unfrozen. Prefer milestone-triggered class-specific one-off rewards rather than an endlessly stacking permanent multiplier.

See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

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

## v8 — auto-attack/combo diagnostic
Auto 40 / 2.0 s contributes roughly:
- 13.9% of Average timing DPS,
- 10.8% of Skilled,
- 8.8% of Expert.

With +8% ordinary HP candidate, net baseline pace remains slightly easier:
- Average +5.5%,
- Skilled +2.6%,
- Expert +0.7%.

High-combo rarity supports unbounded counting. Approx 150-judgment reach rate:
- Skilled P40: 5 combo 60.9%, 10 combo 0.8%, 20 ~0,
- Expert P65: 10 50.9%, 20 0.8%, 30 0.016%,
- Master-like P80: 20 27.5%, 30 2.9%, 40 0.3%.

These are independence-model diagnostics only; actual human pressure may create more mistakes.

---

# Exact next work boundary

1. Human/device check v0.17:
   - Timing Square fade continuity,
   - four-player spacing,
   - AI skill progression/behavior.
2. Fix implementation defects only.
3. Build the auto-attack + combo **experimental** block from v8 candidate values.
4. Run no-timing / Average / Skilled / Expert comparisons.
5. Simulate several milestone reward strengths before freezing combo rewards.
6. Report/discuss before final HP compensation or reward coefficients.

## Still unresolved
- final auto-attack damage/interval,
- final enemy HP compensation,
- exact 5/10/20/30+ combo mechanical rewards,
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
