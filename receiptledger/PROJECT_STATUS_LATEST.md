# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP27 — Price Intelligence V2 — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-price-intelligence-v2-20261016`
- predecessor CP26 handoff: `b5a20233fbe9d64d45e00c46adafadfbe6925f6e`
- frozen CP27 implementation HEAD: `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`
- canonical Actions run: `38831623548` — SUCCESS
- job: `116751473084` — SUCCESS
- artifact ID: `12017014494`
- artifact digest: `sha256:660ead5ea86bae86fbd6cf67643866c17acfa5f144c9b1d06f29d50f71f44dd5`
- debug APK SHA-256: `8455e4ce23e15c6a113e87ddbd0ddb000e41d9f1849e7f431c9ed5dfbfabe1bc`
- Price Intelligence V2 tests: 8/8 PASS
- legacy Price History tests: 2/2 PASS
- Commodity / Non-standard V2 tests: 8/8 PASS
- Category System tests: 8/8 PASS
- Identity Resolver V2 tests: 8/8 PASS
- Receipt Product Semantics tests: 7/7 PASS
- Catalog Domain V2 tests: 15/15 PASS
- Persistence V2 tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.25-price-intelligence-v2` / versionCode 26

Any later handoff commit is documentation-only. The executable/evidence boundary remains `4edc37c5...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

CP27 establishes the trustworthy historical-price layer. Price judgment itself remains CP28.

## 3. CP27 comparison-price contract

A comparison price is a receipt-traceable ratio:

`effective item amount / comparison denominator`

Source numerator and denominator remain available instead of being replaced by a rounded display value.

STANDARD:

- same stable exact product ID;
- compare one package;
- line amount / positive item quantity when available;
- unit-price fallback only when line/quantity is unavailable;
- arithmetic conflicts are excluded, not silently repaired.

NON_STANDARD:

- kg/g -> strict per-kg cohort;
- L/mL -> strict per-L cohort;
- count -> strict per-each cohort;
- 봉/팩/상자/단/OTHER -> contextual same-form cohorts only.

Grouping remains distinct from comparability.

## 4. Discount/validation boundary

Current persistence has receipt-level `discountSum` but no item-discount attribution graph.

Frozen rule:

- exactly one item row -> receipt discount can be attributed exactly to that item;
- multiple item rows + non-zero unallocated discount -> keep observation visible but exclude from aggregates;
- never prorate a coupon/discount by guesswork.

Only PASS / PASS_WITH_WARNINGS observations can become eligible. MISMATCH / INCOMPLETE remain visible but excluded.

## 5. Statistics and filters

Per comparison cohort CP27 supplies:

- latest / previous;
- absolute / percentage delta;
- min / max;
- mean / median.

Filters:

- all history;
- inclusive date period;
- exact-normalized store;
- period + store.

CP27 does not label prices cheap/normal/expensive.

## 6. Canonical local evidence

`observations=10 eligible=7 excluded_discount=1 excluded_invalid=1 missing_form=1 standard_cohorts=1 commodity_strict_cohorts=1 commodity_contextual_cohorts=1 scope_checks=2 receipt_traceable_rates=7`

These are deterministic synthetic contract fixtures, not CP35 real-receipt accuracy claims.

## 7. Frozen upstream/storage boundary

Unchanged:

- stable catalog ID authority;
- product schema 2;
- receipt schema 1;
- legacy `price/**` core;
- CP23 semantics;
- CP24 identity;
- CP25 category;
- CP26 commodity grouping/form model;
- receipt price/date/store/validation truth;
- permissions/network/privacy posture.

No duplicate price-observation table was introduced.

## 8. Known limitations

- multi-item discounted receipts cannot safely enter aggregate comparison until item-level discount attribution exists;
- same-form package cohorts are contextual, not strict normalized commodity price;
- store scope is exact normalized text, not merchant-entity consolidation;
- no current-price judgment label yet;
- no chart/UI redesign yet.

## 9. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> **CP27 Price Intelligence V2**.

## 10. Next planned checkpoint

**CP28 — Price Evaluation**.

CP28 must define deterministic, explainable judgment rules over CP27 eligible cohorts:

- minimum data sufficiency;
- baseline/window selection;
- robust usual-price statistic;
- explicit thresholds for cheap/normal/expensive;
- sparse data and zero-baseline behavior;
- treatment of contextual LIKE_FORM cohorts;
- transparent reasons for every judgment.

No free-form AI price judgment and no cross-cohort mixing.

**Do not begin CP28 without explicit user authorization.**

## 11. Canonical restart order

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

GitHub is canonical. Verify current branch/ref and frozen implementation boundary before future work.

## 12. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

Forbidden APK permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

**Current stop condition: CP27 is complete. Await explicit authorization for CP28.**
