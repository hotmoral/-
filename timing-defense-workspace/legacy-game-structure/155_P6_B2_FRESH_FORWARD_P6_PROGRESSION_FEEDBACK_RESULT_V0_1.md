# Timing Defense — P6-B2 FRESH_FORWARD_P6 Progression Feedback Result V0.1

Date: 2026-10-24 KST  
Status: **P6-B2 FRESH-FORWARD DIAGNOSTIC COMPLETE / STRUCTURAL DIVERGENCE RECONFIRMED / ABSOLUTE MAGNITUDE WATCH / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority / depends on:
- `154_P6_B2_FRESH_FORWARD_P6_AUTHORITY_AND_FIDELITY_CONTRACT_V0_1.md`
- `153_P6_B2_P4B_RECONSTRUCTION_FIDELITY_BOUNDARY_RESULT_V0_1.md`
- `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
- `111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`

User approval:
- FRESH_FORWARD_P6 execution approved before implementation.

Canonical execution base:
- `timing-defense-workspace@cca6ce7e8ec0f874faf33069ec922e15c3c07ef1`

Temporary execution lane:
- branch `timing-defense-workspace-temp-p6-b2-fresh-forward`
- final temp head `5093a151142090d58c0e1d26f52cdbee43653542`
- no planning or production authority

Production / harness at close:
- production `timing-defense-cloudflare-do-poc@ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- harness `timing-defense-skilled-v2-harness-v01@063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- unchanged

---

# 0. Question

The fresh-forward lane did not attempt to reconstruct or reverse-fit the lost P4-B implementation.

It asked:

> Conditional on a Stage being entered, what happens to actual root timing-action opportunity, provisional EXP opportunity and milestone reach when current class-skill structure and the existing diagnostic stagewise shop trajectory are propagated forward from surviving authority?

This lane deliberately does **not** claim full-campaign survival.
P6-B1 remains the independent survival-extension authority.

---

# 1. Execution model

Bounded inputs:

```text
P4-A CENTRAL synthetic Stage opportunity fixtures
+ current run-state semantics
+ current Lv6-Lv26 skill structure
+ SKILLED_V2_CENTRAL
+ P5 CLEAR_KILL_70_30 / CENTER50 / BALANCED diagnostic shop trajectory
+ diagnostic ATK +8%/rank lane
+ provisional per-root-action XP_CREDIT
```

Fixtures:
- `T1_CENTRAL`
- `T2_CENTRAL`
- `T3_CENTRAL`
- `T4_CENTRAL`

Matrix:

```text
4 fixtures
× 5 classes
× 20 deterministic seeds
× SHOP_OFF / diagnostic ATK_ON
```

The runner stops when Lv31 is first acquired.
It does not need to invent a post-Lv31 final-package implementation for this question.

Important explicit fidelity choices:
- Stage access is forced/conditional; wall arrival is not converted into campaign failure.
- Heavy X+Y consumes two judgments but gives exactly one EXP award.
- generated skill hits and N3 give zero independent EXP.
- level unlock applies beginning with the **next** root action, not retroactively to the action that crossed the threshold.
- Rogue Lv16 may shorten the next attack interval on a qualifying PERFECT-containing root.
- Archer Lv11 projectile-speed meaning is not incorrectly converted into attack-cadence compression.
- Mage Lv26 preserves `immediate package -> death/spawn -> chain -> delayed resonance` ordering.
- exact Stage recipes, 1500ms serial packet assembly, Lv26 coefficients and shop-effect coefficient remain diagnostic.

---

# 2. Exact execution / determinism

## First run

```text
run 40038596684
job 120704038229
commit ca7ee2562c9fad10b28f611a5d4749aa03f51116
```

The runner itself completed twice with exact-byte equality.
Output SHA256:

```text
80c920d4e2c3982b6a5562768ed4b37f87e2f41703077e46ae8e3cf9d411c6d4
```

The workflow nevertheless ended FAIL because the first validator treated any isolated same-Stage ATK exception as a hard failure.

That validator condition was stronger than the pre-written contract.
The contract explicitly required discrete skill/target-chronology exceptions to be **reported, not hidden**.

## Final contract-aligned rerun

Only the validator/workflow interpretation was changed.
The combat/progression runner was not changed.

```text
run 40039163053
job 120705885236
commit 5093a151142090d58c0e1d26f52cdbee43653542
SUCCESS
```

Two executions again compared exact-byte equal.
Output SHA256 remained exactly:

```text
80c920d4e2c3982b6a5562768ed4b37f87e2f41703077e46ae8e3cf9d411c6d4
```

Therefore the validator correction did not change the result.

Final artifact:
- artifact id `12538760728`
- artifact ZIP SHA256 `e80ea6db2c9a545662d309851ff51c240073a6c777c4d58ecc9443a4f237b968`

---

# 3. Fidelity checks

## 3.1 Invariants

```text
invariantFailures = 0
survivalClaim = false
```

Heavy / judgment / EXP-accounting rules passed.

## 3.2 Independent early-Lv6 direction

Fresh runner first-10 directional response:

| Class | root-action delta | expected | result |
|---|---:|---|---|
| Knight | -3.8123% | approximately neutral | PASS |
| Rogue | -41.3490% | reduced | PASS |
| Tank | 0.0000% | approximately neutral | PASS |
| Archer | -40.4692% | reduced | PASS |
| Mage | -38.8406% | reduced | PASS |

The required direction passes for all five classes.

However, historical independent P3 first-10 magnitude was approximately:

```text
Knight  -0.2%
Rogue  -20.2%
Tank     0.0%
Archer -18.9%
Mage   -14.7%
```

The fresh runner therefore compresses early offensive-class opportunities substantially more strongly than historical P3 magnitude.

This does **not** fail the predeclared direction-only gate and must not be reverse-fit away.
It creates an explicit:

```text
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
```

Consequences:
- structural direction may be interpreted;
- exact Stage-delay magnitude must not be promoted to production authority.

---

# 4. Same-entered-Stage ATK direction

Independent same-state Stage pairs were used so cumulative judgment/progression phase drift could not contaminate this check.

Across 240 isolated pairs:

```text
ATK_OFF root actions = 1982
ATK_ON  root actions = 1750
net = -11.7053%
```

Across the 80 fixture/class/Stage/level groups:
- 65 decreased;
- 14 equal;
- 1 increased.

Exactly one pair-level exception was recorded:

```text
T3_CENTRAL
Archer Lv21
Stage30
seed307
ATK_OFF 5 root actions
ATK_ON  6 root actions
```

## 4.1 Why that exception is legitimate chronology

The Stage contains SPLITTER composition.
With more ATK, Archer kills the front SPLITTER one action earlier.
The two children spawn immediately and become live targets.
They then consume the remaining penetration target slots of the same root package, shielding rear enemies that would otherwise have been reached.
This produces one extra later root action.

The current production capability chain confirms the same ordering principle:
- SPLITTER death immediately inserts children into the live monster list;
- Archer penetration target selection occurs from the then-current live monster list after the primary damage path.

Therefore:

```text
MORE_ATK_CAN_RARELY_INCREASE_ROOT_WORK_VIA_DISCRETE_TARGET_CHRONOLOGY
```

This is not evidence that ATK usually increases EXP opportunity.
It is the exact kind of discrete chronology exception the contract required to expose rather than erase.

No fidelity gate was relaxed after results; the erroneous validator was aligned back to the already written contract while preserving the exception and identical runner output.

---

# 5. Fresh-forward progression result

The following Stage values are **diagnostic magnitude only** because of the explicit magnitude watch.
They are included to expose direction and accumulation, not to freeze exact acquisition Stages.

## 5.1 SHOP_OFF

| Class | Lv6 | Lv11 | Lv16 | Lv21 | Lv26 | Lv31 | mean root actions to stop |
|---|---:|---:|---:|---:|---:|---:|---:|
| Knight | 4.51 | 9.41 | 18.38 | 28.51 | 40.51 | 0/80 reached | 404.69 |
| Rogue | 4.58 | 12.05 | 20.00 | 28.27 | 38.91 | 1/80 at S50 | 421.05 |
| Tank | 4.42 | 9.04 | 14.28 | 20.30 | 29.57 | 80/80 mean 41.75 | 446.55 |
| Archer | 4.51 | 11.79 | 20.16 | 30.71 | 43.25 | 0/80 reached | 382.23 |
| Mage | 4.42 | 11.72 | 20.41 | 31.16 | 43.64 | 0/80 reached | 379.93 |

## 5.2 Diagnostic stagewise ATK_ON

| Class | Lv6 | Lv11 | Lv16 | Lv21 | Lv26 | Lv31 | mean root actions to stop |
|---|---:|---:|---:|---:|---:|---:|---:|
| Knight | 4.58 | 9.53 | 19.24 | 31.14 | 45.06 | 0/80 reached | 366.46 |
| Rogue | 4.64 | 12.60 | 21.40 | 30.80 | 43.23 | 0/80 reached | 378.94 |
| Tank | 4.47 | 9.20 | 14.71 | 21.48 | 31.98 | 80/80 mean 46.91 | 446.55* |
| Archer | 4.58 | 12.21 | 21.39 | 33.27 | 65/80 mean 47.11 | 0/80 reached | 350.03 |
| Mage | 4.47 | 12.16 | 21.48 | 33.70 | 75/80 mean 47.97 | 0/80 reached | 349.08 |

`*` Tank reaches the same provisional Lv31 threshold after approximately the same root-action budget; stronger ATK spreads that budget over more entered Stages. It does not mean ATK has no within-Stage effect—the isolated Stage test shows the opposite.

Approximate accumulated ATK_ON delay among milestones reached in both lanes:

```text
Knight: Lv16 +0.86 / Lv21 +2.63 / Lv26 +4.55 Stages
Rogue:  Lv11 +0.55 / Lv16 +1.40 / Lv21 +2.53 / Lv26 +4.32
Tank:   Lv16 +0.43 / Lv21 +1.18 / Lv26 +2.41 / Lv31 +5.16
Archer: Lv11 +0.42 / Lv16 +1.23 / Lv21 +2.56 / Lv26 +3.86 among reaches
Mage:   Lv11 +0.44 / Lv16 +1.07 / Lv21 +2.54 / Lv26 +4.33 among reaches
```

Again: these exact Stage deltas are **not production-authoritative**.
The robust evidence is the direction and accumulation.

---

# 6. Causal interpretation

The fresh model reproduces the same structural feedback identified by historical P4-B, now with current Lv26 structure and stagewise shop history present:

```text
offensive class skill / shop power
-> faster or broader enemy removal
-> fewer future root timing actions remain
-> fewer provisional EXP awards remain
-> later skill acquisition shifts later
```

This means pure per-root-action EXP is causally coupled to class removal efficiency.

Efficient removal classes can partially **self-starve their own progression opportunity**.
Tank, whose approved identity intentionally retains lower removal and emphasizes control/defense/wall protection, retains more timing-action opportunity and therefore accumulates provisional EXP faster under this baseline.

This is **not** evidence that:
- Tank damage should be nerfed or buffed;
- all classes should have equal kill throughput;
- class identity should be flattened to equalize EXP;
- hidden class-specific EXP multipliers should be introduced.

It is evidence that the EXP source itself remains structurally entangled with class combat efficiency.

Classification:

```text
PURE_PER_ROOT_ACTION_EXP_CLASS_PROGRESSION_DIVERGENCE = RECONFIRMED
TANK_FAST_PROGRESSION_SIGNAL = OPPORTUNITY_RETENTION_EFFECT, NOT DAMAGE_BALANCE DEFECT
```

---

# 7. Shop feedback remains bidirectional

Fresh-forward Lane A confirms the same-entered-Stage side:

```text
shop ATK
-> faster removal
-> generally fewer root timing actions
-> less provisional EXP opportunity
```

P6-B1 independently established the other side:

```text
shop ATK
-> can prevent failure
-> additional later Stages become reachable
-> more future timing actions become available
-> more total provisional EXP can be gained
```

Therefore the global relation remains:

```text
SHOP_ATK_TO_EXP_FEEDBACK = BIDIRECTIONAL / OUTCOME-CONDITIONED
```

A flat `shop power -> EXP delay` multiplier remains invalid.

---

# 8. Historical consistency

This result does not replace archived P4-B.
It independently reproduces its causal direction without fitting to its milestone outputs.

Historical P4-B already showed:
- offensive skill power removes timing-action opportunity;
- Tank can retain an early progression lead because control/defense removes less work;
- pure per-turn universal EXP conflicts with common shared milestone windows;
- simply inflating all Stage HP/count is not a complete structural fix.

P4-E and the user-approved R2 route therefore remain correct:

```text
pure per-valid-turn EXP = provisional diagnostic baseline only
final EXP semantics = OPEN
P10 multiplayer scaling baseline first
-> P10R mandatory EXP/timebase reconvergence
```

FRESH_FORWARD_P6 does not reopen or override that approved routing.

---

# 9. What is and is not closed

Closed by this execution:

```text
FRESH_FORWARD_P6 executable bounded model = BUILT
contract fidelity = PASS_WITH_REPORTED_CHRONOLOGY_EXCEPTION
exact-byte determinism = PASS
current structural self-damping direction = RECONFIRMED
stagewise diagnostic shop adds cumulative self-damping = CONFIRMED
old-P4B reverse-fit remains unnecessary/forbidden
```

Still open:

```text
exact Stage reach = NOT AUTHORITY
exact EXP thresholds/credits = OPEN
final EXP semantics = OPEN / deferred to P10R
full campaign survival-coupled progression = NOT modeled here
exact shop coefficients = OPEN
exact Lv26/Lv31 numeric production values = OPEN
Tier count = OPEN
monster availability/unlock ladder = OPEN
exact Tier1 roster = OPEN
exact Tier1 Stage1-50 authoring = NOT STARTED
```

Active new watch:

```text
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
```

---

# 10. P6 boundary after this result

P6-S1, P6-A, P6-B1 and P6-B2 now have sufficient evidence for a **P6 closure synthesis**.

However, the user approved the fresh-forward methodology/execution—not silent adoption of a new phase boundary.

Therefore this document does **not** automatically declare all of P6 closed and does not start Tier-count or monster-unlock adoption.

Next decision boundary:

```text
P6 CLOSURE SYNTHESIS
-> decide whether current causal convergence is sufficient to close P6 structurally
-> only if user approves, begin Tier-count / monster-availability / unlock-order candidate review
```

No Tier or monster-unlock choice is implied by this result.

---

# 11. Final classification

```text
P6_B2_FRESH_FORWARD = DIAGNOSTIC_COMPLETE_PASS_WITH_ABSOLUTE_MAGNITUDE_WATCH
PURE_PER_ROOT_ACTION_EXP_DIVERGENCE = STRUCTURALLY_RECONFIRMED
SHOP_ATK_SAME_STAGE_SELF_DAMPING = STRUCTURALLY_RECONFIRMED
SHOP_ATK_GLOBAL_EXP = BIDIRECTIONAL_OUTCOME_CONDITIONED
TANK_LOW_REMOVAL_IDENTITY = PRESERVED
FINAL_EXP_ROUTING = R2 / P10R UNCHANGED
P6_OVERALL_CLOSURE = USER_DECISION_PENDING
TIER_UNLOCK_AUTHORING = NOT STARTED
PRODUCTION = UNCHANGED
```
