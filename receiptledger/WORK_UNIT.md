# ReceiptLedger public execution work unit

Updated: 2026-10-16 KST

## Current stage

**CP27 — Price Intelligence V2 is COMPLETE.**

- branch: `receiptledger/run-v1-price-intelligence-v2-20261016`
- frozen implementation HEAD: `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`
- canonical Actions: `38831623548` — SUCCESS
- job: `116751473084` — SUCCESS
- artifact ID: `12017014494`
- artifact digest: `sha256:660ead5ea86bae86fbd6cf67643866c17acfa5f144c9b1d06f29d50f71f44dd5`
- APK SHA-256: `8455e4ce23e15c6a113e87ddbd0ddb000e41d9f1849e7f431c9ed5dfbfabe1bc`
- CP27 tests: 8/8 PASS
- legacy price tests: 2/2 PASS
- CP26 commodity: 8/8 PASS
- CP25 category: 8/8 PASS
- CP24 identity: 8/8 PASS
- CP23 semantics: 7/7 PASS
- CP21 catalog: 15/15 PASS
- CP22 persistence: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionCode 26
- versionName `1.0.25-price-intelligence-v2`

## Frozen CP27 contract

- comparison price is receipt-traceable numerator/denominator evidence;
- STANDARD basis is one exact stable product package;
- kg/g, L/mL and count use exact normalized quantity bases;
- same 봉/팩/상자/단/OTHER form is contextual only;
- different forms are never combined by guessed conversion;
- PASS/PASS_WITH_WARNINGS only can contribute to aggregates;
- MISMATCH/INCOMPLETE stay visible but excluded;
- sole-item discount can be exactly attributed to its only item;
- multi-item receipt discount without persisted attribution is excluded from aggregates;
- item arithmetic conflict is excluded rather than silently corrected;
- latest/previous/delta/delta-percent/min/max/mean/median are deterministic per cohort;
- date/store scopes are supported;
- price judgment labels are deferred to CP28;
- product schema 2 / receipt schema 1 / legacy price core remain unchanged.

## Local quality evidence

`observations=10 eligible=7 excluded_discount=1 excluded_invalid=1 missing_form=1 standard_cohorts=1 commodity_strict_cohorts=1 commodity_contextual_cohorts=1 scope_checks=2 receipt_traceable_rates=7`

Interpretation:

- every eligible rate in the bounded fixture is receipt-traceable;
- one deliberately unallocated discount stays excluded;
- one invalid receipt stays excluded;
- one missing commodity form stays excluded;
- strict and contextual commodity cohorts remain separate;
- store/date filters passed.

## Next planned work unit

**CP28 — Price Evaluation**

Before implementation:

1. define minimum data sufficiency;
2. define the historical baseline/window;
3. choose a robust usual-price statistic;
4. freeze explicit cheap/normal/expensive thresholds;
5. handle sparse data and zero baseline safely;
6. decide whether contextual LIKE_FORM history can receive judgment and label its weaker evidence;
7. provide transparent explanation fields;
8. never mix CP27 comparison cohorts;
9. do not introduce online price or free-form generative judgment.

## Group discipline

- recover canonical GitHub state;
- restate essential goal/non-goals;
- inspect relevant contradictions and risks;
- resolve cheap contract issues before code;
- avoid unrelated cleanup and speculative scope;
- implement smallest coherent proof;
- run scoped CI/evidence;
- freeze exact refs;
- synchronize handoff materials;
- stop before the next unauthorized checkpoint.

## Public/privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipt photos, personal purchase DBs/backups, identifiers or uncleared assets.

Forbidden APK permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless explicitly reauthorized.

## Stop condition

**CP27 is complete. Await explicit authorization for CP28.**
