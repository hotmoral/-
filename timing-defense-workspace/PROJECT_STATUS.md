# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Current playable version
- Prototype: `v0.15`
- URL: https://timing-defense-v011.onrender.com/v015.html
- Render service: `timing-defense-v011`
- Live deployment branch: `timing-defense-live-v011`

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

## Current balance workflow
A headless Monte Carlo simulator was introduced before implementing Lv11+ skills. Numerical role validation is performed automatically first; human playtesting then checks feel and readability.

## Important live-game UX decisions
- No `X LOCK` explanatory text after first tap of heavy attack.
- Shop never auto-advances; user presses READY / NEXT.
- Shop opens with short input protection to prevent accidental purchase/advance.
- Top duplicate LV/EXP text removed; the Timing Square-side EXP gauge is the primary growth HUD.
- Persistent skill-name text beside EXP gauge removed to prevent overlap.
