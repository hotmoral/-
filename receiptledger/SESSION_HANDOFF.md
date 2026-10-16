# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP27_PRICE_INTELLIGENCE_V2_CLOSEOUT.md`
4. `receiptledger/CP27_PRICE_INTELLIGENCE_V2_EVIDENCE.md`
5. `receiptledger/CP27_PRICE_INTELLIGENCE_V2_PLAN.md`
6. `receiptledger/PRICE_INTELLIGENCE_V2_CONSISTENCY_REVIEW.md`
7. `receiptledger/PRICE_INTELLIGENCE_V2_GOLDEN_VECTORS.md`
8. `receiptledger/CP26_COMMODITY_NONSTANDARD_V2_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP27 — Price Intelligence V2 — PASS / COMPLETE**

- branch: `receiptledger/run-v1-price-intelligence-v2-20261016`
- predecessor handoff: `b5a20233fbe9d64d45e00c46adafadfbe6925f6e`
- frozen implementation HEAD: `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`
- canonical Actions: `38831623548` — SUCCESS
- job: `116751473084` — SUCCESS
- artifact ID: `12017014494`
- artifact digest: `sha256:660ead5ea86bae86fbd6cf67643866c17acfa5f144c9b1d06f29d50f71f44dd5`
- APK SHA-256: `8455e4ce23e15c6a113e87ddbd0ddb000e41d9f1849e7f431c9ed5dfbfabe1bc`
- CP27 price-intelligence tests: 8/8 PASS
- legacy price-history tests: 2/2 PASS
- CP26 commodity: 8/8 PASS
- CP25 category: 8/8 PASS
- CP24 identity: 8/8 PASS
- CP23 semantics: 7/7 PASS
- CP21 catalog: 15/15 PASS
- CP22 persistence: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionName `1.0.25-price-intelligence-v2`, versionCode 26

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색·탐색 -> 과거 가격과 현재 가격 판단`

CP27 supplies the historical comparison facts. CP28 will decide how those facts become a human-readable price judgment.

## 3. CP27 comparison-price contract

Comparison price is a **receipt-traceable ratio**, not an opaque aggregate.

Every eligible observation retains:

- receipt/item identity;
- date/store;
- raw unit price / line amount / receipt discount;
- validation/link source;
- PurchaseForm and provenance;
- comparison basis;
- exact source numerator and denominator.

### STANDARD

- stable exact product ID defines the history;
- denominator = one purchased package;
- line amount / item quantity preferred;
- direct unit price fallback only if line/quantity unavailable;
- conflicting item arithmetic is excluded.

### NON_STANDARD

Strict normalized cohorts:

- `WEIGHT_KG`
- `VOLUME_L`
- `EACH`

Contextual only:

- `LIKE_FORM:<unit>:<raw form>` for 봉/팩/상자/단/OTHER.

Do not combine distinct cohorts.

## 4. Discount contract

Receipt persistence currently has aggregate `discountSum`, not an item-discount attribution graph.

Therefore:

- sole-item receipt + discount -> exact attribution permitted;
- multi-item receipt + unallocated discount -> observation visible but excluded from aggregates;
- no proportional or proximity-based discount allocation.

Do not reinterpret excluded multi-item discounts as zero discount.

## 5. Validation/statistics contract

Eligible receipt validation:

- PASS
- PASS_WITH_WARNINGS

Excluded:

- MISMATCH
- INCOMPLETE

Each safe cohort supports:

- latest / previous;
- delta / delta-percent;
- min / max;
- mean / median;
- all-history, period, store, and period+store scope.

CP27 produces no cheap/normal/expensive judgment.

## 6. Canonical metric

`observations=10 eligible=7 excluded_discount=1 excluded_invalid=1 missing_form=1 standard_cohorts=1 commodity_strict_cohorts=1 commodity_contextual_cohorts=1 scope_checks=2 receipt_traceable_rates=7`

Synthetic/local contract evidence only.

## 7. Frozen upstream rules

- stable catalog ID = identity authority;
- product schema 2;
- receipt schema 1;
- legacy `price/**` unchanged;
- CP23 semantics unconfirmed;
- CP24 identity unchanged;
- CP25 category non-authoritative;
- CP26 grouping/form rules unchanged;
- grouping != comparability;
- receipt-derived price/date/store/validation truth preserved;
- no duplicate mutable price table;
- no permission/network/privacy expansion.

## 8. Deliberate limitations

- multi-item receipt discounts cannot enter strict aggregates until item-level attribution is represented with evidence;
- contextual same-form cohorts are not physical normalization;
- exact-normalized store text is not merchant-entity consolidation;
- CP27 does not judge price desirability;
- no chart or commercial UI here.

Do not solve these through unrelated scope expansion.

## 9. Next planned implementation checkpoint

**CP28 — Price Evaluation**

Required preflight:

1. choose data-sufficiency thresholds;
2. choose deterministic baseline/window semantics;
3. use a robust “usual price” statistic rather than arbitrary free-form judgment;
4. define explicit cheap/normal/expensive thresholds;
5. handle sparse history and previous price = 0 safely;
6. decide whether contextual LIKE_FORM cohorts may receive judgment, and if so label their weaker basis clearly;
7. every result must expose the evidence/baseline/reason;
8. never mix cohorts;
9. no online price or generative-AI opinion.

CP28 is planned, not automatically authorized.

## 10. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Do not use other project namespaces. Never commit secrets, signing material, private receipts, personal purchase DBs/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

## 11. Group discipline

For every checkpoint:

- recover canonical state;
- restate essence/non-goals;
- inspect materially relevant contradictions and risks;
- resolve cheap problems before implementation;
- avoid ritual re-audits and unrelated cleanup;
- implement the smallest coherent proof;
- run scoped CI/evidence;
- freeze exact executable refs;
- synchronize handoff/status docs;
- stop before the next unauthorized group.

## 12. Stop condition

**CP27 is complete and handoff-synchronized. Await explicit authorization for CP28.**
