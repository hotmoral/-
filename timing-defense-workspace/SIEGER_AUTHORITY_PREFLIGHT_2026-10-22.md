# SIEGER Authority Preflight

Date: 2026-10-22 KST
Status: **IMPLEMENTATION PREFLIGHT / PROVISIONAL NUMBERS / STRUCTURAL CONTRACT RETAINED**

## Purpose
Implement SIEGER as a stage-number-independent authoritative capability without turning it into another direct-contact wall monster.

Frozen structural identity:
- approaches the objective,
- stops at a standoff position,
- telegraphs a shot,
- repeatedly damages the wall from range,
- remains alive after each shot,
- authoritative knockback can force it to reposition before resuming siege,
- no legacy Stage4→10 recipe is enabled.

## Provisional capability-test anchors
- HP 520
- approach speed `.045`
- knock resistance `.55`
- armor `1.00`
- reward 11
- standoff X `.38`
- windup 800 ms
- siege-shot raw wall damage 75
- repeat interval 2200 ms

These are **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN**.

## State machine
Authoritative phases:
`ADVANCE -> WINDUP -> COOLDOWN -> WINDUP -> ...`

`FIRE` is an instantaneous authoritative event, not a persisted movement phase.

### ADVANCE
- moves toward wall using base approach speed,
- SUPPORTER aura may multiply approach X speed,
- exact arrival at `standoffX` is a scheduler due event,
- position is materialized to standoff and phase becomes WINDUP.

### WINDUP
- X speed is exactly zero,
- first shot fires after provisional 800 ms,
- SUPPORTER aura does not shorten windup.

### FIRE
- emits a wall-damage event while keeping SIEGER alive,
- applies existing team DEF policy before base HP subtraction,
- does not change SIEGER HP or reward state,
- immediately enters COOLDOWN.

### COOLDOWN / repeat interpretation
`repeatMs = 2200` is interpreted for the capability sandbox as **shot-to-shot interval**.

Therefore after a shot:
- cooldown duration = `repeatMs - windupMs = 1400 ms`,
- then a fresh 800 ms WINDUP,
- next FIRE occurs 2200 ms after previous FIRE.

This interpretation preserves both existing provisional fields (`windupMs=800`, `repeatMs=2200`) and the phrase “repeat interval”. It is not a production cadence freeze and will be recalibrated with the final campaign.

## Knockback/reposition
SIEGER at standoff is materialized exactly at X `.38` provisional.

If authoritative knockback during WINDUP or COOLDOWN makes `x > standoffX`:
- current siege cycle is cancelled,
- phase -> ADVANCE at the same timestamp,
- next shot schedule is cleared,
- it must physically re-approach standoff,
- upon re-arrival it begins a fresh full WINDUP.

Knockback while already ADVANCING simply increases remaining approach distance.

## SUPPORTER composition
SUPPORTER aura:
- affects ADVANCE X speed only,
- has no effect on WINDUP duration,
- has no effect on repeat interval,
- has no effect on shot damage.

When the SIEGER is stationary, SUPPORTER topology may still change because the SUPPORTER itself moves; v0.44 event-driven aura crossing remains authoritative.

## Wall interaction/event representation
SIEGER should not be removed by the generic direct-contact wall path.

For SIEGER, `wallAt()` is effectively non-contact/infinite while the siege state machine is healthy. Objective damage comes only from the siege-shot scheduler.

A siege shot reuses event type `wall` for existing client/base-damage presentation compatibility, with explicit metadata:
- `monsterType: 'sieger'`
- `siegeShot: true`
- `source: 'siege-shot'`
- `targetId: <sieger id>`

Unlike normal direct-contact `wall` events, the monster remains in authoritative state after this event.

## Team DEF
Use the already validated wall-damage policy:
- aggregate team DEF ranks,
- 2.5 percentage points reduction per rank,
- cap at 60%,
- `incoming = round(shotDamage * (1 - defense))`, minimum 1.

No separate SIEGER-specific DEF exception is introduced in this capability slice.

## Scheduler / chronology
`nextDueAt()` includes:
- standoff arrival while ADVANCING,
- windup completion / FIRE,
- cooldown end / next WINDUP,
- all inherited spawn/AI/passive/Lv6/N3/CHARGER/SUPPORTER events.

Late `advanceTo()` must replay these timestamps chronologically rather than collapsing multiple siege shots at the wake time.

## Reconnect
Persist at least:
- `siegerPhase`
- `siegerPhaseAt`
- `siegerNextAt` / last-shot timing as needed
- X/refAt
- aura source membership inherited from v0.44.

Reconnect must reconstruct identical future standoff/shot times.

## Acceptance requirements
- exact standoff arrival,
- WINDUP stationary,
- first FIRE exactly after windup,
- repeated FIRE shot-to-shot interval exactly 2200 ms provisional,
- SIEGER survives repeated shots,
- team DEF applied once and correctly,
- knockback during WINDUP/COOLDOWN forces ADVANCE/reposition,
- fresh full WINDUP after re-arrival,
- SUPPORTER aura changes approach time only,
- aura does not change shot cadence/damage,
- stage cannot clear while SIEGER remains alive,
- reconnect reproduces same future transitions,
- late advanceTo chronological replay,
- event IDs remain monotonic,
- all prior capability regressions remain PASS.

## Stop conditions
- Do not introduce a fixed gameplay tick.
- Do not let SIEGER fall through GRUNT movement/wall/reward semantics.
- Do not treat provisional shot cadence or damage as production balance freeze.
