# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

---

# Current phase

**P3 — TEN-STAGE PERSISTENT RUN KERNEL / PROPOSAL AWAITING USER DECISION**

Completed:
- campaign spine validation;
- all-20 role-expression validation;
- provisional streak-aware `SKILLED_V2_CENTRAL` integration;
- system dependency / calibration-order review;
- user-approval decision governance;
- P1 Run-State Lifecycle structural closure;
- P2 Modifier Pipeline / Power Attribution structural closure;
- P3 dependency/fixture/state-boundary analysis and proposal authoring.

Current authority / proposal:
- `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/75_TEN_STAGE_PERSISTENT_RUN_KERNEL_PROPOSAL_V0_1.md` — **PROPOSED / NOT APPROVED**
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`
- `legacy-game-structure/data/system_dependency_calibration_order_v0_1.yaml`

P3 implementation is not yet authorized.

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
- current bounded Model A roster ladder:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future
```

- provisional non-T1 `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60% as an upper difficulty gate.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- intended monster roles must become perceivable before deletion.

Model A is the active bounded simulation spine, not production freeze.

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

Watches retained:
- T4 siege wall pressure in persistent/full-Tier runs;
- T3 E13 wall pressure;
- E20 CHARGER lower-tail readability;
- combo40 needs persistent-run context.

Player central prior remains a design prior, not empirical population fit:
`PERFECT 70 / GOOD 20 / NORMAL 10`, implemented streak-aware.
Primary-user observed traces remain upper-tail `HIGH_MASTERY_STRESS_CANDIDATE` evidence only.

---

# P1 — STRUCTURALLY CLOSED

Authority: `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`.

Approved:
- Base HP / Max HP persist across Stage/shop; no automatic transition heal.
- Base HP 0 ends the attempt.
- retry starts fresh Stage1 run-local state while account-permanent state remains.
- combo and charge persist across Stage/shop downtime.
- started Heavy X->Y resolves before Stage transition finalizes.
- reconnect restores same authoritative attempt without reset/heal.
- transient multiplayer disconnect does not immediately lower pressure or invalidate progression credit.

Reconnect grace, AI takeover, abandonment, post-abandon scaling, long-absence reward credit, host migration and durable storage remain downstream.

---

# P2 — STRUCTURALLY CLOSED

Authority: `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`.

Approved:
- same ordinary scalar stat progression bonuses aggregate additively by default;
- multiplication is explicit/opt-in;
- scalar stats are separate from effect rules/procs/geometry;
- outgoing and incoming operation orders are explicit;
- source modifier state is authoritative; effective values are derived/recomputable;
- deterministic Power Attribution Ledger is required for simulator/test;
- repeated intermediate rounding is avoided; realized-effect-boundary rounding is the default.

Exact star/achievement/shop values, caps, Base HP, unresolved multihit crit inheritance, final Lv26/Lv31 contracts and production implementation remain OPEN.

---

# P3 proposal — USER DECISION REQUIRED

Authority candidate:
`75_TEN_STAGE_PERSISTENT_RUN_KERNEL_PROPOSAL_V0_1.md`.

Key consistency correction:
- old `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md` belongs to the superseded all-nine-monsters-in-T1 direction;
- current Model A first 10 T1 Stages use GRUNT baseline and RUNNER teach/mix, with BRUTE first-teach later;
- P3 therefore proposes a separate current-Model-A synthetic fixture, not exact launch authoring.

Recommended package awaiting approval:
1. T1-shaped GRUNT/RUNNER first-10 synthetic fixture; no BRUTE/boss in the main lane.
2. `LV1_CONTINUITY` + `FORCED_LV6_TRANSITION` power lanes; no exact EXP formula/reach claim.
3. neutral Stage transition; no real shop/economy; sentinel coin/shop persistence tests only.
4. ordinary Stage-local TEMPORARY combat effects settle then clear; only explicit RUN-scoped effects may persist.
5. `STAGE_SETTLED` barrier drains authorized current-action effects and forbids transient leakage.
6. one continuous skilled judgment/RNG state across the whole attempt; no per-Stage reseeding.
7. 30-run primary structural matrix plus bounded targeted fixtures.
8. P3 output = `lv6_transition_plumbing_evidence`; actual Lv6 reach calibration remains P4.

Until approved:
- do not implement P3 kernel/data/validator;
- do not treat any P3 proposal item as structural freeze.

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
 -> author / validate / record accepted direction
```

A passing simulation does not self-authorize a design decision.

---

# Still not frozen

- final launch Tier count / unlock policy
- production monster coefficients/coordinates
- exact 200-Stage schedule
- exact EXP formula
- exact shop cadence/economy
- exact Base HP
- modifier numeric coefficients/caps
- permanent star values
- achievement reward graph/value
- exact boss cadence/design
- unresolved Lv26/Lv31 details
- multiplayer disconnect operational policy
- multiplayer progression credit/scaling coefficients

No production gameplay source or production balance value was changed by the P3 proposal.
