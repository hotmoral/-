# ReceiptLedger V1 — CP24 Identity Resolver V2 Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_IDENTITY_RESOLVER_V2_01`
Branch: `receiptledger/run-v1-identity-resolver-v2-20261016`
Depends on: CP21 Catalog Domain V2, CP22 Persistence V2, CP23 Receipt Product Semantics

## 0. Product essence

ReceiptLedger must remember the same purchased product under one stable identity often enough to make personal price history useful, while refusing unsafe automatic merges that poison that history.

CP24 therefore optimizes two different failure classes at once:

- false merge: a different product is linked to an existing identity;
- false split / fragmentation: the same product cannot be recovered as an existing identity and is at risk of being duplicated.

False merge remains higher severity, but false split is a first-class measured product failure.

## 1. Scope

CP24 implements and verifies:

- deterministic Identity Resolver V2 decision objects;
- exact MERCHANT alias lookup before GLOBAL alias lookup;
- confirmed alias reuse;
- explicit contradiction guard for confirmed alias reuse;
- deterministic ranking of STANDARD catalog candidates from CP23 semantic evidence;
- a narrowly bounded strict semantic auto-link authority;
- suggestion/review path for weaker or ambiguous semantic evidence;
- unresolved path that never auto-creates a new catalog entity;
- store-backed read adapter over existing CP22 persistence without schema change;
- deterministic synthetic quality metrics including false merge, false split/fragmentation, auto-link success, incorrect auto-link, review burden, and repeat reuse.

## 2. Explicit non-goals

CP24 MUST NOT:

- change product DB schema version 2 or receipt DB schema version 1;
- merge or delete catalog rows;
- create a catalog entity automatically from a resolver miss;
- use category as identity evidence;
- infer commodity equivalence beyond exact confirmed aliases; CP26 owns commodity grouping semantics;
- use edit distance, embedding, phonetic similarity, OCR similarity, or fuzzy string similarity as auto-link authority;
- define category taxonomy;
- define price comparability/statistics;
- redesign capture/review UI;
- add network/catalog/barcode/cloud capability;
- weaken CP23 ambiguity semantics merely to improve automation rate.

## 3. Decision states

`IdentityDecisionV2` has three externally meaningful states:

- `AUTO_LINK`: resolver has sufficient authority to reuse one existing stable catalog ID;
- `REVIEW`: existing identity evidence exists but automatic authority is insufficient or conflicting;
- `UNRESOLVED`: no defensible existing candidate was found.

An unresolved decision is not permission to create a new identity without user/review flow.

## 4. Authority precedence

Resolver order is deterministic:

1. exact MERCHANT alias in the current merchant namespace;
2. exact GLOBAL alias;
3. unique strict semantic exact match;
4. ranked semantic suggestion;
5. unresolved.

MERCHANT exact alias overrides a different GLOBAL alias for the same raw string because it is the more specific confirmed namespace. The decision reason records that override.

A dangling confirmed alias fails to REVIEW and never silently falls through to another identity.

## 5. Confirmed-alias contradiction guard

A confirmed alias normally provides auto-link authority, but CP24 fails to REVIEW when current explicit semantic evidence strongly contradicts confirmed identity fields.

The guard considers only defensible explicit evidence, not the free lexical product string:

- explicit brand candidate vs confirmed brand;
- explicit variant candidate vs confirmed variant;
- non-ambiguous package specification vs confirmed specification.

This protects against stale/reused POS aliases without treating harmless lexical abbreviations as contradictions.

## 6. Strict semantic auto-link boundary

CP23 confidence alone never grants identity authority.

A STANDARD catalog candidate can become `STRICT_SEMANTIC_EXACT` auto-link only when all conditions hold:

1. CP23 result is not review-required / measure-ambiguous;
2. catalog `productName` is CONFIRMED and exactly matches normalized CP23 productName;
3. catalog specification is CONFIRMED and CP23 has the exact same deterministic specification token;
4. if either side carries brand evidence, catalog brand must be CONFIRMED and CP23 brand must be present and exact;
5. if either side carries variant evidence, catalog variant must be CONFIRMED and CP23 variant must be present and exact;
6. there is exactly one strict candidate.

Thus product name alone, HIGH parser confidence alone, category, merchant, or an unconfirmed catalog field cannot create semantic auto-link authority.

Standalone `1KG`/`1L` ambiguity from CP23 remains review-gated even when a plausible STANDARD product exists.

## 7. Semantic suggestion ranking

For STANDARD entries only, confirmed exact semantic fields contribute deterministic rank after exact product-name equality. Contradicting confirmed fields reject a candidate.

Ranking is stable across catalog iteration order; ties are resolved for display ordering by stable catalog ID but ties do not become auto-link authority.

Commodity semantic matching is deferred to CP26. Confirmed exact aliases may still recover a commodity because the alias itself is identity knowledge.

## 8. Repeat confirmation / alias learning policy

CP24 preserves least-authority learning:

- with a merchant context, a newly user-confirmed raw alias should normally be remembered in MERCHANT scope;
- GLOBAL alias creation requires an explicit global decision or a context where no merchant exists;
- migrated V1 aliases remain GLOBAL per CP22.

Once that exact confirmed alias exists, a repeated purchase should resolve automatically unless explicit current evidence contradicts it.

## 9. Quality metrics

Synthetic golden evaluation records separately:

- known-identity fixtures;
- automatic links;
- correct automatic links;
- incorrect automatic links;
- false merges;
- false split / fragmentation-risk cases where a known identity is absent from the resolver output;
- review-required cases;
- unresolved cases;
- repeat-after-confirmation cases;
- correct repeat reuse.

Acceptance targets for this bounded synthetic set:

- false merge = 0;
- incorrect automatic link = 0;
- repeat confirmed reuse = 100%;
- all alias/semantic conflicts review-gated;
- false split/fragmentation rate explicitly reported and <= 5%;
- deterministic result independent of catalog enumeration order.

These are local resolver metrics, not CP35 real-receipt accuracy claims.

## 10. Storage and compatibility

CP24 consumes existing CP22 contracts:

- `CatalogV2PersistenceStore.aliasCatalogEntryIdV2()` for context-aware exact alias lookup;
- `CatalogV2PersistenceStore.catalogEntryV2()` for V2 entity fields;
- `ProductCatalogStore.listProducts()` only as the persisted stable-ID enumeration source through a read adapter.

No table, migration, receipt persistence, price truth, permission, or network behavior changes.

## 11. Acceptance criteria

CP24 PASS requires:

1. no schema change;
2. MERCHANT-before-GLOBAL precedence tested;
3. dangling/conflicting aliases fail to review;
4. strict semantic auto-link conditions tested;
5. ambiguous standalone physical measure never semantic-auto-links;
6. weaker semantic evidence suggests/reviews rather than auto-links;
7. duplicate strict semantic candidates review rather than auto-link;
8. commodity semantic inference is not introduced;
9. deterministic candidate order/ranking tested;
10. synthetic false-merge / false-split / auto-link / review / repeat metrics emitted;
11. false merge and incorrect automatic link are zero on golden fixtures;
12. repeat reuse is 100% on golden fixtures;
13. fragmentation risk <= 5% on the bounded fixture set;
14. CP21, CP22 and CP23 unit suites still pass;
15. lint 0 errors / 0 warnings;
16. debug APK assembles and forbidden-permission audit stays clean;
17. diff is limited to CP24 identity package/tests/build metadata/workflow/docs;
18. implementation evidence is frozen before docs-only handoff synchronization.

## 12. Downstream gate

CP25 Category System may consume resolved catalog IDs, but category must never become identity authority.

CP26 may define NON_STANDARD commodity grouping. It must not reinterpret CP24 STANDARD auto-link rules or turn package-form similarity into comparability.
