# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE / P4-B DIVERGENCE FOUND / USER DECISION GATE**

Completed chain:

```text
P0 Foundation / role expression PASS_WITH_WATCHES
 -> SKILLED_V2_CENTRAL all-20 540/540 PASS
 -> P1 Run-State Lifecycle STRUCTURAL COMPLETE
 -> P2 Modifier Pipeline / Power Attribution STRUCTURAL COMPLETE
 -> P3 Ten-Stage Persistent Run Kernel STRUCTURAL PASS
 -> P4 methodology USER APPROVED
 -> P4-A Marker-Only Inverse Design PASS
 -> P4-B Lv6→Lv21 Combat Feedback diagnostic COMPLETE
 -> EXP stabilization direction USER DECISION REQUIRED
```

Active dependency plan:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_5.yaml`

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
- EXP must not force every Tier into the same encounter-flow shape.

---

# Closed lower layers

## P1
Authority: `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`

Persistent Base HP/combo/charge/level/EXP/run-state semantics, failure/retry and reconnect identity are structurally closed.

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

---

# P4 methodology — USER APPROVED

Authority:
- `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`

Approved baseline before P4-B evidence:
1. valid completed local timing turn is the baseline EXP source;
2. Heavy X+Y creates one combined-tier award;
3. calibrate in `XP_CREDIT`;
4. six cumulative milestone anchors + monotonic interpolation;
5. T1–T4 × LOW/CENTRAL/HIGH synthetic calibration;
6. Lv6 current authority + Lv11/16/21 v0.16 parity may feed P4-B; Lv26/Lv31 remain separate gates;
7. first fit P50 while recording P25/P50/P75/P90;
8. one universal EXP curve, no hidden class/Tier correction.

User-confirmed additional principle:
- gameplay-natural encounter levers should address bad Stage pacing where appropriate;
- progression calibration must not homogenize Tier identity.

---

# P4-A — PASS / COMPLETE

Authority/evidence:
- `legacy-game-structure/80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4a_marker_opportunity_corpus_v0_1.json`
- `legacy-game-structure/data/p4a_marker_inverse_design_summary_v0_1.json`

Executed:

```text
12 synthetic 50-Stage fixtures
× 100 deterministic central streams
= 1,200 marker-only Tier runs
```

Marker-only CENTRAL supported common universal threshold intervals for all six milestones.
First midpoint anchors remain **candidate only / NOT FROZEN**:

```text
A6    130.59375
A11   251.84375
A16   389.40625
A21   562.18750
A26   747.87500
A31   987.84375
```

P4-A therefore proved universal progression is feasible only before real skill-power feedback is coupled in.

---

# P4-B — DIVERGENCE FOUND

Authority/evidence:
- `legacy-game-structure/81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4b_combat_feedback_divergence_v0_1.json`

Permitted power used:
- Lv6 current authoritative mechanics;
- Lv11/Lv16/Lv21 exact v0.16 mechanics as simulation-only parity candidates;
- Lv26/Lv31 power OFF.

Independent P3 Lv6 cross-check was reproduced closely for Knight/Rogue/Tank/Archer; Mage is retained as a conservative WATCH.

Main finding:

```text
P4B_UNIVERSAL_PURE_PER_TURN_WINDOW_CONFLICT
```

Cause:

```text
offensive class skill
 -> faster removal
 -> fewer valid timing turns
 -> less later XP
 -> later subsequent skills

control/defensive early skill
 -> more timing turns remain
 -> more later XP
 -> earlier subsequent skills
```

Refitting the six universal thresholds alone did not solve the current milestone windows.
Best bounded pure-per-turn search still produced approximately:

```text
Lv11 worst miss 1 Stage
Lv16 worst miss 3
Lv21 worst miss 4
Lv26 worst miss 5
Lv31 worst miss 5
```

Representative Lv31 conflict against the confirmed Stage41–45 target:
- Tank: around Stage36–37 in several Tiers;
- Mage: around Stage49–50 in some Tiers;
- Knight T3: around Stage46.

Therefore P4-B cannot proceed directly to Lv26 calibration while pretending the original pure-per-turn baseline remains structurally adequate.

No class balance nerf, class/Tier XP multiplier, Stage-clear XP, encounter rewrite or new stabilization rule is authorized by this finding.

---

# Current decision gate

Proposal:
`legacy-game-structure/82_P4B_EXP_STABILIZATION_DECISION_PROPOSAL_V0_1.md`

Options:
- A — keep pure per-turn EXP and reopen common skill-reach expectations;
- B — class-specific XP/threshold correction;
- C — encounter-authoring-only correction;
- D — **class-neutral Stage Quality Budget + raw-turn hybrid**.

Current recommendation: **D**, with C retained as the normal tool for local gameplay-shape defects.

Option D is not approved yet.
Exact blend, Stage budget, quality vector, visible EXP scale and thresholds remain OPEN.

Exploratory reduced-order sensitivity only:

```text
100% raw turn -> worst common-window miss ~5 Stages
75% raw       -> ~3
50% raw       -> ~2
25% raw       -> a few ~1-Stage misses
10% raw       -> all tested current windows feasible
0% raw        -> all tested current windows feasible
```

These percentages are not candidate final values; they only show that a tiny generic bonus is unlikely to solve the structural bias.

---

# Exact current boundary

```text
P4B_DECISION — EXP_OPPORTUNITY_STABILIZATION_DIRECTION
= AWAITING USER DECISION
```

Do not start P4-C Lv26 yet.
Do not implement P4-B2 normalization methodology until the user chooses a direction.

If Option D is approved, next bounded test is proposed as:

```text
raw-turn weight λ = 0.00 / 0.10 / 0.25 / 0.50
```

with full reach/class-spread/quality-sensitivity comparison before any exact value is selected.

---

# Still not frozen

- new EXP stabilization semantics
- exact XP_CREDIT vector
- exact Stage progression budget
- exact raw-turn blend
- exact A6/A11/A16/A21/A26/A31
- intermediate-level formula
- player-visible EXP scale
- percentile tail acceptance gates
- production monster coefficients / exact 200 Stages
- shop/economy / Base HP
- star/achievement numerical power
- Lv26/Lv31 mechanics
- boss values
- multiplayer progression/scaling
- production numerical implementation

No production gameplay source was changed by P4-A/P4-B planning and diagnostics.
