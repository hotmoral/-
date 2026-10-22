# Timing Defense — SKILLED_V2 Central Sequence Model V0.1

Date: 2026-10-22 KST  
Status: **PROVISIONAL CENTRAL SIMULATION CANDIDATE / STRUCTURAL VALIDATION PASS / NOT PRODUCTION FROZEN**

Depends on:
- `66_SKILLED_V2_CENTRAL_DESIGN_PRIOR_AND_HARNESS_CLOSURE_AMENDMENT_V0_1.md`
- `data/skilled_v2_central_sequence_candidate_v0_1.yaml`
- `tools/validate_skilled_v2_central_sequence.py`

---

## 0. Decision being implemented

The current campaign-modeling gate no longer waits for ordinary-skilled population telemetry.

The user-approved provisional central marginal judgment mix is:

- PERFECT 70%
- GOOD 20%
- NORMAL 10%

This remains a **design prior**, not measured population telemetry.

A direct iid 70/20/10 draw is rejected because it would make long PERFECT streaks structurally inconsistent with the existing anchor that combo40 is ordinarily achievable when a skilled player concentrates.

---

## 1. Candidate structure

V0.1 uses two latent player states.

### FOCUS

Interpretation:
> the skilled player has entered a sustained concentration rhythm.

Judgments:
- PERFECT 100%

State persistence:
- stay FOCUS: 98%
- leave to BASE: 2%

Implied mean FOCUS run length:
- 50 judgment events

### BASE

Interpretation:
> ordinary skilled play outside a sustained concentration run.

Judgments:
- PERFECT 50%
- GOOD 33.333...%
- NORMAL 16.666...%

State persistence:
- stay BASE: 98.666...%
- enter FOCUS: 1.333...%

Implied mean BASE run length:
- 75 judgment events

The stationary state split is exactly:
- FOCUS 40%
- BASE 60%

Therefore the implied long-run marginal is exactly:

```text
PERFECT = 0.40 × 1.00 + 0.60 × 0.50 = 0.70
GOOD    = 0.40 × 0.00 + 0.60 × 1/3  = 0.20
NORMAL  = 0.40 × 0.00 + 0.60 × 1/6  = 0.10
```

---

## 2. Determinism

Simulation must remain replayable.

V0.1 therefore uses a fixed `XORSHIFT32` PRNG with an explicit integer seed.

Same:
- model version
- seed
- judgment count

must produce the same state sequence and judgment sequence.

Randomness here represents bounded simulation variation, not nondeterministic production behavior.

---

## 3. Structural validation

A local-equivalent deterministic probe of the committed model parameters was run before admission.

### Long-run marginal probe

Configuration:
- 100 seeds
- 10,000 judgments per seed
- 1,000,000 judgment events total

Observed approximation:
- PERFECT: 69.9729%
- GOOD: 20.0121%
- NORMAL: 10.0150%
- FOCUS occupancy: 39.9384%

This is consistent with the exact stationary target 70/20/10.

### Combo diagnostic

Configuration:
- seeds 1..5000
- 100 judgment events per seed

Observed diagnostic:
- combo40 reached in approximately 58.86% of 100-judgment windows

This percentage is **not** a production target and is not frozen.
It is retained only as evidence that V0.1 does not accidentally turn combo40 into a high-mastery-only event.

---

## 4. What this model does not yet specify

V0.1 deliberately does **not** invent values for:
- target-turnover degradation
- no-target recovery penalty
- encounter-density degradation
- MISS probability
- INVALID probability
- conservative skilled bracket
- strong skilled bracket
- production clear-rate distribution

Those are separate layers.

The user's observed H0/H3 traces remain a high-mastery upper-tail anchor and are not mixed into this central model.

---

## 5. Timing/cadence boundary

This candidate specifies **judgment sequence behavior**, not a new timing-square mechanic.

Do not change:
- timing-square size
- PERFECT-zone size
- line speed
- Heavy input semantics

merely to make this model fit.

Existing analysis-bracket action intervals (`900/750/600 ms`) remain historical sensitivity-probe values and are not promoted by this document to fitted skilled cadence.

The next encounter integration must use the current gameplay timing semantics or explicitly label any retained cadence value as a bounded simulation control rather than player-skill truth.

---

## 6. Heavy / P×P semantics

The existing authoritative combat simulation treats Heavy as consuming two judgment events.
V0.1 preserves that rule.

Therefore:
- a Heavy may consume two consecutive outputs from the sequence model;
- `PERFECT + PERFECT` remains the P×P / CRITICAL case under existing mechanics;
- Heavy/P×P is not given a separate fabricated success probability in this model.

---

## 7. Admission result

Decision:

> **PASS AS PROVISIONAL `SKILLED_V2_CENTRAL` SEQUENCE CANDIDATE FOR DOWNSTREAM SIMULATION.**

This means it may now be injected into representative encounter analysis.
It does **not** mean production skill balance is frozen.

---

## 8. Exact next boundary

Next work:

1. add an isolated integration path that feeds this seeded judgment stream into the existing class-aware role/encounter simulator without deleting the historical trace brackets;
2. keep production timing geometry unchanged;
3. run the 20 representative encounter set across all 5 classes and multiple deterministic seeds;
4. compare:
   - role-expression survival
   - wall damage
   - clear time / failure
   - combo peaks
   - Heavy/P×P outcomes
   - target reorder exposure
5. determine whether any previously PASS role becomes structurally invalid under the central skilled sequence;
6. only after that proceed to synthetic multi-stage/Tier calibration.

No production gameplay deployment is authorized by this document.
