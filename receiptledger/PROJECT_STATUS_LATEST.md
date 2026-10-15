# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

The latest completed checkpoint is **CP20 — Product Rebaseline / V1 Master Specification**.

- branch: `receiptledger/run-v1-product-rebaseline-20261016`
- frozen CP20 specification boundary: `961d64ecfa484478b97e6fcd8e9ffec542be7b51`
- checkpoint type: documentation/specification only
- result: **PASS / COMPLETE**
- production Android source changed by CP20: **NO**
- DB schema/runtime/OCR/permissions/toolchain changed by CP20: **NO**

The latest executable implementation baseline remains **V1 Target API 36 Core**:

- frozen implementation HEAD: `56abeee3bb185cea8dd136d972a9660f243ded27`
- canonical successful Actions run: `38800790544` — SUCCESS
- artifact ID: `12004666174`
- artifact digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- debug APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`
- lint: 0 errors / 0 warnings
- AGP / Gradle / JDK: 8.11.1 / 8.13 / 17
- compileSdk / targetSdk / minSdk: 36 / 36 / 23
- version: `1.0.18-target-api36-core` (versionCode 19)

CP20 does not supersede this executable evidence; it supersedes only the previous statement that no next product plan existed.

## 2. Product definition frozen by CP20

ReceiptLedger is now explicitly defined as a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trusted extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

The receipt is input/evidence. The primary user-facing objects are repeat-purchase products, non-standard commodities/items, and their historical prices.

Key frozen principles:

- preserve evidence/provenance and fail closed on ambiguous identity;
- wrong product merge is worse than leaving an item unresolved;
- repeat use should become easier through confirmed reusable knowledge;
- NON_STANDARD goods may be grouped under one commodity while retaining raw unit/form;
- grouping does not imply cross-unit comparability;
- no guessed unit conversion;
- price history remains traceable to canonical saved receipt records + links;
- price judgments require explicit statistics and data-sufficiency rules;
- commercial UI hides OCR/debug implementation detail but does not delete proven internals prematurely;
- V1 remains offline/private by default unless separately authorized.

## 3. CP20 canonical documents

Primary:

1. `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
2. `PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
3. `PRODUCT_REBASELINE_V1_ROADMAP.md`

Supporting:

- `CP20_PRODUCT_REBASELINE_DECISIONS.md`
- `CP20_PRODUCT_REBASELINE_RISK_REGISTER.md`
- `CP20_PRODUCT_REBASELINE_DEPENDENCY_GATES.md`
- `CP20_PRODUCT_REBASELINE_SCOPE_AUDIT.md`
- `CP20_PRODUCT_REBASELINE_ACCEPTANCE.md`
- `CP20_PRODUCT_REBASELINE_EVIDENCE.md`
- `CP20_PRODUCT_REBASELINE_CLOSEOUT.md`
- `CP20_PRODUCT_REBASELINE_NAVIGATION.md`

## 4. Consistency result

CP20 reviewed the completed V1 foundation from domain, data/migration, identity, price-comparison, UX, privacy/security, performance and test/evidence perspectives.

Result: **COMPATIBLE WITH CONTROLLED EXTENSION**.

No blocking contradiction requiring a rewrite was found.

Existing foundations to preserve include:

- external-camera/system-picker privacy model
- EXIF/document correction
- bundled local Korean OCR
- source-coordinate preservation
- geometry layout reconstruction
- structure/item extraction with provenance
- arithmetic validation
- bounded OCR recovery / conservative merge
- required review/edit before save
- app-private receipt/image persistence
- merchant/store handling
- STANDARD / NON_STANDARD / UNCLASSIFIED base semantics
- confirmed exact alias reuse / no fuzzy silent auto-merge
- receipt-derived price history
- invalid-receipt exclusion from comparable history
- API36/lint/permission firewall

Known gaps are extensions rather than prior-checkpoint failures:

- structured brand/specification/pack identity
- merchant-context aliases
- category taxonomy
- explicit non-standard sales-unit/form model
- canonical comparable-observation layer
- richer statistics / price judgment
- search/browse/detail product UX
- commercial capture/review/UI system

## 5. Completed checkpoint chain

1. Foundation
2. Image Intake / Document Core
3. OCR Core
4. Layout Core
5. Structure Core
6. Item Tuple Core
7. Validation Core
8. Persistence Core
9. Image Archive Core
10. Receipt Library Core
11. Review / Edit Core
12. Product Identity Core
13. Price History Core
14. OCR Quality / Recovery Core
15. Vertical Integration Core
16. Merchant / Store Core
17. Conservative Cross-Pass Merge Core
18. Build Hygiene Core
19. Target API 36 Core
20. **Product Rebaseline / V1 Master Specification — COMPLETE**

## 6. Planned dependency-ordered roadmap

The roadmap now defines, but does not automatically authorize:

- CP21 Catalog Domain V2
- CP22 Persistence V2
- CP23 Receipt Product Semantics
- CP24 Identity Resolver V2
- CP25 Category System
- CP26 Commodity / Non-standard V2
- CP27 Price Intelligence V2
- CP28 Price Evaluation
- CP29 Search / Browse
- CP30 Product Detail
- CP31 Commodity Detail
- CP32 Capture / Review UX V2
- CP33 Design System
- CP34 Commercial UI Shell
- CP35 Real Receipt Evaluation
- CP36 Performance / Reliability

Dependency gates are defined in `CP20_PRODUCT_REBASELINE_DEPENDENCY_GATES.md`.

## 7. Next checkpoint boundary

The next planned checkpoint is **CP21 — Catalog Domain V2**.

CP21 should freeze exact Product/Commodity/Specification/SalesUnit/Category/AliasContext/PurchaseObservation contracts and legacy compatibility **before CP22 persistence migration begins**.

Planning existence is not execution authorization. Do not begin CP21 until the user explicitly authorizes the next group.

## 8. Public repository / namespace firewall

ReceiptLedger may modify only:

- `receiptledger/**`
- explicitly ReceiptLedger-prefixed `.github/workflows/receiptledger-*.yml`

Do not read/use/modify/depend/cache/artifact from other project namespaces.

Never commit/upload signing material, credentials, real private receipt photos, actual personal purchase databases, private backups, personal identifiers, or uncleared private assets.

The executable app privacy contract remains no CAMERA / broad media-storage / INTERNET / ACCESS_NETWORK_STATE permission.

## 9. Restart order

For a new session:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
4. `receiptledger/PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
5. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
6. `receiptledger/README.md`
7. `receiptledger/WORK_UNIT.md`
8. supporting CP20 docs only when detailed rationale is needed
9. current Android source / prior core plans only when the next checkpoint touches them

At restart verify the CP20 branch against prior handoff HEAD `7008bc28374042c0cd1d8524913e69c455735545` and confirm CP20 changes are ReceiptLedger documentation only.

**Current stop condition: CP20 is complete. Await explicit authorization before CP21.**
