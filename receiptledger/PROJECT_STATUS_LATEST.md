# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP24 — Identity Resolver V2 — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-identity-resolver-v2-20261016`
- predecessor CP23 handoff: `d04667a5dd9f257117f59bcde194d5b702fa1337`
- frozen CP24 implementation HEAD: `4b556afd4dd52b68cf768e937bb456665ad4c231`
- canonical Actions run: `38824134990` — SUCCESS
- job: `116727478370` — SUCCESS
- artifact ID: `12014915453`
- artifact digest: `sha256:4740590ca2c7d7525842aa3ebe6ec7964911d303322ebad77b5701344ce76867`
- debug APK SHA-256: `0656c60110ba7debcb0801ddee048cd2220b959c2119539a79274eebbc05eb6e`
- Identity Resolver V2 tests: 8/8 PASS
- Receipt Product Semantics tests: 7/7 PASS
- Catalog Domain V2 tests: 15/15 PASS
- Persistence V2 tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.22-identity-resolver-v2` / versionCode 23

Any later documentation-only handoff commit is not additional CP24 implementation. The executable/evidence boundary remains `4b556afd...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

The receipt remains evidence/input. Reliable repeat identity is necessary so historical prices accumulate under the correct product instead of being poisoned by false merges or fragmented across duplicate identities.

## 3. CP24 result

CP24 implemented deterministic resolution to **existing** stable catalog IDs with three states:

- `AUTO_LINK`
- `REVIEW`
- `UNRESOLVED`

Authority order is frozen:

1. exact MERCHANT alias;
2. exact GLOBAL alias;
3. unique strict semantic exact;
4. semantic suggestion/review;
5. unresolved.

The resolver never auto-creates or merges catalog entities.

## 4. Safety / automation boundary

Confirmed exact aliases are strong reusable identity knowledge, but a dangling alias or explicit current brand/variant/non-ambiguous specification contradiction is review-gated.

Strict semantic auto-link is allowed only for one unique existing STANDARD candidate with non-ambiguous CP23 evidence, confirmed exact product name and confirmed exact specification, plus symmetric confirmed exact brand/variant when present.

Not identity authority by itself:

- product-name similarity;
- parser HIGH confidence;
- category;
- merchant/store;
- fuzzy/edit-distance/embedding/phonetic similarity.

CP23 standalone physical-measure ambiguity remains review-required.

## 5. Repeat-use learning

After explicit user confirmation, alias knowledge follows least-authority scope:

- merchant context -> MERCHANT alias by default;
- explicit global choice or no merchant -> GLOBAL alias.

This supports the client goal that a previously confirmed repeat purchase becomes automatic without turning a store-specific POS code into unsafe global knowledge.

## 6. Local quality evidence

Canonical metric:

`fixtures=24 known_identity=20 auto_links=14 correct_auto_links=14 incorrect_auto_links=0 false_merge=0 false_split=1 review_required=6 unresolved=4 repeat_cases=4 repeat_reused=4`

Thus:

- automatic-link correctness: 14/14;
- incorrect automatic link: 0;
- false merge: 0;
- false split / fragmentation risk: 1/20 known identities = 5%;
- repeat confirmed reuse: 4/4 = 100%.

The single false-split case is intentionally retained as a visible weak-evidence fragmentation risk. It must not be erased by unsafe resolver broadening. These metrics are synthetic/local, not CP35 real-receipt accuracy claims.

## 7. Frozen upstream/storage/security contracts

Preserve:

- stable catalog ID = identity/equality authority;
- product schema = 2;
- receipt schema = 1;
- UNCLASSIFIED remains unresolved;
- category is not identity authority;
- HIGH confidence != CONFIRMED;
- unknown != invented default;
- grouping != comparability;
- no guessed package-form conversion;
- price/date/store/validation truth remains receipt-derived;
- no new network or permission capability;
- semantic commodity grouping remains CP26 work.

## 8. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> **CP24 Identity Resolver V2**.

## 9. Next planned checkpoint

**CP25 — Category System**.

Goal: define taxonomy, persistence, assignment/suggestion, correction and confirmed reuse for browsing/classification while preserving the hard rule that category never proves product identity.

CP25 must measure category suggestion accuracy and user-review burden locally and must not reopen CP24 identity authority without an explicit amendment.

**Do not begin CP25 without explicit user authorization.**

## 10. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP24_IDENTITY_RESOLVER_V2_CLOSEOUT.md`
4. `receiptledger/CP24_IDENTITY_RESOLVER_V2_EVIDENCE.md`
5. `receiptledger/CP24_IDENTITY_RESOLVER_V2_PLAN.md`
6. `receiptledger/IDENTITY_RESOLVER_V2_CONSISTENCY_REVIEW.md`
7. `receiptledger/IDENTITY_RESOLVER_V2_GOLDEN_VECTORS.md`
8. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify current branch/ref and frozen implementation boundary before future work.

## 11. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase databases/backups, personal identifiers or uncleared assets.

Forbidden APK permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

**Current stop condition: CP24 is complete. Await explicit authorization for CP25.**
