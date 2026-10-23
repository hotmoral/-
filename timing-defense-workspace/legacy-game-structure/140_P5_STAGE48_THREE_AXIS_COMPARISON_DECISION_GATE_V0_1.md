# Timing Defense — P5 Stage48 Three-Axis Comparison / Decision Gate V0.1

Date: 2026-10-23 KST  
Status: **OBSERVED COMPARISON COMPLETE / USER DECISION REQUIRED BEFORE ADOPTION / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
- `139_P5_STAGE48_SIEGER_PROTECTION_TIME_DIAGNOSTIC_V0_1.md`
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `MONSTER_CAPABILITY_CONTRACT_V1.md`
- `138_SESSION_BOOTSTRAP_COGNITIVE_REVIEW_AMENDMENT_V0_1.md`

Temporary diagnostic evidence only:
- branch `timing-defense-workspace-temp-check`
- armored-vs-real run `39958245978`
- extended standoff run `39958394484`
- no temporary script/fixture has planning or production authority

---

## 0. Plain-language question

Three previously identified Stage48 repair axes were compared before making any design decision:

1. use only existing real BRUTE/SHIELD screening;
2. use a **limited armored-durable body** derived from the earlier proxy idea;
3. move SIEGER's provisional siege/standoff trigger earlier.

The user clarified an important design intent:

> The armored-durable idea was not created only to protect SIEGER. It was also intended as a possible late-stage answer to Mage/Archer ending large-volume encounters too quickly.

Therefore this comparison evaluates both:
- SIEGER role opportunity; and
- late-stage anti-wipe / durable-frontline value.

No armored monster, elite system, standoff value, Stage48 packet, or numerical value is adopted here.

---

## 1. Fixed comparison frame

Held fixed where applicable:

```text
physical spawnX = 0.92
same pre-Stage48 carried wall state
same BALANCED late-segment diagnostic shop snapshot
same class numerics
Tank 0.25 = diagnostic center only, not selected
same SIEGER speed = 0.045 diagnostic anchor
same current SIEGER windup = 0.8 s diagnostic anchor
STAGE_SETTLED lifecycle
no production changes
```

The old repeated proxy stress packet is **not** used as the primary comparison because it repeated a Knight-only test body roughly 23 times and is already known to bury/overpressure Mage.

The limited-armored test instead uses the same old proxy anchor only as an **upper-bound heavy-body diagnostic**, with 2 or 3 bodies in one bounded pulse:

```text
ARMORED_DURABLE_PROXY
HP = 1600
armor multiplier = 0.55
knockResist = 0.65
speed = 0.04
wall = 160
```

These are not candidate production numbers.

---

## 2. Axis A — existing real BRUTE/SHIELD only

Strongest deliberately constructed real-monster handoff boundary tested:

```text
BRUTE + SHIELD + six delayed SHIELD handoffs + SIEGER
```

Representative BALANCED result:

| Class | SIEGER lifetime after spawn | death X | windups | shots |
|---|---:|---:|---:|---:|
| Knight | 2.325 s | 0.8086 | 0 | 0 |
| Rogue | 1.950 s | 0.8322 | 0 | 0 |
| Tank | 11.325 s | 0.5396 | 0 | 0 |
| Archer | 4.575 s | 0.7141 | 0 | 0 |
| Mage | 3.450 s | 0.7647 | 0 | 0 |

No tested class produced a SIEGER windup or shot at the current `x <= 0.38` siege trigger.

Interpretation:
- lowest structural complexity;
- preserves the current ordinary roster cleanly;
- but even an intentionally dense handoff ladder does not create the required SIEGER role opportunity;
- does not address the broader user-identified late-game problem that Mage/Archer can erase ordinary-volume pressure too quickly.

Classification:

```text
REAL_ONLY_AS_STANDALONE_STAGE48_REPAIR = INSUFFICIENT
```

---

## 3. Axis B — limited armored-durable body

### Two-body limited pulse

```text
2 x ARMORED_DURABLE_PROXY
1 x SIEGER
```

Representative BALANCED result:

| Class | SIEGER lifetime | death X | windups | shots |
|---|---:|---:|---:|---:|
| Knight | 2.325 s | 0.8154 | 0 | 0 |
| Rogue | 2.350 s | 0.8142 | 0 | 0 |
| Tank | 5.700 s | 0.7453 | 0 | 0 |
| Archer | **6.825 s** | **0.6129** | 0 | 0 |
| Mage | **7.200 s** | **0.5960** | 0 | 0 |

Compared with the real-only handoff, this materially extends SIEGER survival for Archer and Mage.
It therefore has genuine leverage on the same two late-stage damage identities the user originally wanted to keep from trivializing volume pressure.

However it still produces zero SIEGER windups/shots at the current siege trigger.

### Three-body limited pulse

Adding a third heavy body did **not** monotonically improve the result:

```text
Knight SIEGER lifetime -> 1.2 s
Rogue -> 4.8 s
Tank -> 5.7 s
Archer -> 5.7 s
Mage -> 3.45 s
```

Mage falls back to the same short SIEGER lifetime as the real-only case.

This is important evidence:

```text
MORE_ARMORED_BODIES != AUTOMATICALLY_BETTER_SCREENING
```

Density, alignment and target geometry interact with:
- Mage AoE/chain behavior;
- Knight penetration;
- Archer line penetration;
- Rogue front-clearing/retarget chronology;
- Tank global/control effects.

Therefore the armored idea should not be reduced to raw HP inflation or “add more tanks”.
Its usefulness depends on **limited frequency + formation/geometry + encounter timing**.

Classification:

```text
LIMITED_ARMORED_AXIS = MATERIAL_PROMISE
LIMITED_ARMORED_AXIS_AS_COMPLETE_SIEGER_FIX = NOT YET
REPEATED_OLD_PROXY_PACKET = STILL REJECTED
```

---

## 4. Axis C — SIEGER standoff trigger alone

The strongest real-monster handoff chronology was held fixed while only the provisional SIEGER siege trigger was moved earlier.

Observed boundary:

```text
x=0.38  -> all classes 0 shots
x=0.78  -> Tank 2 shots; Knight/Rogue/Archer/Mage 0 shots
x=0.84  -> Tank 2 shots; Knight/Rogue/Archer/Mage 0 shots
x=0.88  -> Rogue gets 1 windup but 0 shots; Tank 2 shots; others 0 shots
x=0.90  -> Knight/Rogue/Archer/Mage each get only 1 windup and 0 shots; Tank 2 shots
```

At `x=0.90`, SIEGER starts the siege transition after only about:

```text
(0.92 - 0.90) / 0.045 ~= 0.44 s
```

of straight travel.

So even moving the trigger to almost the spawn edge does not create all-class meaningful SIEGER firing under the tested real-only pressure chronology.

This means a standoff-distance-only fix would need to change the encounter grammar toward an almost immediate artillery unit while still failing to solve the separate Mage/Archer volume-erasure problem.

Classification:

```text
STANDOFF_ONLY_AS_PRIMARY_REPAIR = POOR FIT
MODEST_STANDOFF_CHANGE_AS_FUTURE_SECONDARY_AXIS = STILL OPEN
```

No standoff value is selected.

---

## 5. Comparison table

| Axis | SIEGER protection | Mage/Archer anti-wipe leverage | Cross-class risk | Added system complexity | Current verdict |
|---|---|---|---|---|---|
| Real BRUTE/SHIELD only | Low | Low | Low | Low | insufficient standalone |
| Limited armored-durable body | Medium, especially Archer/Mage | **High potential** | Medium; geometry-sensitive | Medium | **most promising primary exploration axis** |
| Earlier SIEGER standoff only | Low for 4/5 classes unless near-entry | None | Medium; changes SIEGER grammar | Low-medium | poor standalone |
| Buff/resistance/skill-like monster mechanics | Unknown | Potentially high | **High coupling** | **High** | defer until simpler axes exhausted |

---

## 6. Why buff/resistance mechanics are deferred, not rejected

The user correctly noted that monster buffs, resistances, or skill-like mechanics could be considered later.

They are not rejected.
They are deferred because they introduce more coupled relationships:

```text
which source grants the buff/resistance
-> duration / stacking / dispel semantics
-> class-specific penetration/AoE/crit/knock interactions
-> telegraph/readability
-> target/frontmost behavior
-> reward/economy value
-> encounter frequency
-> Stage/Tier introduction
-> multiplayer scaling
-> deterministic attribution
```

A new mechanic should be introduced only if simpler content/formation/value axes cannot provide the intended late-game pressure cleanly.

---

## 7. Current recommendation — NOT ADOPTED

Evidence supports this ordering for the next decision:

```text
1. keep real BRUTE/SHIELD as baseline vocabulary;
2. treat LIMITED armored-durable / hardened-frontline concept as the strongest primary exploration candidate;
3. do not use the old repeated proxy packet;
4. do not use standoff distance as the sole repair;
5. keep a modest standoff adjustment available only as a possible secondary partner after the armored formation is understood;
6. defer new buff/resistance mechanics until this simpler combined space is tested.
```

Why:
- it is the only tested axis that directly showed material leverage against both Archer and Mage;
- it also matches the user's original late-stage design purpose;
- but its non-monotonic 2-body vs 3-body behavior proves that formation must be solved before any numerical/roster adoption.

This is a recommendation only.

---

## 8. User decision gate

Before any working direction is adopted, ask the user whether to authorize the following **diagnostic direction only**:

> Use the limited armored-durable concept as the primary Stage48 exploration axis, keep ordinary BRUTE/SHIELD as baseline, and allow only a small secondary SIEGER-standoff sensitivity if needed; do not yet introduce new buff/resistance mechanics.

If approved, the next bounded work should **not** tune a broad HP/armor grid.
It should first test a few formation/chronology layouts using limited heavy bodies and measure:

```text
Mage/Archer packet-clear delay
Knight penetration leakage
Rogue front-clear / retarget leakage
Tank slow-clear/control behavior
SIEGER first windup / first shot
wall loss and STAGE_SETTLED
formation density/alignment sensitivity
```

Only if a promising common all-class layout appears should exact heavy-body numbers, elite status, standoff range, Stage48 count/frequency, or Stage49 integration be proposed.

---

## 9. Authority / non-authority

```text
THREE_AXIS_COMPARISON = COMPLETE
REAL_ONLY_STANDALONE = INSUFFICIENT
LIMITED_ARMORED_PRIMARY_EXPLORATION = RECOMMENDED_NOT_APPROVED
STANDOFF_ONLY = NOT_RECOMMENDED
BUFF_RESISTANCE_MECHANIC = DEFERRED_OPEN_OPTION
NEW_MONSTER_OR_ELITE_ADOPTED = NO
NEW_STAGE48_PACKET_APPROVED = NO
SIEGER_STANDOFF_VALUE_SELECTED = NO
MONSTER_NUMERICS_FROZEN = NO
PRODUCTION_CHANGE = NONE
NEXT = USER_DECISION_GATE
```
