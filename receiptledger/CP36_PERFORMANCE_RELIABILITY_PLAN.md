# ReceiptLedger V1 — CP36 Performance / Reliability Plan

Updated: 2026-10-16 KST
Checkpoint: **CP36 — Performance / Reliability**
Status: **AUTHORIZED / IN PROGRESS**

## 1. Canonical baseline

- predecessor handoff: `8a8a9ee0bb3bcd7e198f76b436087d54170a469d`
- predecessor frozen executable/evaluation: `6ae9fbcfe0abc17dd9471de243170a9a87272767`
- working branch: `receiptledger/run-v1-performance-reliability-20261016`

The handoff ref and executable/evidence ref remain distinct.

## 2. Governing objective

CP36 validates whether the completed V1 product remains responsive, bounded and recoverable under representative scale and failure conditions.

The checkpoint is **measurement-driven**. No FTS, index, cache, schema change, algorithm rewrite or architecture migration is allowed merely because a potential hot path is visible in source.

Production changes are authorized only after a reproducible measurement or reliability fixture demonstrates a material defect, and must be the smallest coherent correction.

## 3. Frozen product contracts

CP36 must preserve all CP20–35 meaning, including:

- stable catalog ID as final identity authority;
- search/category/UI never gaining identity authority;
- product schema 2 / receipt schema 1 unless an explicit migration necessity is demonstrated;
- CP27 comparison eligibility and single-basis semantics;
- CP28 evaluation thresholds;
- CP31/32 receipt-traceable detail semantics;
- CP33 review/provenance/save ordering;
- CP34 navigation meaning;
- CP35 safety conclusions and evidence limitations;
- offline/local OCR posture and forbidden permission boundary;
- programmatic `Activity + android.widget` architecture.

Performance work may alter *how efficiently existing facts are read*, but not what those facts mean.

## 4. Measurement layers

### A. Deterministic JVM structural scaling

Use test-only counting stores around frozen interfaces to measure operation amplification independently of runner speed.

Required workloads:

- CP29 text search at 1,000 and 10,000 catalog entries;
- CP29 recent/frequent build cost;
- CP27 price intelligence with long single-product history;
- CP31 Product Detail projection over long history;
- deterministic repeated recovery output.

Wall-clock values may be recorded, but deterministic call counts and result equality are the primary JVM evidence.

### B. Android runtime / SQLite measurement

Use a bounded emulator job and production SQLite implementations.

Required measurements:

- Home cold-launch `am start -W` samples;
- process PSS after Home idle;
- bundled Korean ML Kit OCR cold and warm latency on a synthetic receipt bitmap;
- actual SQLite CP29 search/recent at 1k and 10k catalog scale;
- CP27/CP31 long-history load at 1,000 observations;
- chart draw at the same history scale;
- product catalog migration 1 -> 2 with preserved rows/aliases;
- archive orphan/temp reconciliation and sampled image reopen;
- DB close/reopen persistence and deterministic failure/recovery behavior.

The emulator is evidence for relative/runtime behavior on the CI profile, not a claim about every physical phone.

## 5. Pre-declared budgets and decision rules

Shared hosted runners and emulators have variance. Therefore CP36 distinguishes **decision budgets** from gross CI safety ceilings.

### User-path decision budgets

- Home cold-launch median: <= 2,500 ms; no sample > 5,000 ms.
- Home idle PSS: <= 220 MiB on the CP36 emulator profile.
- OCR first pass: <= 5,000 ms.
- OCR warm median: <= 1,500 ms.
- CP29 SQLite exact search 1k: <= 750 ms.
- CP29 SQLite exact search 10k: <= 3,000 ms.
- CP29 SQLite recent 10k: <= 3,000 ms.
- CP27 + CP31 detail over 1,000 observations: <= 2,000 ms each measured user-facing load.
- 1,000-point chart draw: <= 500 ms.
- archive reconcile over ~2,000 files: <= 2,000 ms.
- product migration 1 -> 2 over 1,000 products/aliases: <= 5,000 ms.

### Scaling / amplification rules

A path is a material optimization candidate if any of the following is true:

1. it exceeds the relevant decision budget reproducibly;
2. 10k runtime is grossly super-linear relative to 1k without a semantic reason;
3. service-level call amplification creates O(N) per-item nested database reads large enough to dominate user latency;
4. memory growth is unbounded for a bounded-result user action;
5. a reliability fixture loses, duplicates, misattributes or makes authoritative data inconsistent.

A threshold miss does **not** automatically authorize a broad rewrite. First identify the dominant cost and choose the smallest correction.

## 6. Reliability vectors

Required bounded vectors:

- `PR-01` clean Home cold start;
- `PR-02` repeated Home start/stop without crash or leaked durable state;
- `PR-03` ML Kit synthetic receipt cold/warm processing;
- `PR-04` CP29 1k search correctness + cost;
- `PR-05` CP29 10k search correctness + cost;
- `PR-06` 10k recent/frequent correctness + bounded cost;
- `PR-07` 1,000-observation CP27/CP31 history correctness + cost;
- `PR-08` 1,000-point chart draw;
- `PR-09` product DB 1->2 migration preserves product/alias/link authority;
- `PR-10` unsupported migration remains fail-fast;
- `PR-11` archive reconcile removes orphan/temp files and preserves live files;
- `PR-12` receipt/image close/reopen/delete remains consistent;
- `PR-13` repeated recovery of identical input is deterministic;
- `PR-14` malformed/missing archive/record conditions fail safely rather than fabricating state.

## 7. Phase discipline

### Phase A — measurement-only

Allowed changes:

- CP36 planning/evidence documents;
- test-only JVM benchmark/reliability harness;
- Android instrumentation benchmark/reliability harness;
- CP36 workflow and measurement scripts;
- version bump.

Production Java, manifest and production resources remain frozen during Phase A.

### Phase B — measured hardening, only if required

If Phase A proves a material defect, first record:

- failing vector;
- exact metric or invariant;
- dominant cause;
- alternatives considered;
- why the proposed change is the smallest correction;
- regression that protects semantics.

Then permit only the specifically justified production files. Rerun the full Phase A measurement set after correction.

## 8. Acceptance criteria

CP36 may close only when:

- 1k/10k search has been actually measured before any FTS/index/cache decision;
- startup, OCR, memory, price/detail/chart, migration, archive and recovery evidence exists or a limitation is explicitly justified;
- any material budget miss is either corrected or explicitly accepted with evidence and product impact analysis;
- no optimization changes identity/price/review/provenance meaning;
- product schema 2 / receipt schema 1 remain unchanged unless migration need is separately proven;
- CP29–35 key regressions remain green;
- lint is clean;
- debug APK builds and forbidden permissions remain absent;
- post-green plan/code/evidence comparison is performed;
- exact executable HEAD/run/artifact/hash are frozen;
- handoff synchronization after freeze is documentation-only.

## 9. Non-goals

CP36 does not include:

- feature expansion;
- new cloud/network services;
- market price data;
- release signing;
- Compose/Material migration;
- premature FTS/index/cache introduction;
- private real-receipt publication;
- statistically representative device/OCR certification;
- arbitrary micro-optimization unrelated to a measured user path.

## 10. Stop condition

After CP36 acceptance/evidence and docs-only handoff synchronization, stop. Any post-V1 work requires a separately authorized next phase.
