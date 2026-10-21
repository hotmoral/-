# Timing Defense — Monster Provisional Test Envelope V1

Date: 2026-10-22 KST
Status: **PROVISIONAL — NOT BALANCE FROZEN**

## Purpose

Provide executable numbers for the monster-capability sandbox only.

These values exist so server state machines, damage/armor, movement, event delivery, kill/reward attribution and presentation can be tested deterministically before the final approximately 50-stage campaign is authored and calibrated.

**None of the numbers in this document are production balance commitments.**

Final values must be reconsidered after:
- all nine monster capabilities exist,
- required player skill authority exists,
- tier/S-E-X authoring exists,
- 2/3/4-player simulations exist,
- progression/economy pressure can be measured.

---

# 1. Neutral sandbox assumptions

For capability tests:
- no stage HP multiplier unless a specific regression test is intentionally checking legacy Stage 1–3,
- no ordinary-nonboss +10% experiment unless explicitly requested by a legacy regression test,
- one monster's base stats are tested at 1.0 scale,
- wall contact point remains the current normalized wall front,
- all special timers/distances use server-authoritative timestamps/positions,
- rewards are test values only and exist to validate attribution.

This separation prevents a Stage 4/5 recipe from becoming an accidental production contract.

---

# 2. Provisional executable table

| Type | HP | Base speed | Wall damage | Knock resist | Armor | Test reward | Extra provisional capability values |
|---|---:|---:|---:|---:|---:|---:|---|
| GRUNT | 320 | .070 | 90 | .85 | 1.00 | 6 | reference |
| RUNNER | 165 | .135 | 60 | 1.00 | 1.00 | 5 | sustained fast movement |
| BRUTE | 900 | .040 | 180 | .38 | 1.00 | 14 | raw durability anchor |
| SHIELD | 540 | .057 | 120 | .62 | .72 | 10 | flat mitigation test anchor |
| FLYER | 225 | .100 | 70 | .90 | 1.00 | 7 | Y oscillation/geometry anchor |
| CHARGER | 380 | .060 | 110 | .80 | 1.00 | 8 | windup 650 ms; charge speed .210 |
| SPLITTER | 420 | .065 | 100 | .82 | 1.00 | 8 total package budget | children: 2 × HP120, speed .115, wall40 |
| SUPPORTER | 280 | .055 | 70 | .90 | 1.00 | 8 | aura radius .18; ally speed ×1.18; no stack |
| SIEGER | 520 | .045 | — | .55 | 1.00 | 11 | standoff x=.38; windup 800 ms; wall shot 75; repeat 2200 ms |

Notes:
- GRUNT/RUNNER/BRUTE/SHIELD/FLYER numbers are current legacy/reference anchors reused for capability parity tests only.
- new-type values are deliberately simple and spaced apart for debugging readability, not tuned for final difficulty.
- SIEGER uses repeated wall-shot damage instead of ordinary contact damage as its primary sandbox behavior.

---

# 3. Relative design checks

## 3.1 Durability ordering
Approximate raw/effective durability under neutral single-target damage:
- RUNNER: 165
- FLYER: 225
- SUPPORTER: 280
- GRUNT: 320
- CHARGER: 380
- SPLITTER parent only: 420
- SIEGER: 520
- SHIELD effective pre-special-ignore durability: `540 / .72 ≈ 750`
- BRUTE: 900

SPLITTER's total package durability is larger than its parent alone because two child bodies appear after death. That is intentional for the sandbox and must later be calibrated as one authored threat package.

## 3.2 Speed ordering
Normal/base movement:
- BRUTE .040
- SIEGER .045
- SUPPORTER .055
- SHIELD .057
- CHARGER .060 before charge
- SPLITTER .065
- GRUNT .070
- FLYER .100
- SPLITTER child .115
- RUNNER .135
- CHARGER charge .210

This preserves the critical identity split:
- RUNNER = always fast,
- CHARGER = ordinary pace then temporary fastest burst.

## 3.3 Armor vs raw HP
SHIELD remains below BRUTE in effective durability under the provisional anchor:
- SHIELD ≈ 750 effective raw-equivalent HP,
- BRUTE = 900 raw HP.

This helps keep their identities separate during capability tests.

---

# 4. Provisional special-state details

## CHARGER
Test state machine:
`ADVANCE -> WINDUP(650ms) -> CHARGE(.210) -> resolution`

Sandbox trigger:
- enter WINDUP after reaching a deterministic trigger-X supplied by the test harness.
- do not hard-wire the final campaign trigger distance into monster identity yet.

Default deterministic scenario may use trigger x=.62 for visualization/testing.

Interrupt:
- any authoritative positive knockback during WINDUP cancels the current windup in V1 tests.
- after cancellation, harness may apply a provisional 900 ms re-arm delay to prevent immediate same-tick re-entry.

Both trigger position and re-arm delay remain provisional.

## SPLITTER
Parent:
- HP420 / speed .065.

On authoritative death:
- create exactly 2 children,
- each child HP120 / speed .115 / wall40,
- children cannot split,
- child offsets deterministic around parent death position.

Sandbox reward rule:
- total coin package must not exceed test budget 8.
- exact parent/child allocation is implementation detail for the harness and is not production-frozen.

## SUPPORTER
Aura:
- radius .18 normalized world units,
- eligible allies ×1.18 movement speed,
- SUPPORTER does not buff itself,
- same aura never stacks on one target.

Transition requirement:
- materialize target at the exact aura-enter/aura-exit timestamp before changing its speed modifier.

## SIEGER
Movement:
- advance at .045 until standoff condition.

Sandbox standoff:
- x=.38.

Attack loop:
`STOP -> WINDUP 800 ms -> WALL SHOT 75 -> REPEAT after 2200 ms`

Knockback:
- if pushed beyond valid siege range, cancel active windup/repeat schedule and return to positioning/advance.

No final campaign cadence/damage inference should be made from these test numbers.

---

# 5. Required deterministic measurements before any production tuning

The sandbox should automatically expose per archetype:
- time from spawn to first threat event,
- time-to-wall or time-to-first-wall-shot,
- damage required to kill under each damage source,
- displacement per timing tier,
- number/order of state transitions,
- event count generated,
- reward/kill/contribution attribution,
- behavior after reconnect/state reconstruction.

Special metrics:
- CHARGER: interrupt success timing window and charge travel time,
- SPLITTER: parent-death -> child-spawn event ordering and max population delta,
- SUPPORTER: aura enter/exit continuity and no speed-position jump,
- SIEGER: first-shot latency, repeat cadence and knockback-induced reposition.

These measurements are diagnostic. They do not self-authorize balance changes.

---

# 6. Freeze boundary

Frozen here:
- these numbers are approved **only as provisional executable test anchors** for the capability sandbox.

Not frozen:
- every production monster coefficient,
- tier introduction points,
- stage composition/frequency,
- player-count scaling,
- elite/hardened variants,
- reward economy.

Production freeze requires:
`capabilities implemented -> authoring model -> simulation -> classify -> report -> discuss -> explicit decision -> production patch/freeze`.
