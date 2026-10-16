# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP26_COMMODITY_NONSTANDARD_V2_CLOSEOUT.md`
4. `CP26_COMMODITY_NONSTANDARD_V2_EVIDENCE.md`
5. `CP26_COMMODITY_NONSTANDARD_V2_PLAN.md`
6. `COMMODITY_NONSTANDARD_V2_CONSISTENCY_REVIEW.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP26 — Commodity / Non-standard V2 — COMPLETE**

- branch `receiptledger/run-v1-commodity-nonstandard-v2-20261016`
- frozen implementation HEAD `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`
- canonical Actions `38829423445` — SUCCESS
- job `116744485504` — SUCCESS
- artifact ID `12016292501`
- artifact digest `sha256:6ad4342d61274530aecc090fbe7caa8f606f3a20c113285e3b18cd86893336bd`
- APK SHA-256 `250d4d00bb93334fede3873c92e85b63d1ccd05ee5d09f9a4c7970fb366b90cb`
- commodity tests 8/8 PASS
- category tests 8/8 PASS
- identity tests 8/8 PASS
- semantics tests 7/7 PASS
- catalog tests 15/15 PASS
- persistence tests 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.24-commodity-nonstandard-v2`, versionCode 25

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

CP26 makes one commodity history span heterogeneous purchase forms while preserving every observation's original quantity/unit/form.

Key current rules:

- commodity grouping resolves only to existing NON_STANDARD stable IDs;
- confirmed MERCHANT alias -> confirmed GLOBAL alias -> exact commodity name -> REVIEW suggestion -> unresolved;
- `감자` must not silently match `감자칩` or `감자전분`;
- category and purchase form are not identity authority;
- modifier names remain review-only until confirmed;
- confirmation learns the narrowest useful alias scope for repeat use;
- raw quantity/unit/form and provenance remain observation-specific;
- exact physical/count conversions are distinguished from same-form-only and incomparable observations;
- **grouping != comparability**;
- no guessed 봉/팩/상자 conversion;
- price truth remains receipt-derived.

## CP26 local quality

`fixtures=25 known_commodity=21 auto_groups=18 correct_auto_groups=18 incorrect_auto_groups=0 false_group=0 review_suggestions=2 false_split=1 negative_fixtures=4 raw_form_cases=12 raw_form_preserved=12 repeat_cases=3 repeat_reused=3`

These are synthetic/local metrics, not final real-receipt accuracy.

## Next planned checkpoint

**CP27 — Price Intelligence V2**

It must first define a canonical receipt-traceable comparison price and eligibility rules, then compute deterministic personal-history statistics without turning incomparable NON_STANDARD forms into fake normalized prices.

Do not start CP27 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
