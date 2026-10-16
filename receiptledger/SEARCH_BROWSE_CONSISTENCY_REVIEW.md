# ReceiptLedger V1 — CP29 Search / Browse Consistency Review

Updated: 2026-10-16 KST

## 1. Verdict

**IMPLEMENTATION ALLOWED / CONTROLLED READ-ONLY EXTENSION**

CP29 can be implemented without a schema migration and without changing identity/category/price semantics.

## 2. Upstream compatibility

### CP21 / CP24 identity
Search score, observed receipt text, category and store context are discovery metadata only. No search result can create, merge, relink or rename a catalog entity.

### CP22 persistence
Product schema remains 2 and receipt schema remains 1. CP29 reads current stores and creates no duplicate mutable search table.

### CP23 semantics
Search may display/search already-persisted structured product fields, but does not reinterpret semantic confidence or promote unconfirmed evidence into identity.

### CP25 category
Category is searchable/browsable metadata. Parent-category browse includes descendants. Category remains non-identifying.

### CP26 commodity
One commodity may contain heterogeneous purchase forms. CP29 product search groups by stable commodity ID, while price-change browse remains cohort-specific.

### CP27 price intelligence
CP29 consumes existing safe cohorts only. It cannot re-include excluded discounts/invalid receipts or combine comparison bases.

### CP28 price evaluation
Price-change browse includes only `EVALUATED` strict cohorts with a non-TYPICAL judgment. `CONTEXTUAL_ONLY`, `INSUFFICIENT_HISTORY`, `NON_POSITIVE_BASELINE` and TYPICAL are not represented as change alerts.

## 3. Alias/read-model decision

The current V2 persistence contract resolves aliases but does not enumerate them.

CP29 does **not** widen that contract solely for search. Instead, it uses observed raw receipt item names from existing stable item links as searchable discovery text.

Benefits:

- no schema/API migration;
- text remains traceable to actual receipts;
- search cannot become alias authority;
- no stale duplicate alias index.

Limitation: an alias whose source receipt/link was later deleted may no longer be discoverable by that text. This is accepted for V1 and may be reconsidered only with measured search needs.

## 4. Ranking safety

V1 uses deterministic exact/prefix/contains/token matching only. No edit-distance or embedding fuzzy search is needed for the first coherent proof.

Whitespace-compacted matching is safe because it affects discovery ranking only, not identity equality.

## 5. Browse semantics

- recent = latest purchase occasion by purchase date, then persisted creation time;
- frequent = number of distinct receipt occasions, not number of item lines or purchased quantity;
- category = exact selected category plus descendants;
- store filter = exact normalized store string, matching CP27 store scope;
- price change = one row per strict evaluated cohort with material change.

## 6. Performance boundary

CP29 deliberately performs a canonical-store scan. No speculative FTS/search cache is introduced before scale evidence exists.

Search results expose scanned and matched counts so CP36 can benchmark the linear path. A later index/cache is allowed only if representative scale demonstrates a need and cache invalidation can preserve canonical truth.

## 7. Main risks and controls

| Risk | Control |
|---|---|
| search similarity becomes merge authority | no mutating API/path in CP29 |
| observed POS text treated as confirmed alias | discovery token only |
| category used as identity evidence | filter/display only |
| partial store filter changes scope semantics | store filter exact-normalized |
| same receipt counted multiple times for frequency | distinct receipt IDs |
| NON_STANDARD bases mixed in price change | product+basis row identity |
| contextual 봉/팩/상자 shown as cheap/expensive | CP28 status gate excludes them |
| stale search table | no separate mutable index in V1 |
| final UI work pulled forward | no commercial visual redesign in CP29 |

## 8. Required regression

CP29 CI must freeze upstream packages and verify:

- product schema 2 / receipt schema 1;
- CP27 price-intelligence tests;
- CP28 evaluation tests;
- CP21–26 targeted regression suites;
- lint/build/permission evidence.

## 9. Stop condition

CP29 ends after the read-only search/browse contract, deterministic tests, evidence and handoff synchronization. CP30 Design System must not start automatically.
