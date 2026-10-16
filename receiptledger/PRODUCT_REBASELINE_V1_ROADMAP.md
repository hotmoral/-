# ReceiptLedger — Product / Validation Roadmap

Updated: 2026-10-17 KST

## 0. Governing objective

ReceiptLedger is a personal purchase-price memory and comparison system. Receipts are input/evidence; the product outcome is trustworthy, receipt-traceable product/commodity price memory.

Checkpoint work must preserve authority boundaries, catch material contradictions early, avoid speculative scope and freeze exact evidence before advancing.

## 1. Completed V1 chain

The planned V1 chain is complete:

CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> CP29 Search / Browse -> CP30 Design System Foundation -> CP31 Product Detail -> CP32 Commodity Detail -> CP33 Capture / Review UX V2 -> CP34 Commercial UI Shell -> CP35 Real Receipt Evaluation -> CP36 Performance / Reliability.

### CP36 final boundary

- frozen executable: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- canonical run: `38926526457` SUCCESS
- docs-only handoff: `d0a3a9ec7658808c82247715d58ac106a3778186`

CP36 corrected only the measured SQLite search bottleneck. 10k search improved from 17,106ms to 1,524ms without FTS, persistent cache, new index or schema change. Warm OCR on the CI emulator remained an explicit accepted V1 risk because physical-device performance and real-image accuracy were not known.

## 2. Post-V1 validation

### CP37 — Physical Device / Real-Image OCR Validation — IN PROGRESS

Purpose: resolve the evidence gap left by CP35/36 before changing OCR.

#### Phase A — Device Validation Instrumentation — READY_FOR_DEVICE_EVIDENCE

- frozen executable: `9bb5dcc276fae4632ade5ac3134e586baad65235`
- canonical run: `38950400666` SUCCESS
- artifact ID: `12068811009`
- APK SHA-256: `f9e5b73db79043a6fc6f76f3381e0e2fdab164b7b53c59d8b9ce405d1147120f`
- version: `1.0.35-physical-ocr-validation` / 36

Phase A adds privacy-safe, debug-only instrumentation. It does not change OCR recognition, preprocessing, recovery, review, identity, price, schema or permission semantics.

#### Phase B — Physical Device Campaign — PENDING

Minimum decision target:

- 10 real saved receipt samples;
- >=3 CAMERA and >=3 GALLERY where practical;
- >=3 materially different layouts.

Every result must be visually checked even when AUTO_CONFIRMED. Only sanitized `RL_CP37_SAMPLE ...` lines are returned; real receipt data stays local.

Possible outcomes:

- PASS_NO_OCR_CHANGE;
- REMEDIATION_REQUIRED;
- INSUFFICIENT_EVIDENCE.

## 3. CP37 decision priority

Correctness and trust precede speed.

`false_auto_confirm=1` means an initially AUTO_CONFIRMED sample required a factual/structural correction before save. This is blocker-quality evidence and must be investigated before a PASS decision.

Latency evidence is interpreted together with correction burden. No downsampling/pass reduction/model change may be justified by latency alone.

## 4. Frozen authority gates

Still authoritative:

- stable catalog ID is final product identity authority;
- category/search/price/UI relevance cannot create identity;
- commodity grouping != comparability;
- strict kg/L/each bases stay separate from contextual package forms;
- CP27 defines eligible price evidence;
- CP28 owns judgment thresholds;
- review convenience cannot erase provenance;
- product schema 2 / receipt schema 1 remain frozen;
- no network/broad media/storage permission posture remains frozen.

## 5. Post-Phase-B rule

Do not invent a CP38 or OCR remediation group before Phase B analysis.

If Phase B proves a material defect, first define the smallest bounded remediation checkpoint with before/after evidence on the same physical corpus where practical. If Phase B passes without material defect, close CP37 with no OCR change.

## 6. Handoff discipline

At every boundary:

1. recover canonical refs;
2. inspect predecessor consistency and material risks;
3. implement only the smallest coherent scope;
4. run regression/evidence;
5. perform post-green plan/code/evidence review;
6. freeze executable HEAD;
7. synchronize docs-only handoff;
8. stop before unauthorized work.

## 7. Current boundary

**CP37 Phase A is READY_FOR_DEVICE_EVIDENCE. Phase B is next and requires user-supplied physical-device sanitized reports. CP37 is not yet complete.**
