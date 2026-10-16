# ReceiptLedger V1 — CP36 Performance / Reliability Evidence

Updated: 2026-10-17 KST
Checkpoint: CP36
Canonical executable HEAD: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`

## 1. Canonical CI identity

- workflow: `ReceiptLedger V1 Performance Reliability`
- canonical run: `38926526457`
- conclusion: SUCCESS
- canonical job: `117059359644`
- artifact ID: `12057296715`
- artifact name: `receiptledger-v1-performance-reliability-38926526457`
- artifact digest: `sha256:3e11a5b85f15ad860f4c5a9a81f948d79bb4dd80122fcba6b1f8d2bfffe85756`

## 2. APK / runtime identity

- versionName: `1.0.34-performance-reliability`
- versionCode: 35
- compileSdk: 36
- targetSdk: 36
- minSdk: 23
- signing: debug only
- APK SHA-256: `f17ade820165ab40213f17c38b9e720488b7791aa3621b09b3b19cdd4a53c5f7`
- lint: `No issues found.`
- runtime emulator: Android API 34 / x86_64 / 2,048 MiB

## 3. Measurement methodology

CP36 separates deterministic structural/regression checks from Android runtime measurements.

JVM evidence covers deterministic scale/read-amplification structure, long-history semantics and recovery invariants. Android instrumentation uses the actual SQLite implementations and the bundled local Korean ML Kit OCR engine. Home cold launch and PSS are measured separately through `adb`.

Wall-clock budgets are safety/decision thresholds, not claims of physical-device certification.

## 4. Baseline evidence before remediation

First valid complete Android baseline:

- run: `38906614301` (Run #8)
- HEAD: `3b2e03709ab4f6b763ec76d10bc97f17d0f34ad1`
- artifact ID: `12048563411`
- artifact digest: `sha256:4a26af068e7f27f8bcd2d1a2570772c18ca107e2670e576f0d10e79223b8000b`

Key baseline metrics:

| Metric | Baseline |
|---|---:|
| Search 1k | 2,385 ms |
| Search 10k | 17,106 ms |
| Recent 10k | 10,267 ms |
| OCR cold | 4,765 ms |
| OCR warm median | 4,635 ms |
| Price 1k | 574 ms |
| Detail 1k | 565 ms |
| Chart 1k | 29 ms |
| Home startup median | 642 ms |
| Home PSS | 42,621 KB |

Budget breaches: search 1k, search 10k, recent 10k, OCR warm.

## 5. Search remediation scope

Production changes are exactly the bounded CP29 read optimization:

- modified `SearchBrowseServiceV1.java`;
- added `SqliteSearchBrowseSnapshotV1.java`.

No product/receipt schema changes, FTS, persistent cache, new search index, identity broadening or ranking rewrite were introduced.

The SQLite-specific path bulk-loads existing discovery inputs into a transient snapshot. Generic stores retain the original path.

## 6. Canonical final runtime evidence

`CP36_STARTUP_METRICS samples=5 startup_median_ms=516 startup_max_ms=748 home_pss_kb=42787`

`CP36_ANDROID_METRICS version=1 search_1k_ms=189 search_10k_ms=1524 recent_10k_ms=856 search_10k_scanned=10000 history_observations=1000 price_1k_ms=461 detail_1k_ms=459 chart_1k_ms=19 ocr_cold_ms=4448 ocr_warm_median_ms=4078 ocr_pss_before_kb=104611 ocr_pss_after_kb=111183 migration_1k_ms=4 migration_rows=1000 archive_files=2000 archive_removed=1000 archive_ms=41 reopen_cycles=10 semantic_failures=0`

Final budget status:

| Metric | Actual | Budget | Status |
|---|---:|---:|---|
| Startup median | 516 ms | 2,500 ms | WITHIN |
| Startup max | 748 ms | 5,000 ms | WITHIN |
| Home PSS | 42,787 KB | 225,280 KB | WITHIN |
| OCR cold | 4,448 ms | 5,000 ms | WITHIN |
| OCR warm median | 4,078 ms | 1,500 ms | **BREACH — ACCEPTED** |
| Search 1k | 189 ms | 750 ms | WITHIN |
| Search 10k | 1,524 ms | 3,000 ms | WITHIN |
| Recent 10k | 856 ms | 3,000 ms | WITHIN |
| Price 1k | 461 ms | 2,000 ms | WITHIN |
| Detail 1k | 459 ms | 2,000 ms | WITHIN |
| Chart 1k | 19 ms | 500 ms | WITHIN |
| Migration 1k | 4 ms | 5,000 ms | WITHIN |
| Archive reconciliation | 41 ms | 2,000 ms | WITHIN |

Search 10k improved from 17,106 ms to 1,524 ms (~91% reduction) while preserving CP29 semantics.

## 7. SQLite search parity evidence

Canonical workflow separately runs `SearchBrowseSqliteParityInstrumentedTest`.

Result: **1/1 PASS**.

It compares the optimized SQLite path with an adapter-forced generic/frozen CP29 path for canonical/compact/structured/specification/observed/store search, normalized store filter, category browse, recent and frequent ordering.

It also injects an invalid present catalog-field source (`UNKNOWN`) and verifies both paths reject it, preserving fail-fast integrity.

## 8. Regression / reliability evidence

Run #11 passed:

- public namespace audit;
- CP36 bounded-diff guard;
- complete Gradle unit regression;
- CP29 SearchBrowseV1Test regression;
- CP35/34/33/32/31 and price/evaluation regressions;
- AndroidTest build;
- startup/memory measurement;
- runtime performance/reliability profile;
- migration 1→2 with 1,000 products;
- archive reconciliation with 2,000 files / 1,000 stale removals;
- repeated reopen cycles: 10;
- semantic failures: 0;
- SQLite search parity test;
- lint 0 errors / 0 warnings;
- debug APK/evidence packaging.

## 9. OCR warm-latency accepted-risk evidence

Warm OCR breach repeated across valid runs:

- Run #8: 4,635 ms;
- Run #9 attempt 1: 4,579 ms;
- Run #9 attempt 2: 4,573 ms;
- Run #10: 4,624 ms;
- Run #11: 4,078 ms.

The same recognizer instance is reused for warm samples. This is therefore not explained by recognizer recreation.

No OCR production change was made because real-photo recognition accuracy versus image resolution/merchant variation has not been quantified, and reducing optical work purely to satisfy an x86_64 emulator latency budget could regress the primary correctness objective. Cold OCR and memory remain within safety budgets.

This risk is explicitly accepted for V1 and remains suitable for physical-device / real-image follow-up only if separately authorized.

## 10. Permission / privacy evidence

`aapt dump permissions` contains only the internal dynamic-receiver permission.

Absent:

- CAMERA;
- READ_MEDIA_IMAGES;
- READ_EXTERNAL_STORAGE;
- WRITE_EXTERNAL_STORAGE;
- MANAGE_EXTERNAL_STORAGE;
- INTERNET;
- ACCESS_NETWORK_STATE.

No private real receipt or personal purchase database was introduced.

## 11. Evidence limitations

- Runtime latency values are from GitHub-hosted API 34 x86_64 emulator execution, not a physical Galaxy performance certificate.
- CP35's public evaluation starts at synthetic `OcrDocument` token/geometry input, so real-image OCR accuracy is still not statistically characterized.
- CP36 does not authorize post-V1 redesign based on those unresolved measurements.

## 12. Evidence conclusion

CP36 found and corrected the material CP29 SQLite search bottleneck without changing schema or discovery semantics, demonstrated semantic/fail-fast parity, and closed the planned V1 performance/reliability checkpoint with one transparent accepted risk: warm OCR latency on the CI emulator.