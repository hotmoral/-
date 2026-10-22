# Timing Defense — User Approval Decision Gate Governance V0.1

Date: 2026-10-22 KST  
Status: **ACTIVE GOVERNANCE / USER-CONFIRMED**

Depends on:
- `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `../NEXT_WORK.md`

---

# 0. User-confirmed operating rule

For Timing Defense, when a next-step item requires a design, structural, numerical, progression, economy, balance, content, or production decision, the assistant must **not silently infer, choose, and close the decision**.

Required operating sequence:

```text
inspect live canonical state
 -> identify the actual decision question
 -> analyze upstream/downstream dependencies
 -> calculate/simulate where useful
 -> compare alternatives
 -> state the assistant's recommendation and reasons
 -> identify risks / side effects / reversibility
 -> ask for user approval or selection
 -> only after approval: record as accepted direction / freeze at the appropriate level
```

The user is the decision authority for unresolved product/game-design choices.

This rule applies even when one option appears technically convenient.
Convenience alone does not authorize a design decision.

---

# 1. What may proceed without a separate approval gate

The assistant may independently perform **diagnostic and preparatory work** that does not close an unresolved game/product decision.

Examples:
- read and reconcile canonical documents;
- inspect legacy/live source;
- calculate derived quantities from already accepted rules;
- run simulations against already accepted candidate inputs;
- identify contradictions, defects, coupling, or missing state;
- generate comparison tables;
- derive sensitivity ranges;
- validate deterministic behavior;
- patch an unambiguous implementation defect where the intended contract is already frozen and the patch does not change game semantics;
- document evidence and keep a decision marked `OPEN_DECISION`, `PROPOSED`, `CANDIDATE`, or equivalent.

Diagnostic work should continue far enough to make the eventual user decision informed rather than superficial.

---

# 2. What requires explicit user approval before closure

Explicit approval is required before converting an unresolved item into accepted/frozen direction when it changes any of the following.

## 2.1 Structural semantics
Examples:
- what persists/resets across Stage/shop/run/account;
- Tier unlock rules;
- fail/retry semantics;
- solo/team progression ownership;
- boss/checkpoint structure;
- modifier operation/stacking semantics;
- star/achievement eligibility rules.

## 2.2 Numerical balance or economy
Examples:
- EXP formula;
- shop prices/cadence/effect values;
- permanent stat values;
- achievement reward magnitudes;
- production monster HP/speed/damage;
- clear-rate target refinements;
- exact caps/scalars.

## 2.3 Content/progression authoring choices
Examples:
- exact Stage schedule;
- exact boss mechanics;
- sourceClass -> targetClass achievement graph;
- final Tier count;
- new monster placement;
- mandatory mechanic introduction timing.

## 2.4 Production-impacting changes
Examples:
- live gameplay behavior;
- production data migration;
- live balance coefficients;
- production networking/progression behavior.

---

# 3. Required decision proposal packet

Before asking the user to decide, the assistant should provide a compact but rigorous decision packet.

Minimum fields:

1. **Decision question** — exactly what must be decided now.
2. **Why now** — which downstream work is blocked or distorted without it.
3. **Known constraints** — already frozen/user-confirmed rules that candidates must preserve.
4. **Dependency analysis** — systems affected upstream/downstream.
5. **Evidence/calculation** — simulation, source behavior, sensitivity or quantitative reasoning where applicable.
6. **Options** — normally 2–4 materially distinct choices; avoid fake alternatives.
7. **Recommendation** — assistant's preferred option.
8. **Reason for recommendation** — expected benefit, complexity, consistency, player experience, rework cost.
9. **Risks / failure modes** — including cross-system effects.
10. **Reversibility** — cheap/medium/expensive to change later.
11. **What remains open** — approval should not accidentally freeze unrelated numbers or systems.
12. **Requested user action** — approve recommendation, choose another option, or request further analysis.

If one option is clearly dominated, explain why rather than presenting it as equal.

---

# 4. Decision-state vocabulary

Use explicit states to prevent accidental closure.

- `OBSERVED` — factual evidence only.
- `DERIVED` — calculation from accepted inputs; no new design choice.
- `CANDIDATE` — plausible working input for simulation.
- `PROPOSED` — recommended choice awaiting user approval.
- `USER_APPROVED_DIRECTION` — user accepted the direction; exact values may still be open.
- `STRUCTURAL_FROZEN` — semantics/contract fixed.
- `NUMERIC_FROZEN` — exact balance/economy number explicitly accepted.
- `PRODUCTION_AUTHORIZED` — live implementation/deployment explicitly authorized.
- `OPEN_DECISION` — unresolved and must not be silently assumed.

A simulation candidate must not be promoted to `USER_APPROVED_DIRECTION` merely because it passes a test.

---

# 5. Approval scope must be narrow

User approval applies only to the decision actually presented.

Example:

```text
User approves:
"Base HP persists across Stages with no automatic full heal."
```

This does **not** automatically approve:
- exact starting Base HP;
- shop healing availability;
- heal amount;
- Tank wall-defense coefficient;
- star HP rewards;
- multiplayer wall scaling.

Those remain separate decisions unless explicitly included in the proposal.

---

# 6. Do not use approval gates to stop useful analysis

The approval requirement is not a reason to ask the user a question before doing obvious preparatory analysis.

Bad workflow:

```text
Need to decide Base HP persistence
 -> immediately ask user without analysis
```

Required workflow:

```text
Need to decide Base HP persistence
 -> inspect current rules/legacy behavior
 -> map interaction with Tank, shop, stars, fail curve, reconnect
 -> compare candidate policies
 -> simulate or estimate consequences if useful
 -> recommend one
 -> ask user to approve/select
```

The goal is **user-authorized decisions informed by deep analysis**, not constant interruption.

---

# 7. Conflict handling

If new evidence conflicts with a user-approved direction:

1. do not silently override it;
2. mark the conflict;
3. quantify/materialize the consequence;
4. present whether the prior decision should remain, be amended, or be reopened;
5. obtain user approval before changing the accepted direction.

A prior approved rule can therefore be reopened, but only transparently.

---

# 8. Interaction with P1–P18 dependency plan

The dependency order in document 70 remains active.

However, each phase now has two internal substeps where decisions are required:

```text
ANALYZE / CALCULATE / PROPOSE
             ↓
        USER DECISION GATE
             ↓
AUTHOR / VALIDATE / RECORD
```

For P1 and P2 specifically:
- do not automatically close every unresolved lifecycle/modifier rule;
- first produce decision packets for the material choices;
- low-level derived/schema consequences may then be authored from the approved choices.

P3 remains blocked until the P1/P2 material decisions required by its simulator are user-approved and structurally coherent.

---

# 9. Efficiency rule

To avoid excessive micro-approval overhead, related decisions may be grouped **only when their dependencies are tightly coupled and the tradeoff can be evaluated as one coherent package**.

Do not group unrelated decisions merely to reduce conversation turns.

Preferred grouping example:
- Base HP persistence + inter-Stage recovery + fail boundary, because they jointly define run attrition.

Poor grouping example:
- Base HP persistence + final boss weakness mechanic + achievement title cosmetics.

---

# 10. Current next application

The first use of this governance is P1 `RUN_STATE_LIFECYCLE_CONTRACT`.

The assistant should first analyze and prepare recommendations for material P1 decisions such as:
- Base HP persistence/recovery;
- charge/heavy persistence across Stage/shop;
- Tier-attempt fail/end/retry semantics;
- reconnect restoration boundary where not already frozen.

The assistant must present the recommendation before recording those choices as accepted/frozen.

No production gameplay change is authorized by this governance document.