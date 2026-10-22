# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

---

# Current phase

**P3 — TEN-STAGE PERSISTENT RUN KERNEL / STATE+PIPELINE INTEGRATION**

The project has completed:
- campaign spine validation;
- all-20 role-expression validation;
- provisional streak-aware `SKILLED_V2_CENTRAL` integration;
- system dependency / calibration-order review;
- user-approval decision governance;
- P1 Run-State Lifecycle structural closure;
- P2 Modifier Pipeline / Power Attribution structural closure.

Current execution authority:
- `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`
- `legacy-game-structure/data/system_dependency_calibration_order_v0_1.yaml`

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
- T1 does not expose all 9; higher Tiers introduce species.
- future T5/T6/T7+ and new monsters remain open.
- provisional non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60% as an upper difficulty gate.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- intended monster roles must become perceivable before deletion.

Model A remains the default bounded simulation spine:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future
```

NOT production frozen.

---

# Closed validation chain

Historical all-20:
```text
20 recipes × 3 deterministic brackets × 5 classes = 300 combat rows
36 designated role pairs × 15 rows = 540 structural checks
540 / 540 PASS
```

Corrected provisional central all-20:
```text
20 recipes × 3 base seeds × 5 classes = 300 combat rows
36 designated role pairs × 15 rows = 540 structural checks
540 / 540 PASS
```

Historical regression after localized E08/E20 refinements also remains `540 / 540 PASS`.

Important watches:
- T4 siege wall pressure in persistent/full-Tier runs;
- T3 E13 wall pressure;
- E20 CHARGER lower-tail readability;
- combo40 cannot be judged from short representative encounters.

---

# Player-model boundary

Primary-user observed traces remain `HIGH_MASTERY_STRESS_CANDIDATE`, not ordinary-skilled population evidence.

User-authorized bounded design prior:

```text
PERFECT 70%
GOOD    20%
NORMAL  10%
```

Implemented as a streak-aware deterministic candidate.
Status: `PROVISIONAL DESIGN PRIOR / NOT EMPIRICAL POPULATION FIT`.

---

# P1 — STRUCTURALLY CLOSED

Authority: `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`.

Approved:
- Base HP / Max HP persist through Stage/shop within the attempt.
- no automatic Stage/shop healing.
- Base HP 0 ends the attempt.
- retry starts a fresh Stage1 run-local state while account-permanent state remains.
- combo and charge persist through Stage/shop downtime.
- started Heavy X->Y resolves before Stage transition finalizes.
- disconnect != leave.
- reconnect restores same authoritative run/player state without reset/heal.
- transient multiplayer disconnect does not immediately reduce enemy pressure.
- transient disconnect alone does not immediately invalidate reward/star/achievement eligibility.

Deferred to P10/P16 or later engineering policy:
- reconnect grace duration;
- AI takeover/substitution;
- confirmed-abandonment threshold;
- pressure rescaling after abandonment;
- reward/achievement credit after long disconnect/AI takeover;
- host migration details;
- all-human disconnect behavior;
- storage/retention implementation.

---

# P2 — STRUCTURALLY CLOSED

Authority: `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`.

Approved:
- ordinary same-stat progression bonuses aggregate additively by default;
- multiplication is explicit/opt-in, not implied by subsystem boundaries;
- scalar stats are separated from effect rules/procs/geometry;
- authoritative outgoing order is action validation -> timing/Heavy/P×P -> attack template -> effective scalar stats -> action transforms/combo -> crit policy -> hit geometry -> per-target mitigation -> realized effect -> consequences -> isolated procs;
- generic wall DR -> unique class/team defense -> shield -> Base HP;
- source modifier state is authoritative and effective stats are derived/recomputable;
- deterministic Power Attribution Ledger is required for simulator/test authority;
- repeated intermediate rounding is avoided; rounding occurs at realized effect boundaries, preserving existing fixed-budget contracts.

Still open:
- exact star/achievement/shop values;
- crit and generic defense caps;
- exact Base HP;
- unresolved multihit crit inheritance;
- final Lv26/Lv31 contracts;
- exact numeric representation;
- production implementation.

---

# Exact current boundary

Completed through:
`P2 MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION`.

## NEXT — P3 TEN_STAGE_PERSISTENT_RUN_KERNEL
Purpose:
- integrate P1 state lifecycle and P2 power pipeline in one deterministic multi-stage run;
- validate persistence/transition/failure/retry and attribution;
- expose provisional multi-stage wall-pressure and early skill-reach evidence;
- **not** final campaign balance.

P3 must keep OFF / parameterized:
- permanent star values;
- achievement values;
- final shop tuning;
- exact final EXP formula;
- final boss novelty;
- multiplayer progression credit;
- exact launch Stage authoring.

Material P3 design choices still require analysis -> proposal -> user approval before closure.

---

# Decision governance

For every unresolved material decision:

```text
inspect live canonical
 -> analyze dependencies
 -> calculate/simulate
 -> compare alternatives
 -> recommend
 -> USER APPROVAL
 -> record accepted direction
```

A candidate passing simulation is not authorization to freeze it.

---

# Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster coefficients/coordinates
- exact 200-Stage schedule
- exact EXP formula
- Lv11+ production coefficients not already frozen
- exact shop cadence/economy
- modifier numeric coefficients/caps
- permanent star milestone/value ladder
- achievement reward graph/value
- exact boss cadence/design
- multiplayer disconnect operational policy
- multiplayer progression credit/scaling coefficients

No production gameplay source or production balance value was changed by P2 closure.
