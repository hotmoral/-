# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Current playable version
- Prototype: `v0.15`
- URL: https://timing-defense-v011.onrender.com/v015.html
- Render service: `timing-defense-v011`
- Live deployment branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`

## Current implemented scope
- Landscape mobile/browser defense prototype.
- Local player fixed near left-side wall; monsters approach from the right.
- Local timing input uses one Timing Square.
- Attack rhythm: X → X → X → X+Y.
- Judgments: NORMAL / GOOD / PERFECT and heavy HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL.
- Five classes: Knight / Rogue / Tank / Archer / Mage.
- Team controls: solo through +3 AI.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Current playable stage prototype: 1–10.
- Run-only EXP / level / coin / shop system.
- Current live skill layer: Lv6 only.

## Planned growth structure
Automatic skill unlocks:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Lv21 is the first major fourth-attack transformation point. Lv31 P×P CRITICAL is intended to become the class-signature finisher.

## Frozen class/balance decisions
- Archer penetration is true straight-line geometry only.
- Tank is team-specialized; fresh-run solo Stage-10 parity is not required.
- Rogue has no same-target dagger hit cap.
- Boss dagger damage scalar starting value: 0.70.
- Boss knockback scalar starting value: 0.40.
- EXP remains tied to timing attack results/events.
- Faster-clearing classes are not automatically compensated for fewer attack events.
- Simulation is diagnostic. Report/discuss before any numerical live patch.

## Player-skill interpretation
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 with modestly faster commitment.

Skilled is treated as an attainable learned-player state. Strong improvement from Average → Skilled is desirable.

## Simulation status

### v1 — role separation
Established the intended class identity split.

### v2 — Stage 1–10 + run shop
Exposed and resolved the Archer auto-chain artifact, Tank solo/team interpretation and EXP/attack-count coupling.

### v3 — mastery curve
Confirmed a useful Average→Skilled progression. No live change.

### v4 — team composition
13,780 deliberate runs.

Key result:
- Tank team utility is real under pressure.
- Rogue durable-normal niche is real.
- Archer and Mage remain line-vs-density distinct.
- Knight remains a useful stabilizer.
- current unscaled Stage 1–10 waves saturate with 3–4 players.

Report: `BALANCE_SIM_REPORT_V4_TEAM.md`

### v5 — latest completed: Tier Pressure Grammar
The co-op pressure philosophy has now been formalized structurally.

Pressure families:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Stages may use 1, 2 or 3 pressure families. All three are **not** forced into every stage.

Five representative 50-stage tier prototypes were generated:
- T1 Foundations: 30 / 17 / 3 single/double/triple stages.
- T2 Breakers: 21 / 23 / 6.
- T3 Rushline: 17 / 25 / 8.
- T4 Crossfire: 11 / 25 / 14.
- T5 Extremes: 23 / 19 / 8.

Across the 250 prototype stages:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

Thus 84.4% of stages use only one or two pressure families.

The prototype also stores:
- S/E/X frequency,
- pair/triple internal pressure ratios,
- line/cluster/scatter/split geometry,
- early/mid/late/final timing bias,
- overlap tendency,
- focused-extreme behavior.

Structural role-coverage across all 250 prototype stages:
- Knight 18.6%
- Rogue 20.1%
- Tank 20.4%
- Archer 22.0%
- Mage 18.9%

Tier-specific peaks still exist, which is intentional:
- Rogue peaks in elite-heavy T2,
- Archer peaks in line-heavy T3,
- Tank peaks in split/special-heavy T4,
- Knight remains comparatively stable.

This supports the pressure-grammar concept but does not freeze the exact final stage data.

See:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`

## Current next boundary
Do not patch live difficulty yet.

Next analysis:
1. convert S/E/X pressure budgets into concrete spawn recipes using GRUNT/RUNNER/BRUTE/SHIELD/FLYER,
2. then run 2/3/4-player headless scaling calibration,
3. measure clear rate, wall pressure, concurrency/readability, target-type contribution and Average→Skilled response,
4. report and discuss before any live difficulty change.

Still not frozen:
- exact player-count scaling multipliers,
- exact S enemy counts,
- exact E HP/armor multipliers,
- exact X compositions,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- sync-bonus implementation.

## Important live-game UX decisions
- No X LOCK explanatory text after first heavy tap.
- Shop does not auto-advance.
- Short shop input protection prevents accidental purchase/advance.
- Timing Square-side EXP is the primary growth HUD.
- Persistent skill-name text beside EXP remains removed.
- Timing Square renders above monsters.
