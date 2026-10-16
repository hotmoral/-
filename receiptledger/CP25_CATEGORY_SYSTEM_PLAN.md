# ReceiptLedger V1 — CP25 Category System Plan

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_CATEGORY_SYSTEM_01`
Branch: `receiptledger/run-v1-category-system-20261016`
Depends on: CP21 Catalog Domain V2, CP22 Persistence V2, CP23 Receipt Product Semantics, CP24 Identity Resolver V2

## 0. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system. Category exists to make already-resolved products/items easier to find and browse. It is not part of product identity and must never repair or override an identity decision.

## 1. Scope

CP25 implements the smallest coherent category foundation:

- a stable bounded V1 taxonomy for common food and household repeat purchases;
- deterministic local category suggestion from catalog text/fields;
- four explicit category states: persisted reuse, auto-assignable suggestion, review, unresolved;
- persistence of effective assignments using the existing CP22 `category_refs(product_id,category_id)` table;
- user correction by replacing category metadata on the same stable catalog ID;
- repeat reuse from the persisted stable catalog ID;
- deterministic synthetic metrics for suggestion correctness, automation, review burden, unresolved cases and correction/reuse;
- CI evidence proving category code cannot modify frozen identity/schema/runtime contracts.

## 2. Explicit non-goals

CP25 does not:

- change product DB schema 2 or receipt DB schema 1;
- alter CP24 resolver/alias precedence or identity authority;
- use category as evidence to link, merge, split or create catalog entities;
- create a cloud taxonomy or network classifier;
- implement user-authored custom taxonomy;
- infer NON_STANDARD comparability or unit conversion;
- define price statistics/evaluation;
- redesign browse UI;
- expand permissions/network capability.

## 3. Persistence decision

CP22 already created `category_refs(product_id PRIMARY KEY, category_id)` and its category lookup index. CP25 therefore does **not** introduce schema v3.

Category suggestion remains transient until accepted by the product flow. Persistence stores only the effective category reference for an existing stable product/commodity ID. User correction simply replaces that category reference on the same ID.

No category confidence/source table is added in CP25 because it is not required to prove V1 behavior. If later analytics require category-decision provenance, that must be a separate explicit persistence amendment rather than speculative schema growth here.

## 4. Taxonomy contract

V1 has two roots:

- `FOOD` — 식품
- `HOUSEHOLD` — 생활

The bounded hierarchy contains 28 stable nodes, focused on common repeat-purchase browsing:

- dairy: milk, yogurt, cheese;
- noodles/ramen;
- frozen/dumpling;
- produce: vegetable, fruit;
- rice/grain;
- snacks;
- beverages: water, coffee;
- sauce/seasoning;
- cleaning: laundry, dish;
- paper: toilet paper, wipes;
- personal care: oral, hair.

There is deliberately no forced `OTHER` bucket. Unsupported evidence remains unresolved so browse data is not polluted by arbitrary classification.

## 5. Decision states

`CategoryDecisionV1`:

- `REUSE_PERSISTED` — an effective category already exists on the stable catalog ID; do not reclassify it;
- `AUTO_ASSIGNABLE` — one unique high-confidence local rule dominates and may be accepted automatically by downstream save integration;
- `REVIEW` — only generic evidence or conflicting category evidence exists;
- `UNRESOLVED` — no defensible category evidence exists.

An `AUTO_ASSIGNABLE` result is a category suggestion, not identity authority.

## 6. Rule design

Rules are deterministic, offline and conservative.

Strong examples:

- 우유 -> milk;
- 요구르트/요거트 -> yogurt;
- 라면 -> ramen;
- 만두/교자 -> frozen dumpling;
- exact commodity names 감자/양파 -> vegetable, 사과/바나나 -> fruit;
- 생수 -> water;
- 세탁세제 -> laundry;
- 주방세제 -> dish;
- 화장지, 물티슈, 치약, 샴푸 -> dedicated household leaves.

Generic examples such as `세제`, `음료`, `냉동`, `농산물` are review-gated at a parent category.

When multiple top rules tie across different categories, the result is REVIEW rather than arbitrary automatic assignment.

## 7. Correction/reuse semantics

Category assignment service operates through the existing `CatalogV2PersistenceStore` only.

Assignment/correction must preserve exactly:

- stable catalog ID;
- CatalogKind;
- canonical name;
- brand/productName/variant/specification values and evidence;
- creation time/origin;
- aliases and item links.

Only `CategoryRef` changes.

After persistence, the next category decision returns `REUSE_PERSISTED`, reducing repeat review burden.

## 8. Acceptance

CP25 passes only if:

- taxonomy IDs are unique and hierarchy is acyclic;
- product schema remains 2 and receipt schema remains 1;
- CP24 identity package is unchanged;
- category assignment never changes stable identity or aliases;
- unknown category IDs cannot be persisted;
- synthetic automatic suggestions have zero incorrect auto assignments;
- repeat persisted category reuse is 100% in the bounded fixture set;
- corrected category reuse is 100% in the bounded fixture set;
- generic/conflicting evidence is review-gated;
- unsupported text remains unresolved rather than forced into `OTHER`;
- full upstream tests, lint, assemble and forbidden-permission audit pass;
- exact CI/artifact/APK evidence is recorded;
- handoff docs are synchronized after the implementation boundary is frozen.

## 9. Stop condition

After implementation, evidence and handoff synchronization, stop. CP26 Commodity / Non-standard V2 is not authorized by CP25 itself.
