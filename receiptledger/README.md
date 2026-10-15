# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
4. `CATALOG_DOMAIN_V2_PLAN.md`
5. `CATALOG_DOMAIN_V2_CONSISTENCY_REVIEW.md`
6. `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `README.md`
9. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP21 — Catalog Domain V2 — COMPLETE**

- frozen implementation HEAD `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical implementation Actions `38808985222` — SUCCESS
- artifact ID `12008555521`
- artifact digest `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- APK SHA-256 `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- tests 15/15 PASS
- lint 0 errors / 0 warnings
- version `1.0.19-catalog-domain-v2`, versionCode 20

Client-requirement alignment amendment:
`60f40f1eba0792bbcb5a3c08aa6724b4010297bd`

CI scope/trigger maintenance:
`94de4de3bef32e0165fd33810c9460ff6356b243`

Verification run:
`38812273375` — SUCCESS.

Runs `38811970256` and `38812118401` were stale-scope guard failures on the new docs before tests/build and are not app regressions.

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

Current governing additions:

- measure false split as well as false merge;
- repeated confirmed products should reduce review burden;
- define the canonical comparison-price basis before price statistics;
- prevent fake cross-unit comparison;
- establish Design System before final commercial detail screens.

## Revised roadmap

Next: **CP22 — Persistence V2**.

Then:

CP23 Receipt Product Semantics
-> CP24 Identity Resolver V2
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

## CI efficiency rule

CP21 automatic workflow triggers are now limited to CP21 code/test/audit/workflow paths. Normal handoff/status markdown edits no longer trigger a full Android build. Manual dispatch remains available for explicit validation.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared private assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.

## Stop condition

**CP21 and the client-alignment amendment are complete. Do not begin CP22 until explicitly authorized.**
