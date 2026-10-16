# ReceiptLedger V1 — CP30 Design System Foundation Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_DESIGN_SYSTEM_FOUNDATION_01`

## 1. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system. CP30 must make the already-frozen semantics legible and consistent; it must not reinterpret product identity, comparison eligibility, price judgment, search ranking or receipt truth for visual convenience.

## 2. Scope

CP30 establishes the reusable visual/interaction grammar that CP31–34 will consume:

- Korean-first typography roles, including numeric/price emphasis;
- neutral and semantic color tokens;
- spacing/grid, radius, elevation and minimum touch-target tokens;
- responsive page gutter/content-width policy;
- programmatic View-based UiKit helpers compatible with the current architecture;
- buttons, text fields, search fields, chips, list/card rows and status surfaces;
- price/judgment/review/error semantic presentation mapping;
- chart grammar for price history and comparison-basis separation;
- loading/empty/error/review state contracts;
- accessibility contrast/touch target/content-label rules;
- deterministic contract tests and CI evidence.

## 3. Architecture decision

The app currently uses `Activity + android.widget` programmatic Views and has no Compose/AppCompat/Material dependency. CP30 will **not** introduce a Compose or Material dependency migration.

Instead:

1. pure-Java design token and semantic contract classes are the canonical foundation;
2. a small Android `UiKitV1` applies those tokens to current `TextView/Button/EditText/LinearLayout` widgets;
3. CP31–34 use this kit rather than adding new hardcoded sizes/colors;
4. a later toolkit migration is allowed only as an explicit migration checkpoint, not as an incidental CP30 side effect.

## 4. Typography

System sans-serif is retained for Korean/platform compatibility; no bundled font asset is introduced.

Roles:

- `PRICE_HERO` — primary current price/strong numeric focus;
- `TITLE_LARGE` — screen title;
- `TITLE_MEDIUM` — section title/card title;
- `BODY_LARGE` — primary readable body;
- `BODY_MEDIUM` — supporting body;
- `LABEL` — metadata/chips/captions.

Price emphasis must never remove the accompanying unit/basis/context text. Percentage change and previous/usual price use secondary hierarchy rather than competing with the primary price.

## 5. Semantic color contract

Semantic states use both text/icon/label and color; color is never the sole carrier of meaning.

Roles:

- neutral/default;
- primary/action;
- positive/cheap;
- negative/expensive;
- review/warning;
- error;
- disabled;
- information.

`VERY_CHEAP/CHEAP` map to positive, `TYPICAL` to neutral, `EXPENSIVE/VERY_EXPENSIVE` to negative. CP28 no-judgment states remain explicit states and never receive a misleading cheap/expensive color.

## 6. Spacing / shape / responsive contract

- base spacing scale: 4, 8, 12, 16, 24, 32 dp;
- minimum interactive touch target: 48dp;
- narrow phone page gutter: 16dp;
- >=600dp width page gutter: 24dp;
- content max width: 720dp;
- compact controls may be visually smaller only when their interactive hit area remains >=48dp;
- standard radii are small/medium/large tokens rather than per-screen ad hoc values.

## 7. Accessibility baseline

Current Android guidance is adopted as a contract:

- minimum touch target 48dp;
- small text foreground/background contrast >=4.5:1;
- large text/graphics contrast >=3:1;
- non-text interactive controls require meaningful accessibility labels when their visible text does not already name the action;
- support user font scaling; no fixed pixel text sizes;
- important state changes must be representable in text, not only color.

## 8. Price and chart grammar

Charts may display only one comparison basis per series. A commodity's `WEIGHT_KG`, `VOLUME_L`, `EACH`, and contextual package-form histories must never be connected into one line.

Every chart surface must expose:

- comparison basis/unit label;
- observed purchase points;
- current/latest point;
- usual-price reference only when CP28 has a valid baseline;
- store/date context on detail interaction;
- no cheap/expensive color for contextual/no-judgment cohorts.

CP30 defines grammar only; final chart screen implementation belongs to CP31/32.

## 9. State surfaces

Required states:

- loading;
- empty;
- no search result;
- review required;
- insufficient price history;
- contextual-only price history;
- validation/error;
- disabled/unavailable action.

Each state has a title, short explanation and optional action; raw enum names must not be the final user-facing copy.

## 10. Frozen upstream boundary

CP30 must not change:

- CP21 catalog equality/identity rules;
- CP22 product/receipt schemas;
- CP23 semantic parsing;
- CP24 resolver authority;
- CP25 category meaning;
- CP26 commodity grouping/comparability;
- CP27 price eligibility/discount attribution;
- CP28 thresholds/judgment policy;
- CP29 search ranking or mutation boundary;
- OCR/document/persistence behavior;
- permissions/network/privacy model.

## 11. Representative adoption

CP30 may apply the new UiKit to a small representative subset of existing programmatic UI (titles, standard action buttons/status text) to prove the foundation compiles and is consumable. It must not turn into a full screen redesign.

## 12. Acceptance

CP30 closes only if:

- token roles are deterministic and centrally defined;
- semantic CP28 mappings cover every judgment and no-judgment status;
- accessibility contrast audit passes the frozen palette;
- minimum touch target and responsive policies are tested;
- chart grammar forbids cross-basis line series;
- representative Android UiKit compiles on minSdk 23;
- CP21–29 targeted regressions pass;
- lint/build/forbidden-permission evidence passes;
- no schema/domain/search mutation occurs;
- exact implementation/evidence refs are frozen;
- status/roadmap/handoff documents are synchronized.

## 13. Non-goals

- full Product Detail screen;
- full Commodity Detail screen;
- final Capture/Review UX redesign;
- final commercial navigation shell;
- Compose migration;
- downloadable/custom fonts;
- animation/motion system redesign;
- user-selectable themes;
- dark theme finalization;
- market-price semantics;
- changing CP28 evaluation thresholds.
