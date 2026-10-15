# ReceiptLedger public execution work unit

Updated: 2026-10-16 KST

## Current stage

**CP24 — Identity Resolver V2 is COMPLETE.**

- branch: `receiptledger/run-v1-identity-resolver-v2-20261016`
- frozen implementation HEAD: `4b556afd4dd52b68cf768e937bb456665ad4c231`
- canonical Actions: `38824134990` — SUCCESS
- job: `116727478370` — SUCCESS
- artifact ID: `12014915453`
- artifact digest: `sha256:4740590ca2c7d7525842aa3ebe6ec7964911d303322ebad77b5701344ce76867`
- APK SHA-256: `0656c60110ba7debcb0801ddee048cd2220b959c2119539a79274eebbc05eb6e`
- identity tests: 8/8 PASS
- CP23 semantics: 7/7 PASS
- CP21 catalog: 15/15 PASS
- CP22 persistence: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionCode 23
- versionName `1.0.22-identity-resolver-v2`

## Frozen CP24 contract

- resolver reuses existing stable IDs only; it never auto-creates or merges entities;
- authority order: MERCHANT exact alias -> GLOBAL exact alias -> unique strict semantic exact -> suggestion/review -> unresolved;
- merchant-specific exact alias is more specific than a different GLOBAL mapping;
- dangling aliases and strong explicit brand/variant/non-ambiguous specification contradictions are review-gated;
- strict semantic auto-link requires confirmed exact productName + confirmed exact specification and symmetric confirmed brand/variant when applicable;
- CP23 ambiguity blocks semantic auto-link;
- category/store/parser confidence do not prove identity;
- fuzzy/edit-distance/embedding/phonetic similarity is not automatic identity authority;
- user-confirmed alias learning defaults to merchant scope when merchant context exists;
- NON_STANDARD semantic grouping remains CP26;
- product schema v2 and receipt schema v1 are unchanged;
- receipt-derived price truth remains unchanged.

## Local quality evidence

`fixtures=24 known_identity=20 auto_links=14 correct_auto_links=14 incorrect_auto_links=0 false_merge=0 false_split=1 review_required=6 unresolved=4 repeat_cases=4 repeat_reused=4`

Important interpretation:

- zero false merges / incorrect automatic decisions;
- repeat confirmation reuse 100%;
- one known-product fragmentation-risk fixture = exactly 5%;
- the fragmentation risk remains visible rather than being hidden by unsafe matching expansion.

## Next planned work unit

**CP25 — Category System**

Before implementation:

1. define the smallest useful V1 taxonomy/hierarchy for client browsing;
2. determine stable category identity and persistence needs without making category part of product identity;
3. define assignment/suggestion authority and review boundary;
4. define user correction and repeat reuse;
5. verify STANDARD and NON_STANDARD can both carry category metadata without changing their identity semantics;
6. measure suggestion accuracy and review burden locally;
7. preserve privacy/offline/schema/price-truth contracts unless a justified minimal persistence change is required.

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

**CP24 is complete. Await explicit authorization for CP25.**
