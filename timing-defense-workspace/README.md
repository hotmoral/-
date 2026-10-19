# Timing Defense — Public Workspace

This directory is the persistent planning / balance / simulation / handoff workspace for the Timing Defense prototype.

## Repository layout
- Live playable code branch: `timing-defense-live-v011`
- Workspace branch: `timing-defense-workspace`
- Public service: https://timing-defense-v011.onrender.com
- Current playable prototype: `v0.15`

The workspace branch is intentionally separated from the Render deployment branch so documentation and balance work do not trigger a live deploy.

## Read order for a new session
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `DESIGN_DECISIONS.md`
4. `SKILL_PLAN_LV6_31.md`
5. `BALANCE_SIM_REPORT_V2.md`
6. `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`
7. `BALANCE_SIM_REPORT_V4_TEAM.md`
8. `SIMULATION_METHOD.md`
9. `NEXT_WORK.md`

`BALANCE_SIM_REPORT_V1.md` remains useful as the original role-separation baseline, but v2/v3/v4 supersede it for current interpretation.

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

Simulation is diagnostic, not self-authorizing. A large measured class gap must be explained and discussed before any live balance patch is made.

## Current simulation boundary
The latest completed analysis is **v4 team-composition / co-op role validation**.

Current accepted interpretation:
- Tank has real team defensive utility under meaningful pressure.
- Rogue has real durable-normal execution value in teams.
- Archer and Mage remain geometrically distinct.
- Knight remains a useful generalist.
- the current Stage 1–10 wave saturates with 3–4 players, so co-op pressure scaling must be designed before final multiplayer balance can be judged.
- double-Knight stacking is flagged for exact-implementation re-test, not for an immediate nerf.

No live balance change was made from v4.

The next design discussion is the philosophy for team-size enemy-pressure scaling before building v5.
