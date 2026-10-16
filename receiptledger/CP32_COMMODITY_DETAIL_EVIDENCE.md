# ReceiptLedger V1 — CP32 Commodity Detail Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_COMMODITY_DETAIL_01`

## 1. Canonical refs

- predecessor handoff: `1025f3d4f319ae6924bcf5012797b879757434fe`
- frozen implementation HEAD: `e42629ccd66a80a4a1a14de0c7798b178d6b0062`
- branch: `receiptledger/run-v1-commodity-detail-20261016`

## 2. Canonical CI

- workflow: `ReceiptLedger V1 Commodity Detail`
- run: `38855942283`
- job: `116827303606`
- conclusion: SUCCESS

Passed stages:

1. Android/JDK/Gradle setup;
2. public namespace audit;
3. CP32 scope and frozen-contract enforcement;
4. full unit-test run + Android lint + debug build;
5. CP32 deterministic metric extraction;
6. permission/evidence packaging;
7. artifact upload.

## 3. Artifact identity

- artifact ID: `12027322130`
- artifact name: `receiptledger-v1-commodity-detail-38855942283`
- artifact digest: `sha256:ce1ae60e5a9e5295359f433a85417b2efc5a39bca95b29b2480e82e7154f4a9b`
- APK file: `receiptledger-v1-commodity-detail-debug.apk`
- APK SHA-256: `320379024800e5c0ee441656ea8d28bef20ac2ee0377332190b770645c8606d2`
- signing: debug only

Artifact inspection reproduced the APK SHA above from the downloaded evidence ZIP.

## 4. Build identity

Packaged evidence records:

- `checkpoint=RL_V1_COMMODITY_DETAIL_01`
- `public_commit=e42629ccd66a80a4a1a14de0c7798b178d6b0062`
- `predecessor_handoff=1025f3d4f319ae6924bcf5012797b879757434fe`
- `product_schema=2_UNCHANGED`
- `receipt_schema=1_UNCHANGED`
- `detail_scope=NON_STANDARD_ONLY`
- `strict_bases=WEIGHT_KG,VOLUME_L,EACH`
- `contextual_like_form=REFERENCE_ONLY`
- `fake_conversion=FORBIDDEN`
- `receipt_traceability=PRESERVED`
- `ui_architecture=PROGRAMMATIC_ANDROID_WIDGET_PRESERVED`
- `compose_migration=NONE`
- `material_dependency_added=NO`
- `compile_sdk=36`
- `target_sdk=36`
- `min_sdk=23`
- `version_name=1.0.30-commodity-detail`
- `version_code=31`

## 5. CP32 test evidence

`COMMODITY_DETAIL_V1_TEST.xml`:

- tests: 11
- failures: 0
- errors: 0
- skipped: 0

Covered material boundaries include:

- strict versus contextual cohort partition;
- WEIGHT_KG CP28 evaluation reuse;
- multiple strict bases remaining separate;
- real latest purchase remaining distinct from latest strict observation;
- BAG/BOX contextual cohorts remaining separate and unjudged;
- contextual-only commodity producing no fake strict price;
- Korean purchase-form/rate formatting;
- single-basis chart contract;
- receipt traceability;
- CP30 responsive policy;
- deterministic metric.

## 6. Packaged regression evidence

Downloaded artifact XMLs:

- CP32 Commodity Detail: 11/11 PASS
- CP31 Product Detail: 9/9 PASS
- CP30 Design System Foundation: 9/9 PASS
- CP29 Search/Browse: 8/8 PASS
- CP28 Price Evaluation: 8/8 PASS
- CP27 Price Intelligence V2: 8/8 PASS
- CP26 Commodity/Non-standard V2: 8/8 PASS

Every packaged XML above has:

- failures = 0;
- errors = 0;
- skipped = 0.

The workflow additionally requires the full unit-test run and checks the prior CP25/24/23/21/22 and legacy Price History result files before success.

## 7. Lint/build evidence

Canonical log:

- `BUILD SUCCESSFUL`
- 49 actionable Gradle tasks executed
- lint report exactly: `No issues found.`

The CP32 workflow explicitly fails if lint contains anything other than that clean result.

## 8. Permission evidence

Packaged permission dump contains only:

- `com.receiptledger.v1.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

Absent as required:

- CAMERA;
- READ_MEDIA_IMAGES;
- READ_EXTERNAL_STORAGE;
- WRITE_EXTERNAL_STORAGE;
- MANAGE_EXTERNAL_STORAGE;
- INTERNET;
- ACCESS_NETWORK_STATE.

## 9. Scope evidence

Final predecessor-to-implementation diff contains only:

- CP32 plan/consistency/golden documents;
- CP32 ReceiptLedger-prefixed workflow;
- version update;
- one manifest Activity registration;
- Commodity Detail Activity/read model/service/formatter/chart/test;
- Korean strings;
- minimal NON_STANDARD routing in legacy Price History.

Frozen upstream packages are unchanged:

`catalog / product / semantics / identity / category / commodity / persistence / price / priceintel / priceeval / search / detail / design`

Also unchanged:

- `MainActivity`;
- `ProductDetailActivity`;
- `ReceiptDetailActivity`;
- `ReceiptReviewDialog`.

CP34 shell work was not started.

## 10. Canonical metric

`CP32_METRICS commodity_detail_version=1 strict_basis_kinds=3 contextual_policy=1 grouping_not_comparability=1 responsive_cases=6 traceability=1 chart_single_basis=1 strict_sections=2 contextual_sections=2 purchase_rows=9`

## 11. Evidence limitation

This checkpoint proves deterministic domain-to-presentation behavior, build/lint quality, packaged permissions and regression safety.

It does **not** prove pixel-perfect rendering on the user's device, screenshot parity across all Android configurations, or real-user usability. No emulator/device screenshot campaign is part of CP32 evidence.