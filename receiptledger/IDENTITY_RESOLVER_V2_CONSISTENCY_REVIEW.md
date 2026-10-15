# ReceiptLedger V1 — CP24 Identity Resolver V2 Consistency Review

Updated: 2026-10-16 KST

## 1. Question

Can CP24 add useful automatic identity reuse without contradicting CP21 stable-ID authority, CP22 migration/persistence guarantees, CP23 unconfirmed parsing semantics, or the client's automation objective?

## 2. Upstream compatibility

### CP21

Preserved:

- stable catalog ID remains entity identity/equality authority;
- same semantic fields do not merge entities;
- HIGH confidence is not confirmation;
- category and merchant are not SKU identity;
- grouping and comparability stay distinct.

CP24 uses semantic fields as evidence for a link decision to an existing stable ID. It does not redefine entity equality or merge rows.

### CP22

Preserved:

- product database remains schema 2;
- receipt database remains schema 1;
- legacy IDs and item links remain untouched;
- legacy aliases remain GLOBAL;
- merchant alias namespaces are already persisted;
- price/date/store/validation remain receipt-derived.

No migration is needed for CP24.

### CP23

Preserved:

- parsed fields remain PARSED_FROM_RECEIPT / UNCONFIRMED;
- standalone physical measures retain ambiguity;
- parser does not emit stable IDs;
- parser confidence alone cannot authorize a link.

CP24 may combine unconfirmed current evidence with previously CONFIRMED catalog knowledge. This is downstream evidence use, not retroactive confirmation of CP23 output.

## 3. False-merge review

Highest-risk automatic decisions are limited to:

1. exact confirmed alias lookup; or
2. one unique strict semantic candidate with confirmed product name + confirmed exact specification and any present brand/variant symmetrically confirmed and exact.

Mitigations:

- fuzzy similarity never auto-links;
- category never participates;
- ambiguity blocks semantic auto-link;
- duplicate strict candidates block semantic auto-link;
- explicit current brand/variant/spec contradiction can downgrade even a confirmed alias to REVIEW;
- no resolver path auto-creates a new identity.

Result: false-merge surface is deliberately narrow.

## 4. False-split / fragmentation review

A system that only avoids merges can still fail the product by splitting repeat history. CP24 addresses this through:

- exact confirmed alias reuse;
- merchant-aware namespaces;
- deterministic existing-product suggestions for weaker semantic evidence;
- strict semantic reuse when evidence is complete enough;
- no automatic creation on unresolved evidence;
- explicit fragmentation-risk metric.

Review is not itself counted as a false split when the correct existing catalog ID is presented as a candidate, because the review flow can preserve the existing identity. UNRESOLVED known products or review results omitting the correct identity are fragmentation risks.

## 5. MERCHANT vs GLOBAL alias conflict

A merchant-scoped alias is intentionally more specific than a global alias. Therefore:

- exact MERCHANT match is checked first;
- different GLOBAL mapping does not override it;
- the decision records the merchant override;
- if the merchant alias is dangling or semantically contradicted by strong explicit current evidence, resolution stops at REVIEW instead of falling through.

This prevents a broad GLOBAL alias from poisoning a known store-specific POS meaning.

## 6. Alias staleness / POS reuse

Confirmed aliases are strong but not infallible over time. A store can reuse or change POS labels.

CP24 therefore checks only high-value explicit contradictions:

- bracket/known brand evidence against confirmed brand;
- explicit variant evidence against confirmed variant;
- non-ambiguous package specification against confirmed specification.

The free lexical product name is not used to veto a confirmed alias because abbreviations are precisely why aliases exist.

## 7. Semantic auto-link sufficiency

Product-name equality alone is insufficient because package size/count is central to the client's identical-product price history.

CP24 therefore requires confirmed exact specification for semantic auto-link. This directly protects cases such as 5입 vs 10입, 500mL vs 1L, or 600g vs 1kg.

If specification is missing or ambiguous, the resolver can suggest an existing product but cannot semantic-auto-link it.

## 8. NON_STANDARD boundary

CP24 does not invent commodity matching rules. A commodity can auto-resolve only through existing confirmed exact aliases in CP24. Semantic commodity grouping is deferred to CP26, where mixed purchase forms can be handled explicitly without leaking STANDARD SKU assumptions.

## 9. Automation burden

The client wants repeat purchases to become nearly automatic. CP24 therefore treats `confirmed once -> reused next time` as an explicit acceptance behavior, not a side effect.

Least-authority confirmation policy avoids unsafe global learning:

- merchant context -> MERCHANT alias by default;
- explicit global confirmation -> GLOBAL alias;
- no merchant context -> GLOBAL fallback.

This may require first-time review for a new store-specific POS form, but repeated occurrences should stop requiring review.

## 10. Performance review

Catalog enumeration is linear for semantic ranking. This is acceptable for the current V1 scope and small personal catalog, and avoids premature indexing/schema work. CP36 will evaluate large-catalog performance. Exact alias lookup remains indexed through CP22 persistence.

No new network, OCR pass, bitmap, or receipt DB query is introduced by the pure resolver.

## 11. Security/privacy review

No new permissions, external data source, internet access, analytics, receipt images, personal fixtures, credentials, or non-ReceiptLedger namespace dependencies are introduced.

## 12. Conclusion

CP24 is consistent with the client requirement and upstream contracts if automatic authority remains narrow, both false merge and fragmentation are measured, and review is used as a controlled safety state rather than treated as failure to automate at any cost.

No upstream amendment or schema change is required.
