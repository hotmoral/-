# ReceiptLedger — Product / Validation Roadmap

Updated: 2026-10-17 KST

## 0. Governing objective

ReceiptLedger is a personal purchase-price memory and comparison system. Receipts are input/evidence; the product outcome is trustworthy, receipt-traceable product/commodity price memory.

Checkpoint work must preserve authority boundaries, catch material contradictions early, avoid speculative scope and freeze exact evidence before advancing.

## 1. Completed V1 chain

The planned V1 chain CP20–CP36 is complete.

CP36 frozen executable: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
CP36 docs-only handoff: `d0a3a9ec7658808c82247715d58ac106a3778186`

CP36 corrected only the measured SQLite search bottleneck. Warm OCR on the CI emulator remained an accepted V1 risk because real-device latency and real-image accuracy were unknown.

## 2. CP37 — Physical Device / Real-Image OCR Validation — IN PROGRESS

### Phase A — validation instrumentation — COMPLETE

- frozen executable: `9bb5dcc276fae4632ade5ac3134e586baad65235`
- docs-only handoff: `6b7d7b9b65432701b43da53a0e6f0ff1e47a1449`
- canonical run: `38950400666` SUCCESS

Phase A added privacy-safe debug instrumentation only.

### Phase B first physical sample — DEFECT FOUND

The first physical sample was conservatively REVIEW_REQUIRED and had `false_auto_confirm=0`, but user inspection found a spatially separate address/header row emitted as a product item. The existing review UI could not remove such a row.

This triggered bounded Remediation A before continuing the campaign.

### Remediation A — READY_FOR_PHYSICAL_RETEST

- branch: `receiptledger/run-post-v1-physical-ocr-remediation-20261017`
- frozen executable: `06fafa9db1da0e4592ddc15a468a9c6e4e338515`
- canonical run: `38957744298` SUCCESS
- artifact: `12071212297`
- APK SHA-256: `109b61603c9f4a0a399ecb919399151427ab3ba243e626bbe8543340a4ee0f3d`
- version: `1.0.36-physical-ocr-remediation` / 37

Remediation A adds only:

1. a conservative pre-date false-item gate when a real multi-item body is present below;
2. explicit `상품이 아님` row removal during review;
3. provenance/report support for that removal;
4. side-by-side debug packaging for safe retest.

It does not change OCR/recovery/identity/price/schema behavior.

## 3. Current decision gate

Do **not** resume the broad CP37 sample campaign yet.

First rerun the same receipt on the frozen remediation APK.

If the original false row no longer appears and no new blocker is observed, resume Phase B collection. If the row remains, use explicit removal and analyze the new evidence before broadening any structure rule.

## 4. CP37 decision priority

1. correctness and false-auto-confirm safety;
2. saved-data/provenance reliability;
3. ability to recover from structural false positives;
4. review burden;
5. latency.

A latency improvement never justifies reduced recognition correctness.

## 5. Frozen authority gates

Still authoritative:

- stable catalog ID is final product identity authority;
- category/search/price/UI relevance cannot create identity;
- commodity grouping != comparability;
- strict kg/L/each bases remain separate from contextual package forms;
- CP27 defines eligible price evidence;
- CP28 owns judgment thresholds;
- review convenience cannot erase provenance;
- product schema 2 / receipt schema 1 remain frozen;
- no network/broad media/storage permission posture remains frozen.

## 6. Post-retest rule

Do not invent a broader OCR or structure checkpoint until the same-receipt remediation retest is analyzed.

If Remediation A succeeds, resume the original minimum 10-receipt campaign target. If further false-item patterns appear, define the smallest evidence-backed extension rather than a general-purpose address/product classifier.

## 7. Handoff discipline

At every boundary:

1. recover canonical refs;
2. inspect predecessor consistency and material risks;
3. implement only the smallest coherent scope;
4. run regression/evidence;
5. perform post-green plan/code/evidence review;
6. freeze executable HEAD;
7. synchronize docs-only handoff;
8. stop before unrelated work.

## 8. Current boundary

**CP37 Remediation A is READY_FOR_PHYSICAL_RETEST. CP37 is not complete. Next task is the same-receipt physical retest, not additional coding.**
