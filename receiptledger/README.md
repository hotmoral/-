# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, persistence migrations, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP22_PERSISTENCE_V2_CLOSEOUT.md`
4. `CP22_PERSISTENCE_V2_EVIDENCE.md`
5. `PERSISTENCE_V2_PLAN.md`
6. `PERSISTENCE_V2_CONSISTENCY_REVIEW.md`
7. `PERSISTENCE_V2_GOLDEN_VECTORS.md`
8. `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
9. `CATALOG_DOMAIN_V2_PLAN.md`
10. `PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `README.md`
12. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP22 — Persistence V2 — COMPLETE**

- branch `receiptledger/run-v1-persistence-v2-20261016`
- frozen implementation HEAD `449896c7580fb3412f41c9b58d1ab9412d13d84d`
- canonical Actions `38816200340` — SUCCESS
- artifact ID `12010832560`
- artifact digest `sha256:6b27c9e8aa9541346d9a3f5844c12a2f0dacd26841e869bd5b4834d7cb67bea1`
- APK SHA-256 `1cddd2f19c70b8ab883a97630c3dbc10e8971d75a3c9e4ec62be72eb69328884`
- migration vectors 15/15 PASS
- CP21 domain tests 15/15 PASS
- CP22 persistence tests 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.20-persistence-v2`, versionCode 21

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

## Persistence state

Product catalog DB:

- file stays `receipt-products-v1.db`;
- schema is V2;
- legacy product IDs and item links survive migration;
- legacy aliases become GLOBAL contextual aliases;
- merchant alias context, semantic catalog fields, specification, category reference and linked purchase-form metadata can now be persisted.

Receipt DB:

- remains `receiptledger-v1.db` schema V1;
- price/date/store/validation evidence remains authoritative there;
- CP22 does not create a duplicate price truth.

Direct SQLite / SQLiteOpenHelper remains in use. Room was evaluated and deferred to avoid combining framework migration with data migration without evidence that it is needed.

## Governing client-alignment requirements

- measure false split as well as false merge in CP24;
- repeated confirmed products should reduce review burden;
- CP23–CP26 measure local automation/review quality rather than waiting for CP35;
- CP27 defines the canonical comparison-price basis before price statistics;
- prevent fake cross-unit comparison;
- CP30 Design System Foundation precedes final commercial detail screens.

## Roadmap

Next planned checkpoint:
**CP23 — Receipt Product Semantics**.

Then:

CP24 Identity Resolver V2
-> CP25 Category System
-> CP26 Commodity / Non-standard V2
-> CP27 Price Intelligence V2
-> CP28 Price Evaluation
-> CP29 Search / Browse
-> CP30 Design System Foundation
-> CP31 Product Detail
-> CP32 Commodity Detail
-> CP33 Capture / Review UX V2
-> CP34 Commercial UI Shell
-> CP35 Real Receipt Evaluation
-> CP36 Performance / Reliability.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real personal purchase databases/backups, personal identifiers or uncleared private assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.

## Stop condition

**CP22 is complete. Do not begin CP23 until explicitly authorized.**
