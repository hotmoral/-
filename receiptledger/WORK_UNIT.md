# ReceiptLedger public execution work unit

Updated: 2026-10-16 KST

## Current stage

**CP28 — Price Evaluation is COMPLETE.**

- branch: `receiptledger/run-v1-price-evaluation-20261016`
- frozen implementation HEAD: `dd4f98613677ae998932d77f3e5f89d7bddba107`
- canonical Actions: `38834818192` — SUCCESS
- job: `116761457914` — SUCCESS
- artifact ID: `12018776680`
- artifact digest: `sha256:aa90bff8107f34d1974fd9998ceb543fba33fd8b0d402cc972840f9495b9e4b6`
- APK SHA-256: `692e16f0bd6ad23caba3361d831376620bac09e1505f4780d7147402f9fd48f6`
- CP28 tests 8/8 PASS
- CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint 0 errors / 0 warnings
- versionCode 27
- versionName `1.0.26-price-evaluation`

## Frozen CP28 contract

- input = one CP27 eligible comparison cohort only;
- latest purchase excluded from baseline;
- baseline requires minimum 3 prior observations;
- baseline uses most recent maximum 5 prior observations;
- usual price = median;
- material = >=5% AND >=100 minor units;
- extreme = >=15% AND >=500 minor units;
- labels = VERY_CHEAP/CHEAP/TYPICAL/EXPENSIVE/VERY_EXPENSIVE;
- no-judgment = INSUFFICIENT_HISTORY/CONTEXTUAL_ONLY/NON_POSITIVE_BASELINE;
- contextual LIKE_FORM history never gets cheap/expensive labels;
- previous-purchase delta stays separate from usual-price judgment;
- every result exposes reason/baseline/threshold evidence;
- CP27 eligibility and discount rules cannot be bypassed;
- product schema 2 / receipt schema 1 remain unchanged.

## Local quality evidence

`cases=12 evaluated=9 insufficient=1 contextual=1 nonpositive=1 typical=2 cheap=2 very_cheap=1 expensive=2 very_expensive=2 latest_excluded=1 recent_five_window=1 deterministic_repeat=1`

## Known limitations

- threshold constants are fixed V1 personal-history heuristics;
- no seasonality/time-decay model;
- old prices can remain in baseline for infrequently purchased goods;
- contextual package forms remain intentionally unjudged;
- no market-price lookup or final commercial UI.

## Next planned work unit

**CP29 — Search / Browse**

Before implementation:

1. define query fields/ranking over stable product/commodity identity;
2. make brand/product/spec/category/safe alias discovery useful;
3. support store/recent/frequent/price-change browse facts without changing identity;
4. keep fuzzy discovery suggestion-only, never silent merge authority;
5. define deterministic no-result/unresolved behavior;
6. preserve receipt traceability and price-evaluation scope;
7. measure query cost for later performance hardening;
8. avoid final visual design before CP30 Design System.

## Group discipline

Recover canonical GitHub state -> restate essential goal/non-goals -> inspect material contradictions -> resolve cheap issues before code -> implement smallest coherent proof -> CI/evidence -> freeze refs -> synchronize handoff -> stop before next unauthorized checkpoint.

## Public/privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipt photos, personal purchase DBs/backups, identifiers or uncleared assets.

Forbidden APK permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless explicitly reauthorized.

## Stop condition

**CP28 is complete. Await explicit authorization for CP29.**
