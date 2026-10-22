# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — P2 MODIFIER PIPELINE / POWER ATTRIBUTION

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
```

Current execution authority:
- `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/data/system_dependency_calibration_order_v0_1.yaml`

---

# P1 CLOSED STRUCTURALLY

User-approved P1 directions:
- Base HP / Base Max HP persist across Stage/shop within one Tier attempt.
- No automatic Stage/shop heal.
- Base HP 0 ends the Tier attempt.
- Retry starts a fresh Stage1 Tier attempt; run-local state resets and permanent account state remains.
- combo persists across Stage/shop downtime under the existing combo contract.
- charge persists across Stage/shop.
- an in-progress Heavy X->Y resolves before Stage transition finalizes.
- disconnect != leave.
- reconnect restores the same authoritative player/run state without implicit reset/heal.
- a transient multiplayer disconnect does not immediately rescale enemy pressure downward.
- a transient disconnect alone does not immediately invalidate rewards/stars/achievement eligibility.

Still open for later P10/P16 analysis:
- reconnect grace duration;
- disconnected-player AI takeover/substitution;
- long-disconnect/abandonment threshold;
- rescaling after confirmed abandonment;
- long-disconnect reward/achievement credit;
- host migration exact policy;
- all-player disconnect behavior;
- durable persistence/storage implementation.

These deferred items do not block P2/P3.

---

# Decision governance — mandatory

For unresolved product/game decisions:

```text
live canonical inspection
 -> dependency / interaction analysis
 -> calculation or simulation where useful
 -> compare real alternatives
 -> assistant recommendation + risks/reversibility
 -> USER DECISION GATE
 -> only then record accepted/frozen direction
```

Diagnostic work may proceed without micro-approval, but passing a test does not authorize a design decision.

---

# EXACT NEXT BOUNDARY

## P2 — MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION

Do not begin by choosing numerical bonuses.
First determine the semantics needed so later stars, achievements, shop, skills, combo, crit and defenses cannot stack implicitly or inconsistently.

Required analysis/decision topics:
1. stat scope taxonomy — ACCOUNT / CLASS / RUN / TEMPORARY / TARGET-STATE.
2. canonical stat IDs and base-vs-derived separation.
3. additive vs multiplicative modifier semantics.
4. ordering between:
   - base class/weapon/objective stats
   - star permanent modifiers
   - achievement account/class modifiers
   - run-local shop modifiers
   - level/skill modifiers
   - timing judgment / Heavy / P×P
   - combo
   - crit
   - monster mitigation/armor/state
   - wall defense/shields
5. cap/clamp ownership.
6. duplicate/stack policy by source family.
7. damage/control/wall attribution so simulation can explain *why* an outcome changed.
8. snapshot vs dynamic evaluation for permanent/run modifiers.

Required output after user approval:
- modifier schema: `statId / scope / operation / value / stackPolicy / source / version`;
- authoritative operation order;
- explicit cap/clamp semantics;
- attribution/debug event contract;
- no accidental multiplicative stacking.

P3 remains blocked until P2 material semantics are approved and coherent.

---

# P3 preview — after P2 closure

10-stage persistent run kernel will validate state continuity using the approved P1/P2 contracts.
It is a state/persistence integration slice, not a final difficulty test.

Initial exclusions:
- exact permanent star values OFF
- achievement reward values OFF
- final shop tuning OFF
- final boss novelty OFF
- multiplayer progression credit OFF
- exact launch Stage authoring OFF

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
- convert a candidate into an accepted decision without user approval
