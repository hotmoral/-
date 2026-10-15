# ReceiptLedger V1 — CP20 Decision Register

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`

## Frozen decisions

1. Product essence: personal purchase-price memory and comparison.
2. Receipt role: trusted input/evidence, not the primary product destination.
3. STANDARD: exact repeatable packaged-product identity; enrich rather than replace.
4. NON_STANDARD: one commodity may aggregate different purchase forms, but grouping does not imply direct comparability.
5. UNCLASSIFIED: unresolved state; never force a fake identity to clear workflow.
6. Identity safety: wrong merge is worse than unresolved; fuzzy/semantic similarity is suggestion evidence by default.
7. Alias evolution: future design requires merchant/context scope or collision-safe equivalent.
8. Price truth: remain traceable to saved receipt records + product/item links.
9. Price judgment: must use explicit deterministic statistics and data-sufficiency rules.
10. Category: new dedicated capability; not hidden inside product-name matching.
11. UX destination: product-centric search/category/history/detail, with receipt capture as entry flow.
12. Intake destination: automatic processing + uncertainty-focused review.
13. Core preservation: do not rewrite validated OCR/layout/validation/archive/privacy/API36 foundations for UI modernization.
14. Persistence order: freeze Domain V2 before storage migration.
15. UI migration: incremental; prototype/debug surfaces are retired from normal UX only after replacement parity.
16. Scope control: no budgeting/banking/cloud/online-price/coupon/social expansion before the price-memory loop is complete.
17. Review discipline: each checkpoint examines only materially affected domain/data/UX/privacy/performance/test dimensions; no ritual re-auditing.
18. Handoff discipline: every completed group synchronizes canonical status/handoff material and stops before the next unauthorized group.

## Deferred decisions

The following are intentionally not frozen by CP20:

- exact Category taxonomy
- exact Product/Specification field schema
- exact SalesUnit enum/model
- direct SQLite vs Room
- View vs Compose architecture
- fuzzy ranking algorithm
- safe auto-link threshold beyond already confirmed exact alias behavior
- price judgment thresholds/window sizes/outlier policy
- chart library/visual grammar
- backup/sync/release distribution

These belong to their dependency-appropriate checkpoints.
