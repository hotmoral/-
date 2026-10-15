# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct ReceiptLedger execution state from old chat before reading current files and verifying refs.

Read in order:

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
- canonical implementation Actions: `38808985222` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- CatalogDomainV2Test: 15/15 PASS
- lint: 0 errors / 0 warnings
- versionName `1.0.19-catalog-domain-v2`, versionCode 20

CP21 app/source/schema/runtime semantics remain frozen at this boundary.

## 2. Client requirement alignment amendment

Canonical amendment commit:
`60f40f1eba0792bbcb5a3c08aa6724b4010297bd`

Document:
`CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

Finding:
**current direction matches the client's requirement; no rollback/rewrite is required.**

Mandatory downstream corrections:

- CP24 measures false merge and false split/identity fragmentation;
- CP23–CP26 measure automatic-success, review-required and repeat-confirmation reuse where relevant;
- CP27 defines canonical comparison-price semantics before statistics/labels;
- final commercial screen work follows CP30 Design System Foundation.

## 3. CI governance maintenance

Two amendment/handoff pushes initially failed because the frozen CP21 scope allowlist did not know the new canonical docs:

- `38811970256` — FAILURE at scope guard; first rejected path `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`;
- `38812118401` — FAILURE for the same stale-scope class.

Tests/build were skipped, so these are not app regressions.

Minimal workflow maintenance commit:
`94de4de3bef32e0165fd33810c9460ff6356b243`

It only:

1. adds the amendment/gate/risk docs to CP21 scope audit;
2. narrows automatic push triggers to CP21 code/test/audit/workflow paths so docs-only handoff edits stop causing unnecessary Android builds.

Verification:

- run `38812273375` — **SUCCESS**
- scope/public-tree audit PASS
- unit test PASS
- lint PASS
- assembleDebug PASS
- permission/evidence packaging PASS

Do not replace canonical implementation evidence `38808985222` with this governance verification run.

## 4. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색 -> 과거 가격과 현재 가격 판단`

Receipt is evidence/input; product/commodity history is the main destination.

## 5. CP21 semantics CP22 must preserve

- stable catalog ID = catalog identity/equality authority;
- legacy product IDs/names/types migrate without semantic guessing;
- UNCLASSIFIED remains unresolved, not a V2 entity;
- category is not identity proof;
- merchant scope contextualizes aliases but does not define SKU identity;
- HIGH confidence != CONFIRMED;
- unknown != invented default;
- exact unit canonicalization only where mathematically/physically exact;
- BAG/PACK/BOX/BUNDLE have no guessed conversion;
- grouping != comparability;
- price truth remains receipt-traceable.

## 6. Downstream acceptance amendments

### Identity

CP24 must report both false merge and false split. False merge remains more severe, but split histories are also failure.

### Automation

Repeated confirmed use should reduce review burden. Local quality evidence begins in CP23–CP26 rather than waiting until CP35.

### Price basis

CP27 must explicitly define the comparable price per purchase observation, including quantity > 1, line total vs per-unit/package amount, item discount, unallocated receipt-level discount/coupon, provenance and invalid/incomplete data.

### UI order

CP29 Search/Browse
-> CP30 Design System Foundation
-> CP31 Product Detail
-> CP32 Commodity Detail
-> CP33 Capture/Review UX V2
-> CP34 Commercial UI Shell.

## 7. Next planned implementation checkpoint

**CP22 — Persistence V2**

Before schema writes:

1. inventory current receipt/product DB schemas and lifecycle;
2. preserve every existing product ID and item link;
3. design fail-closed migration sequencing across separate DBs;
4. store merchant alias scope and CP21 structured semantics without duplicating receipt price truth;
5. design indexes for later resolver/search/history work;
6. decide direct SQLite vs Room from concrete requirements;
7. create migration regression vectors before irreversible operations.

CP22 is planned, not automatically authorized.

## 8. Group discipline

For every group:

- recover canonical state;
- state essence/non-goals;
- inspect materially relevant contradictions/risk only;
- fix cheap contract problems before implementation;
- avoid unrelated cleanup and ritual re-audits;
- implement the smallest coherent proof;
- run ReceiptLedger-scoped CI/evidence where executable changes exist;
- freeze exact refs;
- synchronize handoff/status materials;
- stop before the next unauthorized checkpoint.

## 9. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Never use other project namespaces or commit secrets, signing material, real private receipt photos, personal purchase databases/backups, personal identifiers or uncleared assets.

APK permission firewall remains no CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permission unless separately authorized.

## 10. Stop condition

**CP21 plus the client-requirement alignment amendment are complete and synchronized. Await explicit authorization for CP22.**
