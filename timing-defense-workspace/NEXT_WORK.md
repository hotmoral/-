# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — P3 TEN-STAGE PERSISTENT RUN KERNEL

Completed chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> encounter envelope PASS
 -> role-expression calibration
 -> Critical 10 PASS_WITH_WATCHES
 -> All-20 historical 540/540
 -> provisional streak-aware SKILLED_V2_CENTRAL
 -> corrected central all-20 540/540
 -> system dependency / calibration-order review
 -> user-approval decision gate governance
 -> P1 Run-State Lifecycle USER_APPROVED_STRUCTURAL_COMPLETE
 -> P2 Modifier Pipeline / Power Attribution USER_APPROVED_STRUCTURAL_COMPLETE
```

Current authority:
- `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/73_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_PROPOSAL_V0_1.md` — historical proposal
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`
- `legacy-game-structure/data/system_dependency_calibration_order_v0_1.yaml`

---

# P1 CLOSED STRUCTURALLY

Approved P1 directions remain:
- Base HP / Base Max HP persist across Stage/shop within one Tier attempt.
- no automatic Stage/shop healing.
- Base HP 0 ends the attempt.
- retry starts a fresh Stage1 attempt; run-local state resets and permanent account state remains.
- combo and charge persist across Stage/shop downtime.
- started Heavy X->Y resolves before Stage transition finalizes.
- disconnect != leave.
- reconnect restores the same authoritative player/run state without implicit reset/heal.
- transient multiplayer disconnect does not immediately reduce enemy pressure.
- transient disconnect alone does not immediately invalidate reward/star/achievement eligibility.

P10/P16 later decide disconnect grace, AI substitution, abandonment, post-abandonment scaling, reward credit and host migration details.

---

# P2 CLOSED STRUCTURALLY

Approved P2 directions:
1. **Typed hybrid stacking** — ordinary same-stat progression bonuses aggregate additively by default; multiplication is explicit/opt-in.
2. **Stat/effect separation** — penetration, splash, shields, armor-ignore, tracking, proc generation, etc. remain effect rules rather than fake scalar stats.
3. **Outgoing attack pipeline** — action validation -> timing/Heavy/P×P -> attack template -> effective scalar stats -> action transforms/combo -> crit policy -> hit materialization -> per-target mitigation -> realized effect -> death/secondary consequences -> isolated post-action procs.
4. **Incoming wall pipeline** — monster raw damage -> capability/state modifier -> generic DR -> unique class/team defense -> shield -> Base HP.
5. **Derived stats remain derived** — source state is authoritative; effective values are recomputed/cache only.
6. **Deterministic Power Attribution Ledger** required for simulator/test authority.
7. **Delayed rounding** — avoid repeated intermediate rounding; round at realized hit/control boundaries while preserving frozen fixed-budget allocators such as N3.

Still OPEN:
- exact star/achievement/shop modifier values;
- crit cap and generic defense cap;
- exact Base HP;
- unresolved per-skill crit inheritance;
- final Lv26/Lv31 contracts;
- exact numeric representation;
- production implementation.

---

# Decision governance — mandatory

For unresolved material decisions:

```text
live canonical inspection
 -> dependency / interaction analysis
 -> calculation or simulation where useful
 -> compare real alternatives
 -> assistant recommendation + risks/reversibility
 -> USER DECISION GATE
 -> only then record accepted/frozen direction
```

Diagnostic work may proceed without micro-approval, but test success is not self-authorizing.

---

# EXACT NEXT BOUNDARY

## P3 — TEN_STAGE_PERSISTENT_RUN_KERNEL

Purpose:
- integrate the approved P1 state lifecycle with the approved P2 modifier/attribution semantics;
- prove deterministic state continuity across multiple Stage transitions;
- expose the first multi-stage attrition and progression traces;
- do **not** treat the result as final campaign balance.

Required P3 design/implementation analysis before execution:
1. define the smallest 10-stage state machine using the P1 attempt lifecycle;
2. decide which already-authoritative/candidate combat content is safe for the kernel without pretending it is final launch Stage content;
3. define deterministic Stage-transition and seed behavior;
4. persist and verify Base HP, combo, charge, level/EXP candidate state and run identity;
5. execute the approved P2 modifier pipeline even when many downstream modifiers are zero/disabled;
6. emit deterministic Power Attribution records;
7. validate failure/reset/retry behavior;
8. measure, but do not freeze, provisional Lv6 reach and accumulated wall pressure.

P3 exclusions:
- exact permanent star values OFF
- achievement reward values OFF
- final shop tuning OFF
- exact final EXP formula OFF
- final boss novelty OFF
- multiplayer progression credit OFF
- exact launch Stage authoring OFF

Any new material P3 design choice must follow analysis -> recommendation -> user approval before structural closure.

---

# Do not yet

- modify/deploy production v0.45 gameplay
- author exact 200 launch Stages
- freeze exact EXP formula
- freeze exact shop cadence/price/value curve
- freeze permanent star values
- freeze achievement reward graph/value
- freeze exact boss mechanics
- freeze multiplayer disconnect timeout/AI/reward details
- freeze multiplayer progression-credit/scaling values
- silently resolve unresolved Lv26/Lv31 or multihit crit semantics
