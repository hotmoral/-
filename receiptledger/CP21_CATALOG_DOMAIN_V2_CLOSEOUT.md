# ReceiptLedger V1 — CP21 Catalog Domain V2 Closeout

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_CATALOG_DOMAIN_V2_01`
Result: **PASS / COMPLETE**

## 1. Frozen implementation

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- predecessor CP20 handoff HEAD: `3149beb339a2d541a61a694fb1f052556a95c8c1`
- frozen implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical Actions run: `38808985222` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- debug APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- lint: 0 errors / 0 warnings
- CP21 domain tests: 15/15 PASS

## 2. What CP21 completed

CP21 introduced a storage-independent pure-Java Catalog Domain V2 alongside the legacy runtime. It froze:

- `STANDARD_PRODUCT` vs `NON_STANDARD_COMMODITY` boundaries;
- legacy STANDARD/NON_STANDARD compatibility and UNCLASSIFIED fail-closed behavior;
- stable catalog ID as the only catalog-entity equality authority;
- structured STANDARD semantic fields without making them merge authority;
- exact package specification and pack-count semantics;
- raw purchase-form representation for mixed non-standard goods;
- stable category references without freezing taxonomy;
- global vs merchant-scoped alias namespace context;
- independent source / confidence / confirmation state;
- logical receipt-linked purchase-observation contract;
- fail-closed legacy adaptation preserving IDs and avoiding semantic guessing.

## 3. Frozen invariants for CP22 and later

The following must not be reinterpreted implicitly:

1. Existing catalog IDs remain authoritative and must survive migration unchanged.
2. Different IDs do not become the same product merely because semantic fields match.
3. Legacy canonical names are not automatically parsed into authoritative brand/specification during migration.
4. UNCLASSIFIED remains unresolved absence of catalog identity.
5. Category is browse metadata, not product-identity proof.
6. Merchant scope is alias context, not product SKU identity and not a rewrite of historical store evidence.
7. HIGH confidence is not the same as CONFIRMED.
8. Exact kg/g and L/mL equivalence is allowed only as exact physical package measurement.
9. 봉/팩/박스/상자-style sales forms are not silently convertible physical units.
10. NON_STANDARD grouping does not imply price comparability.
11. Unknown pack count remains unknown; it is not silently defaulted to 1.
12. Purchase price truth remains traceable to canonical saved receipts + links.
13. CP21 does not create a second persisted price-observation truth source.
14. Existing OCR, validation, review, privacy and API36 foundations remain preserved.

Changing any of these later requires an explicit canonical amendment explaining the reason and downstream impact.

## 4. Explicitly not done

CP21 did not:

- change product catalog SQLite schema/version;
- migrate user data;
- modify legacy `product/**` runtime behavior;
- change exact-alias auto-link authority;
- implement receipt semantic parsing;
- implement Identity Resolver V2;
- freeze category taxonomy;
- define price statistics or cheap/normal/expensive thresholds;
- change Activities/UI/navigation;
- add network or permissions.

These omissions are dependency boundaries, not unfinished CP21 work.

## 5. Consistency conclusion

Review result: **COMPATIBLE / NO BLOCKING CONTRADICTION**.

The additive domain-layer strategy avoids the high-cost failure modes identified in CP20:

- identity poisoning from premature semantic equality;
- old-product collapse during migration;
- merchant alias collisions;
- fake unit normalization;
- confidence being mistaken for confirmation;
- duplicate price truth;
- UI/storage changes before domain meaning is stable.

## 6. Next planned checkpoint

**CP22 — Persistence V2**

Its task is to design and implement migration-safe storage/indexing for the frozen CP21 meaning. It must begin with an inventory of current schema/data relationships, migration strategy, rollback/fail-closed behavior, and direct-SQLite-vs-Room decision based on concrete migration/runtime needs.

CP22 must not begin automatically. It requires explicit user authorization.

## 7. Stop condition

CP21 closes after canonical status/handoff synchronization and verification that post-implementation changes are documentation-only.
