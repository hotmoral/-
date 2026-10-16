# ReceiptLedger V1 — CP35 Public-Safe Receipt Evaluation Fixtures

Updated: 2026-10-16 KST
Version: 1.0.0

All names, merchants, dates and prices below are synthetic. They are safe for the public repository and are not copied from a private receipt.

## RRE-01 — STANDARD_NEW

Receipt:

- merchant: `가상마트A`
- date: `2026-10-01`
- item: `서울우유1L`
- line amount: 3,200
- total: 3,200

Ground truth:

- receipt structure must be correct;
- semantic parser should expose lexical product/spec evidence;
- no stable product link exists automatically;
- fixture-prescribed user confirmation creates STANDARD product `서울우유 1L` and confirms raw alias `서울우유1L`;
- resulting STANDARD_PACKAGE observation = 3,200 and is receipt-traceable.

## RRE-02 — STANDARD_REPEAT_EXACT

Receipt:

- merchant: `가상마트B`
- date: `2026-10-05`
- item: `서울우유1L`
- line amount: 3,000
- total: 3,000

Ground truth:

- after RRE-01 confirmation, `resolveAndLinkExact()` must reuse the exact same stable ID;
- no new product is created;
- STANDARD_PACKAGE history contains two eligible observations, latest 3,000 / previous 3,200;
- source receipt IDs remain distinct.

## RRE-03 — STANDARD_SIMILAR_NOT_EXACT

Receipt:

- merchant: `가상마트C`
- date: `2026-10-06`
- item: `서울우유900mL`
- line amount: 2,900
- total: 2,900

Ground truth:

- the confirmed alias `서울우유1L` must not cause this merely similar raw name to link;
- exact resolver result remains UNCLASSIFIED;
- no false STANDARD_PACKAGE observation is added to the 1L product.

## RRE-04 — COMMODITY_WEIGHT

Receipts:

1. `가상시장`, `2026-10-07`, `감자 1kg`, 6,000
2. `가상시장`, `2026-10-08`, `감자 500g`, 3,300

Ground truth:

- both raw names may be explicitly confirmed to one NON_STANDARD commodity `감자`;
- semantic purchase forms are 1kg and 500g;
- CP27 combines them only in `WEIGHT_KG`;
- comparison prices are 6,000/kg and 6,600/kg;
- no contextual package cohort substitutes for the strict weight cohort.

## RRE-05 — COMMODITY_CONTEXTUAL

Receipts:

1. `가상시장`, `2026-10-09`, `감자 1봉`, 4,000
2. `가상시장`, `2026-10-10`, `감자 1상자`, 15,000

Ground truth:

- both may be explicitly confirmed to the same NON_STANDARD commodity `감자`;
- grouping does not imply comparability;
- `LIKE_FORM:BAG:봉` and `LIKE_FORM:BOX:상자` remain separate contextual cohorts;
- neither receipt may be converted into WEIGHT_KG without evidence;
- contextual cohorts remain non-judgmental under CP28.

## RRE-06 — MULTI_ITEM_DISCOUNT

Receipt:

- merchant: `가상마트A`
- date: `2026-10-11`
- items: `서울우유1L` 3,200; `신라면5입` 4,990
- receipt-level coupon discount: -500
- total: 7,690

Ground truth:

- structure/arithmetic is valid;
- the already-confirmed milk alias may link exactly;
- because the receipt-level discount cannot be attributed between multiple items, the milk observation is `UNALLOCATED_RECEIPT_DISCOUNT` and is excluded from its comparable STANDARD_PACKAGE cohort;
- no guessed discounted item price is created.

## RRE-07 — TOTAL_MISMATCH_REVIEW

Receipt:

- merchant: `가상마트D`
- date: `2026-10-12`
- items: `테스트과자` 2,000; `테스트음료` 1,500
- printed total: 3,000
- no printed discount

Ground truth:

- computed item sum is 3,500;
- validation is MISMATCH;
- CP33 assessment is REVIEW_REQUIRED;
- this receipt cannot be counted as safe comparable price evidence before correction.

## RRE-08 — DETAIL_TRACEABILITY

Uses the authoritative records created by the earlier fixtures.

Ground truth:

- CP31 Product Detail for `서울우유 1L` contains purchase rows with exact source receipt IDs and eligibility states, including the excluded multi-item-discount receipt;
- CP32 Commodity Detail for `감자` contains strict weight sections and separate contextual sections;
- all purchase rows preserve exact `receiptId` and item ordinal;
- no detail-layer field creates a new identity, comparison basis or price value.

## Corpus limitations

This corpus is deliberately small and deterministic. It covers contract-risk classes, not statistical OCR accuracy across stores/cameras/fonts. It begins from synthetic `OcrDocument` tokens/geometries and therefore does not measure ML Kit image-to-text character recognition or physical-device capture variation.
