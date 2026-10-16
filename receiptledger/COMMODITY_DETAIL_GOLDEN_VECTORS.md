# ReceiptLedger V1 — CP32 Commodity Detail Golden Vectors

Updated: 2026-10-16 KST

## CD01 Commodity identity

Given a NON_STANDARD catalog entry `감자`:

- stable ID remains unchanged;
- canonical commodity name is primary;
- no brand/variant/specification is fabricated;
- grouping does not imply one price basis.

## CD02 Weight normalization

Given `1kg 6,000원` and `500g 3,300원`:

- both belong to WEIGHT_KG;
- normalized rates are 6,000원/kg and 6,600원/kg;
- they may share one strict chart/evaluation;
- original purchase forms remain visible in history.

## CD03 Volume normalization

Given `1L` and `750mL` observations of one commodity:

- both belong to VOLUME_L;
- only their `원/L` rates may share a chart/evaluation.

## CD04 Count normalization

Given `5개` and `10개` observations:

- both belong to EACH;
- `원/개` is the strict comparison basis;
- they are not combined with weight or volume.

## CD05 Multiple strict bases stay separate

If one commodity has WEIGHT_KG and EACH history:

- both may appear on one detail screen;
- each has its own latest/previous/usual/judgment;
- no commodity-wide usual price exists;
- no combined line/chart exists.

## CD06 Contextual bag history

Given `감자 1봉 4,000원` and `감자 2봉 9,000원`:

- LIKE_FORM BAG/봉 cohort may show 4,000원/봉 and 4,500원/봉 as reference;
- CP28 status is CONTEXTUAL_ONLY;
- no cheap/expensive judgment or judgment color is allowed;
- no conversion to kg is allowed.

## CD07 Different forms remain separate

Given `1봉` and `1상자`:

- they produce distinct LIKE_FORM cohorts;
- one form's price must not be baseline/previous/usual for the other;
- neither may be compared to kg/L/each without exact evidence.

## CD08 Real latest purchase versus latest strict comparison

If newest purchase is `1봉` but newest WEIGHT_KG purchase is older:

- latest purchase area shows the `1봉` purchase as the real newest receipt record;
- weight section may separately show its own latest normalized observation;
- the older weight observation must not be relabeled as the commodity's latest purchase.

## CD09 Insufficient strict history

With one WEIGHT_KG observation:

- latest normalized rate may be shown;
- CP28 status = INSUFFICIENT_HISTORY;
- no usual price or cheap/expensive label is invented.

## CD10 No strict comparable history

With only LIKE_FORM or excluded rows:

- detail screen remains useful;
- explicit INFO copy says no direct normalized comparison is available;
- contextual/reference and receipt history remain visible;
- screen does not show a broken/zero strict price.

## CD11 Excluded observation

Given missing PurchaseForm or unallocated receipt discount:

- receipt row remains visible;
- exclusion is explained in safe Korean copy;
- row does not enter any cohort/chart/evaluation.

## CD12 Chart contract

For every Commodity Detail chart:

- exactly one strict basis;
- actual eligible receipt observations only;
- oldest -> newest display;
- usual-price reference only when EVALUATED;
- judgment color only when EVALUATED;
- chart has non-empty Korean accessibility summary.

## CD13 Purchase-form formatting

Examples:

- 500g -> `500g`;
- 1kg -> `1kg`;
- 750mL -> `750mL`;
- 2L -> `2L`;
- 5 each -> `5개`;
- 2 bags -> `2봉`;
- 1 box -> `1상자`;
- OTHER preserves its raw label.

## CD14 Receipt traceability

Every rendered purchase row:

- keeps receipt ID internally;
- shows date/store when available;
- exposes comparison/reference/exclusion status;
- opens existing Receipt Detail without rewriting receipt truth.

## CD15 Responsive contract

- 360dp -> single column;
- 599dp -> single column;
- 600dp -> single column;
- 839dp -> single column;
- 840x479dp -> single column;
- 840x480dp -> two-pane eligible.

## CD16 Scope preservation

CP32 leaves unchanged:

- product schema 2;
- receipt schema 1;
- CP24 identity authority;
- CP26 grouping/comparability rules;
- CP27 basis derivation;
- CP28 thresholds;
- CP29 search authority;
- CP31 STANDARD Product Detail contract;
- Capture/Review behavior;
- forbidden permission posture.

## CD17 Commercial hierarchy

On compact width, the intended order is:

`commodity identity -> real latest purchase -> strict comparisons -> contextual reference forms -> receipt-traceable purchase history`

No debug IDs/enums/reason codes appear as normal user copy.

## CD18 Deterministic metric

Expected metric must cover at minimum:

`commodity_detail_version=1 strict_basis_kinds=3 contextual_policy=1 grouping_not_comparability=1 responsive_cases=6 traceability=1 chart_single_basis=1`

Additional deterministic counts may be included.