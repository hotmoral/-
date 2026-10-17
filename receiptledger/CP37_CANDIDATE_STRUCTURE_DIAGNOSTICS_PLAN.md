# ReceiptLedger CP37 — Candidate Structure Diagnostics Plan

Updated: 2026-10-17 KST

## 1. Trigger

Remediation C preserved review safety but failed its physical objective on the repeated same receipt: the first reviewed item still showed blank quantity and unit price while line amount remained present.

This means the physical row did not satisfy the Remediation C assumption (`no quantity candidates` plus exactly one valid preceding printed unit candidate). Do not add another recovery heuristic before observing the candidate structure.

## 2. Goal

Add debug-only, privacy-preserving diagnostics that explain why the first initially reviewed item did not enter the unique-integer prefill path.

No receipt text, product name, numeric value, OCR token, date, store, ID, file path, or coordinate is emitted.

## 3. Diagnostic line

Keep `RL_CP37_SAMPLE version=2` unchanged.

Append a separate line:

`RL_CP37_DIAG version=1 target=FIRST_REVIEW_ITEM available=1 money_candidates=N quantity_candidates=N quantity_before_first_money=N quantity_between_money=N quantity_after_line=N exact_arithmetic_pairs=N integer_unit_pairs=N solver_resolution=... solver_reason=...`

Definitions:

- `money_candidates`: non-negative MoneyCandidate count on the target row.
- `quantity_candidates`: QuantityCandidate count on the target row.
- `quantity_before_first_money`: quantity candidates geometrically left of the leftmost money candidate.
- `quantity_between_money`: quantity candidates from the leftmost money candidate through the line-amount candidate.
- `quantity_after_line`: quantity candidates right of the rightmost money candidate.
- `exact_arithmetic_pairs`: current solver-compatible printed unit × printed quantity = printed line combinations.
- `integer_unit_pairs`: preceding printed money candidates whose exact line/unit ratio is an integer quantity 1..99, ignoring recognized quantity candidates.
- `solver_resolution` and `solver_reason`: sanitized enum/reason tokens only.

If there is no initially reviewed item or target lookup fails, emit `available=0` with zero counts and `UNKNOWN` tokens.

## 4. Decision matrix

The main physical hypothesis is supported if:

- `quantity_candidates > 0`,
- `quantity_before_first_money > 0`,
- `exact_arithmetic_pairs = 0`, and
- `integer_unit_pairs = 1`.

That combination indicates a product-name-zone numeric token is likely blocking the otherwise unique arithmetic recovery path.

Other outputs remain evidence; no remediation is authorized until the same physical receipt produces the diagnostic line.

## 5. Frozen behavior

This checkpoint must not change:

- ItemTupleSolver behavior;
- OCR/recovery;
- structure gating;
- selective-review policy;
- report v2 semantics;
- false-item removal;
- identity/price/search/persistence;
- product schema 2 / receipt schema 1;
- permission posture.

## 6. Build isolation

Debug validation application:

- applicationId: `com.receiptledger.v1.candidateprobe`
- label: `ReceiptLedger 검증 D`
- versionName: `1.0.39-candidate-diagnostics-validation`
- versionCode: 40

## 7. Acceptance

- focused diagnostic tests PASS;
- existing CP37 report v2 tests PASS;
- Remediation C solver and review tests PASS unchanged;
- full unit regression/lint/APK build PASS;
- forbidden permissions absent;
- bounded diff guard confirms no behavioral source outside diagnostic integration/version/debug label.

## 8. Stop

After CI and artifact verification, rerun the same physical receipt once and return both copied lines. Do not begin the independent 10-receipt campaign and do not add another recovery heuristic before this evidence is analyzed.
