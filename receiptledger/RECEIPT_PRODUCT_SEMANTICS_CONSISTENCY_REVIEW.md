# ReceiptLedger V1 — CP23 Receipt Product Semantics Consistency Review

Updated: 2026-10-16 KST

## 1. Review conclusion

**PASS TO IMPLEMENT.** CP23 can be added as a pure semantic-candidate layer without changing CP21 identity meaning or CP22 persistence meaning.

The cheapest safe implementation is additive: parse the existing receipt item name into unconfirmed evidence objects and leave linking/persistence authority unchanged.

## 2. Upstream consistency checks

### Item Tuple Core

Compatible. Existing `ItemTuple.name` remains the parser input. Quantity/unit price/line amount and their `ValueOrigin` are not reinterpreted.

### Validation Core

Compatible. Product semantic parsing does not change receipt arithmetic validity and cannot repair contradictory prices.

### Review/Edit Core

Compatible. CP23 introduces semantic review reasons but does not bypass the requirement that ambiguous user-facing data can be reviewed before trusted use.

### Product Identity Core / CP21

Compatible if and only if parsed fields remain evidence, not identity authority. Stable catalog ID remains authoritative. `HIGH != CONFIRMED` remains frozen.

### CP22 Persistence V2

Compatible. No schema migration is required. CP22 already supports eventual persistence of semantic fields and purchase forms, but CP23 does not attach a parsed candidate to a catalog row before identity is resolved.

## 3. False-merge perspective

Primary hazard: treating a good-looking parse as proof of SKU identity.

Control:

- no catalog ID is emitted;
- no resolver call is made;
- no alias is created;
- `SemanticCandidate.asCatalogField()` always creates `PARSED_FROM_RECEIPT / UNCONFIRMED` evidence.

## 4. False-split perspective

Overly weak parsing can fragment later histories by giving CP24 too little evidence.

Control:

- preserve lexical product name even when brand/variant cannot be separated;
- parse exact package count/multipack evidence when available;
- support caller-supplied confirmed/known brand knowledge without hard-coding brand authority into identity;
- report field recall and review burden locally.

Unknown brand remains a known limitation and is measured rather than hidden.

## 5. STANDARD vs NON_STANDARD perspective

The dangerous case is a physical unit such as `1KG` or `1L`.

Examples:

- `왕교자 1.05KG` can be packaged net content;
- `감자 1KG` can be a commodity purchase amount.

CP23 has no safe catalog-kind authority at this point. Therefore standalone physical measures are deliberately represented as dual candidates plus ambiguity/review. This preserves both future paths without inventing a kind.

## 6. Pack-count perspective

`입` / `개입` is strong package-count evidence and may be represented as ProductSpecification.

`개` alone is not equivalent to `개입`: it can mean purchased pieces. It remains purchase-form evidence with ambiguity.

`팩` is similarly context-sensitive and remains review-gated.

## 7. Brand perspective

Generic first-token-as-brand parsing was rejected.

Reason: POS names frequently begin with abbreviations, product-family names, store-specific codes or truncated labels. Declaring a brand from position alone would increase false semantics and later false merge risk.

CP23 permits only:

- explicit bracketed brand evidence;
- caller-supplied known-brand prefix knowledge.

This intentionally sacrifices some first-time brand recall for correctness. CP24/CP35 must later measure whether additional local knowledge is justified.

## 8. Variant perspective

Generic flavor/model suffix splitting was rejected for CP23. `진라면 매운맛`, for example, is kept as a lexical product name unless the variant is explicitly delimited such as `(매운맛)`.

Reason: arbitrary lexical splitting is language/domain knowledge, not a cheap deterministic parser rule.

## 9. Persistence perspective

No DB migration is justified.

- Product catalog schema stays 2.
- Receipt schema stays 1.
- Raw item text stays intact.
- No price/date/store truth is copied.

## 10. UI perspective

No UI redesign belongs here. CP23 produces machine-readable review reasons only. CP33 later owns user-facing review interaction.

## 11. Performance perspective

Parser is bounded regular-expression/string logic over one short item name. No OCR rerun, DB scan, network call or fuzzy catalog search is introduced.

## 12. Security/privacy perspective

No new permission, network, file access, private fixture or external service is required. Golden strings are synthetic/public-safe.

## 13. Scope-control decision

Rejected as over-broad for CP23:

- external product/brand databases;
- embedded exhaustive Korean brand catalogs;
- ML/NLP model introduction;
- catalog merge logic;
- category inference;
- UI integration;
- barcode support;
- Room migration;
- price normalization.

These do not advance the narrow checkpoint enough to justify their cost/risk now.

## 14. Required local evidence

Before CP23 closes:

- semantic parser unit/golden tests;
- field precision/recall report from actual parser outputs;
- review/ambiguity metrics;
- all CP21/CP22 regression tests;
- lint/build/permission evidence;
- exact diff showing schemas and prior product/persistence runtime were not modified.
