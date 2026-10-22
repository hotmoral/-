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
 -> P2 analysis / proposal complete
```

Current execution authority / proposal:
- `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/73_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_PROPOSAL_V0_1.md` — **PROPOSED / NOT APPROVED**
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

# EXACT CURRENT BOUNDARY

## P2 — USER DECISION GATE

Analysis/proposal is complete in:
`legacy-game-structure/73_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_PROPOSAL_V0_1.md`.

Recommended structural package awaiting user approval:
1. **typed hybrid stacking** — ordinary bonuses to the same scalar stat aggregate additively; multiplication is explicit/opt-in.
2. **stat/effect separation** — penetration, splash, shields, armor-ignore, tracking, proc generation, etc. are effect rules rather than fake scalar stats.
3. **outgoing attack pipeline** — resolve action/template -> persistent stats -> action transforms/combo -> crit policy -> hit geometry -> per-target mitigation -> realized effect.
4. **defensive pipeline** — monster raw damage -> generic DR -> explicit unique class/team defense -> shield -> Base HP.
5. **derived stats remain derived** — source modifiers/ranks/unlocks are authoritative; effective stats are recomputed/cache, not independent truth.
6. **deterministic attribution ledger** for simulator/test paths.
7. **delayed rounding** — avoid repeated intermediate rounding; round per realized hit/control application, preserving fixed-budget contracts such as N3.

Important:
- this package is `PROPOSED`, not `USER_APPROVED_DIRECTION`;
- no numeric star/shop/achievement values or caps are frozen;
- unresolved per-skill crit inheritance and later Lv26/Lv31 details remain separate gates.

P3 remains blocked until the material P2 semantics are explicitly approved.

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
- convert P2 proposal into an accepted decision without user approval
