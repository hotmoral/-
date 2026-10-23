# Timing Defense — P5 SKILLED_V2 Late-Run Reinterpretation & P5→P6 Fidelity Gate V0.1

Date: 2026-10-23 KST  
Status: **DIAGNOSTIC RESULT / PRIOR ALL-PERFECT INTERPRETATION CORRECTED / P5→P6 USER DECISION REQUIRED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `66_SKILLED_V2_CENTRAL_DESIGN_PRIOR_AND_HARNESS_CLOSURE_AMENDMENT_V0_1.md`
- `67_SKILLED_V2_CENTRAL_SEQUENCE_MODEL_V0_1.md`
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `137_P5_STAGE46_49_EXACT_EXECUTION_STAGE_SETTLED_BOUNDARY_RESULT_V0_1.md`
- `142_P5_STAGE48_FODDER_CHAIN_AND_GLOBAL_STANDOFF_BOUNDARY_RESULT_V0_1.md`

Production remains unchanged and unauthorized for gameplay/numerical modification.

---

## 1. Why this diagnostic was required

The user asked whether the recent Stage46–49 / Stage48 results represented realistic skilled play or all-PERFECT timing.

Source review showed that the current P5 late-run simulator had been using an idealized timing input:

```text
ordinary root attack -> PERFECT
successful Heavy     -> CRITICAL
missed_heavy_indices -> empty in current chains
```

Therefore the recent Stage46–49 survival/reserve results must be interpreted as an **all-PERFECT / effectively all-P×P upper-bound diagnostic**, not as the `SKILLED_V2_CENTRAL` baseline.

`BALANCED` in those runs referred to the shop allocation profile, not player timing mastery.

This reinterpretation does not invalidate geometry, chronology, class-role, proxy-contamination, or standoff-coupling findings. It changes the mastery authority of the survival/reserve numbers.

---

## 2. SKILLED_V2_CENTRAL model used

Canonical candidate:

`data/skilled_v2_central_sequence_candidate_v0_1.yaml`

It is a deterministic, streak-aware two-state Markov design prior, not empirical telemetry.

Long-run intended marginal:

```text
PERFECT 0.70
GOOD    0.20
NORMAL  0.10
```

Heavy consumes two judgment events.
Approved Heavy mapping remains:

```text
P+P -> CRITICAL
weight >= 3 -> SUPER
weight == 2 -> GREAT
weight == 1 -> HEAVY+
else -> HEAVY
```

Only `P+P CRITICAL` owns the Lv31 final package under the approved Stage46+ mastery-gate direction.

No MISS/INVALID probability was invented for this diagnostic because the central candidate does not assign one.

---

## 3. First 3-seed screen — preliminary only

Temporary run:

```text
run id 39967871595
```

The result strongly suggested that realistic P×P frequency materially changes late-run survival, but it was not used as the final quantitative screen because:
- only three base seeds were used;
- the old P5 simulator's `basic_knock()` did not explicitly recognize `HEAVY+`, so that tier fell through to the lowest knockback branch.

The compatibility issue was corrected before the expanded screen:

```text
HEAVY+ knockback = 0.013
```

matching the authoritative timing-tier map.

---

## 4. Expanded 20-seed SKILLED_V2 comparison

Temporary run:

```text
run id 39968100989
repeat determinism = PASS
SHA256 = ec4ed61d8288b9a2bb2e1575bf5f8d4e1191fdbabcae9a5d11cae9b7cde8d6c9
```

Conditions held fixed:
- same current diagnostic Stage48 center: `3 spatial armored proxy + 2 GRUNT + 1 SIEGER`;
- global SIEGER standoff `0.38`;
- BALANCED shop snapshot;
- right-edge spawn `x=0.92`;
- Stage46→49 wall deficit carried;
- no class/monster/shop stat change;
- 20 deterministic base seeds × five classes = 100 central-skilled cases;
- one persistent SKILLED_V2 judgment stream across Stage46→49 within each class/seed;
- P+P alone triggers the Lv31 final package.

### Realized input distribution

Across realized judgments before attempts ended:

```text
PERFECT 72.3672%
GOOD    18.4456%
NORMAL   9.1871%
```

Realized Heavy tiers:

```text
CRITICAL 1919
SUPER     639
GREAT     491
HEAVY+    209
HEAVY      47
```

Realized P×P / CRITICAL share among Heavy:

```text
~58.0635%
```

This is consistent enough with the stateful central design prior for the present causal diagnostic.

### All-PERFECT control

Same current candidate under the old idealized timing input:

```text
5/5 classes survive through Stage49
Stage48 SIEGER shots = 0 for all five
final wall:
  Knight 2320.0
  Rogue  2320.0
  Tank   2320.0
  Archer 1957.3
  Mage   2320.0
```

### SKILLED_V2_CENTRAL screen

```text
45 / 100 survive/settle through Stage49
55 fail or fail to settle through the chain
```

Failure location:

```text
Stage46: 26
Stage47: 21
Stage48:  0
Stage49:  8
```

Per-class through-Stage49 count:

```text
Knight  3/20
Rogue   4/20
Tank    2/20
Archer 18/20
Mage   18/20
```

Stage48 was therefore **not the primary failure source** under central skilled timing. Most failures occurred before the Stage48 candidate was reached.

Archer occasionally allowed SIEGER shots at old `0.38` under weaker-than-perfect clearing, but that fact does not rescue the overall chain because upstream Stage46/47 behavior is already class-skewed.

---

## 5. Factor isolation — what actually causes the skilled regression

Temporary run:

```text
run id 39968400953
repeat determinism = PASS
SHA256 = 1ae220cb0bbebd388f9c014a9208335c4b8eeb895b4163109e78895f95b4a420
```

20 seeds × five classes, Stage46→47 only.

Four modes were compared:

### A. ALL_PERFECT
Ordinary = PERFECT, Heavy = P×P/CRITICAL.

```text
5/5 class controls through Stage47
```

### B. CENTRAL_NORMAL_ONLY
Ordinary judgments follow central skilled stream, but every Heavy is forced P×P/CRITICAL.

```text
100/100 through Stage47
Knight 20/20
Rogue  20/20
Tank   20/20
Archer 20/20
Mage   20/20
```

### C. CENTRAL_HEAVY_ONLY
Ordinary attacks are forced PERFECT, while Heavy P×P frequency follows the central skilled stream.

```text
63/100 through Stage47
Knight 12/20
Rogue  11/20
Tank    0/20
Archer 20/20
Mage   20/20
```

### D. CENTRAL_FULL
Both ordinary and Heavy judgment quality follow the central skilled stream.

```text
58/100 through Stage47
Knight 10/20
Rogue   9/20
Tank    0/20
Archer 20/20
Mage   19/20
```

### Causal conclusion

```text
ORDINARY_NONPERFECT_QUALITY_ALONE != PRIMARY_FAILURE_CAUSE
REDUCED_PXP_LV31_FINAL_FREQUENCY = DOMINANT_CURRENT_SENSITIVITY
```

The current late-run pressure model is strongly dependent on nearly every Heavy producing P×P / Lv31 final output.

Tank is the most severe directional anomaly: its intended survival/control identity is not visible under the central Heavy-frequency screen, because 0/20 reached the end of Stage47 even with ordinary attacks forced PERFECT.

This is a cause-classification result, not authorization to buff Tank or nerf Stage46.

---

## 6. Simulator-fidelity limitation discovered

The exact percentages above are **not yet balance-authoritative** for final late-run tuning.

Approved P1 lifecycle semantics require within one Tier attempt:
- combo persists across Stage/shop/target-wait downtime;
- charge persists across Stage/shop/intermission;
- an in-progress Heavy resolves before Stage completion.

The current P5 Stage46→49 integrated runner was designed as an identity/shop/chronology diagnostic and does not carry the full canonical run-action state:
- stage-local attack numbering effectively recreates Heavy cadence inside each Stage;
- full persistent combo state is not carried through the four-Stage chain;
- combo damage bonuses and N3 milestone effects are not integrated as the full P3 persistent-run action pipeline;
- it therefore cannot yet be the final authority for central-skilled survival probability.

The P3 persistent kernel already models:
- persistent combo;
- persistent charge;
- SKILLED_V2 judgment RNG/state;
- Heavy as `charge >= 3` with two judgments;
- combo damage bonus;
- N3 milestone triggers;
- deterministic run-state continuity.

But the P3 kernel does not by itself contain the full P4-D2 Lv31 packages + P5 shop + current Stage46–49 encounter/STAGE_SETTLED model.

Therefore there is currently no single runner with all required authority layers combined.

---

## 7. Dependency-order interpretation

The active dependency plan defines:

```text
P3 persistent run kernel
-> P4 player-power spine
-> P5 coin/shop candidate
-> P6 JOINT RUN-POWER CONVERGENCE
```

P6 exists specifically to repeat on paired deterministic seeds:

```text
EXP/skill candidate
-> shop candidate
-> Stage pressure
-> resulting event count
-> revised skill reach
```

and explicitly measures timing-event count, wall trajectory, clear/fail slope, shop leverage, and combo40 opportunity.

The new SKILLED_V2 evidence therefore matches the intended P6 coupling problem more closely than a local Stage48 scalar-tuning problem.

However this document does **not** unilaterally declare P5 closed or P6 started.
That work-boundary transition is an important project decision and requires user approval.

---

## 8. What remains valid from Stage48 work

The following causal findings remain useful and are not invalidated by the mastery reinterpretation:
- old repeated proxy packet was contaminated and rejected;
- simple BRUTE/SHIELD screens were insufficient;
- lower armored spatial density helps Archer-screen longevity;
- GRUNT-like cheap-target layering can delay Mage chain access to SIEGER;
- type/order/arrival phase matter more than indiscriminate fodder count;
- large global SIEGER standoff advancement creates cross-stage damage and is not the current repair direction;
- `limited armored/hardened frontline + cheap target layer` remains the most promising Stage48 chronology family.

What is **not** currently valid as a final balance conclusion:
- exact Stage46→49 survival percentages derived from all-PERFECT play;
- exact central-skilled survival percentages from the current P5 diagnostic runner;
- any exact armored stat/count/timing;
- any exact SIEGER standoff value;
- any class buff/nerf derived from the current late-run chain.

---

## 9. User decision gate

### Option A — RECOMMENDED
Pause exact Stage48 micro-tuning and open a bounded **P5→P6 fidelity bridge**:
- combine P1/P3 persistent combo+charge+judgment state;
- preserve P4-D2 Lv31 P×P packages;
- preserve P5 shop snapshot/attribution;
- preserve Stage46→49 right-edge/STAGE_SETTLED encounter semantics;
- compare ALL_PERFECT and SKILLED_V2_CENTRAL on paired deterministic seeds;
- then resume Stage48 armored+fodder tuning only against the contract-faithful skilled baseline.

This does not yet close P5 or numerically start full P6 convergence. It creates the minimum faithful runner needed to decide that boundary safely.

### Option B
Continue local Stage48 armored/fodder chronology tuning on the current P5 runner and defer the full mastery/run-state fidelity issue.

Risk: exact Stage48 tuning may be optimized against the wrong late-run player-power surface and need rework.

### Option C
Formally close P5 now and immediately enter full P6 convergence.

Risk: this may skip a useful narrow bridge/admission step and makes the phase boundary larger than necessary.

Recommendation: **A**.

Reason:
- it follows the canonical repair order `fidelity -> lifecycle/state -> chronology -> exact scalar`;
- it preserves already-learned Stage48 chronology evidence;
- it avoids premature class/monster buffs based on an all-P×P artifact;
- it matches the documented purpose of P6 without claiming P5 is already numerically complete;
- it is the smallest reversible step.

Stop here for explicit user approval before adopting the P5→P6 work-boundary direction.
