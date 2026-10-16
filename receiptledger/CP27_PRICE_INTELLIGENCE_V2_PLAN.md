# ReceiptLedger V1 — CP27 Price Intelligence V2 Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRICE_INTELLIGENCE_V2_01`

## 1. Product essence

ReceiptLedger exists to remember what the user actually paid for repeat purchases and make later price comparison trustworthy.

CP27 therefore does **not** begin with averages or charts. It first defines what a comparison price means and which observations are eligible to participate.

## 2. Scope

CP27 adds a read-only `priceintel/**` engine over existing canonical receipt and catalog data.

It must provide:

- receipt-traceable comparison-price observations;
- explicit inclusion/exclusion reasons;
- STANDARD one-package comparison;
- NON_STANDARD safe quantity/form cohorts;
- latest / previous / delta / delta-percent;
- min / max / mean / median;
- date-period and exact-store filtering;
- deterministic local quality metrics.

## 3. Frozen upstream boundaries

Unchanged:

- stable catalog ID remains identity authority;
- product DB schema remains 2;
- receipt DB schema remains 1;
- CP23 semantics remain unconfirmed evidence;
- CP24 identity authority unchanged;
- CP25 category remains non-identifying metadata;
- CP26 commodity grouping/form preservation unchanged;
- receipt price/date/store/validation remain canonical source truth;
- no network, permission or signing change.

Legacy `price/**` remains intact. CP27 is parallel V2 functionality.

## 4. Canonical comparison-price rule

A comparison price is a **traceable ratio**:

`receipt-derived effective item amount / comparison denominator`

The engine keeps the numerator and denominator, not only a rounded display value.

### STANDARD

Basis: one exact stable product package.

Preferred evidence:

1. item line amount + positive item quantity -> line amount / quantity;
2. if line amount/quantity is unavailable, a non-negative persisted unit price may be used;
3. if unit price, quantity and line amount are all present but disagree (`unitPrice * quantity != lineAmount`) and no attributable discount explains it, exclude as conflict.

This allows exact source ratios such as `10000 / 3 packages` without pretending the receipt contained a rounded per-package price.

### NON_STANDARD

Price denominator comes from the observation-specific `PurchaseForm`:

- weight: normalized exactly to kg;
- volume: normalized exactly to L;
- count: normalized exactly to each;
- package/form units (봉/팩/상자/단/OTHER): only same-form contextual cohorts.

Package/form cohorts are **not** strict normalized commodity price.

## 5. Discount policy

Current canonical persistence stores `discountSum` but does not persist an item-to-discount attribution graph.

Therefore:

- no discount: normal price derivation;
- receipt contains exactly one item row: all receipt discount can be attributed to that sole item without ambiguity, so `lineAmount + discountSum` is eligible;
- multiple item rows + non-zero discount: keep the observation visible but exclude it from comparison aggregates as `UNALLOCATED_RECEIPT_DISCOUNT`;
- never prorate a receipt coupon/discount across items by price, quantity or arbitrary proportion.

This is deliberately conservative. A future item-discount attribution system requires its own evidence/persistence contract.

## 6. Validation eligibility

Only receipts with:

- `PASS`, or
- `PASS_WITH_WARNINGS`

may produce eligible comparison observations.

`MISMATCH` and `INCOMPLETE` observations remain visible with an explicit exclusion reason.

## 7. Comparison cohorts

Strict normalized cohorts:

- `STANDARD_PACKAGE`
- `WEIGHT_KG`
- `VOLUME_L`
- `EACH`

Contextual cohort:

- `LIKE_FORM:<unit>:<raw form>`

Examples:

- 감자 1kg and 감자 500g -> same `WEIGHT_KG` cohort;
- 감자 1봉 and 감자 2봉 -> same contextual 봉 cohort;
- 감자 봉 and 감자 상자 -> different cohorts;
- no guessed 봉↔kg or 상자↔봉 conversion.

## 8. Statistics

For each cohort, sorted newest-first by canonical purchase date then created time:

- latest;
- previous;
- absolute delta;
- percent delta when previous != 0;
- min;
- max;
- arithmetic mean;
- median.

CP27 does not label a price cheap/normal/expensive. That belongs to CP28.

## 9. Scope filters

Support deterministic filters:

- all history;
- inclusive ISO date period;
- exact normalized store name;
- period + store.

No fuzzy store merging is introduced here.

## 10. Non-goals

- CP28 price evaluation labels;
- charts;
- UI redesign;
- item-level discount-row association;
- receipt schema migration;
- cloud/online prices;
- inflation adjustment;
- arbitrary package equivalence;
- changing identity/category/grouping rules.

## 11. Acceptance

CP27 can close only if:

1. existing schemas and upstream authority remain frozen;
2. invalid receipts do not enter aggregates;
3. multi-item unallocated discounts do not enter aggregates;
4. sole-item discount attribution is exact and tested;
5. source numerator/denominator are preserved;
6. STANDARD quantity > 1 is handled;
7. kg/g and L/mL normalization are exact in one cohort;
8. package forms remain contextual and separated;
9. missing/unsupported forms remain visible but excluded;
10. latest/previous/delta/min/max/mean/median are deterministic;
11. period/store filters are tested;
12. full upstream regression, lint, APK permission audit and evidence packaging pass.

## 12. Stop condition

Close CP27 after frozen implementation evidence and handoff synchronization. Do not begin CP28 without explicit authorization.
