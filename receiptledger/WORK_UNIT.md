# ReceiptLedger public execution work unit

Updated: 2026-10-16 KST

## Current stage

**CP23 — Receipt Product Semantics is COMPLETE.**

- branch: `receiptledger/run-v1-receipt-product-semantics-20261016`
- frozen implementation HEAD: `5bffb66bd43814f8d638791b5697f79ff089028b`
- canonical Actions: `38822100885` — SUCCESS
- artifact ID: `12013477721`
- artifact digest: `sha256:fa22d082545adae7c414b0f1c089604174341f7e879c1acd5e4677e1dc2b7195`
- APK SHA-256: `e4e64f85f9700089b32f9f0b8121eef0a2f565d09b5428599d3717296c1b8324`
- semantics tests: 7/7 PASS
- catalog tests: 15/15 PASS
- persistence tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionCode 22
- versionName `1.0.21-receipt-product-semantics`

## Frozen CP23 contract

- parser consumes existing receipt item name only;
- parser outputs semantic evidence, never catalog identity;
- parsed fields are `PARSED_FROM_RECEIPT / UNCONFIRMED`;
- brand requires explicit bracket or caller-supplied known-brand prefix;
- first-token brand guessing is forbidden;
- only explicit parenthetical non-numeric variant is separated;
- explicit pack count/multipack syntax is parsed;
- standalone physical measure is dual interpretation + review;
- 봉/상자/단 are preserved raw purchase forms without conversion;
- 팩/개 are context-sensitive and review-gated;
- product schema v2 and receipt schema v1 remain unchanged;
- receipt-derived price truth remains unchanged.

## Local quality evidence

`fixtures=26 expected_fields=68 predicted_fields=66 correct_fields=64 precision_ppm=969696 recall_ppm=941176 review_required=13 semantic_ready=13 ambiguous=10 ambiguous_reviewed=10 no_invention_negatives=2`

This deliberately exposes conservative misses instead of hiding them with speculative parsing.

## Superseded CI note

Run `38821795314` failed only on minSdk23 lint compatibility because the first sorting implementation used collection convenience APIs treated as API24+.

Fix: API23-safe sorting only. No minSdk increase, no lint suppression, no domain broadening. Final run `38822100885` is canonical.

## Next planned work unit

**CP24 — Identity Resolver V2**

Before any new auto-link authority:

1. define GLOBAL vs MERCHANT alias precedence;
2. define exactly which confirmed knowledge may auto-link;
3. use CP23 semantic candidates only as evidence/ranking input;
4. fail ambiguous candidates to review;
5. measure false merge and false split;
6. measure automatic-link success and incorrect automatic-link rate;
7. measure review burden;
8. prove repeat confirmed purchases reduce review burden;
9. keep category and parser confidence from becoming identity authority.

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

**CP23 is complete. Await explicit authorization for CP24.**
