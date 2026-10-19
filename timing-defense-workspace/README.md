# Timing Defense — Public Workspace

This directory is the persistent planning / balance / handoff workspace for the Timing Defense prototype.

## Repository layout
- Live playable code branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: https://timing-defense-v011.onrender.com
- Latest playable prototype at workspace creation: `v0.15`

The workspace branch is intentionally separated from the Render deployment branch so documentation and balance work do not trigger a live deploy.

## Read order for a new session
1. `PROJECT_STATUS.md`
2. `DESIGN_DECISIONS.md`
3. `SKILL_PLAN_LV6_31.md`
4. `BALANCE_SIM_REPORT_V1.md`
5. `NEXT_WORK.md`

## Current project boundary
Timing-action side defense prototype with five classes:
- Knight
- Rogue
- Tank
- Archer
- Mage

Core timing rhythm is `X → X → X → X+Y`; the 4th attack is the charged/heavy attack. Timing judgment directly drives projectile outcome, EXP and class growth.

## Working principle
Automated simulation is used for numerical balance, growth speed, encounter difficulty and class-role validation. Human playtesting is reserved for timing feel, readability, hit impact, VFX density and subjective fun.
