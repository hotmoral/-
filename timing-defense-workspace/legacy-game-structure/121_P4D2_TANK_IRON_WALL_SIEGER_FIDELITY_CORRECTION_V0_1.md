# Timing Defense — P4-D2 Tank Iron Wall / SIEGER Fidelity Correction V0.1

Date: 2026-10-23 KST  
Status: **CONCRETE FIDELITY DEFECT CONFIRMED / TARGETED REVALIDATION PASS DIRECTIONALLY / EXACT COMMITTED V0.6 REPLAY PENDING / P4 STRUCTURAL CLOSURE PRESERVED**

Authority:
- `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- prior exact admission `109_P4D2_EXACT_V05_AND_STAGE49_V02_REPLAY_ADMISSION_V0_1.md`

New runners:
- `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_6.py`
- `tools/run_p4d2_stage49_full_rotation_probe_v0_3.py`

---

# 0. Trigger

P5 generic DEF integration exposed a concrete cross-stage mismatch.

Recovered Tank Lv11 contract:

```text
Iron Wall: shared wall incoming damage x0.90
multiple Tanks do not stack
```

P2 incoming-wall order also treats this as an explicit unique class/team defensive effect after generic wall DR.

Historical Stage46/P4 kernel behavior:
- ordinary monster wall contact applied Tank `x0.90`;
- SIEGER wall-shot `75` did **not** apply Tank `x0.90`.

No authority defines a SIEGER exception.
Therefore the SIEGER path was a fidelity defect.

---

# 1. Minimal correction

v0.6 changes only the Tank SIEGER wall-shot path:

```text
old diagnostic:
SIEGER incoming = 75

corrected:
SIEGER incoming = 75 * 0.90 for Tank
```

It preserves:
- NO_TARGET opportunities do not bank;
- Rogue recovered -78ms recovery sensitivity;
- Tank Lv31 barrier may not be downgraded by Lv16 guard;
- same Stage49 fixture/grammar;
- same Lv31 provisional centers.

Other classes receive no combat-semantic change from this correction.

---

# 2. Independent reconstruction validation

Before applying the new correction, a focused Tank-only independent reconstruction reproduced the admitted v0.5 Stage49 Tank baselines:

```text
all success:
endWall 2000 / endActive 11

one-miss range:
2000..2000

two-consecutive-miss range:
1725..2000

all finals missed:
burial 34.575s

first burial consecutive misses by grammar:
LINE 6
CLUSTER 6
FRONTLINE 5
DURABLE 5
TIME_BUDGET_SIEGER 4
```

These match the prior exact-admission evidence, supporting the focused reconstruction as a valid directional delta probe.

---

# 3. Corrected directional Tank result

With Iron Wall applied to SIEGER shots:

```text
all success:
endWall 2000 / endActive 11

one-miss range:
2000..2000

two-consecutive-miss range:
1732.5..2000

all finals missed:
burial 34.700s

first burial consecutive misses by grammar:
LINE 6
CLUSTER 6
FRONTLINE 5
DURABLE 5
TIME_BUDGET_SIEGER 5
```

Primary change:

```text
TIME_BUDGET_SIEGER first burial: 4 misses -> 5 misses
```

This is directionally coherent with Tank's approved larger time-budget identity.

---

# 4. Structural impact review

The correction does **not** reverse the key P4 conclusions:

```text
Tank all-success survives = YES
isolated mistake recoverable = YES
repeated failure consumes time budget = YES
all finals missed still buries within 60s = YES
identical class mistake budgets required = NO
```

Therefore:

```text
P4_STRUCTURAL_CLOSURE_REOPEN_REQUIRED = NO
TARGETED_TANK_NUMERICAL_EVIDENCE_SUPERSEDED = YES where SIEGER shots reached wall
```

Do not continue citing v0.5/v0.2 Tank TIME_BUDGET_SIEGER `4` as current fidelity truth.

---

# 5. Exact replay boundary

The independent reconstruction is strong directional evidence because it first reproduced admitted v0.5 Tank outputs exactly.

However the newly committed:
- v0.6 dynamic runner;
- Stage49 v0.3 wrapper

still require live-blob/checkout exact execution before receiving the same exact replay authority as v0.5/v0.2.

Until then:

```text
v0.5/v0.2 = historical exact evidence
v0.6/v0.3 Tank correction = current directional fidelity authority
```

P5 shop/DEF work must use the corrected Iron Wall semantic regardless.

---

# 6. P5 consequence

Generic shop DEF must enter before Tank Iron Wall and before wall shield absorption:

```text
raw wall event
-> monster capability modifier
-> generic shop wall DR
-> Tank Iron Wall x0.90
-> final incoming before shield
-> shield
-> BaseHP
```

This correction must be present in any P5 fixed-rank shop+combat probe.

No production implementation is authorized.