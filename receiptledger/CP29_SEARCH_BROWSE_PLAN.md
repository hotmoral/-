# ReceiptLedger V1 — CP29 Search / Browse Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_SEARCH_BROWSE_01`

## 1. Product essence

ReceiptLedger is useful only if a repeat purchase can be found quickly enough to answer: what did I buy, where, how often, and how does the current/last price compare with my own history?

CP29 adds a read-only discovery layer over the already-frozen catalog, receipt, category, price-intelligence and price-evaluation contracts.

## 2. Scope

CP29 provides:

- deterministic text search over product/commodity canonical names;
- structured STANDARD fields: brand, product name, variant and specification;
- observed receipt item names already linked to a stable catalog ID;
- category display names/path;
- store context;
- category browse including descendants;
- exact-normalized store filtering;
- recent-purchase browse;
- frequent-purchase browse;
- evaluated price-change browse;
- deterministic ranking, empty-query and no-result semantics;
- search/browse quality and performance contract fixtures.

## 3. Frozen upstream boundary

CP29 must not:

- mutate or merge catalog identity;
- create a new product from search;
- write aliases from search;
- widen CP24 identity authority;
- reinterpret CP25 category as identity evidence;
- mix CP26 commodity comparison bases;
- bypass CP27 eligibility/discount rules;
- change CP28 judgment policy;
- introduce a mutable duplicate search/index database;
- change product schema 2 or receipt schema 1;
- add network, permissions or cloud search.

## 4. Searchable data

Each stable catalog entry contributes a read-only search document from existing canonical data:

- stable product ID and type;
- canonical name;
- V2 brand/productName/variant when present;
- specification tokens when present;
- assigned category ID and human-readable category ancestry;
- observed receipt item names from existing item links;
- normalized store names from those receipts;
- purchase count and latest purchase context;
- CP27/28 derived price signals.

Observed item names are discovery text only. They do not become alias/identity authority.

## 5. Text matching

Normalization:

- Unicode NFKC;
- trim;
- collapse whitespace;
- uppercase Latin;
- a compact key also ignores whitespace for queries such as `서울 우유 1L` vs `서울우유1L`.

V1 ranking is deterministic and intentionally non-fuzzy:

1. canonical exact;
2. structured field exact;
3. observed item-name exact;
4. canonical/structured prefix;
5. observed/category/store prefix;
6. all normalized query tokens contained in the combined document;
7. whole-query contains.

No Levenshtein/embedding similarity in V1. Discovery ranking never changes identity.

Ties: higher relevance score -> newer latest purchase -> greater purchase count -> canonical name -> stable ID.

## 6. Filters

- category: exact category or any descendant of the selected taxonomy node;
- store: exact normalized store text, matching CP27 store-scope semantics;
- type: optional STANDARD/NON_STANDARD filter;
- text and filters combine with AND semantics.

Unknown category IDs fail explicitly rather than silently behaving as no filter.

## 7. Browse views

### Recent
One row per stable product/commodity with at least one linked receipt, newest latest-purchase first.

### Frequent
One row per stable product/commodity, purchase count descending; recency breaks ties.

### Category
Same read model filtered by selected category and descendants.

### Price change
One row per **evaluated strict CP28 cohort**, not one forced aggregate per commodity.

- contextual LIKE_FORM cohorts never appear as judged price-change rows;
- rows expose stable product ID + comparison basis + judgment + usual/latest delta;
- sort by absolute latest-vs-usual percent descending, then recency/product ID;
- one commodity may therefore have separate kg/L/each rows if such independent strict histories exist.

This prevents cross-cohort mixing.

## 8. Empty/no-result semantics

- blank text with no filters -> deterministic browse-all result;
- filters without text -> filtered browse-all;
- valid query with no matches -> empty list, never synthetic fallback;
- unclassified catalog state is not manufactured as a searchable product.

## 9. Storage/performance decision

V1 does not create a separate mutable search table/index. The read model is assembled from current canonical stores so search cannot become stale relative to receipt/catalog truth.

Reason: current catalog scale is small and correctness is cheaper than premature indexing. CP36 must benchmark representative 1k/10k histories; only measured need can justify a later index/cache design.

## 10. Acceptance

CP29 closes only if:

- exact/prefix/token search ranking is deterministic;
- canonical/structured/observed/category/store search fixtures pass;
- whitespace-compacted Korean/POS-style search works;
- category descendants browse correctly;
- store filter uses exact normalized equality;
- recent/frequent ordering is deterministic;
- price-change browse exposes only CP28 EVALUATED strict cohorts and never mixes bases;
- search does not mutate catalog/link state;
- CP21–28 targeted regressions pass;
- lint/build/permission evidence passes;
- handoff documents are synchronized.

## 11. Non-goals

- final commercial screen design;
- Compose migration;
- typo-correction/fuzzy search;
- online catalog or market search;
- barcode search;
- custom category authoring;
- full-text SQLite/FTS migration;
- changing CP28 thresholds;
- changing identity rules.
