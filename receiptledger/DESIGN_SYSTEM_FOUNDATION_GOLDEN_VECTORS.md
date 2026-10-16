# ReceiptLedger V1 — CP30 Design System Foundation Golden Vectors

Updated: 2026-10-16 KST

## DS01 Typography roles

Expected roles = 6.

- PRICE_HERO 30/36 bold
- TITLE_LARGE 22/28 bold
- TITLE_MEDIUM 18/24 medium
- BODY_LARGE 16/24 normal
- BODY_MEDIUM 14/20 normal
- LABEL 12/16 medium

## DS02 Spacing / touch

Expected spacing scale = 4, 8, 12, 16, 24, 32dp.
Minimum touch target = 48dp.
List row minimum height = 56dp.
Content max width = 720dp.

## DS03 Semantic tone contrast

Every semantic tone foreground/background pair must pass 4.5:1:

- neutral
- primary
- positive
- negative
- review
- error
- info
- disabled

Secondary text on app background must also pass 4.5:1.

## DS04 CP28 judgment presentation

EVALUATED mappings:

- VERY_CHEAP -> positive + `평소보다 매우 저렴`
- CHEAP -> positive + `평소보다 저렴`
- TYPICAL -> neutral + `평소 수준`
- EXPENSIVE -> negative + `평소보다 비쌈`
- VERY_EXPENSIVE -> negative + `평소보다 매우 비쌈`

No judgment may be represented by color alone.

## DS05 CP28 no-judgment presentation

- INSUFFICIENT_HISTORY -> info / no cheap-expensive judgment
- CONTEXTUAL_ONLY -> info / no cheap-expensive judgment
- NON_POSITIVE_BASELINE -> review / no cheap-expensive judgment

Positive/negative tones are forbidden for all three.

## DS06 Validation presentation

- PASS -> positive
- PASS_WITH_WARNINGS -> review
- MISMATCH -> error
- INCOMPLETE -> review

Every mapping exposes user-facing Korean title and explanation.

## DS07 Reusable UI states

Expected states = 8:

- LOADING
- EMPTY
- NO_RESULT
- REVIEW_REQUIRED
- INSUFFICIENT_PRICE_HISTORY
- CONTEXTUAL_PRICE_HISTORY
- ERROR
- DISABLED

Every state has title, body and tone.

## DS08 Responsive breakpoints

- 360 -> COMPACT
- 599 -> COMPACT
- 600 -> MEDIUM
- 839 -> MEDIUM
- 840 -> EXPANDED

Gutter: 16dp compact, 24dp medium/expanded.
Two-pane: 840x479 -> false; 840x480 -> true.

## DS09 Chart basis separation

- WEIGHT_KG + WEIGHT_KG -> valid one series
- WEIGHT_KG + EACH -> reject
- weight axis -> `원/kg`
- LIKE_FORM BAG/봉 axis begins `참고`

## DS10 Representative Android adoption

Exactly two existing activities are adapted in CP30 proof scope:

- LibraryActivity
- PriceHistoryActivity

Main capture/OCR flow and ReceiptDetail/Review behavior remain unchanged.

## DS11 Canonical metric line

Expected:

`CP30_METRICS typography_roles=6 semantic_tones=8 price_presentations=8 validation_presentations=4 ui_states=8 contrast_pairs=9 responsive_cases=5 chart_cross_basis_rejections=1 min_touch_dp=48 representative_activities=2`
