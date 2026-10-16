# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading current files and verifying refs.

Read in order:

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

## 1. Latest executable checkpoint

**CP32 — Commodity Detail — PASS / COMPLETE**

- branch: `receiptledger/run-v1-commodity-detail-20261016`
- predecessor CP31 handoff: `1025f3d4f319ae6924bcf5012797b879757434fe`
- frozen implementation HEAD: `e42629ccd66a80a4a1a14de0c7798b178d6b0062`
- canonical Actions: `38855942283` — SUCCESS
- job: `116827303606` — SUCCESS
- artifact ID: `12027322130`
- artifact digest: `sha256:ce1ae60e5a9e5295359f433a85417b2efc5a39bca95b29b2480e82e7154f4a9b`
- APK SHA-256: `320379024800e5c0ee441656ea8d28bef20ac2ee0377332190b770645c8606d2`
- CP32 11/11, CP31 9/9, CP30 9/9, CP29 8/8, CP28 8/8, CP27 8/8, CP26 8/8 PASS in packaged XML evidence
- lint: 0 errors / 0 warnings (`No issues found.`)
- versionName `1.0.30-commodity-detail`, versionCode 31

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary from `e42629cc...`.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 검색/탐색 -> 제품/품목 상세 -> 과거 가격과 현재 가격 판단`

CP31 completes STANDARD Product Detail. CP32 completes NON_STANDARD Commodity Detail without treating every purchase form as directly comparable.

## 3. CP32 design direction

Commercial direction remains:

**quiet confidence / price-first / evidence-backed**

For non-standard goods, the additional rule is:

**clarity before apparent simplicity**

The screen must make it immediately clear that one commodity may have several independent price bases.

## 4. Frozen CP32 read model

`CommodityDetailServiceV1` is read-only.

It consumes:

- canonical NON_STANDARD product/commodity identity;
- CP27 observations and basis-specific cohorts;
- CP28 evaluation independently for each cohort;
- receipt provenance.

It returns:

- strict sections: WEIGHT_KG / VOLUME_L / EACH when present;
- contextual sections: independent LIKE_FORM cohorts;
- all newest-first purchase observations, including excluded rows;
- the real newest purchase independently of strict comparability.

It does not persist new price truth, conversion tables, caches, aliases or judgments.

## 5. Comparison safety

Strict bases:

- kg/g -> 원/kg;
- L/mL -> 원/L;
- exact count -> 원/개.

Each strict basis owns its own latest/previous/usual/judgment/chart.

Never:

- connect different strict bases in one chart;
- create a commodity-wide usual price;
- infer `봉 = kg`, `상자 = N개` or another unsupported conversion.

Contextual forms:

- one LIKE_FORM cohort per preserved form key;
- same-form reference only;
- CP28 `CONTEXTUAL_ONLY` / Judgment.NONE;
- no cheap/expensive tone;
- no contextual line chart in CP32.

## 6. Latest purchase semantics

`최근 구매` means the actual newest receipt-linked observation.

If the newest purchase is contextual or excluded, it remains the latest purchase shown at the top.

A strict section separately shows its own latest comparable observation. CP32 never relabels an older strict observation as the commodity's latest purchase.

## 7. UI / chart / traceability

Normal compact order:

`commodity identity -> latest purchase -> strict comparisons -> contextual references -> purchase history`

Strict chart behavior:

- actual eligible purchases only;
- one strict basis only;
- oldest -> newest;
- usual reference only for EVALUATED history;
- judgment color only when permitted by CP28;
- Korean accessibility summary;
- no tiny-point interaction requirement;
- nonlinear font-scaling-safe SP conversion.

Purchase rows are >=64dp and open the existing Receipt Detail using preserved receipt IDs. Excluded observations remain provenance-visible but never enter cohort/chart/evaluation values.

## 8. Responsive/accessibility

Frozen CP30 policy continues:

- compact `<600dp` single-column;
- medium `600..839dp` single-column;
- expanded `>=840dp`;
- two-pane only expanded + height >=480dp;
- text + color semantics;
- minimum interaction target >=48dp.

## 9. Minimal integration boundary

Legacy Price History routing now sends:

- STANDARD -> CP31 Product Detail;
- NON_STANDARD -> CP32 Commodity Detail.

`MainActivity` remains unchanged. The user-approved plan is to defer the complete launcher/home/navigation structure to CP34 rather than add temporary CP32 navigation work.

Frozen/unmodified for CP32:

- Main capture/OCR flow;
- STANDARD Product Detail behavior;
- Receipt Detail behavior;
- Receipt Review behavior;
- catalog/product/semantics/identity/category/commodity/persistence/price/priceintel/priceeval/search/detail/design packages;
- product schema 2 / receipt schema 1.

## 10. Pre-closeout discipline

Meaningful history:

- initial CI `38855330418` caught one nonexistent CP30 spacing-token reference;
- implementation fix produced green run `38855551821`;
- plan/code/lint review rejected that green run because two `SetTextI18n` warnings remained;
- final `e42629cc...` fixed text composition and made clean lint an explicit CI gate;
- `38855942283` is the only canonical CP32 execution run.

## 11. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows.

Never commit secrets, signing material, private receipts, real purchase DB/backups, identifiers or uncleared assets.

Forbidden packaged permissions CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE remain absent.

## 12. Evidence limitation

No emulator/device screenshot campaign or real-user usability study is included in CP32 evidence. Do not interpret deterministic CI as pixel-perfect on-device visual validation.

## 13. Next planned checkpoint

**CP33 — Capture / Review UX V2**

Primary objective:

`영수증 추가 -> 자동 처리 -> 확인 필요한 항목만 검토 -> 저장`

CP33 must reduce review burden without bypassing identity, provenance or validation safety. It must not absorb CP34 commercial shell/navigation work.

## 14. Stop condition

**CP32 is complete and handoff-ready. Await explicit authorization for CP33.**
