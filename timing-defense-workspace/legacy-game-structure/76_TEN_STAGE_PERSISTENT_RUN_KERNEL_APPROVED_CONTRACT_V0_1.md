# Timing Defense — Ten-Stage Persistent Run Kernel Approved Contract V0.1

Date: 2026-10-23 KST  
Status: **USER_APPROVED_DIRECTION / P3 STRUCTURAL CONTRACT / NO NUMERICAL BALANCE FREEZE**

Depends on:
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `75_TEN_STAGE_PERSISTENT_RUN_KERNEL_PROPOSAL_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`

Machine-readable companion:
- `data/p3_persistent_run_kernel_contract_v0_1.yaml`

---

# 0. Approval boundary

The user approved the full eight-item P3 recommendation package in document 75.

This approval freezes P3 **test semantics and integration boundaries only**.
It does not freeze campaign balance, final Stage content, EXP, Base HP, shop, boss, permanent progression, or multiplayer progression values.

Approved package:
1. current-Model-A T1-shaped synthetic first-10 fixture using GRUNT/RUNNER only in the main lane;
2. dual power lanes: `LV1_CONTINUITY` and deterministic `FORCED_LV6_TRANSITION` at Stage6 start;
3. no exact EXP formula in P3;
4. no real shop/economy in P3; neutral Stage transition plus sentinel coin/shop persistence tests;
5. ordinary Stage-local `TEMPORARY` combat effects settle and then clear at Stage boundary;
6. explicit `STAGE_SETTLED` barrier before Stage advancement;
7. one continuous SKILLED_V2_CENTRAL player-model/RNG state across the Tier attempt, with named RNG substreams where applicable;
8. primary execution matrix = 5 classes × 3 base seeds × 2 lanes = 30 persistent runs plus bounded targeted fixtures; P3 output is `lv6_transition_plumbing_evidence`, not Lv6 reach calibration.

---

# 1. Synthetic first-10 fixture

P3 uses a test-only T1-shaped slice consistent with current Model A.

Main-lane vocabulary:
- GRUNT baseline;
- RUNNER teach/mix;
- no BRUTE in Stage1–10;
- no Stage10 boss.

Fixture grammar:

```text
S1  E01 baseline
S2  E01 baseline
S3  E01 baseline
S4  E01 transition
S5  E02 RUNNER teach
S6  E02 RUNNER teach
S7  E02 RUNNER consolidation
S8  E02 mixed
S9  separated E01 -> E02
S10 separated E02 -> E01 checkpoint
```

The fixture reuses existing representative recipe anchors and current analysis coefficients.
It is not exact launch Stage authoring and must not be promoted as such.

---

# 2. Power lanes

## L0 — LV1_CONTINUITY
- level fixed at 1;
- EXP formula disabled;
- valid/EXP-eligible timing-event counts may be recorded for downstream analysis;
- purpose = pure state continuity and P1/P2 integration.

## L1 — FORCED_LV6_TRANSITION
- exact EXP formula disabled;
- deterministic test hook activates Lv6 at Stage6 start;
- purpose = prove LEVEL/effect-rule transition plumbing and attribution.

P3 must not claim that the final game reaches Lv6 at Stage6.
Actual Lv6/11/16/21/26/31 reach calibration belongs to P4.

---

# 3. Shop / coin boundary

Primary P3 lane:
- `shopPolicy = OFF/NEUTRAL`;
- no shop UI or purchase agent;
- no coin income/economy tuning;
- every clear crosses a logical `STAGE_TRANSITION`, not an implied product shop cadence.

Targeted fixtures may inject nonzero test-only `runCoin` and `shopRanks` sentinel values to prove persistence across Stage transition and snapshot/resume.
These sentinel values are not balance candidates.

---

# 4. Temporary combat effects

Default Stage-boundary rule:
- already-authorized current-Stage action effects may finish resolution;
- after the settlement barrier, ordinary `TEMPORARY` Stage-local combat effects are cleared;
- such effects do not pause/bank through intermission and reappear in the next Stage;
- mechanics intentionally designed to cross Stage boundaries require explicit RUN/inter-stage-persistent scope.

This does not change the approved persistence of Base HP, combo, charge, level/EXP, coin, shop ranks, and run identity.

---

# 5. STAGE_SETTLED barrier

A Stage may advance only when:

```text
last authored Stage spawn has occurred
+ no live Stage-owned enemy remains
+ no new current-Stage player turn is accepted
+ already-authorized current-action/effect resolution is drained
+ no unresolved half-Heavy / delayed Stage hit / Stage-local transient remains
= STAGE_SETTLED
```

Then:
- StageState is reset;
- Stage number advances;
- persistent RunState remains.

No projectile, delayed hit, target identity, enemy instance, monster capability state, Stage timer, or Stage-local temporary object may leak into the next Stage.

### Terminal collision boundary
If testing produces a genuinely unresolved same-timestamp terminal collision such as Base HP reaching zero at the exact final-clear boundary, P3 must emit:
`SIMULTANEOUS_TERMINAL_COLLISION_OPEN_DECISION`

P3 must not silently create a new win/loss precedence rule.

---

# 6. Player-model and RNG continuity

One SKILLED_V2_CENTRAL player-model stream belongs to one Tier attempt.

Rules:
- FOCUS/BASE state is not reset per Stage;
- the same short PRNG prefix is not restarted per Stage;
- snapshot/resume preserves player-model state and RNG state exactly;
- random domains should use named deterministic substreams so a combat-proc draw does not silently shift player-judgment draws.

Initial named domains:
- `JUDGMENT`
- `COMBAT_PROC`
- optional future `STAGE_FIXTURE` if random fixture authoring is ever introduced.

Current fixed Stage fixture itself need not consume RNG.

The existing 1100ms action interval remains:
`BOUNDED_CURRENT_MECHANIC_SIMULATION_CONTROL_NOT_SKILL_FIT`.

---

# 7. Execution matrix

Primary structural matrix:

```text
5 classes
× 3 existing base seeds [101, 211, 307]
× 2 power lanes [LV1_CONTINUITY, FORCED_LV6_TRANSITION]
= 30 persistent 10-stage runs
```

The 30-run result is not production clear-rate evidence.
Primary fixture Base HP may use a deliberately nonterminal `TEST_ONLY` sentinel so lifecycle integration can complete 10 Stage transitions without pretending the number is balanced.

Failure/reset semantics are validated separately with a deliberately low-HP test fixture.

---

# 8. Mandatory targeted fixtures

P3 implementation must include bounded deterministic tests for at least:

1. `F1_CHARGE_CONTINUITY`
2. `F2_COMBO_N3_BOUNDARY`
3. `F3_FAILURE_RETRY_RESET`
4. `F4_SNAPSHOT_RESUME_EQUIVALENCE`
5. `F5_MODIFIER_AGGREGATION_ATTRIBUTION`
6. `F6_TEMPORARY_EFFECT_BOUNDARY`
7. `F7_NO_TRANSIENT_LEAKAGE`

Snapshot/resume coverage must include inter-Stage and mid-Stage state, including advanced player-model/RNG state.

---

# 9. Attribution and reconciliation

P3 inherits P2 attribution requirements.

At minimum it must explain and reconcile:
- ordinary player damage;
- forced Lv6 effect contribution;
- combo transform;
- N3 targeted-fixture contribution;
- wall damage;
- generic/unique/shield contribution when activated by a fixture;
- Base HP delta.

With healing/max-HP changes OFF in the primary lane:

```text
sum(realized Base HP damage ledger)
== startBaseHp - endBaseHp
```

per Stage/run as applicable.

---

# 10. P3 acceptance gates

P3 may pass structurally only if:
1. identical versioned inputs + class + lane + seed reproduce identical trace/final hash;
2. all primary lanes can cross the ten configured Stage transitions without hidden state reset/leak;
3. Base HP, combo, charge and run identity obey P1;
4. forced Lv6 changes only authorized LEVEL/effect paths and is attributable;
5. neutral transitions do not mutate coin/shop state;
6. snapshot/resume equals uninterrupted execution;
7. failure/retry exactly matches P1 reset semantics;
8. P2 same-stat additive aggregation and attribution reconciliation pass;
9. `STAGE_SETTLED` has no forbidden StageState/transient leakage;
10. no test-only number is promoted into a final EXP/shop/Base-HP/difficulty value.

Allowed failure classifications include:
- `STATE_LEAK`
- `STAGE_TRANSITION_RESET_DEFECT`
- `SNAPSHOT_REPLAY_DIVERGENCE`
- `PLAYER_SEQUENCE_RESEED_DEFECT`
- `ATTRIBUTION_RECONCILIATION_DEFECT`
- `TEMPORARY_SCOPE_LEAK`
- `FAIL_RETRY_RESET_DEFECT`
- `SIMULTANEOUS_TERMINAL_COLLISION_OPEN_DECISION`

Successful classification:
- `P3_STRUCTURAL_PASS`

---

# 11. Explicitly remains OPEN

P3 approval does not decide:
- exact EXP formula;
- actual Lv6 reach distribution;
- exact Base HP;
- exact shop cadence/price/value;
- coin income/reward curve;
- exact T1 Stage1–10 production authoring;
- Stage10 boss placement/mechanics;
- permanent star or achievement values;
- final difficulty/clear rates;
- production numerical coefficients;
- multiplayer progression/scaling;
- simultaneous terminal collision precedence if actual evidence exposes it;
- production implementation/deployment.

---

# 12. Next execution boundary

P3 structural choices are now user-approved.

Next:
1. implement machine-readable P3 fixture/contract;
2. implement deterministic persistent-run kernel and validator;
3. execute 30 primary runs + targeted fixtures;
4. report defects/watches without turning test-only sentinels into balance values;
5. only if structural gates pass, close P3 and move to P4 EXP / full player-power spine candidate work.
