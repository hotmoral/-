# ReceiptLedger V1 — CP27 Price Intelligence V2 Closeout

Updated: 2026-10-16 KST
Status: **PASS / COMPLETE**

## 1. Closed boundary

- branch: `receiptledger/run-v1-price-intelligence-v2-20261016`
- predecessor CP26 handoff: `b5a20233fbe9d64d45e00c46adafadfbe6925f6e`
- frozen implementation HEAD: `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`
- canonical Actions run: `38831623548` — SUCCESS
- job: `116751473084` — SUCCESS
- artifact ID: `12017014494`
- artifact digest: `sha256:660ead5ea86bae86fbd6cf67643866c17acfa5f144c9b1d06f29d50f71f44dd5`
- APK SHA-256: `8455e4ce23e15c6a113e87ddbd0ddb000e41d9f1849e7f431c9ed5dfbfabe1bc`
- version: `1.0.25-price-intelligence-v2` / versionCode 26

## 2. What CP27 added

CP27 added a read-only V2 price-intelligence layer without replacing the legacy price-history proof.

It provides:

- receipt-traceable comparison-price observations;
- explicit exclusion reasons;
- STANDARD one-package comparison;
- strict NON_STANDARD kg/L/each cohorts;
- contextual same-form cohorts;
- latest/previous/delta/delta-percent;
- min/max/mean/median;
- date-period and store filters.

## 3. Canonical price meaning

A CP27 comparison price is not an arbitrary stored number. It is a traceable ratio:

`receipt-derived effective item amount / comparison denominator`

The exact source numerator and denominator remain available. Display rounding must not replace the underlying evidence.

For STANDARD, the denominator is the count of the same exact stable product package.

For NON_STANDARD, strict denominator families are kg, L and each. Package/form units remain contextual only.

## 4. Discount boundary

Current persistence stores aggregate receipt discount effect but not a stable item-to-discount mapping.

Therefore:

- one item row + receipt discount -> exact attribution to the only item is permitted;
- multiple item rows + non-zero unallocated discount -> observation is retained but excluded from aggregates;
- no coupon/discount prorating is guessed.

This limitation is intentional and protects the meaning of “actual paid price.”

## 5. Validation and conflict boundary

- PASS / PASS_WITH_WARNINGS can participate.
- MISMATCH / INCOMPLETE are visible but excluded.
- contradictory `unitPrice * quantity` vs `lineAmount` is excluded rather than silently repaired.
- missing NON_STANDARD purchase form is visible but excluded.

## 6. NON_STANDARD boundary

Strict normalized:

- kg/g -> per kg
- L/mL -> per L
- EACH -> per each

Contextual only:

- same 봉/팩/상자/단/OTHER form.

`봉` and `상자` remain different cohorts. `LIKE_FORM` must never be presented as mathematically normalized commodity price.

## 7. Local evidence

Canonical metric:

`observations=10 eligible=7 excluded_discount=1 excluded_invalid=1 missing_form=1 standard_cohorts=1 commodity_strict_cohorts=1 commodity_contextual_cohorts=1 scope_checks=2 receipt_traceable_rates=7`

CP27 tests: 8/8 PASS. Legacy price-history regression: 2/2 PASS. All CP21–CP26 targeted regressions passed. Lint: 0 errors / 0 warnings.

## 8. What CP27 deliberately did not change

- product schema remains 2;
- receipt schema remains 1;
- legacy `price/**` unchanged;
- identity/category/commodity grouping unchanged;
- no materialized duplicate price table;
- no UI/chart redesign;
- no online market price;
- no guessed item-level coupon allocation;
- no cheap/normal/expensive label.

## 9. Known limitations

- multi-item discounted receipts cannot safely contribute to strict aggregates until item-discount attribution is represented with evidence;
- same-form package cohorts may hide physical-size differences, so they are contextual only;
- store filters use exact normalized store strings, not merchant-entity consolidation;
- real receipt quality remains a CP35 concern.

## 10. Next boundary

Next planned checkpoint: **CP28 — Price Evaluation**.

CP28 must consume only CP27 eligible cohorts and define explicit, deterministic rules for:

- data sufficiency;
- baseline/window selection;
- robust usual-price statistic;
- cheap/normal/expensive thresholds;
- sparse-data / zero-previous / contextual-like-form handling;
- transparent explanation of why a label was produced.

It must not use free-form AI judgment or silently combine incomparable cohorts.

CP28 is not authorized by this closeout.

## 11. Stop condition

CP27 implementation, CI/evidence and handoff synchronization are complete. Stop at this boundary.
