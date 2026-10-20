# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Public repository: `hotmoral/-`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Live source branch: `timing-defense-live-v011`
- Current public LIVE prototype: **v0.20**
- Public URL: `https://timing-defense-v011.onrender.com/v020.html`
- Live source HEAD: `d5c0e5cb90e8e5aa99c7420beb96202563f07e46`
- Render deploy: `dep-dbbdpd49v7es73esaet0` / LIVE

Workspace is canonical for design decisions, simulation interpretation, and new-session recovery. Live branch remains separate.

---

# Frozen combat / role decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank: team-specialist / knockback / wall protection; fresh-run solo parity not required.
- Archer: true straight-line geometry; launch path locks; no off-line retarget/bending.
- Mage: density/AoE specialist.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to timing results/events.
- Passive basic attacks grant no EXP.

Player mastery reference:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

Balance governance:
`measure/model → identify specialization/artifact/defect → report → discuss → explicit decision → production patch`

---

# Current playable implementation — v0.20

v0.20 retains all v0.18 passive/combo A/B coefficients and v0.19 visible-target/combo/result systems, then fixes turn-boundary combat flow and screen organization.

Files:
- `timing-defense-v011/v020-flow-ui.js`
- `timing-defense-v011/v020-results.js`
- `timing-defense-v011/v020.html`

See `V020_IMPLEMENTATION_REPORT.md`.

## Turn-boundary target rule
A **new** local Timing Square turn starts only when a valid visible monster exists.

If no visible target exists at a turn boundary:
- phase becomes target-wait,
- Timing Square sweep is paused,
- passive attack does not fire,
- AI does not attack/earn attack XP,
- no empty local timing turn starts.

Critical continuity rule:
- if a turn already began while a visible target existed, it remains valid until the whole timing turn ends,
- target disappearance during the moving needle never cancels that turn,
- normal attacks may still be tapped,
- fourth-attack X may still proceed to Y and finish,
- normal timing judgment/EXP for that already-valid turn remains allowed,
- only the next turn waits if no target is visible.

This prevents teammate/passive kills from making the Timing Square appear to hitch or ignore input.

Stage clear/shop or final clear is deferred while such a valid local turn is still active; natural timeout remains allowed.

Waiting for the next target does **not** reset combo.

## Visible-target integrity
- not-yet-visible enemies cannot be targeted/damaged,
- pierce/AoE spill obeys the same visibility rule,
- unseen kills cannot produce rewards,
- attack input no longer force-spawns off-screen enemies.

## Stage intro
Every stage now enters an intro gate:
`STAGE N / READY → fade out → combat starts`.

Current duration ≈ 1050 ms.
During intro there is no spawn/movement, AI/passive attack, Timing Square sweep, or input.
Combo is preserved.

## HUD/layout
- top title simplified to `TIMING DEFENSE`,
- class selector moved upward,
- GOOD/PERFECT/CRITICAL/heavy judgment text moved beside the EXP gauge and reduced in size,
- four-player slot Y widened to `.265 / .425 / .585 / .745`, scale `.41`,
- v0.19 transient combo pop remains unchanged because device feedback said it felt right.

## End-run results
Rows remain character order: YOU / CPU1 / CPU2 / CPU3.
Metrics remain:
- KILLS
- DMG
- COIN
- LV
- MAX COMBO

v0.20 cleans the board with fixed alignment, lighter row bands, compact rank medallions and clearer per-column rank emphasis.

---

# Current experimental combat values — not frozen

Passive:
- `40 raw / 2.0 s`,
- no EXP / charge / crit / skill / combo,
- non-boss HP compensation +10%.

PERFECT combo:
- only PERFECT increments,
- GOOD/NORMAL/MISS reset,
- heavy X/Y separate,
- unbounded count,
- no hidden difficulty escalation.

Persistent bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone budgets:
- 5 = 60
- 10 = 90
- 20 = 150
- 30+ = 210 cap
- every +10 after 30 repeats 30-tier power.

---

# Device feedback already accepted

From v0.18/v0.19 Android play:
- passive fire meaningfully creates battlefield-reading room,
- visible combo count materially improves tension/game feel,
- transient combo popup is preferred over a persistent box,
- off-screen targeting/empty EXP was confusing and led to v0.20 target-gating rule,
- wider party spacing and cleaner end-run table are desired.

This feedback authorized UX/integrity work, not numerical retuning.

---

# Simulation state

## v7 exact v0.16 rerun
- Lv21 3P Average/Skilled clear = 81.6 / 96.4%.
- Lv21 4P = 52.8 / 73.6%.
- Rogue remains best durable-normal killer.
- Archer wins line geometry.
- No numerical class rebalance authorized.

## v8 passive/combo calibration
High-combo rarity around 150 judgments:
- Skilled P40: 5 ~61%, 10 ~0.87%, 20 ~0.
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%.
- Master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%.

Forced battlefield-reading pause (2 s every 12 s):
- 3P Average: `63.7 → 61.3 → 65.7%`
- 3P Skilled: `76.7 → 72.7 → 75.9%`
- 4P Average: `56.8 → 54.4 → 57.2%`
- 4P Skilled: `63.0 → 60.8 → 64.2%`

Sequence = no pause → same game with pause → passive40/2s + HP10% with same pause.

---

# Encounter framework remains accepted

Pressure families:
- S = Swarm
- E = Elite/Heavy
- X = Special/Mixed

1/2/3-pattern stages are all valid; all three are not forced into every stage.

Current Swarm candidate bursts:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

---

# Exact next work boundary

1. Human/device/browser test public v0.20.
2. Verify target-wait begins only at a **new-turn boundary**.
3. Kill the final visible target with AI/passive while the local needle is moving and verify the current turn continues normally.
4. Specifically verify heavy X→Y is never cancelled mid-turn by target disappearance.
5. Verify no empty-turn EXP farming exists.
6. Verify target-wait does not break combo.
7. Verify `STAGE N / READY` fully disappears before combat starts.
8. Verify judgment text placement, four-character spacing, class-selector position and end-run table readability.
9. Fix implementation/visual defects only.
10. Then continue full-run progression simulation before production-freezing passive/HP/combo coefficients.

## Still unresolved / not production-frozen
- final passive attack damage/interval,
- final ordinary/elite/boss HP compensation,
- final combo persistent coefficients,
- final milestone proc coefficients/visuals,
- final result-board metric set,
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
3. `V020_IMPLEMENTATION_REPORT.md`
4. `V019_IMPLEMENTATION_REPORT.md`
5. `V018_IMPLEMENTATION_REPORT.md`
6. `DESIGN_DECISIONS.md`
7. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
8. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
9. `V016_IMPLEMENTATION_REPORT.md`
10. `SKILL_PLAN_LV6_31.md`
11. `TIER_PRESSURE_GRAMMAR_V1.md`
12. `PRESSURE_RECIPES_V1.md`
13. `SIMULATION_METHOD.md`
14. `NEXT_WORK.md`
