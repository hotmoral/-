# Timing Defense — Run-State Lifecycle Approved Contract V0.1

Date: 2026-10-22 KST  
Status: **USER_APPROVED_DIRECTION / STRUCTURAL CONTRACT / NUMERICAL VALUES OPEN**

Depends on:
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `01_META_PROGRESSION.md`
- `03_STAGE_STRUCTURE_50.md`
- `../../DESIGN_DECISIONS.md`

---

# 0. Scope

This document records the P1 run-state lifecycle directions explicitly approved by the user.
It does not freeze numerical balance values, shop healing values, reconnect timeout duration, disconnected-player AI substitution policy, long-disconnect reward policy, host migration details, or production persistence infrastructure.

---

# 1. Tier-attempt attrition contract — USER APPROVED

## 1.1 Base HP persistence
- Base HP and Base Max HP persist across Stage transitions and shop/intermission within the same Tier attempt.
- Stage/shop transition itself does not automatically heal or refill Base HP.
- This does not forbid future explicit healing sources such as shop healing, checkpoint rewards, class effects or other authored mechanics; those remain separate decisions.

## 1.2 Failure boundary
- Base HP reaching zero ends the current Tier attempt.
- The failed Stage determines the attempt star result under the already-approved star bands.

## 1.3 Retry boundary
- Retrying after Tier-attempt failure starts a new Tier attempt from Stage 1.
- Run-local state is reset for the new attempt.
- Permanent account progression remains.

Current run-local reset set includes:
- Stage -> 1
- level -> 1
- EXP -> 0
- run coin -> 0
- run shop ranks -> 0
- combo -> 0
- charge -> 0
- Base HP -> full starting value for the new attempt

Exact starting Base HP value remains numerically open.

---

# 2. Combat continuity across Stage/shop — USER APPROVED

## 2.1 Combo
Existing rule remains authoritative:
- Stage/shop/target-wait downtime does not break combo.
- GOOD/NORMAL/MISS timing judgment breaks combo according to the existing combo contract.

## 2.2 Charge
- Charge persists across Stage transitions and shop/intermission within the same Tier attempt.
- Stage/shop transition does not silently reset charge.

## 2.3 In-progress Heavy X->Y
- An already-started valid timing turn is allowed to resolve fully.
- A Heavy X->Y sequence that has started is not cut in half by Stage completion.
- Stage-clear transition is finalized after the in-progress timing turn has resolved.
- The system should not enter shop/intermission while carrying an unresolved half-Heavy transient state.

---

# 3. Reconnect continuity — USER APPROVED

## 3.1 Core reconnect identity
- Network disconnect by itself is not a Tier-attempt failure.
- Disconnect and explicit leave/abandon are different semantic events.
- A temporarily disconnected player keeps the authoritative player slot and run identity while that reconnectable attempt still exists.
- Reconnect restores the same player into the same authoritative Tier attempt.
- Reconnect itself must not reset gameplay state or act as an implicit heal/reset.

State that must be restorable from authoritative run state includes at least:
- current Stage
- Base HP / Base Max HP
- level / EXP
- run coin
- run shop ranks
- combo
- charge
- deterministic RNG/replay state where required
- player/session/run identity
- input sequence/replay guards required for authoritative duplicate/stale-action rejection

## 3.2 Multiplayer transient-disconnect structural rules
The user approved the following bounded multiplayer semantics:

1. **Disconnect != leave.**
   - A transient network loss does not immediately remove the player from the run or convert the event into voluntary abandonment.
   - Slot/state remain reserved for reconnect under the future grace/persistence policy.

2. **Same-player / same-run restoration.**
   - A reconnecting player returns to their existing run state rather than receiving a new player state.
   - Level, EXP, coin, shop ranks, combo, charge and other run-local progression are not regenerated or reset merely because the connection dropped.

3. **No immediate difficulty rescaling on transient disconnect.**
   - A temporary disconnect does not itself authorize an immediate 4P->3P, 3P->2P, etc. enemy-pressure reduction.
   - This prevents disconnect from becoming a difficulty-manipulation exploit and avoids mid-encounter authored-pressure discontinuity.
   - The eventual policy for very long disconnect/abandonment remains open.

4. **No immediate reward invalidation on transient disconnect.**
   - A temporary disconnect alone does not immediately strip star/reward/achievement eligibility.
   - Eligibility after long absence, abandonment, AI substitution or low contribution remains a later multiplayer progression-credit decision.

## 3.3 Explicitly deferred multiplayer reconnect policy
The structural rules above intentionally do **not** decide:
- reconnect grace duration;
- whether/when disconnected players are controlled by AI;
- whether AI inherits the exact disconnected player's class/level/shop state;
- long-disconnect or abandonment thresholds;
- whether enemy scaling changes after confirmed abandonment;
- reward/star/achievement eligibility after long absence or AI takeover;
- host migration details;
- behavior when all humans disconnect simultaneously;
- durable recovery after server/process loss;
- exact storage/retention implementation.

These require later analysis against P10 multiplayer combat scaling and P16 multiplayer progression-credit/exploit rules before user approval.

---

# 4. State reset summary

## Persists across Stage/shop inside one Tier attempt
- Base HP / Base Max HP
- level / EXP
- run coin
- shop ranks
- combo
- charge
- run identity / deterministic state

## Resets/initializes per Stage
- enemy instances
- Stage spawn counters
- Stage/encounter clock
- current target and other transient timing-turn state after valid resolution
- monster capability transient state
- Stage-local counters/statistics unless explicitly accumulated elsewhere

## Resets at new Tier attempt
- all run-local state above

## Persists across Tier attempts
- class Tier records
- bestStars[class][tier]
- star-derived permanent progression
- achievement completion/rewards
- other explicitly account-permanent state

---

# 5. Rationale

The contract preserves a real 50-Stage attrition run while avoiding hidden Stage-boundary power resets.
It also keeps attribution legible:
- wall preservation matters across the run;
- Tank/defense/HP/shop choices can have cumulative value;
- combo and charge are not accidentally coupled to shop cadence;
- retry cannot farm run-local EXP/coin from a failed late Stage without restarting the Tier attempt;
- reconnect does not become an unintended heal/reset exploit;
- transient disconnect cannot be used as an immediate multiplayer difficulty-reduction exploit;
- ordinary network instability does not automatically erase legitimate run progression.

---

# 6. Explicitly still open

The following are not approved by this document:
- exact Base HP value
- any automatic or explicit healing amount/cadence
- shop cadence/price/value
- reconnect grace duration
- disconnected-player AI substitution/takeover timing and behavior
- confirmed-abandonment semantics after the reconnect window
- multiplayer progression/reward credit after long disconnect, abandonment or AI takeover
- multiplayer rescaling after confirmed abandonment
- all-player disconnect behavior
- exact host migration policy
- exact persistent storage technology or retention period
- Stage restart/checkpoint feature, if one is ever proposed

Any such item requires analysis -> proposal -> user approval under document 71.
