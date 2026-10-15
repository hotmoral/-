# ReceiptLedger V1 — CP20 Product Rebaseline Closeout

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`
Branch: `receiptledger/run-v1-product-rebaseline-20261016`

## Result

**CP20 — Product Rebaseline / V1 Master Specification: COMPLETE**

This checkpoint intentionally changed no production Android source, OCR logic, receipt parser, database schema, runtime behavior, permissions, or CI toolchain.

## Canonical artifacts

- `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
- `PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
- `PRODUCT_REBASELINE_V1_ROADMAP.md`
- `CP20_PRODUCT_REBASELINE_CLOSEOUT.md`

## Frozen decisions

- ReceiptLedger is productized around personal purchase-price memory, not receipt archiving.
- Receipt remains source evidence/input; product/commodity and price history are the primary user-facing domain.
- Existing STANDARD / NON_STANDARD / UNCLASSIFIED semantics are retained and enriched, not discarded.
- Wrong identity merge is treated as higher-risk than unresolved identity.
- Fuzzy/semantic matching may rank suggestions but must not silently merge by default.
- Merchant-scoped alias capability is required in future V2 identity design.
- NON_STANDARD observations may be grouped under one commodity while preserving raw unit/form; grouping does not imply comparability.
- Price history remains traceable to canonical saved receipt records and product/item links.
- Price judgments require explicit statistics/data-sufficiency rules.
- Existing OCR/validation/provenance/privacy/API36 foundations remain preserved.
- Prototype/debug UI should be hidden/replaced incrementally only after functional/evidence parity.
- V2 domain contract must precede persistence migration.

## Compatibility result

The completed V1 foundation is **compatible with controlled extension**. No blocking contradiction requiring a rewrite was found.

Main known gaps to solve in future checkpoints:

- structured brand/specification/pack identity
- merchant-context aliases
- category taxonomy
- explicit non-standard sales-unit/form model
- canonical comparable-observation layer
- richer price statistics and price judgment
- product/commodity search/browse/detail
- commercial intake/review UX and design system

## Next planned checkpoint

**CP21 — Catalog Domain V2**

CP21 exists in the roadmap but is **not automatically authorized** by CP20 completion. A new group begins only after explicit user instruction.

## Handoff requirement

After this closeout document, canonical status/handoff/readme/work-unit documents must be synchronized to CP20 and the branch must be verified as documentation-only relative to the prior frozen implementation boundary.
