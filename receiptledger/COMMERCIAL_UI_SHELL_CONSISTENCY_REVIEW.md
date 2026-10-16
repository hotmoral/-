# ReceiptLedger V1 — CP34 Commercial UI Shell Consistency Review

Updated: 2026-10-16 KST
Status: PRE-IMPLEMENTATION REVIEW

## 1. Predecessor verification

Canonical handoff is `2a15e14e9897aa9785762faef1568254fbeb5f82` and its direct parent is frozen CP33 executable `34cdac2d3e61081ab2a529173dbef9a2431431e0`.

CP34 branches from the handoff commit, not from chat reconstruction.

## 2. Material consistency checks

### Identity
PASS boundary: navigation may consume stable product IDs but must not create, merge, relink or confirm identity. Search relevance/category/price cannot become identity evidence.

### Price
PASS boundary: shell may display CP29 browse metadata and route to CP31/32 detail. It must not compute a new cheap/expensive judgment or mix comparison bases.

### Review/capture
PASS boundary: CP33 MainActivity remains the authoritative add-receipt flow. Home only enters it; CP34 does not reinterpret save readiness or provenance.

### Persistence
PASS boundary: no new truth table, no schema migration, no duplicated price facts. Existing SQLite stores are opened read-only by search/home services except existing destination behavior.

### Commodity
PASS boundary: NON_STANDARD navigation goes to CP32 and keeps strict normalized cohorts separate from contextual package-form reference history.

### Privacy
PASS boundary: no new permission or network requirement. Launcher/navigation must not require INTERNET or broad storage/media permissions.

### Design
PASS boundary: programmatic android.widget and CP30 UiKit remain. No Compose/Material migration.

## 3. Legacy path risk

`LibraryActivity` currently exposes `PriceHistoryActivity` as a prominent product browse path. That screen is a legacy mixed product list/detail harness and is no longer the correct primary commercial route after CP31/32 and CP29.

CP34 should remove that primary dependency from Library while preserving the class for backward/internal compatibility unless deletion is necessary. New discovery must flow through SearchBrowseActivity and the frozen CP29 service.

## 4. Launcher risk

Current launcher is CP33 MainActivity. That makes capture look like the entire app and hides the core price-memory outcome.

Resolution: add HomeActivity as launcher and make MainActivity non-exported internal destination. This changes only navigation/export posture, not capture truth.

## 5. Search service wiring risk

`SearchBrowseServiceV1` requires ReceiptStore, ProductCatalogStore, CatalogV2PersistenceStore, PriceIntelligenceServiceV2 and PriceEvaluationServiceV1. `SqliteProductCatalogStore` implements both catalog interfaces, so one catalog instance can be safely passed to both positions without a second authority.

No new search algorithm is needed.

## 6. Category risk

Category taxonomy is bounded and frozen in CP25. UI may browse `roots()/children()/byCategory()` but must not author arbitrary categories or use category membership to alter identity.

## 7. Performance risk

CP29 currently scans canonical stores. CP34 must use small bounded result limits and not add indexes/caches speculatively. Scale optimization remains CP36 after measurement.

## 8. UI-state risk

Home/search must have explicit loading, empty and failure states. A service exception must not silently imply that no products exist.

Long content must scroll and primary actions must remain reachable.

## 9. Conclusion

CP34 is consistent with CP20–33 if implemented as a thin integration/presentation layer over frozen APIs. No domain rollback, schema change or authority expansion is justified.
