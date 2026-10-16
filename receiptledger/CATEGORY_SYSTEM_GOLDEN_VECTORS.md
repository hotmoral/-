# ReceiptLedger V1 — Category System Golden Vectors

Updated: 2026-10-16 KST

## 1. Purpose

These vectors prove bounded CP25 behavior only. They are synthetic local classification fixtures, not real-receipt accuracy claims.

## 2. Strong automatic suggestions

Expected `AUTO_ASSIGNABLE` examples:

- `서울우유1L` -> `FOOD_DAIRY_MILK`
- `딸기우유` -> `FOOD_DAIRY_MILK`
- `요구르트` -> `FOOD_DAIRY_YOGURT`
- `그릭요거트` -> `FOOD_DAIRY_YOGURT`
- `체다치즈` -> `FOOD_DAIRY_CHEESE`
- `신라면5입` -> `FOOD_NOODLES_RAMEN`
- `진라면` -> `FOOD_NOODLES_RAMEN`
- `비비고왕교자` -> `FOOD_FROZEN_DUMPLING`
- `냉동만두` -> `FOOD_FROZEN_DUMPLING`
- commodity `감자` / `양파` -> `FOOD_PRODUCE_VEGETABLE`
- commodity `사과` / `바나나` -> `FOOD_PRODUCE_FRUIT`
- commodity `쌀` -> `FOOD_GRAIN`
- `초코과자` -> `FOOD_SNACK`
- `제주삼다수생수` -> `FOOD_BEVERAGE_WATER`
- `원두커피` -> `FOOD_BEVERAGE_COFFEE`
- `고추장` -> `FOOD_SAUCE_SEASONING`
- `세탁세제` -> `HOUSEHOLD_CLEANING_LAUNDRY`
- `주방세제` -> `HOUSEHOLD_CLEANING_DISH`
- `3겹화장지` -> `HOUSEHOLD_PAPER_TOILET`
- `물티슈100매` -> `HOUSEHOLD_PAPER_WIPES`
- `치약` -> `HOUSEHOLD_PERSONAL_CARE_ORAL`
- `샴푸` -> `HOUSEHOLD_PERSONAL_CARE_HAIR`

## 3. Review-gated generic evidence

Expected `REVIEW`:

- `생활세제` -> primary suggestion `HOUSEHOLD_CLEANING`
- `탄산음료` -> `FOOD_BEVERAGE`
- `냉동식품` -> `FOOD_FROZEN`
- `농산물꾸러미` -> `FOOD_PRODUCE`

Generic parent-category words are not silently treated as precise leaf classification.

## 4. Conflicting evidence

`우유 치즈` triggers two equal high-confidence category rules and therefore must be `REVIEW`, never arbitrary auto-assignment.

## 5. Unsupported evidence

Expected `UNRESOLVED`:

- `멀티상품A`
- `기획상품B`

There is no forced `OTHER` category.

## 6. Persistence/reuse vectors

- an `AUTO_ASSIGNABLE` category accepted for a stable product ID is persisted through existing `category_refs`;
- the next decision for that same ID is `REUSE_PERSISTED`;
- user correction replaces only the category and the corrected category is reused;
- stable ID, CatalogKind, canonical name, semantic fields, timestamps/origin and aliases remain unchanged;
- unknown category ID is rejected.

## 7. Canonical metric target

Synthetic fixture target:

`fixtures=30 known_category=28 auto_suggestions=24 correct_auto_suggestions=24 incorrect_auto_suggestions=0 review_required=6 unresolved=2 repeat_cases=4 repeat_reused=4 correction_cases=3 correction_reused=3`

CI acceptance requires:

- zero incorrect automatic category suggestions in this bounded set;
- repeat reuse = repeat cases;
- correction reuse = correction cases;
- meaningful automatic coverage (at least half of known-category fixtures);
- upstream identity/catalog/persistence/semantics tests remain green.
