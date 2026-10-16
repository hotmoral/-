# ReceiptLedger V1 — CP33 Capture / Review UX V2 Plan

Updated: 2026-10-16 KST
Checkpoint: `CP33_CAPTURE_REVIEW_UX_V2`
Predecessor handoff: `1996668e1fec6961eb158c5dd2e6b673fdb46ee0`
Working branch: `receiptledger/run-v1-capture-review-ux-v2-20261016`

## 1. Goal

Move the existing capture harness toward the product flow:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

The objective is to reduce avoidable manual review while preserving receipt truth, user acknowledgement, identity authority, provenance, privacy and price eligibility.

## 2. Governing product rule

ReceiptLedger remains a personal purchase-price memory and comparison system. CP33 improves the input/review experience only. It must not redefine product identity, comparison basis, price evaluation, search semantics or navigation architecture.

## 3. Explicit supersession of legacy review UX

`REVIEW_EDIT_CORE_PLAN.md` required an explicit review step before save. CP33 preserves the safety intent but replaces the old interpretation that every receipt must open the full edit dialog.

Frozen CP33 interpretation:

- persistence always requires an explicit user Save action;
- a clean, deterministically validated receipt may be saved without opening the edit dialog;
- a receipt with unresolved material uncertainty must be reviewed before Save is enabled;
- full editing remains available voluntarily;
- raw OCR evidence and edit provenance remain immutable/preserved as before.

This is a UX-policy supersession, not a relaxation of stored-data truth.

## 4. Review assessment V2

Introduce a pure deterministic assessment over `ReceiptRecord`.

### AUTO_CONFIRMED
A record is save-ready without mandatory edit-dialog review only when all material uncertainty gates are clear:

- receipt validation is `PASS`, or `PASS_WITH_WARNINGS` whose remaining issues are only explicit `USER_EDITED_*` provenance after a user review;
- purchase date is present;
- store name is present;
- printed total is present;
- at least one item exists;
- every item has a nonblank name and line amount;
- no item is `PARTIAL`;
- no item uses `ValueOrigin.UNKNOWN`;
- no item uses `ValueOrigin.DEFAULT_ONE` for quantity;
- arithmetic-derived values (`INFERRED_ARITHMETIC`) are allowed when the final receipt arithmetic is valid.

### REVIEW_REQUIRED
Review is mandatory when any material uncertainty remains, including:

- `MISMATCH` or `INCOMPLETE` receipt validation;
- non-user-only `PASS_WITH_WARNINGS`;
- missing purchase date/store/printed total;
- no items;
- blank item name;
- missing line amount;
- `PARTIAL` item;
- `UNKNOWN` provenance;
- quantity defaulted to one (`DEFAULT_ONE`).

The assessment must expose exact receipt fields and item ordinals requiring review. It must not infer replacement values.

## 5. Selective review UX

- Default review dialog shows only flagged receipt fields/items.
- Unflagged values are carried through unchanged to `ReceiptReviewEngine`.
- `ReceiptReviewEngine` remains the sole edit/revalidation engine.
- A separate `전체 내용 수정` path keeps all existing editable fields available.
- Clearing a value never causes silent re-inference.
- Mismatch is shown, never automatically repaired.
- After applying review, the V2 assessment is rerun. Save enables only if material review blockers are gone.

## 6. Capture automation

- Camera and system picker remain the only image acquisition mechanisms.
- Selecting/capturing an image automatically starts OCR/recovery once the image is loaded.
- Manual `OCR` as a required step is removed from the primary flow.
- Re-analysis remains available as a secondary recovery action.
- Perspective correction remains optional; if applied, OCR reruns using the corrected view and preserves coordinate mapping/provenance.
- Normal user UI must not expose raw pass enums, score dumps or engineering diagnostics.

## 7. Repeat known-purchase reuse

After the receipt and image are successfully persisted:

- reuse only the existing exact confirmed GLOBAL alias path via `resolveAndLinkExact`;
- never create a product automatically;
- never confirm a new alias automatically;
- never use search ranking, fuzzy similarity, category or price as identity evidence;
- link failure must not roll back an already-successful receipt save or create duplicate-save risk;
- surface a simple count of exact repeat identities reused when nonzero.

This deliberately does not widen CP24 authority. Merchant-specific/new semantic linking is outside this smallest coherent CP33 proof unless an existing safe write path already provides it.

## 8. Commercial presentation

Consume CP30 design grammar:

- programmatic `Activity + android.widget` remains;
- CP30 typography/spacing/touch targets/semantic cards/buttons are reused;
- normal states use Korean user-facing copy rather than enum/debug text;
- processing, auto-confirmed, review-required, saving, success and error states are visibly distinct by text and semantic tone;
- color is never the only state carrier.

CP33 does not build the CP34 home/navigation shell.

## 9. Frozen upstream boundaries

Do not change:

- OCR recognition/recovery algorithms;
- item tuple inference semantics;
- receipt validation arithmetic;
- CP21–29 domain authority;
- CP27 price eligibility;
- CP28 thresholds;
- CP30 design tokens;
- CP31 Product Detail;
- CP32 Commodity Detail;
- product schema 2;
- receipt schema 1;
- offline/no-broad-permission posture.

## 10. Expected implementation scope

Allowed coherent scope:

- `MainActivity` capture/review presentation and orchestration;
- `review/**` additive V2 assessment/selective-dialog helpers while preserving the existing engine;
- strings/resources;
- app version bump;
- CP33 tests and ReceiptLedger-prefixed workflow/evidence;
- CP33 planning/consistency/golden documents.

Avoid unrelated Activity redesigns or domain cleanup.

## 11. Acceptance

CP33 closes only if all hold:

1. image selection/capture auto-starts processing;
2. clean fixture is save-ready without mandatory full review;
3. default-one/partial/unknown/mismatch/incomplete fixtures require review;
4. safe arithmetic inference can remain auto-confirmed when final validation is trustworthy;
5. selective assessment identifies exact fields/item ordinals;
6. reviewed-and-corrected data can become save-ready despite USER_EDITED provenance;
7. raw OCR survives unchanged through review;
8. full edit path still exists;
9. repeated exact known alias is reused only by existing exact authority after successful save;
10. no fuzzy/new-product auto identity is introduced;
11. schema versions stay 2/1;
12. forbidden permissions remain absent;
13. CP30–32 and relevant older regressions remain green;
14. lint is 0 errors / 0 warnings;
15. plan/code post-green review finds no material gap.

## 12. Non-goals

- CP34 commercial home/navigation shell;
- new product creation automation;
- fuzzy/AI identity matching;
- new OCR model/algorithm;
- price-policy changes;
- receipt DB/product DB migration;
- Compose/Material migration;
- cloud/network sync;
- real-receipt benchmark campaign (CP35).

## 13. Stop condition

After exact executable evidence is frozen, synchronize closeout/status/handoff documents as docs-only and stop before CP34 without explicit authorization.
