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

## Class palette
- Knight: gold + bright steel
- Rogue: charcoal / dark gray + silver, tiny red accent
- Tank: strong blue + dark steel
- Archer: green
- Mage: purple

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

### v3 — latest completed
Average→Skilled mastery progression was simulated after the decisions above were frozen.

Confirmed 500-seed/class clear rates:
- at PERFECT 30%: Knight 32.6%, Rogue 0%, Archer 12.4%, Mage 19.4%.
- at PERFECT 35%: Knight 79.8%, Rogue 5.2%, Archer 60.2%, Mage 73.8%.
- at PERFECT 37.5%: Knight 94.8%, Rogue 15.8%, Archer 80.8%, Mage 92.6%.
- at Skilled PERFECT 40%: Knight 98.4%, Rogue 32.8%, Archer 94.6%, Mage 97.0%.

No playable balance values were changed from v3.

Important v3 finding: mastery includes both timing accuracy and faster recognition/commitment. Keeping Skilled accuracy but Average attack cadence reduced clear rates sharply, so timing cadence itself is a meaningful skill dimension.

## Current next boundary
Do not immediately patch live balance.

Next highest-value validation is **2/3/4-player team-composition simulation**, especially Tank team utility and Rogue specialist value. Results must be reported and discussed before changing live gameplay.

## Important live-game UX decisions
- No `X LOCK` explanatory text after first tap of heavy attack.
- Shop never auto-advances; user presses READY / NEXT.
- Shop opens with short input protection to prevent accidental purchase/advance.
- Top duplicate LV/EXP text removed; the Timing Square-side EXP gauge is the primary growth HUD.
- Persistent skill-name text beside EXP gauge removed to prevent overlap.
