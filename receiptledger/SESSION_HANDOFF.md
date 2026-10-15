# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct ReceiptLedger execution state from old chat before reading current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_CLOSEOUT.md`
4. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_EVIDENCE.md`
5. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_PLAN.md`
6. `receiptledger/RECEIPT_PRODUCT_SEMANTICS_CONSISTENCY_REVIEW.md`
7. `receiptledger/RECEIPT_PRODUCT_SEMANTICS_GOLDEN_VECTORS.md`
8. `receiptledger/CP22_PERSISTENCE_V2_CLOSEOUT.md`
9. `receiptledger/CP22_PERSISTENCE_V2_EVIDENCE.md`
10. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
11. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
12. `receiptledger/README.md`
13. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP23 — Receipt Product Semantics — PASS / COMPLETE**

- branch: `receiptledger/run-v1-receipt-product-semantics-20261016`
- predecessor handoff: `913150c7acb06cb80a18833a10680657213239ec`
- frozen implementation HEAD: `5bffb66bd43814f8d638791b5697f79ff089028b`
- canonical Actions: `38822100885` — SUCCESS
- job: `116720855010` — SUCCESS
- artifact ID: `12013477721`
- artifact digest: `sha256:fa22d082545adae7c414b0f1c089604174341f7e879c1acd5e4677e1dc2b7195`
- APK SHA-256: `e4e64f85f9700089b32f9f0b8121eef0a2f565d09b5428599d3717296c1b8324`
- semantic parser tests: 7/7 PASS
- frozen catalog tests: 15/15 PASS
- frozen persistence tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionName `1.0.21-receipt-product-semantics`, versionCode 22

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색 -> 과거 가격과 현재 가격 판단`

The receipt remains evidence/input. Product/commodity history is the destination.

## 3. CP23 semantic contract

The parser consumes the existing receipt item name and returns unconfirmed evidence candidates only.

Supported evidence:

- brand: explicit `[brand]` or caller-supplied known-brand longest prefix only;
- product/family: conservative remaining lexical text;
- variant: explicit non-numeric parenthetical descriptor only;
- specification: explicit `입/개입`, exact weight/volume and multipack syntax;
- purchase form: raw quantity + sales-unit candidate;
- evidence string, confidence and deterministic reason;
- ambiguity and review reasons.

Every parsed catalog field is `PARSED_FROM_RECEIPT / UNCONFIRMED`. HIGH confidence is not confirmation.

CP23 never emits a catalog ID, creates an alias, links an item, merges products or assigns identity authority.

## 4. Essential ambiguity rule

A standalone physical measure is dual-use evidence.

Examples:

- `왕교자 1.05KG` may be packaged net content;
- `감자 1KG` may be commodity purchase amount.

Without identity/catalog-kind context, CP23 keeps both readings at MEDIUM confidence and requires review. This ambiguity is intentional and must not be removed merely to improve automation numbers.

Strong package evidence such as `200MLX6` and `5입` is parsed more strongly. Strong raw package forms 봉/상자/단 are preserved without conversion. Context-sensitive 팩/개 remain review-gated.

## 5. Canonical local metrics

`fixtures=26 expected_fields=68 predicted_fields=66 correct_fields=64 precision_ppm=969696 recall_ppm=941176 review_required=13 semantic_ready=13 ambiguous=10 ambiguous_reviewed=10 no_invention_negatives=2`

- precision 96.9696%
- recall 94.1176%
- all ambiguity review-gated 10/10
- no-invention negatives 2/2

These are deterministic synthetic-fixture metrics, not CP35 real-receipt acceptance.

## 6. Known conservative limitations

- first token is not automatically a brand;
- an unseen brand can remain inside product lexical text;
- free-form flavor/model suffix is not automatically variant;
- lexical-only items such as `양파` remain review-required because CP23 has no structured evidence beyond the name;
- parser output alone cannot establish STANDARD vs NON_STANDARD or SKU identity.

These limitations are visible by design. CP24 may use confirmed aliases/catalog knowledge to reduce repeat-use burden without weakening CP23 semantics.

## 7. Upstream contracts that remain frozen

### CP21

- stable catalog ID = identity/equality authority;
- UNCLASSIFIED is unresolved;
- category/store context cannot prove product identity;
- source/confidence/confirmation are independent;
- exact unit canonicalization only where defensible;
- grouping != comparability.

### CP22

- product DB `receipt-products-v1.db`, schema 2;
- receipt DB `receiptledger-v1.db`, schema 1;
- legacy product IDs/item links preserved;
- legacy aliases GLOBAL;
- merchant alias context persistable;
- receipt price/date/store/validation remain authoritative;
- direct SQLite retained.

## 8. Superseded failure

Run `38821795314` failed in lint after scope/public-tree guards passed. The initial parser used Java collection sorting convenience APIs classified as API24+ while minSdk is 23.

Fix: API23-safe `Collections.sort` with explicit comparator. No minSdk increase, no suppression, no domain change. Final run `38822100885` passed lint 0/0 and all evidence steps.

## 9. Next planned implementation checkpoint

**CP24 — Identity Resolver V2**

Required concerns before authority is added:

1. exact GLOBAL vs MERCHANT alias precedence;
2. confirmed knowledge reuse;
3. deterministic candidate ranking;
4. ambiguous cases fail to review rather than unsafe auto-link;
5. false merge and false split both measured;
6. automatic-link success and incorrect-auto-link rate measured;
7. repeat purchase after prior confirmation should reduce review burden;
8. CP23 confidence by itself never authorizes a link.

CP24 is planned, not automatically authorized.

## 10. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Do not use other project namespaces. Never commit secrets, release signing material, private receipts, personal purchase databases/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

## 11. Group discipline

For every checkpoint:

- recover canonical state;
- restate essence/non-goals;
- inspect only materially relevant consistency risks;
- resolve cheap contradictions before implementation;
- avoid unrelated architecture cleanup;
- implement the smallest coherent proof;
- run scoped CI/evidence;
- freeze exact executable refs;
- synchronize handoff/status docs;
- stop before the next unauthorized group.

## 12. Stop condition

**CP23 is complete and handoff-synchronized. Await explicit authorization for CP24.**
