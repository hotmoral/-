# ReceiptLedger V1 — CP20 Risk Register

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`

## High-impact risks to carry forward

| Risk | Why it matters | Earliest checkpoint that must control it |
|---|---|---|
| Wrong product merge | Corrupts all future price history for that identity | CP21 / CP24 |
| Merchant alias collision | Same POS abbreviation may mean different products across stores | CP21 / CP24 |
| Legacy migration identity collapse | Existing products/links may be silently merged or orphaned | CP21 / CP22 |
| Fake cross-unit comparison | 봉/상자/kg/개 may appear directly comparable when they are not | CP21 / CP26 / CP27 |
| Duplicate price truth | Separate observation table can diverge from receipt evidence | CP22 / CP27 |
| Category used as identity proof | Similar category does not imply same product | CP24 / CP25 |
| Sparse-history false confidence | App may label a price cheap/expensive with too little evidence | CP27 / CP28 |
| UI rewrite damages proven core | Visual modernization may accidentally replace tested OCR/domain logic | CP32–CP34 |
| Review friction stays too high | Core value is lost if repeated products still require manual linking every time | CP24 / CP32 |
| Search/history scale degradation | App may become slow as receipts/products grow | CP22 / CP29 / CP36 |
| Privacy regression | New features may tempt unnecessary network/media permissions | Every affected checkpoint |
| Scope creep | Budgeting/cloud/online price features can delay core price-memory completion | Roadmap governance |

## Risk-handling rule

A later checkpoint should deeply re-evaluate only risks it can materially change. Unrelated risks remain recorded but do not trigger repetitive analysis or implementation work.
