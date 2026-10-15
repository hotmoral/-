# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP23_RECEIPT_PRODUCT_SEMANTICS_CLOSEOUT.md`
4. `CP23_RECEIPT_PRODUCT_SEMANTICS_EVIDENCE.md`
5. `CP23_RECEIPT_PRODUCT_SEMANTICS_PLAN.md`
6. `RECEIPT_PRODUCT_SEMANTICS_CONSISTENCY_REVIEW.md`
7. `PRODUCT_REBASELINE_V1_ROADMAP.md`
8. `WORK_UNIT.md`

GitHub is canonical; verify refs before relying on old chat context.

## Current boundary

**CP23 — Receipt Product Semantics — COMPLETE**

- branch `receiptledger/run-v1-receipt-product-semantics-20261016`
- frozen implementation HEAD `5bffb66bd43814f8d638791b5697f79ff089028b`
- canonical Actions `38822100885` — SUCCESS
- artifact ID `12013477721`
- artifact digest `sha256:fa22d082545adae7c414b0f1c089604174341f7e879c1acd5e4677e1dc2b7195`
- APK SHA-256 `e4e64f85f9700089b32f9f0b8121eef0a2f565d09b5428599d3717296c1b8324`
- semantic parser tests 7/7 PASS
- upstream catalog tests 15/15 PASS
- upstream persistence tests 7/7 PASS
- lint 0 errors / 0 warnings
- version `1.0.21-receipt-product-semantics`, versionCode 22

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

CP23 converts receipt item text into conservative semantic evidence only. It does not decide catalog identity.

Key current rules:

- parsed semantics remain unconfirmed evidence;
- unknown brand is not guessed merely from first-token position;
- free-form variant is not guessed;
- standalone kg/g/L/mL is ambiguous between package specification and purchase form and therefore review-gated;
- explicit pack forms and multipack syntax are parsed when defensible;
- stable catalog ID remains the only identity authority;
- false merge and false split are both downstream quality risks;
- no fake cross-unit comparison;
- price truth stays receipt-derived.

## CP23 local quality

- field precision 96.9696%
- field recall 94.1176%
- ambiguity review-gating 10/10
- no-invention negatives 2/2
- review-required 13 / semantic-ready 13 across 26 synthetic fixtures

These are parser fixture metrics, not final real-receipt accuracy.

## Next planned checkpoint

**CP24 — Identity Resolver V2**

CP24 must define merchant-aware/confirmed alias authority and measure false merge, false split, automatic-link success, review burden, incorrect automatic decisions and repeat-confirmation reuse.

Do not start CP24 until explicitly authorized.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared private assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
