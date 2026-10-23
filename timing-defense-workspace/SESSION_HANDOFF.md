# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory, or this file alone.
Always fetch live remote first.

Read/check in this order:
1. branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_6.yaml`
6. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
7. `legacy-game-structure/84_P4B_EXP_DECISION_REASSESSMENT_PROPOSAL_V0_1.md`
8. `legacy-game-structure/83_P4B_MULTIPLAYER_TIMEBASE_PRECHECK_V0_1.md`
9. `legacy-game-structure/81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
10. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
11. production and calibration-harness branch heads

Then follow the protocol's structural-spine and active-phase read packs before substantive work.

Important:
- `legacy-game-structure/README.md` is a valuable corpus/history map, but it contains older execution-order / `NEXT` references. Do not treat those older references as current authority when they conflict with live status, latest approved routing, or `system_dependency_calibration_order_v0_6.yaml`.
- Do not re-run already-closed P1/P2/P3 or other PASS/APPROVED checks merely because a new session started. Revalidate only under the explicit triggers in document 86.

Live remote always wins.

---

# Branch checkpoints at handoff creation

Planning branch:
- `timing-defense-workspace`
- exact final handoff HEAD must be re-fetched after all handoff-sync commits; do not trust a copied SHA without live verification.

Production branch:
- `timing-defense-cloudflare-do-poc`
- verified before handoff sync: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes remain unauthorized.

Calibration harness branch:
- `timing-defense-skilled-v2-harness-v01`
- verified before handoff sync: `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE**

R2 routing is USER APPROVED.

Completed chain:

```text
P0 Foundation / role expression PASS_WITH_WATCHES
 -> SKILLED_V2_CENTRAL all-20 closure
 -> P1 Run-State Lifecycle COMPLETE
 -> P2 Modifier Pipeline / Power Attribution COMPLETE
 -> P3 Ten-Stage Persistent Run Kernel PASS
 -> P4 methodology USER APPROVED
 -> P4-A Marker-Only Inverse Design PASS
 -> P4-B Solo Lv6→Lv21 feedback diagnostic COMPLETE
 -> P4-B Multiplayer / Timebase bounded precheck COMPLETE
 -> R2 routing USER APPROVED
```

Exact next package:

```text
P4-C1 — LV26 STRUCTURAL SKILL-CONTRACT DECISION
```

Do not start P4-C2 before P4-C1 user approval.

---

# R2 meaning

Current pure per-valid-turn EXP remains a **provisional diagnostic baseline only**.

Still provisionally true for measurement:
- valid completed local timing turn gives EXP;
- Heavy X+Y gives one combined-tier award;
- timing quality matters;
- `XP_CREDIT` is dimensionless calibration space;
- one universal EXP curve remains preferred;
- no hidden class/Tier XP multipliers.

Not approved/frozen:
- pure per-turn as final launch EXP semantics;
- Stage Quality Budget / prior Option D;
- exact XP values or milestone thresholds;
- player-visible EXP scale;
- player-count EXP correction.

Mandatory active watches:

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
```

Future progression analysis must consider multiple views rather than one metric:
- Stage reach;
- wall-clock reach;
- clear/fail probability;
- retry cost;
- wall attrition;
- homogeneous vs mixed teams;
- same-class teammate sensitivity;
- player-count scaling sensitivity.

---

# Required future reconvergence

Active dependency plan:
`legacy-game-structure/data/system_dependency_calibration_order_v0_6.yaml`

Approved route:

```text
P4-C1 Lv26 structural decision
 -> P4-C2 Lv26 provisional feedback
 -> P4-D1 Lv31 structural decision
 -> P4-D2 Lv31 provisional mastery feedback
 -> P4-E provisional power-spine closure WITH EXP WATCHES
 -> P5/P6/P7/P8
 -> P10 current-roster multiplayer scaling baseline
 -> P10R mandatory EXP / multiplayer-timebase reconvergence
 -> only then may permanent progression rely on converged EXP behavior
```

No final EXP convergence claim before P10R.

---

# P4-C1 instructions

Goal: resolve exact structural contracts for all five Lv26 skills.

First recover live evidence. Known historical retrieval leads only:
- Knight: penetration-decay removal candidate;
- Rogue: secondary tracking dagger candidate;
- Tank: temporary slow-zone candidate;
- Archer: PERFECT penetration extension/full rear damage candidate;
- Mage: conditional chain candidate.

Do not assume those descriptions are canonical until revalidated.

For each class:
1. recover exact documented behavior;
2. classify mechanic/value authority;
3. audit interaction with Lv6/11/16/21;
4. audit P2 modifier/effect-pipeline compatibility;
5. audit monster-role interaction / novelty collision;
6. isolate unresolved targeting/proc/duration/geometry/crit/penetration/knockback/ownership semantics;
7. compare bounded alternatives where needed;
8. give recommendation + risks + reversibility;
9. STOP for USER APPROVAL before structural freeze or P4-C2.

In addition, apply the mandatory cross-stage review lenses from document 86 before closing P4-C1 or any later package.

Never invent a generic Lv26 power proxy just to keep simulation moving.

---

# Stable game truths

- 5 classes: Knight/Rogue/Tank/Archer/Mage.
- independent class Tier progression.
- same Tier/Stage combat content across classes.
- 1 Tier = 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad permanent account growth.
- achievements = targeted/cross-class permanent progression.
- recoverable soft walls intended; hard class lockout forbidden.
- Model A roster ladder: T1 G/R/B; T2 +SH/F; T3 +C/SP; T4 +SUP/SI; T5+ future.
- current 9 monsters are foundation, not lifetime roster.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45 direction.
- Stage46–49 post-Lv31 mastery; Stage50 final application.
- actual timing input is constant-speed line sweep across Timing Square; player taps to register coordinate. Do not describe it as cursor/finger movement.
- ordinary difficulty should come mainly from encounter complexity, not simply shrinking PERFECT zone or increasing sweep speed.

---

# Do not yet

- change/deploy production v0.45 gameplay;
- activate Stage Quality Budget;
- freeze pure per-turn EXP as final;
- add hidden class/Tier EXP multipliers;
- freeze exact EXP anchors;
- invent Lv26/Lv31 proxies;
- freeze exact shop/BaseHP/permanent-progression/boss/multiplayer numbers;
- author exact 200 launch Stages;
- begin P4-C2 before P4-C1 approval.

This handoff boundary intentionally stops **before starting P4-C1 substantive design work**.