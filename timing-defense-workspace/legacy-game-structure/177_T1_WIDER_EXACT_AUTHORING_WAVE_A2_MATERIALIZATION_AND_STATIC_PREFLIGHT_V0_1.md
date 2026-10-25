# Timing Defense — T1 Wider Exact Authoring Wave A2 Materialization & Static Preflight V0.1

Date: 2026-10-25 KST  
Status: **STATIC PASS / CANDIDATE ONLY / NOT ADOPTED / NO DYNAMIC EXECUTION / NO NUMERICAL FREEZE**

## 1. Scope

Wave A2 only:
```text
Stage15
Stage19
```

Exact context anchors:
```text
Stage18 = BRUTE first mixed / Lv16 collision watch
Stage20 = Star Gate A synthesis
```

No A3/A4 authoring occurred in this evidence unit.
A1 remains static-PASS candidate evidence only.

## 2. Authority

- Wave A bounded plan: `data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`
- Wave A plan/static result: `175_T1_WIDER_EXACT_AUTHORING_WAVE_A_PLAN_AND_STATIC_PREFLIGHT_V0_1.md`
- A1 static result: `176_T1_WIDER_EXACT_AUTHORING_WAVE_A1_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`
- T1 signature skeleton: `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`
- representative base: `data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`
- Stage49-50 approved baseline remains closed with watches under doc174.

Candidate:
`data/t1_wider_exact_authoring_wave_a2_candidate_v0_1.yaml`

## 3. Candidate recipes

### Stage15 — BRUTE first teach
```text
E03 / B / F01 / CD01 / C1 / BULWARK
spawns:
0    B y0.46
2200 B y0.46
4400 B y0.46
```

Intent:
- pure BRUTE vocabulary;
- slow readable drip before any BRUTE mix;
- no RUNNER/GRUNT attribution ambiguity;
- materially simpler than Stage18 first mixed encounter.

### Stage19 — first BRUTE/RUNNER target-order stagger
```text
E03+E02 / B+R / F02 / CD05 / C2 / BULWARK
spawns:
0    B y0.46
650  R y0.44
1300 R y0.48
3000 B y0.46
3650 R y0.43
4300 R y0.49
```

Intent:
- two bounded durable-front packets;
- BRUTE leads each packet, RUNNER follows;
- first target-order/stagger contrast after both monster types are already taught;
- remains simpler than Stage20 three-type synthesis.

## 4. Structural progression guard

The intended local sequence is:
```text
Stage15 = pure B teach
Stage18 = G+B first mix
Stage19 = B+R stagger / target reorder
Stage20 = G+R+B synthesis
```

This preserves the skeleton's escalation without inventing a new monster or scalar lever.

## 5. Exact static evidence

Exact run:
```text
run      40200875375
artifact 12601174423
head     ff240f4859fce0e993406b6253fe9edb3ba6631e
artifact sha256 6e6f4837ecbe6ea843c27840405b364acdbffe80d55688e79c081e8e974800a6
status   PASS
errors   []
warnings []
```

Exact identities:
```text
base recipe SHA256 = 3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
Wave A plan SHA256 = da383188a61f0488769b87e5767286ece7840d15262ebb07ed8c449173a6b806
A2 candidate SHA256 = 2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d
materialized inspection SHA256 = aef79d6323154dd0cfe660bc9e2d9a0bd580d75d905f1e15366c3dc3f5c5c617
Stage18 recipe digest = 7b47c81c1b617d1a607729367539abdbc3b16084e253d34854171bc653e53fad
Stage20 recipe digest = ae9d979abc9347b0be1b860579c73994e5c30c1c7c898168390db12d2653b5ba
```

Static result:
```text
Stage15 authored3 / max4=2 / max6=3 / last=4400ms / BRUTE3
Stage19 authored6 / max4=5 / max6=6 / last=4300ms / BRUTE2+RUNNER4
```

Geometry:
```text
Stage15 y = 0.46 only
Stage19 y = 0.43..0.49
entryBaseX = 0.92
```

All guards passed:
```text
contextAnchorsPreserved = true
existingRepresentativeStagesPreserved = true
progressionGuard = PURE_B_TEACH_TO_GB_MIX_TO_BR_STAGGER_TO_GRB_SYNTH
```

## 6. External check separation

The exact source commit also triggered the repository-connected Cloudflare check:
```text
Workers Builds: timing-defense-skilled-v2-harness
check-run 121191618577
conclusion = failure
```

This was **not** the A2 validator. The GitHub Actions `preflight` check-run `121191600322` completed successfully and produced the PASS artifact above.

Do not reinterpret the unrelated Cloudflare build check as A2 authoring failure. Production/harness branch state must be verified separately at session close.

## 7. Admission interpretation

PASS proves:
- Stage15/19 match the admitted Wave A2 skeleton metadata;
- only legal T1 monsters are used;
- Stage15 is a readable pure-BRUTE teach;
- Stage19 is a bounded B+R durable-front stagger;
- authored 4s density remains <= 8;
- Stage18 and Stage20 exact anchors are unchanged;
- all existing representative recipe objects are unchanged;
- no scalar/shop/EXP/P×P/production mutation occurred.

PASS does **not** prove:
- gameplay difficulty;
- dynamic/lifecycle balance;
- content adoption;
- numerical freeze;
- production readiness;
- full T1 exact recipe completion.

## 8. Current status

```text
A1 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A2 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A3 = NOT STARTED
A4 = NOT STARTED
A2 dynamic execution = NOT RUN
```

Dynamic persistent-chain execution remains deferred until contiguous authored context exists or a separately specified non-persistent diagnostic contract is authorized.

Next bounded gate:
```text
A3 STAGES 24,25,29,30,31
-> exact spawn candidate materialization
-> static recipe gate
```

Do not begin A4 before A3 static PASS.
