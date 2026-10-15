# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP23 — Receipt Product Semantics — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-receipt-product-semantics-20261016`
- predecessor CP22 handoff: `913150c7acb06cb80a18833a10680657213239ec`
- frozen CP23 implementation HEAD: `5bffb66bd43814f8d638791b5697f79ff089028b`
- canonical Actions run: `38822100885` — SUCCESS
- job: `116720855010` — SUCCESS
- artifact ID: `12013477721`
- artifact digest: `sha256:fa22d082545adae7c414b0f1c089604174341f7e879c1acd5e4677e1dc2b7195`
- debug APK SHA-256: `e4e64f85f9700089b32f9f0b8121eef0a2f565d09b5428599d3717296c1b8324`
- Receipt Product Semantics tests: 7/7 PASS
- Catalog Domain V2 tests: 15/15 PASS
- Persistence V2 tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.21-receipt-product-semantics` / versionCode 22

The frozen executable/evidence boundary remains `5bffb66...`; later closeout/handoff commits are documentation-only.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

The receipt is evidence/input. Product/commodity history and price judgment are the destination.

## 3. CP23 result

CP23 adds conservative semantic parsing over the existing receipt item name. It emits evidence candidates for:

- brand only from explicit bracket evidence or caller-supplied known-brand prefix knowledge;
- lexical product/family name;
- explicit non-numeric parenthetical variant;
- product specification from explicit pack/measure evidence;
- raw purchase form;
- confidence/reason/evidence;
- ambiguity and review requirement.

Every parsed `CatalogField` remains `PARSED_FROM_RECEIPT / UNCONFIRMED`. CP23 emits no catalog ID and has no merge/link authority.

## 4. Critical ambiguity rule

Standalone physical measures such as `1KG`, `500G`, `1L`, `900ML` cannot safely prove whether the text describes packaged net content or a commodity purchase amount.

CP23 therefore preserves both defensible readings with MEDIUM confidence and requires review. It does not choose STANDARD vs NON_STANDARD from the item string alone.

Strong forms:

- `5입` / `10개입`: package-count evidence;
- `200MLX6` / `6X200ML`: explicit inner measure + count + total;
- 봉/상자/단: strong raw purchase-form evidence without conversion.

Context-sensitive 팩/개 remain review-gated.

## 5. Local quality evidence

Canonical metric:

`fixtures=26 expected_fields=68 predicted_fields=66 correct_fields=64 precision_ppm=969696 recall_ppm=941176 review_required=13 semantic_ready=13 ambiguous=10 ambiguous_reviewed=10 no_invention_negatives=2`

Thus:

- precision: 96.9696%
- recall: 94.1176%
- ambiguous cases review-gated: 10/10
- no-invention negatives: 2/2

These are synthetic parser-fixture metrics, not final real-receipt accuracy claims.

## 6. Deliberate conservative limitations

- unknown first-time brand is not inferred merely from first-token position;
- free-form flavor/model suffix is not guessed as a variant;
- lexical product text is preserved when a finer split is not defensible;
- parser readiness does not imply identity auto-link readiness.

These limitations protect against false semantics while CP24 later addresses identity resolution and false-split pressure.

## 7. Superseded failed run

Run `38821795314` — FAILURE.

Public-tree/scope guards passed. Android lint then rejected initial `List.sort` / comparator convenience APIs as API24+ under minSdk23. No semantic metric/evidence stage ran. The implementation was changed to API23-safe sorting without changing minSdk or suppressing lint.

Canonical successful run is `38822100885`.

## 8. Frozen storage/security contracts

Preserve:

- product catalog schema = 2;
- receipt schema = 1;
- stable catalog ID remains identity authority;
- UNCLASSIFIED remains unresolved;
- category and merchant context are not SKU identity;
- HIGH confidence != CONFIRMED;
- grouping != comparability;
- no guessed package-form conversion;
- price/date/store/validation truth remains receipt-derived;
- no new network or permission capability.

## 9. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> **CP23 Receipt Product Semantics**.

## 10. Next planned checkpoint

**CP24 — Identity Resolver V2**.

It must separately define safe identity authority and measure:

- false merge;
- false split / fragmentation;
- automatic link success;
- ambiguous/review-required rate;
- incorrect automatic decisions;
- repeat-purchase reuse after prior confirmation.

CP23 parser confidence cannot grant CP24 merge authority.

## 11. Restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_CLOSEOUT.md`
4. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_EVIDENCE.md`
5. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_PLAN.md`
6. `receiptledger/RECEIPT_PRODUCT_SEMANTICS_CONSISTENCY_REVIEW.md`
7. `receiptledger/RECEIPT_PRODUCT_SEMANTICS_GOLDEN_VECTORS.md`
8. `receiptledger/CP22_PERSISTENCE_V2_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify branch/ref and frozen implementation boundary before future work.

**Current stop condition: CP23 is complete. Await explicit authorization for CP24.**
