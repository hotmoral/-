# ReceiptLedger — Product / Validation Roadmap

Updated: 2026-10-17 KST

## 1. Completed V1 chain

CP20–CP36 is complete.

## 2. CP37 — Physical Device / Real-Image OCR Validation — IN PROGRESS

### Phase A

Debug-only physical validation instrumentation completed.

### Remediation A

False address/header item physically reproduced, then fixed with narrow pre-date gating and explicit non-product item removal. Triggering sample physically passed the retest.

### Review-Coverage Instrumentation

Report v2 added:

- `corrections_outside_review_items`
- `review_scope_miss`

Physical metric check confirmed a real review-scope miss while `false_auto_confirm=0`.

### Remediation C

Repeated same-receipt evidence showed the first reviewed item with blank quantity and unit price. A narrow exact-integer arithmetic prefill was added while keeping the item PARTIAL/review-required.

Physical retest: **C failed its intended prefill objective**. The item remained review-required, so safety was preserved.

### Remediation D — Candidate Structure Diagnostics

Current state: **READY_FOR_PHYSICAL_DIAGNOSTIC_RETEST**.

D adds no solver/review/OCR behavior. It appends a sanitized `RL_CP37_DIAG version=1` line for the first initially reviewed item so the physical candidate structure can be observed before another remediation is attempted.

Frozen executable:

- `3e19741521b9be4039028bcb9981e400ff2ad867`
- run `38987300764` SUCCESS
- artifact `12083716548`
- APK SHA-256 `1aa0f2d6ec2510b77a7b273eefd2b037ae8f0207021849c7da81ac054cb125e9`
- version `1.0.39-candidate-diagnostics-validation` / 40

## 3. Current decision path

1. Run the same diagnostic receipt once with `ReceiptLedger 검증 D`.
2. Obtain both `RL_CP37_SAMPLE version=2` and `RL_CP37_DIAG version=1`.
3. Determine whether the blank-field defect is caused by:
   - a product-name-zone quantity candidate;
   - multiple/ambiguous money candidates;
   - another candidate geometry pattern.
4. Only after cause is proven, define the smallest remediation.
5. Re-run the same diagnostic receipt once.
6. Only after the defect is closed resume the independent 10-receipt campaign.

## 4. Priority

1. correctness / false-auto-confirm safety;
2. selective-review coverage;
3. deterministic structural recovery;
4. save/provenance reliability;
5. review burden;
6. latency.

## 5. Frozen authority gates

Still authoritative:

- stable catalog ID final identity authority;
- grouping != comparability;
- CP27/28 price contracts;
- CP29 discovery contract;
- product schema 2 / receipt schema 1;
- offline/no broad permission posture;
- no OCR/text substitution from one sample;
- no new solver heuristic before D physical diagnostics identify the cause.

## 6. Current stop

**Await one same-receipt `RL_CP37_DIAG version=1 ...` result before further implementation.**
