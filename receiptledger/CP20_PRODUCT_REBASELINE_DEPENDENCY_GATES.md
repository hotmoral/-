# ReceiptLedger V1 — CP20 Dependency Gates

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## Purpose

Prevent later groups from skipping prerequisites and creating avoidable rework.

## Gates

### Gate A — before persistence implementation

CP21 must freeze:

- identity boundaries;
- specification semantics;
- sales-unit/form semantics;
- category references;
- alias context;
- provenance/confirmation states;
- legacy compatibility rules.

No CP22 schema implementation should begin while those meanings are still moving.

### Gate B — before automatic identity linking expands

CP23 must provide structured semantic candidates with provenance.
CP24 must define evidence authority and ambiguity behavior.

CP24 must measure both false merge and false split/identity fragmentation. False merge remains the higher-severity safety failure, but unresolved fragmentation must not be accepted as success merely because no merge occurred.

CP23/CP24 must also measure materially relevant automatic-success, review-required and repeat-confirmation reuse rates. No fuzzy/semantic similarity may become silent merge authority merely because ranking exists.

### Gate C — before price judgment UI

CP27 must first define the canonical comparison price and observation eligibility/comparability contract, then deterministic statistics.

The comparison-price contract must cover quantity > 1, line amount vs per-unit/package amount, item-specific discount, unallocated receipt-level discount/coupon, provenance and invalid/incomplete observations.

CP28 must define data sufficiency and label thresholds.

No UI should independently invent `싸다/비싸다` rules or silently choose a different price basis.

### Gate D — before final commercial detail screens

CP29 must freeze search/browse data access and interaction requirements.

CP30 Design System Foundation must precede final commercial visual implementation of CP31 Product Detail and CP32 Commodity Detail.

The Design System may not force domain/storage rewrites.

### Gate E — before final product-centric shell

CP31/CP32 detail behavior and CP33 Capture/Review UX contracts must exist before CP34 integrates the final shell.

CP33 must retain the principle `영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장` and must measure review burden/repeat-use automation where materially affected.

### Gate F — before declaring V1 quality

CP23–CP26 must already have local quality evidence for the failure modes they introduce.

CP35 then measures end-to-end purchase-registration correctness and aggregates those local metrics; it is not the first quality checkpoint.

CP36 verifies representative scale/reliability.

## General rule

A gate may be revised only by an explicit later canonical decision that explains why the dependency changed. Do not bypass gates implicitly for convenience.
