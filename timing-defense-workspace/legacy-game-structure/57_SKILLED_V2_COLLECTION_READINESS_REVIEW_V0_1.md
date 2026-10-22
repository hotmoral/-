# Timing Defense — SKILLED_V2 Collection Readiness Review V0.1

Date: 2026-10-22 KST  
Status: **DESIGN-READY / OBSERVED-DATA BLOCKED / NO FITTED PROFILE**

Reviewed:
- `24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `56_SKILLED_V2_TRACE_COLLECTION_PIPELINE_V0_1.md`
- `data/skilled_v2_controlled_harness_v0_1.yaml`
- `data/skilled_v2_trace_schema_v0_1.yaml`
- `tools/validate_skilled_v2_harness.py`
- `tools/validate_skilled_v2_trace_dataset.py`
- `tools/summarize_skilled_v2_trace_dataset.py`

---

# 0. Review question

Is the planning/data contract sufficiently specified to begin collecting real controlled skilled-player traces without inventing numeric `SKILLED_V2` parameters?

## Verdict

**YES — COLLECTION DESIGN READY.**

But:

```text
SKILLED_V2_NUMERIC_FIT = BLOCKED_BY_NO_OBSERVED_TRACE_DATA
```

This is an evidence boundary, not a design defect.

---

# 1. H0–H5 coverage

The harness family covers the required independent questions:

- H0 clean timing/combo ceiling
- H1 sustained tempo degradation
- H2 durable rhythm + heavy/P×P behavior
- H3 target-turnover/reacquisition
- H4 stateful telegraph read/response
- H5 mixed-pressure transfer

The six contexts map one-to-one to:
`BASELINE / TEMPO / DURABLE / TURNOVER / STATEFUL / MIXED`.

No harness is allowed to modify campaign progression.

---

# 2. User anchors preserved

The machine-readable harness explicitly preserves:

- `oldSkilledTooWeak = true`
- `combo40OrdinarySkilledAchievable = true`
- non-T1 CENTRAL full-Tier clear upper-bound goal `0.60`

The 0.60 value is marked as a **post-fit game-difficulty gate**, not a player-fitting objective.

Therefore the design prevents the circular failure:

```text
want harder game
 -> intentionally fit weaker player
 -> declare difficulty solved
```

---

# 3. Campaign contamination prevented

`HARNESS_ONLY` explicitly disables:
- campaign attempt truth
- star effects
- Tier records
- permanent progression
- achievement/title effects
- shop economy
- persistent EXP/coin

This is necessary so calibration activity cannot accidentally become a progression exploit or pollute campaign telemetry.

---

# 4. Sequence-aware trace contract

The collection pipeline retains ordered:
- action timestamps
- judgments
- combo state
- heavy/P×P intent and completion
- target turnover
- no-target waiting
- stateful readable events
- tactical response

This supports context-conditioned sequence fitting rather than a single iid judgment vector.

---

# 5. Anti-overfit / anti-fabrication controls

Required controls now exist for:
- preserving raw event order
- splitting by player/session group
- transfer/holdout validation when sample size permits
- reporting sample size and uncertainty
- preventing single-trace fitting
- preventing combo40 from being classified as high-mastery-only by assumption
- preventing missing contexts from being filled with invented probabilities

If coverage is insufficient, the required outcome is:
`INSUFFICIENT_OBSERVED_TRACE_COVERAGE`.

---

# 6. Role-expression regression connected

After fitting, the all-20 representative encounter candidates must be rerun.

Strong player behavior is allowed to stop full monster activation after readable expression.
It is not allowed to silently reintroduce routine pre-expression deletion without review.

This ties player-model fitting back to the already-closed monster-role contract.

---

# 7. Trace dataset validation design

The dataset validator checks, among other things:
- known record/harness types
- required fields
- harness/context match
- action sequence ordering
- heavy/P×P logical relationships
- combo-break explanation
- H3 turnover evidence
- H4 stateful evidence
- H0 minimum action opportunity for combo40 evaluation
- per-harness completed-trace coverage

The summarizer is descriptive only and explicitly does not output a fitted profile.

---

# 8. Remaining evidence blocker

No observed H0–H5 player dataset currently exists in the canonical planning corpus.

Therefore it would be invalid now to freeze:
- PERFECT/GOOD/NORMAL/MISS probabilities
- action cadence distributions
- combo40 probability
- heavy/P×P completion rates
- turnover reacquisition delay
- stateful response latency
- pressure degradation
- `SKILLED_V2_CONSERVATIVE/CENTRAL/STRONG` numeric parameters

---

# 9. Next executable boundary

The next evidence-producing step requires one of:

1. an explicitly isolated playable `HARNESS_ONLY` implementation using the same timing/judgment semantics, or
2. an equivalent controlled telemetry source producing the canonical trace schema.

A playable harness implementation must remain separate from production campaign progression and must not modify live v0.45 behavior until explicitly authorized/deployed.

---

# 10. Admission result

```text
HARNESS_SPECIFICATION = READY
TRACE_SCHEMA = READY
DATA_VALIDATION_PIPELINE = READY_BY_DESIGN
OBSERVED_TRACE_DATA = MISSING
NUMERIC_PLAYER_MODEL_FIT = NOT_AUTHORIZED_BY_EVIDENCE
```

The project should now stop inventing analysis-only skilled brackets and collect evidence.
