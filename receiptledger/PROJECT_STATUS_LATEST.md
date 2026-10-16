# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP32 — Commodity Detail — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-commodity-detail-20261016`
- predecessor CP31 handoff: `1025f3d4f319ae6924bcf5012797b879757434fe`
- frozen CP32 implementation HEAD: `e42629ccd66a80a4a1a14de0c7798b178d6b0062`
- canonical Actions run: `38855942283` — SUCCESS
- job: `116827303606` — SUCCESS
- artifact ID: `12027322130`
- artifact digest: `sha256:ce1ae60e5a9e5295359f433a85417b2efc5a39bca95b29b2480e82e7154f4a9b`
- debug APK SHA-256: `320379024800e5c0ee441656ea8d28bef20ac2ee0377332190b770645c8606d2`
- CP32 11/11, CP31 9/9, CP30 9/9, CP29 8/8, CP28 8/8, CP27 8/8, CP26 8/8 PASS in packaged XML evidence
- lint: 0 errors / 0 warnings (`No issues found.`)
- version: `1.0.30-commodity-detail` / versionCode 31

Any later handoff/status commit must remain documentation-only. Executable/evidence boundary remains `e42629cc...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> explainable judgment -> find/browse -> inspect`

CP31 provides STANDARD Product Detail. CP32 now provides the corresponding NON_STANDARD commodity detail without weakening comparison safety.

## 3. CP32 Commodity Detail

Commercial direction remains:

**quiet confidence / price-first / evidence-backed**

NON_STANDARD addition:

**clarity before apparent simplicity**

Compact hierarchy:

`commodity identity -> real latest purchase -> strict comparable prices -> contextual package-form references -> receipt-traceable purchase history`

Critical behavior:

- same commodity grouping does not mean one price basis;
- WEIGHT_KG / VOLUME_L / EACH remain independent;
- each strict basis gets its own latest/previous/usual/CP28 judgment/chart;
- LIKE_FORM stays reference-only and unjudged;
- no fake conversion such as bag = kg;
- newest real purchase is not replaced by an older strict-comparable observation;
- excluded observations remain visible provenance but never enter chart/judgment values.

## 4. UI / accessibility / responsive result

CP32 consumes the CP30 design system and CP31 commercial composition bar:

- purpose-based typography and semantic text+color;
- explicit basis/unit copy adjacent to normalized prices;
- strict chart series are single-basis actual purchases only;
- usual-price reference and judgment color only when CP28 is EVALUATED;
- contextual package forms use INFO/reference presentation and no chart;
- purchase rows are >=64dp and open Receipt Detail;
- charts expose Korean accessibility summaries;
- custom chart SP conversion supports nonlinear font scaling;
- compact/medium remain single-column;
- two-pane only expanded + height >=480dp.

## 5. Architecture / safety boundary

Unchanged:

- `Activity + android.widget` architecture;
- no Compose/AppCompat/Material migration;
- no custom/downloadable font;
- product schema 2 / receipt schema 1;
- CP21–31 domain/search/price/detail contracts;
- Main capture/OCR flow;
- Product Detail behavior;
- Receipt Detail/Review behavior;
- offline/privacy posture;
- forbidden CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE permissions remain absent.

No duplicate mutable price truth/cache/index/conversion table was introduced.

## 6. Canonical metric

`CP32_METRICS commodity_detail_version=1 strict_basis_kinds=3 contextual_policy=1 grouping_not_comparability=1 responsive_cases=6 traceability=1 chart_single_basis=1 strict_sections=2 contextual_sections=2 purchase_rows=9`

## 7. Pre-closeout discipline

CP32 was not closed on the first build or first green run.

- run `38855330418` exposed one invalid CP30 spacing-token reference;
- run `38855551821` became functionally green, but closeout review found two Android `SetTextI18n` warnings;
- final HEAD `e42629cc...` moved the text composition into string resources and strengthened CI to require `No issues found.`;
- canonical run `38855942283` passed the complete gate.

## 8. Known limitations

- CP33 Capture/Review UX V2 not started;
- CP34 commercial home/navigation shell not started;
- current launcher remains the existing OCR-development entry until CP34;
- final icon artwork/library and dark-theme finalization remain open;
- no emulator/device screenshot or real-user usability evidence is included in CP32 CI.

## 9. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> CP29 Search / Browse -> CP30 Design System Foundation -> CP31 Product Detail -> **CP32 Commodity Detail**.

## 10. Next planned checkpoint

**CP33 — Capture / Review UX V2**.

Goal: move the front half of the product toward:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

Expected emphasis:

- reduce review burden without bypassing identity/provenance safety;
- clearly separate auto-confirmed versus review-required fields/items;
- preserve raw receipt evidence and correction traceability;
- keep permissions/offline model unchanged unless separately authorized;
- do not prematurely build the CP34 commercial shell.

Do not begin CP33 without explicit user authorization.

## 11. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP32_COMMODITY_DETAIL_CLOSEOUT.md`
4. `receiptledger/CP32_COMMODITY_DETAIL_EVIDENCE.md`
5. `receiptledger/CP32_COMMODITY_DETAIL_PLAN.md`
6. `receiptledger/COMMODITY_DETAIL_CONSISTENCY_REVIEW.md`
7. `receiptledger/COMMODITY_DETAIL_GOLDEN_VECTORS.md`
8. `receiptledger/CP31_PRODUCT_DETAIL_CLOSEOUT.md`
9. `receiptledger/CP31_PRODUCT_DETAIL_EVIDENCE.md`
10. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
11. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
12. `receiptledger/README.md`
13. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify current handoff HEAD and frozen executable boundary separately before future work.

## 12. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

**Current stop condition: CP32 is complete. Await explicit authorization for CP33.**
