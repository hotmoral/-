# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
4. `CP30_DESIGN_SYSTEM_FOUNDATION_EVIDENCE.md`
5. `CP30_DESIGN_SYSTEM_FOUNDATION_PLAN.md`
6. `DESIGN_SYSTEM_FOUNDATION_CONSISTENCY_REVIEW.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP30 — Design System Foundation — COMPLETE**

- branch `receiptledger/run-v1-design-system-foundation-20261016`
- frozen implementation HEAD `ff0745db529499171246866039521a0b83e830e4`
- canonical Actions `38842905325` — SUCCESS
- job `116786812761` — SUCCESS
- artifact ID `12022330459`
- artifact digest `sha256:f1bcb1b2d58e328b15cf4811dd1dc107888cc2f5ba733ce1bb1ee60bf8ec0e5e`
- APK SHA-256 `cb35afb3ee0bf00dafad48f0b33733401661a982df11557bb01f716ca6655373`
- CP30 tests 9/9 PASS
- CP29 8/8, CP28 8/8, CP27 8/8, legacy price 2/2, CP26 8/8, CP25 8/8, CP24 8/8, CP23 7/7, CP21 15/15, CP22 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.28-design-system-foundation`, versionCode 29

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable judgment -> find/browse -> inspect`

CP30 freezes how later commercial screens present that truth. It does not change identity, price, search or persistence semantics.

## CP30 foundation

- 6 purpose-based typography roles;
- 8 semantic tones with text + color, never color alone;
- spacing 4/8/12/16/24/32dp;
- radii 8/12/16dp;
- card/floating elevation 1/3dp;
- minimum touch target 48dp;
- 10 stable icon roles with Korean accessibility labels;
- compact/medium/expanded width classes at 600/840dp;
- chart series forbidden from mixing comparison bases;
- 8 reusable loading/empty/review/error/unavailable state presentations;
- existing programmatic `android.widget` architecture preserved;
- no Compose/Material migration.

Only LibraryActivity and legacy PriceHistoryActivity are representative UiKit adopters in CP30. Full commercial screens begin later.

## CP30 local contract metric

`CP30_METRICS typography_roles=6 semantic_tones=8 price_presentations=8 validation_presentations=4 ui_states=8 contrast_pairs=9 responsive_cases=5 chart_cross_basis_rejections=1 min_touch_dp=48 icon_roles=10 elevation_tokens=2 representative_activities=2`

Synthetic/local foundation evidence only.

## Next planned checkpoint

**CP31 — Product Detail**

It will build the STANDARD-product price-memory detail experience using frozen identity/specification, CP27 price facts, CP28 judgment, CP29 discovery/read models and CP30 visual/interaction grammar.

Do not start CP31 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
