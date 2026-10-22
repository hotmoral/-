# Timing Defense — High-Mastery Player Anchor Amendment V0.1

Date: 2026-10-22 KST  
Status: **USER-SUPPLIED CALIBRATION CLASSIFICATION / MEASURE BEFORE CONFIRMING**

## Purpose
The primary local calibration player reports that they should not be treated as an ordinary skilled player and instead consider their play level above the intended `SKILLED_V2` band.

This amendment prevents a strong local trace from being incorrectly promoted into the ordinary skilled population model.

## Authority boundary
Until observed H0–H5 traces are collected and reviewed:

- the user's traces MUST NOT be used as direct evidence for `SKILLED_V2_CENTRAL`;
- the default classification for those traces is `HIGH_MASTERY_STRESS_CANDIDATE`;
- `HIGH_MASTERY_STRESS_CANDIDATE` is a provisional calibration label, not an objective rank claim;
- reclassification may occur only after trace review and comparison with later skilled-player evidence;
- the non-T1 `<60%` full-Tier clear target continues to apply to fitted `SKILLED_V2_CENTRAL`, not to the high-mastery candidate.

## Intended use of the user's traces
Use the traces primarily to measure:

- upper-tail timing accuracy and cadence;
- combo survival at 40/60+ bands;
- heavy and P×P reliability;
- target-turnover reacquisition under strong play;
- stateful telegraph response latency;
- whether CHARGER/SIEGER/SUPPORTER/SPLITTER role expression survives high-throughput play;
- whether strong play can erase intended mechanics before readable counterplay;
- a practical stress ceiling for future `HIGH_MASTERY_STRESS` simulation.

Do not use the traces to make the game harder until ordinary-skilled evidence exists.

## Difficulty calibration rule
Correct order:

```text
observe high-mastery candidate
+ observe/derive ordinary-skilled evidence separately
-> fit SKILLED_V2_CONSERVATIVE/CENTRAL/STRONG
-> keep HIGH_MASTERY_STRESS separate
-> evaluate non-T1 Central full-Tier clear rate
-> tune game difficulty if needed
```

Forbidden:

```text
user is very strong
-> call user SKILLED_V2_CENTRAL
-> tune every Tier until user's clear rate <60%
```

That would overstate ordinary skilled ability and bias the campaign toward excessive difficulty.

## Harness metadata
For the first local H0–H5 pilot:

- keep existing `classId` informational only;
- set collection interpretation to `HIGH_MASTERY_STRESS_CANDIDATE` in the analysis ledger/report;
- do not change the trace schema solely for this label before smoke validation;
- preserve raw traces so later reclassification is possible without replaying the session.

## Relationship to combo40 anchor
The existing statement that combo40 is ordinary-skilled-achievable remains valid as a lower calibration anchor.
The user's ability to exceed that anchor does not redefine the skilled center.

## Exit condition
This amendment can be replaced by a fitted classification only after:

1. H0/H3/H4 smoke PASS;
2. small H0–H5 pilot collected;
3. dataset validation PASS;
4. trace-quality review completed;
5. enough comparative evidence exists to distinguish ordinary skilled from high mastery.
