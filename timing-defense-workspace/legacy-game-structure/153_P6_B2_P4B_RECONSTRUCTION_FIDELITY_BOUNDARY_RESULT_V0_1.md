# Timing Defense — P6-B2 P4-B Reconstruction Fidelity Boundary Result V0.1

Date: 2026-10-24 KST  
Status: **P6-B2 RECONSTRUCTION ATTEMPT COMPLETE / PREDECLARED FIDELITY GATE NOT MET / OLD PER-RECIPE RESPONSE MAP IRRECOVERABLE FROM CURRENT SOURCES / SHOP INJECTION BLOCKED / NEW METHOD DECISION REQUIRED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`

Production gameplay remains unchanged and unauthorized.

---

## 1. Plain-language result

The user approved P6-B2 method A:

```text
rebuild a bounded P4-B-style synthetic feedback runner
-> first prove fidelity against archived P4-B results
-> only then inject P5 stagewise shop trajectory
```

The fidelity-first rule prevented an unsafe shortcut.

The old P4-B result data survives, but its exact per-recipe response table and dedicated runner do not survive in the repository history available to this project.
Several reconstruction families were tested without changing gameplay values or relaxing the acceptance gate.

The best recovered approximation is very close globally:

```text
120 archived class×Tier×milestone P50 points
85 exact
115/120 = 95.83% within ±1 Stage
mean absolute error = 0.354 Stage
maximum absolute error = 4 Stages
```

However the acceptance gate had been fixed **before** looking at the result:

```text
within ±1 Stage >= 90%
mean absolute error <= 0.75 Stage
maximum absolute error <= 3 Stages
```

The best approximation therefore **fails the gate because max error = 4**.
The gate is not relaxed after the fact.

More importantly, attempts to reconstruct encounter-specific E01–E20 response using currently recoverable geometry/v0.16 rank information made held-out milestone fidelity worse rather than better.
Therefore the missing old per-recipe response map must not be reverse-fit from the archived milestone outputs.

Classification:

```text
OLD_P4B_DEDICATED_RUNNER = NOT_RECOVERED
OLD_P4B_EXACT_PER_RECIPE_RESPONSE_MAP = NOT_RECOVERABLE_FROM_CURRENT_SOURCES_WITHOUT_TARGET_FITTING
GLOBAL_RESPONSE_ENVELOPE_FAMILY = STRONGLY_SUPPORTED_BUT_NOT_GATE_PASSING_EXACT_REPLACEMENT
P5_SHOP_INJECTION_INTO_RECOVERED_OLD_P4B = BLOCKED
```

---

## 2. Why exact recovery matters before shop injection

P6-B1 already proved shop→EXP feedback is bidirectional:

```text
more shop ATK
-> faster removal on the same survived path
-> fewer timing actions / less EXP opportunity

but also

more shop ATK
-> prevents some failures
-> exposes later Stages
-> creates additional later timing actions / EXP opportunity
```

Therefore a 1–4 Stage progression error is not harmless when the next question is exact skill reach.
A shifted unlock can alter combat power, which changes action opportunity again.

For that reason this result does not take the late-run ~4% clean compression from P6-B1 and apply it linearly across Stage1–45, and does not use nominal shop ATK percentage as a direct action-count multiplier.

---

## 3. Surviving historical P4-B authority

Archived P4-B still preserves useful diagnostic outputs.

### 3.1 All-20 median action ratio vs Lv1

```text
          Lv6    Lv11   Lv16   Lv21
Knight    1.000  0.546  0.500  0.447
Rogue     0.636  0.633  0.633  0.500
Tank      1.000  1.000  1.000  0.521
Archer    0.675  0.658  0.552  0.435
Mage      0.650  0.544  0.449  0.429
```

These remain bounded historical evidence that offensive/coverage skills can substantially reduce later EXP-producing timing opportunities.
They are not production balance values.

### 3.2 Independent early P3 cross-check

Archived P3 first-10 Lv6 turn delta:

```text
Knight about -0.2%
Rogue  about -20.2%
Tank     0.0%
Archer about -18.9%
Mage   about -14.7%
```

Archived P4-B bounded response prediction:

```text
Knight   0.0%
Rogue  -20.73%
Tank     0.0%
Archer -19.64%
Mage   -19.27%
```

The structural self-damping signal therefore remains valid even though the lost propagation runner is not exactly recoverable.

---

## 4. Repository-history recovery boundary

The archived P4-B machine-readable result was committed as:

```text
data/p4b_combat_feedback_divergence_v0_1.json
```

and its report as:

```text
81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md
```

Repository history for those commits contains the result/report but does not contain a dedicated P4-B runner or a complete E01–E20 × class × skill-level response table.

The still-present source assets include:
- P4-A corpus and runner;
- 20 representative encounter recipes;
- class-aware Layer-A simulators;
- materialized role-expression overlays;
- v0.16 skill formulas;
- SKILLED_V2 central sequence machinery.

Those assets are enough to test reconstruction hypotheses, but not enough to identify the exact old per-recipe map uniquely without fitting to the archived reach targets.

Target-fitting is rejected because it would manufacture fidelity rather than recover it.

---

## 5. Reconstruction probes

Temporary branch:

```text
timing-defense-workspace-temp-p6-b2-p4b-reconstruction
```

No temp runner/workflow has planning or production authority.

### 5.1 Static all-spawn reconstruction

Run:
```text
40031831033
```
Exact-byte repeat: PASS  
SHA256:
```text
6a0a58363378c106d717962111b30d1ec8987048cbf85be205591c3def4f64fc
```

Result:
- not equivalent;
- offensive/coverage classes were overexpressed because the reduced static model exposed too many simultaneous targets;
- rejected as fidelity basis.

### 5.2 Existing Layer-A Lv6 fidelity

Run:
```text
40032022545
```
Exact-byte repeat: PASS  
SHA256:
```text
f914e024e9584ad03bb283a7bd0e8745fbda1ba988ab03bb6ef793ce1500910e
```

Median action ratios:

```text
Knight 1.000000 vs historical 1.000
Rogue  0.615385 vs historical 0.636
Tank   1.000000 vs historical 1.000
Archer 0.720779 vs historical 0.675
Mage   0.625000 vs historical 0.650
```

This strongly identifies the historical Layer-A family but not exact P4-B fidelity.

### 5.3 Materialized all-20 geometry Lv6 probe

Run:
```text
40032329712
```
Exact-byte repeat: PASS.

Materialized geometry improved Mage/Rogue median proximity but did not recover Archer or the full historical range.
No geometry microtuning was performed.

### 5.4 SKILLED_V2 direct row reuse probe

Run:
```text
40032590027
```
Exact-byte repeat: PASS  
SHA256:
```text
73ef0ee4f3ca96ff85e77e3b8d409d83504957a762f14e11f0a222fde100a279
```

Direct SKILLED_V2 reuse was farther from archived Lv6 action ratios:

```text
Archer ~0.806 vs 0.675
Rogue  ~0.721 vs 0.636
Mage   ~0.696 vs 0.650
Knight  1.000
Tank    1.000
```

Therefore P4-B cannot be reconstructed by simply rerunning the later SKILLED_V2 all-20 rows.

---

## 6. Global response-envelope equivalence probe

A bounded propagation hypothesis used:
- the original P4-A CENTRAL 50-Stage synthetic workload corpus;
- original P4-A 100 deterministic seeds;
- original quality-credit candidate;
- original midpoint threshold candidates;
- archived P4-B class/skill median action-response ratios;
- feedback applied as equivalent Stage workload-clearance change;
- Lv26/Lv31 power inactive, matching archived P4-B scope.

Run:
```text
40032994701
```
Exact-byte repeat: PASS  
SHA256:
```text
7fe959498deba8c3e89b7eb7eb4efd4ddb57d0832e617fe43e2dae7ab44f10f4
```

Held-out validation against 120 archived P50 milestone outputs:

```text
exact                 82/120 = 68.33%
within ±1 Stage       115/120 = 95.83%
mean abs error        0.383 Stage
max abs error         4 Stages
```

The main maximum-error outlier was:

```text
Mage T1 Lv21: predicted 41 vs archived 37
```

Predeclared gate failed only on the maximum-error criterion, but failure is failure; the gate was not changed.

---

## 7. Propagation semantics matrix

Final bounded reconstruction matrix tested four structural variants:

```text
1. global response + immediate same-Stage activation
2. global response + next-Stage boundary activation
3. reconstructed per-recipe response + immediate activation
4. reconstructed per-recipe response + next-Stage boundary activation
```

The per-recipe reconstruction did **not** fit milestone targets.
It only:
- preserved the archived class/level min/median/max response envelope;
- used the currently reconstructable materialized-all20 v0.16 response ordering to rank E01–E20;
- left all 120 milestone outcomes held out for validation.

Execution:

```text
run 40033665060
job 120687797781
commit 730f58ebdc5325766267b8ce9a7e7a72bfe79038
```

Exact-byte repeat: PASS  
SHA256:
```text
af4bb68afa10e6cef4f8e1f8102defb824c1d710e013a48aac82c269eee675ea
```

### Results

#### Global immediate
```text
exact 82/120
within ±1: 115/120 = 95.83%
mean abs error 0.383
max error 4
GATE FAIL
```

#### Global Stage-boundary — best tested mode
```text
exact 85/120 = 70.83%
within ±1: 115/120 = 95.83%
mean abs error 0.354
max error 4
GATE FAIL
```

#### Reconstructed per-recipe immediate
```text
exact 72/120 = 60.00%
within ±1: 102/120 = 85.00%
mean abs error 0.608
max error 5
GATE FAIL
```

#### Reconstructed per-recipe Stage-boundary
```text
exact 71/120 = 59.17%
within ±1: 105/120 = 87.50%
mean abs error 0.579
max error 5
GATE FAIL
```

Thus:

```text
CURRENTLY_RECONSTRUCTABLE_PER_RECIPE_RANK_SIGNAL != OLD_P4B_PER_RECIPE_RESPONSE_MAP
```

The result is evidence against further reverse-fitting.

---

## 8. What remains usable vs irrecoverable

### Usable

```text
P4-A synthetic 50-Stage opportunity corpus
P4-B archived class/skill response envelope and historical divergence classification
P3 independent early Lv6 opportunity signal
current approved/diagnostic skill semantics
P5 stagewise shop economy trajectory
P6-B1 late-run paired shop/EXP attribution
current run-state / STAGE_SETTLED contracts
```

### Not recoverable with current sources without target-fitting

```text
old P4-B dedicated runner bytes
old exact E01–E20 × class × Lv6/Lv11/Lv16/Lv21 action-response map
old exact propagation implementation details beyond the archived outputs
```

---

## 9. P6-B2 closure boundary

Method A was executed as approved through its fidelity gate.
It does **not** authorize shop injection because the fidelity gate failed.

Do not:
- loosen the gate after observing results;
- tune per-recipe response until archived milestone targets fit;
- inject P5 shop into a failed recovered-old-P4B model and report exact Lv31 Stage shifts;
- linearly spread P6-B1 late-run compression across Stage1–45;
- adopt any EXP/shop number;
- change production.

The old P4-B result remains historical bounded evidence, not an exact executable authority.

---

## 10. Next decision required

The safest next method is a **fresh forward P6 progression runner**, not further archaeology of the lost P4-B runner.

### Recommended — FRESH_FORWARD_P6

Build a new bounded Stage1–45 synthetic progression runner from currently surviving authority:

```text
P4-A multi-Tier synthetic Stage opportunity corpus
+ current run-state contract
+ current skill semantics by milestone
+ SKILLED_V2_CENTRAL judgment process
+ P5 stagewise shop economy trajectory
+ explicit diagnostic shop-effect anchors
```

Validate it independently against multiple surviving boundaries rather than one lost runner:

```text
P3 early-run Lv6 behavior
P4-B archived direction/envelope
P6-B1 late shop-ATK bidirectional behavior
P6 class/encounter identity guards
```

Purpose:
- answer current P6 shop→event-count→EXP→skill-reach feedback with a reproducible model that can be maintained going forward;
- stop pretending the lost P4-B implementation is exact authority.

This is a **new methodology choice** and requires user approval before execution.

### Alternative — ACCEPT_FAILED_GLOBAL_APPROXIMATION

Use the best global Stage-boundary approximation despite its predeclared gate failure.

Not recommended because exact skill-reach claims could inherit the known 4-Stage outlier.

### Alternative — DEFER_EXACT_SKILL_REACH

Retain only P6-B1 causal evidence and defer exact shop/EXP/skill-reach propagation until later concrete Tier authoring.

Safer than knowingly using a failed approximation, but it postpones P6 progression convergence.

No next method is adopted by this result document.
