# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — SYSTEM DEPENDENCY / RUN-STATE PRE-SYNTHETIC-TIER

Completed chain:

```text
Master Campaign Spine
 -> Layer-0 PASS
 -> encounter envelope PASS
 -> role-expression calibration
 -> Critical 10 PASS_WITH_WATCHES
 -> All-20 historical PASS_WITH_WATCHES / 540 OF 540
 -> high-mastery trace boundary clarified
 -> provisional streak-aware SKILLED_V2_CENTRAL design prior
 -> corrected central all-20 probe
 -> localized E08/E20 SPLITTER refinements
 -> central 540 OF 540 PASS
 -> historical regression 540 OF 540 PASS
 -> system dependency / calibration-order review
 -> user-approval decision gate governance
```

Current execution authority:
- `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `legacy-game-structure/71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `legacy-game-structure/data/system_dependency_calibration_order_v0_1.yaml`

---

# Decision governance — mandatory from this point

For unresolved game/product decisions, do not silently choose and close a rule.

Required sequence:

```text
live canonical inspection
 -> dependency / interaction analysis
 -> calculation or simulation where useful
 -> compare material alternatives
 -> assistant recommendation + reasons + risks
 -> USER DECISION GATE
 -> only then record accepted/frozen direction
```

Diagnostic work and reversible candidate simulations may proceed without asking permission for every step, but a candidate passing a simulation does not itself authorize a design decision.

Approval scope is narrow: approving one rule does not freeze related numbers or adjacent systems unless they were explicitly included in the decision packet.

---

# Why the next step changed

Do not jump directly from all-20 encounter validation into a 10-stage balance simulator.

The synthetic Tier needs explicit semantics for state persistence and power stacking first.
Otherwise the simulator would silently invent rules for base HP, charge, shop, permanent modifiers or failure boundaries.

The new order is:

```text
P1 Run-State Lifecycle Contract
      +
P2 Modifier Pipeline / Power Attribution Contract
      ↓
P3 10-Stage Persistent Run Kernel
      ↓
P4 Full Player-Power Spine Candidate
      ↓
P5 Coin/Shop Candidate
      ↓
P6 Joint Run-Power Convergence
      ↓
... later full Tier / soft wall / stars / achievements / account / multiplayer / freeze
```

---

# EXACT NEXT BOUNDARY

## P1 — RUN_STATE_LIFECYCLE_CONTRACT

First perform analysis and prepare decision packets; **do not silently close unresolved material choices**.

For every state field determine or propose:
- reset boundary;
- persistence boundary;
- derived vs stored;
- authoritative owner.

Material topics requiring recommendation before closure:
1. Tier attempt start/end semantics.
2. base/wall HP persistence and any recovery between Stages/shop.
3. combo persistence — current direction: Stage/shop/target-wait does not break combo.
4. charge/heavy state persistence across Stage/shop.
5. level/EXP persistence — run-local, starts from Lv1.
6. run coin persistence — run-local, resets at attempt start.
7. shop rank persistence — run-local.
8. Stage clear/fail transition semantics.
9. reconnect restoration boundary.
10. deterministic RNG/replay state ownership.

P1 workflow:

```text
inspect accepted rules + legacy/runtime evidence
 -> map interactions with EXP/skill/shop/stars/achievements/Tank/multiplayer/reconnect
 -> identify tightly coupled decision groups
 -> calculate/simulate candidate consequences where useful
 -> present recommendation and alternatives to user
 -> obtain approval
 -> author structural contract
```

No numerical balancing is required in P1 unless a bounded numeric example is needed only to compare semantics.

## P2 — MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION

Likewise analyze/propose first; user approval is required before material stacking semantics are structurally frozen.

Define semantics before values for:
- base class/weapon/objective stats;
- star account modifiers;
- achievement account/class modifiers;
- run-local shop modifiers;
- level/skill modifiers;
- timing/Heavy/P×P/combo/crit modifiers;
- monster mitigation/state interaction;
- wall defense/shields.

Required outputs after approval:
- `statId`/scope/operation/value/stackPolicy/source/version schema;
- explicit operation ordering;
- no implicit multiplicative stacking;
- attribution/debug contract for final damage/control/wall events.

P1 and P2 may be analyzed together where dependencies overlap, but P3 is blocked until their material decisions are user-approved and coherent.

---

# P3 preview — do not implement before P1/P2 closure

10-stage persistent run kernel purpose:
- prove multi-stage state continuity cheaply;
- validate Stage transitions and failure semantics;
- cross the Lv6 reach window;
- create a stable base for later EXP/shop integration.

Initial exclusions:
- permanent star values OFF;
- achievement rewards OFF;
- final shop tuning OFF;
- final boss novelty OFF;
- multiplayer progression credit OFF;
- exact launch Stage authoring OFF.

This is a state/persistence slice, not a final difficulty test.

---

# Important feedback gates to preserve later

## EXP/Skill ↔ Shop
Shop power changes kill speed, timing-event count and therefore EXP opportunity.
A provisional EXP curve must be rechecked after shop integration.

## Permanent power ↔ Skill reach
Stars/achievements can increase entry power, shorten combat and reduce EXP-producing events.
Lv milestones must be rechecked for P0/P1/P2/P3 meta states.

## Stars ↔ Snowball
Star rewards must be sized from observed soft-wall movement, not arbitrary stat increments.

## Achievements ↔ Class viability
Exact sourceClass→targetClass reward edges must wait for the measured class soft-wall map and stat sensitivity matrix.

## Multiplayer ↔ Progression
Multiplayer combat scaling is validated first; star/achievement credit rules are connected later and audited for carry/exploit routes.

---

# Do not yet

- modify/deploy production v0.45 gameplay
- author exact 200 launch Stages
- freeze final Tier count
- freeze exact EXP formula
- freeze exact shop cadence/price/value curve
- freeze permanent star values
- freeze achievement reward graph/value
- freeze exact boss mechanics
- freeze multiplayer progression-credit/scaling values
- infer production clear rate from the 300-row all-20 structural probes
- treat the 70/20/10 central prior as empirical population telemetry
- convert a simulation candidate into an accepted decision without user approval

Governance:

```text
freeze meaning
 -> isolate one power loop
 -> measure
 -> add next coupled system
 -> re-check upstream invariants
 -> author exact content late
 -> full-system stress
 -> explicit numerical freeze
 -> production implementation
```

Decision gate overlay:

```text
ANALYZE / CALCULATE / PROPOSE
             ↓
        USER APPROVAL
             ↓
AUTHOR / VALIDATE / RECORD
```
