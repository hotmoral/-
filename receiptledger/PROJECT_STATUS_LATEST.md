# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP35 — Real Receipt Evaluation — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-real-receipt-evaluation-20261016`
- predecessor CP34 handoff: `386c1b3d9ef7f3737ffd8b4d0f34fe2e076cab8e`
- frozen CP35 executable/evaluation HEAD: `6ae9fbcfe0abc17dd9471de243170a9a87272767`
- canonical Actions run: `38884870134` — SUCCESS
- job: `116920055654` — SUCCESS
- artifact ID: `12038973171`
- artifact digest: `sha256:3336486a5807fa971e8385cdd10008f29cb85daf1779ab5fd226008d9ad72258`
- debug APK SHA-256: `3e89e7ab1358278889c55410fc49f4b5e4e50f54c8a490aeb473dd58c0cab9cf`
- version: `1.0.33-real-receipt-evaluation` / versionCode 34
- lint: 0 errors / 0 warnings (`No issues found.`)

Any later handoff/status synchronization must remain documentation-only. The executable/evidence boundary remains `6ae9fbcf...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Current loop:

`홈 -> 영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 반복 구매 재사용 -> 검색/카테고리 -> 제품/품목 가격기억 -> 영수증 근거`

Receipts are input/evidence; trustworthy product/commodity price memory is the product outcome.

## 3. CP35 evaluation result

CP35 remained evaluation-only and exercised the frozen system with public-safe synthetic receipt fixtures from `OcrDocument` token/geometry input through:

- production recognition/layout/structure;
- ReceiptRecord construction;
- CP33 review decision;
- identity confirmation / exact-alias reuse;
- CP27 comparison eligibility and normalization;
- CP28 contextual safety;
- CP31/32 detail projections;
- exact receipt provenance.

Canonical metric:

`CP35_METRICS evaluation_version=1 fixtures=8 receipts=9 items=11 structured_correct=9 auto_confirmed=8 review_required=1 final_safe_registrations=7 exact_alias_reuse=2 conservative_unresolved=1 false_auto_links=0 strict_weight_observations=2 contextual_cohorts=2 discount_exclusions=1 invalid_exclusions=1 detail_trace_rows=7 schema_unchanged=1`

## 4. Important findings

- false automatic identity links: 0;
- exact confirmed alias reuse worked on later matching receipts;
- similar `서울우유900mL` did not inherit confirmed `서울우유1L` identity;
- kg/g potato purchases normalized only into WEIGHT_KG;
- 봉/상자 stayed separate contextual cohorts with no CP28 judgment;
- multi-item receipt-level discount was excluded rather than guessed onto an item;
- mismatch receipt remained REVIEW_REQUIRED and excluded from eligible price history;
- CP31/32 purchase rows retained exact source receipt IDs.

No production Java correction was required.

## 5. Frozen contracts

Unchanged:

- stable catalog ID identity authority;
- CP21–29 domain/search semantics;
- CP27 comparison eligibility;
- CP28 thresholds;
- CP30 design system;
- CP31/32 detail semantics;
- CP33 capture/review/save/provenance;
- CP34 commercial shell;
- OCR/recovery/item/validation production code;
- product schema 2 / receipt schema 1;
- direct SQLite posture;
- programmatic `Activity + android.widget` architecture;
- offline/no-network/no-broad-permission posture.

CP35 changed no production Java, manifest or production resource file.

## 6. Regression evidence

Canonical artifact confirms:

- CP35 1/1 PASS;
- CP34 7/7 PASS;
- CP33 13/13 PASS;
- CP32 11/11 PASS;
- CP31 9/9 PASS;
- CP29 8/8 PASS;
- full Gradle unit suite/build PASS;
- lint `No issues found.`;
- forbidden camera/media/storage/network permissions absent.

## 7. Evidence limitation

Despite the roadmap name **Real Receipt Evaluation**, the public canonical corpus is deliberately synthetic/public-safe.

Fixtures start at synthetic `OcrDocument` token/geometry input. Therefore CP35 does not measure:

- ML Kit image-to-text character accuracy;
- camera/image variability;
- statistical merchant/font coverage;
- physical-device usability;
- performance/scale/reliability.

Do not reinterpret CP35 evidence as those measurements.

## 8. Completed product checkpoint chain

CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> CP29 Search / Browse -> CP30 Design System Foundation -> CP31 Product Detail -> CP32 Commodity Detail -> CP33 Capture / Review UX V2 -> CP34 Commercial UI Shell -> **CP35 Real Receipt Evaluation**.

## 9. Next planned checkpoint

**CP36 — Performance / Reliability — NOT STARTED**

Expected boundary:

- startup and OCR latency/memory;
- representative large catalog/history workloads;
- CP29 search scan measurement around 1k/10k before any FTS/index/cache decision;
- price/evaluation/detail/chart workloads;
- migrations;
- archive reconciliation and recovery;
- deterministic reliability/failure handling.

CP36 must not be started without explicit user authorization.

## 10. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP35_REAL_RECEIPT_EVALUATION_CLOSEOUT.md`
4. `receiptledger/CP35_REAL_RECEIPT_EVALUATION_EVIDENCE.md`
5. `receiptledger/CP35_REAL_RECEIPT_EVALUATION_PLAN.md`
6. `receiptledger/REAL_RECEIPT_EVALUATION_CONSISTENCY_REVIEW.md`
7. `receiptledger/REAL_RECEIPT_EVALUATION_FIXTURES_V1.md`
8. `receiptledger/CP34_COMMERCIAL_UI_SHELL_CLOSEOUT.md`
9. `receiptledger/CP34_COMMERCIAL_UI_SHELL_EVIDENCE.md`
10. `receiptledger/CP33_CAPTURE_REVIEW_UX_V2_CLOSEOUT.md`
11. `receiptledger/CP32_COMMODITY_DETAIL_CLOSEOUT.md`
12. `receiptledger/CP31_PRODUCT_DETAIL_CLOSEOUT.md`
13. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
14. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
15. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
16. `receiptledger/README.md`
17. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify live handoff HEAD and frozen executable HEAD separately.

## 11. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately reauthorized.

**Current stop condition: CP35 complete. Await explicit authorization for CP36.**
