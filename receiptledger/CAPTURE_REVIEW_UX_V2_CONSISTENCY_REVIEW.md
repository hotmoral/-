# ReceiptLedger V1 — Capture / Review UX V2 Consistency Review

Updated: 2026-10-16 KST
Predecessor: CP32 handoff `1996668e1fec6961eb158c5dd2e6b673fdb46ee0`

## 1. Material contradiction review

### Legacy mandatory review vs CP33 burden reduction

Legacy `REVIEW_EDIT_CORE_PLAN.md` froze `Save disabled after OCR until review is applied`. The later product rebaseline and CP33 roadmap explicitly require `자동 처리 -> 확인 필요한 항목만 검토 -> 저장` and treat review burden as a first-class metric.

Resolution: preserve explicit user Save acknowledgement and mandatory review for unresolved uncertainty, but no longer require opening the full edit dialog for a clean deterministic result. This is an explicit V2 UX-policy supersession and must be documented rather than silently changing the old rule.

### INFERRED does not always mean uncertain

`ItemTupleSolver` uses `INFERRED` both for deterministic arithmetic completion and for `DEFAULT_ONE`. Treating every INFERRED item as review-required would defeat CP33 and ignore existing provenance distinctions.

Resolution:

- `INFERRED_ARITHMETIC` may be auto-confirmed when the receipt is otherwise PASS and no material gate remains;
- `DEFAULT_ONE` remains review-required because quantity affects per-item price memory;
- `UNKNOWN` and `PARTIAL` remain review-required.

### USER_EDITED warnings

`ReceiptReviewEngine` deliberately returns `PASS_WITH_WARNINGS` when valid values were edited. A naive rule that every warning requires review would trap a corrected receipt in an endless review loop.

Resolution: a PASS_WITH_WARNINGS record is save-ready only when remaining issues are exclusively explicit USER_EDITED provenance and all structural/material gates are clear.

## 2. Identity consistency

Current Receipt Detail reuses `SqliteProductCatalogStore.resolveAndLinkExact()` for previously confirmed GLOBAL aliases. Moving the same exact reuse to post-save capture processing does not widen authority.

CP33 must not:

- write a new alias;
- create a product automatically;
- use search/fuzzy/category/price similarity;
- reinterpret CP24 resolver ranking;
- link before the receipt is durably persisted.

Any exact-link failure after receipt save is non-fatal to receipt persistence to avoid duplicate-save risk across separate databases.

## 3. Price-memory consistency

Quantity affects STANDARD per-package price derivation. Therefore `DEFAULT_ONE` cannot be treated as silently trustworthy merely because receipt total arithmetic passes.

Conversely, printed quantity plus deterministic arithmetic-derived unit/line amount can remain auto-confirmed when overall validation is PASS because provenance remains explicit and no guessed denominator is introduced.

CP33 does not decide price eligibility. CP27 remains the authority after persistence/linking.

## 4. Receipt-truth consistency

Frozen:

- raw OCR remains immutable evidence;
- perspective-correction flag/dimensions remain preserved;
- user edits keep USER_EDITED origins;
- cleared values are not re-inferred;
- mismatch is not auto-repaired;
- receipt/image persistence ordering remains archive + receipt DB transaction semantics.

## 5. UX consistency

Current MainActivity is a development harness exposing OCR pass names, scores, raw validation enums and arithmetic diagnostics. That conflicts with CP30 commercial presentation and CP33 user flow.

Resolution: CP33 may redesign only this capture/review surface, using the existing programmatic View toolkit and CP30 components/tokens. It does not imply CP34 navigation-shell authorization.

## 6. Privacy / platform consistency

Frozen:

- external camera app + temporary content URI;
- system picker/document provider;
- bundled local Korean ML Kit OCR;
- no direct CAMERA permission;
- no broad media/storage permission;
- no INTERNET / ACCESS_NETWORK_STATE;
- target/compile SDK 36, minSdk 23.

## 7. Schema consistency

No new durable review-state table is required. CP33 assessment is a deterministic projection from current `ReceiptRecord` and existing catalog knowledge.

- product schema remains 2;
- receipt schema remains 1;
- no duplicate mutable price truth;
- no new search/index/cache truth.

## 8. Scope firewall

CP33 may modify MainActivity, review-layer V2 helpers/dialog presentation, resources, version/tests/workflow/docs. CP31/32 detail screens and frozen domain packages should remain unchanged.

CP34 launcher/home/navigation integration is explicitly excluded.

## 9. Closure risks to check after green CI

- hidden full-edit path accidentally lost;
- corrected USER_EDITED record still stuck as review-required;
- DEFAULT_ONE accidentally auto-confirmed;
- post-save exact linking failure causing receipt-save failure or duplicate retry;
- raw enum/debug diagnostics leaking into primary UI;
- save enabling while a review blocker remains;
- lint/accessibility regressions;
- source changes after frozen executable boundary.
