# ReceiptLedger V1 — Client Requirement Alignment Amendment

Updated: 2026-10-16 KST
Status: CANONICAL / DOCUMENTATION-ONLY
Applies after: CP21 Catalog Domain V2

## 0. Purpose

This amendment records a post-CP21 audit against the client's stated product need. It does not change CP21 implementation semantics or executable behavior. It refines downstream acceptance criteria and roadmap ordering while correction cost is still low.

The client need remains:

> Photograph a receipt, automatically register purchases by product/commodity and category, accumulate historical prices, and later answer quickly whether a current price is cheaper or more expensive than the user's own past purchases.

## 1. Finding

Current CP20/CP21 direction is aligned with the client requirement. No rollback or rewrite is required.

Four downstream corrections are mandatory.

## 2. Amendment A — control false split as well as false merge

Existing policy correctly treats false merge as the higher-severity error because one wrong merge corrupts historical prices.

However, false split is also a core product failure: one real product split across multiple catalog IDs fragments history and defeats price-memory use.

Therefore CP24 must measure both:

- false merge rate;
- false split / identity-fragmentation rate.

False merge remains the stricter safety constraint, but false split may not be ignored merely by leaving identities unresolved forever.

## 3. Amendment B — automation/review burden is a first-class product metric

The target experience is not merely accurate extraction. It is minimal repeated manual work.

CP23–CP26 must define checkpoint-local measurements where materially applicable for:

- automatic registration/link success rate;
- ambiguous/review-required rate;
- incorrect automatic decision rate;
- repeat-purchase reuse rate after prior confirmation.

A repeated known product should require less review over time when evidence and confirmed knowledge are sufficient.

CP35 remains the end-to-end evaluation checkpoint, but it must not be the first time these local failure modes are measured.

## 4. Amendment C — CP27 must define the canonical comparison price

Historical price statistics are meaningless unless the compared value is explicit.

CP27 must define, test and document the canonical comparable price for a purchase observation, including at minimum:

- line amount vs per-purchased-unit amount;
- quantity greater than one;
- item-specific discounts;
- coupons/receipt-level discounts whose allocation is not provable;
- provenance of printed/inferred/user-edited price values;
- invalid/incomplete observations;
- same-product package identity requirements;
- like-unit NON_STANDARD subsets.

Default product principle:

> Compare the price actually attributable to one purchased unit/package of the same catalog identity when the evidence supports it.

Do not arbitrarily distribute a receipt-level discount across items when the receipt does not provide defensible attribution.

## 5. Amendment D — design foundation precedes final commercial detail screens

The previous roadmap placed final-looking Product/Commodity detail work before Design System. That creates avoidable visual rework.

Future execution order is amended to:

- CP29 Search / Browse data access and interaction contract;
- CP30 Design System Foundation;
- CP31 Product Detail;
- CP32 Commodity Detail;
- CP33 Capture / Review UX V2;
- CP34 Commercial UI Shell;
- CP35 Real Receipt Evaluation;
- CP36 Performance / Reliability.

Design System remains presentation-only and must not force domain/storage rewrites.

## 6. Acceptance discipline added to downstream checkpoints

Every affected checkpoint must ask, only where relevant:

1. Can this create a false merge?
2. Can this create or perpetuate a false split?
3. Does repeated confirmed use reduce review burden?
4. Is the price being compared exactly defined and receipt-traceable?
5. Can incomparable units/forms be presented as comparable?
6. Is the local quality metric being measured now rather than deferred unnecessarily?

## 7. What is not changed

This amendment does not change:

- frozen CP21 implementation HEAD `8596106c370e172161ef00e8d460dc78667bf80d`;
- stable-ID catalog equality;
- legacy migration preservation rules;
- UNCLASSIFIED unresolved semantics;
- grouping != comparability;
- confidence != confirmation;
- receipt-derived price truth;
- offline/private permission model;
- CP22 as the next implementation checkpoint.

## 8. Decision

Result: **ALIGNED WITH CLIENT REQUIREMENT, WITH DOWNSTREAM ACCEPTANCE/ORDER AMENDMENTS**.

CP22 may proceed only after these amendments are treated as canonical downstream constraints.
