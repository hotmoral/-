# ReceiptLedger V1 — CP20 Dependency Gates

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`

## Purpose

Prevent later groups from skipping prerequisites and creating avoidable rework.

## Gates

### Gate A — before persistence implementation

CP21 must freeze:

- identity boundaries
- specification semantics
- sales-unit/form semantics
- category references
- alias context
- provenance/confirmation states
- legacy compatibility rules

No CP22 schema implementation should begin while those meanings are still moving.

### Gate B — before automatic identity linking expands

CP23 must provide structured semantic candidates with provenance.
CP24 must define evidence authority and ambiguity behavior.

No fuzzy/semantic similarity may become silent merge authority merely because ranking exists.

### Gate C — before price judgment UI

CP27 must define a single observation-eligibility/comparability contract and deterministic statistics.
CP28 must define data sufficiency and label thresholds.

No UI should independently invent `싸다/비싸다` rules.

### Gate D — before final product-centric shell

Search/browse and detail data contracts must exist before CP34 relies on them.
Design System must not force domain/storage rewrites.

### Gate E — before declaring V1 quality

CP35 must measure end-to-end purchase-registration correctness.
CP36 must verify representative scale/reliability.

## General rule

A gate may be revised only by an explicit later canonical decision that explains why the dependency changed. Do not bypass gates implicitly for convenience.
