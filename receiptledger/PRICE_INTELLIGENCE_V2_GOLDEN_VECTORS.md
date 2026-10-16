# ReceiptLedger V1 — Price Intelligence V2 Golden Vectors

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRICE_INTELLIGENCE_V2_01`

## P27-G01 STANDARD deterministic history

Input:
- same stable STANDARD product;
- 3000, 3200, 2800 per package on increasing dates.

Expected:
- latest 2800;
- previous 3200;
- delta -400;
- min 2800;
- max 3200;
- mean 3000;
- median 3000;
- delta-percent -12.5%.

## P27-G02 store filter

Input: G01 with store A/B/A.

Expected store A cohort:
- 2 observations;
- latest 2800;
- previous 3000.

## P27-G03 period filter

Input: G01, inclusive period 2026-10-02..2026-10-10.

Expected:
- only second and third observations;
- latest 2800;
- previous 3200.

## P27-G04 sole-item discount

Input:
- one item row, line amount 5000;
- receipt discount -1000;
- valid receipt.

Expected:
- exact attributable net numerator 4000;
- eligible;
- discount treatment `SOLE_ITEM_EXACT`.

## P27-G05 multi-item unallocated discount

Input:
- two item rows;
- receipt discount -1000;
- no item-discount attribution graph.

Expected:
- target observation remains visible;
- excluded as `UNALLOCATED_RECEIPT_DISCOUNT`;
- never enters cohort statistics.

## P27-G06 invalid receipt

Input: MISMATCH or INCOMPLETE.

Expected: visible but `INVALID_RECEIPT`, excluded from aggregates.

## P27-G07 item arithmetic conflict

Input:
- quantity 2;
- unit price 3000;
- line amount 6100;
- no discount.

Expected: `ITEM_PRICE_CONFLICT`, not silently corrected.

## P27-G08 repeating exact source rate

Input:
- STANDARD line amount 10000;
- quantity 3;
- no unit price.

Expected:
- source numerator = 10000;
- source denominator = 3;
- eligible one-package rate derived deterministically;
- no requirement that the receipt contain a rounded 3333/3334 allocation.

## P27-G09 NON_STANDARD weight normalization

Input:
- same commodity stable ID;
- 1kg for 6000;
- 500g for 3300.

Expected one strict `WEIGHT_KG` cohort:
- rates 6000/kg and 6600/kg;
- latest 6600;
- previous 6000;
- mean 6300.

## P27-G10 NON_STANDARD volume normalization

Input:
- same commodity;
- 1L and 500mL observations.

Expected: one strict `VOLUME_L` cohort using exact mL→L quantity conversion only.

## P27-G11 count normalization

Input: same commodity with EACH purchase form.

Expected: strict `EACH` cohort, price denominator = exact count.

## P27-G12 same-form contextual cohort

Input:
- 감자 1봉 4000;
- 감자 2봉 9000.

Expected:
- one contextual `LIKE_FORM:BAG:봉` cohort;
- rates 4000/봉 and 4500/봉;
- explicitly not strict commodity normalization.

## P27-G13 different package forms stay separate

Input:
- 봉 observations;
- 상자 observation.

Expected:
- separate BAG and BOX contextual cohorts;
- no 봉↔상자 conversion.

## P27-G14 missing PurchaseForm

Input: linked NON_STANDARD commodity with line amount but no PurchaseForm.

Expected: visible `MISSING_PURCHASE_FORM`; no cohort.

## P27-G15 no price judgment

Any cohort statistics.

Expected: no cheap/normal/expensive label in CP27 API.

## Metric contract

Synthetic metric fixture must demonstrate:

- eligible observations and explicit exclusions coexist;
- at least one unallocated-discount exclusion;
- at least one invalid-receipt exclusion;
- at least one missing-form exclusion;
- one STANDARD cohort;
- at least one strict commodity cohort;
- at least one contextual commodity cohort;
- date/store scope checks pass;
- every eligible rate remains receipt-traceable.

These vectors are local deterministic contracts, not CP35 real-receipt accuracy claims.
