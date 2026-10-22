# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE / PROPOSAL COMPLETE / AWAITING USER DECISION**

Completed through:

```text
P0 Foundation / role expression
 -> historical all-20 540/540
 -> provisional SKILLED_V2_CENTRAL
 -> corrected central all-20 540/540
 -> P1 Run-State Lifecycle structural closure
 -> P2 Modifier Pipeline / Power Attribution structural closure
 -> P3 Ten-Stage Persistent Run Kernel STRUCTURAL PASS
 -> P4 EXP/player-power dependency analysis + reproducible preproposal diagnostic
 -> P4 methodology proposal authored
```

Active dependency plan:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_3.yaml`

P4 proposal / evidence:
- `legacy-game-structure/78_P4_FULL_PLAYER_POWER_SPINE_EXP_MODEL_PROPOSAL_V0_1.md` — **PROPOSED / NOT YET APPROVED**
- `legacy-game-structure/data/p4_exp_preproposal_diagnostics_v0_1.json`
- `tools/analyze_p4_exp_baseline_from_p3.py`

P4-A/B simulator implementation is not yet authorized.

---

# Core structural truth

- 5 classes progress independently through Tiers.
- same Tier/Stage combat content across classes.
- Tier = 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intended; hard class lockout forbidden.
- active bounded Model A roster ladder:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future
```

- provisional non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60% as an upper difficulty gate, not a midpoint.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application, not tutorial.
- intended monster roles must become perceivable before deletion.

Model A remains bounded simulation authority, not production numerical freeze.

---

# Closed lower-layer validation

Historical all-20:
```text
20 recipes × 3 deterministic brackets × 5 classes = 300 combat rows
36 designated role pairs × 15 rows = 540 checks
540 / 540 PASS
```

Corrected provisional central all-20:
```text
20 recipes × 3 base seeds × 5 classes = 300 combat rows
36 designated role pairs × 15 rows = 540 checks
540 / 540 PASS
```

Historical regression after localized E08/E20 refinements remains `540 / 540 PASS`.

Player central prior remains a user-authorized design prior, not empirical population fit:

```text
PERFECT 70%
GOOD    20%
NORMAL  10%
```

---

# P1 — STRUCTURALLY CLOSED

Authority:
`legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`

Approved:
- Base HP / Max HP persist across Stage/shop in one Tier attempt.
- no automatic Stage/shop heal.
- Base HP 0 ends the attempt.
- retry starts fresh Stage1 run-local state while account-permanent state remains.
- combo and charge persist across Stage/shop downtime.
- started Heavy X→Y resolves before Stage transition finalizes.
- reconnect restores same authoritative attempt without implicit reset/heal.

---

# P2 — STRUCTURALLY CLOSED

Authority:
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`

Approved:
- ordinary same-stat scalar progression bonuses aggregate additively by default;
- multiplication is explicit/opt-in;
- scalar stats are separate from effect rules/procs/geometry;
- outgoing/incoming operation orders are explicit;
- source modifier state is authoritative; effective values are derived/recomputable;
- deterministic Power Attribution Ledger is required for simulator/test;
- repeated intermediate rounding is avoided.

---

# P3 — STRUCTURAL PASS / COMPLETE

Authority/evidence:
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p3_execution_summary_v0_1.json`

Final P3 result:

```text
30 / 30 primary 10-Stage runs PASS
8 / 8 targeted fixtures PASS
deterministic replay PASS
continuous player-model stream PASS
snapshot/resume equivalence PASS
P1 failure/retry parity PASS
P2 additive aggregation + attribution PASS
temporary-effect boundary PASS
Base HP attrition continuity PASS
forced Lv6 plumbing PASS across all five classes
```

P3 does not calibrate final EXP, actual Lv6 reach, Base HP, shop, clear rate or exact launch content.

---

# P4 preproposal evidence

Reproducible P3-derived diagnostic found:

Legacy absolute prototype thresholds:

```text
Lv6    420
Lv11  1140
Lv16  2160
Lv21  3480
Lv26  5100
Lv31  7020
```

When replayed on the current synthetic P3 first-10 lane using legacy completed-turn EXP rewards:

```text
Lv6   P25/P50/P75 = Stage2 / 2 / 3
Lv11  P25/P50/P75 = Stage6 / 6 / 7
Lv16  P25/P50/P75 = Stage10 / 10 / 10
```

Therefore the legacy absolute `levelNeed()` curve is incompatible with the current 50-Stage skill windows.

P3 forced-Lv6 event-opportunity feedback in the synthetic first-10 fixture:

```text
Knight  ~ -0.2%
Rogue   ~ -20.2%
Tank      0.0%
Archer  ~ -18.9%
Mage    ~ -14.7%
```

This proves the loop `skill power -> faster kills -> fewer timing opportunities -> slower later EXP` is materially present already at Lv6 for some classes.
It is monitored feedback, not automatic authorization for compensation.

---

# P4 proposal — USER DECISION REQUIRED

Proposal authority candidate:
`legacy-game-structure/78_P4_FULL_PLAYER_POWER_SPINE_EXP_MODEL_PROPOSAL_V0_1.md`

Recommended package awaiting approval:
1. EXP baseline remains valid completed local timing-turn based only; no kill/damage/passive/flat Stage-clear XP and no hidden class correction.
2. one EXP award per completed timing turn; Heavy X+Y resolves to one combined quality reward.
3. calibrate in dimensionless `XP_CREDIT`; use the legacy relative quality vector as primary candidate, not the obsolete absolute scale.
4. replace legacy closed-form `levelNeed()` with six cumulative milestone anchors Lv6/11/16/21/26/31 plus transparent monotonic interpolation.
5. calibrate against T1–T4 multi-schedule synthetic 50-Stage corpus, initially three legal opportunity envelopes per Tier; no exact launch authoring.
6. Lv6 authoritative and Lv11/16/21 exact v0.16 parity mechanics may be used as simulation-only feedback candidates after a marker-only inverse-design pass; Lv26/Lv31 remain separate user gates.
7. first fit P50 to milestone windows and record P25/P50/P75/P90; exact tail cutoffs are proposed only after the first 50-Stage evidence. Lv31 Stage41–45 remains user-confirmed structural direction.
8. one universal EXP curve across classes/Tiers; kill-speed-driven EXP reduction is measured self-damping unless evidence proves structural failure. Any stabilizer/catch-up layer requires a later decision gate.

Until approved:
- do not implement P4-A/B 50-Stage EXP simulator/data as accepted methodology;
- do not freeze any XP credit weight or milestone threshold;
- do not promote Lv11–21 parity candidates to production authority;
- do not invent Lv26/Lv31 power proxies.

---

# Decision governance

For every unresolved material decision:

```text
inspect live canonical
 -> analyze dependencies
 -> calculate/simulate
 -> compare real alternatives
 -> recommend
 -> USER APPROVAL
 -> author / validate / record accepted direction
```

A passing diagnostic does not self-authorize a design decision.

---

# Still not frozen

- final launch Tier count / Tier unlock policy
- production monster coefficients/coordinates
- exact 200-Stage schedule
- exact EXP formula / XP display amounts / milestone thresholds
- exact percentile tail acceptance gates
- exact shop cadence/economy
- exact Base HP
- modifier numeric coefficients/caps
- permanent star milestone/value ladder
- achievement reward graph/value
- exact boss cadence/design
- Lv26/Lv31 mechanics
- multiplayer disconnect operational policy
- multiplayer progression credit/scaling coefficients

No production gameplay source or production balance value was changed by the P4 analysis/proposal.
