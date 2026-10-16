# ReceiptLedger V1 — CP30 Design System Foundation Closeout

Updated: 2026-10-16 KST

## 1. Result

**PASS / COMPLETE**

CP30 establishes a reusable presentation foundation for CP31–34 without changing ReceiptLedger's identity, commodity, price, search, persistence or privacy semantics.

Canonical executable boundary:

- branch `receiptledger/run-v1-design-system-foundation-20261016`
- frozen implementation HEAD `ff0745db529499171246866039521a0b83e830e4`
- Actions `38842905325` SUCCESS
- job `116786812761` SUCCESS
- artifact `12022330459`
- artifact digest `sha256:f1bcb1b2d58e328b15cf4811dd1dc107888cc2f5ba733ce1bb1ee60bf8ec0e5e`
- APK SHA-256 `cb35afb3ee0bf00dafad48f0b33733401661a982df11557bb01f716ca6655373`
- CP30 9/9 PASS
- lint 0 errors / 0 warnings
- version `1.0.28-design-system-foundation`, versionCode 29

## 2. What CP30 solved

Before CP30, programmatic Android screens constructed typography, padding and actions independently. If CP31–34 had proceeded directly, the app would have accumulated new one-off visual rules and could have misrepresented domain states.

CP30 now provides a central contract for:

- Korean-first typography hierarchy and numeric/price emphasis;
- semantic colors and explicit Korean state labels;
- spacing, radii and elevation;
- 48dp minimum interaction area;
- adaptive width policy;
- reusable View-based title/body/status/button/list/search/chip/card helpers;
- CP28 price-judgment presentation;
- validation/review/loading/empty/error states;
- chart basis separation;
- icon role/accessibility semantics.

## 3. Architecture decision

The current app remains `Activity + android.widget` with programmatic Views.

CP30 deliberately did **not** introduce:

- Compose;
- AppCompat/Material migration;
- downloadable/custom fonts;
- a new navigation architecture;
- final commercial screen redesign.

This avoids turning a design-system checkpoint into a broad architecture rewrite.

## 4. Product-semantics preservation

CP30 only presents existing truth.

It does not change:

- stable catalog-ID equality;
- CP24 resolver authority;
- CP25 category meaning;
- CP26 grouping/comparability;
- CP27 price eligibility or discount rules;
- CP28 threshold/judgment calculations;
- CP29 search ranking or identity mutation boundary;
- receipt/product schemas;
- OCR/review/persistence behavior.

A cheap/expensive color is never used as a substitute for an explicit text judgment. CP28 no-judgment states remain visibly and textually non-judgmental.

## 5. Chart and commodity safety

The visual layer cannot connect different CP27 comparison bases into one chart series. Thus a commodity's kg, each, liter and contextual package-form histories cannot be made to look directly comparable merely because they share a commodity ID.

This preserves the product-critical rule:

> same grouped commodity does not imply comparable price.

## 6. Accessibility / responsive foundation

Frozen baseline:

- small-text semantic contrast >=4.5:1;
- minimum interactive hit area 48dp;
- text in sp-based roles;
- icon-only actions require Korean accessibility labels;
- compact `<600dp`, medium `600–839dp`, expanded `>=840dp`;
- two-pane only at expanded width and adequate height.

The contract is based on the available app window rather than a hardcoded phone/tablet distinction.

## 7. Pre-closeout correction

Initial implementation HEAD `5c63a537a14ea183100ee531afce0edb4744482a` passed Actions run `38842440663`.

Before closure, plan-to-code review caught two cheap omissions:

1. icon semantics were described but not yet centralized;
2. card elevation remained a UiKit-local numeric value.

Rather than close a technically green but incomplete foundation, CP30 added:

- `IconGrammarV1` with 10 stable semantic roles, 24dp glyph token, 48dp hit-target contract and Korean accessibility labels;
- centralized `ELEVATION_CARD_DP=1` and `ELEVATION_FLOATING_DP=3` tokens.

The corrected HEAD `ff0745db...` then passed the full second CI run `38842905325`. Therefore the earlier green commit is not the canonical executable boundary.

## 8. Deliberate limitations

CP30 does not claim:

- final Product Detail UX;
- final Commodity Detail UX;
- final chart rendering implementation;
- final capture/review flow redesign;
- final navigation/home shell;
- final icon artwork/library;
- final dark theme;
- user theme customization;
- real-user visual usability validation.

These belong to later checkpoints and must consume the frozen CP30 grammar rather than bypass it.

## 9. Next planned checkpoint

**CP31 — Product Detail**

Goal: build the first full commercial STANDARD-product price-memory screen on top of frozen CP21–30 contracts.

CP31 should expose, without semantic invention:

- stable product identity and structured specification;
- current/latest price;
- previous price and difference;
- usual price and CP28 explanation;
- one-basis price-history chart;
- store/date context;
- receipt traceability;
- insufficient/no-judgment states;
- responsive/accessibility behavior using CP30 components/tokens.

CP31 must not widen identity authority, reinterpret discounts, mix price bases or redesign the foundation ad hoc.

## 10. Stop condition

CP30 is closed. Do not begin CP31 without explicit user authorization.
