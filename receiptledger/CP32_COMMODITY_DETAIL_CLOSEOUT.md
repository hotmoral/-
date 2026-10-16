# ReceiptLedger V1 — CP32 Commodity Detail Closeout

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_COMMODITY_DETAIL_01`
Status: **PASS / COMPLETE**

## 1. Frozen execution boundary

- branch: `receiptledger/run-v1-commodity-detail-20261016`
- predecessor CP31 handoff: `1025f3d4f319ae6924bcf5012797b879757434fe`
- frozen CP32 implementation HEAD: `e42629ccd66a80a4a1a14de0c7798b178d6b0062`
- canonical Actions run: `38855942283` — SUCCESS
- canonical job: `116827303606` — SUCCESS
- artifact ID: `12027322130`
- artifact digest: `sha256:ce1ae60e5a9e5295359f433a85417b2efc5a39bca95b29b2480e82e7154f4a9b`
- debug APK SHA-256: `320379024800e5c0ee441656ea8d28bef20ac2ee0377332190b770645c8606d2`
- versionName: `1.0.30-commodity-detail`
- versionCode: `31`

This HEAD is the executable/evidence boundary. Any later handoff synchronization must remain documentation-only.

## 2. Product result

CP32 completes the first commercial NON_STANDARD commodity detail surface while preserving the central rule:

**commodity grouping does not imply price comparability.**

The detail experience follows the existing commercial direction:

**quiet confidence / price-first / evidence-backed**

with an additional NON_STANDARD rule:

**clarity before apparent simplicity.**

Compact reading order:

`commodity identity -> real latest purchase -> strict comparable prices -> contextual package-form references -> receipt-traceable purchase history`

## 3. Frozen comparison behavior

Strict normalized bases remain independent:

- kg/g -> `WEIGHT_KG` -> 원/kg;
- L/mL -> `VOLUME_L` -> 원/L;
- exact count -> `EACH` -> 원/개.

Each strict basis has its own:

- latest normalized price;
- previous price;
- usual-price baseline;
- CP28 judgment/explanation;
- actual-purchase chart.

There is no commodity-wide merged usual price or combined chart.

Contextual package forms remain independent `LIKE_FORM` cohorts:

- 봉 / 팩 / 상자 / 단 / other preserved forms;
- same-form reference only;
- CP28 `CONTEXTUAL_ONLY`;
- no cheap/expensive judgment;
- no judgment color;
- no contextual line chart in CP32;
- never converted to kg/L/each without exact evidence.

## 4. Latest purchase versus latest comparable price

CP32 deliberately keeps these concepts separate.

The top `최근 구매` area shows the actual newest receipt-linked observation even when it is contextual or excluded from comparison.

A strict basis section separately shows the newest observation within that basis.

Therefore an older kg observation is never relabeled as the commodity's latest purchase merely because the newest purchase was `1봉`, `1상자` or otherwise non-comparable.

## 5. Read-only architecture

New CP32 projection/presentation layer:

- `CommodityDetailV1`
- `CommodityDetailServiceV1`
- `CommodityDetailFormatterV1`
- `CommodityPriceChartViewV1`
- `CommodityDetailActivity`

The service composes frozen CP26–28 facts only. It does not create a new price table, cache, alias, identity rule, conversion table or evaluation policy.

Existing `PriceHistoryActivity` received only the minimal route:

- STANDARD -> existing Product Detail;
- NON_STANDARD -> new Commodity Detail.

`MainActivity` remains unchanged. Full commercial navigation remains CP34 work.

## 6. Chart / accessibility / responsive behavior

Strict charts:

- accept strict cohorts only;
- call the frozen CP30 single-basis guard;
- plot eligible actual purchases only;
- display oldest -> newest;
- show usual-price reference only when CP28 is EVALUATED;
- use judgment color only when CP28 permits;
- expose Korean accessibility summary;
- reuse a preallocated `Path`;
- use Android SP conversion compatible with nonlinear font scaling.

History rows are >=64dp, preserve receipt ID/date/store/purchase form and open the existing Receipt Detail.

Responsive policy remains CP30:

- compact `<600dp` single-column;
- medium `600..839dp` single-column;
- expanded `>=840dp`;
- two-pane only when expanded and height >=480dp.

## 7. Frozen upstream contracts

Unchanged:

- stable catalog ID identity authority;
- product schema 2;
- receipt schema 1;
- CP23 semantic evidence authority;
- CP24 identity resolver authority;
- CP25 category non-authority;
- CP26 grouping/comparability semantics;
- CP27 basis derivation and discount eligibility;
- CP28 thresholds and judgments;
- CP29 search authority;
- CP30 design-system grammar;
- CP31 STANDARD Product Detail contract;
- Main capture/OCR flow;
- Receipt Detail behavior;
- Receipt Review behavior;
- offline/privacy/permission posture.

No fake conversion such as `1봉 = 1kg` was introduced.

## 8. Canonical deterministic metric

`CP32_METRICS commodity_detail_version=1 strict_basis_kinds=3 contextual_policy=1 grouping_not_comparability=1 responsive_cases=6 traceability=1 chart_single_basis=1 strict_sections=2 contextual_sections=2 purchase_rows=9`

The deterministic fixture intentionally contains multiple strict bases, multiple contextual forms and a newest excluded purchase to verify the dangerous boundaries rather than only the happy path.

## 9. Pre-closeout correction history

CP32 was not closed on the first build or first green run.

1. Initial implementation `095a25a68ba442ed9df9995c976cc309dfdf69c3` / run `38855330418` failed compile because one nonexistent CP30 spacing token was referenced.
2. `69b6c3d210479292ecaa0e9663571c47800a1c87` corrected the token; run `38855551821` became green.
3. Green review found two Android `SetTextI18n` warnings, so that green run was rejected for closure.
4. Final `e42629ccd66a80a4a1a14de0c7798b178d6b0062` moved those compositions to string resources and strengthened CI to require the lint report to be exactly `No issues found.`
5. Canonical run `38855942283` then passed the full CP32 gate.

This preserves the project rule that green CI is necessary but not sufficient when a cheap material quality gap remains.

## 10. Known limitations

- final Capture/Review UX V2 is not implemented; that is CP33;
- final commercial home/navigation shell is not implemented; that is CP34;
- launcher still exposes the existing OCR-development entry screen until shell work is authorized;
- final icon artwork/library and dark-theme finalization remain open;
- CP32 CI contains deterministic code/contract evidence, not emulator/device screenshot comparison or real-user visual-usability evidence.

## 11. Closure verdict

No material plan-to-code contradiction remains.

CP32 is **PASS / COMPLETE** at frozen implementation HEAD `e42629ccd66a80a4a1a14de0c7798b178d6b0062`.

Stop before CP33 until explicit user authorization.