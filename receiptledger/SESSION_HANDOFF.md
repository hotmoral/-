# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from chat memory before reading current ReceiptLedger documents and verifying refs.

Read in this order:

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

## 1. Latest executable checkpoint

**CP21 — Catalog Domain V2 — PASS / COMPLETE**

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- frozen implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical Actions: `38808985222` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- CatalogDomainV2Test: 15/15 PASS
- lint: 0 errors / 0 warnings
- versionName `1.0.19-catalog-domain-v2`, versionCode 20

CP21 did not change persistence schema, normal UI/navigation, OCR behavior, manifest, permission model or legacy exact-alias authority.

## 2. Latest planning amendment

Client-requirement alignment review is canonical at:

`60f40f1eba0792bbcb5a3c08aa6724b4010297bd`

Document:
`CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

This is documentation-only and does not supersede the frozen CP21 implementation boundary.

## 3. Product essence

ReceiptLedger exists to make personal purchase-price memory automatic and trustworthy.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색 -> 과거 가격과 현재 가격 판단`

A receipt is evidence/input. Product and commodity price history are the primary user destination.

## 4. CP21 semantics that CP22 must not reinterpret

- stable catalog ID is catalog identity/equality authority;
- legacy product IDs/names/types migrate without semantic guessing;
- UNCLASSIFIED remains unresolved rather than a V2 entity;
- category is not identity proof;
- merchant context scopes aliases but does not define SKU identity;
- HIGH confidence != CONFIRMED;
- unknown != invented default;
- exact physical units may canonicalize only when mathematically exact;
- BAG/PACK/BOX/BUNDLE do not get guessed physical conversion;
- NON_STANDARD grouping != price comparability;
- price truth remains traceable to saved receipt evidence.

## 5. Downstream amendments now mandatory

### Identity quality

CP24 must measure both false merge and false split/identity fragmentation. False merge remains more dangerous, but fragmented same-product history is also a core failure.

### Automation quality

CP23–CP26 must measure relevant automatic-success, review-required and repeat-confirmation reuse behavior locally. Accuracy alone is not enough if the user must repeatedly relink known products.

### Comparison-price contract

CP27 must define the canonical comparison price before statistics or price labels. Quantity > 1, line total vs one purchased unit/package, item discounts, unallocated receipt-level discounts/coupons, provenance and invalid observations must be explicit.

### UI order

Future order is:

CP29 Search/Browse
-> CP30 Design System Foundation
-> CP31 Product Detail
-> CP32 Commodity Detail
-> CP33 Capture/Review UX V2
-> CP34 Commercial UI Shell.

Do not build final-looking detail screens before CP30 visual foundations.

## 6. Next planned implementation checkpoint

**CP22 — Persistence V2**

Before schema writes:

1. inventory current receipt/product DB schemas and lifecycle;
2. preserve all existing product IDs and item links;
3. design fail-closed migration sequencing across separate DBs;
4. store merchant alias context and CP21 structured semantics without duplicating receipt price truth;
5. design indexes for future resolver/search/history requirements;
6. decide direct SQLite vs Room from actual evidence;
7. write migration regression vectors before irreversible operations.

CP22 is not authorized merely because it is planned.

## 7. Group discipline

For every checkpoint:

- recover canonical state;
- restate essence/non-goals;
- inspect materially affected contradictions and risks;
- fix cheap contract problems before implementation;
- avoid unrelated cleanup and ritual re-audits;
- implement the smallest coherent proof;
- run ReceiptLedger-scoped CI/evidence when executable changes exist;
- freeze exact refs;
- synchronize handoff/status material;
- stop before the next unauthorized group.

## 8. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Never use other project namespaces or commit secrets, signing material, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

APK permission firewall remains no CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permission unless separately authorized.

## 9. Stop condition

**CP21 is complete. Client-requirement alignment amendment is synchronized. Await explicit authorization for CP22.**
