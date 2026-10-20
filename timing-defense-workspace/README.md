# Timing Defense — Public Workspace

Persistent planning / balance / simulation / handoff workspace for the Timing Defense prototype.

## Repository layout
- Live playable branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: https://timing-defense-v011.onrender.com
- Current playable prototype: **v0.20**
- Current play page: `https://timing-defense-v011.onrender.com/v020.html`

The workspace branch is separate from the Render deployment branch so documentation/simulation work does not deploy the game.

## New-session read order
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

Older v1–v6 reports remain for historical numerical provenance.

---

# Core project
Timing-action side-defense prototype with five classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

Core rhythm: `X → X → X → X+Y`.
Fourth attack is charged/heavy. Timing judgment drives combat outcome, EXP and class growth.

Implemented automatic skill milestones:
`Lv6 / Lv11 / Lv16 / Lv21`.

Reserved future milestones:
`Lv26 / Lv31`.

---

# Current implementation — v0.20

## Target/turn integrity
- enemies outside the visible viewport cannot be targeted/damaged,
- new Timing Square turns start only while a visible target exists,
- if no target exists at the next-turn boundary the square pauses,
- passive/AI attacks also wait,
- empty turns cannot farm EXP,
- attack input no longer force-spawns an off-screen enemy.

If a valid turn has already started, target disappearance does **not** cancel it:
- current X remains tappable,
- fourth-attack X→Y may finish completely,
- normal judgment/EXP for that already-valid turn remains allowed,
- only the next turn waits.

Target-wait does not reset PERFECT combo.

## Stage intro
Each stage uses:
`STAGE N / READY → fade → combat`.

No movement/spawn/AI/passive/sweep/input runs until the intro has finished.

## HUD/layout polish
- top test descriptor removed; title simplified,
- class selector moved upward,
- combat judgment words moved beside EXP and reduced in size,
- party spacing widened to `.265 / .425 / .585 / .745`, scale `.41`,
- transient tilted combo pop remains near Timing Square.

## Team result board
Rows follow character order and show:
- KILLS
- DMG
- COIN
- LV
- MAX COMBO

Per-column ranks are explicit; v0.20 uses cleaner alignment and compact rank medallions rather than heavy boxes around every value.

See `V020_IMPLEMENTATION_REPORT.md`.

---

# Current experimental combat systems

Passive A/B:
- `40 raw / 2.0 s`,
- no EXP / charge / crit / skill / combo,
- non-boss HP +10%.

PERFECT combo:
- PERFECT only,
- GOOD/NORMAL/MISS reset,
- heavy X/Y count independently,
- numeric streak is unbounded,
- no hidden high-combo timing penalty.

Persistent timing bonus:
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

These are playable A/B values, not production-frozen coefficients.

---

# Encounter framework

Pressure families:
- `S` = Swarm
- `E` = Elite/Heavy
- `X` = Special/Mixed

Tiers use different 1/2/3-pattern distributions rather than forcing all patterns into every stage.

Current Swarm candidate burst envelope:
- S-line 2P/3P/4P = 8 / 11 / 14
- S-cluster = 7 / 10 / 13
- S-scatter = 9 / 12 / 16

Current P95 four-second spawn-density reference:
- 2P ≈ 11
- 3P ≈ 15
- 4P ≈ 18

---

# Working principle
Automated simulation is used for:
- numerical balance,
- growth speed,
- encounter difficulty,
- team-role validation,
- pressure grammar/recipes,
- passive attention-bandwidth calibration,
- combo-reward risk estimation.

Human playtesting is used for:
- feel,
- readability,
- impact,
- UX integrity,
- VFX density,
- subjective fun.

Simulation is diagnostic, not self-authorizing. Large performance gaps must be explained and discussed before numerical live changes.

## Current next boundary
Device/browser validation of v0.20:
- target-wait occurs only at new-turn boundaries,
- in-progress turns survive target disappearance,
- heavy X→Y never cancels midway,
- no empty-turn EXP farming,
- combo survives target-wait,
- stage intro fully gates combat,
- judgment text / party spacing / result table are readable.

After implementation/visual defects are closed, continue the full-run progression simulation before freezing passive/combo/HP coefficients.
