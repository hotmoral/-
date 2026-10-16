# ReceiptLedger public execution work unit

Updated: 2026-10-17 KST

## Current stage

**CP36 — Performance / Reliability is COMPLETE.**

- branch: `receiptledger/run-v1-performance-reliability-20261016`
- predecessor CP35 handoff: `8a8a9ee0bb3bcd7e198f76b436087d54170a469d`
- frozen executable HEAD: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- canonical Actions: `38926526457` — SUCCESS
- job: `117059359644` — SUCCESS
- artifact ID: `12057296715`
- artifact digest: `sha256:3e11a5b85f15ad860f4c5a9a81f948d79bb4dd80122fcba6b1f8d2bfffe85756`
- APK SHA-256: `f17ade820165ab40213f17c38b9e720488b7791aa3621b09b3b19cdd4a53c5f7`
- versionCode 35
- versionName `1.0.34-performance-reliability`
- lint: 0 errors / 0 warnings

## Frozen CP36 result

CP36 used a measure-first strategy. Initial valid Android profiling found CP29 discovery was dominated by repeated SQLite reads.

Baseline:

- search 1k: 2,385 ms;
- search 10k: 17,106 ms;
- recent 10k: 10,267 ms.

Bounded remediation changed only the CP29 discovery read path:

- modified `SearchBrowseServiceV1.java`;
- added read-only transient `SqliteSearchBrowseSnapshotV1.java`.

No FTS, persistent cache, new index, schema or secondary truth was added.

Final canonical metrics:

- startup median/max: 516 / 748 ms;
- Home PSS: 42,787 KB;
- search 1k: 189 ms;
- search 10k: 1,524 ms;
- recent 10k: 856 ms;
- price 1k: 461 ms;
- detail 1k: 459 ms;
- chart 1k: 19 ms;
- OCR cold: 4,448 ms;
- OCR warm median: 4,078 ms;
- OCR PSS before/after: 104,611 / 111,183 KB;
- migration 1k: 4 ms;
- archive reconciliation 2,000 files / 1,000 removals: 41 ms;
- reopen cycles: 10;
- semantic failures: 0.

## Search semantic evidence

The optimized SQLite fast path was compared directly with an adapter-forced original/generic CP29 path.

Covered:

- canonical search;
- compact search;
- structured/specification search;
- observed-name search;
- store search/filter;
- category browse;
- recent ordering;
- frequent ordering;
- corrupt catalog-field fail-fast behavior.

Result: **1/1 PASS**.

## Explicit accepted risk

Warm ML Kit OCR remains above its emulator decision budget:

- final median: 4,078 ms;
- budget: 1,500 ms.

This is an explicit V1 accepted risk, not a hidden pass. Production OCR is unchanged because cold OCR and memory pass, recognizer reuse is already present, and no real-photo accuracy evidence exists to justify downsampling or altered recognition purely for speed.

Physical-device / real-image OCR profiling is not authorized by CP36 closeout.

## Reliability / regression evidence

Canonical Run #11 passed:

- namespace/scope guards;
- complete JVM unit regression;
- lint 0/0;
- APK + AndroidTest build;
- startup/PSS profile;
- Android runtime profile;
- migration stress;
- archive reconciliation;
- reopen/recovery repetition;
- SQLite search semantic/fail-fast parity;
- evidence packaging.

Product schema 2 / receipt schema 1 remain unchanged. Forbidden camera/media/storage/network permissions remain absent.

## Execution-history notes

Early CP36 failures were CI/bootstrap/harness failures rather than product-performance failures, including sdkmanager pipe handling, AndroidTest setup, adb PATH, AVD path resolution and one legacy migration fixture normalization mismatch.

Run #9 attempt 2 was accidentally re-run by the assistant during a user stop request. It is non-canonical and retained only as repeatability evidence.

## Completed V1 boundary

The authorized V1 chain CP20 through CP36 is complete.

No post-V1 work unit is currently authorized.

Before any future work:

1. recover `PROJECT_STATUS_LATEST.md` and `SESSION_HANDOFF.md` first;
2. verify live handoff HEAD and frozen executable `78cdd99c...` separately;
3. define a new bounded checkpoint with explicit scope/non-goals/acceptance/evidence/stop conditions;
4. review contradictions against frozen identity/price/review/search/UI/privacy contracts;
5. avoid changing OCR or schema without direct evidence;
6. preserve public namespace isolation and docs/executable boundary discipline.

## Public/privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipt photos, personal purchase DBs/backups, identifiers or uncleared assets.

## Stop condition

**Planned ReceiptLedger V1 CP20–CP36 is complete. Await explicit authorization for any post-V1 work.**
