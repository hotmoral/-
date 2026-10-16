# ReceiptLedger V1 — Price Evaluation Golden Vectors

Updated: 2026-10-16 KST
Checkpoint: CP28

## Policy constants

- minimum prior observations: 3
- baseline window: latest excluded, then most recent 5 prior observations
- usual price: median
- material threshold: >=5% AND >=100 minor units
- extreme threshold: >=15% AND >=500 minor units
- contextual LIKE_FORM: no judgment

## Golden vectors

| ID | Latest | Prior baseline inputs | Expected |
|---|---:|---|---|
| E01 | 14,000 | 10,000 / 10,200 / 9,800 / 10,100 / 9,900; older 50,000 ignored | usual 10,000; VERY_EXPENSIVE |
| E02 | 12,000 | 10,000 / 10,000 | INSUFFICIENT_HISTORY |
| E03 | 7,000 | 봉 4,000 / 4,200 / 4,100 | CONTEXTUAL_ONLY |
| E04 | 100 | 0 / 0 / 0 | NON_POSITIVE_BASELINE |
| E05 | 10,400 | 10,000 / 10,000 / 10,000 | TYPICAL (+4%) |
| E06 | 1,080 | 1,000 / 1,000 / 1,000 | TYPICAL (+8%, but +80 only) |
| E07 | 9,000 | 10,000 / 10,000 / 10,000 | CHEAP |
| E08 | 11,000 | 10,000 / 10,000 / 10,000 | EXPENSIVE |
| E09 | 8,000 | 10,000 / 10,000 / 10,000 | VERY_CHEAP |
| E10 | 12,000 | 10,000 / 10,000 / 10,000 | VERY_EXPENSIVE |
| E11 | 10,500 | 10,000 / 10,000 / 10,000 | EXPENSIVE at exact +5% boundary |
| E12 | 11,500 | 10,000 / 10,000 / 10,000 | VERY_EXPENSIVE at exact +15% boundary |
| E13 | 9,500 | 10,000 / 10,000 / 10,000 | CHEAP at exact -5% boundary |
| E14 | 8,500 | 10,000 / 10,000 / 10,000 | VERY_CHEAP at exact -15% boundary |

## Separation vector

Latest 12,000; immediately previous 8,000; older prior 10,000 / 10,000:

- previous delta = +4,000 / +50%;
- usual-price median = 10,000;
- usual delta = +2,000 / +20%;
- judgment = VERY_EXPENSIVE.

This proves "지난번보다" and "평소보다" are distinct outputs.

## Window vector

When the cohort contains latest 14,000, recent five prior values 10,000 / 10,200 / 9,800 / 10,100 / 9,900, and an older 50,000 outlier:

- latest 14,000 is excluded from baseline;
- old 50,000 outside the recent-five window is excluded;
- baseline median = 10,000.

No vector permits cross-cohort mixing or judgment on LIKE_FORM.
