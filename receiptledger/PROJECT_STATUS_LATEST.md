# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP21 — Catalog Domain V2 — COMPLETE**.

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- frozen CP21 implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical CP21 Actions: `38808985222` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- debug APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- Catalog Domain tests: 15/15 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.19-catalog-domain-v2` / versionCode 20

Latest canonical planning amendment:

- `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
- amendment commit: `60f40f1eba0792bbcb5a3c08aa6724b4010297bd`
- type: documentation-only
- executable behavior changed: NO

CP21 implementation semantics remain frozen at `8596106...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

The receipt is source evidence; product/commodity history and price judgment are the destination.

## 3. CP21 frozen meanings

- `STANDARD_PRODUCT`: repeatable packaged/manufactured commercial identity;
- `NON_STANDARD_COMMODITY`: semantic commodity/item with potentially mixed raw purchase forms;
- UNCLASSIFIED remains unresolved, not a V2 catalog entity;
- stable catalog ID is entity equality authority;
- semantic similarity/category/store context do not silently merge entities;
- source/confidence/confirmation are independent;
- HIGH confidence != CONFIRMED;
- exact kg/g and L/mL package equivalence is allowed only where physically exact;
- BAG/PACK/BOX/BUNDLE have no guessed physical conversion;
- grouping != price comparability;
- purchase observations remain receipt-linked, not a second independent price truth store.

Legacy `ProductCatalogSchema.VERSION` remains 1. Persistence migration has not started.

## 4. Client-requirement alignment amendment

Post-CP21 review found the overall direction aligned with the client's request. No rollback/rewrite is required.

Four downstream amendments are now canonical:

1. **False split is a first-class quality risk.** CP24 must measure false merge and false split/identity fragmentation. False merge remains the higher-severity error.
2. **Automation/review burden is a product metric.** CP23–CP26 must measure relevant automatic-success, review-required and repeat-confirmation reuse behavior locally rather than waiting until CP35.
3. **CP27 must define the canonical comparison price before statistics.** It must explicitly handle quantity > 1, line amount vs per-unit/package amount, item-specific discounts, unallocated receipt-level discounts/coupons, provenance and invalid observations.
4. **Design System moves ahead of final commercial detail screens.** Future UI order is CP29 Search/Browse -> CP30 Design System -> CP31 Product Detail -> CP32 Commodity Detail -> CP33 Capture/Review UX -> CP34 Commercial UI Shell.

## 5. Next planned checkpoint

**CP22 — Persistence V2**.

CP22 must implement migration-safe storage/indexing for CP21 semantics while preserving the alignment amendment.

Before schema writes CP22 must inspect:

- current receipt/product DB schemas and lifecycle;
- exact product-ID and item-link preservation;
- migration sequencing/fail-closed behavior across separate app-private DBs;
- merchant alias context storage;
- specification/category/purchase-form representation;
- query/index needs for later identity/search/history;
- direct SQLite vs Room based on concrete migration/query evidence.

CP22 must not reinterpret stable-ID authority, legacy preservation, UNCLASSIFIED semantics, category non-authority, grouping != comparability, or confidence != confirmation.

## 6. Canonical roadmap after amendment

CP22 Persistence V2
-> CP23 Receipt Product Semantics
-> CP24 Identity Resolver V2
-> CP25 Category System
-> CP26 Commodity / Non-standard V2
-> CP27 Price Intelligence V2
-> CP28 Price Evaluation
-> CP29 Search / Browse
-> CP30 Design System Foundation
-> CP31 Product Detail
-> CP32 Commodity Detail
-> CP33 Capture / Review UX V2
-> CP34 Commercial UI Shell
-> CP35 Real Receipt Evaluation
-> CP36 Performance / Reliability

## 7. Public/privacy invariants

ReceiptLedger may modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Do not use other project namespaces. Never commit secrets, signing material, real private receipt photos, personal purchase DBs/backups, personal identifiers, or uncleared assets.

APK permission firewall remains no CAMERA, broad media/storage, INTERNET, or ACCESS_NETWORK_STATE permission unless separately authorized.

## 8. Restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
4. `receiptledger/CATALOG_DOMAIN_V2_PLAN.md`
5. `receiptledger/CATALOG_DOMAIN_V2_CONSISTENCY_REVIEW.md`
6. `receiptledger/PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
7. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `receiptledger/CP20_PRODUCT_REBASELINE_DEPENDENCY_GATES.md`
9. `receiptledger/CP20_PRODUCT_REBASELINE_RISK_REGISTER.md`
10. `receiptledger/README.md`
11. `receiptledger/WORK_UNIT.md`

Verify any commit after frozen implementation HEAD `8596106c370e172161ef00e8d460dc78667bf80d` is documentation-only unless a later checkpoint was explicitly authorized.

**Current stop condition: CP21 is complete and the client-requirement alignment amendment is synchronized. Await explicit authorization for CP22.**
