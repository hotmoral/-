# ReceiptLedger V1 — CP20 Risk Register

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`
Amended by: `CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`

## High-impact risks to carry forward

| Risk | Why it matters | Earliest checkpoint that must control it |
|---|---|---|
| Wrong product merge | Corrupts all future price history for that identity | CP21 / CP24 |
| False split / identity fragmentation | Same real product can be split across IDs, fragmenting history and defeating price-memory use | CP23 / CP24 |
| Merchant alias collision | Same POS abbreviation may mean different products across stores | CP21 / CP24 |
| Legacy migration identity collapse | Existing products/links may be silently merged or orphaned | CP21 / CP22 |
| Review burden remains high | The product fails if repeated known purchases still require manual work | CP23 / CP24 / CP25 / CP26 / CP33 |
| Automation optimizes precision only | A system can avoid wrong merges by refusing useful automation; this would miss the client goal | CP23 / CP24 |
| Fake cross-unit comparison | 봉/상자/kg/개 may appear directly comparable when they are not | CP21 / CP26 / CP27 |
| Ambiguous comparison-price basis | Line total, per-unit price, discounts and coupons can produce misleading history if the canonical basis is undefined | CP27 |
| Duplicate price truth | Separate observation table can diverge from receipt evidence | CP22 / CP27 |
| Category used as identity proof | Similar category does not imply same product | CP24 / CP25 |
| Sparse-history false confidence | App may label a price cheap/expensive with too little evidence | CP27 / CP28 |
| UI built before visual foundation | Commercial detail screens may require costly redesign if Design System arrives afterward | CP30–CP34 |
| UI rewrite damages proven core | Visual modernization may accidentally replace tested OCR/domain logic | CP30–CP34 |
| Search/history scale degradation | App may become slow as receipts/products grow | CP22 / CP29 / CP36 |
| Local quality defects discovered only at CP35 | Parser/resolver/category defects become expensive if not measured in their own checkpoint | CP23–CP26 |
| Privacy regression | New features may tempt unnecessary network/media permissions | Every affected checkpoint |
| Scope creep | Budgeting/cloud/online price features can delay core price-memory completion | Roadmap governance |

## Risk-handling rule

A later checkpoint should deeply re-evaluate only risks it can materially change. Unrelated risks remain recorded but do not trigger repetitive analysis or implementation work.

False merge and false split are intentionally not treated as symmetric: false merge remains the more dangerous integrity failure, while false split is a usability/data-fragmentation failure that must still be measured and actively reduced.
