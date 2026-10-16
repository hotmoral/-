# ReceiptLedger — Product / Validation Roadmap

Updated: 2026-10-17 KST

## 1. Completed V1 chain

CP20–CP36 is complete. CP36 fixed the measured SQLite search bottleneck and left real-image OCR/review behavior for physical validation.

## 2. CP37 — Physical Device / Real-Image OCR Validation — IN PROGRESS

### Phase A — validation instrumentation

Completed. Added privacy-safe debug reporting without changing OCR behavior.

### Remediation A — false item row / recoverability

Triggered by the first physical sample. Added a narrow pre-date false-item gate and explicit non-product item removal. Same-receipt physical retest confirmed the triggering false address/header row no longer appeared.

### Review Coverage Instrumentation

A later same-receipt retest showed only 1 of 15 items selected for review while several item corrections were needed. Report schema v2 added:

- `corrections_outside_review_items`
- `review_scope_miss`

Physical v2 metric check confirmed `review_scope_miss=1` with 2 corrected item ordinals outside the initial review set.

### Remediation C — Partial Row Prefill — READY_FOR_PHYSICAL_PREFILL_RETEST

The same receipt repeatedly showed the first item with blank quantity and unit price across validation builds.

Source analysis found a bounded `ItemTupleSolver` gap: multiple printed money values plus a missing quantity token discarded a usable printed unit candidate.

Remediation C pre-fills quantity/unit price only for a unique exact integer relation while keeping the row `PARTIAL`, so explicit review remains required.

Frozen executable:

- `01b22652a45889b6bfaa474131e0c5fa7f19e96e`
- run `38979684033` SUCCESS
- artifact `12080029714`
- APK SHA-256 `65fe0827f3a9ebfeafbbf783c6c8f82544f8594203008692288ab74ec9eb1e0e`
- version `1.0.38-partial-row-prefill-validation` / 39

## 3. Current decision path

1. Re-run the same receipt using Remediation C.
2. Verify the first item quantity/unit price are prefilled.
3. Verify that item is still explicitly review-required.
4. Analyze the returned report v2.
5. Only after this passes, begin the independent 10-receipt campaign.
6. Aggregate correctness, false-auto-confirm, review-scope misses, correction burden, save reliability and latency.
7. Then decide whether any further OCR/review remediation is justified.

Repeated diagnostic/remediation samples do not count toward the final 10 independent receipts.

## 4. Decision priority

1. correctness / false-auto-confirm safety;
2. selective-review coverage;
3. save/provenance reliability;
4. review burden;
5. latency.

`false_auto_confirm=1` is whole-receipt trust failure evidence.

`review_scope_miss=1` means at least one corrected item was outside the selected item-review scope.

## 5. Scope discipline

Do not add generic OCR character substitutions from one receipt. The repeated package-suffix character confusion is evidence to track, not yet a justified normalization rule.

Do not promote arithmetic prefill to an auto-confirm path. Remediation C deliberately keeps the recovered item PARTIAL/review-required.

## 6. Frozen authority gates

Still authoritative:

- stable catalog ID final identity authority;
- commodity grouping != comparability;
- CP27/28 price contracts;
- CP29 discovery contract;
- Remediation A false-item gate;
- report v2 review-coverage semantics;
- product schema 2 / receipt schema 1;
- offline/no broad permission posture.

## 7. Current stop

**Await same-receipt Remediation C physical confirmation before the independent 10-receipt campaign.**
