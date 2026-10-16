# ReceiptLedger V1 — CP30 Design System Foundation Consistency Review

Updated: 2026-10-16 KST

## 1. Verdict

**IMPLEMENTATION ALLOWED / CONTROLLED PRESENTATION EXTENSION**

CP30 can add centralized design tokens and View-toolkit helpers without changing domain, persistence, price or search semantics.

## 2. Current UI reality

The Android harness uses programmatic `android.widget` Views directly. Existing screens hardcode text sizes, padding and button construction independently. There is no Compose/AppCompat/Material dependency.

A Compose or Material migration inside CP30 would be an architecture migration disguised as visual work and is therefore rejected.

## 3. Domain boundary

### Identity / catalog
Visual similarity, card grouping and color can never create or merge a product ID. CP21/24 remain authoritative.

### Category / commodity
Category colors or sections are browsing metadata only. NON_STANDARD grouping and comparison-basis separation remain CP26 authority.

### Price intelligence / evaluation
CP30 displays CP27/28 results; it cannot recalculate eligibility or thresholds. No-judgment states remain visually distinct from cheap/expensive judgments.

### Search
Search field styling cannot change CP29 matching/ranking and has no identity mutation authority.

## 4. Accessibility consistency

The foundation adopts Android's current minimum interaction/contrast baseline:

- 48dp minimum interactive target;
- >=4.5:1 small-text contrast;
- >=3:1 large text/graphics;
- state meaning expressed in text as well as color;
- sp-based typography roles;
- visible action labels satisfy naming for text buttons; icon-only future controls require content descriptions.

The frozen palette is unit-tested for its small-text semantic foreground/background pairs.

## 5. Responsive consistency

Width class contract:

- COMPACT `<600dp`;
- MEDIUM `600..839dp`;
- EXPANDED `>=840dp`.

Page gutter:

- compact 16dp;
- medium/expanded 24dp.

Two-pane is allowed only at expanded width and height >=480dp. This avoids treating physical device type as a layout authority.

## 6. Typography consistency

The system font is retained. CP30 introduces no bundled or downloadable font.

Roles are purpose-based rather than screen-based:

- PRICE_HERO 30sp;
- TITLE_LARGE 22sp;
- TITLE_MEDIUM 18sp;
- BODY_LARGE 16sp;
- BODY_MEDIUM 14sp;
- LABEL 12sp.

Future screens must consume roles rather than add arbitrary sizes.

## 7. Semantic presentation consistency

Every CP28 evaluated price judgment has Korean text plus a semantic tone. Every no-judgment state also has explicit text, but never receives positive/negative judgment color.

Validation states are similarly mapped to explicit user-facing labels rather than raw enum text.

## 8. Chart consistency

A chart series is identified by `stable catalog ID + CP27 comparison basis`.

Cross-basis series are rejected. In particular:

- kg and each cannot be connected;
- L and package cannot be connected;
- LIKE_FORM is explicitly labeled as contextual/reference-only;
- usual-price reference is shown only for CP28 EVALUATED state.

## 9. Representative adoption

Only `LibraryActivity` and legacy `PriceHistoryActivity` are adapted to prove the UiKit works in real programmatic Views.

Not changed:

- Main capture/OCR flow;
- receipt review engine/dialog behavior;
- receipt detail identity flow;
- domain/persistence/search/price packages;
- AndroidManifest/permissions.

## 10. Risk review

### Risk: attractive color becomes business meaning
Mitigation: semantic mapping is derived from existing CP28 states and always includes text.

### Risk: foundation turns into final UI redesign
Mitigation: only two representative activities adopt common creation helpers; CP31–34 own full surfaces.

### Risk: visual toolkit migration introduces dependency/build risk
Mitigation: no new UI dependency; current platform Views retained.

### Risk: responsive logic becomes tablet detection
Mitigation: use available-window width/height breakpoints only.

### Risk: chart visually merges incompatible commodity histories
Mitigation: ChartGrammar rejects mixed comparison bases.

## 11. Result

No blocking contradiction found. CP30 is a presentation-only foundation and does not require schema, identity, search, price-policy or permission changes.
