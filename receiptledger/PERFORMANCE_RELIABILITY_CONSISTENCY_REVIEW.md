# ReceiptLedger V1 — Performance / Reliability Consistency Review

Updated: 2026-10-16 KST
Checkpoint: CP36

## 1. Why CP36 begins with measurement

Several current implementations are visibly linear and may contain nested reads, but source inspection alone does not establish that a user-visible bottleneck exists. CP36 therefore separates a *potential hot path* from a *measured defect*.

This prevents two opposite errors:

- prematurely introducing FTS/index/cache/schema complexity that can drift from CP29 search semantics;
- underestimating real Android SQLite cost by relying only on fast in-memory JVM fixtures.

## 2. Material predecessor consistency checks

### CP29 Search / Browse

`SearchBrowseServiceV1` currently rebuilds discovery entries by scanning catalog products and, per product, reading V2 metadata, item links and source receipts. That is semantically correct and read-only, but potentially expensive at scale.

CP36 may measure and optimize this read path, but must preserve:

- exact/prefix/all-terms/contains ranking semantics;
- category/store filters;
- recent/frequent ordering;
- search relevance as non-authoritative discovery only;
- stable product IDs in results.

A faster result with different identity/ranking meaning is a failure.

### CP27/28 Price Intelligence

Price analysis walks item links and loads source receipts/purchase forms. CP36 may reduce redundant reads if measurement proves necessity, but cannot create a duplicated mutable price table or alter eligibility/basis/threshold semantics.

### CP31/32 Detail and charts

Detail is a read projection over frozen price intelligence. Chart optimization cannot downsample in a way that changes displayed latest/usual semantics or mixes bases. If a future optimization limits drawn points, provenance/history remains complete and the reduction rule must be deterministic and presentation-only.

### CP33 Capture / Review

Performance work must not move durable save before review, erase provenance, or turn uncertain values into authoritative data. OCR cancellation/failure must remain recoverable.

### CP34 Home / Shell

Home data loading already occurs on a worker thread, so slow discovery should not become a UI-thread ANR. CP36 still measures time-to-result because a multi-second async wait is a product performance defect even when the main thread remains responsive.

### CP35 Evaluation

CP35's synthetic token-boundary evidence remains valid. CP36 must not reinterpret an emulator OCR timing fixture as a real-world OCR accuracy study.

## 3. Storage consistency risks

### Receipt DB

`SqliteReceiptStore` reads each receipt row and then separately reads its items and issues. Bulk history/list operations may therefore amplify query count. Any hardening must preserve receipt as the source of price truth and exact issue/item provenance.

### Product DB

The product store has existing product-link/category/catalog-field indexes. Do not add a search index merely because CP29 scans linearly; first measure 1k/10k and identify whether catalog scan, metadata fan-out, receipt fan-out or sorting dominates.

### Cross-database truth

Receipt and product data reside in separate SQLite databases. A performance projection must not become a second mutable authority that can silently diverge after save/edit/delete.

## 4. Migration consistency

Product schema supports only explicit 1 -> 2 migration. Unsupported versions fail fast.

CP36 must verify:

- v1 product IDs remain unchanged;
- v1 aliases migrate as GLOBAL aliases to the same product IDs;
- item links retain source product IDs;
- new V2 tables/indexes exist;
- unsupported migration requests still fail instead of destructive fallback.

Receipt schema remains version 1 and has no migration path to invent in CP36 unless a real necessity is demonstrated.

## 5. Archive consistency

Receipt image save uses temp write, fsync and rename, with DB save rollback deleting the image on DB failure. Reconciliation deletes temp/orphan files and preserves files whose IDs exist in receipt storage.

CP36 must test these invariants under bounded scale without changing the ordering merely to improve benchmark numbers.

## 6. OCR/runtime measurement interpretation

The Android emulator can measure:

- model initialization/processing latency for bundled ML Kit;
- process memory on a fixed CI profile;
- Android SQLite behavior;
- Activity cold launch on that profile.

It cannot prove performance on every physical phone. Record emulator API/ABI and treat absolute values as bounded CI evidence, while using repeat samples and ratios to reduce noise.

## 7. Optimization firewall

The following require measurement evidence before introduction:

- FTS;
- denormalized search tables;
- persistent discovery cache;
- new schema/index solely for speed;
- bulk snapshot storage outside existing truth tables;
- background precomputation;
- chart/history truncation.

Read batching that preserves exact existing records may be lower risk, but still requires a demonstrated bottleneck and semantic regression tests.

## 8. Failure interpretation

Distinguish:

- **PRODUCT DEFECT:** reproducible semantic loss, unsafe recovery, unacceptable bounded latency/memory;
- **SCALING DEFECT:** user path exceeds budget because of deterministic amplification;
- **CI/EMULATOR INFRA:** boot/package/service instability before the benchmark itself;
- **MEASUREMENT NOISE:** isolated timing spike with stable medians and no repeated breach.

Do not modify production code to fix CI infrastructure failures.

## 9. Closure rule

A green CI run is insufficient if the measurements show an accepted budget breach that has not been analyzed. Conversely, a theoretical N+1 pattern is insufficient reason for production change if actual representative workloads remain comfortably bounded.
