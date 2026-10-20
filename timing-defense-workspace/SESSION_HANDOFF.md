# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Live source branch: `timing-defense-live-v011`
- Current public LIVE prototype: **v0.18**
- Public URL: `https://timing-defense-v011.onrender.com/v018.html`
- Live source HEAD: `bacc0b86e356e003bdf697187ff6ea313130fc73`
- Render deploy: `dep-dbbcntjbc2fs73anb9rg` / LIVE

Workspace is canonical for design decisions, simulation interpretation, and new-session recovery. Live branch remains separate.

---

# Frozen combat / progression decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / durable-normal execution.
- Tank: team-specialist / knockback / wall protection / control; fresh-run solo parity not required.
- Archer: true straight-line geometry; launch path locks; no off-line retarget/bending.
- Mage: density specialist / AoE / chained explosions.
- Rogue same-target dagger hits are uncapped.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to timing attack results/events.
- Faster clear does not receive compensating EXP merely for fewer attacks.
- Passive basic attacks do not grant EXP.

Player mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.
- Skilled is considered attainable; strong mastery improvement is intended.

Balance governance:
`measure/model → identify specialization/artifact/defect → report → discuss → explicit decision → production freeze/patch`

---

# Current playable implementation — v0.18

v0.18 layers on the v0.17 AI/UX changes and v0.16 Lv6–21 skill block.

## Foundation retained
- Lv6 / 11 / 16 / 21 skills implemented for all five classes.
- Six-slot skill strip reserves Lv26 / Lv31.
- Archer locked-line collision.
- Tank shield and wall mitigation.
- Mage center-excluding Resonance.
- AI internal EXP/level/skill growth; no visible AI Timing Squares.
- Timing Square remains visible at ~42% opacity during projectile/recovery.
- Four-player spacing widened to approx `.285/.405/.525/.645`.

## PERFECT combo
- Visible from **1 COMBO** near Timing Square.
- Only PERFECT increments.
- GOOD / NORMAL / MISS reset.
- Heavy X/Y are separate combo judgments.
- Counter unbounded: 20 / 30 / 40 / 50+.
- Milestones never consume/reset streak.
- No hidden timing-window shrink or sweep acceleration.
- Visual tiers: 1–4 / 5–9 / 10–19 / 20–29 / 30+.
- 30+ visual intensity may plateau while number continues indefinitely.

### Experimental persistent bonus
- 5–9: +5%
- 10–19: +8%
- 20–29: +12%
- 30+: +15% cap

### Experimental milestone follow-up
Milestones:
- 5,
- 10,
- 20,
- 30,
- every +10 thereafter.

Raw-equivalent first-playable budgets:
- 5 = 60
- 10 = 90
- 20 = 150
- 30+ = 210 cap

Class language:
- Knight: extra blade/frontline break.
- Rogue: dagger burst.
- Tank: local shockwave follow-up.
- Archer: extra straight-line shot.
- Mage: compact secondary explosion.

## Passive basic attack — experimental
- `40 raw / 2.0 s`.
- local player only in current A/B implementation.
- no EXP.
- no charge.
- no crit/proc crit.
- no skill trigger.
- no combo contribution.
- knockback suppressed.

## Enemy compensation — experimental
- non-boss spawned monsters receive `+10% HP`.
- bosses are not automatically given the same +10%.
- compensation is intentionally below full passive-DPS equivalence so the system actually creates attention bandwidth.

Files:
- `timing-defense-v011/v018-combo-ui.js`
- `timing-defense-v011/v018-auto-combo.js`
- `timing-defense-v011/v018.html`

See `V018_IMPLEMENTATION_REPORT.md`.

---

# v8 simulation evidence behind v0.18 A/B

See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

## High-combo rarity (~150 judgments)
- Skilled P40: 5 ~61%, 10 ~0.87%, 20 ~0.
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%.
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%.

These are independent-probability upper bounds; real psychological pressure may make high streaks rarer.

## Combo reward average uplift
- Average ~0.01%
- Skilled ~0.26%
- Expert ~1.99%
- Master-test P80 ~4.74%

## Passive contribution
40 / 2.0 s = 20 raw DPS, about:
- 13.9% of Average no-skill timing DPS,
- 10.8% of Skilled,
- 8.8% of Expert.

## Battlefield-reading test
Forced timing pause = 2 s every 12 s.

3P Average: `63.7 → 61.3 → 65.7%`
3P Skilled: `76.7 → 72.7 → 75.9%`
4P Average: `56.8 → 54.4 → 57.2%`
4P Skilled: `63.0 → 60.8 → 64.2%`

Sequence = current no pause → current with pause → candidate with same pause.

Interpretation: passive fire recovers most of the attention cost of checking the battlefield while retaining timing as the dominant source of power.

Passive-only stage sanity:
- 3P = 0% clear,
- 4P = 0%,
- 2P ~12.2%, with ~357/2000 average surviving wall HP among those rare clears.

---

# Encounter framework remains accepted

Pressure families:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Rules:
- X is primary co-op scaling language.
- S/E are time-separated spike tools.
- 1/2/3-pattern stages are all valid.
- all three are not forced into every stage.
- tier identity comes from frequency, ratio, timing, geometry, intensity and overlap.

Current candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

---

# Exact next work boundary

1. Human/device/browser check public v0.18.
2. Verify combo counter placement relative to charge, EXP and skill strip.
3. Verify 1 COMBO appears immediately; X/Y and reset semantics are exact.
4. Verify passive projectile cadence/visual weakness and no EXP/charge/combo side effects.
5. Verify 5/10/20 milestone attacks are class-distinct and readable.
6. Verify non-boss +10% HP does not make ordinary enemies feel sponge-like.
7. Run full-run progression simulation with wall HP carried stage-to-stage before production-freezing passive/HP values.
8. Report/discuss before revising experimental coefficients.

## Still unresolved / not production-frozen
- final passive attack damage/interval,
- final ordinary/elite/boss HP compensation,
- final persistent combo bonus coefficients,
- final milestone proc coefficients/visuals,
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
3. `V018_IMPLEMENTATION_REPORT.md`
4. `DESIGN_DECISIONS.md`
5. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
6. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
7. `V016_IMPLEMENTATION_REPORT.md`
8. `SKILL_PLAN_LV6_31.md`
9. `TIER_PRESSURE_GRAMMAR_V1.md`
10. `PRESSURE_RECIPES_V1.md`
11. `SIMULATION_METHOD.md`
12. `NEXT_WORK.md`
