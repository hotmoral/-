# ReceiptLedger V1 — Real Receipt Evaluation Consistency Review

Updated: 2026-10-16 KST
Checkpoint: CP35

## 1. Why this checkpoint is evaluation-first

CP20–34 already define the authoritative domain, storage, capture/review, price, detail and shell behavior. CP35 therefore starts from the assumption that production semantics are frozen and must be *measured*, not casually rewritten.

The cheapest trustworthy proof is a public-safe deterministic evaluation harness that composes the same frozen services used by the app.

## 2. Material contract checks

### Identity

PASS by design if:

- a new raw alias has no authority until confirmation;
- a confirmed GLOBAL exact alias can be reused;
- a merely similar alias stays unresolved;
- category, semantic resemblance, price and search relevance never create a stable-ID link.

A false merge is a hard CP35 failure.

### Receipt truth / review

Recognition output is not automatically authoritative. CP33 `CaptureReviewAssessmentV2` remains the review gate. Arithmetic mismatch or material uncertainty must not be counted as a safe final registration.

### Product semantics

`ReceiptProductSemanticParser` may provide semantic evidence such as product name, package specification or purchase form. That evidence may guide fixture assertions and confirmed data, but it does not itself widen identity authority.

### Price truth

CP27 remains authoritative:

- STANDARD_PACKAGE for STANDARD products;
- kg/g -> WEIGHT_KG;
- L/mL -> VOLUME_L;
- count -> EACH;
- contextual package forms remain LIKE_FORM only;
- multi-item receipt-level discounts are not guessed onto individual items;
- invalid/mismatched receipts are excluded.

### Detail traceability

CP31/32 are read projections. CP35 may assert that purchase rows carry exact `receiptId`/item ordinal/eligibility from CP27 observations, but may not introduce a second price truth.

## 3. Test-double validity

Using `InMemoryReceiptStore` and `InMemoryProductCatalogStore` is acceptable for deterministic CP35 domain evaluation because they implement the same frozen interfaces consumed by the price/detail services. The purpose is semantic correctness, not SQLite performance or migration behavior.

A small test-only `CatalogV2PersistenceStore` implementation may retain parsed purchase forms required by CP27 commodity normalization. It is not production persistence and must not be packaged as app truth.

## 4. OCR boundary

Synthetic fixtures enter at the `OcrDocument` token/geometry boundary and are processed by the production `ReceiptRecognitionPipeline`. This deliberately evaluates recognition/structure logic without claiming ML Kit camera/image character-recognition accuracy.

That limitation must be explicit in closeout evidence. Image OCR/model quality and real-device capture variability are not silently inferred from CP35.

## 5. Review burden interpretation

A fixture is not considered a failure merely because explicit confirmation is required. Correct conservative review is preferable to a false authoritative registration.

The evaluation distinguishes:

- automatic safe outcome;
- expected review/identity confirmation;
- final correct registration after the declared confirmation;
- repeat-use automation after prior confirmation.

## 6. Scope conflict review

No material reason currently exists to modify:

- production OCR/recovery/item/validation code;
- identity resolver authority;
- price/evaluation algorithms;
- CP31/32 detail services;
- CP33 capture/review UI;
- CP34 shell;
- DB schemas.

If the first evaluation run exposes a real defect, fix only the failing semantic path and add a regression fixture. Otherwise CP35 remains evaluation-only.

## 7. CP36 firewall

Do not convert CP35 into scale/performance work. No 1k/10k catalog benchmark, FTS/index/cache, startup/OCR latency, memory profiling, migration stress or archive recovery campaign belongs here. Those remain CP36.

## 8. Closure rule

A green build is insufficient if the harness only checks its own expectations without traversing production services. Closure requires fixture-to-production-service traceability, explicit limitations and post-green plan/code comparison.
