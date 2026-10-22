# SUPPORTER Aura Authority Preflight

Date: 2026-10-22 KST
Status: **IMPLEMENTATION PREFLIGHT / PROVISIONAL GEOMETRY & NUMBERS / STRUCTURAL CONTRACT RETAINED**

## Purpose
Implement SUPPORTER V1 without making movement depend on render/update/poll frequency.

Frozen structural contract remains:
- movement-speed aura only,
- no heal/armor/damage/wall-damage/knock-resistance buff,
- SUPPORTER does not buff itself,
- multiple same-type SUPPORTER auras do not stack,
- server authoritative aura membership/effect.

Current provisional anchors remain:
- HP280 / base speed .055 / wall70 / knock .90 / armor1 / reward8
- aura radius .18
- aura movement multiplier 1.18

These are **NOT production balance frozen**.

## Rejected implementation
Do not evaluate aura only on arbitrary snapshots, render frames, client updates or fixed gameplay ticks and then multiply future speed from an old timestamp. That would make position depend on polling frequency and violate the existing authoritative-motion contract.

## Provisional sandbox geometry
For capability validation, `nearby` is interpreted as authoritative normalized **2D Euclidean distance** between SUPPORTER and target positions.

This geometry choice makes FLYER Y motion relevant to aura membership and exercises the strongest existing spatial-authority requirement. It is a capability-test geometry, not a final campaign-radius/tuning freeze.

## Event-driven motion model
Each monster carries persisted aura membership state (source SUPPORTER IDs / active boolean).

While topology and monster phase remain unchanged:
- X motion is integrated at one constant effective speed per segment,
- `effectiveSpeed = currentPhaseBaseSpeed * (auraActive ? auraSpeedMultiplier : 1)`.

At every aura transition:
1. calculate the authoritative transition timestamp,
2. materialize affected position(s) using the **old** movement state through that timestamp,
3. update aura membership/non-stacking source set,
4. continue movement from that exact position/reference timestamp using the new multiplier.

This follows the frozen contract requirement to materialize at enter/leave/death transition time.

## Crossing scheduler
`nextDueAt()` must consider the earliest of:
- existing spawn/AI/passive/Lv6/N3 events,
- wall arrival,
- CHARGER phase transitions,
- SUPPORTER aura boundary crossings.

For static-Y pairs, the next Euclidean radius crossing can be solved analytically from relative linear X motion.

For a FLYER target, Y is deterministic sinusoidal motion. The crossing is found by deterministic bracket + bisection/root refinement over the current motion segment. This is **event root finding**, not fixed-tick movement simulation. The numerical tolerance is an implementation precision bound only and must be far below visible/gameplay timing granularity.

## Topology mutation timestamps
Aura topology must be reconciled immediately when any relevant geometry changes discontinuously:
- SUPPORTER spawn,
- target spawn,
- SPLITTER child spawn,
- knockback of SUPPORTER or target,
- SUPPORTER death,
- SUPPORTER wall removal,
- target death/removal,
- CHARGER phase transition,
- reconnect state restoration.

## Non-stacking semantics
Persist the set of SUPPORTER source IDs currently covering each eligible target.

Effective multiplier is boolean:
- no sources -> 1.00
- one or more sources -> 1.18 provisional

Two or more sources never produce 1.18² or an additive bonus.

A SUPPORTER is excluded from its **own** source ID. Under the literal V1 contract, another SUPPORTER may cover it; overlap still remains non-stacking. This preserves the frozen wording without inventing a blanket SUPPORTER immunity.

## Cross-capability composition
### FLYER
- aura affects X speed only,
- authoritative Y oscillator/epoch remains unchanged,
- Y participates in Euclidean aura distance.

### CHARGER
- multiplier composes with the currently authoritative movement phase:
  - ADVANCE base speed × aura,
  - WINDUP remains zero,
  - CHARGE base speed × aura.
- CHARGER trigger/windup/charge timestamps remain explicit due events.

### SPLITTER
- parent can be covered normally,
- children are inserted at parent-death timestamp,
- child membership is reconciled immediately after spawn,
- child non-recursion remains unchanged.

### SHIELD / BRUTE / RUNNER / GRUNT
- only movement speed changes while covered; armor/HP/knock/damage identities are unchanged.

## Wall prediction
`wallAt()` may predict using the **current movement segment only**. Correctness is preserved because any aura crossing/phase transition that occurs earlier is itself included in `nextDueAt()`; the monster is materialized/rebased there before wall time is reconsidered.

Do not project through unknown future aura topology in one closed-form wall calculation.

## Reconnect
Persisted monster reference position/time plus aura-source membership must reconstruct the same current-segment motion after reconnect. The next crossing is recomputed from authoritative positions/state, not from client history.

## Acceptance requirements
- entry/exit crossing timestamp deterministic across replay,
- position continuous across multiplier changes,
- no self-buff,
- overlap non-stacking,
- supporter removal drops affected speed at exact event timestamp,
- FLYER Y can cause aura enter/leave without client authority,
- CHARGER ADVANCE/CHARGE composition correct; WINDUP stays zero,
- SPLITTER child can inherit immediate membership based on spawn position,
- wallAt/nextDueAt ordering remains chronological,
- reconnect reconstructs identical future positions/crossings,
- prior v0.43/v0.42/v0.41/v0.40/v0.39 regression remains PASS.

## Stop condition
If implementation requires a fixed simulation tick to remain correct, stop and classify rather than silently adopting that approximation.
