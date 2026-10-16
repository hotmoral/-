# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP28_PRICE_EVALUATION_CLOSEOUT.md`
4. `receiptledger/CP28_PRICE_EVALUATION_EVIDENCE.md`
5. `receiptledger/CP28_PRICE_EVALUATION_PLAN.md`
6. `receiptledger/PRICE_EVALUATION_CONSISTENCY_REVIEW.md`
7. `receiptledger/PRICE_EVALUATION_GOLDEN_VECTORS.md`
8. `receiptledger/CP27_PRICE_INTELLIGENCE_V2_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP28 — Price Evaluation — PASS / COMPLETE**

- branch: `receiptledger/run-v1-price-evaluation-20261016`
- predecessor handoff: `c9131d0c6c8e799390ff37a370a1b1c77c38647a`
- frozen implementation HEAD: `dd4f98613677ae998932d77f3e5f89d7bddba107`
- canonical Actions: `38834818192` — SUCCESS
- job: `116761457914` — SUCCESS
- artifact ID: `12018776680`
- artifact digest: `sha256:aa90bff8107f34d1974fd9998ceb543fba33fd8b0d402cc972840f9495b9e4b6`
- APK SHA-256: `692e16f0bd6ad23caba3361d831376620bac09e1505f4780d7147402f9fd48f6`
- CP28 tests 8/8 PASS
- CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint 0 errors / 0 warnings
- versionName `1.0.26-price-evaluation`, versionCode 27

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색·탐색 -> 과거 가격과 현재 가격 판단`

CP28 now supplies the deterministic personal-history judgment layer.

## 3. Frozen evaluation policy

Input: exactly one CP27 eligible comparison cohort.

Baseline:

- latest observation excluded;
- minimum prior observations = 3;
- use at most 5 most recent prior observations;
- usual price = median.

Material change requires >=5% AND >=100 minor units.
Extreme change requires >=15% AND >=500 minor units.
Exact boundaries are inclusive.

Judgments: `VERY_CHEAP / CHEAP / TYPICAL / EXPENSIVE / VERY_EXPENSIVE`.

No-judgment states: `INSUFFICIENT_HISTORY / CONTEXTUAL_ONLY / NON_POSITIVE_BASELINE`.

## 4. Explainability / separation

Every result preserves:

- basis/strength;
- status/judgment/reason code;
- latest and immediately previous price;
- previous delta/percent;
- baseline count/window and baseline receipt IDs;
- usual-price median;
- latest-vs-usual delta/percent;
- frozen thresholds.

`지난번보다` and `평소보다` are intentionally separate calculations.

## 5. Contextual commodity boundary

`LIKE_FORM` package/form histories are contextual only. Equal 봉/팩/상자 label does not prove equal physical contents, so CP28 never produces cheap/expensive labels for those cohorts.

Strict kg/L/each cohorts may be evaluated because CP27 provides exact normalized comparison bases.

## 6. Canonical metric

`cases=12 evaluated=9 insufficient=1 contextual=1 nonpositive=1 typical=2 cheap=2 very_cheap=1 expensive=2 very_expensive=2 latest_excluded=1 recent_five_window=1 deterministic_repeat=1`

Synthetic deterministic contract evidence only.

## 7. Frozen upstream rules

- stable catalog ID remains identity authority;
- product schema 2 / receipt schema 1;
- CP27 `priceintel/**` frozen;
- legacy `price/**` frozen;
- identity/category/commodity rules unchanged;
- CP27 discount/validation exclusions cannot be bypassed;
- no duplicate mutable price table;
- no market-price/network/generative-AI judgment;
- no permission/privacy expansion.

## 8. Deliberate limitations

- thresholds are fixed V1 personal-history heuristics;
- baseline is observation-count based rather than seasonal/time-decay;
- old observations may remain relevant for infrequently purchased goods;
- contextual forms remain unjudged;
- no commercial UI/search implementation in CP28.

Do not solve these through unrelated scope expansion.

## 9. Next planned implementation checkpoint

**CP29 — Search / Browse**

Required direction:

1. define searchable product/commodity fields and ranking;
2. support product/commodity name, confirmed safe aliases, brand/specification and category;
3. include store context without turning store text into identity authority;
4. support recent/frequent/price-change browse views using existing derived facts;
5. fuzzy text may assist discovery but must never silently merge identities;
6. keep search read-only with respect to catalog equality;
7. define deterministic empty/no-result and unresolved states;
8. keep query performance measurable for CP36;
9. do not jump into final commercial visual polish before CP30 Design System.

CP29 is planned, not automatically authorized.

## 10. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipts, personal purchase DB/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

## 11. Group discipline

Recover canonical state -> restate essence/non-goals -> inspect material contradictions -> implement smallest coherent proof -> run scoped CI/evidence -> freeze refs -> synchronize handoff -> stop before next unauthorized checkpoint.

## 12. Stop condition

**CP28 is complete and handoff-synchronized. Await explicit authorization for CP29.**
