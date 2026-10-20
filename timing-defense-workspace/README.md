# Timing Defense — Public Workspace

This directory is the persistent planning / balance / simulation / handoff workspace for the Timing Defense prototype.

## Repository layout
- Live playable code branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: https://timing-defense-v011.onrender.com
- Current playable prototype: **v0.19**
- Current play page: `https://timing-defense-v011.onrender.com/v019.html`

The workspace branch is separated from the Render deployment branch so analysis/documentation work does not deploy automatically.

## New-session read order
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

Older v1–v6 reports remain available for historical reasoning and numerical provenance.

## Core project
Timing-action side-defense prototype with five classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

Core rhythm is `X → X → X → X+Y`. The fourth attack is charged/heavy. Timing judgment drives combat outcome, EXP and class growth.

## Working principle
Automated simulation is used for:
- numerical balance,
- growth speed,
- encounter difficulty,
- team-role validation,
- tier encounter grammar,
- concrete spawn-recipe calibration,
- passive/attention-bandwidth calibration,
- combo-reward risk estimation.

Human playtesting is reserved for feel, readability, impact, VFX density and subjective fun.

Simulation is diagnostic, not self-authorizing. A measured gap must be explained and discussed before numerical live balance changes.

---

# Current implementation — v0.19

## Multi-skill foundation
Implemented automatic skill milestones:
`Lv6 / Lv11 / Lv16 / Lv21`.

HUD reserves:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.

Frozen class mechanics include:
- Rogue same-target dagger hits uncapped.
- Boss dagger scalar 0.70.
- Boss knockback scalar 0.40.
- Tank wall/control kit through Lv21.
- Mage center-excluding Resonance and Lv21 orb.
- Archer fixed straight-line trajectories.

## AI teammate parity
AI teammates internally gain EXP, levels and Lv6/11/16/21 skills without visible Timing Squares.

## Passive / PERFECT combo A/B
Current experimental playable values retained from v0.18:
- passive = `40 raw / 2.0 s`,
- no passive EXP / charge / crit / skill / combo,
- non-boss HP +10%,
- combo persistent bonus = +5 / +8 / +12 / +15% at 5 / 10 / 20 / 30+,
- milestone follow-ups at 5 / 10 / 20 / 30 / every +10 after 30,
- combo count itself is unbounded.

These are not production-frozen values.

## v0.19 UX/integrity changes
- not-yet-visible enemies cannot be targeted or damaged,
- unseen kills therefore cannot award kill coin,
- four-player spacing widened to approx `.255 / .405 / .555 / .705`,
- combo is no longer a persistent boxed HUD; each PERFECT produces a short tilted pop near the Timing Square,
- clear/game-over screen now shows a team contribution table in character order with per-category rankings.

Current result columns:
- KILLS
- DMG
- COIN
- LV
- MAX COMBO

Rank language:
1st gold / 2nd silver / 3rd bronze / 4th muted.

See `V019_IMPLEMENTATION_REPORT.md`.

---

# Encounter framework

Pressure families:
- `S` = Swarm
- `E` = Elite/Heavy
- `X` = Special/Mixed

The game does not force all three into every stage. Tier identity comes from 1/2/3-pattern ratios, S/E/X frequency, geometry, event timing, intensity and overlap.

Current candidate Swarm burst envelope:
- S-line 2P/3P/4P = 8 / 11 / 14
- S-cluster = 7 / 10 / 13
- S-scatter = 9 / 12 / 16

Current candidate P95 four-second spawn density:
- 2P ≈ 11
- 3P ≈ 15
- 4P ≈ 18

X carries most multiplayer scaling through role-bearing composition. E is an effective durability budget rather than one giant mandatory HP bar.

---

# Latest balance analysis — v8

v8 evaluated passive basic attack + unbounded PERFECT combo.

Key conclusions:
- 40/2.0s passive creates measurable battlefield-reading breathing room,
- passive-only does not sustain normal 3P/4P stage completion in the tested pressure samples,
- 30/40 combo is naturally rare enough to function as a high-tension prestige event,
- balanced combo rewards add little average power to ordinary Skilled play and do not numerically explode.

User device feedback on v0.18 confirmed:
- game feel improved,
- combo count creates real tension,
- passive attack provides time to inspect the battlefield.

No production balance freeze has been made from that feedback.

## Current next boundary
Device/browser validation of v0.19:
- visible-target correctness,
- wider character spacing,
- transient combo pop placement/readability,
- end-run table/rank readability.

Fix implementation/visual defects first. Continue full-run progression simulation before freezing passive/combo/HP coefficients.
