# ReceiptLedger V1 — Commodity / Non-standard V2 Golden Vectors

Updated: 2026-10-16 KST

## 1. Identity/grouping vectors

### Auto-group exact commodity name across forms

All resolve to existing `c_potato`:

- `감자 1봉`
- `감자 1KG`
- `감자 5개`
- `감자 1상자`

Purchase form does not alter commodity identity.

### Review-only modifier

- `국산 감자 1봉` -> suggest `감자`, REVIEW
- `햇 대파 1단` -> suggest `대파`, REVIEW

Modifier-bearing names do not gain automatic grouping authority.

### No lexical-substring grouping

- `감자칩 1봉` -> must not suggest/group `감자`
- `감자전분 1KG` -> must not suggest/group `감자`

### STANDARD cue review gate

- `감자 100G 5입` with explicit non-ambiguous packaged specification -> REVIEW rather than commodity auto-group.

### Confirmed repeat alias

User confirms `국산 감자 1봉` -> `감자` at merchant A.

- merchant A repeat -> MERCHANT exact alias auto-group
- merchant B without confirmation -> remains review suggestion

### Cross-kind alias firewall

If a confirmed alias targets a STANDARD catalog row, CP26 returns REVIEW/CROSS_KIND_CONFLICT rather than commodity auto-group.

## 2. Purchase-form preservation vectors

The saved value must exactly preserve CP23 quantity/unit/raw-label/source/confidence/confirmation for examples including:

- `감자 1봉`
- `감자 1KG`
- `감자 5개`
- `감자 1상자`
- `대파 1단`
- `사과 2팩`
- `양파 2KG`
- `당근 500G`

Grouping confirmation does not upgrade purchase-form confirmation state.

## 3. Form-relation vectors

### EXACT_NORMALIZABLE_QUANTITY

- `1kg` vs `500g` -> exact weight basis, 1000g vs 500g
- `1L` vs `750mL` -> exact volume basis
- count vs count -> exact count basis

### SAME_FORM_ONLY

- `1봉` vs `2봉` -> same form only, no normalized price authority
- OTHER `망` vs OTHER `망` -> same form only

### INCOMPARABLE

- 봉 vs 상자
- 개 vs kg
- unrelated OTHER labels
- unknown/non-convertible dimensions

## 4. Metric fixture set

Expected local bounded metrics:

- fixtures: 25
- known commodity: 21
- correct automatic groups: 18
- incorrect automatic groups: 0
- false grouping: 0
- review suggestions: 2
- visible false split / fragmentation risk: 1
- negative fixtures: 4
- raw form preservation sample: 12/12
- confirmed repeat reuse: 3/3

The single false split is deliberate evidence that conservative grouping may miss subtype/attached-token forms such as `알감자`. It must remain visible instead of being hidden with unsafe substring/fuzzy auto-grouping.

## 5. Interpretation limit

These vectors prove the CP26 local policy contract only. They do not claim real-receipt accuracy, price-comparison correctness or complete Korean grocery taxonomy coverage.
