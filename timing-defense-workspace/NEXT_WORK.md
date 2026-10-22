# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — P3 TEN-STAGE PERSISTENT RUN KERNEL / USER DECISION GATE

Completed chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> encounter envelope PASS
 -> role-expression calibration
 -> All-20 historical 540/540
 -> provisional streak-aware SKILLED_V2_CENTRAL
 -> corrected central all-20 540/540
 -> system dependency / calibration-order review
 -> user-approval governance
 -> P1 Run-State Lifecycle USER_APPROVED_STRUCTURAL_COMPLETE
 -> P2 Modifier Pipeline / Power Attribution USER_APPROVED_STRUCTURAL_COMPLETE
 -> P3 analysis / proposal complete
```

Current authority / proposal:
- `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/75_TEN_STAGE_PERSISTENT_RUN_KERNEL_PROPOSAL_V0_1.md` — **PROPOSED / NOT APPROVED**
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`
- `legacy-game-structure/data/system_dependency_calibration_order_v0_1.yaml`

---

# P1 / P2 CLOSED STRUCTURALLY

P1 approved state lifecycle remains authoritative:
- Base HP / Max HP persist across Stage/shop; no automatic transition heal.
- Base HP 0 ends the attempt; retry starts fresh Stage1 run-local state.
- combo and charge persist across Stage/shop downtime.
- started Heavy X->Y resolves before Stage transition finalizes.
- reconnect restores the same authoritative attempt without implicit reset/heal.

P2 approved power semantics remain authoritative:
- same ordinary scalar stat progression bonuses aggregate additively by default;
- scalar stats and effect rules are separate;
- outgoing/incoming operation orders are explicit;
- effective stats are derived from authoritative source state;
- deterministic Power Attribution Ledger is required for simulator/test;
- realized-effect-boundary rounding is used by default.

Numerical reward values/caps remain open.

---

# P3 ANALYSIS RESULT — AWAITING USER APPROVAL

Proposal:
`legacy-game-structure/75_TEN_STAGE_PERSISTENT_RUN_KERNEL_PROPOSAL_V0_1.md`

Important consistency finding:
- the old `11_T1_STAGE_SKELETON_CANDIDATE_V0_1.md` reflects the superseded all-nine-monsters-in-T1 direction;
- current Model A first-10 T1 grammar is GRUNT baseline -> RUNNER teach/mix -> GRUNT/RUNNER checkpoint;
- P3 must therefore use a separate current-Model-A synthetic fixture rather than copy the stale T1 schedule.

Recommended P3 package awaiting decision:
1. T1-shaped synthetic first-10 integration fixture; GRUNT/RUNNER only in the main lane; no BRUTE/boss yet.
2. two power lanes: `LV1_CONTINUITY` and deterministic `FORCED_LV6_TRANSITION` at Stage6; no exact EXP formula/reach claim.
3. no real shop/economy; neutral Stage transition plus sentinel coin/shop persistence fixtures.
4. ordinary Stage-local `TEMPORARY` combat effects settle then clear at Stage boundary; explicit RUN-scoped effects only may persist.
5. explicit `STAGE_SETTLED` barrier drains already-authorized current-action effects before transition and forbids transient leakage.
6. one continuous `SKILLED_V2_CENTRAL` judgment/RNG state across the whole attempt; no per-Stage reseeding.
7. primary structural matrix = 5 classes × 3 seeds × 2 power lanes = 30 persistent 10-stage runs, plus bounded targeted contract fixtures.
8. P3 output should be `lv6_transition_plumbing_evidence`, not `provisional_lv6_reach_evidence`; actual EXP/reach calibration belongs to P4.

Implementation/data/validator creation is **not authorized yet**. User approval or modification is required first.

---

# P3 intended scope after approval

P3 validates:
- deterministic multi-stage state continuity;
- Base HP / failure / retry semantics;
- combo / charge continuity;
- Stage settlement/reset boundaries;
- snapshot/resume equivalence;
- P2 modifier-pipeline execution;
- attribution-ledger reconciliation;
- Lv6 transition plumbing;
- no stale transient StageState leakage.

P3 is not final campaign balance.

Keep OFF / parameterized:
- exact permanent star values;
- achievement reward values;
- final shop tuning/cadence/prices;
- exact final EXP formula;
- final Base HP balance;
- final boss novelty;
- multiplayer progression credit;
- exact launch Stage authoring.

---

# Decision governance — mandatory

For unresolved material decisions:

```text
live canonical inspection
 -> dependency / interaction analysis
 -> calculation/simulation where useful
 -> compare alternatives
 -> assistant recommendation + risks/reversibility
 -> USER DECISION GATE
 -> only then author / validate / record accepted direction
```

Diagnostic work may proceed without micro-approval, but test success is not self-authorizing.

---

# Do not yet

- implement the P3 kernel before the proposal is approved
- modify/deploy production v0.45 gameplay
- author exact 200 launch Stages
- freeze exact EXP formula
- freeze exact shop cadence/price/value curve
- freeze permanent star values
- freeze achievement reward graph/value
- freeze exact Base HP
- freeze exact boss mechanics
- freeze multiplayer disconnect timeout/AI/reward details
- freeze multiplayer progression-credit/scaling values
- silently resolve unresolved Lv26/Lv31 or multihit crit semantics
