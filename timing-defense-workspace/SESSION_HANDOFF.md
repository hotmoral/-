# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Live source branch: `timing-defense-live-v011`
- Current public LIVE prototype: **v0.19**
- Public URL: `https://timing-defense-v011.onrender.com/v019.html`
- Live source HEAD: `0e51e172dc1ea11a78e67eb62c557d9ac4c373bc`
- Render deploy: `dep-dbbd6duq1p3s73c659cg` / LIVE

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

# Current playable implementation — v0.19

v0.19 keeps the v0.18 passive/combo A/B values unchanged and adds targeting integrity + presentation/results UX.

## Foundation retained
- Lv6 / 11 / 16 / 21 skills for all five classes.
- Six-slot skill strip reserves Lv26 / Lv31.
- Archer locked-line collision.
- Tank shield/wall mitigation.
- Mage center-excluding Resonance.
- AI internal EXP/level/skill growth; no visible AI Timing Squares.
- Timing Square remains visible at reduced opacity during projectile/recovery.

## Passive basic attack — experimental
- local passive = `40 raw / 2.0 s`.
- no EXP / charge / crit / skill proc / combo contribution.
- knockback suppressed.
- non-boss monsters +10% HP.

## PERFECT combo — experimental power, frozen semantics
- only PERFECT increments.
- GOOD / NORMAL / MISS reset.
- heavy X/Y count separately.
- counter unbounded.
- no hidden high-combo timing penalty.

Persistent bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone follow-ups:
- 5 / 10 / 20 / 30 / every +10 after 30.
- raw-equivalent budgets 60 / 90 / 150 / 210 cap.

## v0.19 visible-target rule
Legacy targeting could select monsters still beyond the right edge because they had already spawned.

v0.19:
- nearest-target selection ignores enemies until their aim point enters the viewport,
- damage, pierce and AoE spill to not-yet-visible enemies are rejected,
- therefore unseen kills cannot award kill coin,
- an input may still fire an empty attack if no visible target exists.

This is a gameplay-integrity correction, not a numerical balance change.

## v0.19 character spacing
Slot Y candidate:
`.255 / .405 / .555 / .705`

Character scale remains `.41`.
The temporary prototype mode controls are not treated as production layout constraints.

## v0.19 combo presentation
The old persistent rectangular combo display is not used in v0.19.

Instead:
- every PERFECT produces a short popup near the Timing Square,
- visible from `1 COMBO!`,
- slightly tilted and scaled/punched in,
- fades after roughly 460 ms,
- no combo box remains between hits,
- 5 / 10 / 20 / 30+ increase visual emphasis,
- numeric streak remains unbounded above 30.

## v0.19 end-run team contribution board
On clear/game-over, rows follow character order:
1. YOU
2. CPU 1
3. CPU 2
4. CPU 3

Columns:
- KILLS
- DMG
- COIN (kill-reward contribution)
- LV
- MAX COMBO

Every metric receives explicit 1..N ranking.
- 1st gold
- 2nd silver
- 3rd bronze
- 4th muted blue-gray

The board tracks per-slot damage/kills/kill-coin and AI internal PERFECT/max-streak data. Local max combo comes from the actual timing-combo state.

Files:
- `timing-defense-v011/v019-combo-pop.js`
- `timing-defense-v011/v019-ux-results.js`
- `timing-defense-v011/v019.html`

See `V019_IMPLEMENTATION_REPORT.md`.

---

# Device feedback that led to v0.19

User played v0.18 on landscape Android and reported:
- game feel clearly improved,
- visible combo count creates useful tension,
- passive fire gives some time to inspect the battlefield,
- persistent combo HUD was too static/box-like,
- party still felt too tightly packed,
- attacks seemed to hit enemies outside the visible screen,
- Stage 10 clear presentation was promising and should expand into per-player contribution rankings.

This feedback authorized UX/integrity implementation, not numerical retuning.

---

# Simulation status

## v7 — exact v0.16 formula rerun
- Lv21 3P Average/Skilled clear = 81.6 / 96.4%.
- Lv21 4P = 52.8 / 73.6%.
- Rogue remains best durable-normal killer.
- Archer wins line geometry; no numerical class rebalance authorized.

## v8 — passive / combo calibration
See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

High-combo rarity around 150 judgments:
- Skilled P40: 5 ~61%, 10 ~0.87%, 20 ~0.
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%.
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%.

Mean combo reward uplift:
- Average ~0.01%
- Skilled ~0.26%
- Expert ~1.99%
- Master-test P80 ~4.74%

Forced battlefield-reading pause (2s every 12s):
- 3P Average: `63.7 → 61.3 → 65.7%`
- 3P Skilled: `76.7 → 72.7 → 75.9%`
- 4P Average: `56.8 → 54.4 → 57.2%`
- 4P Skilled: `63.0 → 60.8 → 64.2%`

Sequence = current no pause → current with pause → passive40/2s + HP10% with same pause.

---

# Encounter framework remains accepted

Pressure families:
- S = Swarm
- E = Elite/Heavy
- X = Special/Mixed

Rules:
- X is primary co-op scaling language.
- S/E are time-separated spike tools.
- 1/2/3-pattern stages are all valid.
- all three are not forced into every stage.
- tier identity comes from frequency, ratio, timing, geometry, intensity and overlap.

Current candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

---

# Exact next work boundary

1. Human/device/browser check public v0.19.
2. Confirm unseen enemies receive no damage/kill reward.
3. Check widened party spacing/full-body readability.
4. Check transient combo popup position, tilt, scale, fade and overlap.
5. Check result-board density/ranking on landscape Android.
6. Decide whether KILLS / DMG / COIN / LV / MAX COMBO is the right first metric set.
7. Fix implementation/visual defects only.
8. Continue full-run progression simulation before production-freezing passive/HP/combo numbers.

## Still unresolved / not production-frozen
- final passive attack damage/interval,
- final ordinary/elite/boss HP compensation,
- final persistent combo bonus coefficients,
- final milestone proc coefficients/visuals,
- final result-board metric/presentation set,
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
3. `V019_IMPLEMENTATION_REPORT.md`
4. `V018_IMPLEMENTATION_REPORT.md`
5. `DESIGN_DECISIONS.md`
6. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
7. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
8. `V016_IMPLEMENTATION_REPORT.md`
9. `SKILL_PLAN_LV6_31.md`
10. `TIER_PRESSURE_GRAMMAR_V1.md`
11. `PRESSURE_RECIPES_V1.md`
12. `SIMULATION_METHOD.md`
13. `NEXT_WORK.md`
