# 164 — T1 Representative Transition Slice Recipe Materialization and Static Preflight v0.1

Status: **DIAGNOSTIC CANDIDATE / STATIC PASS / NO RUNTIME CLAIM / NO PRODUCTION FREEZE**

## 1. Purpose

Materialize only the representative T1 transition slices authorized by `163_T1_REPRESENTATIVE_TRANSITION_SLICE_PREFLIGHT_V0_1.md` into deterministic spawn recipes, then apply a reproducible static guard check before any dynamic combat interpretation.

This is intentionally **not** full Stage1-50 exact authoring.

Canonical inputs:

- `160_FOUR_TIER_AUTHORING_CONSTRAINT_APPROVED_WITH_T1_BASELINE_CORRECTION_V0_1.md`
- `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`
- `162_T1_STAGE_SIGNATURE_STATIC_CONSISTENCY_AUDIT_V0_1.md`
- `163_T1_REPRESENTATIVE_TRANSITION_SLICE_PREFLIGHT_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/model_a_encounter_envelope_v0_1.yaml`

Materialized data:

- `data/t1_representative_transition_slice_recipes_v0_1.yaml`

Reproducible static analyzer:

- `tools/analyze_t1_transition_slice_recipes_v0_1.py`

## 2. Materialization rules

The candidate recipes obey the following bounded rules:

1. T1 monsters are only `GRUNT / RUNNER / BRUTE`.
2. T1 archetype components are only `E01 / E02 / E03`.
3. T1 formations are only `F01 / F02 / F03 / F04 / F08`.
4. T1 cadence is only `CD01..CD05`.
5. physical spawn entry remains `x=0.92`; no midfield pop-in is introduced.
6. old representative-recipe density guards are reused rather than inventing new density bands.
7. Stage5 and Stage18 OFF/ON comparisons reference the exact same recipe; only skill-enabled state may differ at execution time.
8. sequential slices declare `STAGE_SETTLED` and persistent `wallDeficit / combo / charge` as required runtime semantics.
9. Stage39-45 includes Lv31 activation-position variants at before-Stage41 / 43 / 45 only as a diagnostic reach-position probe. This does not freeze EXP.
10. no recipe here is a production scalar freeze.

## 3. Static result

Static result:

```text
RESULT=PASS errors=0 warnings=0
```

| Stage | Recipe | Authored count | Max 4s density | Max 6s density |
|---:|---|---:|---:|---:|
| 5 | T1_S05_RUNNER_TEACH | 4 | 4 | 4 |
| 18 | T1_S18_BRUTE_FIRST_MIX | 6 | 6 | 6 |
| 20 | T1_S20_STAR_GATE_A_SYNTH | 8 | 6 | 8 |
| 21 | T1_S21_RUNNER_HIGH_PRESSURE | 8 | 8 | 8 |
| 22 | T1_S22_BRUTE_HIGH_PRESSURE | 7 | 6 | 7 |
| 23 | T1_S23_RUSH_BULWARK_MIX | 8 | 8 | 8 |
| 39 | T1_S39_PRE_GATE_SPLIT_PRESSURE | 8 | 6 | 8 |
| 40 | T1_S40_STAR_GATE_B_SYNTH | 8 | 6 | 8 |
| 41 | T1_S41_LV31_RELIEF | 5 | 3 | 4 |
| 42 | T1_S42_ASCENSION_RUSH_READ | 6 | 5 | 6 |
| 43 | T1_S43_ASCENSION_BULWARK_READ | 6 | 5 | 6 |
| 44 | T1_S44_ASCENSION_BASELINE_BURST | 7 | 7 | 7 |
| 45 | T1_S45_ASCENSION_RUSH_BULWARK | 8 | 7 | 8 |
| 46 | T1_S46_POST_LV31_BULWARK | 8 | 8 | 8 |
| 47 | T1_S47_POST_LV31_RUSH | 8 | 6 | 8 |
| 48 | T1_S48_POST_LV31_CLUSTER | 8 | 8 | 8 |
| 49 | T1_S49_POST_LV31_SPLIT | 8 | 6 | 8 |
| 50 | T1_S50_LEARNED_VOCAB_FINAL | 8 | 8 | 8 |

The highest authored 4-second density is `8`, exactly at the inherited NORMAL upper bound. No recipe enters the inherited `9-10` WATCH band.

T1 has no SPLITTER, therefore this candidate's effective entity count equals authored spawn count for the static density check.

## 4. Boundary-specific findings

### Stage5 — RUNNER × Lv6

The encounter remains a simple isolated RUNNER teach recipe. OFF/ON comparison is legally pairable because the recipe object is identical between variants.

Static status: **ADMITTED FOR PAIRED MICRO-SIM**.

### Stage18 — BRUTE first mixed × Lv16

The encounter expresses BRUTE durability with GRUNT support without introducing another vocabulary element.

Static status: **ADMITTED FOR PAIRED MICRO-SIM**.

### Stage20-23 — first star gate into first high pressure

The sequence preserves the intended grammar:

```text
S20 synthesis
-> S21 RUNNER high pressure
-> S22 BRUTE high pressure
-> S23 mixed RUSH + BULWARK
```

Static recipe density does not create a new spike beyond the inherited normal bound.

Static status: **ADMITTED FOR SEQUENTIAL MICRO-SIM, SUBJECT TO LIFECYCLE FIDELITY**.

### Stage39-45 — second star gate and Lv31 ascension

The strongest static transition finding is:

```text
Stage40 max4s = 6
Stage41 max4s = 3
```

Therefore Stage41 is not merely labeled as relief; the authored spawn schedule actually reduces short-window density by 50% relative to Stage40.

This does not prove the Stage is dynamically easy for every class, because BRUTE/RUNNER chronology, persistent wall deficit, combo/charge state and class package effects still require execution.

Static status: **ADMITTED FOR SEQUENTIAL LV31 REACH-POSITION MICRO-SIM**.

### Stage46-50 — post-Lv31 mastery and final

All five recipes stay inside previously taught T1 vocabulary. Stage50 recombines the learned vocabulary without introducing a new monster/archetype/cadence family.

Static status: **ADMITTED FOR SEQUENTIAL POST-LV31 MICRO-SIM**.

## 5. What this PASS does not prove

This static PASS does **not** prove:

- target reorder behavior;
- spawn-to-first-contact runtime timing;
- actual peak active enemy count;
- removal throughput;
- Tank control value or objective-protection value;
- wall damage / wall reserve;
- root timing action count;
- combo or charge carry behavior;
- exact `STAGE_SETTLED` time;
- skill collision severity;
- class clear parity or class balance;
- actual Lv6/Lv16/Lv31 reach from EXP;
- launch balance;
- exact Stage1-50 recipe correctness.

Those claims are reserved for a lifecycle-faithful dynamic diagnostic.

## 6. Runner fidelity finding

Existing runners cannot simply be mixed to obtain valid numbers:

- the old Layer-A runner is useful for isolated encounter semantics but resets state per recipe and does not provide the required Lv16/Lv31 sequential contract;
- later P5/P6 runners demonstrate persistent-state and `STAGE_SETTLED` handling but are wired to different late-stage fixtures and cannot silently substitute those fixtures for the new T1 recipes.

Therefore the next correct step is a small dedicated adapter/runner that consumes the exact new T1 recipe data while reusing the approved lifecycle and skill authorities.

## 7. Decision

```text
T1 representative recipe materialization = COMPLETE
static recipe preflight = PASS
runtime interpretation = NOT YET AUTHORIZED BY EVIDENCE
full T1 Stage1-50 exact recipe freeze = DEFERRED
production gameplay change = UNAUTHORIZED
```
