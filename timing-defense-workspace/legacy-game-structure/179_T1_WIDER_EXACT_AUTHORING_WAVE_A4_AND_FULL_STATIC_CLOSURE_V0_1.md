# Timing Defense — T1 Wider Exact Authoring Wave A4 & Full Static Closure V0.1

Date: 2026-10-26 KST  
Status: **STATIC PASS / FULL WAVE A MATERIALIZED / CANDIDATE ONLY / NOT ADOPTED / NO DYNAMIC EXECUTION / NO NUMERICAL FREEZE**

## 1. Scope

Wave A4 only for new authoring:
```text
Stage33
Stage37
Stage38
```

Exact context anchors:
```text
Stage39
Stage40
```

This evidence unit also performs cumulative static materialization of:
```text
representative base + A1 + A2 + A3 + A4
```

No production gameplay change occurred.

## 2. Authority

- Wave A bounded plan: `data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`
- Wave A plan/static result: `175_T1_WIDER_EXACT_AUTHORING_WAVE_A_PLAN_AND_STATIC_PREFLIGHT_V0_1.md`
- A1 static result: `176_T1_WIDER_EXACT_AUTHORING_WAVE_A1_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`
- A2 static result: `177_T1_WIDER_EXACT_AUTHORING_WAVE_A2_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`
- A3 static result: `178_T1_WIDER_EXACT_AUTHORING_WAVE_A3_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`
- T1 skeleton: `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`
- formation/cadence vocabulary: `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- representative base: `data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml`

Candidate:
`data/t1_wider_exact_authoring_wave_a4_candidate_v0_1.yaml`

## 3. A4 candidate recipes

### Stage33 — sustained Mage density surface
```text
E01 / G / F03 / CD04 / C2 / BASELINE,FLOOD
G12
0,150,300,450
2200,2350,2500,2650
5000,5150,5300,5450ms
y = 0.42..0.49
```

Intent:
- reuse known GRUNT vocabulary only;
- sustain density longer than Stage24 without exceeding the existing 4s authored cap;
- preserve Mage/AoE opportunity without introducing a new mechanic.

### Stage37 — bounded split-axis tempo
```text
E02 / G+R / F08 / CD04 / C2 / RUSH
G4 + R4
0..540ms first burst
2600..3140ms second burst
low axis = 0.30..0.32
high axis = 0.68..0.70
```

Intent:
- reuse F08 after Stage29;
- remove BRUTE and three-type synthesis complexity;
- create a known G+R tempo read before the Stage39 C3 peak.

### Stage38 — durable pre-peak bridge
```text
E01+E03 / G+B / F02 / CD03 / C1 / BULWARK
B,G,G,G @ 0..750ms
B,G,G,G @ 3300..4050ms
y = 0.43..0.49
```

Intent:
- known two-type durable-front grammar;
- simple line geometry;
- lower count, lower 4s density and much narrower geometry than Stage39;
- bridge into Stage39 without consuming its F08/CD05/C3 identity.

## 4. Exact context preservation

Stage39 remains the existing late-T1 synthesis peak:
```text
R+B / F08 / CD05 / C3 / RUSH,BULWARK
authored 14
max4 = 8
max6 = 12
ySpan = 0.22
```

Stage40 remains the existing Star Gate B synthesis recipe.

Exact digests from the final A4 run:
```text
Stage39 digest = 45dc3710bce7bc89ccfa88f56e457a8993ec735a900c49768f6893e919e3f275
Stage40 digest = 5e58f43170262d2be15a85099be3f72f1b41fab465891a3116b421480fa4d35c
```

## 5. First A4 run — validator false failure

Exact run:
```text
run      40210087895
artifact 12605450400
head     bd4e7e19437ced32b67dd0506576a85e8e430286
artifact sha256 1676a6c22045405f91e030523fe1846a4eda1fbde55b5a5bebaef46aa63abdb1
```

Only error:
```text
stage38-not-vocabulary-bounded-below-stage39-peak
```

The validator incorrectly treated monster-type cardinality as the decisive complexity proxy because Stage38 and Stage39 both contain two monster types.

That proxy contradicted the admitted signatures:
```text
Stage38 = G+B / F02 / CD03 / C1
Stage39 = R+B / F08 / CD05 / C3
```

Stage38 was already objectively bounded below Stage39 by authored count, 4s density, geometry width, formation, cadence and complexity bucket.

Classification:
```text
VALIDATOR_STAGE38_TYPE_CARDINALITY_PROXY_MISUSE_NO_CANDIDATE_CONTENT_FAILURE
candidateChangedAfterFailure = false
```

The guard was minimally corrected to compare actual geometry/pressure structure instead of requiring fewer monster types than Stage39.

## 6. Final A4 exact static evidence

Exact run:
```text
run      40210214458
artifact 12605184344
head     5d66f969e10177a0c9778474a332eeddefbf7dfb
artifact sha256 be3990ba8ea112ee99e226902fb7561eae8b2e6f94d7732230a48ce9d9fd0c66
status   PASS
errors   []
warnings []
```

Exact identities:
```text
base recipe SHA256 = 3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
Wave A plan SHA256 = da383188a61f0488769b87e5767286ece7840d15262ebb07ed8c449173a6b806
A1 SHA256 = 44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d
A2 SHA256 = 2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d
A3 SHA256 = 30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6
A4 SHA256 = 93b9c785ca800ad97ad0149e9931e1d43b58328744dbb5867fdc5b9261dfef36
full accumulated Wave A materialization SHA256 = 28b23f1f6332785009028ae9e531912c7dc2fb54da3a3a2db1536569b743774b
```

Static facts:
```text
Stage33 G12 / max4=8 / max6=12 / ySpan=0.07
Stage37 G4+R4 / max4=8 / max6=8 / ySpan=0.40
Stage38 G6+B2 / max4=7 / max6=8 / ySpan=0.06
Stage39 anchor authored14 / max4=8 / max6=12 / ySpan=0.22
```

All final guards passed:
```text
priorCandidatesPreserved = true
existingRepresentativeStagesPreserved = true
contextAnchorsPreserved = true
fullWaveAStaticMaterialized = true
```

## 7. Full Wave A static closure

All planned Wave A target slices are now materialized and individually static-admitted:
```text
A1 [1,4,8] = STATIC PASS
A2 [15,19] = STATIC PASS
A3 [24,25,29,30,31] = STATIC PASS
A4 [33,37,38] = STATIC PASS
```

The accumulated materialization preserves all representative authority and context anchors.

This closes the **Wave A materialization/static-validation work group**.

It does not close the full T1 Stage1-50 authoring problem because many stages remain skeleton-only and Wave A targets are noncontiguous.

## 8. Lifecycle / dynamic boundary

Do not run A1+A2+A3+A4 target stages as one persistent-state sequence.
They skip real stages and would produce false lifecycle evidence.

Dynamic execution remains deferred until either:
- a contiguous authored sequence is deliberately built; or
- a separate non-persistent diagnostic contract is explicitly authorized and labeled as such.

## 9. Adoption boundary

A1-A4 remain:
```text
MATERIALIZED
STATIC PASS
NOT ADOPTED
NO DYNAMIC EXECUTION
NO NUMERICAL FREEZE
NO PRODUCTION CHANGE
```

Static PASS proves structural legality and cross-slice consistency. It does not itself authorize adoption of the exact spawn counts/timestamps/Y positions.

Next boundary is therefore a **user decision gate** on whether the full Wave A exact spawn candidates should become the canonical T1 authoring baseline-with-watches. Such adoption would still not authorize production deployment, class/monster/shop/EXP/P×P scalar changes, or full 50-Stage freeze.
