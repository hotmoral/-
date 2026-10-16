# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP32_COMMODITY_DETAIL_CLOSEOUT.md`
4. `CP32_COMMODITY_DETAIL_EVIDENCE.md`
5. `CP32_COMMODITY_DETAIL_PLAN.md`
6. `COMMODITY_DETAIL_CONSISTENCY_REVIEW.md`
7. `COMMODITY_DETAIL_GOLDEN_VECTORS.md`
8. `CP31_PRODUCT_DETAIL_CLOSEOUT.md`
9. `CP31_PRODUCT_DETAIL_EVIDENCE.md`
10. `PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `WORK_UNIT.md`

GitHub is canonical; verify current handoff ref and frozen executable ref separately before relying on old chat context.

## Current boundary

**CP32 — Commodity Detail — COMPLETE**

- branch `receiptledger/run-v1-commodity-detail-20261016`
- predecessor CP31 handoff `1025f3d4f319ae6924bcf5012797b879757434fe`
- frozen implementation HEAD `e42629ccd66a80a4a1a14de0c7798b178d6b0062`
- canonical Actions `38855942283` — SUCCESS
- job `116827303606` — SUCCESS
- artifact ID `12027322130`
- artifact digest `sha256:ce1ae60e5a9e5295359f433a85417b2efc5a39bca95b29b2480e82e7154f4a9b`
- APK SHA-256 `320379024800e5c0ee441656ea8d28bef20ac2ee0377332190b770645c8606d2`
- CP32 11/11, CP31 9/9, CP30 9/9, CP29 8/8, CP28 8/8, CP27 8/8, CP26 8/8 PASS in packaged evidence
- lint `No issues found.`
- version `1.0.30-commodity-detail`, versionCode 31

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable judgment -> find/browse -> inspect`

CP31 supplies STANDARD Product Detail; CP32 supplies NON_STANDARD Commodity Detail.

## CP32 Commodity Detail

Design direction remains **quiet confidence / price-first / evidence-backed**, with **clarity before apparent simplicity** for non-standard purchases.

Key frozen behavior:

- real latest purchase is shown even when not directly comparable;
- kg/g -> independent 원/kg history;
- L/mL -> independent 원/L history;
- exact count -> independent 원/개 history;
- each strict basis owns its own latest/previous/usual/CP28 judgment and chart;
- package-form LIKE_FORM histories remain independent reference-only groups;
- contextual histories have no cheap/expensive judgment and no line chart;
- no fake conversion such as 봉=kg;
- excluded purchases remain receipt-traceable evidence but not comparison inputs;
- receipt-history rows open existing Receipt Detail.

## Architecture / privacy

The app remains programmatic `Activity + android.widget`.

No Compose/Material migration, schema migration, duplicate price truth, new conversion table, network requirement or new identity authority was introduced.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

Full launcher/home/navigation integration remains intentionally deferred to CP34; MainActivity is unchanged by CP32.

## CP32 metric

`CP32_METRICS commodity_detail_version=1 strict_basis_kinds=3 contextual_policy=1 grouping_not_comparability=1 responsive_cases=6 traceability=1 chart_single_basis=1 strict_sections=2 contextual_sections=2 purchase_rows=9`

CI evidence does not include emulator/device screenshot comparison or real-user visual usability validation.

## Next planned checkpoint

**CP33 — Capture / Review UX V2**

Target: reduce the path to `영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장` while preserving identity/provenance/validation safety.

Do not start CP33 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
