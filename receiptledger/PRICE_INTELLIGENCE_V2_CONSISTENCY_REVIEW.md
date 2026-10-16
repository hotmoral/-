# ReceiptLedger V1 — Price Intelligence V2 Consistency Review

Updated: 2026-10-16 KST

## 1. Review purpose

Verify that CP27 advances the product goal—trustworthy personal purchase-price memory—without silently redefining receipt truth, identity, commodity grouping or discount semantics.

## 2. Existing contracts reviewed

### CP21 / CP24 identity

Price intelligence consumes stable catalog IDs only. Price similarity never links or merges products/commodities.

Result: **compatible**.

### CP22 persistence

Product schema 2 and receipt schema 1 already contain the data required for a conservative CP27 proof:

- item quantity/unit price/line amount;
- receipt discount sum;
- validation status;
- purchase date/store;
- product links;
- observation purchase form.

Result: **no migration justified for CP27**.

### CP23 semantics / CP26 PurchaseForm

Purchase-form evidence remains observation-specific and retains source/confidence/confirmation. CP27 reads it but does not upgrade it.

Result: **compatible**.

### CP25 category

Category is irrelevant to comparison eligibility and cannot combine histories.

Result: **compatible**.

### Legacy Price History Core

Legacy service proved receipt-derived price history but assumes STANDARD comparability and leaves NON_STANDARD raw-only. It remains useful as a regression surface but is not sufficiently expressive for CP27.

Decision: **preserve, do not rewrite**. Add parallel `priceintel/**`.

## 3. Discount contradiction review

Current receipt validation stores only aggregate discount effect. It does not persist a stable association from each discount row to an item.

Possible bad choices:

1. prorate all discounts by item price;
2. attach every nearby discount to the previous item;
3. ignore discounts and call gross item price “actual paid price”.

All three can produce false price history.

Chosen rule:

- if the receipt has exactly one item row, discount attribution is mathematically unique;
- otherwise non-zero receipt discount is unallocated and excluded from strict comparison aggregates.

This preserves evidence instead of inventing allocation.

## 4. STANDARD quantity review

A receipt may record total line amount for several identical packages. Comparison should answer the price of one exact package.

Chosen rate:

`effective line amount / receipt item quantity`

The exact numerator/denominator are retained even when decimal expansion repeats. A conflicting printed unit price causes exclusion rather than silent preference.

## 5. NON_STANDARD review

Same commodity identity does not imply all observations share a denominator.

Safe cohorts:

- kg/g -> per kg;
- L/mL -> per L;
- each -> per each;
- same package/form -> contextual per-form rate only.

Unsafe combinations remain separate:

- 봉 vs 상자;
- 개 vs kg;
- 봉 vs kg;
- OTHER labels that differ.

`LIKE_FORM` is intentionally not described as normalized commodity price.

## 6. Provenance review

Each eligible observation retains:

- receipt ID;
- item ordinal;
- raw item name;
- purchase date/store;
- raw unit price/line amount;
- receipt discount sum;
- validation state;
- link source;
- PurchaseForm and its source/confidence/confirmation;
- comparison basis;
- price source;
- exact source numerator/denominator.

Excluded observations remain visible with explicit reason.

Result: **receipt traceability preserved**.

## 7. Statistics review

CP27 may compute descriptive statistics only inside one cohort. It must not infer a value judgment.

Allowed:

- latest / previous;
- delta / delta-percent;
- min / max;
- mean / median;
- store/date filters.

Deferred:

- cheap/normal/expensive thresholds;
- outlier policy for judgment;
- sparse-data judgment.

Those belong to CP28.

## 8. Performance review

Current implementation derives observations on demand from receipt links, consistent with the earlier no-duplicate-price-table rule. V1 data scale does not justify a new materialized price table in CP27.

Potential future hot path: large histories during CP29/31. Measure before adding cache/materialization.

## 9. Privacy/security review

No new permission, network, external catalog or private fixture is needed. CI remains debug-only and public-safe.

## 10. Residual risks

1. Multi-item discounted receipts lose aggregate comparability until discount attribution exists.
2. Parsed PurchaseForm can still be OCR/semantic evidence rather than explicit user confirmation; CP35 must measure real-world correctness.
3. Same-form package cohorts can hide size variation; they are contextual only and must be labelled accordingly in future UI.
4. Store names are exact-normalized, not merchant-entity merged.
5. No inflation or cross-store market normalization.

These are visible limitations, not reasons to broaden CP27 scope.

## 11. Conclusion

CP27 is consistent if implemented as a read-only, evidence-preserving comparison layer with strict cohort boundaries and explicit exclusions. No upstream schema/domain rewrite is required.
