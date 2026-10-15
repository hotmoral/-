# ReceiptLedger V1 — CP23 Receipt Product Semantics Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_RECEIPT_PRODUCT_SEMANTICS_01`
Branch: `receiptledger/run-v1-receipt-product-semantics-20261016`
Predecessor handoff: `913150c7acb06cb80a18833a10680657213239ec`

## 0. Product purpose

ReceiptLedger exists to remember a user's real purchase prices with minimal manual bookkeeping. CP23 advances that purpose only by converting one saved/extracted receipt item name into conservative semantic candidates that later identity logic can use.

CP23 does **not** decide that two receipt rows are the same product. That authority remains CP24.

## 1. Inputs

Primary semantic input is the existing receipt item `name` produced by the proven item-tuple pipeline. Existing receipt quantity/price/date/store/provenance remain untouched and authoritative in their current layers.

Examples:

- `농심 신라면 5입`
- `서울우유 나100% 1000ML`
- `감자 1봉`
- `감자 1KG`
- `주스 200MLX6`

## 2. Outputs

The parser may emit unconfirmed candidates for:

- brand;
- product/family lexical name;
- explicit parenthetical variant descriptor;
- product specification;
- purchase/sales form;
- ambiguity/review reasons.

Every emitted candidate carries:

- raw evidence text;
- `CatalogField.Confidence`;
- deterministic reason;
- conversion to `CatalogField.parsed(...)`, therefore `PARSED_FROM_RECEIPT + UNCONFIRMED`.

HIGH confidence is still not confirmation and never becomes merge authority.

## 3. Conservative parsing rules

### 3.1 Brand

Brand is emitted only when evidence is explicit:

1. a leading `[브랜드]` marker; or
2. a longest-prefix match from caller-supplied known brand knowledge.

The parser does not declare the first token to be a brand merely because it appears first.

This means an unseen first-time brand can remain inside the lexical product name. That is deliberate fail-closed behavior, not a parsing failure to hide.

### 3.2 Variant

Variant is emitted only from an explicit non-numeric parenthetical descriptor such as `(매운맛)` or `(저지방)`.

Free-form lexical splitting such as deciding that `진라면 매운맛` means product=`진라면`, variant=`매운맛` is deferred. Generic suffix guessing would create false semantics too cheaply.

### 3.3 Pack specification

Strong packaged-product evidence:

- `5입`, `10개입` -> explicit pack count;
- `200MLX6`, `6X200ML` -> explicit inner content + pack count + exact total/net content;
- `1L 2입`, `100G 4입` -> adjacent explicit physical measure plus pack count; interpreted as inner content and exact total with MEDIUM confidence unless the multiplicative form is explicit.

### 3.4 Purchase form

Strong raw purchase-form evidence:

- `봉` -> BAG;
- `상자` -> BOX;
- `단` -> BUNDLE.

`팩` and `개` are context-sensitive. They are preserved as PurchaseForm candidates but marked ambiguous/review-required rather than promoted to a package-identity fact.

### 3.5 Weight/volume without context

A standalone `1KG`, `500G`, `1L`, `900ML` can mean either packaged net content or a commodity purchase amount.

CP23 therefore preserves **both** defensible readings:

- ProductSpecification candidate;
- PurchaseForm candidate;

both with MEDIUM confidence, plus an explicit ambiguity flag and review requirement.

This is essential for `감자 1KG` versus packaged `왕교자 1.05KG`; text alone cannot safely decide the catalog kind.

## 4. Review semantics

`reviewRequired=true` when materially unresolved semantics remain, including:

- empty/no lexical product name;
- standalone weight/volume dual interpretation;
- context-sensitive `팩`/`개` form;
- no structured evidence beyond a lexical name.

`reviewRequired=false` means only that CP23 produced a sufficiently explicit semantic parse for downstream processing. It **does not** mean the item may be auto-linked to a catalog ID.

## 5. Quality evidence

CP23 uses public-safe synthetic Korean/POS-like golden strings. The metric suite reports:

- field-level precision;
- field-level recall;
- brand coverage;
- product-name exactness;
- specification exactness;
- purchase-form exactness;
- review-required count / semantic-ready count;
- ambiguity cases and whether every ambiguity is review-gated.

Thresholds are intentionally conservative:

- field precision >= 90%;
- field recall >= 85%;
- all detected ambiguous measure cases require review;
- no structured semantics invented for designated negative fixtures.

The fixture suite intentionally includes at least one unknown brand and one free-form variant that the parser does not guess, so local metrics do not pretend to be perfect real-world recognition.

These are CP23 local parser metrics, not CP35 real-receipt acceptance.

## 6. Explicit non-goals

CP23 MUST NOT:

- create/merge catalog IDs;
- change stable-ID authority;
- use category as identity proof;
- add fuzzy auto-linking;
- persist semantic guesses automatically to a product entity;
- migrate either database schema;
- duplicate receipt price/date/store truth;
- decide cross-unit price comparability;
- define cheap/normal/expensive labels;
- redesign UI/navigation;
- add network access, online product databases, barcode lookup, permissions, cloud or unrelated scope.

## 7. Storage boundary

CP22 remains frozen:

- product catalog schema = 2;
- receipt schema = 1;
- receipt facts remain authoritative;
- semantic storage capability exists but CP23 parsing does not automatically attach unconfirmed semantics to a catalog identity.

## 8. Acceptance criteria

CP23 is PASS only if:

1. parser is deterministic pure Java;
2. parser consumes raw receipt item name without mutating upstream evidence;
3. candidate provenance/confidence/reason are explicit;
4. emitted `CatalogField` values are unconfirmed parsed evidence;
5. unknown brands are not guessed from positional tokens;
6. explicit pack-count/multipack forms parse deterministically;
7. standalone physical measures remain ambiguous rather than forced to STANDARD or NON_STANDARD;
8. BAG/BOX/BUNDLE purchase forms are preserved without guessed conversion;
9. `팩`/`개` are review-gated;
10. local metric thresholds pass;
11. existing CP21/CP22 tests still pass;
12. catalog/receipt schemas are unchanged;
13. lint is 0 errors / 0 warnings;
14. debug APK builds and forbidden-permission audit stays clean;
15. diff is CP23-scoped only;
16. exact implementation/evidence refs are frozen and handoff documents synchronized.

## 9. Downstream gate

CP24 may consume CP23 candidates as evidence for merchant-aware identity resolution.

CP24 must still prove its own authority rules, false-merge and false-split behavior, auto-link success, ambiguity/review rate and confirmed-repeat reuse. CP23 confidence alone can never authorize a merge.
