# Timing Defense — T1 Representative Transition Slice Preflight V0.1

Date: 2026-10-24 KST  
Status: **BOUNDED DIAGNOSTIC PREFLIGHT / NO GAMEPLAY ADOPTION / NO PRODUCTION NUMERICAL FREEZE**

Depends on:
- `160_FOUR_TIER_AUTHORING_CONSTRAINT_APPROVED_WITH_T1_BASELINE_CORRECTION_V0_1.md`
- `161_T1_STAGE1_50_SIGNATURE_SKELETON_CANDIDATE_V0_1.md`
- `162_T1_STAGE_SIGNATURE_STATIC_CONSISTENCY_AUDIT_V0_1.md`
- P3 `STAGE_SETTLED` / persistent-state authority
- P4/P6 power and EXP watches

## 1. Why bounded slices first

The 50-Stage signature skeleton passes static structure with watches.
The next cheapest uncertainty reduction is **not** to author exact recipes for all 50 Stages.

Deepen only where multiple systems cross:
- new-monster pedagogy;
- first-time skill learning;
- star boundaries;
- first high-pressure promotion;
- soft-wall transition;
- Lv31 acquisition runway;
- post-Lv31 mastery/final.

This follows progressive deepening and avoids expensive rework.

## 2. Slice A — RUNNER teach × Lv6

Reference Stage signature:
```text
Stage5 = E02 / RUNNER / F01 / CD01 / C1
```

Diagnostic paired states:
```text
A0 = Lv6 not yet active
A1 = Lv6 active
```

Purpose:
- confirm RUNNER remains readable in either state;
- confirm Lv6 power does not erase RUNNER's speed question;
- identify whether root-action opportunity changes enough to affect progression interpretation.

Do not fit EXP to make A0 or A1 preferred.

## 3. Slice B — BRUTE first mixed × Lv16

Reference:
```text
Stage18 = E03 / G+B / F02 / CD03 / C1
```

Paired states:
```text
B0 = Lv16 not yet active
B1 = Lv16 active
```

Purpose:
- raw durability remains readable after skill power change;
- target-order/frontline dwell remains the authored question;
- no class must require hidden compensation.

## 4. Slice C — Stage20-23 gate and first high-pressure ramp

Sequential slice:
```text
Stage20 = first T1 synthesis / Star Gate A
Stage21 = RUNNER first high-pressure
Stage22 = BRUTE first high-pressure
Stage23 = speed-vs-durability contrast peak
```

Must execute with persistent within-slice state:
- wall deficit persists;
- combo persists;
- charge persists;
- Stage advances only at STAGE_SETTLED;
- no enemy/transient leakage.

Purpose:
- verify Stage20 reward boundary is not also an arbitrary mechanical cliff;
- verify 20->23 pressure rises by understandable authored questions;
- separate RUSH vs BULWARK pressure rather than stacking every axis simultaneously.

## 5. Slice D — Stage39-45 soft-wall -> 2★ -> Lv31 ascension

Sequential structure:
```text
39 = rare C3 late synthesis peak
40 = C2 Star Gate B known-vocabulary check
41 = C0 acquisition relief
42 = C1 tempo
43 = C1 durable
44 = C1 density
45 = C2 moderate mixed mastery
```

Diagnostic Lv31 reach variants:
```text
D41 = reaches Lv31 around Stage41
D43 = reaches Lv31 around Stage43
D45 = reaches Lv31 around Stage45
```

These are reach-position diagnostics, not an EXP-formula freeze.

Purpose:
- confirm Stage40 is not a cliff;
- confirm 41-45 gives meaningful post-unlock runway across the accepted reach window;
- confirm different class Lv31 packages receive at least one relevant known-vocabulary surface;
- confirm no need for new monster/mechanic novelty here.

## 6. Slice E — Stage46-50 post-Lv31 mastery/final

Sequential structure:
```text
46 = C2 durable mastery
47 = C1 focused tempo
48 = C2 density+tempo mastery
49 = C2 split-axis pre-final mastery
50 = C3 full learned-vocabulary synthesis
```

Assume Lv31 active for the intended diagnostic state.

Purpose:
- verify recovery/focused challenge remains between harder synthesis stages;
- rotate class-opportunity surfaces instead of maximizing one specialist family;
- Stage50 tests learned vocabulary rather than introducing mandatory new grammar.

## 7. Minimum metrics for deterministic recipe phase

For each representative recipe collect:

### Entity / density
```text
authoredSpawnCount
effectiveEntityCount
peakActive
max4sDensity
max6sDensity
```

### Chronology / targeting
```text
frontlineBlockTime
targetReorderCount
backlineExposure where applicable
spawn-to-first-contact timing
```

### Outcome dimensions
```text
removalThroughput
controlValue
wallDamage / wallReserve
rootTimingActionCount
stageSettledTime
failureClassification
```

### Class opportunity
Do not collapse to one fairness score.
Retain per-class directional opportunity/weakness observations.

## 8. Fidelity rules

- physical right-edge spawn authority remains unchanged;
- no mid-field pop-in;
- runtime target order remains actual authoritative position/validity;
- no forced class parity;
- survival != clear;
- Tank low removal alone is not a defect;
- no flat shop->EXP multiplier;
- do not relax a predeclared recipe gate after seeing results;
- exact scalar changes are last, after geometry/chronology/composition diagnosis.

## 9. Scope boundary

This preflight authorizes only **candidate deterministic recipe materialization and diagnostic comparison** for the representative slices.

It does not authorize:
- production gameplay changes;
- exact 50-Stage recipe freeze;
- class buff/nerf;
- monster scalar freeze;
- EXP/shop numerical freeze;
- P×P change;
- boss adoption.

If representative slices pass, widen carefully to the remaining T1 skeleton.
If a slice fails, repair the lowest causal layer first and recheck only the affected neighborhood.
