# ReceiptLedger public execution work unit

Updated: 2026-10-16 KST

## Current stage

**CP31 — Product Detail is COMPLETE.**

- branch: `receiptledger/run-v1-product-detail-20261016`
- predecessor handoff: `f67e39654d1d4cfdc2cd6fce8e7c16f72ed34b60`
- frozen implementation HEAD: `1d2e7ef67e949af9098027a78e30551c228c255c`
- canonical Actions: `38852423981` — SUCCESS
- job: `116816787905` — SUCCESS
- artifact ID: `12025398048`
- artifact digest: `sha256:d4ad68382e6b666f796345c452c42e18f03ef1bd3084d18182a78059da0b4b0f`
- APK SHA-256: `8be04d623cc0bea95f87868dca2a45a774440e0dddc3cd32be5a63baf867e3ae`
- CP31 tests: 9/9 PASS
- CP30 9/9, CP29 8/8, CP28 8/8, CP27 8/8 PASS in packaged XML evidence
- full prior regression suite required by workflow
- lint: 0 errors / 0 warnings
- versionCode 30
- versionName `1.0.29-product-detail`

## Frozen CP31 contract

- STANDARD products only;
- Product Detail is a read-only projection over canonical catalog/CP27/CP28/receipt data;
- no duplicate mutable price truth;
- stable catalog ID remains identity authority;
- structured identity fields displayed only when canonical V2 data exists;
- legacy STANDARD falls back to canonical name without guessing metadata;
- price basis = `STANDARD_PACKAGE` only;
- latest/previous/usual/judgment remain distinct frozen CP28 concepts;
- chart uses actual eligible purchases only, oldest -> newest;
- usual-price reference and judgment color only when CP28 permits;
- excluded observations remain provenance and never enter judgment/chart values;
- every purchase row preserves receipt navigation;
- product schema 2 / receipt schema 1 unchanged.

## Commercial UI result

Design direction:

**quiet confidence / price-first / evidence-backed**

Compact hierarchy:

`identity -> recent price -> judgment/reason -> previous/usual -> chart -> purchase history`

CP30 typography/spacing/radius/elevation/semantic/responsive grammar is reused rather than forked.

History rows are >=64dp. Chart exposes Korean accessibility summary, avoids per-draw Path allocation and uses Android SP dimension conversion compatible with nonlinear font scaling.

Expanded two-pane remains gated by CP30: width >=840dp and height >=480dp.

## Local quality evidence

`CP31_METRICS product_detail_version=1 standard_basis=1 identity_fallbacks=1 price_states=8 responsive_cases=6 traceability=1 chart_single_basis=1 purchase_rows=4`

Canonical artifact inspection confirms:

- APK SHA above;
- lint `No issues found.`;
- CP31/CP30/CP29/CP28/CP27 packaged test XMLs all have zero failures/errors/skips;
- packaged permissions contain only the internal dynamic-receiver permission.

## Pre-closeout corrections

CP31 was not closed at the first green state.

1. initial CI found two Java implementation errors;
2. later green run still had chart `DrawAllocation` and was rejected for closure;
3. next green run still used direct `scaledDensity` for chart text and was rejected for closure;
4. final `1d2e7ef...` corrected both visual-runtime quality issues and passed full canonical Actions `38852423981` with clean lint.

## Known limitations

- NON_STANDARD Commodity Detail is not built yet;
- Capture/Review UX V2 remains later work;
- commercial home/navigation shell remains later work;
- final icon artwork/library and dark-theme finalization remain open;
- CP31 does not include emulator/device screenshot comparison or real-user usability evidence.

## Next planned work unit

**CP32 — Commodity Detail**

Before implementation:

1. recover CP31 frozen and handoff refs separately;
2. re-read CP26/27 commodity grouping/comparability contracts;
3. define NON_STANDARD detail read model without duplicating truth;
4. keep WEIGHT_KG / VOLUME_L / EACH cohorts separate;
5. keep SAME_FORM/LIKE_FORM contextual/reference-only unless strict comparability exists;
6. never fake-convert bag/pack/box/count into kg/L/each;
7. make no-judgment/contextual states visually unmistakable;
8. preserve store/date/receipt provenance;
9. consume CP30 design grammar and CP31 quality bar where appropriate;
10. do not start CP33 Capture/Review or CP34 shell work in the same checkpoint;
11. finish scoped CI/evidence/handoff and stop before CP33.

## Group discipline

- recover canonical GitHub state;
- restate essential goal/non-goals;
- inspect materially relevant contradictions;
- fix cheap contract gaps before closure even if CI is green;
- avoid unrelated cleanup/speculative scope;
- implement smallest coherent proof;
- run scoped CI/evidence;
- freeze exact refs;
- synchronize handoff materials;
- verify post-boundary changes are documentation-only;
- stop before next unauthorized checkpoint.

## Public/privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipt photos, personal purchase DBs/backups, identifiers or uncleared assets.

Forbidden APK permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless explicitly reauthorized.

## Stop condition

**CP31 is complete. Await explicit authorization for CP32.**
