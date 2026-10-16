# ReceiptLedger public execution work unit

Updated: 2026-10-16 KST

## Current stage

**CP26 — Commodity / Non-standard V2 is COMPLETE.**

- branch: `receiptledger/run-v1-commodity-nonstandard-v2-20261016`
- frozen implementation HEAD: `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`
- canonical Actions: `38829423445` — SUCCESS
- job: `116744485504` — SUCCESS
- artifact ID: `12016292501`
- artifact digest: `sha256:6ad4342d61274530aecc090fbe7caa8f606f3a20c113285e3b18cd86893336bd`
- APK SHA-256: `250d4d00bb93334fede3873c92e85b63d1ccd05ee5d09f9a4c7970fb366b90cb`
- commodity tests: 8/8 PASS
- category tests: 8/8 PASS
- identity tests: 8/8 PASS
- semantics tests: 7/7 PASS
- catalog tests: 15/15 PASS
- persistence tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionCode 25
- versionName `1.0.24-commodity-nonstandard-v2`

## Frozen CP26 contract

- commodity grouping resolves to existing NON_STANDARD stable IDs only;
- authority: MERCHANT exact alias -> GLOBAL exact alias -> exact commodity canonical name -> safe REVIEW suggestion -> unresolved;
- purchase form and category cannot prove commodity identity;
- substring/fuzzy similarity cannot auto-group;
- modifier-bearing names remain review-gated until confirmation;
- STANDARD-target aliases are cross-kind conflicts;
- explicit confirmation reuses CP24 least-authority contextual alias learning;
- original quantity/unit/raw unit label and provenance remain observation-specific;
- exact quantity basis is limited to exact built-in dimensions (kg/g, L/mL, count);
- same package form such as 봉 vs 봉 is `SAME_FORM_ONLY`, not normalized price authority;
- guessed 봉/팩/상자 conversion is forbidden;
- grouping != comparability;
- product schema 2 and receipt schema 1 remain unchanged;
- receipt-derived price truth remains unchanged.

## Local quality evidence

`fixtures=25 known_commodity=21 auto_groups=18 correct_auto_groups=18 incorrect_auto_groups=0 false_group=0 review_suggestions=2 false_split=1 negative_fixtures=4 raw_form_cases=12 raw_form_preserved=12 repeat_cases=3 repeat_reused=3`

Interpretation:

- 18/18 automatic groups correct;
- false grouping 0;
- safe review suggestions 2;
- visible false split risk 1/21;
- raw form preservation 12/12;
- confirmed repeat reuse 3/3.

The false split is intentionally visible. Do not remove it through unsafe matching broadening.

## Next planned work unit

**CP27 — Price Intelligence V2**

Before implementation:

1. define one canonical receipt-traceable comparison price for each eligible purchase observation;
2. define line amount / purchased quantity / one package-unit semantics explicitly;
3. include item-specific discounts only when attributable without guessing;
4. retain unallocated receipt-level coupon/benefit provenance without fabricated allocation;
5. define exclusion rules for invalid/incomplete observations;
6. STANDARD comparisons must stay within the correct exact stable product identity;
7. NON_STANDARD comparisons must respect CP26 form relation and never infer package-form conversion;
8. define latest/previous/delta/min/max/mean/median/period/store statistics deterministically;
9. keep insufficient/incomparable states first-class;
10. do not begin CP28 cheap/normal/expensive thresholds early.

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

**CP26 is complete. Await explicit authorization for CP27.**
