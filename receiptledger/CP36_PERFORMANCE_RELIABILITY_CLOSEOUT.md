# ReceiptLedger V1 — CP36 Performance / Reliability Closeout

Updated: 2026-10-17 KST
Checkpoint: **CP36 — Performance / Reliability**
Status: **PASS / COMPLETE — one explicitly accepted emulator OCR warm-latency risk**

## 1. Frozen execution boundary

- branch: `receiptledger/run-v1-performance-reliability-20261016`
- predecessor CP35 handoff: `8a8a9ee0bb3bcd7e198f76b436087d54170a469d`
- predecessor CP35 frozen executable/evaluation: `6ae9fbcfe0abc17dd9471de243170a9a87272767`
- frozen CP36 executable HEAD: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- canonical Actions run: `38926526457` — SUCCESS
- canonical job: `117059359644` — SUCCESS
- artifact ID: `12057296715`
- artifact digest: `sha256:3e11a5b85f15ad860f4c5a9a81f948d79bb4dd80122fcba6b1f8d2bfffe85756`
- debug APK SHA-256: `f17ade820165ab40213f17c38b9e720488b7791aa3621b09b3b19cdd4a53c5f7`
- version: `1.0.34-performance-reliability` / versionCode 35
- lint: `No issues found.`

Any later status/handoff synchronization is documentation-only. The executable/evidence boundary remains `78cdd99c...`.

## 2. Measurement-first result

CP36 first measured the frozen CP35 system before changing production code. Coverage included startup, process memory, ML Kit OCR, 1k/10k CP29 discovery, 1,000-observation price/detail/chart workloads, product migration, archive reconciliation and repeated reopen/recovery.

The first valid Android baseline was Run #8 (`38906614301`, HEAD `3b2e0370...`). It exposed a material search bottleneck caused by product-by-product and receipt-by-receipt SQLite reads.

Baseline Android measurements included:

- search 1k: 2,385 ms;
- search 10k: 17,106 ms;
- recent 10k: 10,267 ms;
- OCR cold: 4,765 ms;
- OCR warm median: 4,635 ms.

## 3. Bounded search remediation

Only the measured search bottleneck was corrected. Production changes are limited to:

- `SearchBrowseServiceV1.java`;
- new read-only `SqliteSearchBrowseSnapshotV1.java`.

The final SQLite path bulk-reads existing product/catalog/link/receipt/item tables into a transient in-memory projection per discovery call. It adds no FTS, persistent cache, new index, schema or secondary truth. Generic/in-memory stores retain the original CP29 path.

CP29 ranking, filters, match reasons, category semantics and identity non-authority remain unchanged. Repeated normalization of the same query/field text was removed without changing `ProductNameNormalizer` semantics.

## 4. Final performance result

Canonical Run #11 measurements:

- Home cold-start median: 516 ms; max: 748 ms;
- Home PSS: 42,787 KB;
- search 1k: 189 ms;
- search 10k: 1,524 ms;
- recent 10k: 856 ms;
- 1,000-observation price intelligence: 461 ms;
- 1,000-observation Product Detail: 459 ms;
- 1,000-point chart draw: 19 ms;
- OCR cold: 4,448 ms;
- OCR warm median: 4,078 ms;
- OCR PSS before/after: 104,611 / 111,183 KB;
- product migration 1,000 rows: 4 ms;
- archive reconciliation 2,000 files / 1,000 removals: 41 ms;
- reopen cycles: 10;
- semantic failures: 0.

All decision budgets passed except OCR warm latency. Search 10k improved from 17,106 ms to 1,524 ms without FTS/index/cache/schema changes.

## 5. Search semantic / reliability parity

A dedicated Android instrumentation test compares the SQLite fast path against an adapter-forced generic/frozen CP29 path for canonical/compact/structured/specification/observed/store searches, store filtering, category browse, recent and frequent ordering.

The same test corrupts a present catalog field source to `UNKNOWN` and verifies both paths fail fast.

Result: **1/1 PASS**.

## 6. Explicitly accepted OCR warm-latency risk

The only remaining budget miss is warm ML Kit OCR latency on the canonical API 34 x86_64 CI emulator:

- Run #8: 4,635 ms;
- Run #9 attempt 1: 4,579 ms;
- Run #9 attempt 2: 4,573 ms;
- Run #10: 4,624 ms;
- Run #11: 4,078 ms;
- decision budget: 1,500 ms.

This is reproducible and is not hidden as noise. It is accepted for V1 rather than changed because the same `MlKitOcrEngine` instance is reused for warm samples, cold OCR remains within 5,000 ms, memory remains well within budget, the measurement is an x86_64 emulator rather than a physical target device, and CP35 did not establish real-photo OCR accuracy against resolution/merchant variation. Downsampling or changing recognition solely to hit the emulator latency target could trade away correctness without evidence.

No production OCR change is made. Physical-device / real-image OCR profiling remains a known post-V1 validation need only if separately authorized.

## 7. Reliability / regression / privacy

Canonical Run #11 passed namespace audit, bounded scope guard, full Gradle unit regression, lint 0/0, APK + AndroidTest build, deterministic JVM reliability tests, emulator startup/PSS profiling, Android runtime profiling, SQLite search parity, budget analysis and evidence packaging.

Product schema 2 and receipt schema 1 remain unchanged. Identity, commodity, price, evaluation, review, UI and OCR semantics remain frozen.

Forbidden CAMERA/media/storage/network permissions remain absent. No private receipt, real purchase DB, credential, release signing material or personal identifier was added.

## 8. Non-canonical execution history

Early runs that failed in SDK/emulator/harness bootstrap are not product failures. Run #9 had two successful attempts on the same SHA; attempt 2 was accidentally re-run by the assistant while responding to a user stop request and is retained only as repeatability evidence. Run #11 is the sole canonical CP36 execution.

## 9. V1 boundary

CP36 is the final checkpoint in the currently authorized V1 roadmap. The planned CP20 → CP36 chain is complete.

No post-V1 feature group, physical-device campaign or OCR redesign is authorized by this closeout.

**Stop after docs-only handoff synchronization and await explicit user authorization for any post-V1 work.**