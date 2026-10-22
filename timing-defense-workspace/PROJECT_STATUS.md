# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE / P4-B MULTIPLAYER-TIMEBASE REASSESSMENT COMPLETE / REVISED USER DECISION GATE**

Completed evidence chain:

```text
P0 Foundation / role expression PASS_WITH_WATCHES
 -> SKILLED_V2_CENTRAL all-20 540/540 PASS
 -> P1 Run-State Lifecycle STRUCTURAL COMPLETE
 -> P2 Modifier Pipeline / Power Attribution STRUCTURAL COMPLETE
 -> P3 Ten-Stage Persistent Run Kernel STRUCTURAL PASS
 -> P4 methodology USER APPROVED
 -> P4-A Marker-Only Inverse Design PASS
 -> P4-B Solo Lv6→Lv21 Combat Feedback diagnostic COMPLETE
 -> P4-B Multiplayer / Timebase bounded precheck COMPLETE
 -> revised EXP-routing decision REQUIRED
```

Current active dependency-plan file remains:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_5.yaml`

Important:
- v0.5 was written before the multiplayer/timebase precheck and still contains the older immediate Option-D recommendation.
- that recommendation is now **superseded for decision purposes** by documents 83/84;
- no new routing or EXP semantic is active until the revised user decision closes.

---

# Stable structural truth

- 5 classes progress independently through Tiers.
- same Tier/Stage combat content across classes.
- Tier = 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intended; hard class lockout forbidden.
- Model A roster ladder:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future
```

- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- EXP must not force every Tier into the same encounter-flow shape.

---

# Closed lower layers

## P1
Authority: `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`

## P2
Authority:
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`

## P3
Authority/evidence:
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`

P3 result:

```text
30 / 30 primary 10-Stage runs PASS
8 / 8 targeted fixtures PASS
```

---

# P4 methodology — USER APPROVED baseline

Authority:
- `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`

Last approved EXP semantic baseline:
- valid completed local timing turn is the EXP source;
- Heavy X+Y gives one combined-tier award;
- use dimensionless `XP_CREDIT` for calibration;
- six cumulative milestone anchors + monotonic interpolation;
- one universal EXP curve is the target;
- no hidden class/Tier multiplier;
- encounter identity must not be homogenized to fit EXP.

This baseline is now treated as **provisional for diagnostics, not numerically/finally frozen** while the multiplayer dependency is unresolved.

---

# P4-A — marker-only PASS

Authority/evidence:
- `legacy-game-structure/80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4a_marker_inverse_design_summary_v0_1.json`

12 synthetic 50-Stage fixtures × 100 deterministic streams = 1,200 marker-only runs.

First midpoint anchors remain candidate only:

```text
A6    130.59375
A11   251.84375
A16   389.40625
A21   562.18750
A26   747.87500
A31   987.84375
```

---

# P4-B solo feedback — divergence remains real

Authority:
- `legacy-game-structure/81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4b_combat_feedback_divergence_v0_1.json`

Finding:

```text
P4B_UNIVERSAL_PURE_PER_TURN_WINDOW_CONFLICT
```

Under solo-oriented combat feedback, offensive skills reduce later timing-turn opportunities while Tank's early defensive/control skills retain more.
A universal threshold refit alone did not keep all current milestone windows, including confirmed Lv31 Stage41–45, jointly feasible.

This remains:

`SOLO_PROGRESSION_DIVERGENCE_WATCH`

It is not discarded.

---

# P4-B multiplayer / timebase precheck — new evidence

Authority/evidence:
- `legacy-game-structure/83_P4B_MULTIPLAYER_TIMEBASE_PRECHECK_V0_1.md`
- `legacy-game-structure/data/p4b_multiplayer_timebase_precheck_v0_1.json`

Boundary:
- bounded historical 5-monster player-count-scaled pressure lane;
- current SKILLED_V2_CENTRAL judgment model;
- exact v0.16 Lv6–21 parity formulas;
- all-human modeled teams;
- not current 9-monster production multiplayer balance.

New findings:
1. shared team combat **does compress** the solo class divergence;
2. mixed-team members still do not gain EXP at identical rates;
3. the same class's XP/min changes with teammates;
4. player-count encounter scaling materially changes per-player XP opportunity;
5. wall-clock normalization does not automatically eliminate the difference because spawn/cadence can floor Stage duration;
6. high EXP opportunity can coincide with worse clear/failure performance.

4P TRAM Lv21 example, credit/min:

```text
Tank    91.83
Rogue   93.53
Archer  79.32
Mage    75.06
```

max/min spread ≈ 24.6% in this bounded lane.

Same-class teammate sensitivity at Lv21 ranged approximately:
- Knight 14.25%
- Rogue 6.96%
- Tank 7.19%
- Archer 6.86%
- Mage 19.45%

New classifications:

```text
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
```

---

# Previous Option-D recommendation — REASSESSED

Historical proposal:
- `legacy-game-structure/82_P4B_EXP_STABILIZATION_DECISION_PROPOSAL_V0_1.md`

Document 82's immediate recommendation of a `Stage Quality Budget + raw-turn hybrid` was made before the multiplayer/timebase evidence existed.

Current status:

**DO NOT APPROVE D AUTOMATICALLY FROM THE SOLO RESULT.**

D remains a possible later stabilizer, but the evidence does not yet justify changing EXP semantics before current-roster multiplayer scaling is known.

---

# Revised decision gate

Proposal:
- `legacy-game-structure/84_P4B_EXP_DECISION_REASSESSMENT_PROPOSAL_V0_1.md`

Options:
- **R1** — adopt Stage Quality Budget direction now;
- **R2 (recommended)** — keep pure per-turn EXP as provisional diagnostic baseline, continue Lv26/Lv31 structural skill work, and require later multiplayer/timebase EXP reconvergence before permanent progression relies on the spine;
- **R3** — freeze pure per-turn EXP as final now.

No route is active until user approval.

R2 is recommended because it distinguishes:

```text
skill identity / player-power definition
from
final progression convergence under multiplayer scaling
```

and avoids both premature normalization and premature pure-per-turn freeze.

---

# Still not frozen

- final EXP acquisition semantics after multiplayer reconvergence
- exact XP_CREDIT vector
- exact A6/A11/A16/A21/A26/A31
- intermediate-level formula
- player-visible EXP scale
- player-count progression treatment
- percentile tail acceptance gates
- production monster coefficients / exact 200 Stages
- shop/economy / Base HP
- star/achievement numerical power
- Lv26/Lv31 mechanics
- boss values
- multiplayer progression/scaling
- production numerical implementation

No production gameplay source was changed by these diagnostics.
