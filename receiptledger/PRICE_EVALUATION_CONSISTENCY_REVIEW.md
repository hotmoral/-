# ReceiptLedger V1 — Price Evaluation Consistency Review

Updated: 2026-10-16 KST
Checkpoint: CP28

## 1. Consistency verdict

CP28 is consistent with CP20–CP27 when implemented strictly as a read-only judgment layer over one CP27 cohort.

## 2. Material risks checked

### Self-referential baseline
If the latest purchase is included in the usual-price baseline, a large current change pulls its own reference toward itself. Resolution: exclude latest; use only prior observations.

### Stale/all-history distortion
An all-history mean can be dominated by old prices or outliers. Resolution: recent-prior window capped at 5; use median.

### Sparse confidence inflation
One previous purchase is not a stable usual price. Resolution: require at least 3 prior observations before labeling.

### Tiny-difference overstatement
Percentage-only rules exaggerate cheap low-price goods; absolute-only rules exaggerate high-price goods. Resolution: material/extreme labels require both percentage and absolute gates.

### Contextual package-form overclaim
`봉/팩/상자` cohorts may contain different physical contents despite same raw form. Resolution: `CONTEXTUAL_LIKE_FORM` is history-only and never receives cheap/expensive judgment.

### Zero baseline division
A zero/free historical median cannot support a meaningful percent deviation. Resolution: return `NON_POSITIVE_BASELINE`, no percentage judgment.

### Previous vs usual conflation
Latest-vs-previous answers "지난번보다?" while latest-vs-median answers "평소보다?". Resolution: expose both separately.

### Cross-cohort leakage
Weight, volume, each and package-form histories cannot be mixed. Resolution: evaluator accepts exactly one already-built CP27 cohort.

### Discount reinterpretation
CP28 must not recover observations CP27 excluded for unallocated discounts. Resolution: no receipt access and no price derivation in CP28.

## 3. Frozen policy

- prior minimum = 3;
- recent-prior window = 5;
- usual price = median;
- material = >=5% AND >=100 minor units;
- extreme = >=15% AND >=500 minor units;
- exact boundaries inclusive;
- latest excluded;
- contextual LIKE_FORM not judged.

The constants are V1 personal-history heuristics. They are explicit and inspectable rather than AI opinion.

## 4. Storage / authority

No persistence/schema change is required. Evaluation is derived on demand from CP27 facts. It has no authority to change product identity, category, commodity grouping, purchase form, receipt validation, discounts or price evidence.

## 5. Scope decision

Do not add seasonality, external prices, forecasting, configurable thresholds or commercial UI in CP28. Those would expand the problem before the core personal-history decision contract is proven.
