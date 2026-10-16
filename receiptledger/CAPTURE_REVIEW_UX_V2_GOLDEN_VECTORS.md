# ReceiptLedger V1 — Capture / Review UX V2 Golden Vectors

Updated: 2026-10-16 KST
Checkpoint: CP33

These vectors test deterministic review-burden policy rather than OCR model quality.

## CR33-G01 — Clean exact receipt

- validation: PASS
- date/store/printed total present
- all items EXACT, printed origins
- expected: AUTO_CONFIRMED
- expected mandatory review items: 0
- Save may be enabled without opening edit dialog.

## CR33-G02 — Safe arithmetic inference

- validation: PASS
- quantity PRINTED
- unit or line amount INFERRED_ARITHMETIC
- no DEFAULT_ONE/UNKNOWN/PARTIAL
- expected: AUTO_CONFIRMED

## CR33-G03 — Default-one quantity

- validation: PASS
- item quantity origin DEFAULT_ONE
- expected: REVIEW_REQUIRED
- expected flagged item: that ordinal
- reason: default quantity can distort per-item price memory.

## CR33-G04 — Partial item

- validation: PASS_WITH_WARNINGS
- item resolution PARTIAL
- expected: REVIEW_REQUIRED
- expected flagged item: that ordinal

## CR33-G05 — Unknown provenance

- validation: PASS or PASS_WITH_WARNINGS
- any material item origin UNKNOWN
- expected: REVIEW_REQUIRED

## CR33-G06 — Receipt mismatch

- validation: MISMATCH
- expected: REVIEW_REQUIRED
- receipt total/discount and all item rows exposed for correction because the mismatch source is not safely attributable.

## CR33-G07 — Incomplete receipt

- validation: INCOMPLETE
- missing printed total or line amount
- expected: REVIEW_REQUIRED
- missing field/item must be flagged.

## CR33-G08 — Missing purchase date

- otherwise clean PASS receipt
- purchaseDate absent
- expected: REVIEW_REQUIRED
- date field flagged.

## CR33-G09 — Missing store

- otherwise clean PASS receipt
- store absent
- expected: REVIEW_REQUIRED
- store field flagged.

## CR33-G10 — Corrected receipt can finish

- begin with REVIEW_REQUIRED
- user edits values through existing ReceiptReviewEngine
- final arithmetic valid
- final validation PASS_WITH_WARNINGS
- issues contain only USER_EDITED provenance
- no material item/receipt blocker remains
- expected: AUTO_CONFIRMED / SAVE_READY

## CR33-G11 — User edit with remaining mismatch

- user edits but arithmetic still mismatches
- expected: REVIEW_REQUIRED
- Save remains disabled.

## CR33-G12 — Raw OCR preservation

- apply selective or full review
- expected: `rawOcrText` byte-for-byte/string-equal to base record.

## CR33-G13 — Selective item set

- three items: exact, default-one, partial
- expected flagged ordinals: default-one + partial only unless receipt-level mismatch requires all rows.

## CR33-G14 — Full edit escape hatch

- AUTO_CONFIRMED receipt
- user requests full edit
- expected: all legacy editable receipt fields and every item remain available; no V2 assessment blocks voluntary correction.

## CR33-G15 — Repeat exact alias reuse

- receipt successfully persisted
- item raw name has an already-confirmed GLOBAL exact alias
- expected: existing stable product ID linked with EXACT_ALIAS authority
- no new product or alias created.

## CR33-G16 — Unknown alias

- receipt successfully persisted
- item raw name has no confirmed exact alias
- expected: remains unclassified
- save still succeeds.

## CR33-G17 — Exact-link failure isolation

- receipt persistence succeeds
- catalog exact-link operation throws/fails
- expected: receipt remains successfully saved; link reuse is best-effort/non-fatal; no second receipt save is attempted.

## CR33-G18 — Auto processing entry

- image load succeeds
- expected: OCR/recovery starts automatically once for that display revision
- no mandatory manual OCR button step.

## CR33-G19 — Re-analysis

- user explicitly requests re-analysis on current image/corrected view
- expected: previous pending record invalidated, same frozen OCR/recovery engine reruns, stale callback cannot overwrite current generation/revision.

## CR33-G20 — Scope/privacy regression

- product schema = 2
- receipt schema = 1
- forbidden permissions absent: CAMERA, READ_MEDIA_IMAGES, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE
- CP31/32 detail behavior unchanged.

## Canonical metric target

`CP33_METRICS capture_review_version=2 auto_confirm_cases=2 review_required_cases=7 user_edit_exit=1 selective_review=1 full_edit=1 raw_ocr_preserved=1 exact_alias_reuse=1 unknown_alias_safe=1 link_failure_isolated=1 auto_processing=1 schema_unchanged=1`
