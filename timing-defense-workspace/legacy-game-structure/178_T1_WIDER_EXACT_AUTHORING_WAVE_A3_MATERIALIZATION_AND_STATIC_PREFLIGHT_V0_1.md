# Timing Defense — T1 Wider Exact Authoring Wave A3 Materialization & Static Preflight V0.1

Date: 2026-10-25 KST  
Status: **STATIC PASS / CANDIDATE ONLY / NOT ADOPTED / NO DYNAMIC EXECUTION / NO NUMERICAL FREEZE**

## 1. Scope

Wave A3 only:
```text
Stage24
Stage25
Stage29
Stage30
Stage31
```

A1 and A2 are prior static-PASS candidate evidence only and were treated as immutable inputs for accumulated materialization.
No A4 authoring occurred in this evidence unit.

## 2. Authority

- Wave A bounded plan: `data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`
- Wave A plan/static result: `175_T1_WIDER_EXACT_AUTHORING_WAVE_A_PLAN_AND_STATIC_PREFLIGHT_V0_1.md`
- A1 static result: `176_T1_WIDER_EXACT_AUTHORING_WAVE_A1_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`
- A2 static result: `177_T1_WIDER_EXACT_AUTHORING_WAVE_A2_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`
- T1 signature skeleton: `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`
- formation/cadence vocabulary: `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- representative base: `data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`
- Stage49-50 approved baseline remains closed with watches under doc174.

Candidate:
`data/t1_wider_exact_authoring_wave_a3_candidate_v0_1.yaml`

## 3. Candidate recipes

### Stage24 — GRUNT density pressure
```text
E01 / G / F03 / CD04 / C1 / BASELINE,FLOOD
0,150,300,450ms       = G cluster burst 1
2800,2950,3100,3250ms = G cluster burst 2
y = 0.42..0.49
```
Intent:
- eight-GRUNT density surface;
- two readable four-unit cluster bursts;
- Mage/AoE opportunity without new monster vocabulary;
- high pressure via density, not complexity.

### Stage25 — Lv21 first-time reward buffer
```text
E01 / G / F04 / CD01 / C0 / BASELINE
0    G y0.24
1800 G y0.72
3600 G y0.36
5400 G y0.64
```
Intent:
- lower count and lower 4s density than Stage24;
- wide scatter geometry;
- explicit recovery/attribution space for the Lv21 candidate window;
- no new grammar.

### Stage29 — first bounded split-axis synthesis
```text
E02+E03 / G+R+B / F08 / CD05 / C2 / RUSH,BULWARK
0    B y0.30
450  R y0.28
900  G y0.32
2100 B y0.70
2550 R y0.72
3000 G y0.68
4500 R y0.30
4950 G y0.28
5400 B y0.70
```
Intent:
- first bounded T1 F08 synthesis;
- two spatially distinct axes with no midfield clutter;
- all three learned T1 monsters represented equally;
- staggered target-order pressure without advanced backline grammar.

### Stage30 — Checkpoint B decompression
```text
E01+E03 / G+B / F01 / CD03 / C1 / BASELINE
0,250,500ms          = G,G,B wave 1
3300,3550,3800,4050 = G,B,G,G wave 2
```
Intent:
- lower geometry/vocabulary complexity than Stage29;
- two-type known-vocabulary read check;
- no RUNNER;
- checkpoint synthesis without a new mechanic.

### Stage31 — soft-wall durable-pressure entry
```text
E03 / G+B / F02 / CD04 / C1 / BULWARK
0,200,400,600ms       = B,G,G,G
3000,3200,3400,3600ms = B,G,G,G
```
Intent:
- repeated durable-front burst;
- narrow F02 line geometry;
- difficulty rises through short-window intensity, not complexity;
- first soft-wall durable-pressure entry.

## 4. Structural progression guard

The admitted local shape is:
```text
Stage24 density pressure
-> Stage25 Lv21 reward buffer
-> Stage29 bounded three-type split-axis synthesis
-> Stage30 two-type checkpoint decompression
-> Stage31 simple but denser durable soft-wall entry
```

This is recorded as:
`DENSITY_TO_LV21_BUFFER_TO_SPLIT_SYNTH_TO_CHECKPOINT_TO_DURABLE_SOFTWALL_ENTRY`.

## 5. First exact run — validator false fail

Run:
```text
run      40205234927
artifact 12603262478
head     8533a37131c036a8fff270176b3cc8c8503f1de6
artifact sha256 ce2a496d58066c8cfba49ee0c0fd6f634596a06bf2cfd1ab9e7f970e6670a606
conclusion = failure
```

Only error:
```text
stage31-geometry-too-complex-for-c1-entry
```

Classification:
```text
VALIDATOR_GEOMETRY_PROXY_MISUSE / NO CANDIDATE CONTENT FAILURE
```

Reason:
- Stage31 actual Y span was only `0.43..0.49` (`0.06`);
- validator incorrectly used the number of distinct Y literals as a complexity proxy;
- F02 line readability is about axis width/distribution, not how many small jitter values are numerically distinct.

Minimal correction:
- replace distinct-Y-count guard with `Stage31 ySpan <= 0.08` guard.

Candidate data was not changed.

## 6. Final exact static evidence

Final exact rerun:
```text
run      40205404257
artifact 12603138180
head     2eb99491bb555e2f15ddc2dbe94429db31abebf7
artifact sha256 c1cfde2a366226e028812a0f3cea7192ba62e7c3050e02b0a98a9be3ce1f8efc
status   PASS
errors   []
warnings []
```

Exact identities:
```text
base recipe SHA256 = 3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
Wave A plan SHA256 = da383188a61f0488769b87e5767286ece7840d15262ebb07ed8c449173a6b806
A1 candidate SHA256 = 44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d
A2 candidate SHA256 = 2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d
A3 candidate SHA256 = 30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6
accumulated materialized SHA256 = a401d619151681befeac38a1b15d0b56c4b9ae2162901eede60e77a737a6bd69
```

Static facts:
```text
Stage24 authored8 / max4=8 / max6=8 / G8 / ySpan=0.07
Stage25 authored4 / max4=3 / max6=4 / G4 / ySpan=0.48
Stage29 authored9 / max4=6 / max6=9 / G3+R3+B3 / ySpan=0.44
Stage30 authored7 / max4=6 / max6=7 / G5+B2 / ySpan=0.06
Stage31 authored8 / max4=8 / max6=8 / G6+B2 / ySpan=0.06
```

Accumulated guards:
```text
existing representative stages preserved = true
A1 preserved = true
A2 preserved = true
no duplicate Wave A stage = true
```

## 7. Admission interpretation

PASS proves:
- all five A3 stages match admitted skeleton metadata;
- only T1 legal monsters are used;
- Stage25 is a real count/density recovery relative to Stage24;
- Stage29 is a bounded split-axis three-type synthesis;
- Stage30 decompresses to two types and simple F01 wave grammar;
- Stage31 raises short-window intensity while keeping narrow F02 geometry and C1 complexity;
- authored 4s density remains <= 8;
- base representative recipes remain unchanged;
- A1 and A2 exact candidate objects remain unchanged in accumulated materialization;
- no scalar/shop/EXP/P×P/production mutation occurred.

PASS does **not** prove:
- gameplay difficulty;
- lifecycle/dynamic balance;
- content adoption;
- numerical freeze;
- production readiness;
- full T1 exact recipe completion.

## 8. Current status

```text
A1 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A2 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A3 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A4 = NOT STARTED
A3 dynamic execution = NOT RUN
```

Persistent-chain dynamic work remains deferred until contiguous authored context exists or a separately specified non-persistent diagnostic contract is authorized.

Next bounded gate:
```text
A4 STAGES 33,37,38
-> exact spawn candidate materialization
-> static recipe gate
```

Preserve Stage39 and Stage40 as exact context anchors. Do not expand to full 50-Stage exact authoring from this PASS alone.
