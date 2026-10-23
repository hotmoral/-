# Timing Defense — P4-D2 Tank Barrier Fidelity Correction V0.1

Date: 2026-10-23 KST  
Status: **METHODOLOGY CORRECTION / TANK TEMPORAL MISS-SEVERITY VALUES PARTIALLY SUPERSEDED / NO GAMEPLAY CHANGE / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority:
- `90_P4D1_LV31_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md` — Tank T-B shared barrier family semantics
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md`
- `100_P4D2_STAGE48_49_CADENCE_CORRECTED_DIRECTIONAL_FEEDBACK_V0_1.md`
- `102_P4D2_DURABLE_TEMPORAL_PRESSURE_DIRECTIONAL_PROBE_V0_1.md`

Correction runner:
- `../../tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_3.py`

---

# 0. Finding

The existing Stage46 temporal kernel and the v0.2 cadence-aware wrapper contain a Tank shield-family fidelity defect.

Approved/proposed Tank T-B semantics state:

```text
one shared non-additive barrier family
active Lv31 Absolute Barrier must not be overwritten/downgraded by weaker Lv16 Perfect Guard
a later weaker Lv16 guard cannot reduce an active stronger Lv31 barrier
repeated Lv31 barriers refresh rather than stack
```

The inherited temporal implementation instead did:

```text
Lv31 final -> shield = 250 / 6s
next ordinary PERFECT -> shield = 80 / 3s
```

Therefore the simulator could downgrade a still-active Lv31 barrier from 250 to 80.

Classification:

`TANK_BARRIER_FAMILY_FIDELITY_DEFECT = CONFIRMED`

This is a simulation-method defect, not a request to buff Tank gameplay.

---

# 1. Correction semantics

For P4-D2 temporal diagnostics, v0.3 tracks barrier source family.

Diagnostic rule:

```text
Lv31 final:
  shield = 250 candidate
  expiry = now + 6s candidate
  source = LV31

ordinary Lv16 Perfect Guard:
  if no active Lv31 barrier remains:
      shield = 80
      expiry = now + 3s
      source = LV16
  else:
      do not downgrade the active Lv31 barrier
```

When the active Lv31 barrier is depleted or expired, later Lv16 guards may create/refresh the Lv16 barrier normally.

This is a fidelity implementation of the existing structural rule, not a new balance choice.

Exact production shield implementation remains deferred.

---

# 2. Effect on prior Tank temporal numbers

A bounded local reconstruction was rerun with only the barrier non-downgrade correction changed.

The correction does **not** weaken Tank. It increases the safety margin, as expected.

## Distributed durable pressure

Two consecutive missed final windows:

```text
pre-correction Tank wall = 1584
barrier-corrected wall   = 1924
```

## Strong durable + role pulse

One missed final:

```text
pre-correction = 1301
corrected      = 1661
```

Two consecutive missed finals:

```text
pre-correction = 1073
corrected      = 1497
```

## Durable + SUPPORTER/SIEGER pulse

One missed final:

```text
pre-correction = 1226
corrected      = 1661
```

Two consecutive missed finals:

```text
pre-correction = 1092
corrected      = 1480
```

These corrected values remain **directional** until the committed v0.3 runner is executed in a repository checkout.

---

# 3. What remains valid from documents 100 / 102

The correction does **not** invalidate the following structural conclusions:

- Tank survives durable pressure primarily by buying time through knockback/slow/barrier rather than deleting durable bodies;
- removing Tank knockback causes severe deterioration and can cause burial;
- therefore Tank control is a real solution and must not be hard-countered by extreme knock resistance;
- distributed durable pressure remains a strong Mage pressure lever;
- clustered durable pressure restores Mage value;
- Rogue execution and Archer armor-ignore identities remain preserved;
- naive universal HP/spawn inflation remains the wrong first repair layer.

The correction **does** supersede earlier Tank-specific miss-severity magnitudes that assumed Lv16 could downgrade an active Lv31 barrier.

---

# 4. Design consequence

Tank is even more clearly a **time-budget class** than the pre-correction probe suggested.

Therefore late authoring should not try to make Tank fair by:

```text
reducing Absolute Barrier power
or
raising durable knock resistance until push stops working
```

Instead, pressure Tank by spending the time it buys:

- staggered second/third pulses;
- multiple readable SIEGER shots across a barrier gap;
- CHARGER windows arriving after the initial reset;
- durable bodies that remain alive and force repeated control cycles;
- role threats that are spatially separated from the first shockwave's ideal cleanup path.

One isolated missed final does not need to be equally dangerous for every class.
Tank may legitimately have a larger mistake budget because protection/control is its class identity.

The requirement remains:

> Tank cannot ignore P×P indefinitely, and sustained failure must eventually exhaust its time budget.

---

# 5. v0.2 replay status change

The previously expected v0.2 replay hash is still useful only for reproducing the **pre-barrier-correction** cadence/no-target lane.

It must no longer be promoted as the final Tank class-fairness temporal authority.

Future class-fairness replay authority must use:

`run_p4d2_stage48_49_dynamic_grammar_probe_v0_3.py`

which preserves:
- no-target non-banking;
- Rogue 78ms recovery sensitivity;
- timestamp-to-grammar Heavy mapping;
- Tank shared barrier non-downgrade semantics.

Exact v0.3 repository-checkout execution/hash is still pending.

---

# 6. Impact on durable Stage48/49 authoring

The durable pressure direction remains supported, but Stage49 authoring now needs a more deliberate Tank pressure mechanism.

Current useful split:

```text
Stage48-like:
  lighter durable pressure
  intermittent role second pulse
  strong Lv31 power revelation still visible

Stage49-like:
  durable backlog persists
  second/third role pulses consume Tank's bought time
  distributed geometry pressures Mage
  cluster windows remain available as Mage recovery opportunities
```

Do not force identical one-miss/two-miss wall-loss targets across classes.

---

# 7. Exact next boundary

1. execute v0.3 cadence/no-bank/barrier-corrected replay in a repository checkout;
2. treat v0.2 Tank miss-severity numbers as historical pre-correction evidence only;
3. refine Stage49 role-pulse timing around Tank's true barrier uptime rather than around the downgraded simulator behavior;
4. preserve Mage distributed-vs-cluster durable asymmetry;
5. continue Archer chronology investigation separately;
6. reassess whether P4-D2 can close provisionally with explicit watches.

No production change is authorized.