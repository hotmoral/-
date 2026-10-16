# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP28 — Price Evaluation — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-price-evaluation-20261016`
- predecessor CP27 handoff: `c9131d0c6c8e799390ff37a370a1b1c77c38647a`
- frozen CP28 implementation HEAD: `dd4f98613677ae998932d77f3e5f89d7bddba107`
- canonical Actions run: `38834818192` — SUCCESS
- job: `116761457914` — SUCCESS
- artifact ID: `12018776680`
- artifact digest: `sha256:aa90bff8107f34d1974fd9998ceb543fba33fd8b0d402cc972840f9495b9e4b6`
- debug APK SHA-256: `692e16f0bd6ad23caba3361d831376620bac09e1505f4780d7147402f9fd48f6`
- CP28 tests: 8/8 PASS
- CP27 tests: 8/8 PASS
- legacy price-history: 2/2 PASS
- CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.26-price-evaluation` / versionCode 27

Any later handoff commit must remain documentation-only. Executable/evidence boundary remains `dd4f986...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable price judgment`

## 3. CP28 evaluation contract

Input is exactly one CP27-safe comparison cohort.

Baseline:

- latest purchase excluded;
- minimum 3 prior observations;
- recent maximum 5 prior observations;
- usual price = median.

Material judgment requires both >=5% and >=100 minor units.
Extreme judgment requires both >=15% and >=500 minor units.

Labels:

- VERY_CHEAP
- CHEAP
- TYPICAL
- EXPENSIVE
- VERY_EXPENSIVE

No-judgment states:

- INSUFFICIENT_HISTORY
- CONTEXTUAL_ONLY
- NON_POSITIVE_BASELINE

## 4. Safety boundary

- CP27 price eligibility/discount rules are frozen;
- contextual 봉/팩/상자/단/OTHER cohorts do not receive cheap/expensive labels;
- kg/L/each strict normalized cohorts may be evaluated;
- no cross-cohort mixing;
- no market-price lookup;
- no generative-AI opinion;
- no schema migration or duplicate price table.

Every result exposes reason code, baseline count/receipt IDs, usual price, latest/previous facts, deltas and threshold values.

## 5. Canonical local metric

`cases=12 evaluated=9 insufficient=1 contextual=1 nonpositive=1 typical=2 cheap=2 very_cheap=1 expensive=2 very_expensive=2 latest_excluded=1 recent_five_window=1 deterministic_repeat=1`

Synthetic deterministic contract evidence only; not market-quality or real-receipt accuracy.

## 6. Known limitations

- V1 thresholds are explicit product heuristics, not user-customized or market-calibrated;
- baseline uses recent purchase count, not seasonality/time decay;
- infrequent goods may have old baseline observations;
- contextual package forms intentionally remain unjudged;
- no final commercial UI/search surface yet.

## 7. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> **CP28 Price Evaluation**.

## 8. Next planned checkpoint

**CP29 — Search / Browse**.

Goal: make product/commodity history practically findable by product name, brand, safe aliases, category, specification, store, recent/frequent use and price change while preserving stable-ID and evaluation boundaries.

CP29 must not widen identity authority or create fuzzy silent merge behavior.

**Do not begin CP29 without explicit user authorization.**

## 9. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP28_PRICE_EVALUATION_CLOSEOUT.md`
4. `receiptledger/CP28_PRICE_EVALUATION_EVIDENCE.md`
5. `receiptledger/CP28_PRICE_EVALUATION_PLAN.md`
6. `receiptledger/PRICE_EVALUATION_CONSISTENCY_REVIEW.md`
7. `receiptledger/PRICE_EVALUATION_GOLDEN_VECTORS.md`
8. `receiptledger/CP27_PRICE_INTELLIGENCE_V2_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify current branch/ref before future work.

## 10. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, personal purchase DB/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

**Current stop condition: CP28 is complete. Await explicit authorization for CP29.**
