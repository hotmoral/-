# ReceiptLedger V1 — CP29 Search / Browse Golden Vectors

Updated: 2026-10-16 KST

## G01 Canonical exact

Query `서울우유 나100% 1L` against canonical product of the same name.

Expected: one result, `CANONICAL_EXACT`, top rank.

## G02 Whitespace-compacted discovery

Stored/canonical text contains `서울우유`; query contains `서울 우유`.

Expected: same product remains discoverable. This affects search only, never identity.

## G03 Structured specification

Product specification `1 L` must expose a searchable equivalent `1000ML` token.

Expected: searching `1000ML` finds the product through structured metadata.

## G04 Observed POS text

Stable product has linked receipt item text `특가우유1000`.

Expected: exact observed search finds the product. Catalog/link counts remain unchanged after search.

## G05 Store discovery vs store filter

Observed store `이마트 강서`.

Expected:

- text search can find through store context;
- store filter `이마트   강서` matches after normalization;
- store filter `이마트` does **not** partially match.

## G06 Category descendants

Products in `FOOD_DAIRY_MILK` and `FOOD_NOODLES_RAMEN`.

Expected:

- browse `FOOD` returns both;
- browse `FOOD_DAIRY` returns only milk descendant.

## G07 Recent vs frequent

A product has 3 older receipt occasions. Another has 1 newer receipt occasion.

Expected:

- recent -> newer product first;
- frequent -> 3-occasion product first;
- multiple item lines in one receipt would still count as one occasion.

## G08 Blank/no-result

Expected:

- blank query returns browse-all after filters;
- unknown text returns empty list;
- diagnostics expose scanned/matched/returned counts.

## G09 Price-change status gate

Three histories:

- STANDARD material increase -> EVALUATED/EXPENSIVE;
- STANDARD within material band -> TYPICAL;
- commodity BAG history -> CONTEXTUAL_ONLY.

Expected price-change browse: only material STANDARD row.

## G10 Multi-basis commodity separation

One `감자` commodity has independent `WEIGHT_KG` and `EACH` strict histories, both with material change.

Expected: two price-change rows sharing product ID but carrying different basis keys. No mixed aggregate row.

## G11 Deterministic ordering

Same data and query repeated.

Expected order: relevance -> purchase recency -> purchase occasion count -> canonical name -> stable ID.

## G12 Read-only invariant

After arbitrary search/browse calls:

- product count unchanged;
- item links unchanged;
- no alias/category/specification write;
- no receipt write;
- no price/evaluation write.

## Canonical metric fixture

Expected line:

`CP29_METRICS documents=3 exact_hits=1 compact_hits=1 observed_hits=1 category_rows=3 store_rows=1 recent_rows=3 frequent_rows=3 no_result_rows=0 mutation_checks=1 diagnostics_scanned=3`

This is deterministic synthetic contract evidence, not real-world search-quality accuracy.
