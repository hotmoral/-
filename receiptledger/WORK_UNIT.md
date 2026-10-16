# ReceiptLedger public execution work unit

Updated: 2026-10-16 KST

## Current stage

**CP34 — Commercial UI Shell is COMPLETE.**

- branch: `receiptledger/run-v1-commercial-ui-shell-20261016`
- predecessor handoff: `2a15e14e9897aa9785762faef1568254fbeb5f82`
- frozen implementation HEAD: `d9764b1447aefaaf3e3fdc5785c72c7c98e8314e`
- canonical Actions: `38878681881` — SUCCESS
- job: `116899840083` — SUCCESS
- artifact ID: `12036721843`
- artifact digest: `sha256:61e31f76bcf1e8d4e7dc596807b2aacd6c7774ad8e9fe05f36b09b59d4a95258`
- APK SHA-256: `64899bfdd715780ecb864f033896f66e2c89d7186da338f2dd59c7fc2033a2af`
- versionCode 33
- versionName `1.0.32-commercial-ui-shell`
- lint: 0 errors / 0 warnings
- CP34 7/7 + CP33 13/13 + CP32 11/11 + CP31 9/9 + CP29 8/8 packaged key regressions PASS.

## Frozen CP34 contract

- HomeActivity is the real packaged launcher;
- Home primary CTA enters frozen CP33 receipt-add flow;
- discovery uses frozen CP29 read-only APIs only;
- search, recent, frequent and category browse do not mutate identity;
- STANDARD stable ID opens CP31 Product Detail;
- NON_STANDARD stable ID opens CP32 Commodity Detail;
- unsupported/unclassified items are not promoted by navigation;
- receipt history opens exact ReceiptDetail rows;
- CP31/32 purchase rows retain exact receipt provenance;
- legacy PriceHistoryActivity is no longer Library's primary browse destination;
- Home/Search/Library long content is vertically scrollable;
- product schema 2 / receipt schema 1 unchanged;
- no new network/broad permissions;
- no Compose/Material migration.

## Commercial shell result

Normal app flow:

`홈 -> 영수증 추가 -> 자동 분석/필요 검토/저장 -> 검색·카테고리 -> 제품·품목 상세 -> 구매 영수증 근거`

The product now exposes the outcome—personal price memory—rather than presenting capture as the whole application.

## Identity and price authority

CP34 has no authority to:

- create/merge/relink product identity from search relevance;
- confirm new aliases;
- reinterpret category as identity;
- recompute CP27 comparison basis;
- reimplement CP28 thresholds;
- fabricate market-price/savings claims;
- reinterpret CP33 save readiness.

The shell only connects already-frozen services and screens.

## Local quality evidence

`CP34_METRICS shell_version=1 launcher_home=1 add_receipt=1 search_browse=1 category_browse=1 standard_detail=1 commodity_detail=1 receipt_history=1 legacy_price_entry_removed=1 schema_unchanged=1`

Canonical artifact inspection confirms:

- HomeActivity packaged as launchable activity;
- APK SHA above;
- lint `No issues found.`;
- forbidden CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE permissions absent;
- internal dynamic-receiver permission only;
- CP34/33/32/31/29 key test XMLs zero failure/error/skip.

## Pre-closeout corrections

CP34 deliberately was not closed at the first implementation state.

1. run `38877757713`: compilation failed because five new layout references used nonexistent `SPACE_5_DP`; corrected to frozen CP30 `SPACE_6_DP` (24dp);
2. run `38877971396`: full green but post-green review found Library constrained-height/large-text accessibility risk and missing list-read failure state;
3. final `d9764b...`: Library hardened; canonical run `38878681881` clean green.

## Known limitations

- no private real-receipt accuracy campaign;
- no emulator/device screenshot comparison;
- no physical-device usability study;
- no representative 1k/10k performance benchmark;
- no release signing evidence;
- CP35 and CP36 remain future validation/hardening stages.

## Next planned work unit

**CP35 — Real Receipt Evaluation**

Before implementation:

1. recover CP34 frozen executable and handoff refs separately;
2. define public-safe synthetic and/or explicitly approved sanitized receipt fixture policy;
3. define end-to-end correct purchase registration as the primary success metric;
4. cover receipt structure, product/commodity identity outcome, quantity/price registration, comparison eligibility and receipt provenance;
5. distinguish safe unresolved/review-required outcomes from incorrect confident registration;
6. measure review burden and confirmed repeat-use behavior where fixtures permit;
7. preserve CP20–34 identity/price/review/schema/privacy contracts;
8. avoid performance/index/cache work reserved for CP36;
9. package deterministic evidence and failure taxonomy;
10. compare plan vs actual even if CI is green;
11. synchronize docs-only handoff;
12. stop before CP36.

## Group discipline

- recover canonical GitHub state;
- restate essential goal/non-goals;
- inspect materially relevant contradictions only;
- fix cheap contract gaps before closure even if CI is green;
- avoid unrelated cleanup/speculative scope;
- implement the smallest coherent proof;
- run scoped CI/evidence;
- freeze exact executable refs;
- synchronize handoff materials docs-only;
- verify post-boundary changes;
- stop before the next unauthorized checkpoint.

## Public/privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipt photos, personal purchase DBs/backups, identifiers or uncleared assets.

## Stop condition

**CP34 is complete. Await explicit authorization for CP35.**
