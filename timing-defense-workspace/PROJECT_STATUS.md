# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE / ANALYSIS & USER DECISION GATE**

Completed through:

```text
P0 Foundation / role expression
 -> historical all-20 540/540
 -> provisional SKILLED_V2_CENTRAL
 -> corrected central all-20 540/540
 -> P1 Run-State Lifecycle structural closure
 -> P2 Modifier Pipeline / Power Attribution structural closure
 -> P3 Ten-Stage Persistent Run Kernel STRUCTURAL PASS
```

Active dependency plan:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_2.yaml`

---

# Core structural truth

- 5 classes progress independently through Tiers.
- same Tier/Stage combat content across classes.
- Tier = 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intended; hard class lockout forbidden.
- current 9 monsters are V1 foundation, not lifetime final roster.
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

Watches retained for later full-Tier work:
- T4 siege wall pressure;
- T3 E13 wall pressure;
- E20 CHARGER lower-tail readability;
- contextual timing degradation is not yet empirically fitted.

Player central prior remains a user-authorized design prior, not empirical population fit:

```text
PERFECT 70%
GOOD    20%
NORMAL  10%
```

implemented as a streak-aware deterministic two-state candidate.

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
- reconnect restores the same authoritative attempt without implicit reset/heal.
- transient multiplayer disconnect does not immediately lower pressure or invalidate progression credit.

Reconnect grace, AI takeover, abandonment, post-abandon scaling, long-absence reward credit, host migration and production storage remain downstream.

---

# P2 — STRUCTURALLY CLOSED

Authority:
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`

Approved:
- same ordinary scalar stat progression bonuses aggregate additively by default;
- multiplication is explicit/opt-in;
- scalar stats are separate from effect rules/procs/geometry;
- outgoing/incoming operation orders are explicit;
- source modifier state is authoritative; effective values are derived/recomputable;
- deterministic Power Attribution Ledger is required for simulator/test;
- repeated intermediate rounding is avoided; realized-effect-boundary rounding is the default.

Exact reward/shop values, caps, Base HP, unresolved multihit crit inheritance, final Lv26/Lv31 contracts and production implementation remain OPEN.

---

# P3 — STRUCTURAL PASS / COMPLETE

Authority/evidence:
- `legacy-game-structure/75_TEN_STAGE_PERSISTENT_RUN_KERNEL_PROPOSAL_V0_1.md` — historical proposal
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p3_persistent_run_kernel_contract_v0_1.yaml`
- `legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json`
- `legacy-game-structure/data/p3_execution_summary_v0_1.json`
- `tools/run_p3_persistent_kernel_v0_1.py`
- `tools/validate_p3_persistent_kernel_v0_1.py`

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

Exact executed canonical Git blobs:

```text
runner    a9395716166185dd253685991a074dfdac3bf3c7
validator f7f4d183c58220435bb7d33aa7add58dd858023b
fixture   cf809f34991fabd94037a8f5a3205731b3447451
```

Important P3 interpretation limits:
- primary Base HP sentinel `100000` is test-only;
- Stage6 forced Lv6 is a plumbing hook, not an EXP reach result;
- shop is OFF/NEUTRAL;
- synthetic first-10 fixture is not exact launch authoring;
- `combo40 observed 30/30` is structural evidence only, not a production frequency target;
- P3 does not calibrate clear rate or final wall pressure.

---

# Exact current boundary — P4

## P4 FULL_PLAYER_POWER_SPINE_CANDIDATE

Purpose:
- build a provisional 50-Stage synthetic run-power spine;
- calibrate EXP/level/skill reach before real shop leverage and permanent progression are introduced;
- measure Lv6/11/16/21/26/31 reach distributions and usable post-unlock windows;
- preserve attribution so skill power spikes are distinguishable from encounter-pressure changes.

Known target windows:

```text
Lv6   Stage 5–7   candidate
Lv11  Stage11–14  candidate
Lv16  Stage18–21  candidate
Lv21  Stage25–28  candidate
Lv26  Stage32–36  candidate
Lv31  Stage41–45  USER-CONFIRMED DIRECTION
```

P4 first pass constraints:
- SOLO first;
- shop OFF/NEUTRAL;
- P0/fresh permanent-power baseline;
- synthetic 50-Stage skeleton, not exact 200 launch Stages;
- no final shop/economy values;
- no star/achievement power tuning;
- no production deployment.

Material P4 choices — especially EXP model/formula, milestone percentile acceptance bands, and any unresolved Lv26/Lv31 simulation authority — require analysis/calculation/recommendation and explicit user approval before closure.

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

A passing simulation does not self-authorize a design decision.

---

# Still not frozen

- final launch Tier count / Tier unlock policy
- production monster coefficients/coordinates
- exact 200-Stage schedule
- exact EXP formula
- exact shop cadence/economy
- exact Base HP
- modifier numeric coefficients/caps
- permanent star milestone/value ladder
- achievement reward graph/value
- exact boss cadence/design
- unresolved Lv26/Lv31 details
- multiplayer disconnect operational policy
- multiplayer progression credit/scaling coefficients

No production gameplay source or production balance value was changed by P3 closure.
