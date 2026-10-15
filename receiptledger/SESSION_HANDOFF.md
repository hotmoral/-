# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

Do **not** reconstruct ReceiptLedger state from old chat memory. GitHub is the source of truth for this public workspace.

Read in this order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
4. `receiptledger/PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
5. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
6. `receiptledger/README.md`
7. `receiptledger/WORK_UNIT.md`
8. supporting CP20 docs only when detailed rationale is required
9. prior core plans / Android source only when the next checkpoint touches them

Before any new implementation, verify exact refs and compare the current CP20 branch against prior handoff HEAD `7008bc28374042c0cd1d8524913e69c455735545`.

## 1. Latest completed checkpoint

**CP20 — Product Rebaseline / V1 Master Specification**

Branch:
`receiptledger/run-v1-product-rebaseline-20261016`

Frozen CP20 specification boundary:
`5d4cd9d0d33536bbda682914af0275e6edb92a33`

Checkpoint type:
**documentation/specification only**

Acceptance:
**PASS / COMPLETE**

CP20 changed no production Android source, DB schema, OCR/runtime behavior, permissions, build toolchain, or executable artifact.

## 2. Latest executable baseline

The executable app remains frozen at **V1 Target API 36 Core**:

- implementation HEAD: `56abeee3bb185cea8dd136d972a9660f243ded27`
- canonical Actions run: `38800790544` — SUCCESS
- artifact ID: `12004666174`
- artifact digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- debug APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`
- lint: 0 errors / 0 warnings
- AGP 8.11.1 / Gradle 8.13 / JDK 17
- compileSdk 36 / targetSdk 36 / minSdk 23
- versionName `1.0.18-target-api36-core`, versionCode 19

Do not mistake CP20 documentation commits for new executable behavior.

## 3. Product essence frozen by CP20

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Target loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

Receipt data remains the source evidence. Product/commodity history becomes the main user experience.

Core principles:

- preserve provenance and contradictions;
- wrong identity merge is worse than unresolved identity;
- confirmed reusable knowledge should reduce future review effort;
- STANDARD remains exact repeatable packaged-product identity;
- NON_STANDARD remains a semantic commodity/item identity that can aggregate mixed purchase forms without claiming cross-unit comparability;
- UNCLASSIFIED remains unresolved, not a fake persisted identity;
- no guessed unit conversion;
- price history stays traceable to saved receipts + links;
- price judgments must use explicit, deterministic statistical rules and data-sufficiency thresholds;
- commercial UI hides debug complexity but does not prematurely delete proven evidence paths;
- offline/private posture remains the V1 default.

## 4. Main consistency result

CP20 reviewed domain, data/migration, identity, price-comparison, UX, privacy/security, performance and test/evidence impacts.

Result:
**COMPATIBLE WITH CONTROLLED EXTENSION**

No blocking contradiction requiring a rewrite was found.

Important extension risks carried forward:

- false product merge / identity poisoning
- merchant POS alias collisions
- migration orphaning or identity collapse
- misleading 봉/상자/kg/개 cross-unit comparison
- duplicate price truth diverging from receipts
- category similarity being misused as identity proof
- confident price labels from sparse history
- UI modernization damaging proven OCR/domain internals
- repeated-use flow remaining too manual
- search/history performance at realistic scale

## 5. Existing vertical slice to preserve

The current executable app already contains:

- external-camera capture without app CAMERA permission
- system picker without broad storage/media permission
- EXIF normalization / bounded bitmap decode
- conservative document detection + perspective correction
- bundled local Korean ML Kit OCR
- source-coordinate preservation
- geometry-based layout reconstruction
- receipt structure classification
- item tuple extraction with provenance
- arithmetic validation
- bounded OCR recovery / conservative cross-pass merge
- review/edit before save
- app-private SQLite receipt persistence
- app-private image archive
- receipt list/detail/delete
- merchant/store handling
- STANDARD / NON_STANDARD / UNCLASSIFIED product identity
- exact confirmed alias reuse only
- derived price history with invalid-receipt exclusion
- API36/lint/privacy permission firewall

Do not casually rewrite these during V2 domain work.

## 6. CP20 canonical documents

Primary:

- `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
- `PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
- `PRODUCT_REBASELINE_V1_ROADMAP.md`

Detailed supporting records are indexed by:

- `CP20_PRODUCT_REBASELINE_NAVIGATION.md`

Important specific records:

- `CP20_PRODUCT_REBASELINE_DECISIONS.md`
- `CP20_PRODUCT_REBASELINE_RISK_REGISTER.md`
- `CP20_PRODUCT_REBASELINE_DEPENDENCY_GATES.md`
- `CP20_PRODUCT_REBASELINE_SCOPE_AUDIT.md`
- `CP20_PRODUCT_REBASELINE_ACCEPTANCE.md`
- `CP20_PRODUCT_REBASELINE_EVIDENCE.md`
- `CP20_PRODUCT_REBASELINE_CLOSEOUT.md`

## 7. Roadmap / next-task boundary

Planned dependency chain:

CP21 Catalog Domain V2
→ CP22 Persistence V2
→ CP23 Receipt Product Semantics
→ CP24 Identity Resolver V2
→ CP25 Category System
→ CP26 Commodity / Non-standard V2
→ CP27 Price Intelligence V2
→ CP28 Price Evaluation
→ CP29 Search / Browse
→ CP30 Product Detail
→ CP31 Commodity Detail
→ CP32 Capture / Review UX V2
→ CP33 Design System
→ CP34 Commercial UI Shell
→ CP35 Real Receipt Evaluation
→ CP36 Performance / Reliability

The next planned checkpoint is **CP21 — Catalog Domain V2**.

CP21 must freeze exact Product/Commodity/Specification/SalesUnit/Category/AliasContext/PurchaseObservation contracts and legacy compatibility before persistence migration.

**Do not start CP21 automatically.** Planning existence is not execution authorization. Wait for explicit user direction.

## 8. Checkpoint discipline going forward

For each group:

1. re-read canonical current state and relevant dependency contracts;
2. state the essential goal and non-goals;
3. check upstream/downstream consistency before changing a contract;
4. inspect materially relevant domain/data/UX/privacy/performance/test risks;
5. avoid ritual re-audits of unrelated proven work;
6. implement the smallest coherent change that proves the goal;
7. use ReceiptLedger-scoped CI/evidence when executable changes exist;
8. close with exact refs and known limitations;
9. synchronize status/handoff materials;
10. stop before the next unauthorized group.

## 9. Security / public-repository boundary

ReceiptLedger may modify only:

- `receiptledger/**`
- explicitly ReceiptLedger-prefixed `.github/workflows/receiptledger-*.yml`

Do not read/use/modify/depend/cache/artifact from other project namespaces.

Never commit/upload release signing material, secrets, real private receipt photos, actual purchase databases, backups, personal identifiers, or uncleared private assets.

Executable permission firewall remains no CAMERA / broad media-storage / INTERNET / ACCESS_NETWORK_STATE permission.

## 10. Current stop condition

**CP20 is complete. Await explicit authorization for CP21.**
