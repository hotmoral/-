# ReceiptLedger V1 — CP30 Design System Foundation Consistency Review

Updated: 2026-10-16 KST

## 1. Verdict

**IMPLEMENTATION ALLOWED / CONTROLLED PRESENTATION EXTENSION**

CP30 can add centralized design tokens and View-toolkit helpers without changing domain, persistence, price or search semantics.

## 2. Current UI reality

The Android harness uses programmatic `android.widget` Views directly. Existing screens hardcode text sizes, padding and button construction independently. There is no Compose/AppCompat/Material dependency.

A Compose or Material migration inside CP30 would be an architecture migration disguised as visual work and is therefore rejected.

## 3. Frozen upstream compatibility

- stable catalog ID remains identity authority;
- search relevance remains discovery-only and cannot merge/relink;
- category remains browse metadata;
- commodity grouping remains distinct from price comparability;
- CP27 price eligibility and CP28 judgment thresholds are consumed, not recalculated;
- product schema 2 / receipt schema 1 remain unchanged;
- OCR/capture/review/detail behavior and permissions remain unchanged.

## 4. Accessibility contract

The foundation adopts the Android accessibility baseline:

- minimum interactive target 48dp;
- small-text contrast >=4.5:1;
- large text/graphics contrast >=3:1;
- state meaning expressed in text as well as color;
- sp-based typography;
- icon-only controls require a non-empty spoken/content description.

The frozen semantic palette is unit-tested for its small-text foreground/background pairs.

## 5. Responsive contract

- COMPACT `<600dp`;
- MEDIUM `600..839dp`;
- EXPANDED `>=840dp`;
- page gutter 16dp compact, 24dp medium/expanded;
- content max width token 720dp;
- two-pane eligible only at expanded width and height >=480dp.

The window dimensions, not physical device type, are the layout authority.

## 6. Typography / spacing / surface contract

System sans-serif is retained; no bundled/downloadable font is introduced.

Roles:

- PRICE_HERO 30/36 bold;
- TITLE_LARGE 22/28 bold;
- TITLE_MEDIUM 18/24 medium;
- BODY_LARGE 16/24 normal;
- BODY_MEDIUM 14/20 normal;
- LABEL 12/16 medium.

Spacing: 4/8/12/16/24/32dp.
Radii: 8/12/16dp.
Elevation: card 1dp, floating 3dp.

Future screens consume these roles rather than adding ad-hoc values.

## 7. Icon grammar

CP30 freezes icon semantics without prematurely choosing a third-party icon library or adding many assets.

- glyph size token: 24dp;
- minimum interactive hit area: 48dp;
- stable roles: ADD_RECEIPT, SEARCH, FILTER, RECEIPT, PRODUCT, CATEGORY, PRICE_TREND, REVIEW, MORE, DELETE;
- every icon-only role has explicit Korean accessibility text;
- icon shape may later change, but role meaning and accessibility contract must not.

## 8. Semantic presentation

Every CP28 evaluated price judgment has Korean text plus semantic tone. No-judgment states never receive positive/negative judgment color. Validation and reusable loading/empty/review/error states also expose explicit Korean title/body text instead of raw enum names.

## 9. Chart consistency

A chart series is `stable catalog ID + CP27 comparison basis`.

- kg and each cannot be connected;
- L and package cannot be connected;
- LIKE_FORM is contextual/reference-only;
- usual-price reference and judgment color are allowed only for CP28 EVALUATED state.

## 10. Representative adoption

Only `LibraryActivity` and legacy `PriceHistoryActivity` consume the new UiKit in CP30. This proves the foundation works with real programmatic Views without turning CP30 into the final screen redesign.

Frozen:

- MainActivity capture/OCR;
- ReceiptDetailActivity identity flow;
- ReceiptReviewDialog behavior;
- AndroidManifest/permissions;
- upstream domain/search/price packages.

## 11. Risk review

- **Color becomes business meaning:** prevented by text + tone mapping.
- **Foundation turns into final redesign:** limited representative adoption only.
- **UI toolkit migration risk:** no new Compose/Material dependency.
- **Tablet assumptions:** window-width/height contract only.
- **Cross-basis chart deception:** mixed basis rejected.
- **Ad-hoc icon semantics:** stable icon roles and accessibility labels frozen.
- **Ad-hoc shadows:** elevation tokens centralized.

## 12. Result

No blocking contradiction remains. CP30 is a presentation-only foundation and does not require schema, identity, search, price-policy or permission changes.
