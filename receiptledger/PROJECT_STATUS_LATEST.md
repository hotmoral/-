# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP21 — Catalog Domain V2 — COMPLETE**.

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- frozen CP21 implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical CP21 implementation Actions: `38808985222` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- debug APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- Catalog Domain tests: 15/15 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.19-catalog-domain-v2` / versionCode 20

CP21 executable evidence remains frozen at `8596106...` / run `38808985222`.

## 2. Client-requirement alignment amendment

Canonical docs-only amendment:

- document: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
- amendment commit: `60f40f1eba0792bbcb5a3c08aa6724b4010297bd`
- executable behavior changed: NO

Result: **current direction aligns with the client's requirement; no rollback/rewrite required.**

Mandatory downstream corrections:

1. CP24 measures both false merge and false split/identity fragmentation; false merge remains higher severity.
2. CP23–CP26 measure relevant automatic-success, review-required and repeat-confirmation reuse behavior locally.
3. CP27 defines the canonical comparison price before statistics/price labels, including quantity > 1, line amount vs per-unit/package price, item discounts, unallocated receipt-level discounts/coupons, provenance and invalid observations.
4. UI order is revised to CP29 Search/Browse -> CP30 Design System Foundation -> CP31 Product Detail -> CP32 Commodity Detail -> CP33 Capture/Review UX -> CP34 Commercial UI Shell.

## 3. CI governance maintenance after the amendment

The original CP21 workflow treated every `receiptledger/**` push as executable work and had a narrow allowlist frozen before the new canonical amendment existed.

Two docs-only pushes therefore failed at the scope guard before tests/build:

- run `38811970256` — FAILURE at `Enforce CP21 scope and frozen predecessor contracts`; first rejected path: `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`;
- run `38812118401` — FAILURE for the same stale-scope reason.

These are **not app/test/build regressions**. Test/build/evidence steps were skipped.

Minimal ReceiptLedger-only workflow maintenance commit:

- `94de4de3bef32e0165fd33810c9460ff6356b243`

Changes:

- permit the new canonical amendment/gate/risk docs in the historical CP21 scope audit;
- narrow automatic push triggers to CP21 app/catalog/test/audit/workflow paths so future handoff-only markdown changes do not waste a full Android build.

Verification run:

- `38812273375` — **SUCCESS**
- scope/public-tree audit: PASS
- unit tests: PASS
- lint: PASS
- assembleDebug: PASS
- APK permission/evidence packaging: PASS

This governance verification run does not replace canonical implementation run `38808985222`.

## 4. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

The receipt is source evidence; product/commodity history and price judgment are the user-facing destination.

## 5. CP21 frozen semantics

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

## 6. Next planned checkpoint

**CP22 — Persistence V2**.

Before schema writes CP22 must inspect:

- current receipt/product DB schemas and lifecycle;
- exact product-ID and item-link preservation;
- migration sequencing/fail-closed behavior across separate app-private DBs;
- merchant alias context storage;
- specification/category/purchase-form representation;
- query/index needs for later identity/search/history;
- direct SQLite vs Room based on concrete migration/query evidence.

CP22 must not reinterpret stable-ID authority, legacy preservation, UNCLASSIFIED semantics, category non-authority, grouping != comparability, or confidence != confirmation.

## 7. Canonical roadmap after amendment

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

## 8. Public/privacy invariants

ReceiptLedger may modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Do not use other project namespaces. Never commit secrets, signing material, real private receipt photos, personal purchase DBs/backups, personal identifiers, or uncleared assets.

APK permission firewall remains no CAMERA, broad media/storage, INTERNET, or ACCESS_NETWORK_STATE permission unless separately authorized.

## 9. Restart order

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

When comparing against frozen implementation HEAD `8596106...`, post-boundary changes are governance/docs plus the single ReceiptLedger-specific workflow trigger/scope-maintenance commit `94de4de3...`; no app source/schema/runtime change was made.

**Current stop condition: CP21 plus client-requirement alignment amendment are complete and synchronized. Await explicit authorization for CP22.**
