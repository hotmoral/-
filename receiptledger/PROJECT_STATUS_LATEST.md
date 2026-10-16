# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP29 — Search / Browse — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-search-browse-20261016`
- predecessor CP28 handoff: `36c361d8c5c5845a15ecf77648861cd2ea7a1b40`
- frozen CP29 implementation HEAD: `b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`
- canonical Actions run: `38839041465` — SUCCESS
- job: `116774625167` — SUCCESS
- artifact ID: `12020980247`
- artifact digest: `sha256:16505e577d84180771fe8e6da8f8d4243cf389aa0892f2446e621933fad4de81`
- debug APK SHA-256: `e8f0503cd12126461f6eb257a11be2d0ef7bac68cc2857c6b4f523c059830088`
- CP29 tests: 8/8 PASS
- CP28 8/8, CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.27-search-browse` / versionCode 28

Any later handoff commit must remain documentation-only. Executable/evidence boundary remains `b73fe865...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable judgment -> find/browse`

CP29 makes the frozen domain and price layers practically discoverable without granting search any identity authority.

## 3. CP29 search contract

Searchable discovery text includes:

- canonical product/commodity name;
- persisted brand/productName/variant;
- exact specification tokens;
- observed linked receipt item names;
- category path/labels;
- store context.

Matching is deterministic and non-fuzzy:

`exact -> prefix -> all terms -> contains`

Whitespace-compacted discovery is allowed, but search never creates/merges/relinks a product.

## 4. Browse contract

- **Recent:** latest purchase occasion first.
- **Frequent:** distinct receipt occasions, not quantity or item-line count.
- **Category:** selected category plus descendants.
- **Store filter:** exact normalized store text.
- **Price change:** strict CP28 `EVALUATED` non-`TYPICAL` cohorts only.

A NON_STANDARD commodity can produce separate price-change rows for separate exact bases such as `WEIGHT_KG` and `EACH`; no cross-cohort aggregate is invented.

## 5. Storage/performance boundary

- product schema remains 2;
- receipt schema remains 1;
- no mutable search table/index/FTS was introduced;
- canonical stores are read directly;
- search result diagnostics expose scan/match counts for CP36 performance validation.

Observed receipt names are discovery terms only. Current persistence does not enumerate all confirmed aliases; V1 does not widen persistence merely for search.

## 6. Canonical local metric

`CP29_METRICS documents=3 exact_hits=1 compact_hits=1 observed_hits=1 category_rows=3 store_rows=1 recent_rows=3 frequent_rows=3 no_result_rows=0 mutation_checks=1 diagnostics_scanned=3`

Synthetic deterministic contract evidence only.

## 7. Known limitations

- no typo/fuzzy/embedding search;
- a discovery term sourced only from a deleted receipt/link may disappear;
- current read path is linear scan and not yet benchmarked at large scale;
- store names are exact normalized text, not merchant-entity consolidation;
- no final commercial search/detail UI yet.

## 8. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> **CP29 Search / Browse**.

## 9. Next planned checkpoint

**CP30 — Design System Foundation**.

Goal: freeze the commercial visual/interaction grammar before Product Detail, Commodity Detail and final shell implementation.

Required areas:

- typography hierarchy;
- color/semantic-state system;
- spacing/grid;
- shape/elevation;
- icons;
- buttons/fields/cards/list rows/search/filter chips;
- price and judgment presentation;
- chart grammar;
- loading/empty/error/review states;
- accessibility baseline and responsive behavior.

CP30 must consume frozen CP29 search/read models rather than rewrite domain semantics for visual convenience.

**Do not begin CP30 without explicit user authorization.**

## 10. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP29_SEARCH_BROWSE_CLOSEOUT.md`
4. `receiptledger/CP29_SEARCH_BROWSE_EVIDENCE.md`
5. `receiptledger/CP29_SEARCH_BROWSE_PLAN.md`
6. `receiptledger/SEARCH_BROWSE_CONSISTENCY_REVIEW.md`
7. `receiptledger/SEARCH_BROWSE_GOLDEN_VECTORS.md`
8. `receiptledger/CP28_PRICE_EVALUATION_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify current branch/ref and frozen implementation boundary before future work.

## 11. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

**Current stop condition: CP29 is complete. Await explicit authorization for CP30.**
