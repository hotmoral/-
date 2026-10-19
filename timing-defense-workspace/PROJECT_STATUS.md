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
- Attack rhythm: first three attacks use X timing, fourth/heavy uses X then Y.
- Judgments: NORMAL / GOOD / PERFECT and heavy outcomes HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL.
- Five playable classes: Knight / Rogue / Tank / Archer / Mage.
- Team controls: solo through +3 AI.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Stage prototype: 1–10, with boss-like BRUTE at stages 5 and 10.
- Run-only EXP / levels / coins / shop upgrades.
- Current implemented skill layer: Lv6 class skill only.
- Skill icon is displayed below Timing Square; charge stack UI stays above it.
- Timing Square is rendered above monsters so approaching enemies cannot obscure it.
- Class palettes are visually separated in character clothing, weapons, Timing Square and VFX.

## Growth structure
Planned automatic skill unlocks:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Lv21 is the first major transformation point for the 4th/heavy attack. Lv31 P×P CRITICAL is intended to become the class-signature finisher.

## Frozen role/balance decisions
- Archer penetration is true straight-line geometry only; no homing/retarget/next-enemy auto-chain.
- Tank is intentionally team-specialized and does not need fresh-run solo Stage-10 parity.
- Rogue has no same-target dagger hit cap.
- Boss dagger damage scalar starting value: `0.70`.
- Boss knockback scalar starting value: `0.40`.
- EXP remains tied to timing attack results/events. Faster-clearing classes are not automatically compensated for fewer attack events.
- Simulation results are diagnostic. Large performance gaps must be reported and discussed before any live numerical patch.

## Player-skill interpretation
Current simulation endpoints:
- Average: NORMAL 25% / GOOD 55% / PERFECT 20%.
- Skilled: NORMAL 10% / GOOD 50% / PERFECT 40%, with modestly faster attack commitment.

The Skilled state is treated as an attainable learned-player level, not an extreme expert-only state. A strong improvement from Average → Skilled is desirable because player mastery should materially reduce difficulty.

## Balance-simulation status

### v1
Role benchmarks validated the intended specialization split.

### v2
Added Stage 1–10 + run-shop campaign simulation. It exposed the Archer penetration-model artifact, Tank solo/team-role question and EXP/attack-count coupling. Those items were discussed and explicit design decisions were made before any patch.

### v3
Average→Skilled mastery progression was simulated after the above decisions were frozen. Knight / Archer / Mage showed a strong but plausible mastery response; Rogue remained a specialist; Tank solo remained non-normative. No live value changed.

### v4 — latest completed
Team-composition / co-op role validation, 13,780 deliberate runs.

Main findings:
- Tank has measurable team defensive value under meaningful pressure.
- Rogue takes a disproportionate share of durable-normal kills in 3-player teams (~39–42% in several tested mixes).
- Archer and Mage remain geometrically distinct: long-line pack favored Archer (~66.8% pair damage), dense cluster favored Mage (~58.4%).
- Knight remains a useful generalist/stabilizer.
- Current Stage 1–10 waves saturate at 3–4 players: most/all 3-player teams and all 4-player teams clear at very high rates even at Average.
- Double-Knight looked unusually strong in the current headless Lv11 penetration approximation; this is flagged for re-test after exact playable collision implementation, not for an immediate nerf.

No playable balance values were changed from v4.

Report: `BALANCE_SIM_REPORT_V4_TEAM.md`

## Current next boundary
Do not immediately patch live balance.

The next major design question is **co-op pressure scaling by team size**. Before a v5 simulation, decide whether extra players should primarily increase enemy count, enemy durability, a mix of both, or elite/special-threat density.

Multiplayer shop/economy ownership, duplicate-class policy and sync-bonus rules are also not frozen yet.

## Important live-game UX decisions
- No `X LOCK` explanatory text after first tap of heavy attack.
- Shop never auto-advances; user presses READY / NEXT.
- Shop opens with short input protection to prevent accidental purchase/advance.
- Top duplicate LV/EXP text removed; the Timing Square-side EXP gauge is the primary growth HUD.
- Persistent skill-name text beside EXP gauge removed to prevent overlap.
