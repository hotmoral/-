# Timing Defense — T1 Wider Exact Authoring Wave A1 Materialization & Static Preflight V0.1

Date: 2026-10-25 KST  
Status: **STATIC PASS / CANDIDATE ONLY / NOT ADOPTED / NO DYNAMIC EXECUTION / NO NUMERICAL FREEZE**

## 1. Scope

Wave A1 only:
```text
Stage1
Stage4
Stage8
```

Context anchor:
```text
Stage5 RUNNER teach = exact preserved representative authority
```

No A2/A3/A4 authoring occurred in this evidence unit.

## 2. Authority

- Wave A bounded plan: `data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`
- Wave A plan/static result: `175_T1_WIDER_EXACT_AUTHORING_WAVE_A_PLAN_AND_STATIC_PREFLIGHT_V0_1.md`
- T1 signature skeleton: `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`
- representative base: `data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`
- Stage49-50 approved baseline remains closed with watches under doc174.

Candidate:
`data/t1_wider_exact_authoring_wave_a1_candidate_v0_1.yaml`

## 3. Candidate recipes

### Stage1 — pure GRUNT baseline teach
```text
E01 / G / F01 / CD01 / C0 / BASELINE
spawns:
0    G y0.46
1600 G y0.46
3200 G y0.46
4800 G y0.46
```

Intent:
- pure timing baseline;
- slow drip;
- no mixed-monster ambiguity;
- readable line-light geometry.

### Stage4 — first clear wave boundary
```text
E01 / G / F01 / CD03 / C0 / BASELINE
spawns:
0    G y0.46
250  G y0.46
500  G y0.46
2800 G y0.46
3050 G y0.46
3300 G y0.46
```

Intent:
- two readable 3-GRUNT wavelets;
- teach group boundary without new monster novelty;
- preserve C0.

### Stage8 — first G+R mixed bridge
```text
E02 / G+R / F01 / CD03 / C1 / RUSH
spawns:
0    G y0.46
250  R y0.46
1700 G y0.46
1950 R y0.46
3400 G y0.46
3650 R y0.46
5100 R y0.46
```

Intent:
- converts already-taught RUNNER into first mixed G+R read;
- repeated GRUNT->RUNNER pair-wave morphology;
- late RUNNER tail preserves RUSH identity;
- no new geometry grammar.

## 4. Exact static evidence

First run:
```text
run 40193721046
head 2b1567572d525f8e93c755cbc89c3d7e4a9c84da
conclusion = failure
```

Classification:
```text
VALIDATOR_MISUSE / NO CANDIDATE CONTENT FAILURE
```

Two validator issues:
1. Wave plan stores `signature: E01 / G`; validator incorrectly expected direct `archetype` inside the plan record.
2. legacy transition `static_recipe_gate` intentionally enforces the old representative-slice fixed stage set, so it cannot validate an expanded Stage1/4/8 set.

Failure artifact showed candidate facts already inside guard:
```text
Stage1 max4=3
Stage4 max4=6
Stage8 max4=6
Stage5 preserved=true
existing representative stages preserved=true
```

Minimal correction:
- derive archetype from plan `signature`;
- use old runner static gate only on the unchanged representative base;
- validate newly added A1 stages with the dedicated A1 expansion gate.

Candidate data was not changed.

Final exact rerun:
```text
run      40193818274
artifact 12599510840
head     44793b082481df5bbff64eea383ed3240166dee4
artifact sha256 231e3b97d32baa158eff069f4897ae889cb280e5aa0aa591d1a11cd7040b141a
status   PASS
errors   []
warnings []
```

Exact identities:
```text
base recipe SHA256 = 3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
Wave A plan SHA256 = da383188a61f0488769b87e5767286ece7840d15262ebb07ed8c449173a6b806
A1 candidate SHA256 = 44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d
materialized inspection SHA256 = dee1fa0c6218f20eb4faeab5e30703323b256d17f02013048e452713ea86caa9
Stage5 recipe digest = eff06fcc5fa6610d0f402ad03a00a0144d2c7d8e4f83f9386f4a431646bf57c5
```

Static result:
```text
Stage1 authored4 / max4=3 / max6=4 / last=4800ms / GRUNT4
Stage4 authored6 / max4=6 / max6=6 / last=3300ms / GRUNT6
Stage8 authored7 / max4=6 / max6=7 / last=5100ms / GRUNT3+RUNNER4
```

All use y=0.46 and right-edge `entryBaseX=0.92`.

## 5. Admission interpretation

PASS proves:
- A1 signatures match the already-admitted Wave A plan;
- legal T1 vocabulary only;
- authored 4s density <= 8;
- Stage5 context anchor is unchanged;
- all existing representative recipe objects are unchanged;
- no scalar/shop/EXP/P×P/production mutation;
- expanded stage set is statically coherent under the dedicated A1 gate.

PASS does **not** prove:
- gameplay difficulty;
- lifecycle/dynamic balance;
- player skill expression;
- content adoption;
- numerical freeze;
- production readiness;
- full T1 exact recipe completion.

## 6. Current status and next boundary

```text
A1 exact spawn candidate = MATERIALIZED
A1 static gate = PASS
A1 dynamic execution = NOT RUN
A1 content adoption = NO
A2 authoring = NOT STARTED
```

Do **not** run a fake persistent-state chain over `[1,4,5,8]`: missing Stage2/3/6/7 would make that sequence lifecycle-incomplete.

Wave A's approved slice-by-slice rule therefore continues with:
```text
NEXT = MATERIALIZE A2 STAGES 15,19 -> STATIC RECIPE GATE
```

Dynamic execution remains deferred until a lifecycle-faithful contiguous context is available or a separately authorized standalone diagnostic contract is defined.

A1 remains candidate evidence only until explicit content adoption later.
