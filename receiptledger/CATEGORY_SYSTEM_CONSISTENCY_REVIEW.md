# ReceiptLedger V1 — Category System Consistency Review

Updated: 2026-10-16 KST

## 1. Review question

Does CP25 add useful automatic/category browsing behavior without weakening the product-identity, persistence, price-evidence or privacy contracts frozen in CP21–CP24?

Result: **YES, with the bounded design in CP25 plan.**

## 2. Identity consistency

Frozen rule: stable catalog ID is identity authority. Category is not.

CP25 preserves this structurally:

- category code consumes a resolved `CatalogEntryV2`;
- CP24 identity package is frozen by CI diff guard;
- category classifier has no alias/link/merge/create API;
- category assignment rehydrates the same stable catalog ID and changes only `CategoryRef`;
- category cannot override MERCHANT/GLOBAL alias or strict semantic identity decisions.

Therefore a wrong category can create browse inconvenience but cannot poison price history by merging products.

## 3. Persistence consistency

CP22 already provisioned `category_refs` and `idx_category_refs_category` under product schema 2. No schema change is required.

The existing table has no category decision provenance fields. CP25 deliberately keeps suggestions transient and persists only an effective assignment after acceptance. This avoids speculative schema growth while still supporting correction and repeat reuse.

Risk: later analytics may want to distinguish auto-accepted from explicitly user-confirmed category assignments. That is a future metadata/provenance concern, not a prerequisite for CP25 behavior. Do not silently reinterpret it as identity evidence.

## 4. CP23 semantic consistency

CP23 receipt semantics remain unconfirmed and are not modified.

CP25 classification uses stable catalog text/fields for browse metadata. Because category is lower-authority metadata, this does not convert CP23 parser confidence into identity authority. Weak/generic category rules are review-gated.

## 5. CP24 resolver consistency

CP24 explicitly states category is not identity proof. CP25 introduces no call path from resolver to category system.

CI freezes `com.receiptledger.v1.identity/**` and all CP24 tests remain required. Any future attempt to feed category back into identity resolution requires an explicit contract amendment.

## 6. False merge / false split perspective

Category does not directly solve CP24 false merge or false split and must not be used as a shortcut to do so.

A category such as `우유` may contain many different SKUs. Treating category co-membership as identity evidence would be a severe false-merge risk. CP25 forbids that.

Conversely, two fragmented identities may receive the same category and remain fragmented. Category agreement does not authorize a merge.

## 7. Automation / review perspective

The client wants minimal manual work. CP25 therefore distinguishes:

- strong unique local rule -> AUTO_ASSIGNABLE;
- existing effective category -> REUSE_PERSISTED;
- generic/conflicting rule -> REVIEW;
- no evidence -> UNRESOLVED.

This preserves automation where classification risk is low without forcing every item into a category.

Persisted category reuse is keyed by stable catalog ID. Once accepted/corrected, repeat purchases that resolve to that ID do not require reclassification.

## 8. Taxonomy scope review

A large retail taxonomy would be premature and expensive to maintain before search/browse UI exists. A tiny flat taxonomy would not support the client's category browsing requirement.

The selected middle ground is a bounded 28-node hierarchy over common food/household repeat purchases. Stable machine IDs are separated from Korean display labels.

Not included now:

- custom user categories;
- tags/multi-category membership;
- deep retail department taxonomy;
- store-specific taxonomies;
- online category catalogs.

These omissions reduce scope without blocking later extension.

## 9. Non-standard goods consistency

CP25 may classify a known commodity such as 감자 into `FOOD_PRODUCE_VEGETABLE`, but this does not define whether 감자 1봉 and 감자 1kg are comparable. CP26 remains responsible for commodity grouping/forms, and CP27 for comparison-price eligibility.

`grouping != comparability` remains frozen.

## 10. Price/history consistency

Category tables store no price/date/store data. Receipt storage remains authoritative for purchase facts. Category correction therefore cannot rewrite historical price evidence.

## 11. Privacy/security consistency

CP25 is offline deterministic logic. It adds no network dependency, permission, cloud catalog, analytics SDK or private fixture requirement.

Public fixtures contain synthetic product strings only.

## 12. Performance perspective

The taxonomy is fixed and small. Rule evaluation is bounded string matching over one catalog entry. Persisted category lookup continues to use the existing indexed `category_refs` table. No new unbounded scan or expensive model is introduced.

## 13. Primary risks and mitigations

### R1 — taxonomy overfitting
Mitigation: small practical categories, unresolved fallback, future extension only from observed need.

### R2 — wrong auto category
Mitigation: only unique high-confidence rules are auto-assignable; conflicts/generic evidence review-gated; corrections overwrite assignment.

### R3 — category becomes hidden identity evidence
Mitigation: identity package frozen, no category dependency, explicit contract/test/CI guard.

### R4 — correction fails to stick
Mitigation: assignment persists on stable catalog ID and reuse is a required golden metric.

### R5 — forced `OTHER` hides uncertainty
Mitigation: no forced OTHER bucket; unsupported evidence stays unresolved.

## 14. Final assessment

CP25 is coherent with the client's request and the frozen upstream architecture if it remains a browse/classification layer over resolved identities. No DB migration, identity redesign or UI expansion is justified in this group.
