# ReceiptLedger V1 — CP29 Search / Browse Closeout

Updated: 2026-10-16 KST
Status: **PASS / COMPLETE**

## 1. Closed boundary

- branch: `receiptledger/run-v1-search-browse-20261016`
- predecessor CP28 handoff: `36c361d8c5c5845a15ecf77648861cd2ea7a1b40`
- frozen implementation HEAD: `b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`
- canonical Actions run: `38839041465` — SUCCESS
- job: `116774625167` — SUCCESS
- artifact ID: `12020980247`
- artifact digest: `sha256:16505e577d84180771fe8e6da8f8d4243cf389aa0892f2446e621933fad4de81`
- APK SHA-256: `e8f0503cd12126461f6eb257a11be2d0ef7bac68cc2857c6b4f523c059830088`
- version: `1.0.27-search-browse` / versionCode 28
- lint: 0 errors / 0 warnings

## 2. What CP29 added

CP29 added a read-only discovery layer over existing canonical receipt/catalog/category/price data.

It provides:

- deterministic product/commodity text search;
- canonical name, brand, product name, variant and specification discovery;
- observed linked receipt item-name discovery;
- category/path and store-context discovery;
- category descendant browse;
- exact-normalized store filtering;
- recent-purchase browse;
- frequent-purchase browse by distinct receipt occasions;
- strict CP28 price-change browse;
- explicit scan/match diagnostics for later scale testing.

## 3. Search authority boundary

Search is discovery only.

It cannot:

- create or merge products;
- relink receipt items;
- write aliases;
- change category/specification;
- widen CP24 identity authority.

Observed POS/item strings are searchable because they are already linked to a stable catalog ID. They remain receipt-derived discovery text and do not become confirmed aliases merely by being searchable.

## 4. Ranking contract

Normalization uses NFKC, whitespace normalization and uppercase Latin. A compact key also ignores whitespace for discovery-only matching.

V1 ranking is deterministic and non-fuzzy:

1. canonical exact;
2. structured-field exact;
3. observed-item exact;
4. canonical/structured prefix;
5. observed/category/store prefix;
6. all query terms contained;
7. whole-query contains.

Tie-break order:

`relevance -> latest purchase -> purchase occasion count -> canonical name -> stable ID`

No Levenshtein or embedding similarity was introduced.

## 5. Browse contract

### Recent
One stable product/commodity row per catalog entry with purchases, ordered by latest purchase.

### Frequent
Frequency means distinct receipt occasions, not item-line count and not purchased quantity.

### Category
Selecting a taxonomy parent includes descendants. Category stays browse metadata only.

### Store
Filter uses exact normalized store text, matching CP27 scope semantics. Partial store strings are not silently treated as the same store.

### Price change
Price-change browse is cohort-specific:

- only CP28 `EVALUATED` non-`TYPICAL` rows appear;
- contextual `LIKE_FORM` is excluded;
- one NON_STANDARD commodity may have separate `WEIGHT_KG`, `EACH`, etc. rows;
- no cross-basis aggregate is manufactured.

## 6. Storage/performance decision

No mutable search table, FTS index or cache was added.

CP29 assembles read models from canonical stores. This avoids stale search truth and keeps product schema 2 / receipt schema 1 unchanged.

The result includes scanned/matched counts so CP36 can measure linear-scan cost at representative scale before any index/cache migration is justified.

## 7. Canonical local evidence

Metric:

`CP29_METRICS documents=3 exact_hits=1 compact_hits=1 observed_hits=1 category_rows=3 store_rows=1 recent_rows=3 frequent_rows=3 no_result_rows=0 mutation_checks=1 diagnostics_scanned=3`

Tests:

- CP29 Search / Browse: 8/8 PASS
- CP28 Price Evaluation: 8/8 PASS
- CP27 Price Intelligence: 8/8 PASS
- legacy Price History: 2/2 PASS
- CP26 Commodity: 8/8 PASS
- CP25 Category: 8/8 PASS
- CP24 Identity: 8/8 PASS
- CP23 Semantics: 7/7 PASS
- CP21 Catalog: 15/15 PASS
- CP22 Persistence: 7/7 PASS
- lint: 0 errors / 0 warnings

These are deterministic local contract fixtures, not real-world search-quality claims.

## 8. Deliberate limitations

- no typo-correction/fuzzy search;
- current V2 persistence cannot enumerate all confirmed aliases, so V1 search uses observed linked receipt names instead;
- deleting the source receipt/link may remove that observed discovery term;
- search currently scans canonical data rather than an FTS/index structure;
- store identity is exact normalized text, not merchant-entity consolidation;
- no final commercial visual/search screen in this checkpoint.

## 9. Frozen upstream boundary

Unchanged:

- stable-ID identity authority;
- product schema 2;
- receipt schema 1;
- CP23 semantic evidence;
- CP24 resolver authority;
- CP25 category semantics;
- CP26 grouping/comparability rules;
- CP27 price derivation/exclusions;
- CP28 judgment policy;
- permissions/network/privacy posture.

## 10. Next boundary

Next planned checkpoint: **CP30 — Design System Foundation**.

CP30 should freeze the visual/interaction grammar needed before final Product/Commodity Detail screens:

- typography;
- color and semantic states;
- spacing/grid;
- shapes/elevation;
- icon rules;
- list/search/filter components;
- price/judgment presentation grammar;
- chart grammar;
- accessibility baseline;
- loading/empty/error/review states.

CP30 must not rewrite the frozen domain/search contracts merely to simplify visuals.

## 11. Stop condition

CP29 implementation, CI/evidence and handoff synchronization are complete. Stop at this boundary; CP30 requires explicit user authorization.
