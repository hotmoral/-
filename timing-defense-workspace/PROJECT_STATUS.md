# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE / P4-A PASS / P4-B NEXT**

Completed chain:

```text
P0 Foundation / role expression PASS_WITH_WATCHES
 -> SKILLED_V2_CENTRAL all-20 540/540 PASS
 -> P1 Run-State Lifecycle STRUCTURAL COMPLETE
 -> P2 Modifier Pipeline / Power Attribution STRUCTURAL COMPLETE
 -> P3 Ten-Stage Persistent Run Kernel STRUCTURAL PASS
 -> P4 methodology USER APPROVED
 -> P4-A Marker-Only Inverse Design PASS
```

Active dependency plan:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_4.yaml`

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

- provisional non-T1 intended-entry `SKILLED_V2_CENTRAL` full-Tier clear normally remains below 60% as an upper difficulty gate.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application, not tutorial.

---

# Closed lower layers

## P1
Authority: `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`

Persistent Base HP/combo/charge/level/EXP/run state semantics, failure/retry and reconnect identity are structurally closed.

## P2
Authority:
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`

Typed additive scalar progression, effect/stat separation, deterministic attribution, N3 isolation and delayed rounding are structurally closed.

## P3
Authority/evidence:
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`

Result:

```text
30 / 30 primary 10-Stage runs PASS
8 / 8 targeted fixtures PASS
```

P3 does not freeze final EXP, Base HP, shop, exact launch content or production difficulty.

---

# P4 methodology — USER APPROVED

Authority:
- `legacy-game-structure/78_P4_FULL_PLAYER_POWER_SPINE_EXP_MODEL_PROPOSAL_V0_1.md` — historical proposal
- `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`

Approved direction:
1. EXP source = valid completed local timing turn only.
2. Heavy X+Y produces one combined-tier EXP award.
3. calibrate in dimensionless `XP_CREDIT`; obsolete prototype absolute EXP scale is rejected.
4. use six cumulative milestone anchors + monotonic interpolation before any closed-form level formula.
5. calibrate across T1–T4 × LOW/CENTRAL/HIGH synthetic opportunity envelopes.
6. Lv6 current authority and Lv11/16/21 v0.16 parity may feed P4-B; Lv26/Lv31 remain later user gates.
7. initial fit uses P50 while recording P25/P50/P75/P90; tail gates remain open.
8. one universal EXP curve across classes/Tiers; no hidden class/Tier correction unless later evidence justifies a new decision gate.

Additional user-confirmed design consequence:
- EXP must not force every Tier into the same Stage-flow shape.
- if timing opportunities collapse because enemies die too quickly, first inspect gameplay-natural encounter levers such as quantity, durability/armor where role-consistent, cadence, formation and pressure composition rather than silently correcting XP.

---

# P4-A — PASS / COMPLETE

Authority/evidence:
- `legacy-game-structure/80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4a_marker_opportunity_corpus_v0_1.json`
- `legacy-game-structure/data/p4a_marker_inverse_design_summary_v0_1.json`
- `tools/run_p4a_marker_inverse_design_v0_1.py`
- `tools/validate_p4a_marker_inverse_design_v0_1.py`

Executed scope:

```text
4 Tiers × 3 opportunity envelopes = 12 synthetic 50-Stage fixtures
100 deterministic central streams per fixture
= 1,200 marker-only Tier runs
```

Static authoring checks all PASS:
- legal Tier encounter availability;
- teach/earliest-use ordering;
- pressure frequency ranges;
- complexity ranges;
- 10-Stage class-opportunity guardrail;
- formation/cadence vocabulary;
- C4 boundedness;
- exact-signature repetition guard.

Initial CENTRAL diagnostic found universal threshold conflicts at Lv16/Lv21. These were resolved by bounded synthetic **encounter-opportunity redistribution** inside existing Tier identities rather than adding Tier-specific XP multipliers.

Final CENTRAL common feasible XP_CREDIT intervals:

```text
Lv6   (119.7500, 141.4375]
Lv11  (227.5000, 276.1875]
Lv16  (382.0625, 396.7500]
Lv21  (532.8125, 591.5625]
Lv26  (702.6250, 793.1250]
Lv31  (973.0000, 1002.6875]
```

Therefore one universal marker-only EXP curve is structurally feasible across T1–T4 CENTRAL synthetic opportunity shapes.

First-pass midpoint anchors, **candidate only / NOT FROZEN**:

```text
A6    130.59375
A11   251.84375
A16   389.40625
A21   562.18750
A26   747.87500
A31   987.84375
```

CENTRAL P50 unlock Stages at those candidate anchors:

```text
       T1  T2  T3  T4
Lv6     7   6   5   7
Lv11   13  11  12  13
Lv16   19  18  19  21
Lv21   26  27  26  27
Lv26   34  34  34  34
Lv31   43  43  45  41
```

LOW/HIGH envelopes intentionally show large opportunity sensitivity and are not required to hit every milestone window. They remain stress evidence, not separate EXP curves.

Canonical P4-A blobs:

```text
runner    0892f332cd177e78b8fa4e31522563a9809b049e
validator ebd5e932189e70891a8e4d4edf65f997e70f367b
corpus    c3f1dff341e65bf81204ad360bafa3cdce7c4c7d
summary   3f21f1a3ee46b8bc0b297e035ffca5b8a97d0652
```

---

# Exact current boundary — P4-B

## P4-B LV6_TO_LV21_COMBAT_FEEDBACK_INTEGRATION

Next task:
- turn on actual/current Lv6 mechanics;
- turn on exact v0.16 Lv11/Lv16/Lv21 mechanics only as simulation-parity candidates;
- use P4-A candidate anchors as starting values, not authority;
- measure class-specific kill-speed and timing-turn-opportunity feedback;
- recompute Lv6/11/16/21/26/31 reach by class/Tier;
- test whether one universal curve remains feasible after real early/mid skill power;
- attribute whether deviations come from encounter opportunity or skill power.

P4-B may refit candidate anchors but cannot numerically freeze them.

Still prohibited:
- inventing Lv26 or Lv31 power proxies;
- hidden class-specific XP multipliers;
- hidden Tier XP multipliers;
- exact launch Stage authoring;
- production gameplay deployment.

P4-C remains the separate Lv26 user-decision gate after P4-B.

---

# Still not frozen

- exact XP_CREDIT vector
- exact A6/A11/A16/A21/A26/A31
- exact intermediate-level formula
- player-visible EXP scale
- percentile tail acceptance gates
- production monster coefficients / exact 200 Stages
- shop/economy
- Base HP
- star/achievement numerical power
- Lv26/Lv31 mechanics
- boss values
- multiplayer progression/scaling
- production numerical implementation

No production gameplay source was changed by the P4 approval or P4-A execution.
