# Timing Defense — New GPT Handoff — 2026-10-23 P4-B R2 Boundary

Repository: `hotmoral/-`

Planning / canonical workspace branch: `timing-defense-workspace`

Important:
- Do not reconstruct state from this handoff, chat history, or memory.
- Always fetch live GitHub remote first.
- Any SHA copied here is a handoff checkpoint only; live remote wins.
- Do not modify or deploy production during initial recovery.

## Recovery order

1. fetch live `timing-defense-workspace` HEAD;
2. read `timing-defense-workspace/PROJECT_STATUS.md`;
3. read `timing-defense-workspace/NEXT_WORK.md`;
4. read `timing-defense-workspace/SESSION_HANDOFF.md`;
5. read `timing-defense-workspace/legacy-game-structure/data/system_dependency_calibration_order_v0_6.yaml`;
6. read `timing-defense-workspace/legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`;
7. read `timing-defense-workspace/legacy-game-structure/84_P4B_EXP_DECISION_REASSESSMENT_PROPOSAL_V0_1.md`;
8. read `timing-defense-workspace/legacy-game-structure/83_P4B_MULTIPLAYER_TIMEBASE_PRECHECK_V0_1.md`;
9. read `timing-defense-workspace/legacy-game-structure/81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`;
10. read `timing-defense-workspace/PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`;
11. verify live production branch `timing-defense-cloudflare-do-poc`;
12. verify live calibration branch `timing-defense-skilled-v2-harness-v01`.

## Handoff checkpoint facts

Production was verified unchanged at:
`ea22cc279603394dc4b439b6fdbb0c83aff4299a`

Calibration harness was verified at:
`063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

Re-fetch both before relying on them.

## Current decision state

R2 was explicitly USER APPROVED.

R2 means:
- pure per-valid-turn EXP remains the provisional diagnostic baseline;
- it is not frozen as final;
- prior Stage Quality Budget Option D is not approved;
- final EXP convergence is intentionally deferred until authoritative multiplayer combat scaling exists;
- a mandatory P10R reconvergence is now part of the dependency route;
- hidden class/Tier EXP multipliers remain disallowed without a new explicit user decision.

Active watches:
- `SOLO_PROGRESSION_DIVERGENCE_WATCH`
- `TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH`
- `PLAYER_COUNT_SCALING_XP_DEPENDENCY`
- `MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE`

Future progression analysis must compare multiple views, including Stage reach, wall-clock reach, clear/fail, retry cost, wall attrition, team composition, same-class teammate dependence and player-count scaling.

## Exact next boundary

Do not begin P4-C2 or any numerical Lv26 power simulation immediately.

First package:

`P4-C1 — LV26 STRUCTURAL SKILL-CONTRACT DECISION`

Goal:
- recover exact live evidence for all five Lv26 skills;
- classify every mechanic/value as authoritative / parity-candidate / candidate-only / unresolved;
- audit interaction with Lv6/Lv11/Lv16/Lv21, P2 modifier/effect pipeline and monster roles;
- identify unresolved targeting/proc/duration/geometry/crit/penetration/knockback/ownership details;
- compare bounded alternatives only where materially needed;
- make a recommendation with risks/reversibility;
- stop for user approval before structural freeze or P4-C2 execution.

Historical retrieval leads only; do not assume canonical until live verification:
- Knight: penetration-decay removal candidate;
- Rogue: secondary tracking dagger candidate;
- Tank: temporary slow-zone candidate;
- Archer: PERFECT penetration extension/full rear damage candidate;
- Mage: conditional chain candidate.

## Stable design rules that matter for P4-C1

- 5 classes; independent class Tier progression.
- same Tier/Stage combat content across classes.
- 1 Tier = 50 Stages.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window direction = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- actual timing input is constant-speed line sweep across the Timing Square; player taps to register coordinate.
- ordinary difficulty should primarily come from encounter/combat complexity rather than simply shrinking PERFECT zone or increasing sweep speed.
- EXP must not homogenize Tier encounter identity.
- do not invent generic Lv26/Lv31 power proxies.

## Initial-session instruction

On entering the new session:
1. recover and cross-check live canonical state;
2. confirm R2 authority and v0.6 dependency plan are internally consistent;
3. verify production remains untouched;
4. report the exact recovered boundary briefly;
5. only then begin P4-C1 evidence recovery/review when the user tells you to proceed.
