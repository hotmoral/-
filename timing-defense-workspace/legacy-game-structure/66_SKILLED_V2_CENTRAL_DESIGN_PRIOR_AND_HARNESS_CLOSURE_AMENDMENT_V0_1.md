# Timing Defense — SKILLED_V2 Central Design Prior & Harness Closure Amendment V0.1

Date: 2026-10-22 KST  
Status: **USER-AUTHORIZED DESIGN PRIOR / NOT EMPIRICAL POPULATION FIT / HARNESS PILOT CLOSED FOR CURRENT DECISION GATE**

Depends on:
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `61_HIGH_MASTERY_PLAYER_ANCHOR_AMENDMENT_V0_1.md`
- `63_HIGH_MASTERY_H0_OBSERVED_TRACE_REPORT_V0_1.md`
- `64_HIGH_MASTERY_H3_OBSERVED_TRACE_REPORT_V0_1.md`
- `65_HIGH_MASTERY_H4_OBSERVED_TRACE_INSTRUMENTATION_AUDIT_V0_1.md`

---

## 0. Decision

The user authorizes the project to stop treating ordinary-skilled population measurement as a blocker for the current campaign-modeling gate.

For provisional `SKILLED_V2_CENTRAL` modeling, use the following user-approved design prior for valid ordinary timing judgments:

- PERFECT: **70%**
- GOOD: **20%**
- NORMAL: **10%**

This is a **design prior**, not an empirically measured population estimate.

It may be used to continue simulation, encounter stress analysis, and campaign calibration work, provided the interpretation boundary below is preserved.

---

## 1. Interpretation boundary

The 70/20/10 vector is the provisional central **marginal judgment mix** for an ordinary skilled player under the current timing mechanic.

It must not be represented as:
- a measured percentile of the player population;
- a claim that the observed high-mastery user performs at 70/20/10;
- a production telemetry result;
- an independent per-input Bernoulli/iid model.

The observed user traces remain classified separately as `HIGH_MASTERY_STRESS_CANDIDATE` evidence.

No attempt should be made to weaken the high-mastery traces to fabricate ordinary-skilled data.

---

## 2. Sequence / combo constraint

Existing canonical design states that combo 40 is readily achievable for an ordinary skilled player when concentrating and must not be modeled as a rare high-mastery-only event.

Therefore the 70/20/10 marginal vector **must not** be implemented by independently drawing PERFECT with probability 0.70 on every action.

Reason:
- an iid 0.70 PERFECT process would make long PERFECT streaks, including combo 40, unrealistically rare;
- that would contradict the existing combo design anchor even while matching the aggregate 70/20/10 ratio.

The provisional `SKILLED_V2_CENTRAL` model must therefore be **stateful / streak-aware**.

At minimum it must permit:
- sustained focused PERFECT runs;
- ordinary GOOD/NORMAL errors outside those runs;
- recovery back into a focused run after an error;
- an aggregate long-run mix centered on 70/20/10 without forcing each short window to match that ratio exactly.

Exact transition coefficients are not frozen by this amendment.

---

## 3. MISS / INVALID treatment

The user-approved 70/20/10 vector sums to 100% and is therefore interpreted as the mix among ordinary valid timing judgments.

This amendment does **not** assign a baseline population percentage to MISS or INVALID.

MISS/INVALID may still arise from separately modeled encounter conditions such as:
- target unavailability;
- target turnover timing;
- interruption/lockout;
- player failure to produce a valid input opportunity;
- future mechanics that explicitly create such states.

Do not invent a baseline MISS share merely to complete a four- or five-way probability vector.

---

## 4. H0/H3/H4 disposition

Current user traces establish an upper-tail anchor, not ordinary-skilled center:

- H0: accepted as high-mastery clean timing evidence;
- H3: accepted as high-mastery turnover/reacquisition evidence;
- H4: runtime/state-event wiring valid, but reaction-latency skill fit not admitted because the current implementation confounds ordinary attack rhythm with tactical response.

The current personal harness pilot is closed for the present decision gate.

Do not require the user to continue H1/H2/H5 merely to unlock campaign modeling.

H4 is not a required ordinary-skilled calibration dimension under the current gameplay rule because the player uses the same timing-square input method whether or not the monster is in a telegraphed state. Stateful monster readability remains primarily a monster role-expression / encounter-structure concern unless a future production mechanic introduces a genuinely distinct player response rule.

---

## 5. Next modeling boundary

Next work should convert the user-approved 70/20/10 central prior into a deterministic, streak-aware `SKILLED_V2_CENTRAL` simulation candidate and test it against existing structural anchors before using it for campaign calibration.

Required checks before admission:

1. aggregate judgment mix remains centered on 70/20/10 over sufficiently long runs;
2. combo 40 remains ordinarily achievable rather than high-mastery-only;
3. the model is deterministic/replayable for simulation;
4. target-turnover and encounter-pressure effects are modeled as context effects, not by shrinking the timing square or arbitrarily increasing line speed;
5. production timing-square geometry and speed remain unchanged for this calibration step;
6. high-mastery observations remain a separate upper-tail stress anchor.

After those checks, the project may proceed to:

- rerun representative encounter/role-expression analysis under the provisional fitted-central candidate;
- run synthetic multi-stage/Tier calibration;
- evaluate clear/failure/star distributions;
- apply the existing non-T1 central clear-rate gate.

---

## 6. Deferred idea — boss weak-point burst

Keep as a future boss-design idea only; do not mix into current calibration:

> During a late-tier boss weak-point exposure phase, line speed may increase substantially while the PERFECT zone expands to occupy most of the timing square, turning the mechanic into a short high-frequency multi-hit reward window rather than a precision punishment.

This is not a current production rule and no numeric values are frozen here.

---

## 7. Non-goals

This amendment does not freeze:
- conservative/strong skilled brackets;
- exact state-transition coefficients for the central model;
- exact combo40 reach probability;
- production encounter coefficients;
- production boss timing mechanics;
- future telemetry-based re-fitting.

If later real-player evidence becomes available, this design prior may be revised. Until then it is sufficient authority to continue the current simulation/campaign-design lane.