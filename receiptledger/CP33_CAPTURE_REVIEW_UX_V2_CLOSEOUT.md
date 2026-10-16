# ReceiptLedger V1 — CP33 Capture / Review UX V2 Closeout

Updated: 2026-10-16 KST
Checkpoint: **CP33 — Capture / Review UX V2 — PASS / COMPLETE**

## 1. Canonical execution boundary

- branch: `receiptledger/run-v1-capture-review-ux-v2-20261016`
- predecessor CP32 handoff: `1996668e1fec6961eb158c5dd2e6b673fdb46ee0`
- frozen implementation HEAD: `34cdac2d3e61081ab2a529173dbef9a2431431e0`
- canonical Actions run: `38874509796` — SUCCESS
- canonical job: `116886197267` — SUCCESS
- artifact ID: `12034453925`
- artifact digest: `sha256:36da341582f3e4083699a31d87eb5366b62e6c99c555d1fcd41dec4b9dd3f912`
- debug APK SHA-256: `8f78d9dab92c65bdccd31008f9cd15221f26ef63dbfcfab2741e9a066d2237b0`
- versionName: `1.0.31-capture-review-ux-v2`
- versionCode: `32`

Any later handoff/status commit is documentation-only. The executable/evidence boundary remains `34cdac2d...`.

## 2. Product result

CP33 moves the capture flow from a development harness toward the intended product loop:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

The user still explicitly presses Save. What changed is that a clean deterministic receipt no longer has to open the full edit dialog merely to satisfy a procedural gate.

## 3. Frozen review policy V2

`CaptureReviewAssessmentV2` is a read-only deterministic projection over the existing `ReceiptRecord`.

A receipt can become **AUTO_CONFIRMED / save-ready** when:

- validation is PASS; or PASS_WITH_WARNINGS whose remaining issues are only explicit user edit/confirmation provenance;
- date, store and printed total are present;
- at least one item exists;
- item name and line amount are present;
- there is no PARTIAL item;
- there is no UNKNOWN material origin;
- a DEFAULT_ONE quantity has been explicitly confirmed by the user;
- arithmetic-derived values may remain when final receipt arithmetic is trustworthy.

A receipt remains **REVIEW_REQUIRED** for material uncertainty such as mismatch, incomplete data, missing required receipt context, PARTIAL/UNKNOWN items or unconfirmed DEFAULT_ONE quantity.

## 4. Selective review / full edit

- Default review displays only fields/items identified by the V2 assessment.
- Unflagged values pass through unchanged to the frozen `ReceiptReviewEngine`.
- `ReceiptReviewEngine` remains the edit/revalidation authority.
- `전체 내용 수정` remains available for voluntary full correction.
- If a warning cannot safely be narrowed to specific fields/items, the primary review action falls back to full edit instead of dead-ending.
- Cleared values are not silently re-inferred.
- Mismatch is never automatically repaired.
- raw OCR remains unchanged through review.

For a user-confirmed quantity that originally came from `DEFAULT_ONE`, CP33 adds `USER_CONFIRMED_DEFAULT_ONE:<ordinal>` provenance while preserving the original `ValueOrigin.DEFAULT_ONE`.

## 5. Capture automation

- Camera and system picker remain the acquisition paths.
- Successfully loading a selected/captured image automatically starts the frozen OCR/recovery flow.
- Manual OCR is no longer a required primary step.
- `다시 분석` remains a secondary recovery action.
- Perspective correction remains optional and triggers re-analysis while preserving the existing coordinate/provenance path.
- Primary UI no longer exposes raw OCR pass diagnostics or score/debug enums.

## 6. Repeat-purchase reuse

After receipt/image persistence succeeds, CP33 performs best-effort reuse through the already-frozen exact authority:

`SqliteProductCatalogStore.resolveAndLinkExact()`

This may reuse only an already-confirmed GLOBAL exact alias.

It does **not**:

- create a product;
- confirm a new alias;
- use fuzzy similarity;
- use search relevance, category or price as identity evidence.

Unknown aliases remain unclassified without blocking save. Per-item exact-link failures are isolated from receipt persistence.

The final pre-closeout correction also ensures that only the actual `repository.save()` failure can be reported as a save failure; optional post-save work no longer causes an already-persisted receipt to be presented as failed.

## 7. Presentation / accessibility

CP33 consumes the frozen CP30 programmatic design system.

- Korean user-facing processing/review/save/error copy;
- semantic text + tone rather than raw engineering states;
- CP30 button/touch-target rules;
- complete capture surface placed in a vertical ScrollView so review/save controls remain reachable on constrained heights or enlarged text;
- full edit dialog itself remains scrollable.

CP34 commercial navigation/home integration is deliberately not part of CP33.

## 8. Frozen upstream boundaries

Unchanged:

- OCR / recovery algorithms;
- item tuple inference semantics;
- receipt arithmetic validation;
- stable identity authority and CP21–29 domain semantics;
- CP27 price eligibility;
- CP28 thresholds;
- CP30 design tokens;
- CP31 Product Detail;
- CP32 Commodity Detail;
- product schema 2;
- receipt schema 1;
- offline / no broad permission posture.

## 9. Canonical metric

`CP33_METRICS capture_review_version=2 auto_confirm_cases=2 review_required_cases=7 user_edit_exit=1 selective_review=1 full_edit=1 raw_ocr_preserved=1 exact_alias_reuse=1 unknown_alias_safe=1 link_failure_isolated=1 auto_processing=1 schema_unchanged=1`

## 10. Validation result

Packaged evidence confirms:

- CP33: 13/13 PASS;
- legacy ReceiptReviewEngine: 4/4 PASS;
- CP32: 11/11 PASS;
- CP31: 9/9 PASS;
- CP30: 9/9 PASS;
- CP29: 8/8 PASS;
- CP28: 8/8 PASS;
- CP27: 8/8 PASS;
- CP26: 8/8 PASS;
- all above have zero failures/errors/skips;
- Android lint: `No issues found.`;
- forbidden CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE permissions absent;
- packaged permission is only the internal dynamic-receiver permission.

## 11. Pre-closeout correction history

CP33 was not closed on the first build or first green run.

1. Run `38873199997` built/tests successfully but the CP33 zero-warning gate rejected 27 obsolete `UnusedResources` warnings left by the old development harness strings.
2. The unused strings were removed and run `38873592904` became green.
3. Post-green plan/code review still rejected closure because:
   - optional `repository.count()` after successful persistence could misreport an already-saved receipt as failed;
   - a review-required warning with no narrow target could lead to a non-actionable primary review path;
   - fixed-height capture composition could make review/save controls unreachable on constrained heights.
4. These were corrected in `34cdac2d...` and the full canonical run `38874509796` passed with clean lint.

Only the final HEAD/run pair is canonical.

## 12. Evidence limitation

CP33 CI provides deterministic code/unit/lint/build/artifact evidence. It does not include real private receipts, emulator screenshot comparison, physical-device usability testing or the CP35 real-receipt evaluation campaign.

## 13. Next boundary

Next planned checkpoint: **CP34 — Commercial UI Shell**.

CP34 may integrate product-centric home/navigation/search/category/product/commodity/receipt/settings destinations. It must not be started without explicit user authorization.
