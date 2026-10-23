# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE / R2 ROUTING USER APPROVED / NEXT = P4-C1 LV26 STRUCTURAL SKILL CONTRACT**

Completed evidence/decision chain:

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
 -> R2 revised routing USER APPROVED
 -> P4-C1 Lv26 structural review is next
```

Active dependency plan:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_6.yaml`

R2 authority:
- `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`

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
- Lv31 target unlock window = Stage41–45; this remains a target direction to re-test, not a final numerical guarantee.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- EXP must not force every Tier into the same encounter-flow shape.
- final progression decisions must consider Stage reach, wall-clock reach, fail/retry behavior and multiplayer context together where relevant.

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

# P4 approved methodology baseline

Authority:
- `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`

Provisional diagnostic EXP baseline:
- valid completed local timing turn is the EXP source;
- Heavy X+Y gives one combined-tier award;
- quality tiers matter;
- use dimensionless `XP_CREDIT` for calibration;
- one universal EXP curve remains the preferred target;
- no hidden class/Tier multiplier;
- encounter identity must not be homogenized to fit EXP.

R2 explicitly means this EXP baseline is **not final semantic/numerical freeze**.

---

# P4-A — marker-only PASS

Authority/evidence:
- `legacy-game-structure/80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4a_marker_inverse_design_summary_v0_1.json`

12 synthetic 50-Stage fixtures × 100 deterministic streams = 1,200 marker-only runs.

Candidate-only midpoint anchors:

```text
A6    130.59375
A11   251.84375
A16   389.40625
A21   562.18750
A26   747.87500
A31   987.84375
```

None are frozen.

---

# P4-B — solo + multiplayer/timebase diagnostics complete

Solo authority:
- `legacy-game-structure/81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4b_combat_feedback_divergence_v0_1.json`

Multiplayer/timebase authority:
- `legacy-game-structure/83_P4B_MULTIPLAYER_TIMEBASE_PRECHECK_V0_1.md`
- `legacy-game-structure/data/p4b_multiplayer_timebase_precheck_v0_1.json`

Keep all watches active:

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
```

Interpretation:
- solo offensive efficiency can reduce later EXP opportunities;
- multiplayer shares part of that effect across the team and therefore compresses solo divergence;
- multiplayer does not eliminate individual class/action-cadence differences;
- teammate composition and player-count scaling can also change XP opportunity;
- real-time normalization alone does not guarantee equal progression because spawn/cadence may floor Stage duration;
- high EXP opportunity can coexist with worse clear/fail outcomes.

Therefore neither pure per-turn final freeze nor Stage Quality Budget activation is justified yet.

---

# R2 — USER APPROVED

Authority:
- proposal: `legacy-game-structure/84_P4B_EXP_DECISION_REASSESSMENT_PROPOSAL_V0_1.md`
- approved contract: `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`

Approved route:

```text
P4-C1  Lv26 structural decision
 -> P4-C2 Lv26 provisional feedback
 -> P4-D1 Lv31 structural decision
 -> P4-D2 Lv31 provisional mastery feedback
 -> P4-E provisional player-power-spine closure WITH EXP WATCHES
 -> P5/P6/P7/P8
 -> P10 current-roster multiplayer scaling baseline
 -> P10R mandatory EXP / multiplayer-timebase reconvergence
 -> only after P10R may permanent-progression layers rely on converged EXP behavior
```

R2 does NOT approve:
- Option D / Stage Quality Budget;
- pure per-turn EXP as final;
- class/Tier EXP multipliers;
- exact EXP thresholds or visible values.

---

# Exact current boundary

```text
P4-C1 — LV26 STRUCTURAL SKILL-CONTRACT DECISION
```

Before any P4-C2 power simulation:
1. recover exact evidence for all five Lv26 skills;
2. classify each element as authoritative / parity-candidate / unresolved;
3. audit interactions with Lv6/11/16/21 and monster roles;
4. compare meaningful alternatives only where unresolved;
5. present recommendation, risks and reversibility;
6. require user approval before structural freeze.

Do not invent generic Lv26 power proxies.

---

# Still not frozen

- Lv26 exact mechanics/numbers
- Lv31 exact mechanics/numbers
- final EXP acquisition semantics
- exact XP_CREDIT vector
- exact A6/A11/A16/A21/A26/A31
- intermediate-level formula
- player-visible EXP scale
- player-count progression treatment
- percentile tail acceptance gates
- production monster coefficients / exact 200 Stages
- shop/economy / Base HP
- star/achievement numerical power
- boss values
- multiplayer combat/progression scaling
- production numerical implementation

No production gameplay source was changed by P4-A/P4-B/R2 planning.