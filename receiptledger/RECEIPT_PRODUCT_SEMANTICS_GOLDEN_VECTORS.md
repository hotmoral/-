# ReceiptLedger V1 — CP23 Receipt Product Semantics Golden Vectors

Updated: 2026-10-16 KST

Purpose: public-safe synthetic POS-like strings that exercise conservative semantic parsing. These are parser contract fixtures, not claims about all Korean receipt formats.

## 1. Strong packaged-product evidence

| ID | Raw item text | Expected semantic result |
|---|---|---|
| S01 | `농심 신라면 5입` | brand=농심, product=신라면, packCount=5, no ambiguity |
| S02 | `오뚜기 진라면 (매운맛) 5입` | brand=오뚜기, product=진라면, variant=매운맛, packCount=5 |
| S03 | `주스 200MLX6` | product=주스, inner=200mL, pack=6, total=1200mL |
| S04 | `탄산수 6X200ML` | product=탄산수, inner=200mL, pack=6, total=1200mL |
| S05 | `동원 참치 100G 4입` | brand=동원, product=참치, inner=100g, pack=4, total=400g; MEDIUM because relation is not explicit multiplication |
| S06 | `코카콜라 제로 500ML 2입` | brand=코카콜라, product=제로, inner=500mL, pack=2, total=1000mL; MEDIUM |

## 2. Standalone physical-measure ambiguity

| ID | Raw item text | Expected semantic result |
|---|---|---|
| A01 | `서울우유 나100% 1000ML` | brand=서울우유, product=나100%, spec 1000mL + purchase-form 1000mL, ambiguous, review |
| A02 | `비비고 왕교자 1.05KG` | brand=비비고, product=왕교자, spec 1050g + purchase-form 1.05kg, ambiguous, review |
| A03 | `감자 1KG` | product=감자, spec 1000g + purchase-form 1kg, ambiguous, review |
| A04 | `생수 2L` | product=생수, spec 2000mL + purchase-form 2L, ambiguous, review |

Rule: CP23 does not choose STANDARD vs NON_STANDARD from these strings alone.

## 3. Raw purchase forms

| ID | Raw item text | Expected semantic result |
|---|---|---|
| P01 | `감자 1봉` | product=감자, PurchaseForm 1 BAG, no conversion |
| P02 | `대파 1단` | product=대파, PurchaseForm 1 BUNDLE, no conversion |
| P03 | `과자 3봉` | product=과자, PurchaseForm 3 BAG |
| P04 | `상품 1상자` | product=상품, PurchaseForm 1 BOX |
| P05 | `사과 5개` | product=사과, PurchaseForm 5 EACH, context-sensitive, review |
| P06 | `세제 리필 2팩` | product=세제 리필, PurchaseForm 2 PACK, context-sensitive, review |

## 4. Explicit brand / variant evidence

| ID | Raw item text | Expected semantic result |
|---|---|---|
| B01 | `[브랜드X] 테스트제품 500G` | explicit brand=브랜드X; physical measure remains ambiguous |
| B02 | `요거트 (저지방) 450G` | product=요거트, variant=저지방; physical measure remains ambiguous |
| B03 | `제품A (1+1) 500G` | `(1+1)` is NOT a variant because it is numeric/promotion-like |

## 5. Conservative limitations deliberately measured

| ID | Raw item text | Expected behavior |
|---|---|---|
| L01 | `새브랜드 초코바 50G` | if `새브랜드` is not supplied as known brand knowledge, do not invent brand; keep it in lexical product name; physical measure ambiguity forces review |
| L02 | `오뚜기 진라면 매운맛 5입` | brand and pack parse, but free-form `매운맛` is not split into variant; lexical product remains `진라면 매운맛` |
| L03 | `양파` | lexical product only; no invented unit/brand/specification; review |
| L04 | `ABC123 9900` | no brand/unit/specification invented from product/code/price-like digits; review |
| L05 | empty string | no candidates; review |

## 6. Quality thresholds

The executable metric suite calculates field-level expected/predicted/correct counts from these and related fixtures.

CP23 minimums:

- precision >= 90%;
- recall >= 85%;
- every detected ambiguous-measure fixture is review-gated;
- designated no-invention fixtures emit no false structured brand/specification/purchase-form evidence.

A perfect score is neither required nor expected. Conservative misses must remain visible so later checkpoints can decide whether additional knowledge is justified.
