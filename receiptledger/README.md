# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP31_PRODUCT_DETAIL_CLOSEOUT.md`
4. `CP31_PRODUCT_DETAIL_EVIDENCE.md`
5. `CP31_PRODUCT_DETAIL_PLAN.md`
6. `PRODUCT_DETAIL_CONSISTENCY_REVIEW.md`
7. `PRODUCT_DETAIL_GOLDEN_VECTORS.md`
8. `CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
9. `CP30_DESIGN_SYSTEM_FOUNDATION_EVIDENCE.md`
10. `PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `WORK_UNIT.md`

GitHub is canonical; verify current handoff ref and frozen executable ref separately before relying on old chat context.

## Current boundary

**CP31 — Product Detail — COMPLETE**

- branch `receiptledger/run-v1-product-detail-20261016`
- predecessor handoff `f67e39654d1d4cfdc2cd6fce8e7c16f72ed34b60`
- frozen implementation HEAD `1d2e7ef67e949af9098027a78e30551c228c255c`
- canonical Actions `38852423981` — SUCCESS
- job `116816787905` — SUCCESS
- artifact ID `12025398048`
- artifact digest `sha256:d4ad68382e6b666f796345c452c42e18f03ef1bd3084d18182a78059da0b4b0f`
- APK SHA-256 `8be04d623cc0bea95f87868dca2a45a774440e0dddc3cd32be5a63baf867e3ae`
- CP31 9/9, CP30 9/9, CP29 8/8, CP28 8/8, CP27 8/8 PASS in packaged XML evidence
- lint `No issues found.`
- version `1.0.29-product-detail`, versionCode 30

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable judgment -> find/browse -> inspect`

CP31 implements the first commercial `inspect` destination for STANDARD products without changing upstream business truth.

## CP31 Product Detail

Design direction: **quiet confidence / price-first / evidence-backed**.

The detail screen prioritizes:

`exact identity -> recent price -> personal-history judgment/reason -> previous/usual context -> purchase trend -> receipt-traceable history`

Key frozen behavior:

- STANDARD only;
- exact `STANDARD_PACKAGE` comparison basis;
- no UI-side identity inference or CP28 threshold reimplementation;
- structured brand/product/variant/specification when canonical V2 data exists;
- legacy STANDARD canonical-name fallback;
- actual eligible purchase points only in the chart;
- latest point emphasized;
- usual-price reference only for evaluated histories;
- >=64dp history rows opening existing Receipt Detail;
- excluded observations remain provenance but not chart/evaluation inputs;
- compact/medium single-column;
- expanded two-pane only when width >=840dp and height >=480dp;
- chart Korean accessibility summary and nonlinear font-scaling-safe SP handling.

## Architecture / privacy

The app remains programmatic `Activity + android.widget`.

No Compose/Material migration, schema migration, duplicate price truth, network requirement or new identity authority was introduced.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## CP31 metric

`CP31_METRICS product_detail_version=1 standard_basis=1 identity_fallbacks=1 price_states=8 responsive_cases=6 traceability=1 chart_single_basis=1 purchase_rows=4`

CI evidence does not include emulator/device screenshot comparison or real-user visual usability validation.

## Next planned checkpoint

**CP32 — Commodity Detail**

CP32 must present NON_STANDARD history without confusing commodity grouping with price comparability. Strict kg/L/each cohorts remain separate; package-form SAME_FORM/LIKE_FORM history remains contextual unless genuinely comparable.

Do not start CP32 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
