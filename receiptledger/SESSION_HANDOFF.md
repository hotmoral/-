# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading current files and verifying refs.

Read in order:

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

## 1. Latest executable checkpoint

**CP29 — Search / Browse — PASS / COMPLETE**

- branch: `receiptledger/run-v1-search-browse-20261016`
- predecessor handoff: `36c361d8c5c5845a15ecf77648861cd2ea7a1b40`
- frozen implementation HEAD: `b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`
- canonical Actions: `38839041465` — SUCCESS
- job: `116774625167` — SUCCESS
- artifact ID: `12020980247`
- artifact digest: `sha256:16505e577d84180771fe8e6da8f8d4243cf389aa0892f2446e621933fad4de81`
- APK SHA-256: `e8f0503cd12126461f6eb257a11be2d0ef7bac68cc2857c6b4f523c059830088`
- CP29 search/browse tests 8/8 PASS
- CP28 8/8, CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint 0 errors / 0 warnings
- versionName `1.0.27-search-browse`, versionCode 28

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 검색/카테고리 탐색 -> 과거 가격/평소 가격/가격변화 판단`

CP29 supplies the read-only discovery layer for this loop.

## 3. Frozen CP29 discovery rules

Search document can use:

- stable product/commodity canonical name;
- persisted brand/productName/variant;
- exact specification representations;
- observed raw item names from already-linked receipts;
- category labels/path;
- store context.

Ranking is deterministic:

`canonical exact -> structured exact -> observed exact -> prefix -> all terms -> contains`

Whitespace-compacted discovery is allowed. Fuzzy edit-distance/embedding search is not part of V1.

Search has **zero identity mutation authority**.

## 4. Alias boundary

Current V2 persistence can resolve a known alias but cannot enumerate all aliases.

CP29 did not expand schema/API solely for search. Observed linked receipt item names are searchable discovery text instead.

Do not treat observed text as confirmed alias evidence and do not use search matches to merge stable IDs.

## 5. Browse rules

- recent = newest distinct purchase occasion;
- frequent = number of distinct receipt occasions;
- category parent includes descendants;
- store filter = exact normalized text;
- blank query = browse-all after filters;
- no result = explicit empty result, no synthetic fallback.

Price-change browse:

- consumes existing CP27/28 derived cohorts;
- only `EVALUATED` non-`TYPICAL` strict cohorts appear;
- `LIKE_FORM` contextual cohorts do not receive change alerts;
- separate comparison bases remain separate rows even under one commodity stable ID.

## 6. Storage/performance rules

- product schema 2;
- receipt schema 1;
- no new mutable search DB/index/FTS;
- canonical stores remain source truth;
- linear scan is accepted for current V1 scale;
- scanned/matched diagnostics must remain available for CP36 scale benchmarking.

Do not introduce a cache/index before representative scale proves a need and invalidation semantics are defined.

## 7. Canonical metric

`CP29_METRICS documents=3 exact_hits=1 compact_hits=1 observed_hits=1 category_rows=3 store_rows=1 recent_rows=3 frequent_rows=3 no_result_rows=0 mutation_checks=1 diagnostics_scanned=3`

Synthetic deterministic contract evidence only.

## 8. Deliberate limitations

- no typo/fuzzy search;
- confirmed alias enumeration remains absent;
- observed discovery text may disappear if its receipt/link is deleted;
- exact store text is not merchant-entity consolidation;
- large-catalog search latency has not yet been validated;
- no final search/detail commercial UI in CP29.

Do not solve these through unrelated scope expansion.

## 9. Next planned implementation checkpoint

**CP30 — Design System Foundation**

Required direction:

1. define typography roles for Korean text, numbers and price emphasis;
2. freeze color tokens including semantic price/judgment/review/error states;
3. define spacing/grid, radius, elevation and icon grammar;
4. define search field, filter chips, list/card rows, buttons and empty/loading/error states;
5. define graph/chart grammar compatible with STANDARD and NON_STANDARD cohort distinctions;
6. preserve CP28 explanation states and CP29 search/read-model semantics;
7. include accessibility/touch-target/contrast and responsive baselines;
8. do not rewrite domain or search contracts for visual convenience;
9. do not yet build the full Product Detail/Commodity Detail/Commercial Shell unless explicitly scoped.

CP30 is planned, not automatically authorized.

## 10. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipts, personal purchase DB/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

## 11. Group discipline

Recover canonical state -> restate essence/non-goals -> inspect material contradictions -> implement smallest coherent proof -> run scoped CI/evidence -> freeze refs -> synchronize handoff -> stop before next unauthorized checkpoint.

## 12. Stop condition

**CP29 is complete and handoff-synchronized. Await explicit authorization for CP30.**
