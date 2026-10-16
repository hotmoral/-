# ReceiptLedger V1 — CP28 Price Evaluation Closeout

Updated: 2026-10-16 KST
Status: **PASS / COMPLETE**

## 1. Closed boundary

- branch: `receiptledger/run-v1-price-evaluation-20261016`
- predecessor CP27 handoff: `c9131d0c6c8e799390ff37a370a1b1c77c38647a`
- frozen implementation HEAD: `dd4f98613677ae998932d77f3e5f89d7bddba107`
- canonical Actions run: `38834818192` — SUCCESS
- job: `116761457914` — SUCCESS
- artifact ID: `12018776680`
- artifact digest: `sha256:aa90bff8107f34d1974fd9998ceb543fba33fd8b0d402cc972840f9495b9e4b6`
- APK SHA-256: `692e16f0bd6ad23caba3361d831376620bac09e1505f4780d7147402f9fd48f6`
- version: `1.0.26-price-evaluation` / versionCode 27

## 2. What CP28 added

CP28 turns one already-safe CP27 comparison cohort into an explainable personal-history price judgment.

Judgments:

- `VERY_CHEAP`
- `CHEAP`
- `TYPICAL`
- `EXPENSIVE`
- `VERY_EXPENSIVE`

No-judgment states:

- `INSUFFICIENT_HISTORY`
- `CONTEXTUAL_ONLY`
- `NON_POSITIVE_BASELINE`

## 3. Frozen baseline contract

The latest purchase is never allowed to influence the baseline used to judge itself.

Canonical V1 baseline:

- latest eligible observation excluded;
- minimum prior observations = 3;
- use at most the 5 most recent prior observations from the same CP27 cohort;
- usual price = median;
- older observations outside the recent-five window do not affect the current judgment.

Latest-vs-previous remains separately exposed from latest-vs-usual-price.

## 4. Frozen threshold contract

A material change requires both:

- absolute difference >= 100 minor currency units;
- percentage difference >= 5%.

An extreme change requires both:

- absolute difference >= 500 minor currency units;
- percentage difference >= 15%.

Exact threshold boundaries are inclusive.

These are transparent V1 personal-history heuristics, not external market-value claims.

## 5. Contextual/non-standard safety

`CONTEXTUAL_LIKE_FORM` cohorts such as 봉/팩/상자 remain history-only. They can expose latest/previous facts but do not receive cheap/expensive labels because equal raw form does not prove equal physical content.

Strict CP27 kg/L/each cohorts may be evaluated because their comparison basis is mathematically normalized.

## 6. Explainability

Every evaluation result exposes:

- comparison basis/strength;
- status/judgment;
- deterministic reason code;
- latest and previous price facts;
- baseline count/window and baseline receipt IDs;
- usual-price median;
- current-vs-usual delta/percent;
- all policy thresholds.

No free-form AI opinion is involved.

## 7. Local evidence

Canonical metric:

`cases=12 evaluated=9 insufficient=1 contextual=1 nonpositive=1 typical=2 cheap=2 very_cheap=1 expensive=2 very_expensive=2 latest_excluded=1 recent_five_window=1 deterministic_repeat=1`

Tests:

- CP28 Price Evaluation: 8/8 PASS
- CP27 Price Intelligence: 8/8 PASS
- legacy Price History: 2/2 PASS
- CP26 Commodity: 8/8 PASS
- CP25 Category: 8/8 PASS
- CP24 Identity: 8/8 PASS
- CP23 Semantics: 7/7 PASS
- CP21 Catalog: 15/15 PASS
- CP22 Persistence: 7/7 PASS
- lint: 0 errors / 0 warnings

## 8. Frozen upstream/storage boundary

Unchanged:

- product schema 2;
- receipt schema 1;
- CP27 `priceintel/**` derivation/exclusion rules;
- legacy `price/**`;
- identity/category/commodity contracts;
- receipt price/date/store/validation truth;
- permissions/network/privacy posture.

No new persistence table or migration was introduced.

## 9. Known limitations

- thresholds are frozen V1 product heuristics, not user-customized or market-calibrated;
- baseline is purchase-count based rather than time-decay/seasonality based;
- infrequently purchased products may therefore have old baseline observations;
- contextual package-form prices intentionally receive no judgment;
- no external market-price or future-price forecast;
- no final commercial UI yet.

## 10. Next boundary

Next planned checkpoint: **CP29 — Search / Browse**.

CP29 should make the accumulated product/commodity/price/evaluation knowledge practically findable by product name, brand, aliases, category, specification, store, recency/frequency and price change without redesigning identity authority.

CP29 is not authorized by this closeout.

## 11. Stop condition

CP28 implementation, CI/evidence and handoff synchronization are complete. Stop at this boundary.
